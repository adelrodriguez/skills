---
name: how
description: Explain how a subsystem, flow, or module works, or where code belongs, from source evidence.
disable-model-invocation: true
metadata:
  reference:
    - "https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md"
---

# How

Answer "how does X work?" and placement questions such as "where should this live?" or "which layer owns this?". Write for a senior engineer who is new to the subsystem, so they can build a mental model and change the code safely. Describe the design as it is, and leave critique and proposals for when the user asks.

This skill explains what the code does and how it works. The `why` skill investigates why the code has its shape, from commits, PRs, tickets, docs, and chat. When the user asks for a reason, a tradeoff, or the history behind a decision, suggest `/why`.

Use the available subagent tools with their default model unless the user names one. If subagents are unavailable, explore and explain yourself with the same templates.

## Scope the question

When the question is ambiguous, state your interpretation and continue. The user can redirect.

Classify the question:

- **Simple:** one module, one function, or a narrow question. Spawn one explainer with [`references/explainer-prompt.md`](references/explainer-prompt.md) and no explorer findings. Go to "Present the explanation".
- **Complex:** a subsystem across several files or services, a cross-cutting feature, or an architectural overview. Go to "Explore".

When in doubt, treat the question as simple.

The step is done when you have stated the interpretation and the classification.

## Explore

Split the question into 2 to 4 angles. An angle is a distinct slice of the subsystem, such as entry points, state, control flow, or external boundaries. Spawn one explorer per angle in a single message, each with [`references/explorer-prompt.md`](references/explorer-prompt.md).

The step is done when every explorer has returned.

## Synthesize

Spawn one explainer with [`references/explainer-prompt.md`](references/explainer-prompt.md) and every explorer's findings.

The step is done when the explainer has returned.

## Present the explanation

Present the explainer's output as written, with light edits for clarity or for context from the conversation.

The step is done when the explanation passes the check below.

## Check the explanation

- It follows the output and style rules in the explainer template.
- Every open question from the explorers and the explainer appears in the explanation.
