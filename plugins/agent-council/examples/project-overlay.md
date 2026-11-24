# Project rules for the Council of Agents

Copy this file to `.claude/agent-council.md` in your project and edit it. Every
section is optional; delete the ones you do not need. The council skill
reads the file once before the first edit or agent launch.

These rules add to the team's own rules. They do not override the testing
rule (targeted tests by default) or the review gate.

## Main-session steps

Checks or calls the main session runs between pipeline steps. Say when each
one runs.

- Before the first agent edits a file: `<command>`
- After each agent finishes: `<command>`

## Agent rules

Copied verbatim into every agent's task prompt.

- Before each write, run `<command>`; stop if it reports `<condition>`.
- Record design decisions in `<place>`.

## Paths

- Security audit log: `docs/security/YYYY-MM-DD-security-audit.md`
- Change logs: `docs/changes/YYYY-MM-DD-<topic>.md`
- Change log for unattended runs: `docs/changes/YYYY-MM-DD-unattended.md`
- Scratch files: the system temp directory
