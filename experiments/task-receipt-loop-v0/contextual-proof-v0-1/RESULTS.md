# Contextual Proof Object v0.1 — Results

## Experiment question

Can AoN represent partially verifiable agent work without falsely marking it as fully completed?

This experiment tested whether a worker submission can move through:

task
→ worker submission
→ contextual proof object
→ reviewer/requester acceptance state

without AoN overclaiming completion.

## Test task

Task ID: `task_003`

Task type: `partial_research_submission`

Instruction:

> Find 3 relevant discussions about agent workflow completion proof. For each item, include source, relevance_reason, and boundary.

This task was intentionally not fully machine-verifiable.

The expected support level was:

`partially_supported`

## Artifacts created

- `tasks/task_003.json`
- `submissions/task_003_submission_gpt.json`
- `proofs/proof_task_003.json`
- `acceptance/requester_review_task_003_gpt_needs_revision.json`
- `acceptance/requester_review_task_003_claude_accepted_with_limitations.json`

## What happened

### Worker submission

The GPT worker produced a structurally valid submission:

- 3 items were submitted
- each item included `source`, `relevance_reason`, and `boundary`
- worker non-claims were included
- no receipt was created
- the worker did not claim requester acceptance

However, the submitted sources were broad category-level references rather than concrete discussion URLs.

Examples:

- LangChain / LangGraph discussions and documentation
- AutoGPT / Agent Protocol discussions
- OpenAI Evals / SWE-bench style evaluation discussions

## AoN proof object result

AoN normalized the worker submission as:

`partially_supported`

AoN did not mark the task as completed.

Observed:

- submission exists
- item count matches minimum requirement
- required fields are present per item
- worker non-claims are present

Not observed:

- concrete discussion URLs verified
- source quality independently verified
- market demand verified
- business value verified
- requester acceptance granted

Recommended next state:

`requester_review_required`

## Reviewer results

### GPT reviewer

Result:

`needs_revision`

Reason:

The submission satisfied the structural shape but did not provide concrete source references. GPT required specific discussion threads, documentation pages, issues, papers, or benchmark pages before acceptance.

Next state:

`awaiting_worker_revision`

### Claude reviewer

Result:

`accepted_with_limitations`

Reason:

Claude accepted the submission as a first-pass landscape map and scoping artifact. Claude did not treat it as a fully executed research submission.

Accepted scope:

- structural requirement met
- required fields present
- topical relevance acknowledged
- worker non-claims present
- partial research value recognized

Non-claims:

- concrete discussion URLs not provided
- source quality not independently verified
- specific discussion threads not identified
- market demand not assessed
- business value not assessed
- partial acceptance does not constitute full task completion

Next state:

`accepted_with_limitations_logged`

## Key finding

The same partially verifiable worker submission produced different reviewer outcomes:

- GPT reviewer: `needs_revision`
- Claude reviewer: `accepted_with_limitations`

This is not a failure.

This shows that partially verifiable agent work cannot be reduced to a single automatic completion verdict.

AoN needs to record:

- who reviewed the work
- what scope was accepted
- what was not claimed
- what revision was required
- whether the result is eligible for limited receipt, revision, or dispute

## Main learning

For partially verifiable tasks, AoN should not issue a full completion receipt after automatic review.

Instead, AoN should produce a contextual proof object and route the task into one of these states:

- `requester_review_required`
- `accepted_with_limitations`
- `needs_revision`
- `rejected`
- `disputed`

Only accepted scope should be eligible for receipt.

## What this validates

This experiment supports the hypothesis that AoN can act as a market-readable state layer for agent work.

It does not prove that the work was fully completed.

It proves that AoN can prevent overclaiming by separating:

- worker claim
- evidence
- support level
- reviewer acceptance
- non-claims
- next state

## What this does not validate

This experiment does not validate:

- external market demand
- payment release
- reputation scoring
- source quality
- business value
- autonomous task discovery
- real marketplace liquidity

## Current conclusion

Contextual Proof Object v0.1 passes as a controlled experiment.

It shows that AoN can represent partially verifiable agent work without forcing a false completed/not-completed binary.

The correct next direction is not to add more schema fields.

The next direction is to test whether a revised worker submission with concrete sources can move from:

`needs_revision`
→ `worker_revision_submitted`
→ `accepted_with_limitations` or `accepted`
→ `limited_receipt_candidate`

## Next recommended test

Run a revision loop.

The worker should revise task_003 by replacing broad source descriptions with concrete references.

Required revision:

- provide 3 concrete source references
- include title plus URL or stable identifier where possible
- keep `source`, `relevance_reason`, and `boundary`
- do not create receipt
- do not claim requester acceptance

Expected decision after revision:

- if concrete references are adequate: `accepted_with_limitations`
- if still broad or unverifiable: `needs_revision`
