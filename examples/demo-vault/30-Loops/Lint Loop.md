---
status: ratificado
updated: 2026-09-11
---

# Lint Loop

**Objective.** Keep the vault healthy on its three independent axes.

**Entry state.** Any time; typically at the end of a working session.

**Phases.**
1. Completeness: contradictions, broken links, stale statuses, index vs reality.
2. Startup weight: `python3 scripts/check_vault.py`. Amber or red is work for
   this loop even when nothing is missing.
3. Content consistency: the domain's own mechanical linter, before spending any
   judgement on subagents.

When a result looks wrong in a boring way (missing files, mangled accents),
check [[Quirks del Entorno]] before debugging the vault itself.

**Validation.** Auditor green, findings addressed at the SOURCE of the datum.

**Exit state.** Index, LOG and Current-State updated.
