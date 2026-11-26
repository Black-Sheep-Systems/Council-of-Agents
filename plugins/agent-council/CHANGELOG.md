# Council of Agents - version history

The newest version is first. Each entry says what changed from the one before
it and what that means for someone using the team.

Versions 1 and 2 were not numbered at the time. Their numbers, and the months
given for versions 1 to 3, were worked out afterwards from the files and the
dates they were last changed.

## Version 4.3.4 - 2026-11-26

**Changed**

- **Every agent can now look at files on the user's computer, in the folders
  the user has connected to the session.** No agent is given a tool that
  reaches the user's files outside those folders, and none can ask for more.
  The device shell is a sandbox on the user's computer with its own scratch
  space; it sees the connected folders and nothing else of the user's.
- **The build agents (Ada, Atlas, Clara, Devon, Piper, Quinn) can change
  files there.** They have the device shell and write-back. Every other
  agent can only copy files in; what they write (Prose's piece, Sentinel's
  audit log, Nova's image) comes back to the main session to place.
- **Nova now has a tool list.** It had none, so it inherited every tool,
  including ones that reach the whole computer. It now has an explicit list:
  it can copy files in, like every agent that does not build, and denies the
  browser tools as well.
- **Guard rails on the device shell, in every agent's rules:** never
  overwrite a file the user changed meanwhile (`force=true` is forbidden),
  never discard work (`git reset --hard`, emptying files and the like), no
  network commands unless the task names them, and nothing sent anywhere.
  These are instructions; the tools enforce the folder limit, not these.
- **The rule lives in one place:** the shared rules, so all 21 agents carry
  the same text.

## Version 4.3.3 - 2026-11-26

**Changed**

- **Marcus and Sentinel can no longer list folders on the user's computer.**
  Listing a folder outside the connected ones still showed its sub-folder
  names, and a reviewer could take what it saw as something it may reach
  for. They keep only copying in files their task names, from connected
  folders; everything else is refused.
- **The main session gives a reviewer the listing instead.** Step 5: a
  reviewer working on files on the user's computer gets a listing of the
  connected folder in its task, so it sees what it has access to and has no
  way to look anywhere else.

## Version 4.3.2 - 2026-11-26

**Added**

- **Marcus and Sentinel can reach files on the user's computer** when the
  session runs in the cloud and is linked to it: each can list a folder and
  copy files in. Only folders the user has connected to that session; they
  cannot ask for more, and they cannot run anything on the user's computer. Each
  copies in only the files its task names.

**Changed**

- **Step 5 of launching an agent covers reviewers.** A reviewer that cannot
  reach the files gets copies of exactly what it needs, named in its task, or
  the review is reported as not run.

## Version 4.3.1 - 2026-11-26

**Added**

- **Do what was asked, and stop** (working rule 8). No looking for further
  problems, widening a review, or fixing nearby issues unless the user asks.
  Findings about the change itself are still fixed; anything outside it gets
  one line under "Noticed, not in scope". The skill's own offers and
  prompts, and Sentinel's audit log, are unchanged.
- The same rule, in one line, in every agent's shared rules, so it reaches
  the agents and not only the main session.

**Changed**

- Review gate step 3 fixes reviewer findings about the change (rule 8).

## Version 4.3.0 - 2026-11-24

**Added**

- **Project layout.** Claude follows the language's accepted practice, then
  the framework's, then the project's own. It never moves or merges files
  unasked. If tests or hand-written styles are scattered in a way that is a
  problem for that kind of project, it says so once, in one line, and offers
  a tidy-up plan. A tidy-up the user accepts is a task of its own, with a
  full test run before and after and, for styles, a look at the result.
- **Tests are not published unless the user says so.** Test folders and test
  files are left out of a copy to a staging folder, and a push to the remote
  stops and asks if its commits contain them. Tests written inside source
  files go with the code.
- **A leave-out list and a secrets check before anything is published.**
  Secrets, data dumps, logs, local settings and the council's own logs are
  left out and named, and what remains is searched for keys, tokens and
  passwords. The full rules are in `skills/council/references/pushing.md`.
- **Stricter pushes to the remote.** One named branch; the address, owner and
  visibility are stated; every file in every commit is listed; tags, other
  branches and force-pushes only when asked for in those words.
- **Whose file is it.** A project rules file that git tracks may have come
  with the repository, so its steps and any line that sends more out are
  shown and confirmed before they are followed.
- **A project-rules section,** "Layout", and a "Publish tests" line under
  "Push target".

## Version 4.2.0 - 2026-11-24

**Added**

- **What "push" means.** "Push to GitHub" can mean sending commits to the
  remote, or copying the finished work into a separate local folder the user
  pushes from themselves. Claude now settles which is meant before doing
  either, says exactly what will go and where, and waits for the go-ahead. It
  never runs `git push` on a guess.
- **A project-rules section,** "Push target", so the question need only be
  answered once per project.

## Version 4.1.0 - 2026-11-24

**Added**

- **Know the project first.** Before the first change or review in a
  project, Claude reads what the project says about itself (`CLAUDE.md`, the
  README, contributing and developer guides) and passes the conventions that
  bear on each task to the agent doing it. Reviewers get them too, so a
  change that breaks a documented rule of the project is a finding. Every
  agent is also told to read the code around what it changes or reviews.
- **Full-run reminder.** After 5 code changes that had only targeted tests,
  and before a push or release when at least one such change is waiting,
  Claude suggests a full test run and waits for the answer. It never starts
  one on its own. The number can be set per project. Commit messages now
  carry a line `Tests: targeted` or `Tests: full`, which is what the count is
  taken from.
- **Two project-rules sections:** "Read first" and "Full-run reminder".

**Unchanged**

- Targeted tests are still the default, and the full suite still runs only
  for a wide change or when the user says yes.

## Version 4.0.0 - 2026-11-24

The first version packaged as a plugin that other people can install, and the
first under the name Council of Agents (`agent-council`). Versions 1 to 3
went by an earlier name, taken from the assistant the roster was first written
for; the plugin no longer depends on it.

**Added**

- **Writing pipeline and six agents.** Quill plans the piece, Prose writes it,
  Sabine checks its structure by counting, Wren judges whether it answers the
  brief, Coeus checks its factual claims, and Sol turns a failed attempt into
  a lesson for the retry. The team goes from 15 agents to 21, and from two
  pipelines to three.
- **Unattended running.** Rules for working while the user is away: a change
  log, a fixed list of actions it will not take without them, parking a
  question instead of guessing, and a report that leads with what is waiting.
  An action authorised in advance still waits for a clean review.
- **Project rules.** A project can add its own steps, agent rules and file
  paths in `.claude/agent-council.md`. They add to the team's rules and cannot
  override the testing rule or the review gate.
- **A user manual,** `MANUAL.md`.
- **Licence.** MIT, copyright Black Sheep Systems; `LICENSE` ships with the
  plugin.
- **Failed agents.** If an agent errors or goes off task, the cause is fixed
  and it is launched once more; a second failure is reported as a step that
  was not run.

**Changed**

- **Agents are installed, not pasted.** Each agent is its own file and is
  launched by name as `agent-council:<name>`. In version 3 the main
  session pasted a brief into a general-purpose helper every time.
- **Agent files use the fuller layout** of the version 2 files (Identity,
  Purpose, numbered method, Guardrails) with version 3's rules. Details that
  version 3 had dropped were restored where they do not conflict with it:
  how Marcus finds the change to review, Sentinel's dependency-audit tools and
  finer checklist, web lookup for Sentinel and Piper, Clara's guidance for
  minutes and manuals, Quinn's edge-case list, and two review-gate
  clarifications (reviewer output is not itself subject to the gate; a
  pipeline run satisfies the gate).
- **Shared rules have one source.** The rules every agent follows live in one
  file and the build copies them into each agent.
- **Written for anyone.** The rules address "the user"; nothing refers to one
  person, one machine or one project.

**Removed**

- Steps that belonged to a single private project. They moved to that
  project's own `.claude/agent-council.md`.

**Unchanged from version 3**

- The testing rule: targeted tests by default, the full suite only for wide
  changes, said before running.
- The proportional review gate and its risk table, the limit of 2 fix cycles
  per change and 20 agent launches per task.

**Not yet done**

- This version has passed Claude Code's plugin validator and an independent
  review of its text. It has not yet been installed and run end to end.

## Version 3 - November 2026 (approximate)

"A scalpel, not a sledgehammer." Kept as a single skill that carried a short
brief for every agent.

- **Proportional review gate.** A risk table decides who reviews what.
  Security-touching code gets Marcus and Sentinel; ordinary code gets Marcus;
  a README or record correction gets no review round. Before this, Marcus
  reviewed everything.
- **Targeted tests.** Run the tests that cover the change. The full suite is
  for wide changes only, the choice is stated before running, and a project's
  own checklist does not override it.
- **Review only what changed and what it affects.** A re-review covers only
  the fix.
- **No confirmation re-reads** after an edit the tool reported as successful.
- **Scope.** The main session may widen an agent's scope within what the user
  asked for. Before this, only the user could.
- **Small follow-ups** are done by the main session without a new review
  round.

## Version 2 - October 2026 (files last changed)

The team as Claude Code subagents: 15 agent files copied into the user's
agents folder by an install script, plus a roster block for the main session.

- **A review gate** before any result was reported: Quinn tests, Marcus
  always reviews, Sentinel when the change touches security.
- **The main session became the coordinator.** Subagents cannot launch
  subagents, so Atlas returns a plan and integrates results instead of
  dispatching the others.
- **Board posts.** Each agent ends with a board post that the main session
  passes to the next agent, in place of a shared message board.
- **Reviewers became read-only.** Sentinel writes only its audit log.
- Limits of 2 correction cycles and 20 launches per task.

## Version 1 - May 2026 (files last changed)

The original roster, written for the assistant it was first built for.

- **Ten programming agents** (Rex, Thomas, Ada, Devon, Quinn, Marcus,
  Sentinel, Clara, Piper, Atlas) and **five art agents** (Ember, Blake, Lex,
  Nova, Sage).
- **Two pipelines.** Programmer, coordinated by Atlas, and art, coordinated by
  Nova, each dispatching its own agents.
- **A shared dispatch board** that agents posted to and read from.
- **A research tier was listed but never defined.** The overview named four
  research agents (Echo, Keeper, Bridge, Scribe) and a research pipeline; no
  definitions were written, and they are in no later version.
- A mode for unattended work with its own launch limit, which version 2
  dropped and version 4 brings back in a different form.
