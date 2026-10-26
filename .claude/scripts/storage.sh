#!/usr/bin/env bash
# Disk-budget management for the studio workspace.
#   storage.sh report                    — where the bytes are + free-space verdict
#   storage.sh prune [--force]           — reclaim safe-to-delete artifacts
#   storage.sh link <project> <repo> <slug> — point a worktree's heavy dirs at shared cache
#   storage.sh doctor                    — verify no worktree holds real build artifacts
#
# Which directories are heavy, cacheable, or prunable comes from each repo's stack
# preset — this script hardcodes no repo and no toolchain.

source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

DANGER_FREE=$((15 * 1024 * 1024 * 1024))   # 15 GB
WARN_FREE=$((40 * 1024 * 1024 * 1024))     # 40 GB

cmd_report() {
  local free; free=$(free_bytes)
  echo "STUDIO DISK REPORT — $(date '+%Y-%m-%d %H:%M')"
  echo "==================================================="
  printf 'Free disk      : %s\n' "$(human "$free")"

  if   (( free < DANGER_FREE )); then printf 'Verdict        : \033[31mCRITICAL\033[0m — prune before starting new work\n'
  elif (( free < WARN_FREE  )); then printf 'Verdict        : \033[33mTIGHT\033[0m — worktree cap %s enforced\n' "$WT_CAP"
  else printf 'Verdict        : \033[32mHEALTHY\033[0m\n'; fi

  echo
  echo "--- Source checkouts ---------------------------------"
  while IFS='	' read -r p r reldir stack integ; do
    [[ -n "$p" ]] || continue
    [[ -d "$ROOT/$reldir" ]] || continue
    printf '  %-28s %8s  (%s)\n' "$p/$r" "$(du -sh "$ROOT/$reldir" 2>/dev/null | cut -f1)" "$stack"
  done < <(proj resolve all)

  echo
  echo "--- Heaviest artifacts (reclaimable) ----------------"
  local total=0
  while IFS='	' read -r p r path sub seed; do
    [[ -n "$p" ]] || continue
    local d; d="$ROOT/$(proj resolve "$p/$r" | cut -f3)/$path"
    [[ -e "$d" && ! -L "$d" ]] || continue
    local kb; kb=$(du -sk "$d" 2>/dev/null | cut -f1)
    total=$((total + kb))
    printf '  %-40s %8s\n' "$p/$r/$path" "$(human $((kb*1024)))"
  done < <(proj artifacts all)
  printf '  %-40s %8s\n' "TOTAL RECLAIMABLE" "$(human $((total*1024)))"

  echo
  echo "--- Shared cache (.cache) ---"
  if [[ -d "$CACHE_DIR" ]] && [[ -n "$(ls -A "$CACHE_DIR" 2>/dev/null)" ]]; then
    du -sh "$CACHE_DIR"/*/* 2>/dev/null | sed "s|$CACHE_DIR/|  |"
  else
    echo "  (empty)"
  fi

  echo
  echo "--- Worktrees (cap: $WT_CAP) ---"
  local n=0
  if [[ -d "$WT_DIR" ]]; then
    while IFS= read -r d; do
      [[ -n "$d" ]] || continue
      n=$((n+1))
      printf '  %-44s %8s  last-used %s\n' \
        "${d#"$WT_DIR"/}" "$(du -sh "$d" 2>/dev/null | cut -f1)" \
        "$(fmt_mtime "$d")"
    done < <(find "$WT_DIR" -mindepth 3 -maxdepth 3 -type d 2>/dev/null | sort)
  fi
  (( n == 0 )) && echo "  (none)"
  printf '  %d/%d slots used\n' "$n" "$WT_CAP"
}

cmd_prune() {
  local force="${1:-}"
  local before; before=$(free_bytes)
  info "pruning reclaimable artifacts (safe: all regenerable by a build)"

  local targets=()
  while IFS='	' read -r p r reldir stack integ; do
    [[ -n "$p" ]] || continue
    local d="$ROOT/$reldir"
    [[ -d "$d" ]] || continue
    local pd
    while IFS= read -r pd; do
      [[ -n "$pd" ]] || continue
      while IFS= read -r hit; do
        [[ -n "$hit" && ! -L "$hit" ]] || continue
        # A name match is not proof of a build folder: never delete anything git tracks.
        if [[ -n "$(git -C "$d" ls-files -- "${hit#"$d"/}" 2>/dev/null | head -1)" ]]; then
          warn "kept ${hit#"$ROOT"/} — it holds tracked source"; continue
        fi
        targets+=("$hit")
      done < <(find "$d" -maxdepth 2 -name "$pd" -type d -prune 2>/dev/null)
    done < <(proj field "$p" "$r" prune_dirs)
  done < <(proj resolve all)
  while IFS= read -r p; do [[ -n "$p" ]] && targets+=("$p"); done \
    < <(find "$ROOT" -name '.DS_Store' -type f 2>/dev/null)

  if (( ${#targets[@]} == 0 )); then ok "nothing to prune"; return; fi

  printf '%s\n' "${targets[@]}" | while read -r t; do
    printf '  %-8s %s\n' "$(du -sh "$t" 2>/dev/null | cut -f1)" "${t#"$ROOT"/}"
  done

  if [[ "$force" != "--force" ]]; then
    warn "dry run. re-run with --force to delete."
    return
  fi

  for t in "${targets[@]}"; do rm -rf "$t"; done
  local after; after=$(free_bytes)
  ok "reclaimed $(human $((after - before))) — free now $(human "$after")"
}

# Point a worktree's heavy dirs at the shared cache so it costs ~source size only.
# Symlinks are RELATIVE, so renaming the workspace root never dangles them.
cmd_link() {
  local project="${1:?project}" repo="${2:?repo}" slug="${3:?slug}"
  is_repo "$project" "$repo" || die "unknown repo: $project/$repo"
  local wt; wt="$(wt_path "$project" "$repo" "$slug")"
  [[ -d "$wt" ]] || die "no worktree at $wt"

  local gitdir excl
  gitdir="$(git -C "$wt" rev-parse --git-common-dir 2>/dev/null)" || gitdir=""

  while IFS='	' read -r p r path sub seed; do
    [[ -n "$p" ]] || continue
    local cache="$CACHE_DIR/$sub"
    mkdir -p "$cache" "$(dirname "$wt/$path")"
    [[ -e "$wt/$path" && ! -L "$wt/$path" ]] && rm -rf "$wt/$path"
    [[ -L "$wt/$path" ]] && rm -f "$wt/$path"
    python3 -c 'import os,sys; os.symlink(os.path.relpath(sys.argv[1], os.path.dirname(sys.argv[2])), sys.argv[2])' \
      "$cache" "$wt/$path"
    # A repo .gitignore usually has a DIRECTORY pattern (e.g. "/.next/"), which does not
    # match the symlink we just created — git would report it as untracked and block
    # `wt.sh land`. Exclude it worktree-locally instead of touching the repo's .gitignore.
    # NOTE: a linked worktree reads info/exclude from the COMMON git dir, not its own.
    if [[ -n "$gitdir" ]]; then
      excl="$gitdir/info/exclude"
      mkdir -p "$(dirname "$excl")"
      grep -qxF "/$path" "$excl" 2>/dev/null || echo "/$path" >> "$excl"
    fi
    ok "linked $path -> .cache/$sub"

    # Seed the cache from the main checkout when it is cold (e.g. node_modules).
    if [[ "$seed" == "seed" && -z "$(ls -A "$cache" 2>/dev/null)" ]]; then
      local main; main="$(repo_dir "$project" "$repo")/$path"
      if [[ -d "$main" && ! -L "$main" ]]; then
        info "seeding $path cache from the main checkout (one-time move)"
        rmdir "$cache" 2>/dev/null || true
        mv "$main" "$cache"
        python3 -c 'import os,sys; os.symlink(os.path.relpath(sys.argv[1], os.path.dirname(sys.argv[2])), sys.argv[2])' \
          "$cache" "$main"
        ok "main checkout now shares the same $path"
      fi
    fi
  done < <(proj artifacts "$project/$repo")
}

cmd_doctor() {
  local bad=0
  echo "STORAGE DOCTOR"
  echo "=============="
  while IFS= read -r wt; do
    [[ -n "$wt" ]] || continue
    local rel="${wt#"$WT_DIR"/}"
    local wproj="${rel%%/*}"; rel="${rel#*/}"
    local wrepo="${rel%%/*}"; local wslug="${rel#*/}"
    while IFS='	' read -r p r path sub seed; do
      [[ -n "$p" ]] || continue
      if [[ -d "$wt/$path" && ! -L "$wt/$path" ]]; then
        warn "$wproj/$wrepo/$wslug holds a REAL $path ($(du -sh "$wt/$path" | cut -f1)) — run: storage.sh link $wproj $wrepo $wslug"
        bad=1
      fi
    done < <(proj artifacts "$wproj/$wrepo" 2>/dev/null)
  done < <(find "$WT_DIR" -mindepth 3 -maxdepth 3 -type d 2>/dev/null)

  # A dangling cache symlink silently breaks every build in that worktree.
  local dangling=0
  while IFS= read -r l; do
    [[ -n "$l" ]] || continue
    [[ -e "$l" ]] || { warn "dangling cache symlink: ${l#"$ROOT"/} -> $(readlink "$l")"; dangling=1; bad=1; }
  done < <(find "$WT_DIR" "$PROJECTS_DIR" -maxdepth 5 -type l 2>/dev/null)
  (( dangling == 0 )) && ok "no dangling cache symlinks"

  local free; free=$(free_bytes)
  (( free < DANGER_FREE )) && { warn "free space $(human "$free") below 15 GB floor"; bad=1; }
  (( bad == 0 )) && ok "all worktrees share caches; disk within budget"
  return 0
}

case "${1:-report}" in
  report) cmd_report ;;
  prune)  shift; cmd_prune "${1:-}" ;;
  link)   shift; cmd_link "$@" ;;
  doctor) cmd_doctor ;;
  *) die "usage: storage.sh {report|prune [--force]|link <project> <repo> <slug>|doctor}" ;;
esac
