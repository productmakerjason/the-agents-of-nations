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
