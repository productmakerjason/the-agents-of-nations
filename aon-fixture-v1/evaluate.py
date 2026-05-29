#!/usr/bin/env python3
"""
AoN Completion Proof Boundary v1 evaluator.

Rule:
completed requires target-system evidence.

A case can be marked completion_allowed=true only when:
- receipt_returned is true
- proof_origin == "target_system"
- validation.status == "passed"

Everything else remains non-completed, even if the agent self-reports success.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).resolve().parent
CASES_DIR = ROOT / "cases"


def evaluate_case(case: Dict[str, Any]) -> Dict[str, Any]:
    receipt_returned = case.get("receipt_returned") is True
    proof_origin_ok = case.get("proof_origin") == "target_system"
    validation_ok = case.get("validation", {}).get("status") == "passed"

    completion_allowed = receipt_returned and proof_origin_ok and validation_ok

    if completion_allowed:
        observed_state = "submitted_with_receipt"
    elif case.get("post_attempted") or case.get("tool_call_observed"):
        observed_state = "execution_attempted_no_receipt"
    elif case.get("agent_self_reported"):
        observed_state = "agent_reported_only"
    else:
        observed_state = "no_completion_evidence"

    return {
        "case_id": case.get("case_id"),
        "observed_state": observed_state,
        "completion_allowed": completion_allowed,
        "expected_state": case.get("expected_state"),
        "expected_completion_allowed": case.get("completion_allowed"),
        "passed": (
            observed_state == case.get("expected_state")
            and completion_allowed == case.get("completion_allowed")
        ),
    }


def main() -> None:
    results = []
    for path in sorted(CASES_DIR.glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        result = evaluate_case(case)
        results.append(result)

    report = {
        "fixture_name": "aon_completion_proof_boundary_v1",
        "rule": "completed_requires_target_system_evidence",
        "results": results,
        "all_passed": all(r["passed"] for r in results),
    }

    output_path = ROOT / "run_results.json"
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        allowed = "completion allowed" if r["completion_allowed"] else "completion denied"
        print(f"{r['case_id']} -> {status}: {r['observed_state']} ({allowed})")

    print(f"\nall_passed={report['all_passed']}")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
