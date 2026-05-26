#!/usr/bin/env python3
"""
Mini Evidence-Chain Agent for The Agents of Nations

Purpose:
  White-box baseline agent that follows a public task-flow and logs every transition:
  /llms.txt -> /tasks.json -> task selection -> schemas -> payload preparation.

What it does NOT do:
  - It does not submit publicly.
  - It does not claim submission.
  - It does not invent task IDs if tasks.json cannot be fetched.

Outputs:
  ./mini_agent_output/run_log.json
  ./mini_agent_output/payload.json
  ./mini_agent_output/summary.md

Run:
  python mini_evidence_agent.py

Optional:
  python mini_evidence_agent.py --start https://the-agents-of-nations.vercel.app/llms.txt
  python mini_evidence_agent.py --out ./my_run_output
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin

try:
    import requests
except ImportError as exc:
    raise SystemExit("Missing dependency: requests. Install with: pip install requests") from exc

DEFAULT_START_URL = "https://the-agents-of-nations.vercel.app/llms.txt"
DEFAULT_BASE = "https://the-agents-of-nations.vercel.app"
CANONICAL_ROUTES = {
    "tasks": "/tasks.json",
    "task_schema": "/task-schema.md",
    "submission_schema": "/submission-schema.md",
    "submit": "/submit",
}
RAW_FALLBACKS = {
    "tasks": "https://raw.githubusercontent.com/productmakerjason/the-agents-of-nations/main/public/tasks.json",
    "task_schema": "https://raw.githubusercontent.com/productmakerjason/the-agents-of-nations/main/public/task-schema.md",
    "submission_schema": "https://raw.githubusercontent.com/productmakerjason/the-agents-of-nations/main/public/submission-schema.md",
}


@dataclass
class FetchResult:
    label: str
    url: str
    ok: bool
    status_code: Optional[int]
    content_type: Optional[str]
    content_length: int
    error: Optional[str]
    elapsed_ms: int


class EvidenceChainAgent:
    def __init__(self, start_url: str, out_dir: Path, timeout: int = 20) -> None:
        self.start_url = start_url
        self.base_url = self._base_from_start(start_url)
        self.out_dir = out_dir
        self.timeout = timeout
        self.events: List[Dict[str, Any]] = []
        self.fetches: List[FetchResult] = []
        self.sources: List[str] = []
        self.first_break: Optional[str] = None
        self.payload: Optional[Dict[str, Any]] = None

    @staticmethod
    def _base_from_start(start_url: str) -> str:
        if "/llms.txt" in start_url:
            return start_url.split("/llms.txt", 1)[0]
        return DEFAULT_BASE

    def event(self, event_type: str, detail: Dict[str, Any]) -> None:
        record = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event": event_type,
            **detail,
        }
        self.events.append(record)
        print(f"[{event_type}] {json.dumps(detail, ensure_ascii=False)}")

    def fetch(self, label: str, url: str) -> Tuple[Optional[str], FetchResult]:
        started = time.time()
        try:
            resp = requests.get(
                url,
                timeout=self.timeout,
                headers={
                    "User-Agent": "mini-evidence-agent/0.1 (+https://the-agents-of-nations.vercel.app)",
                    "Accept": "text/plain, application/json, text/markdown, */*",
                },
            )
            elapsed_ms = int((time.time() - started) * 1000)
            text = resp.text if resp.ok else None
            result = FetchResult(
                label=label,
                url=url,
                ok=resp.ok,
                status_code=resp.status_code,
                content_type=resp.headers.get("content-type"),
                content_length=len(resp.content or b""),
                error=None if resp.ok else f"HTTP {resp.status_code}",
                elapsed_ms=elapsed_ms,
            )
            self.fetches.append(result)
            self.event("fetch", asdict(result))
            if resp.ok:
                self.sources.append(url)
            return text, result
        except Exception as exc:  # noqa: BLE001
            elapsed_ms = int((time.time() - started) * 1000)
            result = FetchResult(
                label=label,
                url=url,
                ok=False,
                status_code=None,
                content_type=None,
                content_length=0,
                error=repr(exc),
                elapsed_ms=elapsed_ms,
            )
            self.fetches.append(result)
            self.event("fetch", asdict(result))
            return None, result

    def fetch_with_fallback(self, label: str, canonical_url: str, fallback_url: Optional[str]) -> Tuple[Optional[str], str, FetchResult]:
        text, result = self.fetch(label, canonical_url)
        if text is not None:
            return text, canonical_url, result
        if fallback_url:
            self.event("fallback_attempt", {"label": label, "canonical_url": canonical_url, "fallback_url": fallback_url})
            text, result = self.fetch(f"{label}_fallback", fallback_url)
            if text is not None:
                return text, fallback_url, result
        if self.first_break is None:
            self.first_break = f"Failed to fetch {label}: {canonical_url}"
        return None, canonical_url, result

    @staticmethod
    def extract_urls(text: str) -> List[str]:
        return re.findall(r"https?://[^\s)>'\"]+", text or "")

    def select_task(self, tasks: Any) -> Optional[Dict[str, Any]]:
        if isinstance(tasks, dict):
            task_list = tasks.get("tasks") or tasks.get("items") or tasks.get("data")
        else:
            task_list = tasks
        if not isinstance(task_list, list) or not task_list:
            if self.first_break is None:
                self.first_break = "tasks.json did not contain a non-empty task list"
            return None

        # Prefer the discovery task because it is directly aligned with this arena test.
        for task in task_list:
            if isinstance(task, dict) and task.get("task_id") == "agent_discovery_001":
                return task
        for task in task_list:
            if isinstance(task, dict) and task.get("task_id"):
                return task
        if self.first_break is None:
            self.first_break = "No task object with task_id found in task feed"
        return None

    def prepare_payload(self, task: Dict[str, Any], task_schema_url: str, submission_schema_url: str) -> Dict[str, Any]:
        task_id = task.get("task_id")
        title = task.get("title", "Untitled task")
        payload = {
            "agent_name": "mini-evidence-agent",
            "operator": "local human operator",
            "framework": "custom Python script",
            "task_id": task_id,
            "output_format": task.get("output_format", "structured_markdown"),
            "output": (
                f"# Mini Evidence Agent Run\n\n"
                f"Selected task: `{task_id}` — {title}\n\n"
                f"The agent fetched the start file, task feed, and schemas, then prepared this payload without submitting it.\n\n"
                f"First evidence-chain break: {self.first_break or 'None within required path'}\n"
            ),
            "confidence": 0.82 if self.first_break else 0.92,
            "capabilities_used": ["http_fetch", "json_parse", "schema_reading", "payload_preparation", "safe_stop"],
            "sources": self.sources,
            "method_summary": "Fetched public files in sequence, selected a real task_id from tasks.json, read schemas, prepared payload, and stopped before submission.",
            "assumptions": [
                "No public submission should be claimed without a GitHub Issue or confirmed receipt.",
                "Fallback routes, if used, must be logged as fallback routes rather than canonical success.",
            ],
            "limitations": [
                "This script does not perform public submission.",
                "This script validates file retrieval and payload preparation, not paid reward settlement or identity verification.",
            ],
            "notes": "Prepared only. No public GitHub Issue or confirmed submission receipt exists.",
            "submission_status": "prepared_not_submitted",
            "evidence_chain": {
                "start_file_fetched": any(f.label == "start_file" and f.ok for f in self.fetches),
                "task_feed_fetched": any("tasks" in f.label and f.ok for f in self.fetches),
                "real_task_id_selected": bool(task_id),
                "task_schema_read": any("task_schema" in f.label and f.ok for f in self.fetches),
                "submission_schema_read": any("submission_schema" in f.label and f.ok for f in self.fetches),
                "payload_prepared": True,
                "submission_claimed": False,
                "receipt_present": False,
                "safe_stop": True,
                "first_break": self.first_break,
                "task_schema_source": task_schema_url,
                "submission_schema_source": submission_schema_url,
            },
        }
        return payload

    def run(self) -> int:
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.event("run_started", {"start_url": self.start_url})

        start_text, start_fetch = self.fetch("start_file", self.start_url)
        if start_text is None:
            self.first_break = f"Failed to fetch start file: {self.start_url}"
            self.write_outputs(None, None, None)
            return 2

        urls_in_start = self.extract_urls(start_text)
        self.event("start_file_parsed", {"urls_found": urls_in_start[:20], "url_count": len(urls_in_start)})

        tasks_url = urljoin(self.base_url + "/", CANONICAL_ROUTES["tasks"].lstrip("/"))
        task_schema_url = urljoin(self.base_url + "/", CANONICAL_ROUTES["task_schema"].lstrip("/"))
        submission_schema_url = urljoin(self.base_url + "/", CANONICAL_ROUTES["submission_schema"].lstrip("/"))

        tasks_text, tasks_source, _ = self.fetch_with_fallback("tasks", tasks_url, RAW_FALLBACKS["tasks"])
        if tasks_text is None:
            self.write_outputs(None, None, None)
            return 3

        try:
            tasks_json = json.loads(tasks_text)
            self.event("tasks_parsed", {"source": tasks_source})
        except json.JSONDecodeError as exc:
            self.first_break = f"tasks.json fetched but could not be parsed as JSON: {exc}"
            self.event("parse_error", {"label": "tasks", "error": str(exc)})
            self.write_outputs(None, None, None)
            return 4

        task = self.select_task(tasks_json)
        if task is None:
            self.write_outputs(None, tasks_source, None)
            return 5
        self.event("task_selected", {"task_id": task.get("task_id"), "title": task.get("title")})

        task_schema_text, task_schema_source, _ = self.fetch_with_fallback("task_schema", task_schema_url, RAW_FALLBACKS["task_schema"])
        if task_schema_text is None:
            self.write_outputs(task, tasks_source, None)
            return 6

        submission_schema_text, submission_schema_source, _ = self.fetch_with_fallback("submission_schema", submission_schema_url, RAW_FALLBACKS["submission_schema"])
        if submission_schema_text is None:
            self.write_outputs(task, tasks_source, task_schema_source)
            return 7

        self.event("schemas_read", {
            "task_schema_source": task_schema_source,
            "task_schema_chars": len(task_schema_text),
            "submission_schema_source": submission_schema_source,
            "submission_schema_chars": len(submission_schema_text),
        })

        self.payload = self.prepare_payload(task, task_schema_source, submission_schema_source)
        self.event("payload_prepared", {"task_id": task.get("task_id"), "submission_status": "prepared_not_submitted"})
        self.event("safe_stop", {"reason": "No public submission attempted; no receipt exists."})
        self.write_outputs(task, tasks_source, task_schema_source)
        return 0

    def write_outputs(self, task: Optional[Dict[str, Any]], tasks_source: Optional[str], task_schema_source: Optional[str]) -> None:
        run_log = {
            "agent": "mini-evidence-agent",
            "framework": "custom Python script",
            "start_url": self.start_url,
            "first_evidence_chain_break": self.first_break,
            "events": self.events,
            "fetches": [asdict(f) for f in self.fetches],
            "selected_task_id": task.get("task_id") if task else None,
            "submission_status": "prepared_not_submitted",
            "did_submit": False,
        }
        (self.out_dir / "run_log.json").write_text(json.dumps(run_log, indent=2, ensure_ascii=False), encoding="utf-8")
        if self.payload:
            (self.out_dir / "payload.json").write_text(json.dumps(self.payload, indent=2, ensure_ascii=False), encoding="utf-8")
        else:
            (self.out_dir / "payload.json").write_text(json.dumps({"payload_prepared": False, "first_break": self.first_break}, indent=2), encoding="utf-8")

        summary = [
            "# Mini Evidence Agent Run Summary",
            "",
            f"Start URL: {self.start_url}",
            f"Selected task_id: {task.get('task_id') if task else 'None'}",
            f"First evidence-chain break: {self.first_break or 'None within required path'}",
            "Did submit: No",
            "Submission status: prepared_not_submitted",
            "",
            "## Fetches",
        ]
        for f in self.fetches:
            summary.append(f"- {f.label}: {f.url} — ok={f.ok}, status={f.status_code}, error={f.error}")
        summary.extend([
            "",
            "## Output files",
            "- run_log.json",
            "- payload.json",
        ])
        (self.out_dir / "summary.md").write_text("\n".join(summary), encoding="utf-8")
        self.event("outputs_written", {"out_dir": str(self.out_dir)})


def main() -> int:
    parser = argparse.ArgumentParser(description="Mini Evidence-Chain Agent")
    parser.add_argument("--start", default=DEFAULT_START_URL, help="Start URL, default is the arena llms.txt")
    parser.add_argument("--out", default="mini_agent_output", help="Output directory")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout in seconds")
    args = parser.parse_args()

    agent = EvidenceChainAgent(start_url=args.start, out_dir=Path(args.out), timeout=args.timeout)
    return agent.run()


if __name__ == "__main__":
    raise SystemExit(main())
