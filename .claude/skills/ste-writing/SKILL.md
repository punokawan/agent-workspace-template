---
name: ste-writing
description: Write briefs, agent instructions, technical documents and every report in a controlled style based on ASD-STE100 Simplified Technical English — one instruction or fact per sentence, short active sentences, one word for one meaning, conditions before actions, exact values verbatim. Covers agent dispatch briefs, AGENTS.md and skill text, runbooks, task docs, review findings, agent reports and HANDOFFs, status reports to the owner (English and Indonesian), commit messages and PR descriptions. Load before you write or review any of those. Not for user-facing UI copy (use copywriting) and not a licensed copy of the ASD-STE100 specification.
license: MIT
---

# STE writing for briefs and documents

Text that an agent or an engineer acts on must have one reading. These rules adapt the
principles of ASD-STE100 Simplified Technical English (STE) to agent briefs and engineering
documents. They are a house style, not the official specification. For formal STE
compliance, get the specification from the ASD-STE100 maintenance group and use its
dictionary.

## When to use it

| Text | Use this skill |
|---|---|
| Agent dispatch briefs, SendMessage fix rounds, review requests | Yes |
| AGENTS.md, skills, agent definitions, commands | Yes |
| Runbooks, task docs, PLAN/TASK files written in English | Yes |
| Review findings, handoffs, commit messages, PR descriptions | Yes |
| UI copy, toasts, emails a user reads | No: use `copywriting` and the project's copy overlay |
| Agent reports, HANDOFF blocks, status reports to the owner | Yes: section 8 |
| Indonesian documents and reports | Apply the principles (sections 1–4 and 8); the word list in section 5 is English only, section 8 has the Indonesian one |

## 1. Sentences

- **One instruction per sentence.** "Run the tests. Then run lint." Not "Run the tests and lint,
  then fix anything that fails and report back."
- **Instructions are imperative.** "Add the guard." Not "The guard should be added" or "You may
  want to add the guard."
- **Put the condition first, then the action.** "If the claim count is 0, return the refusal."
  The reader knows when the action applies before they read it.
- **Keep sentences short.** Procedure sentences: at most about 20 words. Descriptive sentences:
  at most about 25 words. If a sentence needs "and", "which" or a semicolon twice, split it.
- **Use the active voice.** "The webhook writes the row." Not "The row is written by the webhook."
  Name the actor; a passive sentence hides who does the work.
- **One topic per paragraph.** A paragraph has at most about six sentences.
- **Give the reason after the rule, in its own sentence.** "Never write a cancel for a 412.
  Midtrans returns 412 when the payment already settled."

## 2. Words

- **One word for one meaning, every time.** If the brief says "claim", do not later say "lock",
  "reserve" or "take" for the same step. Define a term once, then repeat it exactly.
- **One meaning for one word.** Do not use "check" for both "read a value" and "refuse when a
  value is wrong". Say "read" and "refuse".
- **Prefer short, common words** (section 5). Technical names (file paths, function names,
  table names, flags, status values) are allowed and must be exact.
- **No vague quantities.** Not "a few", "some", "soon", "large". Write the number, the limit or
  the date: "at most 3 retries", "≤ 300 lines", "2026-11-04".
- **No hedges in binding text.** "Should", "might", "consider", "ideally" make a rule optional.
  For a rule, write "do", "must" or "never". For a real option, say so: "Optional: …".
- **Spell out negatives once.** "Do not touch payment-admin.ts." Not "Avoid touching files
  outside scope where possible."

## 3. Structure

- **Number the steps** when order matters. One action per step. Put the expected result of a
  step in the same item: "Run `npm test -- refund`. Expect exit 0."
- **Use a table** for anything compared across rows: files and owners, options and costs,
  findings and severity.
- **Lead with the goal.** The first sentence says what "done" means.
- **Put exact values verbatim** (strings, messages, numbers, signatures) in code format, and
  say "verbatim". Never paraphrase a value the reader must reproduce.
- **Keep warnings separate** and before the step they protect: "Warning: this writes to
  production. Do not run it without `--apply` approval."
- **Cite, don't paste.** Point to `path:line`. Paste an excerpt only when the exact text matters.

## 4. Briefs for agents

A dispatch brief is a procedure. Write it in this order:

1. **Goal**: one sentence that states the definition of done.
2. **Read first**: the paths, in reading order.
3. **Rulings**: numbered, one decision each. Mark owner decisions with their date.
4. **Scope**: the files the agent may change, and the files it must not change.
5. **Contract**: what the agent must never do (commit, push, DB, subagents), in short negatives.
6. **Run**: the exact commands, one per line or step.
7. **Return**: what to write to the report file and what to return in the message.

Rules for briefs:

- Write each ruling so that a reviewer can mark it ✅ or ❌ without asking.
- State the stop condition: "If the change needs a file outside this list, stop and report."
- When a value comes from an earlier task, name the source: "use the helper Task 6.3 added
  (`addCommunityCalendarMonths`)".
- Do not paste the conversation history. Give the decisions, not the discussion.

## 5. Word choices

Use the word in the right column. The left column has more than one meaning, is longer than
needed, or hides the action.

| Instead of | Write |
|---|---|
| utilize, leverage | use |
| ensure, make certain | make sure (or state the check: "assert that …") |
| verify (as a loose instruction) | test, read and compare, or run `<command>` |
| facilitate, enable | let, allow |
| perform, conduct, carry out | the verb itself: run, test, write |
| in order to | to |
| prior to | before |
| subsequent to, following | after |
| in the event that | if |
| at this point in time | now |
| a number of | the number: 3, 12 |
| approximately | about (and give the value) |
| terminate | stop, end |
| commence, initiate | start |
| obtain, acquire | get |
| modify, amend | change |
| eliminate | remove |
| implement (a fix) | add, change, or write (say which) |
| handle (an error) | catch, log, return, retry (say which) |
| deal with, take care of | the exact action |
| appropriate, proper | the actual rule ("≤ 300 lines", "status pending") |
| simply, just, obviously | delete the word |
| etc., and so on | list every item, or write "for example" before a partial list |
| it, this, that (unclear) | repeat the noun |

## 6. Review checklist

Read the text once with these questions:

- [ ] Does the first sentence state the goal or the result?
- [ ] Does each sentence carry one instruction or one fact?
- [ ] Is every instruction imperative and active, with the condition first?
- [ ] Is every binding rule free of "should", "might", "consider", "ideally"?
- [ ] Does each term keep one meaning, and each meaning one term?
- [ ] Are numbers, limits, dates, paths and messages exact and verbatim?
- [ ] Are steps numbered where order matters, one action each, with the expected result?
- [ ] Is every pronoun's noun clear from its own sentence?
- [ ] Can a reviewer mark each ruling ✅ or ❌ without asking?

## 7. Before and after

Before:
> You should probably make sure the webhook handles refunds properly, and it might be a good
> idea to also look at the cron so it doesn't do anything weird when Midtrans is slow.

After:
> 1. The webhook writes status from the Midtrans re-fetch only. It never writes status from the
>    request body.
> 2. If the re-fetch times out, return 500. Do not write any row.
> 3. Apply the same rule to the cron sync in `src/lib/cron-payment-check.ts`.
> 4. Run `npm test -- payment-notification-route cron-payment-check`. Expect exit 0.

Before:
> This basically ensures that RT data gets utilized correctly across the various flows etc.

After:
> `applyEffectiveTier` writes the same tier and status to the community and to its RT.
> Downgrade, expiry and refund all call it.

## 8. Reports

Every report uses this style: agent reports and HANDOFFs, review results, and status reports
to the owner in any language. A report is read to decide the next action. Make that fast.

Order:

1. **Status line first**: the result in one sentence. "Phase 5 landed on local codex as
   `1444b081`. Not pushed." Not a greeting, not a recap of the request.
2. **Evidence**: what was run and its result, with exit codes or counts. "Verify --full: PASSED."
3. **What changed**: one fact per bullet, grouped by who it affects.
4. **Open items**: decisions the reader must make, risks, deferred work. Each one with the
   options or the next step.
5. **Next step**: one sentence. Ask one direct question when the reader must decide.

Rules:

- **One fact per bullet or sentence.** If a bullet needs "and" to join two facts, split it.
- **Numbers, not adjectives.** "174 tests pass", "9.25 of 10 GB". Not "many tests", "almost full".
- **Mark evidence.** Say what is verified and what is estimated or unverified, in the sentence
  that makes the claim.
- **Use a table** when three or more items share the same fields (task, status, file, result).
- **No filler.** No restating the question, no "as requested", no closing summary of the summary.
- **Paths, commands and IDs in code format.** Give the exact command the reader runs.
- **Keep the reader's language.** The rules apply the same in English and Indonesian.

Indonesian reports — word choices (same principle as section 5):

| Hindari | Tulis |
|---|---|
| sepertinya, kayaknya, mungkin (untuk fakta) | tulis faktanya, atau "belum terverifikasi: …" |
| pada dasarnya, sebenarnya, intinya | hapus |
| beberapa, banyak, sedikit | angkanya: 3, 12, 9,25 GB |
| sudah dilakukan pengecekan | sudah dicek (aktif, sebut pelakunya bila perlu) |
| dalam rangka, guna | untuk |
| melakukan perubahan pada | mengubah |
| terkait dengan hal tersebut | sebut nomornya: "terkait poin 2" |
| akan segera | tanggal atau urutan: "setelah review selesai" |
| dsb., dll. | sebut semua, atau "misalnya" sebelum daftar sebagian |
| ini, itu (tidak jelas) | ulangi kata bendanya |

Example (Indonesian status report):

> Task 6.1 selesai. 156 test lulus, lint dan tsc exit 0.
> - Voucher yang kuotanya habis tetap mengaktifkan paket. `usedCount` tidak melewati `maxUsage`.
> - Kelebihan dicatat di metadata pembayaran dan dikirim sebagai alert setelah commit.
> - Belum terverifikasi: race di Postgres nyata. Dicakup Task 7.2.
>
> Berikutnya: review akhir Phase 6.
