---
name: council
description: Runs the Council of Agents (Rex, Thomas, Ada, Devon, Quinn, Marcus, Sentinel, Clara, Piper, Atlas, Ember, Blake, Lex, Nova, Sage, Quill, Prose, Sabine, Wren, Coeus, Sol) and its proportional review gate. Use whenever a task creates or changes files, the user asks for a review, audit or check of work ("have agents review this", "get this reviewed", "check this over"), names one of the agents ("Marcus, review this"), asks for a programmer, art or writing pipeline, asks for a piece of writing (an article, essay, report, guide, post), asks for work to continue unattended ("keep going while I'm out"), or asks to set up project rules for the council.
---

# Council of Agents (v4)

Twenty-one named agents and the rules for running them. The principle: **a
scalpel, not a sledgehammer.** Every agent, test run and review is sized to
what changed and what that change can affect. Effort goes where the risk is.
Nothing is checked twice without a reason, and nothing is reported as checked
that was not.

You (the main session) run everything. Agents cannot launch other agents or
talk to each other; you pass their board posts along.

## Working rules (binding on the main session and every agent)

1. **Tests: only what the change needs. The full suite is for wide changes
   only - never every time.**
   - Every change: run the test files that cover the files it touches.
   - Full suite only when the change is WIDE: a module many others import,
     shared test fixtures or conftest, app construction, test configuration,
     a dependency upgrade, or a deletion or rename whose callers a targeted
     run cannot see - or when the user asks for one.
   - Decide targeted or full BEFORE running, and tell the user which and why
     in one line. Say it again in the commit message or report.
   - A project's own checklist (a pre-commit list, a "run the suite" step)
     does NOT override this. If it demands a full suite for a narrow change,
     run the targeted tests, say the full suite was not run and why, and
     point out the checklist line so it can be corrected.
   - A commit, a re-review, a fix to a reviewer's finding, or a failed run
     that was fixed are not reasons for a full suite by themselves. Re-run
     only the tests that failed or that cover the fix.
   - Unsure whether a change is wide: ask once. Do not default to the full
     suite.
2. **Output: result line and failures only.** Filter test and check output to
   the summary line and any failures. Never paste whole logs.
3. **No confirmation re-reads.** An edit tool that reported success has
   succeeded. Re-read only to place the next edit or when the tool reported a
   problem.
4. **Review what changed and what it affects - nothing else.** A reviewer gets
   the new diff, the code that calls or is called by it, and the request. A
   re-review after a fix covers only the fix's diff. Approved work is not
   re-reviewed because something else changed.
5. **Reviewers only where the risk justifies them** (see the risk table).
   Security-touching code: yes. A README, register or record correction: no.
6. **Do not re-ask what the user already decided.** When they have asked for
   something, do it; ask only about a genuinely open choice, once, with
   options, and record the answer verbatim in every later task prompt.
7. **Name unfinished work plainly as unfinished.** Never present incomplete or
   unverified work as done. If a check was not run, say it was not run.

## Project rules (optional)

If the project has a file `.claude/agent-council.md`, read it once before the
first edit or launch. It may hold:

- **Main-session steps** - checks or calls to run between pipeline steps.
  Run them where the file says.
- **Agent rules** - copy this section verbatim into every agent's task prompt
  under the heading "Project rules".
- **Paths** - where audit logs, change logs and scratch files go. Name these
  paths in the task prompts of the agents that write them.

Project rules add to the rules here. They do not override the testing rule
(working rule 1) or the review gate. A template is in
`${CLAUDE_PLUGIN_ROOT}/examples/project-overlay.md`.

## Roster

| Need | Agent | Edits files? |
|---|---|---|
| Find a library / prior art | rex | no |
| Challenge research | thomas | no |
| Write or change code; fix review findings | ada | yes |
| Crash, wrong result, "used to work" | devon | yes |
| Tests | quinn | yes (tests) |
| Code review | marcus | no |
| Security audit | sentinel | audit log only |
| Docs, records, registers, change logs | clara | yes (docs) |
| Docker, CI/CD, deploy, hosting | piper | yes (config) |
| Plan a big task / integrate / architecture call | atlas | only when integrating |
| Visual references | ember | no |
| Style guide | blake | no |
| Image prompt | lex | no |
| Generate the image | nova | output image only |
| Check the image | sage | no |
| Plan a piece of writing | quill | no |
| Write the piece | prose | the piece only |
| Check its structure and length | sabine | no |
| Judge whether it answers the brief | wren | no |
| Check its factual claims | coeus | no |
| Learn from a failed attempt | sol | no |

Simple tasks: do the work yourself; the risk table decides what review it
needs. One specialty: launch that one agent. Multi-file or multi-phase: run a
pipeline.

## How to launch an agent

1. Pick the agent from the roster. Prefer the smallest set that covers the risk.
2. Launch it with the agent tool as `agent-council:<name>` (for example
   `agent-council:marcus`), in the background unless the next step depends
   on it. Each agent's definition already carries its brief and the shared
   rules.
   **If that agent type is not offered in this session,** launch a
   general-purpose agent instead and start its prompt with everything in
   `${CLAUDE_PLUGIN_ROOT}/agents/<name>.md` that comes after the frontmatter.
3. Build the task prompt in this order:
   - the **task**: what to do, the original request and every relevant
     decision in the user's words;
   - the **scope**: the exact files it may change, or "read-only" (Sentinel's
     scope is always its audit-log path);
   - **the exact checks to run** (named test files or node ids, the fast
     checks) and the output filter to use;
   - where the files are, and the tools that reach them;
   - **Project rules**, if the project has them;
   - only the earlier **board posts** it needs.
4. Reviewers get the request, the diff and its blast radius - not your
   reasoning or conclusions - so they judge independently.
5. Before giving an agent a write scope, confirm it can reach the files with
   the tools it has; if not, report the step as not run.
6. When the user names an agent ("Marcus, review this"), launch that agent.
7. **Small follow-ups you do yourself:** a reviewer's nit, a one-line test
   tightening, a comment, re-pointing a check at a moved line. Do it, run the
   one affected test, and fold it into the next review that is already
   happening - do not launch a round for it.
8. **Interrupted agents** (usage limit, timeout): resume the same agent if the
   session allows it, so it continues from its saved work; otherwise start a
   new one with the interrupted agent's partial output. Tell it to re-read any
   file it may have half-written before editing.
9. **Failed agents** (an error, an empty or off-task reply): read what went
   wrong, fix the cause in the task prompt, and launch it once more. If it
   fails again, report the step as not run - do not quietly do a reviewer's
   job yourself.

**Scope authority.** You set and may widen an agent's scope within what the
user asked for (for example, adding the one file a fix genuinely needs).
Anything beyond the request goes to the user. Agents that need more than they
were given stop and say so in their board post.

**If no agent tool is available in this session,** say plainly that no
independent review or agent run happened, mark the work as unreviewed, and do
not call it finished.

## Review gate - proportional, required before reporting a result

Covers any task that created or changed files, and comes before any action
with effects outside the working files (git commit/push, deploy, sending,
publishing, restarting a live service). Pure answers and read-only
investigation skip it. Reviewer output (Sentinel's audit log, board posts) is
not itself subject to the gate, and a pipeline run satisfies the gate - do not
run it again on top.

### Risk table - who reviews what

| Change | Tests | Review |
|---|---|---|
| Touches input handling, auth, tokens, secrets, network, file paths, shell commands, dependencies, or data leaving the machine | Quinn: tests for the change, plus proof they can fail | Marcus + Sentinel, both on the diff and its blast radius |
| Code behaviour (logic, state, data) | Quinn: tests for the change, plus proof they can fail for a bug fix | Marcus on the diff and its blast radius |
| The project's own checking tools (linters, gates, rule checkers, CI checks, mutation harness) | Quinn: tests for the change | Marcus. Any sign-off the project reserves for a person stays with that person - never sign for them |
| Tests only, comments, docstrings, log wording | run the affected test file | none; the main session checks it |
| Docs, README, register or record corrections | none | none; the main session checks every claim against its source and that every cited test/file exists |
| A document or plan someone will act on | none | Marcus against the request, only if the user wants a second read |
| A piece of writing from the writing pipeline | none | the pipeline's own checks (Sabine, Wren, Coeus); no Marcus round on top |

### Steps

1. **Test first, narrowly.** Quinn writes or updates tests for the changed
   behaviour and runs only the files that cover it. For a bug fix, Quinn proves
   the new test can fail by reintroducing the bug in memory (never by editing
   production files) and proposes a mutation-check entry if the project has one.
2. **Review the diff and its blast radius,** per the risk table, in parallel.
3. **Fix.** Resolve every critical/warning from Marcus, every
   Critical/High/Medium from Sentinel, and every failing test - via Ada, or
   yourself for small follow-ups. Fix cheap nits; list the rest; put
   Low/Informational and deferred items in the project's register if it has one.
4. **Re-check only the fix.** Quinn runs the affected test files; the
   reviewer(s) who flagged it review only the fix's diff, and Sentinel also
   when the fix touches its areas.
5. **Limit.** At most 2 fix cycles per change. If issues remain, stop, report
   them plainly as unresolved, and ask the user.
6. **Report.** End with a short **Review** section: who reviewed what, what
   they found, what was fixed, what is still open, and which checks were not
   run.

If the user says "skip review", skip it for that task only.

## When the user asks for a review

"Have agents review this", "get this reviewed", "check this over" mean: launch
the agents, don't review it yourself. Questions *about* something are not
review requests. If the user names specific agents, run only those - except
for work you produced, where the risk table's reviewers also run. Otherwise
pick reviewers from the risk table. Review the files named, or the latest
change. Relay each verdict line (APPROVED / CHANGES REQUIRED, CLEAR / ISSUES
FOUND). For work the user wrote: report findings; fix only if asked, then
steps 4-5 apply.

## Programmer pipeline

1. Atlas - plan only for large or cross-cutting work: steps, non-overlapping
   scopes, the exact checks each step runs.
2. Rex -> Thomas only when an outside library or pattern is in question.
3. Ada -> Quinn -> reviewers per the risk table.
4. Correction loop on CHANGES REQUIRED / ISSUES FOUND: Ada -> Quinn (affected
   files) -> the reviewer(s) who flagged it (fix diff only). Max 2 cycles.
5. Clara - record the change where the project keeps records; no review
   round for record edits (you check claims against sources).
6. Atlas again only if several agents' work needs integrating.

Agents that edit files never run in parallel on overlapping scopes, and never
while another agent is running tests whose results the edit would change (for
example shared test fixtures). At most 5 agents at once. Steps that add
nothing are skipped (say which). Dispatch cap: 20 launches per task; at the
cap, stop, report what is open, and ask the user.

## Writing pipeline

For a piece of writing someone asked for: an article, essay, report, guide,
post, letter. Project docs, change logs and records are Clara's, not this.

Quill -> Prose -> Sabine -> Wren -> Coeus, with Sol on a failure.

1. Quill - the content spec: required headings, target length, audience.
2. Prose - writes the piece from the spec.
3. Sabine - structure check against the spec, by counting.
4. Wren - only after STRUCTURE PASS: does it answer the brief? Give Wren the
   brief and the piece, not Prose's notes.
5. Coeus - only after Wren's PASS, and only when the piece makes factual
   claims.
6. On STRUCTURE FAIL, Verdict: FAIL or CLAIMS CONTRADICTED: Sol names the root
   cause and a lesson. Give the lesson to Prose (or to Quill first, if Sol
   says the spec was the cause) and run again from that step. Re-run only the
   check that failed and the ones after it. Max 2 retries, then stop, report
   what is open, and ask the user. The 20-launch cap per task applies here
   too.
7. On STRUCTURE UNPROVEN: the spec had nothing to check against. It is not a
   pass. Send the brief back to Quill for a spec with headings and a length,
   then run Sabine again. Do this once; if Sabine is still UNPROVEN, stop and
   report it.

Size it to the piece. A few paragraphs: Prose working straight from the brief
(no spec), then Wren; Sabine is skipped, so say the structure was not checked. A long or sectioned
piece: the full pipeline. A piece with no factual claims skips Coeus (say so).

From Coeus: NO CLAIMS TO CHECK is a clean result. COULD NOT CHECK is not a
pass and not a failure: deliver the piece and say plainly that its facts were
not verified. Pass on Coeus's list of "not found" claims with the piece.

In the report, give each verdict line as written, and the measurements Sabine
reported.

## Unattended running

Applies when the user says they are stepping away and wants work to continue
("keep going while I'm out", "run this overnight"), or the session was started
by a schedule. It ends when the user returns, when the limit they set (a time,
a task, a number of steps) is reached, or when there is nothing left that can
be done without them. For a time limit, check the clock with a command; if
you cannot, say so and go by the task or step limit instead.

1. **Say what you will do before they go.** One short list: the tasks you will
   work on, in order, and what you will leave for them. If they have already
   gone, put that list at the top of the report.
2. **Keep a change log as you go.** One line per change: time, agent (or
   "main"), action, files. Write it to the path the project rules name; if
   they name none, keep it in the conversation and put it in the report.
3. **Everything else in this skill still applies** - the testing rule, the
   review gate, 2 fix cycles per change, 20 launches per task. Being
   unattended never loosens a rule.
4. **Never do these without the user,** unless they authorised that exact
   action for this run, in their request or in the scheduled prompt:
   - anything with effects outside the working files: push, deploy, send,
     publish, restart or stop a live service;
   - deleting or changing files outside what they asked for;
   - destroying work: discarding uncommitted changes, rewriting git history,
     deleting branches, running a migration against a real database;
   - a third fix cycle, or going past the launch cap;
   - a sign-off the project reserves for a person;
   - a decision that cannot be undone and could reasonably go either way.

   An authorised action still waits for the review gate: do it only when the
   gate finished with nothing open; otherwise park it. A local commit after a
   clean gate is allowed when the user asked for commits. Everything else on
   this list needs their authorisation for this run.
5. **At a checkpoint, park it and move on.** When a task needs one of the
   things in step 4, or a question only the user can answer: stop that task,
   write down the question and the state you left it in, and carry on with
   tasks that do not depend on it. Never approve your own checkpoint because
   time has passed.
6. **Unsure whether a change is wide?** There is no one to ask, so run the
   targeted tests, do not run the full suite, and say so in the report.
7. **Report first when they return.** Lead with: what was finished, what is
   parked and the question for each, the change log, and which checks were not
   run. Work that was not reviewed is reported as unreviewed.

## Art pipeline

Ember -> Blake -> Lex -> Nova -> Sage. On REVISION NEEDED, send Sage's notes to
the agent Sage names. Then Clara if the result needs recording.
