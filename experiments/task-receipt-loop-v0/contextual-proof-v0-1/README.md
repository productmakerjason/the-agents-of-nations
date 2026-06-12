# Contextual Proof Object v0.1

This experiment extends Task Receipt Loop v0 from fully machine-checkable completion into partially verifiable agent work.

The goal is not to prove that a task is perfectly completed.

The goal is to test whether AoN can represent a more realistic marketplace flow:

requester task
→ worker claim
→ submitted evidence
→ contextual proof object
→ requester acceptance or rejection
→ receipt or dispute record

## Core problem

In agent work markets, many tasks cannot be automatically verified as simply complete or incomplete.

Examples:

- research tasks
- lead discovery
- summary generation
- strategy drafts
- document review
- workflow recommendations

For these tasks, the important question is not only:

> Did the agent say it was done?

The better question is:

> What claim was made, what evidence supports it, what remains unverified, and did the requester accept the result?

## Hypothesis

A partially verifiable task can be represented without overclaiming completion if AoN separates:

- task_ref
- worker claim
- target evidence
- support_level
- requester acceptance
- receipt or dispute state

## Minimal proof object

This experiment keeps the proof object intentionally small.

Required fields:

- task_ref
- target_evidence
- support_level

Optional fields may be added later, but are not required in this version.

## What this experiment tests

This experiment tests whether AoN can handle a task that is not fully machine-verifiable.

The expected result is not `completed`.

The expected result is:

- `partially_supported`
- `requester_acceptance_required`

## What this experiment does not do

This experiment does not include:

- crypto
- real payment
- reputation
- dashboard
- login
- open marketplace submission
- full dispute court
- autonomous payment release

## Success criteria

This experiment passes if:

1. A partially verifiable task exists.
2. Worker claim and proof object are separated.
3. The proof object does not overclaim completion.
4. The proof object uses support_level.
5. Requester acceptance exists as a separate state.
6. A receipt is issued only for the accepted scope.
