---
name: example-copywriting
description: Example project-level skill (reference only). Shows where a project's voice and terms live when they apply to every repo in that project. Load with the shared copywriting skill when writing text for the Example project.
---

# Example — copy voice

A project-level skill lives in `projects/<project>/.claude/skills/` because it applies to every
repo of that project and may carry project data. Keep shared rules in the workspace
`copywriting` skill; put only this project's choices here.

- Voice: short and calm. "Booking confirmed", never "Yay, you're booked!".
- Use the terms in the project `AGENTS.md` vocabulary exactly: Slot, Booking.
