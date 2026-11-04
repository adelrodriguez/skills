# App screens

Rules for Operate surfaces, such as dashboards, admin pages, settings, and editors, plus a section for Read surfaces. On these screens, familiarity is a feature. A person who knows the category should trust every component at once. The failure to avoid is strangeness without purpose, not plainness.

## Start from the question

- Write the screen's one question in one line, such as "Which deploy broke?" The block that answers it is the largest, comes first in reading order, and decides what the screen leaves out.
- Name the one finding in the current data that most needs attention, such as "the 23:28 deploy doubled the error rate". Put it under the title, next to the action it drives.
- Put the most frequent job one click from the first screen.
- At 1440 by 900 pixels, show the header and first rows of every block the brief names. Cap long lists at 4 to 6 rows with a "View all" link.
- Name the product and the current scope, such as the workspace or account, in the shell.

## Type and color

- Use one typeface, a fixed rem scale with a ratio of 1.125 to 1.2, titles of 18 to 32 pixels, and figures of 16 to 40 pixels. Use a noun title, with no hero header or greeting.
- Put color on data, not on chrome. Colored pixels stay at a few percent of the screen, and the accent marks primary actions, the current selection, and states.
- Define the state colors once: hover, focus, active, disabled, selected, loading, error, warning, success, and info.
- Color a change by whether it is good or bad, not by whether it went up or down. Latency, errors, cost, and churn are better when they fall. Show zero or undefined change in gray, and a change from zero as "+4 (new)".
- Use a second neutral for sidebars and panels. On light screens, the sidebar sits on the page ground. On dark screens, use true neutral grays rather than navy or slate.

## Components

- Show KPIs as type, not tiles: one container split by 1px dividers, with the label above the value. Never put an icon in a colored circle or a sparkline on a KPI. The figure that answers the screen's question is the largest, at about 1.3 times its siblings.
- Give each chart one question and one hue, with at most four hues on the screen. Draw a single series with no legend, 3 to 5 faint gridlines, and a 2px straight line with no gradient fill.
- Build tables from rules and alignment. Use 12px gray sentence-case headers and right-aligned tabular figures, with no zebra stripes or header bands. Give each row one status mark and an action only where one is needed.
- Draw status pills as a pale tint with dark text of the same hue, and only inside rows or beside a value.
- Keep surfaces flat, separated by a 1px border or a step in tone. Shadows go only on what floats.
- Use one outline icon set at 14 to 20 pixels, in gray.
- Show skeletons while loading instead of a spinner in the middle of content. An empty state keeps its frame and says what fills it.
- Keep one component vocabulary across screens. If "Save" looks different in two places, one of them is wrong.
- Use the standard patterns: a top bar with side navigation, breadcrumbs, tabs, and a command palette. Never restyle scrollbars, form controls, or modals into something new.

## Tells of generated dashboards

- A dark or tinted sidebar with a colored active pill and a left bar.
- "Welcome back" with a waving hand.
- Four KPI cards with icons in tinted circles and a green "+12.5%" on each.
- A gradient area chart with a smoothed line and a dot on every point.
- A rainbow chart palette with one hue per bar.
- Placeholder people and companies, round vanity totals, and totals that do not add up.
- Pagination under a five-row list.

## Read surfaces

- Set body text at 65 to 75 characters per line. Tables can run wider.
- Write headings that name their content, give long pages a visible table of contents, and link back to the index from every page.
