# Day 2 Mapping Rules — msaleme-like receipt to CCPP v0

## Purpose

This document explains how the representative `msaleme-like-receipt.json` sample maps into the Common Completion Proof Profile v0.

This is not an official msaleme schema.

It is a representative compatibility test based on the publicly described idea of an attested completion receipt.

## Input model

Representative input:

```json
{
  "receipt_id": "rct_demo_001",
  "task_hash": "taskhash_9f3a_demo",
  "actual_outcome": "success",
  "timestamp": "2026-06-04T00:00:00Z",
  "attestation": {
    "merkle_root": "merkleroot_demo_abc123",
    "evaluator": "demo_security_harness"
  }
}
```

## Output model

CCPP v0 output:

```json
{
  "claim": "task completed",
  "task_id": "taskhash_9f3a_demo",
  "evidence_type": "receipt",
  "proof_source": "durable_record",
  "target_reference": "rct_demo_001",
  "validation_result": "passed",
  "timestamp": "2026-06-04T00:00:00Z",
  "issuer": "demo_security_harness"
}
```

## Field mapping

| msaleme-like field | CCPP v0 field | Reason |
|---|---|---|
| `task_hash` | `task_id` | The task hash identifies the task being attested. |
| `receipt_id` | `target_reference` | The receipt id is the durable reference to the completion proof. |
| `actual_outcome` | `validation_result` | The outcome is normalized into `passed`, `failed`, `pending`, or `unknown`. |
| `timestamp` | `timestamp` | The original proof timestamp is preserved. |
| `attestation.evaluator` | `issuer` | The evaluator/harness is treated as the issuing authority for this representative sample. |
| `attestation` exists | `proof_source = durable_record` | Attestation implies this is not merely an agent claim. |
| fixed string | `claim = task completed` | The MVP only tests completion proof compatibility. |
| fixed string | `evidence_type = receipt` | This sample represents a receipt-style completion proof. |

## Validation result normalization

The converter normalizes common outcome words:

```txt
success / succeeded / passed / pass / completed -> passed
failure / failed / fail / error -> failed
pending / attempted / submitted -> pending
anything else -> unknown
```

## What this does not prove

This mapping does not prove:

- the cryptographic validity of the receipt,
- the correctness of the real upstream schema,
- the legitimacy of the authority transition,
- whether the outcome was desirable or in scope.

It only tests whether a receipt-style proof can be read through a shared CCPP v0 structure.

## Day 6 usage question this mapping supports

When sent back to a receipt/harness builder, the important question is not:

> Is this concept correct?

The important question is:

> If another evaluator, workflow, or agent market had to consume your receipt, what field would be missing from this profile?
