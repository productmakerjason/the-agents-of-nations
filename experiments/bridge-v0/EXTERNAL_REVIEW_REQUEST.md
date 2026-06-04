# External Review Request — The Bridge v0

## What this is

The Bridge v0 is a small compatibility experiment for agent completion proof.

It maps two representative completion-proof artifacts into the same minimal profile:

```txt
msaleme-like attested receipt        -> CCPP v0
Mycelium-like git Resolution Note    -> CCPP v0
```

This is not a standard.

This is not an official adapter for either project.

The samples are representative examples based on publicly described proof models.

## Why I made this

The problem I am testing is not whether agents should provide evidence.

That part seems increasingly clear:

```txt
agent-reported completion != verified completion
```

The next question is interoperability:

```txt
If one system produces completion proof,
can another evaluator, workflow, or agent market consume it?
```

If every workflow, harness, or agent system creates its own local proof format, completion evidence may remain trapped inside local systems.

That becomes a problem if agent work is meant to support:

- task handoff,
- external evaluation,
- reputation,
- payment,
- dispute resolution,
- or market-level trust.

## What the demo shows

The demo converts two different local proof shapes into the same CCPP v0 structure.

Run:

```bash
python3 bridge.py --all
```

Expected result:

```txt
[msaleme-like receipt] -> CCPP v0: passed
[mycelium-like note]   -> CCPP v0: passed
```

Saved output:

```txt
demo-output.txt
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

## What I am asking you to review

I am not asking whether this is a complete standard.

I am asking three narrow questions:

1. Is this mapping directionally correct?
2. If another system had to consume your proof, what field would be missing?
3. Have you actually needed cross-system proof consumption, or is local proof enough?

## What would count as useful feedback

Useful feedback would be something like:

```txt
This field is wrong.
This field is missing.
This should be split into two fields.
Our proof would need X to be consumed externally.
Local proof is enough; cross-system proof is not a real problem for us.
We have needed this when moving between harnesses/workflows/evaluators.
```

## What this MVP does not do

It does not verify cryptographic signatures.

It does not define a universal receipt standard.

It does not decide authority or outcome legitimacy.

It does not prove that CCPP v0 is the right long-term format.

It only tests whether local completion-proof artifacts can be translated into a shared minimal profile that another system could inspect.
