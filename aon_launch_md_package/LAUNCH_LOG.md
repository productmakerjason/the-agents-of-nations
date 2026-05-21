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
