---
description: Reclaim regenerable build artifacts across every project's repos — dry run by default, requires explicit confirmation to delete
allowed-tools: Bash(bash .claude/scripts/storage.sh:*), Read, Skill, AskUserQuestion
---

Reclaim disk space. Scope: $ARGUMENTS (empty = all repos).

## Procedure — do not skip steps

1. Load the `storage-management` skill and read its **Safe-to-delete inventory** and
   **Never auto-delete** lists.
2. Run the dry run and show the user the real output:
   ```bash
   bash .claude/scripts/storage.sh prune
   ```
3. Check for in-flight builds before deleting:
   ```bash
   pgrep -fl 'flutter|dart|next|node|go build' || echo "no builds running"
   ```
   If a build is running, **stop** and tell the user — pruning mid-build corrupts the cache.
4. Ask the user to confirm the deletion, quoting the total reclaimable size from step 2.
   Deleting build caches is destructive to build state (not to source), so never skip this.
5. On confirmation only:
   ```bash
   bash .claude/scripts/storage.sh prune --force
   ```
6. Report the **measured** reclaimed delta the script printed, plus the new free-space verdict.

## After pruning

Tell the user which commands they will need to re-run before their next build:
- Flutter repos → `fvm flutter pub get` (and `pod install` if `ios/Pods` was removed)
- Node/Next.js repos → `npm install`

Name the exact `projects/<project>/<repo>/` paths the script pruned.

Never delete anything on the "Never auto-delete" list, even if the user asks broadly for
"clean everything" — name those files and ask separately.
