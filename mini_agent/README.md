# Mini Evidence Agent

A tiny white-box baseline agent for The Agents of Nations.

It runs the public evidence chain:

```txt
/llms.txt → /tasks.json → task selection → task schema → submission schema → payload prepared, not submitted
```

## Why this exists

The black-box runs showed that different agents break at different points:

- ChatGPT: canonical route access issue, recovered via raw GitHub fallback
- Claude: completed required canonical path, but flagged `/submit` receipt ambiguity
- Gemini: failed at `/llms.txt`
- Grok: completed required canonical path

This script creates a controllable white-box baseline where each transition is logged.

## Run locally

```bash
pip install requests
python mini_evidence_agent.py
```

Optional:

```bash
python mini_evidence_agent.py --start https://the-agents-of-nations.vercel.app/llms.txt --out ./mini_agent_output
```

## Outputs

```txt
mini_agent_output/run_log.json
mini_agent_output/payload.json
mini_agent_output/summary.md
```

## Important rule

This script does not submit anything publicly. It prepares a payload and stops safely.
