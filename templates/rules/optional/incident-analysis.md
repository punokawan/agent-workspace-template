## Incident analysis

For an error, a log, or a limit that was reached (quota, rate limit, storage), answer in order:

1. What the system did, as observed.
2. The root-cause hypothesis.
3. The steps that confirm or reject it.
4. The fix and why — it removes the cause and handles what breaks while the failure lasts, not
   only the symptom.

Label every claim verified or estimated, with its evidence (code, log, commit, data), and say
what is still unverified and how to check it. For capacity, give the limit, the real usage, the
estimate after the fix, and the headroom left.
