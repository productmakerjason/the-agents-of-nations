# Review Package: task_003

You are the requester/reviewer agent in The Agents of Nations Contextual Proof Object v0.1 experiment.

You will receive:
1. the original requester task
2. the worker submission
3. the AoN contextual proof object

Your job is to decide the requester acceptance state.

Important rules:
- Do not create a receipt.
- Do not mark the full task as completed unless the submitted work fully satisfies the task.
- You may choose one of:
  - accepted
  - accepted_with_limitations
  - needs_revision
  - rejected
- If accepted_with_limitations, define accepted_scope.
- If needs_revision, define required_revision.
- Include explicit non_claims.
- Return only one JSON object.

## ORIGINAL TASK

```json
{
  "task_id": "task_003",
  "task_ref": "aon://tasks/task_003",
  "requester": "gemini",
  "status": "open",
  "task_type": "partial_research_submission",
  "instruction": "Find 3 relevant discussions about agent workflow completion proof. For each item, include source, why it is relevant, and which boundary it relates to.",
  "completion_mode": "requester_acceptance_required",
  "minimum_submission_requirements": {
    "item_count": 3,
    "required_fields_per_item": [
      "source",
      "relevance_reason",
      "boundary"
    ]
  },
  "expected_support_level": "partially_supported",
  "acceptance_mode": "requester_review",
  "non_claims": [
    "source_quality_not_independently_verified",
    "market_demand_not_verified",
    "business_value_not_verified"
  ],
  "created_at": "2026-06-11T00:00:00Z"
}
cat > file <<'EOF'
...
