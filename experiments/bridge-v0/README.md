# The Bridge v0

A 7-day MVP for testing completion-proof compatibility.

The Bridge v0 maps publicly described agent completion-proof models into a minimal Common Completion Proof Profile (CCPP v0), so different systems can inspect completion evidence in a shared structure.

This is not a standard and not an official adapter.

These samples are representative samples based on publicly described proof models, not official schemas.

## Why this exists

Agent workflows increasingly produce local completion proof:

- attested receipts
- git ledger notes
- API responses
- database updates
- webhook confirmations
- evaluator verdicts

The question is not only whether a task was completed locally.

The market question is:

Can another evaluator, workflow, or future agent market consume that proof?

## MVP scope

This MVP only does one thing:

```txt
two different proof samples -> CCPP v0
```

Included inputs:

```txt
samples/msaleme-like-receipt.json
samples/mycelium-like-resolution-note.json
```

Included output profile:

```txt
ccpp-v0.schema.json
```

Run:

```bash
python bridge.py --all
```

Expected result:

```txt
[msaleme-like receipt] -> CCPP v0: passed
[mycelium-like note]   -> CCPP v0: passed
```

## CCPP v0 fields

```json
{
  "claim": "task completed",
  "task_id": "...",
  "evidence_type": "receipt | git_artifact",
  "proof_source": "durable_record | target_system | evaluator | agent_self_reported",
  "target_reference": "...",
  "validation_result": "passed | failed | pending | unknown",
  "timestamp": "...",
  "issuer": "..."
}
```

## Day 6 validation questions

When sending this MVP to external respondents, do not ask: “Is this concept right?”

Ask:

1. Is this mapping directionally correct?
2. If another system had to consume your proof, what field would be missing?
3. Have you actually needed cross-system proof consumption, or is local proof enough?

## Day 7 decision rule

Go:

```txt
Layer 1 all passed + usage-intent 2+ + compatibility-not-needed <= 1
```

Narrow Go:

```txt
Layer 1 all passed + usage-intent 1
```

Pause:

```txt
Layer 1 passed + usage-intent 0 + compatibility-not-needed 0-1
```

Pivot:

```txt
usage-intent 0 + compatibility-not-needed 2+
```

Fail:

```txt
Layer 1 not passed
```
## Day 2: msaleme-like mapping rule

The first mapping target is the representative `msaleme-like-receipt.json` sample.

The mapping is documented here:

```txt
docs/msaleme-like-mapping.md
```

Core mapping:

```txt
msaleme.task_hash          -> ccpp.task_id
msaleme.receipt_id         -> ccpp.target_reference
msaleme.actual_outcome     -> ccpp.validation_result
msaleme.timestamp          -> ccpp.timestamp
msaleme.attestation.evaluator -> ccpp.issuer
msaleme.attestation exists -> ccpp.proof_source = durable_record
```

This mapping is intentionally minimal. It tests whether a receipt-style proof can be inspected through CCPP v0, not whether this is a complete or official receipt schema.
## Day 3: Mycelium-like mapping rule

The second mapping target is the representative `mycelium-like-resolution-note.json` sample.

The mapping is documented here:

```txt
docs/mycelium-like-mapping.md
```

Core mapping:

```txt
mycelium.commit_ref                  -> ccpp.task_id
mycelium.execution_receipt           -> ccpp.target_reference
mycelium.output_hash                 -> ccpp.target_reference fallback
mycelium.signature exists            -> ccpp.proof_source = durable_record
mycelium.signature + receipt exist   -> ccpp.validation_result = passed
missing signature or receipt         -> ccpp.validation_result = unknown
```

This mapping is intentionally minimal. It tests whether a git-ledger-style proof artifact can be inspected through CCPP v0, not whether this is a complete or official Resolution Note schema.
## Demo output

A saved terminal output is included here:

```txt
demo-output.txt
```

Run locally:

```bash
python3 bridge.py --all
```

The demo shows two different representative completion-proof artifacts being converted into the same CCPP v0 structure:

```txt
msaleme-like attested receipt -> CCPP v0
Mycelium-like Resolution Note -> CCPP v0
```

The important point is not that CCPP v0 is a standard.

The important point is that two different local completion-proof artifacts can be inspected through the same minimal profile.

This supports the Day 6 validation question:

> If another evaluator, workflow, or agent market had to consume your completion proof, what field would be missing from this profile?
## External review request

A short external review note is available here:

```txt
EXTERNAL_REVIEW_REQUEST.md
```

This file is intended for Day 6 outreach.

The review question is intentionally narrow:

```txt
If another evaluator, workflow, or agent market had to consume your completion proof, what field would be missing from CCPP v0?
```

The goal is not to validate a taxonomy.

The goal is to test whether completion proof needs a portable compatibility layer.
