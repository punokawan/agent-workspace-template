## Capacity review

Before a change adds load to a metered or free-tier service — requests, scheduled jobs, queries,
writes, storage, messages:

- Show, per service: the limit (and the date it was checked in the provider's docs), the real
  current usage read from its dashboard (date and source), the estimated added load, and the
  total after the change as a share of the limit.
- When you cannot read real usage, say so and ask the owner; never present an estimate as real
  usage.
- The owner approves the load, not only the feature. Above 50% of any limit after the change
  needs a stated fallback.
- Record the limits, the usage and each feature's load in the project's docs in the same change.
