# Craft

Rules for building an interface. The checks apply to every screenshot. The sections after them hold the rules behind the checks.

## Checks on the render

- **Contrast:** Body and placeholder text reach 4.5:1, and large text reaches 3:1. On a colored surface, secondary text takes a tint of that hue instead of gray.
- **Headings:** Every heading fits in two lines at every width. The first screen says what this is and what to do next, and its title is the page's one `h1`.
- **Measure:** Body text runs 45 to 75 characters per line.
- **Frame:** The left and right margins are equal at every width. No section leaves half its width empty, and no stretch taller than half a screen holds nothing.
- **Spacing:** Related items sit close and unrelated items sit far apart. The gap between sections is clearly larger than any gap inside one, and a heading has more space above it than below.
- **Overflow:** Nothing overflows or scrolls sideways at 320 pixels, and nothing covers a heading or a button at any scroll position.
- **States:** Every control has hover, focus, active, and disabled states. Every view that loads data has loading, empty, and error states.
- **Keyboard:** Every control works from the keyboard in reading order and shows a visible focus ring.
- **Browser surfaces:** Text selection, focus rings, the caret, scrollbars, and link underlines take their colors from the palette instead of browser defaults.
- **Coverage:** Every requirement in the brief is on the page and can be found within a few seconds.

## Type

- Use one typeface or two. With two, make them clearly different. Choose them for this brief, not the faces you would use on any project.
- Self-host the display face the plan names. A system font standing in for it is a failure, not a fallback.
- On Persuade and Experience surfaces, let two or three sizes do the visible work: one very large and one small. Make the headline at least three times the body size, and use at most five sizes on the page.
- On Operate surfaces, use a fixed rem scale with a ratio of 1.125 to 1.2.
- Set display type with tracking between -0.02em and -0.04em, never tighter, and line height between 0.85 and 1.05.
- Set body text at 16 to 20 pixels with line height 1.45 to 1.6. Give serif body text slightly more line height than sans.
- Left-align text by default, and center at most one moment on the page.
- Use tabular figures for numbers that align in columns or update in place.

## Color

- Use one ground, one ink, and one accent. The accent marks the primary action and at most one other thing.
- Set running text in the full ink color. A page set in soft gray reads as unfinished.
- Separate surfaces with a small step in tone. Use a border or a shadow, never both.
- Choose light or dark from where and when people use the product, not from the category.
- Give a shadow an offset and a soft blur, and only to things that float, such as menus and dialogs. A colored glow with no offset is decoration.

## Layout

- Use one grid and one pair of outer margins everywhere. Text blocks share two or three left edges across the page.
- Give neighboring sections different compositions. Name each section's layout in one word, such as split, list, full-bleed, or statement. The same word twice in a row shows the template.
- Keep asymmetry inside the grid. Balance an off-center element with something on the far side.
- Compose the phone layout on its own, with its own crops and line breaks, instead of squeezing the desktop layout.
- Use fluid type only on Persuade and Experience surfaces. On Operate surfaces, change the structure at breakpoints instead, such as collapsing the sidebar.

## Imagery

- Choose pictures in this order:
  1. The project's own pictures.
  2. Generated pictures, when an image tool is available.
  3. Real pictures of the subject's world from open collections.
  4. Pictures drawn in code from the subject.
  5. Type and color alone.
- Prefer one dominant image to six small ones. Keep crop ratios and treatment consistent across the page.
- Present a found picture as the world around the client, never as the client's own product, place, or people. Credit it in the footer and list it in the report.
- Show software through its own interface, built in HTML with believable data. Never ship gray boxes, lorem ipsum, or fake screens made of bars.
- Draw icons from one library or one set of authored SVGs, with one stroke width and weight.

## Components

- Decide the button shape once: square-cornered or fully round.
- Give the navigation a wordmark, three to five plain links, and one action.
- Use a modal only when the task needs an interruption or protected focus.
- Let dropdowns and popovers escape their container through `<dialog>`, the popover API, or a portal, so that an `overflow: hidden` ancestor cannot clip them.
- Check CSS specificity where a class selector and an element selector set the same spacing, because one silently cancels the other.
