---
name: why
description: Investigate why code is shaped the way it is, from history, tickets, docs, and chat, with cited confidence.
disable-model-invocation: true
metadata:
  reference:
    - "https://github.com/cursor/plugins/blob/main/pstack/skills/why/SKILL.md"
---

# Why

Answer why code has its current shape: a design rationale, a tradeoff, a motivating edge case, an external constraint, a threshold, dead code, or a regression.

The `how` skill explains what the code does and how it works, from the source alone. When the user asks how something runs or where code belongs, suggest `/how`.

Work as a careful investigator. Each claim carries the confidence its evidence supports, and an honest "we don't know" beats a confident guess.

Use the available subagent tools with their default model unless the user names one. Give investigators and the synthesizer a subagent type that can call the source's tools, including MCP servers, because some read-only types cannot. If subagents are unavailable, run each investigator and the synthesizer yourself with the same templates.

## Name the target and the question

The target is a piece of code, a pattern, a feature, or a named decision. The question is what the user wants to know about its origin. When the target is vague, infer it from the conversation, such as open files, recent edits, and what was just discussed, then state your interpretation and continue.

Treat a hypothesis in the question, such as "I assume it's for performance?", as one candidate to check.

The step is done when you have stated the target and the question.

## Build the code anchor

Gather the seed context that every investigator and the synthesizer receive:

- File paths with line ranges, and the key symbols.
- The commits that last touched the target, from `git blame` and `git log --follow`, traced back past the most recent commit to the change that introduced the shape.
- PR numbers from commit subjects, such as `(#1234)`, and each substantive PR's body, reviews, and comments from `gh pr view`.
- Ticket IDs mentioned in commits or PR bodies.

The step is done when every substantive commit on the target has its PR and ticket IDs recorded, or a note that it has none.

## Map the sources

List the available tools and MCP servers, and map each to one category in [`references/sources.md`](references/sources.md). Source control is always available through `git` and `gh`. When a tool fits several categories, choose its primary evidence and note the choice.

Investigate every category with an available tool. Skip one only when it has no available tool, or when it is provably irrelevant, such as error tracking for a build-time script. Record each skip with its reason.

When one PR description fully answers the question for a single-commit target, you may answer directly instead. State that you skipped the investigation and why.

The step is done when every category in `references/sources.md` is mapped to a tool or recorded as skipped with a reason.

## Investigate

Spawn one investigator per mapped category in a single message, each owning exactly one source. Build each prompt from [`references/investigator-prompt.md`](references/investigator-prompt.md), and append that category's section of `references/sources.md`. When the target looks defensive, such as null checks, retries, timeouts, rate limits, feature flags, or out-of-memory handling, also append the "Defensive code" section.

The step is done when every investigator has returned.

## Synthesize

Spawn one synthesizer with [`references/synthesizer-prompt.md`](references/synthesizer-prompt.md), what the user plans to do with the answer when known, every investigator's findings, the skipped categories with reasons, and [`references/epistemics.md`](references/epistemics.md) appended.

The step is done when the synthesizer has returned.

## Present the answer

Present the synthesizer's output as written, with light edits for clarity or for context from the conversation. Keep its confidence tiers and wording exactly.

The step is done when the answer passes the check below.

## Check the answer

- Every claim in "What we found" has a citation.
- "Sources consulted" has one line per category, including skipped and empty ones.
- "What we don't know" names specific searches, not a general disclaimer.
- A hypothesis in the user's question is confirmed or rejected by evidence.
- When the user plans to change the code, the answer ends with the constraints section.
