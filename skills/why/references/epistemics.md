# Epistemics

The rules for weighing historical evidence and stating confidence. Code shows what it does, not why it exists. The reason lives in commits, PRs, tickets, docs, and conversations, which are incomplete and sometimes contradict each other.

## Confidence tiers

Every claim sits in exactly one tier. The tier decides its section and its wording.

| Tier | Meaning | Wording |
|---|---|---|
| Direct | An author wrote the reason, such as a PR saying "fixes pagination for users with more than 1000 items" or a comment saying "clamp to 100 because the upstream API rejects larger values". | Plain and cited: "This exists because X." |
| Supported | Several indirect items point to one conclusion, such as a PR titled "improve performance", a `perf` ticket label, and tests that all use very large inputs. | Confident and cited item by item: "The evidence points strongly to X: A, B, C." |
| Inferred | A reasonable reading that no source states, such as a same-day merge during an incident suggesting a hotfix. | Hedged, with the chain shown: "Given A and B, C seems likely because D." |
| Speculative | A plausible guess that other explanations fit equally well. | "One possibility is X, but we found no direct evidence." |
| Unknown | You searched and found nothing. | "We searched X, Y, and Z and found no evidence of why." |

Write Unknown with the exact searches: "We searched the tracker for `rate limit` and `429`, read the six PRs that touched this file since 2023, and searched the repo for the threshold value. None gave a reason."

## Wording

Reserve "because", "the reason is", "was designed to", "fixes", and "the team decided" for Direct and Supported claims, with the citation next to them.

Use hedges such as "appears to", "likely", "suggests", "is consistent with", and "may have been" for Inferred claims.

Write "the evidence suggests" in place of "I think" or "I believe". Cut "obviously", "clearly", "of course", and "just", which hide uncertainty.

## Reading the record

- **Code is mechanics, not motivation.** Cite what an author wrote as evidence of intent, never the code itself.
- **Trace past the latest commit.** The current shape is often the sum of earlier decisions, and the latest commit may only have moved the code.
- **Leave messy history messy.** A reason may no longer apply or may have been wrong at the time, and a consistent pattern may be copy-paste. Report what the record shows rather than the cleanest story.
- **Treat silence as a gap.** "Nobody mentioned security" means the record is silent, not that security was not a concern.
- **Check the user's hypothesis.** When the question proposes a reason, weigh it against the evidence like any other candidate, and say plainly whether the evidence supports it.
- **Show contradictions.** When a ticket says "customer compliance requirement" and the PR says "tech-debt cleanup", present both with citations. Both may be true, and the user decides.
- **Name each gap.** For each open question, list the sources searched, the queries, and what came back. Name the people likely to know, such as the original author or product owner.
