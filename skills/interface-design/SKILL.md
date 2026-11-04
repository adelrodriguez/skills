---
name: interface-design
description: Use when building, redesigning, or restyling UI, such as pages, screens, and components, or when the user says a design looks generic, templated, or AI-made.
metadata:
  reference:
    - "https://github.com/pbakaus/impeccable/blob/main/skill/SKILL.src.md"
    - "https://github.com/pbakaus/impeccable/blob/main/skill/reference/craft-floor.md"
    - "https://github.com/pbakaus/impeccable/blob/main/skill/reference/new-work.md"
    - "https://github.com/pbakaus/impeccable/blob/main/skill/reference/operate.md"
    - "https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md"
    - "https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md"
    - "https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/references/app-screens.md"
    - "https://github.com/emilkowalski/skills/blob/main/skills/review-animations/STANDARDS.md"
---

# Design interfaces

Make design decisions for this product and this surface instead of reaching for the category default. A generated page tends to look like the average of every page the model has seen. Each step below replaces one default with a decision.

Other skills own parts of the work:

- `design-context` writes `PRODUCT.md` and `DESIGN.md`.
- `writing-for-humans` writes the copy.
- `restraint` decides what to cut.
- `harden-ui` tests the UI with worst-case data and failure states.
- `design-review` reviews a finished design.

## Read the context

Read `PRODUCT.md` and `DESIGN.md` when they exist. Read the code of the target and the screens around it, including its tokens, components, and assets. Look at the current render at the widths it ships at. When the app cannot run, use committed screenshots or visual-regression images, and check that they match the current code.

If `PRODUCT.md` is missing and the work is a new surface or a redesign, run `design-context` first to write it. `DESIGN.md` for a new look waits until the user approves the plan. A narrow change to existing code can go ahead without it.

The brief wins. Follow every font, color, era, material, and reference that the user or `DESIGN.md` pins, even when it matches a default in [`references/tells.md`](references/tells.md).

Finish when you can name the audience, the surface's job, and the tokens the surface uses or must use.

## Decide the kind of change

- **Refinement:** Keep the existing look, behavior, and copy, and leave everything outside the scope alone. Ask before you replace factual copy.
- **Addition to a surface:** Inherit the surface's look and composition. Decide only the new content, hierarchy, states, and how the addition joins the page.
- **New surface in an established look:** Keep the visual system and design a new composition.
- **Redesign or new look:** Keep the product's content, function, and constraints. Treat the old look as evidence of what the subject is, not as a style to polish.

A missing `DESIGN.md` does not make a project new. When the code already has a coherent look, it is an established look.

Finish when you have stated the kind of change in one line.

## Choose the mode

The mode names what success looks like for the visitor on this surface. Choose it from the surface, not the product: a developer tool's landing page is Persuade, and a fashion brand's documentation is Read.

- **Persuade:** The visitor decides and acts, as on landing pages, marketing pages, and pricing. Commit fully to one bold idea.
- **Operate:** The visitor completes a task, as on app screens, dashboards, settings, and editors. Familiar patterns, density, and consistency come first, and the brand shows in precise details. Read [`references/app-screens.md`](references/app-screens.md).
- **Read:** The visitor understands something, as in docs, articles, and changelogs. Structure the content for comprehension, then make the reading pleasant. Read the "Read surfaces" section of `references/app-screens.md`.
- **Experience:** The visitor explores the work itself, as in portfolios, galleries, and showcases. The work leads and the interface recedes.

Finish when you have named one mode.

## Find the idea

Skip this step for a refinement or an addition to a surface.

1. List 8 to 12 things that belong to this subject and to no competitor. Look at its name and what the name means, its place, its numbers, its constraints, its materials, its rituals, and the printed things of its world, such as tickets, labels, and timetables. Ask the user for what the brief and the code do not say.
2. Name the rut: the page this category always ships. Read `references/tells.md` for the looks that generated design converges on.
3. Write the idea as one sentence: "On this page, [a thing from the list] becomes [a device, such as the hero, the layout, the navigation, or one interaction]." Put the nearest competitor's name into the sentence. If the sentence still works, the idea belongs to the category, so choose again.
4. Write the page as a list of claims, one per section, each with the proof the product actually has. Delete each section that has no claim. For an Operate screen, write the one question the screen answers first, and list each block as the answer to the next question.

Finish when the idea sentence fails for the nearest competitor and every planned section has a claim or a question.

## Plan before you build

Write a short plan:

- 4 to 6 named colors with hex values, and the role of each.
- One or two typefaces, their roles, and the type scale.
- The layout as one sentence and an ASCII wireframe for each breakpoint that changes it, with the text alignment.
- The one element that carries the boldness. Keep everything around it quiet.

Check each part of the plan against the rut by asking whether a similar brief would land on the same choice. Revise each part that would, and note what you changed and why.

For a redesign or a new look, show the plan to the user and wait for approval before you build. Once the user approves it, record it in `DESIGN.md` with `design-context`. For other kinds of change, continue.

Finish when every part of the plan has a reason that comes from this brief and, for a new look, the user has approved the plan.

## Build it

Build in this order, and check each part at the shipping widths before you start the next: tokens as CSS custom properties, the first screen, each section, imagery, states, then motion. Every style downstream uses the tokens.

- Use real content: the product's own copy, data, and pictures. Write the copy with `writing-for-humans` before the markup. Where the brief leaves gaps, write believable sample content and list it in the report.
- Replace ornament with substance. When you remove a default, fill the space with scale, full content, a real picture of the subject, or a field of color, not with another ornament. In blind tests, judges preferred a rich page with some tells over a clean page that was thin.
- Follow [`references/craft.md`](references/craft.md) for type, color, layout, imagery, and components.
- Add motion last, following [`references/motion.md`](references/motion.md).
- In a redesign of an existing page, change the type first, then color, then the frame (margins, rhythm, and headings), then states, then components. Keep the stack, the routes, and the behavior.

Finish when every section in the plan is built with real content or listed sample content, and every interactive element has its states.

## Look at the result

Take screenshots at 390, 768, and 1440 pixels, or at the widths the product ships at, and look at every one. Judge the screenshots rather than the code, because you read your intentions into code you wrote.

Check each screenshot against the checks in `references/craft.md` and the defaults in `references/tells.md`. Fix everything one look shows before you take the next screenshots. Stop after three rounds, and report what still falls short.

When no browser tool is available, check the CSS instead, and list the checks that ran only on code.

Finish when every check in `references/craft.md` passes at every width, or each failure is in the report.

## Check the design

- Every font, color, and reference the brief pins is followed.
- For new work, the idea sentence fails for the nearest competitor.
- Every section has a claim or a question, and its real content.
- No default from `references/tells.md` appears unless the brief asks for it, and no banned item appears.
- You looked at every screenshot after the last change.

## Return the result

Report the kind of change and the mode. For new work, include the idea sentence and the plan, with what you revised against the rut. List each piece of sample content to replace before launch, each default you kept with its reason, and each check that did not run.
