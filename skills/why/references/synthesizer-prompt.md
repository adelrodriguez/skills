# Synthesizer prompt

Build the synthesizer's prompt from this template. Fill in the placeholders, and append `epistemics.md`.

---

Leave files, commits, and external state untouched, and leave subagents unstarted.

Answer a question about why code has its current shape. Investigators searched separate sources and returned evidence, not conclusions. Weigh it yourself and write an answer that says what the evidence supports, with the confidence it supports, and what it leaves open. The user will act on this answer, so leave an open question open.

## Question

> {QUESTION}

## What the user plans to do

{INTENT}

## Code anchor

**Target files:** {FILES_WITH_LINE_RANGES}

**Key symbols:** {SYMBOLS}

## Investigator findings

{FINDINGS}

## Skipped categories

{SKIPPED_WITH_REASONS}

## Instructions

Follow the epistemics rules appended below.

1. Merge overlaps. When several investigators cite the same item, cite it once.
2. Place every claim in one confidence tier, and word it for that tier.
3. Spot-check citations you doubt by reading the code or calling the source's tools. Drop or correct any that do not say what the investigator reported.

## Output

### The question

The user's question in one or two sentences.

### The code

File paths, line ranges, and key symbols, in two or three lines.

### What we found

Direct and Supported claims, each cited:

- **[Direct]** Claim. Source: PR, ticket, or `file:line`. A short quote.
- **[Supported]** Claim. Evidence: each item and what it adds.

### What we can infer

Inferred claims, each hedged, with the reasoning shown:

- **[Inferred]** Claim. Reasoning: the evidence and the step from it to the claim.

Drop this section when nothing is inferred.

### Competing hypotheses

When the evidence fits several stories, give each:

- **Hypothesis:** one sentence.
- **For:** the supporting items.
- **Against or missing:** the counter-signals, or what would need to be true but is not shown.

Drop this section when one answer is clear.

### What we don't know

Each gap, with the sources and queries searched, the sources unavailable and why, and the people likely to know.

### Sources consulted

One line per category: Source control, Issue tracker, Documents, Team chat, Observability, Error tracking, Analytics warehouse. List what was searched, such as files, commit counts, PR numbers, ticket IDs, queries, channels, date ranges, or tables. For a skipped category, write "Not searched" and the reason.

### Confidence summary

One or two sentences on overall confidence, such as: "The core reason (A) has direct PR and ticket evidence. The threshold value (100) is inferred. Whether a customer request drove it is unknown, and team chat was not searchable."

### Constraints for the change

Include this section only when the user plans to change the code. Turn the findings into four lists:

- **Preserve:** behavior the evidence says must stay.
- **Change:** what the evidence shows is safe or intended to change.
- **Avoid:** approaches the record shows were tried and rejected.
- **Risk:** what could break, and the open questions to settle first.

## Check the answer

Revise until every item holds:

- Every claim in "What we found" has a citation. Move uncited claims to "What we can infer" or "Competing hypotheses".
- Every claim's wording matches its tier.
- Every contradiction is shown with both sides.
- "What we don't know" names specific searches.
- A hypothesis in the question is confirmed or rejected by evidence.
- No claim cites code as evidence of its own intent.
