---
name: vault-checkpoint
description: >-
  Close a working session, or checkpoint after a single task, so the next
  session can pick up cold without losing a decision. Use when the user says
  "close the session", "checkpoint", "wrap up", "save state", "I'm done for
  today", when a task finishes, or when context is about to run out. Runs the
  seven-step routine: Current-State, LOG, index, lessons, private journal,
  clean working tree, and evidence. Do NOT use it to audit vault health (that
  is vault-lint) or to initialise a vault (that is vault-bootstrap).
---

# Checkpoint a session

## Why after every task, not just at the end

Long sessions die without warning: compaction, token limits, a model change. A
checkpoint that only runs "at the end" is a checkpoint that often never runs.

Run the full routine at the end of a session, and a reduced version after
**each** task.

## Before anything: get today's date

**Never take the date from the prompt, a filename, or memory.** Run the system
date command in the first turn that is going to write anything dated: a file in
`90-Raw/`, a LOG entry, an `updated:` field, a note in an external system.

A prompt written on Friday and executed on Monday is a stale clock. A long run
with retries can cross midnight mid-execution, so on a long session run it
again before stamping any new snapshot.

```bash
date +%Y-%m-%d
```

## The seven steps

### 1. `Current-State.md` reflects reality

Present tense only: milestone, what closed, what is in flight, what is blocked
**and with what diagnostic suspicion**, visible debt, risks.

It must end with a **"NEXT SESSION"** section: what comes next, in what order,
and **which decisions are waiting on the human**, listed explicitly. An agent
starting cold, possibly a different model, has to continue from
`CLAUDE.md → Current-State.md` alone without losing a decision.

Stay under the 2,500 token ceiling. If you catch yourself narrating *how* the
project got here, that belongs in the LOG.

Record blockers with their suspicion, not just their existence. "Hangs;
suspicion: resource contention; next step: X" means the next session starts
investigating instead of rediscovering.

### 2. `LOG.md`

One entry per operation this session, newest at the top:

```
## [YYYY-MM-DD] op | short title
What happened, decisions made, pointers.
```

If the LOG passed its ceiling, rotate it (see `vault-lint`).

### 3. `00-Index.md`

Update it if pages were created, moved, or re-described.

### 4. `Lecciones.md`

**If the session paid for a lesson, write it before closing.** A lesson that
does not get written gets paid for again.

Each entry is an actionable rule with its reason: never X, on this date it
caused Y, do Z instead. This file is overwritten and refined, not appended to:
a lesson that turns out to be incomplete gets corrected on the spot.

### 5. Private journal

If the project uses one, add a raw entry. It never goes to the repo. The curated
LOG entry can be distilled from it later.

### 6. Clean working tree

Descriptive commit and push. Nothing stays uncommitted unless the human
explicitly decides so, and then it is noted in `Current-State.md` as WIP.

In a multi-axis repo, stage only the axis you worked on. Files another axis left
modified are not yours to commit.

### 7. Nothing is reported as finished without evidence

Green gates, or reviewable artefacts. Anything unverified is marked "pending
sign-off", without embarrassment.

**And evidence only counts if the instrument is validated.** A green result from
a suite with no control case proves nothing (VAULT-STARTER §8.5). Before
reporting a measurement, ask whether the instrument would have detected the
failure had it occurred.

## The reduced version, after each task

Steps 1, 2 and 6. Thirty seconds. It is what makes the difference between losing
one task and losing a session.

## Anti-goals

- **Do not write history into `Current-State.md`.** It is the present. The LOG
  is the past.
- **Do not summarise when archiving.** Rotating a LOG preserves it verbatim;
  summarising destroys exactly the detail it exists for.
- **Do not mark something ratified because the human liked it in chat.**
  Ratification is explicit or it is not ratification. Ask, and record it with a
  date.
- **Do not commit another axis's changes** to tidy the working tree.
- **Do not close with a lesson unwritten.** That is the one step whose cost is
  invisible today and certain later.
