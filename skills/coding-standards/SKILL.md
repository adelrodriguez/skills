---
name: coding-standards
description: Use when writing, updating, or auditing CODING_STANDARDS.md, or when a mistake from a session or review should become a coding rule.
metadata:
  reference:
    - "https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md"
    - "https://github.com/mattpocock/skills/blob/main/docs/engineering/retro.md"
---

# Keep the coding standards

`CODING_STANDARDS.md` holds the coding rules that belong to one repository and that no automated check can enforce. Each rule exists because a real mistake showed the need for it.

## Read what exists

Read the root `CODING_STANDARDS.md`, `AGENTS.md`, and `GLOSSARY.md` when they exist, and every file the standards point to. Then read how the repository checks its code: its check scripts, its hooks, and its CI workflows.

Finish when you can list every existing rule and every check the repository runs.

## Collect the evidence

For each candidate rule, name the mistake that shows the need for it, such as a session the user pointed to, a review comment that keeps coming back, or a mistake that got merged. Link or quote the mistake.

Drop a candidate that has no evidence. Drop general best practices, because the global instructions in [adelrodriguez/instructions](https://github.com/adelrodriguez/instructions) already cover them. A global rule belongs in the file only as an exception that the repository makes to it.

Finish when every remaining candidate has its evidence linked or quoted.

## Sort each candidate

For each candidate, ask whether a check the repository already runs could catch the mistake automatically. If it could, add the check there instead of writing a rule, using the tools the repository already has. If catching it needs a tool the repository does not have, propose the tool to the user instead of adding it.

Write a rule only for a judgement call that no check can make, such as consistency across files, choosing between two valid shapes, or matching the surrounding style.

Finish when every candidate is marked as a check or a rule, and every check is added or proposed.

## Write each rule

Create `CODING_STANDARDS.md` at the repository root if it does not exist. Keep only a one-line pointer to it in `AGENTS.md`, and move any coding rule you find in `AGENTS.md` into the standards.

Group rules under a heading for each domain, and give each rule this format:

````markdown
## <Domain>

### <Rule name>

<One sentence that states the rule.> <One sentence with the reason.>

Spot it: <what a violation looks like in a diff>.

```<language>
// Avoid
<code from the repository that breaks the rule>

// Prefer
<the same code following the rule>
```
````

Take both examples from the repository's own code. Keep a rule's heading once it exists, because findings and comments cite rules by heading. Write the rules with the `writing-for-agents` skill.

Finish when every new rule has a heading, a statement, a reason, a "Spot it" line, and examples from the repository, and `AGENTS.md` points to the file.

## Prune the file

Prune on every change, and on its own when the user asks for an audit. Delete a rule when any of these is true:

- A check now enforces it.
- The code it guarded no longer exists.
- It keeps flagging code that is correct.
- It repeats `AGENTS.md`, the global instructions, or another rule.

Once the file passes about 1,000 lines, move whole domain sections into `docs/` and leave a one-line pointer in their place.

Finish when you have checked every rule against the four conditions.

## Check the standards

- Every new rule has evidence and is a judgement call that no check could enforce.
- No rule repeats `AGENTS.md`, the global instructions, or another rule.
- Every heading that existed before still exists, unless you deleted its rule.
- `AGENTS.md` has one line that points to the file and no coding rules.
- Every example comes from the repository's code.
- Use the `unslop` skill on the prose.

## Return the result

List each rule you added, changed, or deleted, with its evidence or the reason for the deletion. List each check you added or proposed, and each change to `AGENTS.md`.
