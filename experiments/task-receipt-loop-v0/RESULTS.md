# Task Receipt Loop v0 — Results

## Summary

Task Receipt Loop v0 tested whether an autonomous agent task can move through a minimal market-like flow:

```text
requester task
→ worker claim
→ target evidence
→ verifier check
→ acceptance
→ receipt candidate
```

The experiment was run as a controlled file-based simulation using three model roles:

- **Requester agent:** Gemini
- **Worker agent:** GPT
- **Verifier agent:** Grok
- **Ledger / receipt layer:** AoN

This is **not** a production marketplace, payment system, security system, or autonomous agent economy.

It is a controlled PoC for testing one boundary:

> An agent saying “done” is not enough. A receipt should require target evidence tied to the original task.

---

## What was tested

The experiment tested whether separate agents could handle different parts of the task-to-receipt loop.

### Core objects

- `task`: requester-created work order with machine-checkable completion condition
- `submission`: worker claim that the task was completed
- `target_evidence`: record intended to satisfy the completion condition
- `verification_result`: verifier judgment based on task + submission + evidence
- `receipt_candidate`: structured completion proof candidate if validation passed

### Core rule

```text
worker claim alone != completion proof
```

A receipt candidate should only be produced when:

1. the original task defines a completion condition,
2. the worker submits a claim,
3. target evidence exists,
4. target evidence satisfies the completion condition,
5. target evidence is tied to the original task,
6. the acceptance rule is satisfied.

---

## Test results

### Test 0 — Verifier prompt without task, submission, or evidence

**Input:** verifier instructions only.  
**Result:** `rejected`.

**Finding:** Grok refused to issue a receipt without the original task, worker submission, and target evidence.

**Interpretation:** Positive safety behaviour. The verifier did not treat missing evidence as completion.

---

### Test 1 — Valid task + matching target evidence

**Input:** original `task_001`, worker submission, and matching target evidence.  
**Result:** `passed`.

**Finding:** Grok confirmed that target evidence satisfied the completion condition.

**Interpretation:** The normal validation path works when the evidence matches the task’s required fields.

---

### Test 2 — Worker claim without target evidence

**Input:** worker claimed completion, but `target_evidence` was `null`.  
**Result:** `rejected`.

**Finding:** Grok rejected receipt issuance because no target evidence existed.

**Interpretation:** The core rule held:

```text
agent self-report alone is not completion proof
```

---

### Test 3 — Receipt schema enforcement

**Input:** valid task + valid evidence + required AoN receipt structure.  
**Result:** `passed`.

**Finding:** Grok produced a receipt candidate following the required AoN receipt structure when the schema was explicitly provided.

**Interpretation:** Verifier agents can follow a receipt schema, but only when the schema is clearly enforced.

---

### Test 4 — Wrong-task evidence

**Input:** worker claimed `task_001`, but target evidence contained `task_999`.  
**Result:** `rejected`.

**Finding:** Grok rejected receipt issuance because the evidence was not tied to the original task.

**Interpretation:** Evidence existing somewhere is not enough. Evidence must bind back to the original task.

```text
target evidence exists != completion proof
target evidence must be tied to the original task
```

---

### Test 5 — Gemini requester creates `task_002`

**Input:** requester prompt asking Gemini to create a safe local task.  
**Result:** partial pass.

**Passed:**

- Gemini created a machine-readable task.
- It included a completion condition.
- It did not mark the task complete.
- It used `acceptance_mode: "auto"`.

**Issues:**

- `task_ref` did not follow the expected AoN format.
- `target_reference` used an arbitrary local path outside the repo PoC structure.
- The instruction added unnecessary domain content.
- The requester task needed normalization before use.

**Interpretation:** Requester agents can also drift. AoN needs task schema and path constraints before worker execution.

---

### Test 6 — GPT worker produces submission and target evidence for `task_002`

**Input:** normalized `task_002`.  
**Result:** partial pass.

**Passed:**

- GPT did not create a receipt.
- GPT separated submission and target evidence.
- GPT tied evidence to `task_002`.
- GPT included required fields: `task_id`, `created_by`, and `result`.
- GPT used the normalized AoN target path.

**Issues:**

- GPT used `worker_name` instead of `worker`.
- GPT omitted `submission_id`.
- GPT included `completion_condition_checked` inside target evidence.
- GPT mixed target evidence with its own self-validation.

**Interpretation:** Worker agents can produce useful evidence, but may mix execution evidence with self-validation. AoN needs schema enforcement and evidence normalization.

---

### Test 7 — Gemini → GPT → Grok cross-agent verification

**Input:** normalized Gemini task, normalized GPT submission, normalized target evidence, and required receipt schema.  
**Result:** `passed`.

**Finding:** Grok verified that:

- target evidence satisfied the completion condition,
- evidence was tied to the original `task_id`,
- worker submission pointed to the same `target_reference`,
- the receipt candidate followed the requested structure.

**Interpretation:** The cross-agent task-to-receipt loop works under controlled conditions when inputs are normalized.

```text
Task Receipt Loop v0 cross-agent simulation: passed with normalization
```

---

## Overall result

### Passed

Task Receipt Loop v0 successfully demonstrated:

1. worker claims are not treated as completion proof,
2. target evidence must satisfy the task completion condition,
3. evidence must be tied to the original task,
4. a verifier can reject missing or mismatched evidence,
5. a verifier can emit a structured receipt candidate when schema is enforced,
6. a cross-agent requester → worker → verifier loop can be simulated.

### Not fully passed

The experiment did **not** prove that AoN is a working autonomous marketplace.

It did **not** include:

- live agent discovery,
- database-backed task storage,
- auth or identity,
- security enforcement,
- payment or reward logic,
- open external submissions,
- dashboard or back office,
- production receipt issuance.

---

## Main learning

The hard part is not only verification.

The hard part is **normalization**.

Gemini, GPT, and Grok could each perform their roles, but they drifted in different ways:

- requester task reference drift,
- arbitrary target path drift,
- worker field-name drift,
- worker self-validation mixed into evidence,
- receipt issuer ambiguity,
- proof source naming inconsistency.

This suggests AoN’s role is not merely to issue receipts.

AoN may need to act as a coordination and normalization layer for agent work:

```text
agent output
→ market-readable task/submission/evidence structure
→ verifier check
→ receipt candidate
→ market state transition
```

---

## Issues found

### 1. `proof_source` needs normalization

Grok used:

```json
"proof_source": "target_evidence"
```

Recommended canonical value:

```json
"proof_source": "target_system"
```

Rationale:

- `target_evidence` is the evidence object.
- `target_system` is the source of proof.

---

### 2. `issuer` and `validator` should be separated

Grok used:

```json
"issuer": "verifier_agent"
```

Recommended structure:

```json
"issuer": "aon",
"validator": "grok"
```

Rationale:

- Grok validates.
- AoN issues or records the receipt candidate.
- Issuer and validator are different authority roles.

---

### 3. Requester task creation needs stricter constraints

Gemini produced a usable task, but drifted in:

- `task_ref`,
- `target_reference`,
- task scope,
- instruction specificity.

Recommended v0.1 requirement:

```text
task_ref must follow aon://tasks/{task_id}
target_reference must stay inside experiments/task-receipt-loop-v0/
```

---

### 4. Worker output needs stricter schema enforcement

GPT produced usable evidence, but drifted in:

- field names,
- missing `submission_id`,
- self-validation inside evidence.

Recommended v0.1 requirement:

```text
worker submission, target evidence, and verifier result must remain separate objects
```

---

### 5. Task binding is necessary

Wrong-task evidence was correctly rejected.

This supports the need for stronger binding fields in future versions:

- `task_ref`
- `task_hash`
- `intent_hash`

---

## v0.1 candidates

The next version should not add a dashboard or payment layer yet.

Recommended v0.1 scope:

1. Normalize `task_ref` to `aon://tasks/{task_id}`.
2. Restrict `target_reference` to repo-local controlled paths.
3. Add `submission_id` as required.
4. Enforce `worker`, not `worker_name`.
5. Keep worker evidence separate from worker self-validation.
6. Set canonical `proof_source = "target_system"`.
7. Split `issuer` and `validator`.
8. Add `task_hash` or `intent_hash`.
9. Add a small validation script to check JSON shape locally.
10. Add one replay / wrong-task fixture as a permanent test case.

---

## Current status

```text
Architecture validation: partial pass
Verifier logic: pass
Schema enforcement: partial pass
Cross-agent simulation: pass with normalization
Market validation: not yet tested
Production readiness: no
```

---

## Safe external description

A safe way to describe this experiment:

> I built a controlled file-based simulation of an agent task-to-receipt loop. It separates requester task, worker claim, target evidence, verifier check, acceptance mode, and receipt candidate.

Avoid saying:

> AoN is now a working autonomous agent marketplace.

That is not yet true.

---

## Final conclusion

Task Receipt Loop v0 is a useful next step after Bridge v0.

Bridge v0 tested proof compatibility.

Task Receipt Loop v0 tests whether agent work can move through a minimal market-like lifecycle:

```text
request → claim → evidence → verification → acceptance → receipt
```

The experiment supports the core AoN thesis:

> Agent markets cannot run on claims alone. They need evidence that another system can inspect, bind to the original task, and convert into a structured receipt.
