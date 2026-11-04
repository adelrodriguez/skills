# Motion

Rules for adding or reviewing motion. Decide whether something animates before you decide how. The `restraint` skill's frequency rule applies first.

## Decide whether it animates

| How often people see it | Decision |
|---|---|
| 100 or more times a day, or triggered from the keyboard | No animation |
| Tens of times a day, such as hover effects and list navigation | Remove or reduce the animation |
| Occasionally, such as modals, drawers, and toasts | Standard animation |
| Rarely, such as onboarding and first-time moments | Room for delight |

Every animation needs a purpose: spatial consistency, a change of state, feedback on an action, an explanation, or softening an abrupt change. Looking good is not a purpose for anything people see often.

On Persuade and Experience surfaces, compose one authored moment, such as a page-load sequence or a reveal, rather than scattered effects. On Operate surfaces, motion only shows a change of state, and it never stages a page-load sequence.

## Easing

- Entering or exiting: ease-out.
- Moving or morphing on screen: ease-in-out.
- Hover and color changes: ease.
- Constant motion, such as a progress bar or marquee: linear.
- Never use ease-in on UI, because it delays the moment the user watches most.
- Use strong custom curves, because the built-in ones are weak: `cubic-bezier(0.23, 1, 0.32, 1)` for ease-out and `cubic-bezier(0.77, 0, 0.175, 1)` for ease-in-out.
- Keep bounce and elastic easing out of UI. Limit spring bounce to 0.1 to 0.3, for drag and playful moments only.

## Duration

| Element | Duration |
|---|---|
| Press feedback | 100 to 160ms |
| Tooltips and small popovers | 125 to 200ms |
| Dropdowns and selects | 150 to 250ms |
| Modals and drawers | 200 to 500ms |

Keep other UI animation under 300ms. Explanatory and marketing animation can run longer.

## Physical correctness

- Never animate from `scale(0)`. Start from `scale(0.95)` with `opacity: 0`.
- Scale popovers, dropdowns, and tooltips from their trigger by setting `transform-origin`. Modals stay centered.
- Give pressable elements `transform: scale(0.97)` on `:active`.
- Once one tooltip is open, open neighboring tooltips at once, with no delay and no animation.
- Make deliberate actions slow and system responses fast. A hold-to-delete fills slowly and releases quickly.

## Interruptions and performance

- Use CSS transitions, not keyframes, for anything people trigger rapidly, such as toasts and toggles. A transition retargets from its current state, and a keyframe animation restarts from zero.
- Use springs for gestures that can reverse partway through.
- Animate `transform` and `opacity`. Animating `width`, `height`, `margin`, `padding`, `top`, or `left` runs layout on every frame. Blur, `clip-path`, masks, and `backdrop-filter` are allowed while they stay smooth, with blur kept under 20px.
- Never write `transition: all`.
- Set a transform on the element itself rather than through a CSS variable on its parent, which recalculates styles for every child.
- Stagger group entrances by 30 to 80ms, and keep the group interactive while the stagger plays.

## Accessibility

- Honor `prefers-reduced-motion` with gentler motion rather than none. Keep opacity and color changes, and drop movement.
- Gate hover motion behind `@media (hover: hover) and (pointer: fine)`, because touch screens fire hover on tap.
