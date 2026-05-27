#!/usr/bin/env python3
"""
Mini Evidence Agent — bundle-path receipt baseline

Purpose:
  Control baseline for The Agents of Nations.
  This version starts from the single-file bundle and attempts a real POST
  to the machine-readable receipt endpoint.

Flow:
  /agent-test-bundle.json -> payload preparation -> /api/submit -> receipt check

Outputs:
  ./mini_agent_output/run_log.json
  ./mini_agent_output/payload.json
  ./mini_agent_output/summary.md
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict
from urllib import error, request


BUNDLE_URL = "https://the-agents-of-nations.vercel.app/agent-test-bundle.json"

OUTPUT_DIR = Path("mini_agent_output")
RUN_LOG_PATH = OUTPUT_DIR / "run_log.json"
PAYLOAD_PATH = OUTPUT_DIR / "payload.json"
SUMMARY_PATH = OUTPUT_DIR / "summary.md"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def http_get_json(url: str) -> Dict[str, Any]:
    req = request.Request(
        url,
        method="GET",
        headers={
            "User-Agent": "mini-evidence-agent/0.2",
            "Accept": "application/json",
        },
    )

    with request.urlopen(req, timeout=20) as response:
        raw = response.read().decode("utf-8")
        return {
            "ok": True,
            "status_code": response.status,
            "content_type": response.headers.get("content-type"),
            "json": json.loads(raw),
            "raw": raw,
        }


def http_post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")

    req = request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "User-Agent": "mini-evidence-agent/0.2",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    with request.urlopen(req, timeout=20) as response:
        raw = response.read().decode("utf-8")
        return {
            "ok": True,
            "status_code": response.status,
            "content_type": response.headers.get("content-type"),
            "json": json.loads(raw),
            "raw": raw,
        }


def to_error(stage: str, exc: Exception) -> Dict[str, Any]:
    if isinstance(exc, error.HTTPError):
        try:
            body = exc.read().decode("utf-8")
        except Exception:
            body = ""
        return {
            "stage": stage,
            "ok": False,
            "error_type": "HTTPError",
            "status_code": exc.code,
            "reason": exc.reason,
            "body": body,
        }

    if isinstance(exc, error.URLError):
        return {
            "stage": stage,
            "ok": False,
            "error_type": "URLError",
            "reason": str(exc.reason),
        }

    return {
        "stage": stage,
        "ok": False,
        "error_type": type(exc).__name__,
        "reason": str(exc),
    }


def write_outputs(run: Dict[str, Any], payload: Dict[str, Any] | None) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    RUN_LOG_PATH.write_text(json.dumps(run, indent=2, ensure_ascii=False), encoding="utf-8")

    if payload is not None:
        PAYLOAD_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    else:
        PAYLOAD_PATH.write_text(
            json.dumps(
                {
                    "payload_prepared": False,
                    "first_evidence_chain_break": run.get("first_evidence_chain_break"),
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    summary = f"""# Mini Evidence Agent Bundle Receipt Run

Started at: {run.get("started_at")}
Finished at: {run.get("finished_at")}

## Result

- Bundle fetched: {bool(run.get("files_fetched"))}
- Selected task_id: {run.get("selected_task_id")}
- Payload prepared: {run.get("payload_prepared")}
- Did submit: {run.get("did_submit")}
- Receipt returned: {run.get("receipt_returned")}
- receipt_id: {run.get("receipt_id")}
- proof_origin: {run.get("proof_origin")}
- validation.status: {run.get("validation_status")}
- final_submission_status: {run.get("final_submission_status")}
- completion_judgement: {run.get("completion_judgement")}

## First evidence-chain break

```json
{json.dumps(run.get("first_evidence_chain_break"), indent=2, ensure_ascii=False)}
```
"""
    SUMMARY_PATH.write_text(summary, encoding="utf-8")


def main() -> int:
    run: Dict[str, Any] = {
        "agent_name": "mini-evidence-agent",
        "framework": "python-urllib",
        "started_at": now_iso(),
        "bundle_url": BUNDLE_URL,
        "files_fetched": [],
        "selected_task_id": None,
        "payload_prepared": False,
        "did_submit": False,
        "receipt_returned": False,
        "receipt_id": None,
        "proof_origin": None,
        "validation_status": None,
        "final_submission_status": "safe_stopped",
        "completion_judgement": "FAIL_OR_PARTIAL",
        "first_evidence_chain_break": None,
        "events": [],
    }

    payload: Dict[str, Any] | None = None

    try:
        bundle_response = http_get_json(BUNDLE_URL)
        bundle = bundle_response["json"]
        run["files_fetched"].append(BUNDLE_URL)
        run["events"].append(
            {
                "ts": now_iso(),
                "event": "bundle_fetched",
                "url": BUNDLE_URL,
                "status_code": bundle_response["status_code"],
                "content_type": bundle_response["content_type"],
            }
        )
    except Exception as exc:
        err = to_error("bundle_fetch", exc)
        run["first_evidence_chain_break"] = err
        run["events"].append(err)
        run["finished_at"] = now_iso()
        write_outputs(run, payload)
        print(json.dumps(run, indent=2, ensure_ascii=False))
        return 1

    selected_task = bundle.get("selected_test_task") or {}
    task_id = selected_task.get("task_id")
    output_format = selected_task.get("output_format", "structured_markdown")

    if not task_id:
        err = {
            "stage": "task_selection",
            "ok": False,
            "error": "selected_test_task.task_id missing from bundle",
        }
        run["first_evidence_chain_break"] = err
        run["events"].append(err)
        run["finished_at"] = now_iso()
        write_outputs(run, payload)
        print(json.dumps(run, indent=2, ensure_ascii=False))
        return 1

    run["selected_task_id"] = task_id
    run["events"].append(
        {
            "ts": now_iso(),
            "event": "task_selected",
            "task_id": task_id,
        }
    )

    endpoint = bundle.get("machine_readable_receipt_endpoint") or {}
    submit_url = endpoint.get("url")
    submit_method = endpoint.get("method")

    if not submit_url or submit_method != "POST":
        err = {
            "stage": "receipt_endpoint_read",
            "ok": False,
            "error": "missing valid POST receipt endpoint",
            "endpoint": endpoint,
        }
        run["first_evidence_chain_break"] = err
        run["events"].append(err)
        run["finished_at"] = now_iso()
        write_outputs(run, payload)
        print(json.dumps(run, indent=2, ensure_ascii=False))
        return 1

    payload = {
        "agent_name": "mini-evidence-agent",
        "operator": "human-supervised-local-run",
        "framework": "python-urllib",
        "task_id": task_id,
        "capabilities_used": [
            "web_fetch",
            "schema_following",
            "payload_preparation",
            "http_post",
        ],
        "output_format": output_format,
        "output": (
            "Mini Evidence Agent read the single-file agent test bundle, "
            "selected the listed task, prepared a schema-compatible payload, "
            "and submitted it to the machine-readable receipt endpoint. "
            "Completion is claimed only because the endpoint returned a receipt."
        ),
        "sources": [BUNDLE_URL],
        "confidence": 0.95,
        "notes": (
            "Control baseline run from an environment with direct HTTP GET and POST capability. "
            "This distinguishes arena/receipt failures from black-box chatbot runtime POST limitations."
        ),
    }

    run["payload_prepared"] = True
    run["events"].append(
        {
            "ts": now_iso(),
            "event": "payload_prepared",
            "task_id": task_id,
        }
    )

    try:
        post_response = http_post_json(submit_url, payload)
        receipt = post_response["json"]

        run["did_submit"] = True
        run["receipt_returned"] = True
        run["receipt_id"] = receipt.get("receipt_id")
        run["proof_origin"] = receipt.get("proof_origin")
        run["validation_status"] = (receipt.get("validation") or {}).get("status")
        run["final_submission_status"] = receipt.get("submission_status", "unknown")

        run["events"].append(
            {
                "ts": now_iso(),
                "event": "payload_submitted",
                "url": submit_url,
                "status_code": post_response["status_code"],
                "receipt": receipt,
            }
        )

    except Exception as exc:
        err = to_error("payload_submit", exc)
        run["did_submit"] = True
        run["receipt_returned"] = False
        run["final_submission_status"] = "submission_attempted_no_receipt"
        run["first_evidence_chain_break"] = err
        run["events"].append(err)

    valid_completion = (
        run["receipt_returned"] is True
        and bool(run["receipt_id"])
        and run["proof_origin"] in ["target_system", "public_durable_record"]
        and run["validation_status"] == "passed"
        and run["final_submission_status"] == "submitted_with_receipt"
    )

    run["completion_judgement"] = "PASS" if valid_completion else "FAIL_OR_PARTIAL"
    run["finished_at"] = now_iso()

    write_outputs(run, payload)
    print(json.dumps(run, indent=2, ensure_ascii=False))
    return 0 if valid_completion else 2


if __name__ == "__main__":
    raise SystemExit(main())
