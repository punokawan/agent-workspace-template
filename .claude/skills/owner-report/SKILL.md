---
name: owner-report
description: How to write an analysis, incident report or decision document for the project owner or other non-developers — format choice, a five-sentence opening, one plain diagram, a glossary, and technical detail kept in an appendix. Load before writing any report or explanation meant for someone who does not read code.
license: Proprietary
---

# Owner report

For analyses, incident reports and decision documents read by the owner or by non-developers.

## Format

Ask which format they want, unless they already said:

- **Markdown (`.md`)** — lives in the repository with history. Diagrams in Mermaid render on
  GitHub but not in every Markdown viewer.
- **A shareable page** (an artifact or HTML) — for reading once or sending by link; diagrams and
  charts render.

When unsure, suggest a page for a one-off report and Markdown for a document that must stay with
the code.

## Structure

1. **Summary** — at most five sentences, plain words: what happened, what it means for users or
   the business, and what the owner has to decide.
2. **One diagram** of the flow, the timeline or the options. Label boxes by what they mean for
   users or the business, not by code names; about seven boxes at most; colour for status (red
   broken, yellow degraded, green working). Draw charts of numbers to scale.
3. **The body** — the reasoning, in everyday words, with each unavoidable technical term
   explained once.
4. **Glossary** — every technical term the reader meets, in a line each.
5. **Developer appendix** — file paths, line numbers, commands and logs. Keep them out of the
   main text.

## Rules

- State what is verified and what is estimated; never round an estimate up to a fact.
- A decision needs options: give at least two, with what each costs and risks.
- Keep it as short as the decision allows.
