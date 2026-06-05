# Task Receipt Loop v0

Task Receipt Loop v0 is a controlled file-based PoC for testing how an autonomous agent task can move from request, to worker claim, to target evidence, to acceptance, and finally to receipt issuance.

This is not a marketplace, production workflow, payment system, or security product.

It is a minimal loop for testing one question:

> When an agent says a task is complete, what evidence allows another agent, evaluator, or future market to rely on that work?

## Core distinction

A worker agent claim is not completion proof.

A receipt should only be issued when:

1. the original task has a defined completion condition,
2. the worker submits a claim,
3. target evidence satisfies the completion condition,
4. the task is accepted by either:
   - a predefined auto-accept rule, or
   - a requester approval step.

## Roles

- Requester agent: Gemini
- Worker agent: GPT
- Verifier agent: Grok
- Ledger / receipt issuer: AoN

## State flow

```text
TASK_CREATED
→ TASK_ACCEPTED_BY_WORKER
→ WORK_SUBMITTED
→ TARGET_EVIDENCE_CHECKED
→ ACCEPTED
→ RECEIPT_ISSUED
```

## What this PoC tests

This PoC tests whether a task can be represented in a way that separates:

- requester intent
- worker claim
- target-system evidence
- acceptance mode
- receipt issuance

## What this PoC does not do

This PoC does not support:

- arbitrary task submission
- arbitrary URL execution
- external payments
- real credentials
- private data
- open agent access
- production authorization
- real security guarantees

Only predefined task types and local file-based target evidence are used.

## Why this matters

For autonomous agent markets, completion cannot be based on claims alone.

A future agent market needs to know:

- what task was requested,
- who claimed completion,
- what evidence supports the claim,
- whether the evidence matched the completion condition,
- whether the result was accepted,
- whether a receipt should be issued.
