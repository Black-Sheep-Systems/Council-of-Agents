# Council of Agents - user manual

For version 4. This is the guide for a person using the council. The rules
Claude itself follows are in `skills/council/SKILL.md`; this manual explains
them in plain terms and shows what to say.

## Contents

1. [What it is](#1-what-it-is)
2. [Getting started](#2-getting-started)
3. [How to ask](#3-how-to-ask)
4. [The agents](#4-the-agents)
5. [The programmer pipeline](#5-the-programmer-pipeline)
6. [The writing pipeline](#6-the-writing-pipeline)
7. [The art pipeline](#7-the-art-pipeline)
8. [Reviews](#8-reviews)
9. [Testing](#9-testing)
10. [Working while you are away](#10-working-while-you-are-away)
11. [Project rules](#11-project-rules)
12. [Limits](#12-limits)
13. [Troubleshooting](#13-troubleshooting)

## 1. What it is

The council is 21 named agents, each with one job, and one set of rules for
running them. You talk to Claude as usual. Claude is the coordinator: it
decides which agents a task needs, launches them, passes each one's findings
to the next, and reports back to you.

The idea behind the rules is **a scalpel, not a sledgehammer**. Every agent,
test run and review is sized to what changed and what that change can affect.
A one-line README fix does not get a security audit. A change to how passwords
are handled does.

Three things follow from that:

- **Nothing is reported as checked that was not.** If a test or a review did
  not run, the report says so.
- **Nothing is checked twice without a reason.** A re-review covers only the
  fix, not the whole change again.
- **Unfinished work is named as unfinished.** It is never presented as done.

## 2. Getting started

### Install

From a GitHub repository (replace `<owner>/<repo>` with where the plugin is
hosted):

```bash
claude plugin marketplace add <owner>/<repo>
claude plugin install agent-council@worldsmith
```

Check that it loaded:

```bash
claude plugin details agent-council
```

It should list one skill, `council`, and 21 agents.

Other routes: from a local copy of the repository, run `claude plugin
marketplace add` with the folder's path in place of `<owner>/<repo>`; to try
it for one session without installing, start Claude Code with `claude
--plugin-dir` and the path to the plugin folder; and in the Claude desktop
app, add the `.plugin` file, if you were sent one or have built it.

### A first request

Start Claude Code in a project and ask for something small that changes a
file:

> Change `format_duration` so durations of an hour or more are shown as hours
> and minutes.

What happens:

1. Claude makes the change itself, because it is small.
2. Because code behaviour changed, **Quinn** writes a test for it and runs
   only the test file that covers it.
3. **Marcus** reviews the change and the code around it.
4. If Marcus finds a problem, it is fixed and he re-reviews only the fix.
5. You get the result with a short **Review** section at the end: who
   reviewed what, what they found, what was fixed, what is still open, and
   which checks were not run.

You did not have to ask for any of that. It applies whenever a task creates
or changes files.

## 3. How to ask

There are four ways to use the council.

| You want | Say something like | What happens |
|---|---|---|
| Work done, reviewed as needed | "Add rate limiting to the API, with tests and docs" | Claude plans it, runs the agents the risk calls for, and reports |
| One agent | "Marcus, review my last commit" | That agent runs |
| A review of existing work | "Have agents review this" or "check this over" | Claude picks reviewers by risk and relays each verdict |
| The rules loaded by hand | `/agent-council:council` | The skill loads for this session |

### Getting good results

- **Say what is in scope.** "Fix the null check in `src/auth.rs` line 47"
  beats "fix the code".
- **Ask for the kind of check you want.** "Run a security audit on this" goes
  to Sentinel. "Review this for correctness" goes to Marcus. A plain "check
  this over" gets whichever reviewers the risk table picks.
- **Give context.** "The `/api/users` endpoint takes 5 seconds; here is the
  query it runs" beats "why is this slow?".
- **For big jobs, describe the outcome, not the order.** "Build a login system
  with tests and docs" lets the plan choose the agents. You do not need to
  list them.
- **A question is not a review request.** "What does this error mean?" gets
  an answer, not a round of agents.

## 4. The agents

Agents are launched as `agent-council:<name>`, for example
`agent-council:marcus`. You only need the short name when you talk to Claude.

### Programming

| Agent | What they do | Changes files? | Ask them when |
|---|---|---|---|
| **Rex** | Finds and compares libraries, patterns and prior art, with a source for every claim | No | "Find a Rust CSV parser and compare the options" |
| **Thomas** | Challenges research: is it maintained, is the licence a problem, do the sources say what was claimed | No | "Check Rex's findings before we commit to this library" |
| **Ada** | Writes and changes code; applies fixes that reviewers ask for | Yes | "Ada, implement the sort function" |
| **Devon** | Debugs: reproduces, traces, finds the root cause, makes the smallest fix | Yes | "Devon, why does this crash on an empty list?" |
| **Quinn** | Writes tests for a change and runs the ones that cover it | Tests only | "Quinn, add a regression test for that fix" |
| **Marcus** | Reviews a change and the code it affects | No | "Marcus, review this before I merge" |
| **Sentinel** | Security audit of a change and its attack surface | Audit log only | "Sentinel, audit the upload handler" |
| **Clara** | Docs, READMEs, change logs, registers, manuals, minutes | Docs | "Clara, document what changed" |
| **Piper** | Docker, CI/CD, deployment config. Never deploys unless told to | Config | "Piper, set up a GitHub Actions build" |
| **Atlas** | Plans large work, integrates several agents' output, makes architecture calls | Only when integrating | "Atlas, plan how to split this module" |

### Writing

| Agent | What they do | Changes files? |
|---|---|---|
| **Quill** | Turns a brief into a spec: exact headings, target length, audience | No |
| **Prose** | Writes the piece from the spec, every section in full | The piece only |
| **Sabine** | Checks structure by counting: headings, length, hollow sections, padding | No |
| **Wren** | Judges whether the piece really answers the brief | No |
| **Coeus** | Checks factual claims against sources | No |
| **Sol** | After a failed check, names the root cause and a lesson for the retry | No |

### Art

| Agent | What they do | Changes files? |
|---|---|---|
| **Ember** | Researches visual references | No |
| **Blake** | Writes the style guide: mood, palette, lighting, composition | No |
| **Lex** | Writes the image prompt and a negative prompt | No |
| **Nova** | Checks the prompt and generates the image | The image only |
| **Sage** | Checks the image and approves it or says what must change | No |

### How agents work together

Agents cannot launch each other or talk to each other. Claude runs every
step. Each agent ends its reply with a **board post**: a short section the
next agent can act on without redoing the work. Claude passes along the board
posts each agent needs.

Each agent is given a **scope**: the exact files it may change, or
"read-only". An agent that needs more than it was given stops and says so.

## 5. The programmer pipeline

For multi-file or multi-step coding work. Small jobs skip most of it.

| Step | Agent | When it runs |
|---|---|---|
| 1 | Atlas plans | Only for large or cross-cutting work |
| 2 | Rex, then Thomas | Only when an outside library or pattern is in question |
| 3 | Ada writes the code | When there is code to write |
| 4 | Quinn tests | When code changed |
| 5 | Reviewers | Chosen by risk (see [Reviews](#8-reviews)) |
| 6 | Fix and re-check | Only if a reviewer asked for changes; at most twice |
| 7 | Clara records the change | Where the project keeps records |
| 8 | Atlas integrates | Only if several agents' work needs joining up |

### Example

> Add rate limiting to the API. Include tests and docs.

1. Atlas reads the code and returns a plan: which agents, in what order, which
   files each may touch, and which test files each runs.
2. Rex looks for a rate-limiting library; Thomas checks his findings.
3. Ada writes the middleware.
4. Quinn writes tests for under the limit, at the limit, over the limit and
   window reset, runs that test file, and shows the tests fail when the limit
   check is removed.
5. Rate limiting touches network input, so both Marcus and Sentinel review.
6. Marcus flags a counter that is not thread-safe. Ada fixes it; Quinn re-runs
   the affected tests; Marcus reviews only the fix, and Sentinel too, because
   the fix is in code it audited.
7. Clara writes the usage doc.

Steps that add nothing are skipped, and the report says which.

## 6. The writing pipeline

For a piece of writing someone asked for: an article, essay, report, guide,
post or letter. Project docs and change logs are Clara's job, not this.

Quill -> Prose -> Sabine -> Wren -> Coeus, with Sol if a check fails.

| Step | Agent | Result |
|---|---|---|
| 1 | Quill | A spec: required headings, target length, audience |
| 2 | Prose | The finished piece |
| 3 | Sabine | `STRUCTURE PASS`, `STRUCTURE FAIL` or `STRUCTURE UNPROVEN` |
| 4 | Wren | `Verdict: PASS` or `Verdict: FAIL`, with one specific reason |
| 5 | Coeus | `CLAIMS SUPPORTED`, `CLAIMS CONTRADICTED`, `NO CLAIMS TO CHECK` or `COULD NOT CHECK` |

Each check runs only if the one before it passed.

### What the verdicts mean

- **STRUCTURE UNPROVEN** means the spec gave Sabine nothing to check against.
  It is not a pass. The brief goes back to Quill once for a proper spec. If it
  is still unproven after that, it stops and tells you.
- **CLAIMS CONTRADICTED** means a source says otherwise about at least one
  claim. Any contradicted claim fails the piece.
- **COULD NOT CHECK** is neither a pass nor a failure. You get the piece with
  a plain statement that its facts were not verified.
- Claims Coeus could find nothing about, either way, do not fail the piece.
  They are listed for you so you can keep, source or soften them.

### When a check fails

Sol names the root cause and a one-sentence lesson, and says whether it
started in the brief, the spec or the writing. Prose (or Quill, if the spec
was the cause) tries again with that lesson. Only the failed check and the
ones after it run again. After two retries it stops and asks you. If Sol says
the cause was the brief itself, it stops and asks you straight away, because
only you can change the brief.

### It is sized to the piece

- **A few paragraphs:** Prose, then Wren. The report says the structure was
  not checked.
- **A long or sectioned piece:** the full pipeline.
- **No factual claims:** Coeus is skipped, and the report says so.

### Example

> Write a 600-word guide for new users on setting up two-factor
> authentication.

Quill returns four headings and a 600-word target. Prose writes it. Sabine
reports 587 words, all four headings present, no hollow sections. Wren passes
it. Coeus checks the steps against the vendor's documentation and finds one
menu name that has changed, so the verdict is `CLAIMS CONTRADICTED`. Sol says
the cause was in the writing. Prose corrects the menu name, Coeus checks
again, and you get the piece with each verdict line.

## 7. The art pipeline

Ember -> Blake -> Lex -> Nova -> Sage.

Ember gathers references, Blake sets the style, Lex writes the prompt, Nova
checks it and generates the image, and Sage looks at the result. Sage ends
with `APPROVED`, or `REVISION NEEDED` plus what must change and which agent
should change it.

### Example

> Create a logo for my project: a minimalist mountain with a rising sun.

Ember gathers logo and mountain references. Blake sets a flat, two-colour
style with exact hex values. Lex writes the prompt. Nova generates the image.
Sage finds the sun is cut off by the edge and ends with `REVISION NEEDED`,
naming Lex. Lex adjusts the composition, Nova generates again, and Sage ends
with `APPROVED`.

**Nova needs an image tool in the session.** If there is none, Nova hands
back the final prompt, the negative prompt and the settings, and says plainly
that no image was generated.

## 8. Reviews

A review gate runs before any result that created or changed files is
reported, and before anything with effects outside the working files: a git
commit or push, a deploy, sending or publishing something, restarting a live
service. Pure answers and read-only investigation skip it.

### Who reviews what

| Change | Tests | Review |
|---|---|---|
| Touches input handling, auth, tokens, secrets, network, file paths, shell commands, dependencies, or data leaving the machine | Quinn, plus proof the tests can fail | Marcus and Sentinel |
| Code behaviour: logic, state, data | Quinn; proof the test can fail for a bug fix | Marcus |
| The project's own checking tools | Quinn | Marcus. A sign-off your project reserves for a person stays with that person |
| Tests only, comments, docstrings, log wording | The affected test file is run | None; Claude checks it |
| Docs, README, record corrections | None | None; Claude checks each claim against its source |
| A document or plan someone will act on | None | Marcus, only if you want a second read |
| A piece from the writing pipeline | None | The pipeline's own checks |

### The verdicts

- **Marcus** labels each finding critical, warning or nit, and ends with
  `APPROVED` or `CHANGES REQUIRED`. Any critical or warning means changes are
  required.
- **Sentinel** labels each finding Critical, High, Medium, Low or
  Informational, and ends with `CLEAR` or `ISSUES FOUND`. Any Critical, High
  or Medium means issues were found.

### What happens to findings

Every critical or warning from Marcus, every Critical, High or Medium from
Sentinel, and every failing test is fixed. Cheap nits are fixed too; the rest
are listed. Then only the fix is re-checked.

There are **at most two fix cycles per change**. If problems remain after
that, the work stops, the open problems are reported as unresolved, and you
are asked what to do.

### Controlling reviews

- **Skip one:** say "skip review". It applies to that task only.
- **Ask for one:** "have agents review this", "get this reviewed", "check this
  over".
- **Name the reviewers:** "Sentinel, audit this" runs only Sentinel. The
  exception is work Claude itself produced: the reviewers the risk table
  calls for also run.
- **Your own work:** if agents review something you wrote, they report their
  findings and fix nothing unless you ask.

### Proof that a test can fail

For a bug fix, and for any change in the first row of the table, Quinn shows
that the new test fails when the bug is put back or the new check is taken
out. This is done in a scratch copy in memory. Your production files are never
edited to do it.

## 9. Testing

**Only the tests that cover the change are run. The full suite is for wide
changes only.**

A change is wide when it touches something many other things depend on: a
module that many others import, shared test fixtures, how the app is
constructed, test configuration, a dependency upgrade, or a deletion or
rename whose callers a targeted run cannot see.

What to expect:

- Before running tests, Claude tells you in one line whether the run is
  targeted or full, and why.
- A commit, a re-review, or a failed run that was fixed is not by itself a
  reason for a full run.
- If your project has a checklist that says "run the whole suite before every
  commit", this rule still applies. For a narrow change Claude runs the
  targeted tests, tells you the full suite was not run, and points at the
  checklist line so you can decide whether to change it.
- If it is unclear whether a change is wide, Claude asks once. While you are
  away it runs the targeted tests instead, and says so in the report.

To get a full run, ask for one: "run the full suite".

Test output is shown as the result line and any failures. Whole logs are not
pasted.

## 10. Working while you are away

This applies when you say you are stepping away and want work to continue
("keep going while I'm out", "run this overnight"), or when a session is
started by a schedule.

It ends when you return, when a limit you set is reached (a time, a task, a
number of steps), or when nothing is left that can be done without you.

### What happens

1. **Before you go,** you get a short list: what will be worked on, in order,
   and what will be left for you.
2. **While you are away,** a change log is kept: time, agent, action, files.
   It is written to the path your project rules name; without one, it is kept
   in the conversation and given in the report. The testing rule, the review
   gate and the limits all still apply.
3. **When something needs you,** that task is parked with the question
   written down, and work continues on anything that does not depend on it.
4. **When you return,** the report leads with what was finished, what is
   parked and the question for each, the change log, and which checks were
   not run.

### What it will not do without you

- Push, deploy, send, publish, or restart or stop a live service.
- Delete or change files outside what you asked for.
- Discard uncommitted work, rewrite git history, delete branches, or run a
  migration against a real database.
- Start a third fix cycle, or go past the launch limit.
- Sign off on something your project reserves for a person.
- Make a decision that cannot be undone and could reasonably go either way.

### Authorising something in advance

You can allow one of those by naming the exact action in your request, or in
the scheduled prompt. It covers that run only:

> Fix the failing import test and push when it is done.

The push still waits for the review. It happens only if the review finished
with nothing open. Otherwise it is parked, and you are told why.

A local commit is allowed after a clean review when you asked for commits.

Passing time never counts as approval. A parked item stays parked until you
answer.

## 11. Project rules

To add steps for one project, put a file at `.claude/agent-council.md` in
that project. The plugin ships a template, `examples/project-overlay.md`. The
quickest way to get it is to ask Claude to "set up project rules for the
council".

The file is read once, before the first edit or agent launch in a session, so
after changing it, start a new session or ask Claude to read it again.

The file can have three sections, all optional:

- **Main-session steps:** checks or commands Claude runs between pipeline
  steps.
- **Agent rules:** copied into every agent's task, word for word. Use this
  for things like "before each write, run this check" or "write all dates as
  YYYY-MM-DD".
- **Paths:** where the security audit log, Clara's change records, the change
  log for unattended runs, and scratch files go.

Without a paths section, Sentinel's audit log goes to
`docs/security/YYYY-MM-DD-security-audit.md`, Clara's change records go to
`docs/changes/YYYY-MM-DD-<topic>.md`, the unattended change log stays in the
conversation and the report, and scratch files go to the system temp
directory.

Project rules add to the council's rules. They cannot override the testing
rule or the review gate.

## 12. Limits

| Limit | Value | What happens at the limit |
|---|---|---|
| Fix cycles per change | 2 | Stops, reports what is open, asks you |
| Retries in the writing pipeline | 2 | Stops, reports what is open, asks you |
| Agent launches per task | 20 | Stops, reports what is open, asks you |
| Agents running at once | 5 | The rest wait |

Agents that edit files do not run at the same time on overlapping files, and
do not run while another agent is running tests their edit would affect.

## 13. Troubleshooting

**"Marcus, review this" does nothing special.**
Check the plugin is installed and enabled with `claude plugin details
agent-council`. Then load the rules by hand with `/agent-council:council`.

**An agent type is not found.**
If `agent-council:<name>` is not offered in a session, Claude falls back to a
general-purpose agent and gives it that agent's instructions from the plugin.
The work still happens. If you see this, check the plugin with `claude plugin
details agent-council` and reinstall it; it usually means the plugin did not
load fully.

**Reviews seem to follow different rules from this manual.**
An older copy of the agents or their rules may be loaded as well, for example
agent files in your user-level agents folder or an older skill on your
account. Remove the older copy so only one set of rules applies.

**No image was generated.**
The art pipeline needs an image-generation tool in the session. Without one,
Nova returns the final prompt and says no image was made.

**Coeus says COULD NOT CHECK.**
Coeus could not reach sources, or found nothing either way. The piece is
delivered with a statement that its facts were not verified. Give Coeus
source material, or check the listed claims yourself.

**A full test suite ran when you did not expect it.**
Claude should have said why before running it. A checklist in your project is
not a reason for one; tell Claude, and see [Testing](#9-testing).

**The report says the work is unreviewed.**
The session had no way to launch agents, so no independent review happened.
The work is not finished until it is reviewed; run it again in a session
where agents are available.

**A step is reported as not run.**
An agent failed twice, or could not reach the files. A failed agent is
launched once more with the cause fixed; after a second failure the step is
reported as not run. Claude does not quietly do a reviewer's job itself.

**The work stopped and asked a question.**
A limit was reached, or a decision came up that only you can make. Answer the
question, or say what to drop.

**An agent could not reach the files.**
Before giving an agent files to change, Claude checks the agent can reach
them. If it cannot, the step is reported as not run, not quietly skipped.
