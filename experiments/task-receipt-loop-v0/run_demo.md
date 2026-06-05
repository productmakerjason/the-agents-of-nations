# Run Demo — Task Receipt Loop v0

This demo is a controlled file-based simulation.

It does not run a production agent marketplace.

## Goal

Show that a worker agent claim is not enough to issue a receipt.

A receipt is issued only when the target evidence satisfies the completion condition defined by the original task.

## Success case

1. Read `tasks/task_001.json`.
2. Read `submissions/task_001_submission_gpt.json`.
3. Read `target/target_record_task_001.json`.
4. Compare the target evidence with the task completion condition.
5. Read `verification/verification_pass_task_001.json`.
6. Read `receipts/receipt_task_001.json`.

Expected result:

```text
receipt issued
```

Reason:

```text
Target evidence contains the required task_id, created_by, and result fields.
```

## Failure case

1. Read `tasks/task_001.json`.
2. Read `submissions/task_001_submission_gpt_fail_no_evidence.json`.
3. Do not use target evidence.
4. Read `verification/verification_reject_no_evidence.json`.

Expected result:

```text
receipt rejected
```

Reason:

```text
The worker claimed completion, but no target evidence was provided.
Worker claim alone is not completion proof.
```

## What to test with Gemini / GPT / Grok

- Gemini can act as the requester and create a task.
- GPT can act as the worker and produce a submission plus target evidence.
- Grok can act as the verifier and decide whether a receipt can be issued.

The test passes only if the verifier rejects worker claims that lack target evidence.
