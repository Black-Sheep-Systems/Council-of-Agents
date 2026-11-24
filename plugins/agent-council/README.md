# Council of Agents

21 specialist agents for Claude Code, and one skill that says how to run
them. Safe, simple changes get a light check; changes that touch security get a
code review and a security audit.

## Who it is for

Anyone using Claude Code directly. The agents and their rules are all in this
plugin; there is no separate harness, service or account to set up.

## What you get

| Agent | Role | Edits files? |
|---|---|---|
| rex | Research: libraries, prior art | no |
| thomas | Challenges research | no |
| ada | Writes and changes code; fixes review findings | yes |
| devon | Debugging and diagnostics | yes |
| quinn | Tests | tests |
| marcus | Code review | no |
| sentinel | Security audit | audit log only |
| clara | Docs, records, change logs | docs |
| piper | Docker, CI/CD, deployment config | config |
| atlas | Plans big tasks, integrates, architecture calls | when integrating |
| ember | Visual reference research | no |
| blake | Style guide | no |
| lex | Image prompt | no |
| nova | Generates the image | output image only |
| sage | Checks the image | no |
| quill | Plans a piece of writing: sections and length | no |
| prose | Writes the piece | the piece only |
| sabine | Checks structure and length by counting | no |
| wren | Judges whether the piece answers the brief | no |
| coeus | Checks factual claims against sources | no |
| sol | Turns a failed attempt into a lesson for the retry | no |

The `council` skill adds:

- **Working rules.** Targeted tests by default; the full suite only for wide
  changes. Result lines and failures only. Review what changed and what it
  affects, nothing else.
- **A proportional review gate.** A risk table decides who reviews what:
  security-touching code gets Marcus and Sentinel, ordinary code gets Marcus,
  a README correction gets no review round.
- **Unattended running.** Rules for working while you are away: a change log,
  a fixed list of things it will not do without you, and a report that leads
  with what is waiting on you.
- **Three pipelines.** Writing (Quill, Prose, Sabine, Wren, Coeus, Sol), for
  an article, essay, report, guide or post. Programmer (Atlas, Rex, Thomas, Ada, Quinn, reviewers,
  Clara) and art (Ember, Blake, Lex, Nova, Sage).

## Install

Replace `<owner>/<repo>` with the repository that hosts this plugin's
marketplace:

```bash
claude plugin marketplace add <owner>/<repo>
claude plugin install agent-council@worldsmith
```

## Use

Ask for work as usual; the skill applies when a task creates or changes
files. You can also name an agent ("Marcus, review this"), ask for a review
("have agents review this"), ask for something to be written ("write a guide
to X for new users"), or run the skill directly with
`/agent-council:council`.

Agents appear as `agent-council:<name>`, for example
`agent-council:marcus`.

### Getting good results

- **Say what is in scope.** "Fix the null check in src/auth.rs line 47" beats
  "fix the code".
- **Ask for the kind of check you want.** "Run a security audit on this" goes
  to Sentinel; "review this for correctness" goes to Marcus. A plain "check
  this over" gets whichever reviewers the risk table picks.
- **Give context.** "The /api/users endpoint takes 5 seconds; here is the query
  it runs" beats "why is this slow?".
- **For big jobs, describe the outcome, not the order.** "Add rate limiting to
  the API, with tests and docs" lets the plan choose the agents.

### How each agent tends to answer

| Agent | Style |
|---|---|
| rex | Thorough; lists options and compares trade-offs |
| thomas | Skeptical; challenges every claim |
| ada | Pragmatic; ships working code, avoids over-engineering |
| devon | Methodical; shows reasoning, never guesses |
| quinn | Systematic; covers edge cases, no flaky tests |
| marcus | Direct; severity-labelled, actionable findings |
| sentinel | Security-first; no finding waved away |
| clara | Clear, structured, written for the reader |
| piper | Careful, incremental, always gives a rollback |
| atlas | Coordinating; plans and integrates |
| ember | Researched; references with sources |
| blake | Decisive; one style guide with exact colors |
| lex | Dense; one prompt, concrete visual detail |
| nova | Final say; plain about what was and was not generated |
| sage | Exacting; approves or names what must change and who changes it |
| quill | Spare; exact headings and a word count, no prose |
| prose | Finished writing only; no outlines, no placeholders |
| sabine | Numbers; every verdict comes with a measurement |
| wren | Two lines; a verdict and one specific reason |
| coeus | A table of claims, each with its source; plain when it could not check |
| sol | Three lines; a root cause, where it started, a lesson |

## Project rules (optional)

To add steps for one project (a pre-write check, where logs go), put them in
`.claude/agent-council.md` in that project. The plugin ships a template,
`examples/project-overlay.md`; the quickest way to get it is to ask Claude to
"set up project rules for the council".

## Manual

`MANUAL.md` is the full guide: how to ask, what each agent does, the three
pipelines with worked examples, reviews, testing, working while you are away,
project rules and troubleshooting.

## Versions

This is version 4. `CHANGELOG.md` says what changed in each version since the
original roster.

## Limits

- Agents cannot launch other agents; the main session runs every pipeline.
- Nova needs an image-generation tool in the session. Without one it hands
  back the final prompt and says no image was generated.
- The gate allows at most 2 fix cycles per change and 20 agent launches per
  task, then stops and asks.
