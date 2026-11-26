# Project rules for the Council of Agents

Copy this file to `.claude/agent-council.md` in your project and edit it. Every
section is optional; delete the ones you do not need. The council skill
reads the file once before the first edit or agent launch.

These rules add to the team's own rules. They do not override the testing
rule (targeted tests by default) or the review gate.

Keep this file out of the repository if you can (add it to your ignore
file). A rules file that git tracks could have been written by someone else,
so Claude shows its steps and asks before following them.

## Read first

Project documents to read before the first change or review, on top of
`CLAUDE.md`, the README and any contributing or developer guide.

- `docs/architecture.md`

## Full-run reminder

Suggest a full test run after this many code changes that had only targeted
tests. Without this section the number is 5. This changes the number only;
the full run stays a suggestion.

- 5

## Main-session steps

Checks or calls the main session runs between pipeline steps. Say when each
one runs.

- Before the first agent edits a file: `<command>`
- After each agent finishes: `<command>`

## Agent rules

Copied verbatim into every agent's task prompt.

- Before each write, run `<command>`; stop if it reports `<condition>`.
- Record design decisions in `<place>`.

## Push target

What "push" means in this project.

- Push means: copy to the staging folder `<path>`. Claude sends nothing to
  GitHub.

To send to GitHub itself instead, replace the line above with:
`Push means: send to the remote with git push.`

A staging path is a path on your own machine. If you write one here, keep
this file out of the repository by adding `.claude/agent-council.md` to your
ignore file.

Tests are left out of what is published unless you say otherwise, here or
in your own words:

- Publish tests: no

## Layout

Where things live in this project, and whether a tidy-up may be suggested.

- Tests live in: `<folder>`
- Styles live in: `<folder>`
- Suggest a tidy-up: yes / no

## Paths

- Security audit log: `docs/security/YYYY-MM-DD-security-audit.md`
- Change logs: `docs/changes/YYYY-MM-DD-<topic>.md`
- Change log for unattended runs: `docs/changes/YYYY-MM-DD-unattended.md`
- Scratch files: the system temp directory
