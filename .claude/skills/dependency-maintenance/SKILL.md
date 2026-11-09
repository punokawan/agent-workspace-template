---
name: dependency-maintenance
description: How to safely update dependencies and SDK versions in any project, per stack — Flutter SDK via FVM, Dart pub packages, Android/iOS platform layers, Go modules, and Next.js/npm packages — and a structured process for triaging and fixing breakage after each update step.
license: MIT
compatibility: Flutter (FVM), Dart pub, Go modules, npm, Android Gradle, iOS CocoaPods
---

# Dependency Maintenance

Updates are done **incrementally** — one layer at a time, with a verify step between each layer.
All edits happen in a worktree (`/wt-start`), never in `projects/<project>/<repo>/`.

## Source of truth — read before acting

1. `bash .claude/scripts/project.sh show <project>` — which repos and stacks are in scope
2. `projects/<project>/AGENTS.md`, then `projects/<project>/<repo>/AGENTS.md` if present
3. `projects/<project>/**/.claude/skills/<project>-dependencies/SKILL.md`, only if it exists — pinned versions, make
   targets, project-only risky packages, local patches (e.g. `example-dependencies`)
4. The real version files: `.fvmrc` / `.fvm/fvm_config.json`, `pubspec.yaml`,
   `android/build.gradle`, `android/app/build.gradle`, `ios/Podfile`, `go.mod`, `package.json`

Never quote a version from memory or from a doc — read the file. Overlay and project rules win.

Commands below use the plain toolchain. Where a repo has wrappers (e.g. `$CODEGEN` for
codegen, `$TEST` for tests), use the wrapper the overlay names.

```bash
CODEGEN="fvm dart run build_runner build --delete-conflicting-outputs"
TEST="fvm flutter test"
```

---

## Golden Rule: One Layer at a Time

```
Flutter SDK → verify → Dart packages → verify → codegen → verify → platform layers → verify
Go toolchain → verify → Go modules → verify
npm patch/minor → verify → npm majors one at a time → verify
```

Never upgrade Flutter SDK + packages + Android SDK in the same session. Each layer can break independently; mixing them makes root-cause analysis impossible.

---

## Layer 1: Flutter SDK Upgrade

Flutter SDK is managed via FVM. Never run `flutter upgrade` — it bypasses FVM.

### Check what's available

```bash
fvm releases         # all releases
fvm list             # installed versions
```

### Strategy: stable channel only

Target the **latest stable** release on the Flutter stable channel. Never use `beta` or `master` in production.

```bash
fvm install <new-version>          # e.g. fvm install 3.45.0
fvm use <new-version>              # updates .fvm/fvm_config.json
```

### After Flutter SDK upgrade — verify checklist

```bash
# in the worktree: .wt/<project>/<repo>/<slug>
# 1. Sync dependencies with new Flutter
fvm flutter pub get

# 2. Analyze — catch any API-level breaks immediately
fvm flutter analyze

# 3. Run unit tests
$TEST

# 4. Check codegen still works (new Flutter may change generated output)
$CODEGEN
fvm flutter analyze
```

### Common Flutter SDK upgrade breakage

| Symptom | Cause | Fix |
|---|---|---|
| `The argument type 'X' can't be assigned to 'Y'` | Flutter renamed or re-typed an API | Update call sites to new signature |
| `deprecated: use X instead` | Flutter deprecated a widget/method | Migrate to the new API; treat as error if `--fatal-deprecations` is in CI |
| `pub get` fails with constraint conflict | A package hasn't updated its Flutter SDK constraint yet | Pin that package to a known-compatible version or check for a pre-release |
| Generated `.g.dart` files have errors | build_runner needs a version bump after SDK upgrade | `fvm flutter pub upgrade build_runner freezed` then re-run codegen |
| `Missing concrete implementation` on sealed classes | Dart added a new case to a Flutter sealed type | Add the case to every `switch`/`when` |

---

## Layer 2: Dart Package Upgrades

### Step 1: See what's outdated

```bash
fvm flutter pub outdated
```

Output columns: **current** | **upgradable** (respects constraints) | **resolvable** | **latest**

Read this carefully. The `resolvable` column shows what `pub upgrade --major-versions` would pick. The `latest` column shows what's actually on pub.dev.

### Step 2: Decide upgrade scope

Two modes — choose based on risk tolerance:

**Conservative (patch/minor only)** — safe for hotfix windows:
```bash
fvm flutter pub upgrade
```
Upgrades within existing `^` constraints. Rarely breaks anything.

**Aggressive (major versions)** — do this intentionally, not before a release:
```bash
fvm flutter pub upgrade --major-versions
```
This rewrites `pubspec.yaml` constraints to the latest. High risk — treat as a planned maintenance session.

### Step 3: Verify after pub upgrade

```bash
fvm flutter pub get
fvm flutter analyze
$CODEGEN            # regenerate freezed/json/objectbox after API changes
fvm flutter analyze     # re-analyze after codegen
$TEST             # run tests
```

### High-risk packages — extra care needed

These packages frequently introduce breaking changes or require platform-level changes:

| Package | Risk | Why |
|---|---|---|
| `objectbox` / `objectbox_flutter_libs` (if used) | **Critical** | Database schema changes require migration; `objectbox_generator` must match; run `$CODEGEN` after every objectbox upgrade |
| `firebase_core` + `firebase_*` | **Critical** | Firebase packages must all upgrade together — mismatched versions crash at init; check `firebase_core` compatibility matrix |
| `flutter_bloc` / `bloc` / `bloc_test` | **Medium** | All three must be version-compatible; `bloc_test` constraint changes often |
Project-only risky packages (IAP, auth plugins, local patches) are listed in the overlay.

### ObjectBox-specific upgrade procedure (apps that use ObjectBox)

ObjectBox upgrades are the most dangerous — wrong sequence can corrupt the local DB.

```bash
# 1. Upgrade objectbox and generator together
fvm flutter pub upgrade objectbox objectbox_flutter_libs

# 2. Re-run codegen — ObjectBox model changes require regenerating the Store
$CODEGEN

# 3. Check generated objectbox.g.dart for schema version bump
# If the schema version increased, a migration is needed for existing installs.
# Check ObjectBox migration docs before shipping.

# 4. Analyze + test
fvm flutter analyze
$TEST
```

### Firebase-specific upgrade procedure

Firebase packages share a BOM — they must all update together.

```bash
# Check which firebase_* packages are in pubspec.yaml first:
grep 'firebase_' pubspec.yaml

# Upgrade every firebase_* package the app uses, in one command:
fvm flutter pub upgrade firebase_core firebase_analytics ...   # the full set from the grep

# Verify FlutterFire compatibility table:
# https://firebase.flutter.dev/docs/overview#version-compatibility

fvm flutter pub get
fvm flutter analyze
```

If Firebase packages are incompatible with each other, `pub get` will error with the conflict. Pin all to the same compatible set.

### freezed / json_serializable codegen procedure

```bash
# Upgrade both runtime and generator together
fvm flutter pub upgrade freezed_annotation freezed json_serializable

fvm flutter pub get

# Full codegen rebuild — delete conflicting outputs is required
$CODEGEN

# Analyze — freezed changes sometimes alter generated APIs
fvm flutter analyze
```

---

## Layer 3: Codegen Packages (build_runner, objectbox_generator)

These are dev dependencies, but mismatches break the build pipeline.

```bash
fvm flutter pub upgrade build_runner <every *_generator in dev_dependencies>

$CODEGEN
fvm flutter analyze
```

---

## Layer 4: Android Platform Upgrade

### Kotlin version

`android/build.gradle` (or `settings.gradle`):
```groovy
id 'org.jetbrains.kotlin.android' version '<x.y.z>' apply false
```

Check the latest stable Kotlin version at kotlinlang.org. Update the version string, then
`fvm flutter build apk --debug` to verify Android builds.

### Android SDK levels (compileSdk / targetSdk / minSdk)

`android/app/build.gradle`. Google Play requires targeting the latest SDK within a year of release.
Read the current values from the file. **Never lower `minSdk`** without checking the overlay —
plugins such as biometrics set a floor.

When bumping `targetSdk`:
1. Read the Android behavior changes for that API level
2. Search the codebase for any APIs that changed: `grep -r "targetSdkVersion\|Build.VERSION" lib/`
3. Build a debug APK: `fvm flutter build apk --debug`
4. Test on a physical device or emulator running the new API level

### AGP (Android Gradle Plugin)

`android/build.gradle` / `settings.gradle` — update `com.android.tools.build:gradle` version. Always check the AGP/Kotlin compatibility matrix before changing both in the same session.

### desugar_jdk_libs

`android/app/build.gradle`:
```groovy
coreLibraryDesugaring 'com.android.tools:desugar_jdk_libs:<x.y.z>'
```

Update when bumping AGP — they are typically released together.

---

## Layer 5: iOS Platform Upgrade

### Deployment target

Set in both `ios/Podfile` and `Runner.xcodeproj` — read both; they must agree.

Apple raises the minimum OS requirement for App Store submissions periodically. When bumping:

1. Update `ios/Podfile`:
   ```ruby
   platform :ios, '14.0'
   ```

2. Update `Runner.xcodeproj` → `IPHONEOS_DEPLOYMENT_TARGET` in all build configurations (Debug, Profile, Release).

3. Re-run CocoaPods:
   ```bash
   cd ios && pod install
   ```

4. Build for iOS simulator: `fvm flutter build ios --simulator`

### CocoaPods update

```bash
cd ios
pod update          # updates all pods to their latest compatible version
pod install         # install resolved versions
```

Then build: `fvm flutter build ios --simulator`

---

## Layer 6: Go Backend Updates

### Go version

The `go` directive in `go.mod`. Read it; do not assume.

To upgrade Go version:
1. Install the new Go toolchain on the machine
2. Update `go.mod`: `go mod tidy` (or manually edit the `go` directive)
3. Run: `go build ./...` and `go vet ./...`

### Go module updates

```bash
# in the worktree
# See what's outdated
go list -m -u all 2>/dev/null | grep '\['

# Conservative: update patch/minor versions
go get -u=patch ./...
go mod tidy

# Or update specific packages:
go get <module>@latest
go mod tidy

# Verify
go build ./...
go vet ./...
```

### High-risk Go packages

| Package | Risk |
|---|---|
| `gorm.io/gorm` + `gorm.io/driver/postgres` | Must upgrade together; GORM breaking changes are rare but impactful |
| `github.com/golang-jwt/jwt` | Note: v3 uses `+incompatible`; v4/v5 have module paths like `golang-jwt/jwt/v4` — a version jump changes the import path everywhere |
| `golang.org/x/crypto` | Upgrade eagerly — CVEs appear here frequently |
| `google.golang.org/api` | Updates frequently; rarely breaks, but check CHANGELOG |

---

## Layer 7: Next.js / npm Updates

```bash
# in the worktree
npm outdated
npm update                      # patch/minor within ranges
npm install <pkg>@latest        # one major at a time, then verify
npm audit --omit=dev            # CVEs in shipped code
```

| Package | Risk | Why |
|---|---|---|
| `next` + `react` + `react-dom` + `eslint-config-next` | **Critical** | Move together; read the Next.js upgrade guide; hosting may block vulnerable `next` builds |
| `@supabase/*` | **High** | Auth/session API changes; regenerate DB types after |
| `typescript`, `@types/*` | **Medium** | New strictness surfaces as `tsc` errors |
| `tailwindcss`, shadcn/ui deps | **Medium** | Config format changes between majors |

Verify each step: `npx tsc --noEmit`, lint, `next build`.

---

## Post-Update Verification Checklist

Run the repo's own checklist from the overlay if it has one, then the gate:

```bash
bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --full
```

For Flutter, also build both platforms once: `fvm flutter build apk --debug` and
`fvm flutter build ios --simulator` — `verify.sh` does not.

---

## Triaging Breakage After an Update

### Identify the source

```bash
fvm flutter analyze 2>&1 | head -50
# or for backend:
go build ./... 2>&1 | head -50
```

Work top-down — the first error often cascades into many others. Fix the root error first.

### Common error patterns and fixes

**`Undefined name 'X'`**
The package renamed or removed `X`. Check the package's CHANGELOG or migration guide on pub.dev.

**`Too many positional arguments` / `No named parameter 'X'`**
A constructor or method signature changed. Read the new API signature in the package source or pub.dev docs.

**`The method 'X' isn't defined`** on a type you use
Extension method was removed or moved to a different type. Check the upgrade guide.

**`type 'X' is not a subtype of type 'Y'`** at runtime (not analyze)
Usually a platform channel type mismatch — common with `permission_handler`, `local_auth`, `google_sign_in`. Read the package's migration guide for the version you jumped to.

**Build runner fails with conflicting outputs**
```bash
fvm flutter pub run build_runner clean
$CODEGEN
```

**ObjectBox generator fails after upgrade**
The `objectbox` and `objectbox_generator` versions must match. Check `pubspec.yaml` — if one was upgraded without the other, align them.

**iOS build: CocoaPod version conflict**
```bash
cd ios && pod deintegrate && pod install
```

**Android build: `Duplicate class` or `Manifest merger failed`**
Usually a dependency bringing in a conflicting version of an AndroidX library. Run:
```bash
fvm flutter build apk --debug 2>&1 | grep "Duplicate class\|Manifest"
```
Fix by forcing resolution in `android/app/build.gradle`:
```groovy
configurations.all {
    resolutionStrategy {
        force 'androidx.core:core-ktx:<x.y.z>'
    }
}
```

**`package_info_plus` returns null after upgrade**
Requires `android:label` set in `AndroidManifest.xml` — verify it's present.

**`firebase_*` crash at startup after upgrade**
The `google-services.json` (Android) or `GoogleService-Info.plist` (iOS) may need regenerating if the Firebase project config changed. Also verify all `firebase_*` packages are on mutually compatible versions.

---

## Scheduling Maintenance

| Trigger | Action |
|---|---|
| Flutter stable release | Upgrade Flutter SDK (Layer 1 + 2) |
| Firebase CVE or major release | Upgrade all `firebase_*` together |
| Google Play policy deadline | Bump `targetSdk` to required level |
| `golang.org/x/crypto` CVE | Upgrade immediately (`go get -u golang.org/x/crypto`) |
| Regular cadence (monthly) | `fvm flutter pub outdated` / `go list -m -u all` / `npm outdated`, upgrade conservative packages |
| `next` security advisory | Upgrade `next` to the patched release |
| Pre-release | Run full post-update checklist above |

---

## What NOT to do

- **Do not** run `flutter upgrade` — bypasses FVM, corrupts the pinned version
- **Do not** upgrade ObjectBox without running codegen immediately after — stale codegen will crash at runtime
- **Do not** mix Flutter SDK + major package upgrades in one session — impossible to bisect
- **Do not** upgrade Firebase packages individually — they must move together
- **Do not** lower `minSdk` or bypass a local patch package — see the project overlay
- **Do not** land an update without `verify.sh --full` exiting 0
