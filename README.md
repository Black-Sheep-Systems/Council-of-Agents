# Council of Agents

A Claude Code plugin marketplace holding one plugin, **agent-council**
(Council of Agents):
twenty-one named specialist agents and the rules for running them with review
sized to the risk of each change. See
[the plugin's README](plugins/agent-council/README.md) for what it does.

## Install

From a GitHub repository (replace `<owner>/<repo>` with where this is hosted):

```bash
claude plugin marketplace add <owner>/<repo>
claude plugin install agent-council@worldsmith
```

From a local copy, run this in the folder that contains your copy, using its
folder name:

```bash
claude plugin marketplace add ./agent-council
claude plugin install agent-council@worldsmith
```

Without a marketplace: send someone the `plugins/agent-council` folder (or
a zip of it) and they load it with `claude --plugin-dir <folder>`.
`dist/agent-council.plugin` is that same folder zipped, for adding the
plugin in the Claude desktop app. Either way they get a separate copy and no
later updates.

## Layout

```
.claude-plugin/marketplace.json     the marketplace catalog
plugins/agent-council/          the plugin
  .claude-plugin/plugin.json
  agents/                           the twenty-one agents
  skills/council/SKILL.md           working rules, review gate, pipelines
  examples/project-overlay.md       template for per-project rules
  CHANGELOG.md                      what changed in each version
tools/shared-rules.md               the rules appended to every agent
tools/build.py                      check and package
tools/private-terms.example.txt     template for your own never-publish list
dist/agent-council.plugin       written by the build
```

## Change and rebuild

Edit the files under `plugins/agent-council/`. The "Shared rules" block at
the end of each agent file is written by the build from
`tools/shared-rules.md`; edit it there, not in the agent files.

```bash
python tools/build.py           # sync shared rules, check, write dist/*.plugin
python tools/build.py --check   # check only
claude plugin validate .        # Claude Code's own check
```

The build fails if a machine path or a banned word is found in the plugin,
this README or the marketplace file. To have it also catch your own name or
private project names, copy `tools/private-terms.example.txt` to
`tools/private-terms.txt` and list them there; that file is never committed.

To release a change, raise `version` in
`plugins/agent-council/.claude-plugin/plugin.json` and add an entry at the
top of `plugins/agent-council/CHANGELOG.md`. People who installed
from the marketplace stay on the version they have until it changes.
