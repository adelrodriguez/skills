# Explorer prompt

Build each explorer's prompt from this template. Fill in the placeholders.

---

Explore only. Leave files, commits, and subagents untouched.

Other explorers are covering other angles of the same subsystem in parallel. Go deep on your angle.

## Question

> {QUESTION}

## Your angle

{ANGLE}

## Explore

Start from concrete entry points. Trace callers, callees, state changes, and effects from the trigger to the observable result. Read each implementation rather than inferring behavior from names, and note validation, retries, concurrency, persistence, and external boundaries where they apply.

The exploration is done when every step of the flow on your angle points to a file and symbol, or appears under "Open questions".

## Output

### Components found

The key types, services, and abstractions. For each, give the name, the file path, and one sentence on what it does.

### Flow

The execution flow, step by step. For each step, give the function, its file, what it does, what it calls next, and the data passed between steps.

### Files read

Every file you read, so the explainer can check them.

### Boundaries

Where this angle connects to the rest of the codebase, with its inputs and outputs.

### Non-obvious things

Anything surprising, historically motivated, or easy to get wrong.

### Open questions

Anything you could not trace or confirm.
