# The Campaign Brief

Write one before every launch. It fixes the decisions the weekly operating check later grades: what counts as success, what the budget has to buy, and who acts on a lead. Write MISSING for any input you don't have and list it under open decisions; never estimate it.

## Template

```
Campaign name:     [Platform]_[Objective]_[Audience]_[Offer]_[Date]  (naming convention in SKILL.md)
Objective:         [one measurable outcome, e.g. 50 sales-qualified leads from accounts above a deal size]
Budget:            [amount per month] for [duration]; testing or scaling phase
Channels:          [platforms, placements, formats]
Audience:          [ICP; job titles, firmographics or interests; exclusions]
Offer:             [what the ad promises, and the landing page that keeps the promise]
Conversion:        [primary conversion action, how it is tracked, attribution window]
Targets:           [break-even CPA or CPL from deal math; target ROAS; payback limit]
Success metrics:   Primary: [e.g. cost per qualified lead below target]
                   Secondary: [e.g. lead-to-SQL rate, click-through to page]
Kill / scale rule: [the account's own rule, with the sample size and lag it waits for]
Lead handling:     [qualification criteria, routing, follow-up time, owner]
CRM setup:         [campaign ID, lead-source fields, offline conversion import]
Pre-launch:        [checklist status: test conversion seen, page speed, UTMs]
Open decisions:    [every MISSING input]
```

Derive the targets from the business, not from platform averages: breakeven CPL and CPC in [b2b-paid-playbook.md](b2b-paid-playbook.md), the payback gate in [payback-period.md](payback-period.md). Lead qualification, routing, and follow-up times belong to the **revops** skill; the brief only records what was agreed.

## Launch deliverables

Hand these over with the brief:

| Deliverable | Contents |
|---|---|
| Campaign architecture | Campaigns, ad sets or ad groups, naming, budget split between testing and scaling |
| Audience brief | Primary audiences, lookalike seeds, retargeting segments, and exclusions per platform |
| Ad copy set | Variants per format and placement from the **ad-creative** skill, checked against character limits |
| Pre-launch checklist | The universal checklist in SKILL.md plus the platform list in [platform-setup-checklists.md](platform-setup-checklists.md) |
| Weekly check | The inputs and calls in [operating-check.md](operating-check.md), set up before the first week ends |
