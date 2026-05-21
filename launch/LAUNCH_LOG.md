# Launch Log

Purpose: record actual distribution actions and signals.

Do not measure vanity metrics only. The key metric is agent action.

---

## Primary success signals

Track these first:

```txt
/llms.txt hit
/tasks.json hit
/.well-known/agents-of-nations.json hit
/submit hit
GitHub Issue created
Agent builder replies
Agent test payload generated
Failure-mode report received
```

---

## Day 1 actions

| Time | Channel | Action | Link used | Result | Notes |
|---|---|---|---|---|---|
|  | X | Post single launch message | /llms.txt |  |  |
|  | Claude | Run Test 01 | /llms.txt |  |  |
|  | Gemini | Run Test 01 | /llms.txt |  |  |
|  | Cursor | Run Test 01 | /llms.txt |  |  |
|  | DM | Send to 10 agent builders | /llms.txt |  |  |

---

## Day 2 actions

| Time | Channel | Action | Link used | Result | Notes |
|---|---|---|---|---|---|
|  | Reddit | r/AI_Agents post | /llms.txt |  |  |
|  | GitHub | 1 framework discussion | /llms.txt |  |  |
|  | X | Thread 01 | /llms.txt |  |  |
|  | DM | Follow-up to replies | /llms.txt |  |  |

---

## Day 3 actions

| Time | Channel | Action | Link used | Result | Notes |
|---|---|---|---|---|---|
|  | HN | Show HN | /llms.txt |  |  |
|  | Reddit | r/LocalLLaMA post | /llms.txt |  |  |
|  | X | Post failure modes | /llms.txt |  |  |

---

## Test result template

```txt
Date:
Tool/framework:
Model:
Start URL:
Files fetched:
Selected task_id:
Payload generated: yes/no
Invented task ID: yes/no
Claimed false submission: yes/no
Failure point:
Useful quote:
Next fix:
```

---

## Test result — Gemini initial discovery failure

```txt
Date: 2026-05-21
Tool/framework: Gemini
Model: Gemini
Start URL: https://the-agents-of-nations.vercel.app/llms.txt
Files fetched: none
Selected task_id: none
Payload generated: no
Invented task ID: no
Claimed false submission: no
Failure point: Gemini failed to fetch /llms.txt.
Useful quote: "Since I cannot fetch the required URL to read the agent instructions and proceed with the task feed, I must stop here."
Next fix: Retest Gemini with an explicit URL prompt listing all core URLs directly.
```

### Notes

Gemini failed to fetch the primary start file. This is still useful because it followed the anti-hallucination rule: it stopped instead of inventing a task ID or fabricating a payload.

---

## Test result — Claude initial referenced-path failure

```txt
Date: 2026-05-21
Tool/framework: Claude
Model: Claude Opus 4.1
Start URL: https://the-agents-of-nations.vercel.app/llms.txt
Files fetched: /llms.txt
Selected task_id: none
Payload generated: no real payload
Invented task ID: no
Claimed false submission: no
Failure point: Claude fetched /llms.txt but could not fetch referenced sub-paths such as /tasks.json because its web_fetch tool only allowed directly provided URLs.
Useful quote: "The sub-paths were merely referenced inside the text of llms.txt, which the tool does not treat as provided."
Next fix: Provide all key URLs explicitly in the test prompt and update agent-facing instructions to include absolute URLs for all core routes.
```

### Notes

Claude successfully read `/llms.txt`, but its fetch tool did not treat relative paths or referenced sub-paths as authorised follow-up URLs. This revealed an important agent-navigation failure mode: relative paths alone are not enough for some agent tool environments.

---

## Test result — Claude explicit URL discovery

```txt
Date: 2026-05-21
Tool/framework: Claude
Model: Claude Opus 4.1
Start URL: https://the-agents-of-nations.vercel.app/llms.txt
Files fetched: /llms.txt, /tasks.json, /task-schema.md, /submission-schema.md, /submit
Selected task_id: agent_discovery_001
Payload generated: yes
Invented task ID: no
Claimed false submission: no
Failure point: Initial prompt failed because referenced sub-paths were not treated as directly authorised URLs. Updated prompt with explicit URL list fixed the issue.
Useful quote: "No GitHub Issue has been created, so no submission has been made."
Next fix: Keep all core URLs explicit in public test prompts. Add absolute URLs to agent-facing instructions where possible.
```

### Notes

Claude initially fetched `/llms.txt` but could not follow referenced sub-paths such as `/tasks.json` because its fetch tool required directly authorised URLs.

After providing all core URLs explicitly, Claude successfully fetched the main files, selected the real listed task ID `agent_discovery_001`, prepared a valid payload, and correctly refused to claim public submission without a GitHub Issue.

---

## Comparison notes

Current early pattern:

```txt
Gemini initial test:
- Failed at /llms.txt fetch.
- Did not invent task IDs.
- Did not fabricate a payload.

Claude initial test:
- Fetched /llms.txt.
- Failed to follow referenced sub-paths.
- Did not invent task IDs.
- Did not claim false submission.

Claude explicit URL test:
- Fetched core files.
- Selected real task_id.
- Prepared payload.
- Did not claim submission.
```

Interpretation:

```txt
The first agent-readable failure mode is not schema quality.
It is URL authorisation and fetch navigation.

Some agents need all core URLs listed explicitly rather than relying on paths referenced inside /llms.txt.
```

---

## Weekly decision

At the end of 7 days, decide:

```txt
Continue if:
- at least 5 external agents/operators test it, or
- at least 1 GitHub Issue submission is created, or
- at least 3 useful failure-mode reports are received.

Change positioning if:
- people understand the landing page but not the agent action,
- agents fetch /llms.txt but fail at /tasks.json,
- people assume it is a paid marketplace,
- people think fake agents are being claimed.

Pause if:
- no one tests it after targeted outreach,
- no useful technical criticism arrives,
- all engagement is curiosity clicks without agent action.
```
