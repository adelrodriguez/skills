# Boundaries

## Candidates

External input that reaches domain code without parsing into a domain type. External input includes request bodies, query strings, headers, environment variables, config files, CLI arguments, database rows, queue messages, webhook payloads, `localStorage`, and responses from other services. Also validation repeated deep in the call chain, which shows that the boundary does not parse.

## Detect

- Search for `JSON.parse(...) as`, `as unknown as`, `response.json() as`, and generic fetch helpers typed by the caller.
- Search for direct reads of `process.env`, `import.meta.env`, `os.environ`, and `req.body` outside a config or handler module.
- Search for database query results cast to domain types without a schema.
- Search for the same check, such as `if (!email.includes("@"))`, in several functions on one call path.

## Confirm

A value with the wrong shape can arrive, and the code accepts it and fails later or stores it. For example, a webhook sends `amount` as a string, the cast hides it, and `amount + fee` concatenates instead of adding. Or a missing environment variable becomes `undefined` and fails on the first request instead of at startup.

## Reject

- A schema parses the value at the boundary, and the cast only names the parsed type.
- The source is generated from the same schema the code uses, such as a typed client generated from an OpenAPI file the repository owns, and the schema version cannot drift.

## Encode

Parse at the boundary with the repository's schema library, and pass the parsed domain type inward. Parse configuration and environment variables once at startup, so a missing value fails before the first request. Delete the repeated checks deeper in the call chain once the boundary parses.
