## Commit discipline

Other agents may be committing to the same repositories at the same time.

- Stage only your own change, by explicit path. Never `git add -A` or `git add .`; leave files
  you did not change alone and mention them.
- Never rewrite history that is pushed or shared: no rebase, amend, squash or force-push of
  those commits.
- One commit per finished, coherent change — the code, its tests and its docs together.
- Keep binaries small or out of git: screenshots as compressed JPEG, no videos or large exports.
