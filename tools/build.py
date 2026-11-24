#!/usr/bin/env python3
"""Check and package the Council of Agents plugin.

Run from anywhere:

    python tools/build.py           sync shared rules, check, write dist/*.plugin
    python tools/build.py --check   check only; change nothing

All paths are relative to this file, so the script works wherever the
repository is cloned. It uses only the Python standard library and needs
Python 3.10 or later.

What it does:
  1. Copies tools/shared-rules.md into the end of every agent file, so the
     shared rules have one source.
  2. Checks the manifests, the 21 agent files, the skill, and that
     CHANGELOG.md has an entry for the manifest's version.
  3. Fails if a machine path, a banned word, or any term listed in the
     optional tools/private-terms.txt is in the plugin or the files beside it.
  4. Zips plugins/agent-council into dist/agent-council.plugin.
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_NAME = "agent-council"
PLUGIN = ROOT / "plugins" / PLUGIN_NAME
SHARED = ROOT / "tools" / "shared-rules.md"
DIST = ROOT / "dist"
SHARED_HEADING = "## Shared rules"

AGENTS = [
    "ada", "atlas", "blake", "clara", "coeus", "devon", "ember", "lex",
    "marcus", "nova", "piper", "prose", "quill", "quinn", "rex", "sabine",
    "sage", "sentinel", "sol", "thomas", "wren",
]

# Text that must never ship. These patterns apply to everyone.
LEAKS = [
    (re.compile(r"\b[A-Za-z]:[\\/]"), "drive path"),
    (re.compile(r"/mnt/user-data|/home/|/Users/"), "machine path"),
    (re.compile(r"\bstub\w*", re.I), "banned word"),
]

# The maintainer's own list: names, private project names, internal function
# names. One regular expression per line, matched without regard to case;
# blank lines and lines starting with # are skipped. The file is optional and
# is never committed (see .gitignore), so the terms themselves stay private.
PRIVATE_TERMS = ROOT / "tools" / "private-terms.txt"


def load_private_terms() -> list[tuple[re.Pattern[str], str]]:
    if not PRIVATE_TERMS.is_file():
        return []
    terms = []
    lines = PRIVATE_TERMS.read_text(encoding="utf-8-sig").splitlines()
    for number, line in enumerate(lines, 1):
        line = line.strip()
        if line and not line.startswith("#"):
            try:
                terms.append((re.compile(line, re.I), "private term"))
            except re.error:
                raise SystemExit(f"FAILED - {PRIVATE_TERMS.name} line {number}: "
                                 "not a valid pattern")
    return terms

# Files that never go in the package.
JUNK = re.compile(r"(^\.DS_Store$|^Thumbs\.db$|^desktop\.ini$|\.bak$|\.orig$|~$)")


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (fields, body) for a markdown file with --- frontmatter."""
    if not text.startswith("---\n"):
        raise ValueError("no frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter not closed")
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "#")):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields, text[end + 5:]


def with_shared_rules(text: str, shared: str) -> str:
    """Replace everything from the shared-rules heading line on with `shared`."""
    match = re.search(r"^" + re.escape(SHARED_HEADING) + r"[ \t]*$", text, re.M)
    head = text if match is None else text[:match.start()]
    return head.rstrip("\n") + "\n\n" + shared.strip("\n") + "\n"


def main() -> int:
    args = sys.argv[1:]
    if any(arg != "--check" for arg in args):
        print("usage: build.py [--check]")
        return 2
    check_only = "--check" in args
    private_terms = load_private_terms()
    leaks = LEAKS + private_terms
    errors: list[str] = []

    # Stop before touching any agent file if the shared rules are malformed.
    shared = SHARED.read_text(encoding="utf-8-sig")
    if shared.splitlines()[:1] != [SHARED_HEADING]:
        print(f"FAILED - {SHARED.name}: first line must be '{SHARED_HEADING}'")
        return 1

    # 1. Agents: shared rules in sync, frontmatter sound.
    found = sorted(p.stem for p in (PLUGIN / "agents").glob("*.md"))
    if found != AGENTS:
        errors.append(f"agents: expected {AGENTS}, found {found}")
    for name in found:
        path = PLUGIN / "agents" / f"{name}.md"
        text = path.read_text(encoding="utf-8")
        wanted = with_shared_rules(text, shared)
        if text != wanted:
            if check_only:
                errors.append(f"agents/{name}.md: shared rules out of date "
                              "(run without --check)")
            else:
                path.write_text(wanted, encoding="utf-8", newline="\n")
                text = wanted
        try:
            fields, body = split_frontmatter(text)
        except ValueError as exc:
            errors.append(f"agents/{name}.md: {exc}")
            continue
        if fields.get("name") != name:
            errors.append(f"agents/{name}.md: name must be '{name}'")
        if not fields.get("description"):
            errors.append(f"agents/{name}.md: description missing")
        if not body.split(SHARED_HEADING)[0].strip():
            errors.append(f"agents/{name}.md: no brief above the shared rules")

    # 2. Manifests and skill.
    version = "?"
    try:
        manifest = json.loads(
            (PLUGIN / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        version = str(manifest.get("version", "?"))
        if manifest.get("name") != PLUGIN_NAME:
            errors.append(f"plugin.json: name must be '{PLUGIN_NAME}'")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"plugin.json: {exc}")
    try:
        market = json.loads(
            (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        entries = {e.get("name"): e for e in market.get("plugins", [])}
        entry = entries.get(PLUGIN_NAME)
        if entry is None:
            errors.append(f"marketplace.json: no entry named '{PLUGIN_NAME}'")
        elif entry.get("source") != f"./plugins/{PLUGIN_NAME}":
            errors.append("marketplace.json: source must be "
                          f"'./plugins/{PLUGIN_NAME}'")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"marketplace.json: {exc}")
    changelog = PLUGIN / "CHANGELOG.md"
    heading = re.compile(rf"^## Version {re.escape(version)}(\s|$)", re.M)
    if not changelog.is_file() or not heading.search(
            changelog.read_text(encoding="utf-8")):
        errors.append(f"CHANGELOG.md: no heading line '## Version {version}'")
    skill = PLUGIN / "skills" / "council" / "SKILL.md"
    try:
        fields, _ = split_frontmatter(skill.read_text(encoding="utf-8"))
        if fields.get("name") != "council" or not fields.get("description"):
            errors.append("SKILL.md: needs name 'council' and a description")
    except (OSError, ValueError) as exc:
        errors.append(f"SKILL.md: {exc}")

    # 3. Nothing personal or single-project in what ships.
    files = sorted(p for p in PLUGIN.rglob("*")
                   if p.is_file() and not JUNK.search(p.name))
    published = files + [ROOT / "README.md",
                         ROOT / ".claude-plugin" / "marketplace.json", SHARED]
    for path in published:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT).as_posix()}: unreadable ({exc})")
            continue
        for number, line in enumerate(text.splitlines(), 1):
            for pattern, label in leaks:
                if pattern.search(line):
                    errors.append(
                        f"{path.relative_to(ROOT).as_posix()}:{number}: {label}")

    # The build's own files are public too. Check them against the private
    # terms only: the generic patterns would match this script's own text.
    for path in (Path(__file__).resolve(),
                 ROOT / "tools" / "private-terms.example.txt",
                 ROOT / ".gitignore"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            for pattern, label in private_terms:
                if pattern.search(line):
                    errors.append(
                        f"{path.relative_to(ROOT).as_posix()}:{number}: {label}")

    if errors:
        print(f"FAILED - {len(errors)} problem(s)")
        for item in errors:
            print("  " + item)
        return 1

    private = "" if PRIVATE_TERMS.is_file() else \
        " [no tools/private-terms.txt - private terms not checked]"
    if check_only:
        print(f"OK - {PLUGIN_NAME} {version}, {len(found)} agents, "
              f"{len(files)} files (check only, nothing written){private}")
        return 0

    # 4. Package.
    DIST.mkdir(exist_ok=True)
    out = DIST / f"{PLUGIN_NAME}.plugin"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(PLUGIN).as_posix())
    print(f"OK - {PLUGIN_NAME} {version}, {len(found)} agents, "
          f"{len(files)} files -> {out.relative_to(ROOT).as_posix()}{private}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
