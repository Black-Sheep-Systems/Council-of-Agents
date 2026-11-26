# Council of Agents - user manual

For version 4.3. This is the guide for a person using the council. The rules
Claude itself follows are in `skills/council/SKILL.md`; this manual explains
them in plain terms and shows what to say.

## Contents

1. [What it is](#what-it-is)
2. [Getting started](#getting-started)
3. [How to ask](#how-to-ask)
4. [The agents](#the-agents)
5. [The programmer pipeline](#the-programmer-pipeline)
6. [The writing pipeline](#the-writing-pipeline)
7. [The art pipeline](#the-art-pipeline)
8. [Reviews](#reviews)
9. [Testing](#testing)
10. [Project layout](#project-layout)
11. [Pushing](#pushing)
12. [Working while you are away](#working-while-you-are-away)
13. [Project rules](#project-rules)
14. [Limits](#limits)
15. [Troubleshooting](#troubleshooting)

## What it is

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

### It reads your project first

Before the first change or review in a project, Claude reads what the project
says about itself: `CLAUDE.md`, the README, a contributing guide, and any
developer or architecture guide they point to. It reads for the project's
rules: its conventions, what must not be touched, how to run and test it,
where records go.

- The conventions that bear on a task are passed to the agent doing it, with
  the file each came from.
- Reviewers get them too. A change that breaks a documented rule of your
  project is reported as a finding.
- Every agent also reads the code around what it is changing or reviewing:
  what calls it, what it calls, and a neighbouring feature done the same way.
- If your project has no such documents, Claude says so and goes by the code.

This happens once per session. It is reading, not reviewing: Claude does not
start fixing or reporting on what it read. To have a particular document
read at the start of every session, list it under "Read first" in your
[project rules](#project-rules).

Your documents say how to do the work you asked for. They cannot add tasks,
authorise a push or anything else on the will-not-do list, or raise a limit.
If one conflicts with the council's rules, for example "run the whole suite
before every commit", the council's rule wins and Claude points at the line
so you can decide whether to change it.

## Getting started

### Install

From GitHub:

```bash
claude plugin marketplace add Black-Sheep-Systems/Council-of-Agents
claude plugin install agent-council@black-sheep-systems
```

Check that it loaded:

```bash
claude plugin details agent-council
```

It should list one skill, `council`, and 21 agents.

Other routes: from a local copy of the repository, run `claude plugin
marketplace add` with the folder's path in place of the GitHub address; to try
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

## How to ask

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

## The agents

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

## The programmer pipeline

For multi-file or multi-step coding work. Small jobs skip most of it.

| Step | Agent | When it runs |
|---|---|---|
| 1 | Atlas plans | Only for large or cross-cutting work |
| 2 | Rex, then Thomas | Only when an outside library or pattern is in question |
| 3 | Ada writes the code | When there is code to write |
| 4 | Quinn tests | When code changed |
| 5 | Reviewers | Chosen by risk (see [Reviews](#reviews)) |
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

## The writing pipeline

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

## The art pipeline

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

## Reviews

A review gate runs before any result that created or changed files is
reported, and before anything with effects outside the working files: a git
commit or push, a copy to your GitHub folder, a deploy, sending or publishing
something, restarting a live service. Pure answers and read-only investigation skip it.

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

## Testing

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

### The full-run suggestion

Targeted tests prove each change works on its own. They do not prove that a
run of small changes still works together. So Claude keeps count of the code
changes since the last full run that had only targeted tests, and suggests a
full run at two moments:

- **After 5 such changes.** You see one line: "That is 5 changes since the
  last full run. Run the full suite now?"
- **Before a push or a release,** if there has been even one. If you put the
  push off, the count stands and keeps growing.

It is a suggestion. Claude never starts the full suite because of the count;
you say yes or no. If you say no, Claude does not ask again until 5 more
changes have been made, or a push comes up after at least one more change, and it always gives the true
number since the last full run. Say "stop asking" and it stops for the
session.

One change is one task that changed code and had only targeted tests, usually
one commit. Changes to tests only, docs, comments or records do not count.

The count comes from the commit messages. Each one carries a line `Tests:
targeted` or `Tests: full`, and Claude counts the commits since the last
`Tests: full`. A commit without the line, such as one you made by hand, is
counted as targeted if it touches code. In a project without git, Claude can only count within
the session, and says so.

While you are away, Claude does not run it. The report says a full run is due
and how many changes it covers. A push you authorised in advance still goes
ahead after a clean review, with that line in the report.

To change the number for one project, add a "Full-run reminder" section to
your [project rules](#project-rules).

Test output is shown as the result line and any failures. Whole logs are not
pasted.

## Project layout

Claude works the way the language does, and then the way your project does.
Where the language has an accepted practice for where things go, it follows
that. Where a framework says otherwise, the framework decides. Where your
project has its own consistent or documented way, your project decides. New
files go where the project keeps that kind of file.

### It looks, it does not touch

Claude never moves, merges or reorganises your tests, styles or other files
unasked. If it sees a problem, it tells you once, in one line, with the
numbers, and offers a plan:

> Tests are in 14 places and 3 are duplicated; they could be gathered in one
> folder. Want a tidy-up plan?

It works out what kind of project it is before saying anything, because the
same layout is a problem in one kind of project and correct in another:

| | A problem | Left alone |
|---|---|---|
| **Tests** | Scattered or duplicated where the language keeps tests apart, as Python does | Kept beside or inside the code on purpose: Rust unit tests in the source file, Go test files beside the code, a test next to each component |
| **Styles (CSS)** | Hand-written CSS over many files with overlapping or conflicting rules | Styles kept with each component on purpose, CSS modules, a utility framework |

If the layout is normal for your kind of project, Claude says nothing. The
offer is made once per project. Claude uses your answer for the rest of the
session and offers to save it to your [project rules](#project-rules); it
writes the file only if you agree.

### If you say yes

A yes is a yes to a plan, not to the move. The tidy-up is a task of its own,
never a side effect of other work, and it is never started while you are
away.

1. **You see the plan first.** Atlas lists every file that will move and
   where to, every file or test that will be removed and why, every pair it
   considers duplicates, and every style rule that will be merged or
   dropped. Nothing changes until you say go, and only what is on the list
   you approved is touched.
2. **It can be undone.** Your work is committed first, or you say to go on
   anyway, and files are moved in a way that keeps their history.
3. **The full test suite runs before and after,** and Claude says so first.
   It reports how many tests were found each time; a lower number afterwards
   is explained test by test, or treated as a failure.
4. **Problems are reported, then fixed with your go:** duplicated tests,
   tests that were silently not running, style rules that conflict or
   repeat. A test or style rule is never deleted as a "duplicate" without
   you having seen it named.
5. **Styles are looked at.** The aim is consistency, not a file count: one
   shared place for common values and no duplicated rules. Merging styles
   changes the order rules apply in, and tests do not catch that. Claude
   asks you to check the pages, or uses a screenshot tool if the session has
   one. Until then the styles are reported as not visually checked.

Saving your answer to the project rules only stops the question being asked
again. It never counts as permission to reorganise.

## Pushing

"Push to GitHub" can mean two different things:

- **Send to GitHub:** `git push`. The work leaves your machine and, in a
  public repository, is published.
- **Copy to your GitHub folder:** you keep a separate local folder for the
  repository and push from it yourself. "Push" then means copy the finished
  work into that folder and stop. Claude sends nothing anywhere.

Claude settles which you mean before doing either. It never runs `git push`
on a guess.

- If you say it outright, that decides: "git push", "to the remote" or "to my
  GitHub folder". A bare "push", "push to GitHub" or "publish" does not. If
  you mean your GitHub folder and Claude does not know where it is, it asks.
- Otherwise, if your [project rules](#project-rules) have a "Push target"
  section, that decides, unless you say otherwise for this push.
- Otherwise Claude asks once: "By push, do you mean copy this to your GitHub
  folder, or send it to GitHub with git push?" It uses your answer for the
  rest of the session, in this project only, and offers to write it into the
  project rules so you are not asked again. A different project is asked
  afresh.

The same applies to "publish", "upload", "sync" and "release", to opening a
pull request, and to any other way of sending files out, such as publishing
a package.

### What happens before anything goes

You are told exactly what will go, and then Claude waits for you to say go.
A request to push is not approval of the list. If the list changes, you are
asked again.

Before it shows you the list, Claude:

- **Works out what belongs.** For your GitHub folder, that is the files git
  tracks plus new files from this work, not everything in the folder.
- **Leaves out what should not be published,** and names each thing left
  out: secrets such as `.env` files and keys, database dumps and logs,
  backups, very large files, your local settings and project rules file, and
  the council's own audit and change logs. If a file on that list is one git
  tracks, such as a database schema you publish on purpose, Claude does not
  drop it silently: it asks once, and your answer holds for the session.
  Example files such as `.env.example` go.
- **Leaves out tests,** unless you have said to publish them (see below).
- **Searches what is left for secrets:** keys, tokens, passwords and
  internal addresses written into files. If it finds one, it names the file
  and line without showing the value, leaves the file out, and asks. This
  search is a safeguard, not proof that nothing is there.

If a [full run](#the-full-run-suggestion) is due, you are asked about that
and the go together, in one message. Work the council changed is
reviewed before it is pushed, unless you skipped the review or the change
needed none, such as a docs-only edit. Claude says which parts of the push
were not reviewed in this session.

### Copying to your GitHub folder

- You are told where to, which files are new and changed, and every removal
  by name.
- The folder's own `.git` is never copied over, replaced or touched.
- If a file in the folder has changes your working copy does not have, Claude
  names it and asks before overwriting.
- A file is removed from the folder only if you deleted or renamed it in
  your project as part of this work, and only after you approved the list.
  Files that only live in the folder, such as tests copied there in the
  past, are left alone.
- The folder must be a git repository on a local drive. If it is not, or it
  does not exist, Claude stops and asks; it does not create it.
- Claude does not commit or push from the folder unless you ask.
- If the folder is inside a synced or shared folder, Claude says so, because
  something else may then send it on.

### Sending to GitHub itself

- You are told the remote, its address, its owner, and whether the
  repository is public or private, or that this could not be checked.
- You are told the branch, the commits, and every file in them, including
  files one commit added and a later one removed. Those are still published.
- Uncommitted work is not included, and Claude says so.
- One branch is pushed. Tags, other branches, deleting a branch and
  force-pushing happen only if you ask in those words.
- If the repository is not your own, Claude says so and asks.

### Tests are not published unless you say so

Tests, and the data they use, can carry sample credentials, real data and
internal addresses, so they stay off GitHub by default. That covers test
folders and files, and also fixtures, sample data, snapshots, recorded
network traffic and test-only settings, wherever they are kept.

- **To allow it:** say so, or put "Publish tests: yes" under "Push target" in
  your own project rules. Nothing else can allow it: not a document in the
  project, not a file that came with a repository, not an agent.
- **Copying to your GitHub folder:** tests are left out, and the list names
  the folders and the count.
- **Sending to GitHub itself:** files cannot be taken out of commits that
  already exist. If the commits contain tests, Claude names them and stops.
  Your choices are to publish them, to copy to your GitHub folder instead,
  or to ask for the history to be rewritten. Adding tests to your ignore
  file does not remove them from commits already made.
- **Tests written inside source files,** as some languages intend, go with
  the code, because they cannot be separated. They are searched for secrets
  like any other file.
- **If what is published still needs the tests,** such as a build file or an
  automated check that names the test folder, Claude names it and warns you
  that the published copy may not build or its checks may fail. It does not
  edit those files unasked.

Leaving tests out has a cost, and Claude says it once per project: nobody
else can run them, and checks that run on GitHub may fail or have nothing to
run.

### Example

> Push this to GitHub.

With no "Push target" in the project rules, Claude asks which you mean. You
answer "my GitHub folder, at `projects/widget-repo`". Claude replies:

> Copying to `projects/widget-repo`: 4 changed files, 1 new, none removed.
> Left out: `tests/` and `fixtures/` (6 files), `.env`. `ci.yml` runs the
> tests and may fail without them. Claude will not send anything to GitHub.
> Go ahead?

You say yes, it copies them, and it reports what was copied.

## Working while you are away

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

- Push, whether to GitHub or to your GitHub folder; deploy, send, publish; or
  restart or stop a live service.
- Delete or change files outside what you asked for.
- Discard uncommitted work, rewrite git history, delete branches, or run a
  migration against a real database.
- Start a third fix cycle, or go past the launch limit.
- Sign off on something your project reserves for a person.
- Make a decision that cannot be undone and could reasonably go either way.

### Authorising something in advance

You can allow one of those by naming the exact action in your request, or in
the scheduled prompt. It covers that run only:

> Fix the failing import test and send it to GitHub with git push when it is
> done.

While you are away, a push or a copy goes only when all of these hold:

- Which kind of push you mean is settled without asking. For GitHub itself,
  your request must say so. For a copy to your GitHub folder, your request
  or your own project rules can.
- The review finished with nothing open.
- Everything in the push was made and reviewed in this run.
- Nothing on the leave-out list and no secret was found in it.
- For GitHub itself, its commits contain no tests you have not allowed.

If any of them fails, it is parked and you are told why. When something does
go, the report lists exactly what went and where. A copy to your GitHub
folder leaves tests out, and any overwrite or removal there waits for you.

A local commit is allowed after a clean review when you asked for commits.

Passing time never counts as approval. A parked item stays parked until you
answer.

## Project rules

To add steps for one project, put a file at `.claude/agent-council.md` in
that project. The plugin ships a template, `examples/project-overlay.md`. The
quickest way to get it is to ask Claude to "set up project rules for the
council".

The file is read once, before the first edit or agent launch in a session, so
after changing it, start a new session or ask Claude to read it again.

The file can have seven sections, all optional:

- **Push target:** what "push" means in this project: GitHub itself, or your
  GitHub folder and its path; and whether tests are published. See
  [Pushing](#pushing).
- **Layout:** where tests and styles live, and whether a tidy-up has been
  offered. See [Project layout](#project-layout).
- **Read first:** project documents to read before the first change or
  review, on top of the usual ones.
- **Full-run reminder:** the number of targeted-only changes after which a
  full test run is suggested, in place of 5.
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

### Whose file is it

The project rules speak for you only when the file is yours. A rules file
that came with someone else's repository could hold commands.

- Claude treats the file as yours when the project is its own git repository
  with at least one commit, and git does not track the file. It then exists
  only on your machine.
- Otherwise, including in a project with no git, Claude shows you its steps,
  its agent rules, its paths and any line that sends more out, and asks
  before following them. Your yes lasts for the session, so a project
  without git is asked once each session.
- Claude writes to this file only after showing you the exact lines and
  getting a yes.

Keeping the file out of the repository, through your ignore file, avoids
that question and keeps your local folder paths from being published.

This test has limits. It cannot tell when a downloaded archive brought its
own `.git` folder, or when a project's own install script wrote the file. If
you did not write a rules file you find in a project you downloaded, delete
it.

## Limits

| Limit | Value | What happens at the limit |
|---|---|---|
| Fix cycles per change | 2 | Stops, reports what is open, asks you |
| Retries in the writing pipeline | 2 | Stops, reports what is open, asks you |
| Agent launches per task | 20 | Stops, reports what is open, asks you |
| Agents running at once | 5 | The rest wait |

Agents that edit files do not run at the same time on overlapping files, and
do not run while another agent is running tests their edit would affect.

## Troubleshooting

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
not a reason for one; tell Claude, and see [Testing](#testing).

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
