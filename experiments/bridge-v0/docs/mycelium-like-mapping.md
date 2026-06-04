# Day 3 Mapping Rules — Mycelium-like Resolution Note to CCPP v0

## Purpose

This document explains how the representative `mycelium-like-resolution-note.json` sample maps into the Common Completion Proof Profile v0.

This is not an official Mycelium schema.

It is a representative compatibility test based on the publicly described idea of a git-ledger-backed Resolution Note.

## Input model

Representative input:

```json
{
  "commit_ref": "commit_demo_8b7c",
  "output_hash": "outputhash_demo_456",
  "filesystem_changes": [
    "tasks/task-001/result.json",
    "receipts/task-001.receipt.json"
  ],
  "execution_receipt": "exec_receipt_demo_789",
  "signature": "sig_demo_ed25519"
}
```

## Output model

CCPP v0 output:

```json
{
  "claim": "task completed",
  "task_id": "commit_demo_8b7c",
  "evidence_type": "git_artifact",
  "proof_source": "durable_record",
  "target_reference": "exec_receipt_demo_789",
  "validation_result": "passed",
  "timestamp": "unknown",
  "issuer": "mycelium_git_ledger"
}
```

## Field mapping

| Mycelium-like field | CCPP v0 field | Reason |
|---|---|---|
| `commit_ref` | `task_id` | The commit reference anchors the task state in the git ledger. |
| `execution_receipt` | `target_reference` | The execution receipt is the strongest available reference to the completed operation. |
| `output_hash` | fallback for `target_reference` | If no execution receipt exists, the output hash can still identify produced output. |
| `signature` exists | `proof_source = durable_record` | A signed git note implies a durable record rather than an agent self-report. |
| `signature` + `execution_receipt` exist | `validation_result = passed` | The MVP treats signed receipt-backed evidence as enough to support completion. |
| missing `signature` or `execution_receipt` | `validation_result = unknown` | Without both, the profile does not claim completion has been verified. |
| fixed string | `claim = task completed` | The MVP only tests completion-proof compatibility. |
| fixed string | `evidence_type = git_artifact` | This sample represents a git-ledger-backed proof artifact. |
| fixed string | `issuer = mycelium_git_ledger` | The representative issuer is the git ledger mechanism. |
| no timestamp field | `timestamp = unknown` | The representative sample does not include a timestamp. |

## Why `timestamp` is unknown

The representative sample does not include an explicit timestamp.

In a real implementation, the timestamp might come from:

- the git commit timestamp,
- the Resolution Note metadata,
- the execution receipt,
- an external ledger or signing event.

CCPP v0 keeps the field as `unknown` instead of inventing a timestamp.

## What this does not prove

This mapping does not prove:

- the cryptographic validity of the signature,
- the correctness of the real upstream schema,
- the full semantics of Mycelium’s git-note mechanism,
- whether the signed completion was authorized,
- whether the completed outcome was desirable or in scope.

It only tests whether a git-ledger-style completion artifact can be read through a shared CCPP v0 structure.

## Day 6 usage question this mapping supports

When sent back to a git-ledger or receipt-system builder, the important question is not:

> Is this concept right?

The important question is:

> If another evaluator, workflow, or agent market had to consume your Resolution Note, what field would be missing from this profile?
