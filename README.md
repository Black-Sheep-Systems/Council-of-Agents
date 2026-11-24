# Council of Agents

**21 specialist agents for Claude Code. Safe, simple changes get a light
check; changes that touch security get a code review and a security audit.**

You talk to Claude as usual. Claude acts as coordinator: it decides which
agents a task needs, launches them, passes each one's findings to the next,
and reports back with what was checked and what was not.

**[Read the manual](plugins/agent-council/MANUAL.md)** ·
[Install](#install) ·
[The agents](#the-agents) ·
[What changed in each version](plugins/agent-council/CHANGELOG.md)

## What it does

- **Gives Claude a team.** Each agent has one job: research, writing code,
  debugging, testing, code review, security audit, documentation,
  infrastructure, planning, writing and art.
- **Checks each change only as much as it needs.** A typo fix in a README
  gets no agents. A change to how a total is calculated gets a test and a
  code review. A change to how passwords or uploads are handled gets a test,
  a code review and a security audit.
- **Runs only the tests that cover the change.** The full test suite is for
  wide changes, and Claude says which it is running, and why, before it runs.
- **Says plainly what was not checked.** Every result that changed files ends
  with a short review section: who reviewed what, what they found, what was
  fixed, what is still open, and which checks did not run.
- **Keeps working while you are away, within limits.** It keeps a change log,
  will not push, deploy, delete anything outside the task, or sign off
  without you, and parks any question only you can answer.

## Who it is for

Anyone using Claude Code directly. The agents and their rules are all in this
plugin; there is no separate harness, service or account to set up.

## Install

Replace `<owner>/<repo>` with this repository's address on GitHub:

```bash
claude plugin marketplace add <owner>/<repo>
claude plugin install agent-council@worldsmith
```

Check that it loaded:

```bash
claude plugin details agent-council
```

It should list one skill, `council`, and 21 agents.

## Try it

Start Claude Code in a project and ask for a small change:

> Change `format_duration` so durations of an hour or more are shown as hours
> and minutes.

Claude makes the change, Quinn writes a test and runs the one test file that
covers it, Marcus reviews the change and the code around it, and you get the
result with a review section at the end. You did not have to ask for any of
that.

Other ways to use it:

| You want | Say something like |
|---|---|
| Work done, reviewed as needed | "Add rate limiting to the API, with tests and docs" |
| One agent | "Marcus, review my last commit" |
| A review of existing work | "Have agents review this" |
| Something written | "Write a 600-word guide to setting up two-factor authentication" |
| Work to continue while you are out | "Keep going while I'm out; leave anything you're unsure of for me" |
| The rules loaded by hand | `/agent-council:council` |

## The agents

### Programming

| Agent | Job |
|---|---|
| **Rex** | Finds and compares libraries, patterns and prior art |
| **Thomas** | Challenges research before it becomes code |
| **Ada** | Writes and changes code; applies fixes reviewers ask for |
| **Devon** | Debugs: reproduces, finds the root cause, makes the smallest fix |
| **Quinn** | Writes tests for a change and runs the ones that cover it |
| **Marcus** | Reviews a change and the code it affects |
| **Sentinel** | Audits a change for security problems |
| **Clara** | Docs, READMEs, change logs, manuals, minutes |
| **Piper** | Docker, CI/CD and deployment config; never deploys unless told to |
| **Atlas** | Plans large work and integrates several agents' output |

### Writing

| Agent | Job |
|---|---|
| **Quill** | Turns a brief into a spec: headings, length, audience |
| **Prose** | Writes the piece |
| **Sabine** | Checks structure and length by counting |
| **Wren** | Judges whether the piece really answers the brief |
| **Coeus** | Checks factual claims against sources |
| **Sol** | After a failed check, names the cause and a lesson for the retry |

### Art

| Agent | Job |
|---|---|
| **Ember** | Researches visual references |
| **Blake** | Writes the style guide |
| **Lex** | Writes the image prompt |
| **Nova** | Generates the image, if the session has an image tool |
| **Sage** | Checks the image |

## Three pipelines

- **Programmer:** Atlas plans, Rex and Thomas research, Ada writes, Quinn
  tests, reviewers check, Clara records. Steps a task does not need are
  skipped.
- **Writing:** Quill, Prose, Sabine, Wren, Coeus, with Sol if a check fails.
  For an article, essay, report, guide or post.
- **Art:** Ember, Blake, Lex, Nova, Sage.

## The manual

[The manual](plugins/agent-council/MANUAL.md) is the full guide:

1. [What it is](plugins/agent-council/MANUAL.md#what-it-is)
2. [Getting started](plugins/agent-council/MANUAL.md#getting-started)
3. [How to ask](plugins/agent-council/MANUAL.md#how-to-ask)
4. [The agents](plugins/agent-council/MANUAL.md#the-agents)
5. [The programmer pipeline](plugins/agent-council/MANUAL.md#the-programmer-pipeline)
6. [The writing pipeline](plugins/agent-council/MANUAL.md#the-writing-pipeline)
7. [The art pipeline](plugins/agent-council/MANUAL.md#the-art-pipeline)
8. [Reviews](plugins/agent-council/MANUAL.md#reviews)
9. [Testing](plugins/agent-council/MANUAL.md#testing)
10. [Working while you are away](plugins/agent-council/MANUAL.md#working-while-you-are-away)
11. [Project rules](plugins/agent-council/MANUAL.md#project-rules)
12. [Limits](plugins/agent-council/MANUAL.md#limits)
13. [Troubleshooting](plugins/agent-council/MANUAL.md#troubleshooting)

## Limits

- Agents cannot launch other agents; Claude runs every step.
- At most 2 fix cycles per change and 20 agent launches per task, then it
  stops and asks.
- The art pipeline needs an image-generation tool in the session. Without
  one, Nova hands back the final prompt and says no image was made.
- Installing adds a short description of each agent and of the skill to
  every Claude Code session.

## Other ways to install

From a local copy of this repository, give the folder's path in place of
`<owner>/<repo>`:

```bash
claude plugin marketplace add ./agent-council
claude plugin install agent-council@worldsmith
```

To try it for one session without installing, start Claude Code with
`claude --plugin-dir` and the path to `plugins/agent-council`.

In the Claude desktop app, add the `agent-council.plugin` file. The build
writes it to `dist/`; it is not stored in this repository.

## For maintainers

### Layout

```
.claude-plugin/marketplace.json     the marketplace catalog
plugins/agent-council/              the plugin
  .claude-plugin/plugin.json
  agents/                           the twenty-one agents
  skills/council/SKILL.md           working rules, review gate, pipelines
  examples/project-overlay.md       template for per-project rules
  MANUAL.md                         the user manual
  CHANGELOG.md                      what changed in each version
tools/shared-rules.md               the rules appended to every agent
tools/build.py                      check and package
tools/private-terms.example.txt     template for your own never-publish list
_config.yml                         settings for the website version
```

### Change and rebuild

Edit the files under `plugins/agent-council/`. The "Shared rules" block at
the end of each agent file is written by the build from
`tools/shared-rules.md`; edit it there, not in the agent files.

```bash
python tools/build.py           # sync shared rules, check, write dist/*.plugin
python tools/build.py --check   # check only
claude plugin validate .        # Claude Code's own check
```

The build fails if a machine path or a banned word is found in the plugin,
this README, `_config.yml` or the marketplace file. To have it also catch your own name or
private project names, copy `tools/private-terms.example.txt` to
`tools/private-terms.txt` and list them there; that file is never committed.

To release a change, raise `version` in
`plugins/agent-council/.claude-plugin/plugin.json` and add an entry at the
top of `plugins/agent-council/CHANGELOG.md`. People who installed from the
marketplace stay on the version they have until it changes.

### The website version

This repository can also be served as a website by GitHub Pages, with this
page as the home page and the manual as a page of its own. `_config.yml`
holds the title and theme. Turn it on in the repository's Pages settings,
publishing from the main branch.
