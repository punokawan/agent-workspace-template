# {{TITLE}} — bug records

One file per bug: `YYYY-MM-DD-<slug>.md`. Write what a later agent needs to not repeat it.

```markdown
# <one-line symptom>

- **Found:** <date>, <where — repo, screen, endpoint>
- **Reproduce:** <steps or the failing command>
- **Cause:** <root cause, with file:line>
- **Fix:** <commit or branch>, verified by <command and its exit code>
- **Guard:** <the test or check that now fails if it comes back>
```
