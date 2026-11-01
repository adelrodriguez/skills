---
name: what
description: Restate the last message in plain language, with context and no jargon.
disable-model-invocation: true
metadata:
  reference:
    - "https://github.com/cursor/plugins/blob/main/pstack/skills/bro/SKILL.md"
    - "https://github.com/mattpocock/skills/blob/main/skills/productivity/wait-what/SKILL.md"
---

# What

The user did not follow your last message. Restate it more simply and more briefly, the way one person would explain it to another.

## Give the context first

Open with one or two sentences that say what you were trying to do and where you got to. Then restate the message.

## Use the project's words

Use the terms from the repository's `GLOSSARY.md` when it exists. If the repository has a `GLOSSARY-MAP.md`, follow it to the glossary for the area you are talking about. Replace other jargon with everyday words, or define it in one clause the first time it appears.

## Keep the content

Keep every fact, decision, and request for the user from the original. Do not add new information or start new work.

## Unslop the draft

Use the `unslop` skill on the draft before you send it.

## Check the restatement

- The first sentences say what you were doing and where you got to.
- Every project term matches the glossary, and every other technical term is replaced or defined.
- Every fact, decision, and request from the original is still there, and nothing new is added.
- The restatement is shorter than the original.
- The `unslop` skill ran on the final draft.
