---
name: design-review
description: Use when the user asks to critique, review, or audit the design of a page, screen, or component.
metadata:
  reference:
    - "https://github.com/pbakaus/impeccable/blob/main/skill/reference/critique.md"
    - "https://github.com/pbakaus/impeccable/blob/main/skill/reference/audit.md"
    - "https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/references/critique.md"
---

# Review a design

Review a built interface through two independent lenses, then verify and rank what they find. The design lens judges screenshots. The implementation lens checks the code and the rendered page. This skill reports and stops. Fix findings only when the user asks, using the `design-ui` skill.

For worst-case data and failure states, use the `harden-ui` skill. For a review of code changes, use the `code-review` skill.

## Set the target

Resolve the request to source files and, when the app runs, a URL. Prefer a narrow target, because a section reviewed closely yields more than a whole page at a glance. Read `PRODUCT.md` and `DESIGN.md` when they exist. Choose the surface's mode as the "Choose the mode" step of `design-ui` describes.

Take full-page screenshots at 390, 768, and 1440 pixels, or at the widths the product ships at. Add screenshots of the states the target has, such as an open menu or a form error. When no browser tool is available, the design lens cannot run. Say so at the top of the report and run only the implementation lens.

Load the `design-ui` skill, and write down the absolute paths of `references/craft.md`, `references/tells.md`, and `references/motion.md` under the base directory that the harness reports when it loads the skill, so that the lenses can read them.

Finish when the target, the mode, every screenshot path, and the three reference paths are written down.

## Run the two lenses

Start two subagents in one message, one per lens, with the briefs below. Neither may see the other's output, because one lens's findings anchor the other's judgment. If subagents are unavailable, run the design lens first and write down its findings before you read any code, then run the implementation lens. Say at the top of the report that both lenses ran in one context.

Both lenses use these severities:

- **P0:** The visitor cannot complete the task or cannot see content.
- **P1:** The visitor has significant difficulty, or the page fails WCAG AA.
- **P2:** An annoyance that has a workaround.
- **P3:** Polish with no real effect on the visitor.

Design lens brief:

```
Review only. Do not edit files or start subagents.
Target: <target>. Mode: <mode>. Product: <one line from PRODUCT.md, or "unknown">.
Screenshots: <paths>.
Judge only the screenshots, not the code. Make each pass on its own:
1. Glance for one second: what do you see first? Then read for five seconds as a stranger:
   can you say what this is, who it is for, and what to do next?
2. Squint: does the page reduce to two or three masses with clear differences in size?
3. Cover the name: could this page belong to a competitor or to another industry?
   Does the page's idea reach the last section?
4. Edges: count the distinct left edges of text blocks. Two or three means a composed page.
5. Space and frame: equal outer margins, gaps between sections larger than gaps inside them,
   and no accidental holes.
6. Type: the step from body to headline, the number of sizes, orphaned words, line length.
7. Color: which color covers most of the surface, and in how many places the accent appears.
8. Images: real and doing a job, with consistent crops and treatment, and no placeholders.
9. Sameness: one word per section's layout. The same word twice in a row is a finding.
10. Phone: its own composition, or the desktop layout squeezed?
11. Substance: does every section deliver its content in full?
12. Tells: compare against <tells.md path>.
Severities: <the four severity lines>.
Reply with one line per finding, named the way a designer would name it to a colleague:
D1 [P0|P1|P2|P3] <screenshot>: <what is wrong>. Fix: <specific change>.
Then list three things that work.
```

Implementation lens brief:

```
Review only. Do not edit files or start subagents.
Target: <source files>, <URL or "not running">.
Check the code, and the rendered page when it runs:
- Accessibility: contrast, keyboard access and focus, semantic HTML and heading order,
  labels and accessible names, alt text, reduced motion.
- Responsive: fixed widths, overflow at 320px, touch targets under 24 by 24 CSS pixels,
  text at 200% zoom.
- Theming: colors and sizes hard-coded outside the tokens, and dark mode.
- Performance: animated layout properties, unoptimized images, layout shift,
  needless re-renders.
- Motion: compare against <motion.md path>.
- Craft: compare against <craft.md path> and <tells.md path>.
Severities: <the four severity lines>.
Reply with one line per finding:
I1 [P0|P1|P2|P3] <file>:<line>: <what is wrong and who it affects>. Fix: <smallest change>.
Standard: <WCAG success criterion, when one applies>.
Then list three things that work.
```

Finish when both lenses have replied, or the report's first line names the lens that could not run.

## Verify and rank

Check each finding against its screenshot or its file and line before you report it. Drop findings the evidence does not support, merge duplicates across the lenses, and correct severities that do not match the definitions. Keep P3 findings few, because a long tail buries the findings that matter.

Then choose the three changes that would improve the design most. Rank problems in this order, because a fix lower in the list cannot rescue a problem higher in it: the idea, hierarchy, composition, type, imagery, color, detail, and motion.

Finish when every finding has evidence, a severity, and a fix.

## Report and stop

Report in this order:

1. How the lenses ran, and any lens that could not run.
2. The three changes that would improve the design most.
3. A findings table with the columns `#`, `Severity`, `Where`, `Problem`, and `Fix`, with P0 findings first.
4. What works, so that the user knows what not to touch.
5. What you could not check.

End with one question: which findings to fix. Put nothing after the question.

## Check the review

- Both lenses ran in isolation, or the report says they did not.
- Every finding cites a screenshot or a file and line, and you verified it.
- No fix was applied before the user chose findings.
