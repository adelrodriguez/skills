# Failure signatures

What a break looks like, its usual cause, and its fix. Find the row that matches the screenshot or the behavior.

## Layout and text

| What you see | Cause | Fix |
|---|---|---|
| An avatar or icon squished into an oval | A flex child shrinking | `flex-shrink: 0` on the avatar, the icon, and any fixed-size box |
| Text overflows its box instead of wrapping or truncating | A flex or grid child with `min-width: auto` | `min-width: 0` on the text column, or `minmax(0, 1fr)` in a grid |
| An email or URL runs past the edge | No break opportunities in the string | `overflow-wrap: anywhere` on that element |
| A trailing action, such as a menu button, is pushed off-screen | The middle content took all the space | `min-width: 0` on the middle, and `flex-shrink: 0` on the action |
| A badge wraps onto two lines | The badge is allowed to shrink | `white-space: nowrap; flex-shrink: 0` on the badge, then decide what yields instead |
| An avatar looks adrift beside a three-line name | `align-items: center` on rows of varying height | `align-items: flex-start` once the text can wrap |
| The last row is cut off mid-glyph at a hard edge | A fixed-height container with no scroll affordance | A visible scrollbar or a fade mask, and an intentional `overflow` value |
| A long word in a heading breaks mid-word | `word-break: break-all` | `overflow-wrap: anywhere`, which breaks only when it has to |
| Wrong initials, such as `J` for "Jo" or `�` for a name that starts with an emoji | Initials from `.split(' ')[0][0]` | Initials from grapheme clusters with `Intl.Segmenter`, first and last word, and a fallback icon |
| An orphaned `—` or an empty line where an optional field was | A placeholder rendered for a missing value | Omit the line, or reserve its height on purpose |
| "1 members" or "0 member" | A hard-coded plural | `Intl.PluralRules`, or a separate string per plural form |
| Numbers jitter when they update, or columns misalign | Proportional figures | `font-variant-numeric: tabular-nums` |
| `1284`, `NaN`, or `undefined` on screen | A raw number rendered | `Intl.NumberFormat` with the user's locale, and a guard for missing values |
| A translated button label overflows | A fixed-width button | Width from content with a `min-width`, never a fixed `width` |
| Diacritics or tall scripts clipped at the top or bottom | A tight `line-height` with `overflow: hidden` | A looser `line-height`, or no clipping on text boxes |
| A broken-image icon in an avatar | No `onError` fallback | Fall back to initials, and use `object-fit: cover` for any aspect ratio |
| Truncated text that no one can read in full | `text-overflow: ellipsis` and nothing else | A `title` attribute or tooltip, and the full value in a detail view |
| Raw `<b>`, `&amp;`, or `**text**` on screen | Escaping at the wrong layer | Escape once, at render. Never pass user data to `dangerouslySetInnerHTML`. |
| Icons and padding on the wrong side in RTL | Physical properties such as `margin-left` | Logical properties such as `margin-inline-start`, and mirrored directional icons |
| Scrolling 1,000 rows stutters | Every row rendered | Virtualize or paginate, and say which |

## Requests and actions

| What you see | Cause | Fix |
|---|---|---|
| A spinner that never stops | A request with no timeout | An `AbortController` with a timeout, then an error state with a retry button |
| `TypeError: Failed to fetch` or a stack trace on screen | The raw error rendered | Map each failure to a message that says what happened and what to do next, following `writing-for-humans` |
| The form clears after a failed submit | State reset on error | Keep the input, and show each error beside its field |
| Duplicate records after a double click | The button stays active while the request runs | Disable the button while the request is pending, and send an idempotency key when the API accepts one |
| A whole page goes blank when one widget fails | No error boundary | An error boundary around each region that loads its own data |
| Content jumps when loading finishes | A skeleton shaped differently from the content | A skeleton with the content's dimensions |
| A change stays on screen after its request failed | An optimistic update with no rollback | Roll back the change and say that it failed |
| An action shows and then fails with 403 | No permission check in the UI | Hide the action, or disable it with the reason, based on the user's role |
| A drag stays stuck after an interruption | No handling for cancelled pointers | Clear the drag state on `pointercancel`, `lostpointercapture`, and `blur`, and set `touch-action` on the drag surface |
| A screen reader says nothing when results update | No live region | Put the updating content, or a summary of it, in an `aria-live="polite"` region |

## Truncate, wrap, or clamp

Every long string forces this choice. Make it for each field, not for the whole page.

- **Wrap** text that people need in full to identify something, such as names and titles in a detail view. Two lines are usually fine. Four lines mean the column is too narrow.
- **Truncate at the end** for secondary text whose start carries the meaning, such as a role, a description, or a message preview. Pair it with a way to see the full value.
- **Truncate in the middle** when items differ at the end, such as file names, emails that share a long domain, paths, and hashes. End truncation makes them look identical.
- **Clamp** multi-line previews in cards with `line-clamp: 2`, so that card heights stay predictable.
- **Never truncate** numbers, amounts, dates, or anything people compare. Give them the room.
