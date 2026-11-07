# Sources

Each category below is one investigator's source. Append the category's section to that investigator's prompt. The tool names are examples. Adapt the searches to whichever tool is available.

| Category | Example tools | Best at |
|---|---|---|
| Source control | `git`, `gh` | Rationale recorded during implementation and review |
| Issue tracker | Linear, Jira, GitHub Issues | The product or business reason |
| Documents | Notion, Confluence, Google Docs | Design rationale written before the code |
| Team chat | Slack, Discord, Microsoft Teams | Discussion that never reached a doc |
| Observability | Datadog, Grafana, Honeycomb | Runtime behavior that prompted the code, such as timeouts and retries |
| Error tracking | Sentry, Rollbar, Bugsnag | Exceptions that prompted defensive or corrective code |
| Analytics warehouse | Databricks, Snowflake, BigQuery | Data behind thresholds, flags, experiments, and migrations |

## Source control

Covers commits, PR descriptions and reviews, code comments, TODOs, ADRs, tests, changelogs, and files changed in the same commits.

- Trace history through renames with `git log --follow`.
- Find the commit that added or removed an exact value with `git log -S '<string>'`, or a pattern with `git log -G '<regex>'`.
- Read the full PR body, reviews, and comments for each substantive commit with `gh pr view <pr> --comments`, and the inline review comments with `gh api --paginate repos/<owner>/<repo>/pulls/<pr>/comments`. `gh pr view` leaves out inline comments, where most review findings live.
- Search for ADRs, and for TODO, FIXME, HACK, and NOTE comments near the target.
- Read the tests added with the change. Their names and inputs often show the edge case that motivated it.

## Issue tracker

- Fetch the tickets linked from commits and PRs first, including every comment.
- Search by feature name, key symbol, and business terms, with several phrasings.
- Walk from a sub-issue to its parent and project. The parent often states the reason.
- Read labels and milestones, such as `customer-request`, `compliance`, or `incident-followup`, and the attached specs.
- Read the whole history. A ticket may have been reopened with a different scope, or closed as a duplicate of the real one.
- Treat boilerplate "why" sections, such as "improve user experience", as no answer.

## Documents

- Search for the feature name, key symbols, and terms from the PR and tickets.
- Prefer specs, design docs, RFCs, and decision records dated before the code shipped.
- Compare the doc's date with the ship date. A plan written earlier may have changed.

## Team chat

- Search for the PR URL or `/pull/<number>`, the ticket ID, and error strings the code handles.
- Search messages from the PR author around the merge date.
- Read each full thread. A single message read without its thread can mean something else.
- Treat a joke or offhand remark as no decision. Look for considered discussion.
- Record the retention limit when nothing exists before a date, and note that DMs are not searchable.
- When the tool is not authenticated, stop and report the gap.

## Observability

- Look for monitors, incidents, and metrics around the dates the target was added or changed.
- Match values in the code, such as timeouts and limits, against observed latencies and error rates from that time.

## Error tracking

- Search for the exception types and messages the target catches or guards against.
- Compare when each error was first and last seen with the commit dates. An error that stops after the fix supports the link.

## Analytics warehouse

- Query the tables behind the flag, experiment, or threshold, for the time window around the change.
- Report fully qualified table names, the time windows, and the numeric results, such as counts, percentiles, and first and last seen times.

## Defensive code

Append this section as well when the target looks defensive. Run these searches inside the investigator's own source:

- Issue tracker: tickets labeled `incident`, `sev-*`, `postmortem`, or `reliability`.
- Team chat: incident channels around the dates the target was added.
- Source control: commits such as "fix for incident", "add defensive check", "hotfix", or a revert followed by a reapply.
- Observability and error tracking: incidents and error spikes just before the target was added.
