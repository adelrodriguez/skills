---
name: design-context
description: Use when writing or updating PRODUCT.md or DESIGN.md, or when interface-design needs product or visual context that does not exist yet.
metadata:
  reference:
    - "https://github.com/pbakaus/impeccable/blob/main/skill/reference/init.md"
    - "https://github.com/pbakaus/impeccable/blob/main/skill/reference/document.md"
    - "https://github.com/google-labs-code/design.md/blob/main/docs/spec.md"
---

# Record the design context

Write the two files that every design task reads first. `PRODUCT.md` records who the product is for and what it must do. `DESIGN.md` records the visual system. Keeping them separate lets a redesign replace the look while the product facts stay the same.

## Read what exists

Read any existing `PRODUCT.md`, `DESIGN.md`, and `GLOSSARY.md`, then the README, docs, and marketing copy. Read the routes, roles, and features, and the tokens, theme files, global CSS, and component library.

Update existing files instead of creating competing ones. In a monorepo, ask the user whether the context belongs at the root or in one app.

Finish when you have a list of the facts the repository proves and a list of the gaps.

## Write PRODUCT.md

Ask the user only about gaps that would change future design decisions. Ask at most three questions per round, through the structured question tool when one is available. Start with these:

1. Who is the primary user, in what situation, and doing what job?
2. What does the product make possible that a competitor could not truthfully claim?
3. Which constraints, assets, and evidence must future work keep?

Do not ask about colors, fonts, or style. If the user volunteers a visual constraint, record it under "Brand commitments". If no one can answer, write the facts you inferred and mark each one as inferred.

Use these sections, and omit any section that has neither confirmed nor inferred facts:

```markdown
# Product

## Users
<!-- Primary users, their situation, and their job. -->

## Purpose
<!-- What the product does, why it exists, and what success means. -->

## Positioning
<!-- What the product does that a competitor could not truthfully claim. -->

## Context of use
<!-- Where, when, and with what tools and materials people use it. -->

## Capabilities and constraints
<!-- Confirmed features, technical limits, and open decisions. -->

## Brand commitments
<!-- Name, voice, assets, and visual constraints the user made binding. -->

## Evidence on hand
<!-- Real testimonials, data, case studies, and assets, with paths. Name what is absent. -->

## Accessibility
<!-- Known user needs or the required standard. -->
```

When `GLOSSARY.md` exists, link to it instead of defining terms again. Under "Evidence on hand", name the proof that does not exist, so that later work does not invent it.

Finish when `PRODUCT.md` exists and every statement in it is either confirmed or marked as inferred.

## Write DESIGN.md

Follow the [DESIGN.md format](https://github.com/google-labs-code/design.md/blob/main/docs/spec.md): YAML front matter with the tokens, then these sections in order: Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, and Do's and Don'ts. Omit a section that does not apply.

- **Existing look:** Extract the tokens from the code, such as CSS custom properties, the Tailwind theme, or token files. Keep the project's own token names and color formats. Then ask the user to describe the look's personality in a few words and what it must never become, and write the prose from their answer.
- **New look:** Write `DESIGN.md` only from a plan the user approved in `interface-design`. If no plan is approved yet, skip this step and say that `DESIGN.md` waits for the plan.

Under "Do's and Don'ts", record each direction the user rejected and why, so that a later session does not propose it again.

Finish when every token in `DESIGN.md` exists in the code or matches the approved plan, or when you skipped the step because no plan is approved yet.

## Check the context

- `PRODUCT.md` holds no colors, fonts, or layouts, and `DESIGN.md` holds no audience or positioning.
- Neither file contains an invented testimonial, customer, number, or claim.
- You updated existing files instead of replacing them, and showed the user each change.

## Return the result

List each file you wrote or changed, the facts marked as inferred, and the questions that remain open.
