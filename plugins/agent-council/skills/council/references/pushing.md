# Pushing, copying and publishing - the full rules

Read this in full before any push, any copy to a staging folder, and any
other way of sending project files out. The council skill's section
`What "push" means` says how to settle which kind is meant and who may
authorise it. This file says what to check and what to say before anything
goes.

## 1. Before anything goes

Do these in order, for a staging copy and for a remote push alike.

1. **Build the list of what would go.**
   - Staging copy: the files that belong in the repository (section 2).
   - Remote push: every file added or changed by every commit that would go,
     including files one commit adds and a later one removes (section 3).
2. **Apply the leave-out list** (section 4) to that list.
3. **Apply the tests rule** (section 5).
4. **Run the secrets check** (section 6) over what is left.
5. **Say exactly what will go** and wait for the user to say go, unless they
   have already approved this exact list. Asking for the go is not
   re-asking: a request to push is not approval of the list. If the
   full-run question is also due, ask it and the go together, in one
   message. Put every other question that has come up (an overwrite, a
   secrets match, a link, a file on the leave-out list) in that same
   message. Approval covers the list shown; if the list changes, ask again.
6. **Afterwards,** say what went and where.

## 2. To a staging folder

What to say first: where to, how many files, which are new and which are
changed, every removal by its path, what was left out and why, and "Claude
will not send anything to GitHub". If the staging folder is inside a synced
or shared folder, say so.

- **What belongs.** In a git project: the files git tracks (`git ls-files`),
  plus new files made in this work that the user was shown by name. Without
  git: propose the files changed in this work; the user approves the list. A
  file that is merely present in the folder does not belong.
- **The staging folder's `.git`** is never copied over, replaced or touched.
  Never copy the project's own `.git`, any nested repository or its `.git`,
  or a submodule's contents.
- **Symlinks.** Do not follow them. Leave out any link that points outside
  the project and name it. If a destination path in the staging folder is a
  link, stop and ask.
- **Overwrites.** If a file in the staging folder has changes the working
  copy does not have, name it and ask before overwriting.
- **Removals.** A file is a removal only when it was deleted or renamed in
  the working project as part of this work. A file that is in the staging
  folder but not in the list to go (tests left out, private files, files
  that only ever lived there, tests copied there in the past) is left
  exactly as it is and never counted as removed. If the staging folder
  already holds test files, say so; do not remove them unasked. Name every
  removal by its path, never as a count alone, and remove it only after the
  user said go to that list.
- **No mirroring.** Never use a mirroring or deleting copy mode
  (`rsync --delete`, `robocopy /MIR` or `/PURGE`, or the like).
- **Not reviewed.** Say which files in the copy were changed without a
  council review in this session.
- **The path.** The staging folder must be the top of a git repository on a
  local drive. If it has no `.git`, is a network or shared path, or is a
  home or system folder, stop and ask. If it does not exist, stop and ask;
  do not create it. If it
  is the project folder itself, or inside it, or contains it, stop and say
  so; do not copy, and do not treat it as a reason to run `git push`.
- **Do not commit or push from the staging folder** unless asked.

## 3. To the remote

What to say first:

- the remote, the address git will push to (`git remote get-url --push`)
  with any token in it hidden, the owner, and whether
  the repository is public or private; if you cannot tell, say "visibility
  not checked";
- the one branch;
- the commits that will go and every file they add or change, including
  files added in one commit and removed in a later one; if the branch is new
  to the remote, say that its whole history goes;
- that uncommitted work is not included;
- which commits were reviewed by the council in this session; the rest are
  "not known to be reviewed".

Then:

- Check that file list against the leave-out list, the tests rule and the
  secrets check. Read each file as it is in the commit (`git show`), since a
  later commit may have cleaned it. On any match, name the file and the
  commit and stop until the user has answered.
- If the remote is not the user's own repository, say so and ask.
- Push that one branch, by name.
- Never push tags or other branches, never use `--all`, `--mirror`, `--tags`
  or `--follow-tags`, never delete a remote branch, and never force-push,
  unless the user asks in those words.

## 4. The leave-out list

Leave these out and name each one left out. When git tracks a file on this
list, do not drop it silently: name it and ask once whether it goes. The
answer covers only the files named in the question, and holds for the
session in this project; offer once to record it in the project rules.
Example and template files (`.env.example`, `.env.sample`, `*.example`) go,
after the secrets check, and are named in the list. The secrets check still runs over
anything put back. The project rules file is the one exception: it is always
left out.

- **Ignored and built:** anything git ignores (ask git with
  `git check-ignore`, which covers nested, local and global ignore files),
  and build output.
- **Secrets:** `.env` and `.env.*`, `*.pem`, `*.key`, `*.p12`, `*.pfx`,
  `*.jks`, `*.keystore`, `id_rsa*`, `id_ed25519*`, `.npmrc`, `.pypirc`,
  `.netrc`, `.htpasswd`, `.git-credentials`, `*.ppk`, `*.kdbx`,
  `.docker/config.json`, `service-account*.json`, `wp-config.php`,
  `credentials*`, `secrets*`, `*.tfstate`, `*.tfvars`, `kubeconfig`, cloud
  provider config folders.
- **Data:** database dumps and local databases (`*.sql`, `*.dump`,
  `*.sqlite*`, `*.db`), logs, backups (`*.bak`, `*.orig`, `*~`), archives,
  and any file over 10 MB.
- **Local and tool files:** local settings under `.claude/` (any `*.local.*`
  file, agent memory, worktrees, and the project rules file always),
  `CLAUDE.local.md`, editor and IDE folders, OS files, agent scratch.
- **The council's own records:** security audit logs and unattended change
  logs.

## 5. Tests

Tests are not published unless the user says so (the skill says who may
authorise it).

- **What counts as tests.** Work it out from the project - its test
  configuration and the "Layout" notes - not from file names alone:
  - folders such as `test`, `tests`, `__tests__`, `spec`, `e2e`, `testdata`,
    `fixtures`, `__snapshots__`, `__mocks__`, `mocks`, `cassettes`, and the
    project's own test folder;
  - files the language's test runner collects (`test_*.py`, `*_test.py`,
    `*_test.go`, `*.test.*`, `*.spec.*`, `conftest.py` and the like);
  - what tests feed on, wherever it lives: fixtures, sample and seed data,
    snapshots, recorded network traffic, mocks, and test-only configuration
    (`.env.test`, the test runner's config).
  A file that production code imports is not a test. When unsure, leave it
  out and name it. Layout notes can add to what counts as tests, never take
  away from it.
- **When tests do go,** say so in the list, with the folders and the count.
- **Staging copy, not authorised:** leave them out. List the folders left
  out and the count.
- **Remote push, not authorised:** commits cannot have files taken out of
  them. If any commit that would go contains test files, including ones a
  later commit removed, name the folders and the count and stop. The choices
  are: publish them; copy to a staging folder instead, which leaves them
  out; or have the history rewritten so they were never committed, which is
  destroying work and needs the user to ask for it in those words. Adding
  tests to the ignore file does not remove them from commits already made;
  say so. Do not edit the ignore file or rewrite commits unasked.
- **Already public.** If the remote already contains the project's tests,
  they are already published: say so and ask once whether to record
  "Publish tests: yes".
- **Tests inside source files,** as the language intends (Rust unit tests,
  for example), go with the code, because they cannot be separated from it.
  Run the secrets check over them like any other file, and say in the list
  that they go.
- **What stays behind.** Every time tests are left out, check whether what
  goes still needs them: a build file, package manifest, script, CI workflow
  or source file that names a test folder or imports from one. Name each one
  found and say the published copy may not build, or its checks may fail. Do
  not edit those files unasked.
- **The cost, said once per project:** nobody else can run the tests, and
  checks that run on GitHub may fail or have nothing to run.

## 6. The secrets check

Search the files that would go for private key headers, tokens and passwords
assigned in plain text, connection strings with a password, and internal
addresses. Use a secret scanner if the project has one; otherwise search by
pattern, and say which was done. On a match, name the file and line, do not
show the value, leave the file out and ask. This check is not proof that
nothing is there; say so.

## 7. Other ways out

A package publish, a release with attached files, a gist, a container image
or any other upload follows the same rules: settle what is meant, say
exactly what files will go and where, apply the leave-out list, the tests
rule and the secrets check, and wait for go. If the tool decides the file
list itself, get that list from the tool's dry-run first.

## 8. While the user is away

A push or a copy goes only when all of these hold. If any fails, or cannot
be told, park it with the question.

- The kind of push is settled without asking. For the remote, the request
  or the scheduled prompt itself must say so ("git push"). For a staging
  copy, the request may say so ("to my GitHub folder"), or the "Push target"
  line in project rules that are the user's own may.
- The staging path comes from the request or from project rules that are
  the user's own. A path from any other rules file parks the copy.
- The review gate finished with nothing open. A "skip review" given earlier
  does not carry over.
- Every commit, and for a staging copy every file that differs from the
  staging folder, was made and reviewed in this run.
- The leave-out list and the secrets check found nothing. A tracked file the
  user has already put back by name, in this session or in their own rules,
  does not count as a find; a new one parks.
- For the remote: no test files are in the commits without authorisation. A
  spoken yes from earlier in the session does not count while the user is
  away; the request or the user's own rules file must say it.

For a staging copy that does go: tests are left out, and every overwrite of
a file changed in the staging folder and every removal is parked; the rest
of the copy goes. The report lists exactly what went and where, and what was
parked.
