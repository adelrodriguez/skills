# Worst-case catalog

Realistic values that break UI, grouped by the kind of value a component renders. Use the rows that match the fields and requests in your tables. Each value is something a real user could produce, and its note says what it tends to break.

Use `example.com`, `example.org`, or `.test` domains for emails and URLs, so that no fixture points at a real inbox or site.

## People and names

| Value | Breaks |
|---|---|
| `Aleksandra Wiśniewska-Kowalczyk` | Long, hyphenated, and accented. It wraps to two lines, and the hyphen becomes a break point. |
| `Christopher Alexander Montgomery III` | A long name with a suffix. Naive first-and-last initials give `CI`. |
| `Jo` | Two letters. The name column looks empty, and naive initials give `J`. |
| `J` | One letter. Single-character initials, and a tiny click target when the name is the link. |
| `Ólafur Darri Ólafsson` | A leading accented capital. Sorting, uppercasing, and initials (`ÓÓ`). |
| `Đặng Thị Ngọc Hân` | Stacked Vietnamese diacritics, clipped by a tight `line-height` with `overflow: hidden`. |
| `王秀英` | CJK with no spaces. Word-based initials find one word, and the text can break anywhere. |
| `نور الهدى عبد الرحمن` | Right-to-left text. Punctuation and icons land on the wrong side without `dir="auto"`. |
| `Seán O'Brien-Ó Súilleabháin` | An apostrophe and accents. Escaping, initials, and search. |
| `María José de la Cruz y Fernández` | Lowercase particles. Initials and sorting by last name. |
| `dana` | All lowercase. Initials must still be uppercase. |
| `🦊 Fox` | A leading emoji. `.charAt(0)` returns half a surrogate pair (`�`). |
| `👩🏽‍💻 Priya` | A joined emoji sequence. `.length` is 7 or more, and slicing splits it. |
| `  Sam   Lee ` | Leading, trailing, and repeated spaces. Empty words in initials, and odd gaps. |
| No name, only an email | The fallback must show something. |

## Emails, URLs, and identifiers

| Value | Breaks |
|---|---|
| `bartholomew.fitzgerald@northwind-industries-holdings.example.com` | Pushes every sibling off the row without `overflow-wrap: anywhere`. |
| `a@b.co` | The shortest realistic email. A layout that assumed a long one looks empty. |
| `first.last+billing-notifications@example.com` | Plus addressing. Validation that rejects `+`, and truncation that hides the part that matters. |
| `ops@sub.department.region.example.co.uk` | Many subdomains and a two-part TLD. Domain extraction. |
| `https://example.com/workspaces/acme/projects/q3-launch/docs/9f8e7d6c5b4a?tab=comments&filter=unresolved` | A long URL. Overflow, and end truncation that hides the part that differs. |
| `9f8e7d6c-5b4a-4c3d-8e2f-1a0b9c8d7e6f` | A UUID. Fixed width, and a candidate for middle truncation. |
| `Q3 Board Deck — FINAL (revised) v12 [approved by legal].pdf` | A file name. End truncation hides the version and extension. |
| `IMG_20250914_183022_HDR_portrait_edited_edited.HEIC` | A camera file name with no break points and an uppercase extension. |
| `@a` and `@thisisaverylongusernamethatisallowed` | The extremes of a handle. |

## Labels, titles, and copy from data

| Value | Breaks |
|---|---|
| `Senior Product Design Engineer, Platform Infrastructure` | A long job title that wraps to three lines in a secondary slot. |
| `Invitation expired 12 days ago` | A long status badge that wraps or squeezes the name column. |
| `Benachrichtigungseinstellungen` | A 30-character German compound with no spaces. |
| `Paramètres de confidentialité et de sécurité` | French for "Privacy & security". Translations run about 30% longer. |
| Twelve tags on one item | Tag rows that wrap into a wall and need a `+8` overflow. |
| `customer-feedback-from-enterprise-onboarding` as one tag | A single tag wider than its container. |
| `Untitled`, an empty string, or spaces only | A missing title. A collapsed heading or a zero-height row. |
| `<script>alert(1)</script>`, `&amp;`, `**bold**` | Escaping. Each must render as literal text. |
| `Line one`, a newline, then `Line two` | A newline in a single-line field doubles the row height or vanishes. |
| A pasted description of 2,000 characters | Clamping, "Show more", and textarea growth. |
| `می‌خواهم` (Persian, with a zero-width non-joiner) | A sanitizer that strips U+200C changes the word's meaning. |
| `ی` and `ي`, `ک` and `ك` | Persian and Arabic letter variants. Search and validation that reject the other keyboard's letter. |

## Numbers and money

| Value | Breaks |
|---|---|
| `0` | Zero states, such as "0 members", an empty progress bar, and division by zero in percentages. |
| `1` | Plurals, such as "1 members" and "1 days ago". |
| `1284` | Needs a thousands separator: `1,284`. |
| `1000000` | The width of a count badge. Consider `1M` where precision does not matter. |
| `12345678.9` as currency | `$12,345,678.90` overflows a totals column. |
| `-42.5` | The minus sign, red-color logic, and parentheses in accounting formats. |
| `0.1 + 0.2` | Renders raw as `0.30000000000000004`. |
| `142%` and `-3%` | Progress bars and meters past their bounds. |
| `null`, `undefined`, `NaN` | Rendered literally. |
| `1.284` in `de-DE` and `1,284` in `en-US` | Hard-coded separators are wrong for half the world. |
| `۱٬۲۳۴` in `fa-IR` | Eastern Arabic digits. Hard-coded Western digits and number parsing. |
| A value that updates live, from `99` to `100` | A width jump and jitter without `tabular-nums`. |

## Collections

| Value | Breaks |
|---|---|
| 0 items | The empty state, and whether one exists at all. |
| 1 item | Grids that look broken with one card, and "1 of 1". |
| Exactly one page, and one page plus one | Off-by-one copy such as "Showing 40 of 40", and an empty page 2. |
| 1,000 or more items, unpaginated | Scroll performance, render time, and memory. |
| One item ten times the size of the others | Grid rows that stretch to the tallest item. |
| Items with identical names | Lists where the name is the only distinguishing field. |

## Time

| Value | Breaks |
|---|---|
| Now | "0 seconds ago" instead of "just now". |
| 12 days, 11 months, and 3 years ago | Relative-time thresholds. Switch to an absolute date after about a week. |
| A future date | "In 3 days" against "-3 days ago". |
| `1970-01-01` | A zero timestamp shown as a real date. |
| `2025-12-31T23:30:00-08:00` | A different day in UTC and in the user's time zone. |
| `1,284 hours` | A duration that never rolls up into days. |
| A date in `fa-IR` or `ar-SA-u-ca-islamic` | Persian and Hijri calendars. Use `Intl.DateTimeFormat` with the locale. |

## Images and media

| Value | Breaks |
|---|---|
| An avatar URL that returns 404 | A broken-image icon instead of the initials fallback. |
| No avatar | The fallback itself: initials, color, and size parity with real avatars. |
| A 4000 by 200 panorama as an avatar or cover | Distortion without `object-fit: cover`. |
| A 200 by 4000 image | Distortion on the other axis, and a card that grows very tall. |
| A transparent PNG logo, or a dark logo in dark mode | Invisible against the background. |
| A slow-loading image | Layout shift without fixed dimensions or `aspect-ratio`. |

## Requests and actions

| Condition | Breaks |
|---|---|
| A request that takes 3 seconds or more | Missing loading state, skeletons that do not match the final layout, and spinners that shift content. |
| A request that never answers | A spinner that never stops, with no timeout or retry. |
| The network goes offline | A raw `TypeError: Failed to fetch`, and lost input. |
| `400` or `422` with field errors | Errors shown in a toast instead of beside each field, and input cleared. |
| `401` | A generic error instead of a path back to sign-in that returns the user here. |
| `403` | Actions that appear and then fail, with no explanation. |
| `404` | A blank screen instead of a not-found state. |
| `409` | A save that overwrites someone else's change without warning. |
| `429` | Instant retries that make the limit worse, and no message. |
| `500` | Raw stack traces, or a whole page that goes blank because one region failed. |
| A partial response, with some fields missing | Misaligned rows and `undefined` in the copy. |
| A double click on submit | Duplicate records. |
| An optimistic update whose request fails | The change stays on screen with no rollback. |
| Every status value at once | All enum values in one list, such as `active`, `invited`, `expired`, and `suspended`, with varying badge widths. |
| The current user in the list | "You" labels, and actions that should not apply to yourself. |

## Environment

These are not data, but they are checked the same way: switch to the worst case, then change the setting.

| Setting | Breaks |
|---|---|
| A container 320 pixels wide | Every overflow above at once. |
| A narrow sidebar placement | A full-width component reused in a 280-pixel column. |
| A 2560-pixel window | Lines too long to read, and content stranded on one side. |
| Browser zoom at 200%, or large text | Fixed heights that clip growing text. |
| Dark mode | Hard-coded colors, invisible borders, and invisible logos. |
| `dir="rtl"` | Icons, chevrons, padding, and the order of trailing actions. |
| A touch device | Actions that appear only on hover cannot be reached. |
