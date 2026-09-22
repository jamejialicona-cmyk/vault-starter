# vault-starter

A method, an auditor and three agent skills for running long projects with an
AI agent, where the project's knowledge lives in a versioned Markdown vault
instead of in chat history.

[![CI](https://github.com/jamejialicona-cmyk/vault-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/jamejialicona-cmyk/vault-starter/actions/workflows/ci.yml)

---

## Why this exists

AI-assisted work that lives in conversations fails in predictable ways once a
project runs for months.

**Decisions get buried.** The reason something was built a certain way is
somewhere in message four hundred of a chat nobody will reopen.

**Every session starts cold.** The agent is re-taught how the project works,
by hand, each time, and each retelling drifts a little.

**The fix creates a new problem.** Teams that do move knowledge into a wiki or
vault find that a vault can stay complete and accurate and still cost 100,000+
tokens to load before the first message. People stop opening sessions because
it has become slow.

The method answers all three. The agent maintains a Markdown vault, and the
human directs it. Every session starts from one small state file. The cost of
opening a session is treated as a metric with its own traffic light, audited
by a script rather than judged by feel.

It is distilled from two independent deployments of several months each, in
unrelated domains: company operations, and the production of a video game.
Every rule in it traces back to an incident that was measured.

## What is in the repo

| Path | What it is |
|---|---|
| [`VAULT-STARTER.md`](VAULT-STARTER.md) | The method itself: one self-contained file, v4. Written in Spanish (see [Language](#language)). |
| [`scripts/check_vault.py`](scripts/check_vault.py) | Read-only auditor for startup weight and vault health. Standard library only. |
| [`scripts/test_check_vault.py`](scripts/test_check_vault.py) | Test suite for the auditor, with a control case for every defect it claims to detect. |
| [`scripts/hook_current_state.sh`](scripts/hook_current_state.sh) | Claude Code hook: re-audits whenever `Current-State.md` is edited. |
| [`skills/`](skills/) | Three agent skills: bootstrap, lint and checkpoint. |
| [`examples/demo-vault/`](examples/demo-vault/) | The smallest correct vault. Also the CI fixture. |

## Quick start

Copy `VAULT-STARTER.md` to the root of your repository and tell your agent:

> Read VAULT-STARTER.md and initialise the Vault for this project.

Section 10 of the file contains the bootstrap instructions the agent follows:
a short interview, the directory layout, the seed files, the privacy wiring, and
a baseline audit.

## The auditor

```bash
python3 scripts/check_vault.py [path]              # readable table
python3 scripts/check_vault.py [path] --json       # for an agent to consume
python3 scripts/check_vault.py [path] --eje Juego  # one axis only
```

Run against the demo vault:

```
EJE: demo-vault  (demo-vault/)
  [   OK] soft      122t  demo-vault/20-State/Current-State.md
  [   OK]    -      107t  demo-vault/00-Index.md
  [   OK]    -      105t  demo-vault/20-State/Lecciones.md
  [   OK]    -       62t  demo-vault/LOG.md
  [   OK]    -       92t  demo-vault/SCHEMA.md
  -> ARRANQUE: ~122t [VERDE]

[VERDE] ARRANQUE PEOR CASO: ~122 tokens
```

What it measures and reports:

- **Startup weight** per axis: `CLAUDE.md`, plus the axis's `Current-State.md`,
  plus every `@import`. Green under 10,000 tokens, amber to 30,000, red above.
  In a repo with several vaults the **worst case** rules, because an average
  hides the one that hurts.
- **Ceilings as contracts.** `Current-State.md` has a ceiling of about 2,500
  tokens and `LOG.md` about 40,000. You can move a ceiling in
  `vault-config.json`, but the report then flags it as `TECHO MODIFICADO`.
  Moving a ceiling so the file fits is a decision and has to be visible.
- **Discovery by name, not by path.** Any folder with its own
  `Current-State.md` is an axis. The script works unedited in any project,
  which removes the per-project copy where drift used to creep in.
- **Structural errors:** two entry points in one axis, an axis with no method
  file, an `@import` that does not exist.
- **Leaks:** a private notes file that git would commit, checked with
  `git check-ignore` rather than by reading `.gitignore`.

It never writes anything.

## The skills

Each skill says when to fire and, just as importantly, when **not** to. The
anti-goals keep the three from stepping on each other.

| Skill | Fires on | Does not fire on |
|---|---|---|
| [`vault-bootstrap`](skills/vault-bootstrap/SKILL.md) | "set up a vault here", adding a second axis | reorganising an existing vault |
| [`vault-lint`](skills/vault-lint/SKILL.md) | health checks, an amber or red audit, "why is startup slow" | initialising, closing a session |
| [`vault-checkpoint`](skills/vault-checkpoint/SKILL.md) | "wrap up", end of a task, context about to run out | auditing, initialising |

To use them with Claude Code, copy the folders into `.claude/skills/` in your
project or into `~/.claude/skills/` for every project.

`vault-lint` carries the lesson that cost the most to learn: **a fix goes to
the source of the datum, never to the reported line, and the whole class of
mentions is swept before the finding is closed.** Four QA rounds in a row
failed on one project because they fixed the line the linter pointed at.

## The hook

`hook_current_state.sh` runs after every `Edit` or `Write`. If the file was a
`Current-State.md`, it audits that axis and returns the traffic light and any
ceiling breach to the agent in the same turn. Trimming happens while the agent
is still in the file, not later as a chore at the end of the session.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": "bash scripts/hook_current_state.sh" }]
      }
    ]
  }
}
```

It parses JSON with Python rather than `jq`, which Git Bash on Windows does not
ship with.

## How the auditor is tested

The method has a rule that governs its own test suite: **an instrument with no
control does not measure, and a green report is not a measurement.**

The demo vault passing proves little on its own. An auditor that had stopped
detecting anything would pass it too. So the suite builds each defect on
purpose in a temporary vault: a state file over its ceiling, a LOG over its
ceiling, two entry points, a moved ceiling, a missing import, an unignored
private file. Then it asserts the auditor reports each one.

The suite was checked against a deliberately broken auditor, with one ceiling
disabled and the leak check disabled. Exactly the two matching tests failed.

```bash
python3 scripts/test_check_vault.py
```

CI runs it on Linux and Windows, on Python 3.10 and 3.13.
Windows is included on purpose, because the auditor has to force UTF-8 output
to survive the Windows console.

## Language

`VAULT-STARTER.md` and the auditor's output are in Spanish, the working language
of both deployments the method came from. The skills, the demo vault and this
README are in English. The method itself makes this kind of split an explicit
bootstrap decision (section 5.6): what is written in the working language and
what in the audience's.

## Sources

Built on three ideas: *LLM-WIKI* by A. Karpathy (the model as a compiler of
knowledge, not a search layer), *Vault-Driven Development v1.0* (the vault
directs the work rather than documenting it), and the `project-context`
playbook (startup cost as a measured, first-class metric). The version history
is in section 13 of the method.

## License

[MIT](LICENSE)
