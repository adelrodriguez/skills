#!/usr/bin/env bash
# Check that the README lists every skill, and that skills name only skills
# this repository ships or the README's Requirements section names as "the `x` skill".
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

exec python3 - <<'PY'
import pathlib
import re
import sys

skills_dir = pathlib.Path("skills")
readme = pathlib.Path("README.md").read_text()

skills = {path.parent.name: path.read_text() for path in sorted(skills_dir.glob("*/SKILL.md"))}
user_invoked = {
    name for name, text in skills.items()
    if re.search(r"^disable-model-invocation: true$", text.split("\n---", 1)[0], re.M)
}

requirements = readme.split("## Requirements", 1)[1].split("\n## ", 1)[0]
table = readme.split("## Skills", 1)[1].split("\n## ", 1)[0]
rows = re.findall(r"^\| `([a-z0-9-]+)` \|([^|]*)\|", table, re.M)
listed = [name for name, _ in rows]

errors = []

for name in sorted(skills.keys() - set(listed)):
    errors.append(f"README.md: the Skills table has no row for `{name}`")
for name in sorted(set(listed) - skills.keys()):
    errors.append(f"README.md: the Skills table lists `{name}`, which is not a folder in skills/")
for name, agent_invocation in rows:
    expected = "" if name in user_invoked else "✓"
    if name in skills and agent_invocation.strip() != expected:
        mark = "a ✓" if expected else "no ✓"
        errors.append(f"README.md: put {mark} under Agent invocation for `{name}`, to match its disable-model-invocation setting")
if listed != sorted(listed):
    errors.append("README.md: sort the Skills table by skill name")

def skill_references(text):
    """Yield (line number, name) for each skill a document names: "the `x` skill"
    in prose, and every name in a table column whose header contains "skill"."""
    skill_columns = []
    for number, line in enumerate(text.splitlines(), start=1):
        yield from ((number, name) for name in re.findall(r"`([a-z0-9-]+)` skills?\b", line))
        if not line.startswith("|"):
            skill_columns = []
            continue
        cells = line.strip("|").split("|")
        if not skill_columns:
            skill_columns = [i for i, cell in enumerate(cells) if "skill" in cell.lower()] or [None]
            continue
        for i in skill_columns:
            if i is not None and i < len(cells) and not set(cells[i].strip()) <= set("-: "):
                yield from ((number, name) for name in re.findall(r"`([a-z0-9-]+)`", cells[i]))


for path in sorted(skills_dir.rglob("*.md")):
    for number, name in skill_references(path.read_text()):
        if name not in skills and f"`{name}` skill" not in requirements:
            errors.append(
                f"{path}:{number}: `{name}` is not a skill in skills/. "
                f"Add it, or name it as the `{name}` skill under Requirements in README.md, with where to install it"
            )

for error in errors:
    print(error, file=sys.stderr)
if errors:
    sys.exit(1)
print(f"Checked {len(skills)} skills.")
PY
