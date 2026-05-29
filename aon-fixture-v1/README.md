# AoN Completion Proof Boundary — v1 Fixture

**Principle:** Completed is not a claim. Completed is a state supported by target-system evidence.

This fixture tests the smallest useful boundary in agent completion proof:

1. **Narrative only**  
   The agent says the task is done, but there is no observed execution and no target-system receipt.  
   Expected result: `agent_reported_only`, completion denied.

2. **Execution without receipt**  
   The agent attempts or submits the task, but no durable receipt or confirmation returns from the target system.  
   Expected result: `execution_attempted_no_receipt`, completion denied.

3. **Submitted with receipt**  
   The agent submits the task and the target system returns a durable receipt with `proof_origin=target_system` and `validation.status=passed`.  
   Expected result: `submitted_with_receipt`, completion allowed.

## Test rule

```txt
completed requires target-system evidence
```

In this v1 fixture, completion is allowed only when all three are true:

```txt
receipt_returned == true
proof_origin == "target_system"
validation.status == "passed"
```

## Files

```txt
aon-fixture-v1/
  cases/
    case_1_narrative_only.json
    case_2_execution_no_receipt.json
    case_3_submitted_with_receipt.json
  expected_results.json
  evaluate.py
  README.md
```

## Run

```bash
python3 evaluate.py
```

Expected output:

```txt
case_1_narrative_only -> PASS: agent_reported_only (completion denied)
case_2_execution_no_receipt -> PASS: execution_attempted_no_receipt (completion denied)
case_3_submitted_with_receipt -> PASS: submitted_with_receipt (completion allowed)

all_passed=True
```

## Explicitly out of scope for v1

The following are intentionally excluded from v1:

- authority-continuity check
- platform/dashboard
- broad standard/spec
- marketplace mechanics
- proof level taxonomy

Authority continuity is a likely v2 layer: a target-system receipt proves completion, while authority continuity helps prove legitimacy.
