# Feature flags

## Candidates

Flags whose rollout or retirement is complete, along with the branches that can no longer run. Count distinct flag keys, with their evaluation sites listed under each key.

## Detect

Find flag definitions, evaluation calls, defaults, and tests. Read the provider's current configuration when available, including environments, targeting rules, cohorts, variants, and supported clients.

A constant development value or a fully enabled production default is a candidate signal, not proof of retirement.

## Prove unused

The final value is settled for every supported environment and audience. The flag has no remaining rollout, experiment, emergency-switch, or rollback purpose, and supported clients do not need another branch or fallback.

Record the final value and the evidence that the flag can be retired. A percentage alone does not establish that decision.

## Send to Ask

- Provider state or targeting rules that cannot be read.
- Flags still used as operational switches, experiments, or rollback controls.
- Different values across supported environments or clients.
- Evaluation calls whose required side effects, such as telemetry, are unclear.

## Remove

Keep the settled branch and remove the flag check, unreachable branch, obsolete local definition, and tests of the retired alternatives. Preserve required side effects and coverage of the surviving behavior.

Run the affected flows with the settled behavior and verify that the key has no remaining repository consumer. Deleting a provider flag is a separate external change; this target removes repository code and reports any provider cleanup still needed.
