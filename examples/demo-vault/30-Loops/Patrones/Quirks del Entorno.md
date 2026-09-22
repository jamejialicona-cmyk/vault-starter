---
status: ratificado
source: "VAULT-STARTER.md sections 3.5, 6.5, 7, 8 and 12"
updated: 2026-09-22
access: equipo
---

# Quirks del Entorno

> A shared pattern, not a loop (`VAULT-STARTER.md` section 6.5). Several loops
> hit the same environment traps; this page is where each trap is written once
> so no loop pays for it twice. Referenced by [[Lint Loop]] and by every
> executor brief alongside [[Lecciones]].

## When to use it

Before trusting any result that looks wrong in a boring way: missing files,
mangled accents, a change that "did not apply", a date that is off by one. Check
this page before debugging the work itself. The cause is often the environment.

## Entry format

Every quirk has the same four parts. The **check** matters most: it has to
be something you can run in under a minute that separates "the quirk" from "a
real bug".

- **Symptom**: what you see.
- **Cause**: what is actually happening.
- **Check**: one action that confirms or rules it out.
- **Rule**: what to do from now on.

## Quirks

### The console mangles accents

- **Symptom**: `Situaci├│n` instead of `Situación` in script output, or a file
  that was fine now shows `Ã©` everywhere.
- **Cause**: the Windows console opens in cp1252. Separately, PowerShell 5.1's
  `Get-Content | Set-Content` rewrites a file in the ANSI codepage.
- **Check**: print one known accented string. Then open the file in an editor
  that shows its encoding.
- **Rule**: scripts force UTF-8 on stdout. Vault files are edited only with
  tools that preserve UTF-8, never with shell one-liners.

### The notes app shows fewer files than the disk has

- **Symptom**: a listing shows 2 of 24 files, or a long page comes back as its
  last paragraph only. No error.
- **Cause**: the notes app's MCP desynchronised mid-session. The vault on disk
  is intact.
- **Check**: list the same folder through the filesystem.
- **Rule**: work the vault through the filesystem. Suspect the MCP before
  assuming data loss.

### Something deleted comes back by itself

- **Symptom**: a folder removed from the repo reappears days later, with nothing
  in git history explaining it.
- **Cause**: a registry outside the repo, usually the notes app's global
  config listing a nested vault, which the app regenerates on start.
- **Check**: search the app's global config for the folder name.
- **Rule**: remove it through the app's own vault picker, never by hand-editing
  config while the app may be running.

### The scheduled task can create files but not edit them

- **Symptom**: an automated loop writes new files fine, then fails with an
  unclear permissions error on `Current-State.md`.
- **Cause**: the scheduler inherits a session whose OS permissions allow creating
  files but not modifying ones that existed before it first ran.
- **Check**: have the task make one trivial edit to an existing file before it
  runs a full loop.
- **Rule**: no loop is trusted to a scheduler until that edit succeeds.

### Today's date is wrong

- **Symptom**: a LOG entry or `updated:` field dated the day the prompt was
  written, not the day it ran.
- **Cause**: the date was taken from the prompt, a filename, or the agent's
  memory.
- **Check**: run the system date command.
- **Rule**: run it in the first turn that writes anything dated, and again if
  the session crosses midnight.

### "Last modified by" is not "who did it"

- **Symptom**: a record credits an action to someone who says they never touched
  it.
- **Cause**: the last-write field names whoever saved the record LAST, for any
  reason.
- **Check**: look up the audit or activity log, which has author and time per
  action.
- **Rule**: attribute actions from the audit log only.

### CLI login authorised the wrong account

- **Symptom**: a device-code login (`gh auth login --web` and similar) reports
  success in the browser, but the CLI still lists only the old account.
- **Cause**: two separate traps. The browser approved the code with whatever
  account was already signed in. And the CLI only starts polling for the token
  after you press Enter at its prompt. If you skip that step, the grant is
  never collected, and later commands get typed into the prompt that is still
  open.
- **Check**: ask the CLI who it is (`gh api user --jq .login`) instead of
  trusting the success page.
- **Rule**: sign in to the target account in a private window, press Enter at
  the CLI prompt, and verify the identity from the CLI afterwards.

### The hook works in the terminal but not from the agent

- **Symptom**: a hook script runs by hand and silently does nothing when the
  agent triggers it.
- **Cause**: the agent's shell differs from yours. On Git Bash for Windows,
  `jq` is usually missing and the interpreter is `python`, not `python3`.
- **Check**: run the hook with the same shell and the same stdin payload the
  agent sends.
- **Rule**: hooks parse JSON with Python and call `python`. They assume nothing
  the shell does not ship with.

## Sanitising a quirk before it enters a shared vault

A quirk found in a private context often carries private detail. Before
writing it here:

1. **Keep** the symptom, the cause, the check and the rule.
2. **Strip** usernames, account handles, absolute paths, hostnames, client names
   and every credential or token fragment.
3. **Generalise** the tool only if the quirk really is generic. "The notes app's
   MCP" is fine. A version-specific bug keeps its version.
4. **Link** the full story in the private journal if one exists. The shared page
   says what happened, never who it happened to.

A quirk nobody can recognise from its symptom will never be found when it
matters. Specific symptoms stay specific. Only the identifying details go.
