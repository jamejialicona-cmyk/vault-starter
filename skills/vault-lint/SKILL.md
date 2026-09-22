---
name: vault-lint
description: >-
  Audit the health of a Vault on its three independent axes: completeness,
  startup weight, and content consistency. Use when the user asks for a "lint",
  "vault health check", "why is the session slow to start", "is the vault
  consistent", "run the audit", when check_vault.py reports amber or red, or
  periodically at the end of a working stretch. Also covers how to ACT on a
  finding, which is where most audits fail. Do NOT use it to initialise a vault
  (that is vault-bootstrap) or to close a session (that is vault-checkpoint).
---

# Lint a Vault

## The three axes are independent

This is the idea the skill exists to enforce. A vault can be **complete** and
still be **expensive** to open, and it can be both and still be
**inconsistent**. Each axis is audited separately and each has its own fix.

Confusing them is why "nothing is missing" gets mistaken for "the vault is
healthy".

| Axis | Question | Instrument |
|---|---|---|
| Completeness | Is anything missing or contradictory? | Reading, and the index |
| Startup weight | What does opening a session cost? | `check_vault.py` |
| Content consistency | Do the facts agree with each other? | The domain's own linter |

## Axis 1 — Completeness and coherence

- Contradictions between pages, and between pages and the deliverables.
- Broken `[[wikilinks]]`. **These are backlog, not garbage.** List them, never
  delete them.
- Orphan pages nothing links to.
- Stale `status:` values. A page marked `propuesto` for two months was either
  ratified in conversation and never recorded, or abandoned.
- Index versus reality, both directions: every page in the index, every index
  entry a real page.
- State versus repo: does `Current-State.md` reflect the actual branch?

## Axis 2 — Startup weight

```bash
python3 scripts/check_vault.py            # readable table
python3 scripts/check_vault.py --json     # for the agent to consume
python3 scripts/check_vault.py --eje Boda # one axis only
```

Read the **worst case** across axes, not the average: an average hides the one
that hurts. Green under 10,000 tokens, amber to 30,000, red above.

**Read the FINDINGS too, not just the colour.** A modified ceiling, an unrotated
LOG, or an axis with two `Current-State.md` files do not move the colour and
matter just as much.

Levers, in order of friction. Always start with the frictionless one:

1. **`@imports` to on-demand.** Drop the `@` from knowledge pages that are not
   needed every session. Edits one file, touches no content.
2. **Stop auto-reading the LOG and private journal.** The saving comes from not
   loading them, not from trimming them.
3. **Rotate the LOG** to `LOG-Archivo/<period>.md` if it is over its ceiling.
   Append-only: archiving is not summarising. Nothing is rewritten.
4. **Split the private notes** into live and archived.
5. **Trim `Current-State.md`** to present tense only. History goes to the LOG.

**Never raise a ceiling so the file fits.** If a ceiling truly must move, put it
in `vault-config.json` and record the decision in the LOG with its reason. A
ceiling that follows the file is not a ceiling.

## Axis 3 — Content consistency

Run the domain's mechanical linter **before** spending any judgement on
subagents. A deterministic check is cheap, reproducible and does not
hallucinate; a judgement subagent is expensive and its value is in what cannot
be mechanised. Spending it on a broken citation wastes it and buries the three
findings that needed a human mind.

What is usually mechanisable in any domain:

- **Referential integrity** — every citation resolves, every link lands.
- **Arithmetic** — derived numbers add up.
- **Single source** — the same datum declared in two pages is a design error.
- **Class completeness** — if the domain defines eight categories, all eight
  appear where they should.
- **Freshness** — `updated:` against the file's real modification.

If no such linter exists yet, propose one. It can start with two checks.

## How to act on a finding

Most audits fail here, not at detection.

> **Every fix goes to the SOURCE of the datum, never to the reported line. And
> before closing it, sweep the ENTIRE CLASS of mentions across the vault.**

A linter reports **a symptom with coordinates**. That is not the problem. The
problem is the page that originated the wrong datum and propagated it to six
others. Fixing the reported line leaves the source intact, so the next sweep
finds it again on a different line and it looks like a new finding.

1. Find the source. Which page declares this first, and with what `source:`?
2. Fix it there, and bump `updated:`.
3. Grep the whole class, not the exact reported string. If it was a date, every
   date for that event. If a figure, every mention and its derivations.
4. Only then close it, and record in the LOG how many occurrences the class had.
   That number says whether the fix was worth anything.

**When a finding comes from a review or a QA that describes a source rather than
quoting it, and the description contradicts the original: the source wins.**
Every paraphrase is lossy translation.

## Closing

Re-run the auditor. Confirm the weight came down **without any ceiling having
moved**, and that `git status` still leaves the private files out of git.

Then the closing routine: index, LOG, `Current-State.md`.

## Anti-goals

- **Do not delete broken links** to make a report look clean. They are backlog.
- **Do not restructure `Current-State.md` or `LOG.md` in a collaborative vault.**
  They are shared append/edit files; restructuring collides with the next
  person's change. Take them out of auto-load instead.
- **Do not report an axis as healthy because another one is.**
- **Do not trust a green result from an instrument you have not validated.**
