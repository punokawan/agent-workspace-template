#!/usr/bin/env bash
# Check that this machine can run the workspace, and say how to fix what is missing.
# Works on macOS, Linux, and Windows through WSL2 or Git Bash.
#   env.sh        — exit 1 when a required piece is missing
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
set +e

case "$(uname -s)" in
  Darwin) os=macos ;;
  Linux)  grep -qi microsoft /proc/version 2>/dev/null && os=wsl || os=linux ;;
  MINGW*|MSYS*|CYGWIN*) os=gitbash ;;
  *) os=unknown ;;
esac
echo "ENVIRONMENT — $os ($(uname -s))"
echo "==========================================================="

FAIL=0
need() { # need <ok?> <what> <fix>
  if [[ "$1" == 1 ]]; then printf '  \033[32mOK\033[0m    %s\n' "$2"
  else printf '  \033[31mMISS\033[0m  %s — %s\n' "$2" "$3"; FAIL=1; fi
}
want() {
  if [[ "$1" == 1 ]]; then printf '  \033[32mOK\033[0m    %s\n' "$2"
  else printf '  \033[33mWARN\033[0m  %s — %s\n' "$2" "$3"; fi
}
has() { command -v "$1" >/dev/null 2>&1 && echo 1 || echo 0; }

install() { # install hint per platform: <brew name> <apt name> <windows name>
  case "$os" in
    macos)     echo "brew install $1" ;;
    linux|wsl) echo "sudo apt install $2 (or your distro's package)" ;;
    gitbash)   echo "install $3, then reopen Git Bash" ;;
    *)         echo "install $1" ;;
  esac
}

need "$(( BASH_VERSINFO[0] >= 3 ))" "bash ${BASH_VERSION%%(*}" "$(install bash bash 'Git for Windows')"
need "$(has git)" "git" "$(install git git 'Git for Windows')"
need "$(has python3)" "python3" "$(install python3 python3 'Python 3, and make python3 resolve (an alias to py -3)')"

# Skills reach Codex through .agents/skills, a symlink. Windows checks links out as plain
# text files unless symlinks are enabled before cloning.
link_ok=0; [[ -L "$ROOT/.agents/skills" && -d "$ROOT/.agents/skills" ]] && link_ok=1
if [[ "$os" == gitbash ]]; then
  fix="turn on Windows Developer Mode, run 'git config --global core.symlinks true', export MSYS=winsymlinks:nativestrict, then clone again — or use WSL2"
else
  fix="re-create it: ln -s ../.claude/skills .agents/skills"
fi
need "$link_ok" "symlinks (.agents/skills -> .claude/skills)" "$fix"

want "$(has node)" "node (Ponytail plugin hooks)" "$(install node nodejs 'Node.js LTS')"
want "$(has gh)" "gh (GitHub CLI, for pull requests)" "$(install gh gh 'GitHub CLI')"
agent=0; [[ "$(has claude)" == 1 || "$(has codex)" == 1 ]] && agent=1
want "$agent" "an agent CLI (claude or codex)" "install Claude Code or Codex"

# Stack toolchains, only for stacks a registered project uses.
while IFS='	' read -r p r reldir stack integ; do
  [[ -n "$p" ]] || continue
  case "$stack" in
    go)     want "$(has go)" "go (for $p/$r)" "$(install go golang-go 'Go from go.dev')" ;;
    nextjs) want "$(has npm)" "npm (for $p/$r)" "$(install node nodejs 'Node.js LTS')" ;;
    flutter)
      want "$(has flutter)" "flutter (for $p/$r)" "install Flutter from flutter.dev"
      [[ -f "$ROOT/$reldir/.fvmrc" ]] && want "$(has fvm)" "fvm (for $p/$r, pinned in .fvmrc)" \
        "install fvm (https://fvm.app), then run 'fvm install' in the repo" ;;
  esac
done < <(proj resolve all 2>/dev/null)

free=$(free_bytes)
want "$(( free > 15*1024*1024*1024 ))" "free disk $(human "$free")" "below 15 GB — run: bash .claude/scripts/storage.sh prune"

echo
if (( FAIL )); then echo "VERDICT: MISSING REQUIREMENTS"; exit 1; fi
echo "VERDICT: READY"
