#!/usr/bin/env python3
"""
The Bridge v0

A tiny compatibility experiment:
- msaleme-like attested receipt -> CCPP v0
- Mycelium-like Resolution Note -> CCPP v0

These are representative samples based on publicly described proof models,
not official schemas.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


ROOT = Path(__file__).parent
SAMPLES = ROOT / "samples"
OUTPUTS = ROOT / "outputs"


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def normalize_validation_result(value: str | None) -> str:
    if not value:
        return "unknown"
    normalized = value.lower().strip()
    if normalized in {"success", "succeeded", "passed", "pass", "completed"}:
        return "passed"
    if normalized in {"failure", "failed", "fail", "error"}:
        return "failed"
    if normalized in {"pending", "attempted", "submitted"}:
        return "pending"
    return "unknown"


def convert_msaleme(receipt: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a representative msaleme-like receipt into CCPP v0."""
    attestation = receipt.get("attestation") or {}
    issuer = attestation.get("evaluator") or "unknown_evaluator"

    return {
        "claim": "task completed",
        "task_id": str(receipt.get("task_hash", "")),
        "evidence_type": "receipt",
        "proof_source": "durable_record" if attestation else "evaluator",
        "target_reference": str(receipt.get("receipt_id", "")),
        "validation_result": normalize_validation_result(receipt.get("actual_outcome")),
        "timestamp": str(receipt.get("timestamp", "")),
        "issuer": str(issuer),
    }


def convert_mycelium(note: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a representative Mycelium-like Resolution Note into CCPP v0."""
    has_signature = bool(note.get("signature"))
    has_receipt = bool(note.get("execution_receipt"))
    validation_result = "passed" if has_signature and has_receipt else "unknown"

    return {
        "claim": "task completed",
        "task_id": str(note.get("commit_ref", "")),
        "evidence_type": "git_artifact",
        "proof_source": "durable_record" if has_signature else "agent_self_reported",
        "target_reference": str(note.get("execution_receipt") or note.get("output_hash") or ""),
        "validation_result": validation_result,
        "timestamp": "unknown",
        "issuer": "mycelium_git_ledger",
    }


def validate_ccpp_minimal(ccpp: Dict[str, Any]) -> tuple[bool, list[str]]:
    required = [
        "claim",
        "task_id",
        "evidence_type",
        "proof_source",
        "target_reference",
        "validation_result",
        "timestamp",
        "issuer",
    ]
    missing = [field for field in required if field not in ccpp]
    return len(missing) == 0, missing


def run_all() -> None:
    msaleme_input = read_json(SAMPLES / "msaleme-like-receipt.json")
    mycelium_input = read_json(SAMPLES / "mycelium-like-resolution-note.json")

    msaleme_output = convert_msaleme(msaleme_input)
    mycelium_output = convert_mycelium(mycelium_input)

    write_json(OUTPUTS / "msaleme-like.ccpp.json", msaleme_output)
    write_json(OUTPUTS / "mycelium-like.ccpp.json", mycelium_output)

    rows = [
        ("msaleme-like receipt", msaleme_output),
        ("mycelium-like note", mycelium_output),
    ]

    print("\nThe Bridge v0 — CCPP conversion results\n")
    for label, output in rows:
        ok, missing = validate_ccpp_minimal(output)
        status = "passed" if ok else f"failed, missing={missing}"
        print(f"[{label}] -> CCPP v0: {status}")

    print("\nGenerated outputs:")
    print(f"- {OUTPUTS / 'msaleme-like.ccpp.json'}")
    print(f"- {OUTPUTS / 'mycelium-like.ccpp.json'}")

    print("\nSide-by-side CCPP v0 fields:")
    fields = [
        "claim",
        "task_id",
        "evidence_type",
        "proof_source",
        "target_reference",
        "validation_result",
        "timestamp",
        "issuer",
    ]

    print(f"{'field':<20} | {'msaleme-like':<32} | {'mycelium-like':<32}")
    print("-" * 92)
    for field in fields:
        left = str(msaleme_output.get(field))
        right = str(mycelium_output.get(field))
        print(f"{field:<20} | {left[:32]:<32} | {right[:32]:<32}")


def main() -> None:
    parser = argparse.ArgumentParser(description="The Bridge v0 CCPP converter")
    parser.add_argument("--all", action="store_true", help="Convert all sample inputs to CCPP v0")
    args = parser.parse_args()

    if args.all:
        run_all()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
