---
name: vault-bootstrap
description: >-
  Initialise an AI-directed Vault in a repository from VAULT-STARTER.md, or add
  a new axis to a repo that already has one. Use when the user says "set up a
  vault here", "initialise the vault", "read VAULT-STARTER and bootstrap this
  project", "add a second axis", or when a project has months of context living
  in chat and no durable place to put it. Covers the interview, the directory
  layout, the seed files, the privacy wiring and the baseline audit. Do NOT use
  it to reorganise a vault that already exists (that is vault-lint) or to close
  a session (that is vault-checkpoint).
---

# Bootstrap a Vault

## What this does

Turns a repository into one the agent can work from for months without
re-explaining the project every session. The deliverable is a directory of
markdown plus two seed habits: every session starts at `Current-State.md`, and
every operation ends by updating three files.

Read `VAULT-STARTER.md` before starting. This skill is the procedure; that
document is the contract.

## Step 1 — Interview, once

Ask all of it in a single round. A bootstrap that interrupts six times gets
abandoned.

1. **Project name and domain.** Software, research, writing, operations,
   anything. The domain decides the loop names.
2. **Existing raw sources.** README, specs, transcripts, design docs. Anything
   that already holds truth.
3. **How a deliverable is validated here.** Tests, review, acceptance criteria.
   Then the question most people have not thought about: **what control case
   proves that validation actually measures anything?** (VAULT-STARTER §8.5.)
4. **Individual or collaborative.** This changes the optimisation strategy from
   day one (§9.4).
5. **One axis or several.** A repo can hold several independent vaults (§3.6).
   If several: which is the default when a session is ambiguous, and which ones
   are private.
6. **Language boundary.** What is written in the working language and what in
   the audience's language (§5.6). Deciding late leaves translation debt nobody
   has sized.

## Step 2 — Create the structure

Follow §3. Respect whatever already exists; never move a user's files to fit
the template.

```
<repo>/
├── CLAUDE.md
├── VAULT-STARTER.md
└── Vault/                    # or <AxisName>/ per axis in a multi-axis repo
    ├── SCHEMA.md
    ├── 00-Index.md
    ├── LOG.md
    ├── 10-Knowledge/
    ├── 20-State/
    │   ├── Current-State.md
    │   ├── Task-Board.md
    │   ├── Lecciones.md
    │   └── Decisiones/
    ├── 30-Loops/
    └── 90-Raw/
```

## Step 3 — Seed the files

- **`SCHEMA.md`**: sections 2 to 9 of `VAULT-STARTER.md`, with loop names
  adapted to the domain.
- **`Current-State.md`**: the real current state, plus a closing section
  "NEXT SESSION" listing what comes next and **which decisions are waiting on
  the human**. Ceiling 2,500 tokens.
- **`LOG.md`**: one entry, `state | Vault initialised`.
- **`00-Index.md`**: one line per page, grouped by layer.
- **`Lecciones.md`**: start with the Environment section (build, test, paths).
- **`30-Loops/`**: the five base loops from §6.

## Step 4 — Install the auditor

Copy `scripts/check_vault.py` **without editing it**. It discovers axes by
filename, so it works unmodified. If a ceiling genuinely needs to move, create
`vault-config.json` rather than editing the script (§7.1) — an edited copy is
how the ceiling drifts and nobody notices.

Run it once for a baseline.

## Step 5 — Wire privacy

If there is a git repo, add glob patterns, never literal lines:

```
Notas-Privadas*
Bitacora-Privada*
```

Plus any fully private axis directory. **Verify with `git check-ignore -q`, not
by reading `.gitignore`** — a glob does not appear as a literal string.

Never put credentials in any `.md`, only references to where they live.

## Step 6 — First ingest

If sources already exist, run one Ingest Loop to compile them into
`10-Knowledge/`. Flag contradictions explicitly; never resolve one silently.

## Step 7 — Write CLAUDE.md

Use the block in §11. It must name the axes, the default one, and the language
boundary.

## Step 8 — Close

Run the closing routine (§7): commit, and show the auditor's report as the
startup-weight baseline.

## Anti-goals

- **Do not build what §8 defers**: no scheduler, no declarative multi-agent
  orchestration, no embeddings. Under roughly 300 pages the index replaces
  search.
- **Do not auto-load knowledge pages via `@import`.** Only what every single
  session needs. Everything else lives one path away.
- **Do not invent project state.** If you do not know where the project is, ask.
  A confident but wrong `Current-State.md` is worse than an empty one.
