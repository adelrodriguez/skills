# Explainer prompt

Build the explainer's prompt from this template. Fill in the placeholders. For a simple question, leave out the "Explorer findings" section and the first paragraph of "Instructions".

---

Read only. Leave files, commits, and subagents untouched.

Write an architectural explanation for a senior engineer who is new to this area. After reading it, they should understand the subsystem well enough to start working in it.

## Question

> {QUESTION}

## Explorer findings

{EXPLORER_FINDINGS}

## Instructions

Explorers traced different angles of the subsystem in parallel, and their findings overlap and may contradict each other. Merge the overlaps, settle each contradiction by reading the code, and combine the angles into one picture. Read the code to check a detail or fill a gap, and build on the explorers' work rather than exploring again.

Read each implementation rather than inferring behavior from names.

## Output

Use these sections, and drop any that do not apply to the question.

### Overview

One or two paragraphs on what the subsystem is, what it does, and why it exists. A reader should be able to stop here and decide whether to read on.

### Key concepts

Only the types, services, and abstractions the reader needs to follow the rest, each with a short definition.

### How it works

The longest section. Walk from the trigger to the result: each step, where the data goes, and the decision points. Write prose, and include a code snippet only when prose cannot show the mechanism.

When several components talk to each other or data passes through stages, add a diagram. Use mermaid for sequences, flowcharts, and component graphs, and ASCII for simpler relationships.

### Where it lives

The few files and directories someone should open first.

### Gotchas

Surprising behavior, hidden coupling, historical context, pitfalls, and every open question.

## Style

- Name the actual files, functions, and symbols. Write "`UserService` calls `AuthClient.refresh()`", not "the service delegates to the client".
- When something is complex, explain why it is complex.
