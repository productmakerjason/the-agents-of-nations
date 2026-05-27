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
|  | X | Posted launch thread | https://the-agents-of-nations.vercel.app/llms.txt | pending | Thread focused on Claude/Gemini behaviour, fetch failures, safe stopping, and hallucination avoidance. |
|  | Threads | Posted launch content | https://the-agents-of-nations.vercel.app/llms.txt | pending | First public Threads post published. |
|  | Threads | Contacted relevant AI agent accounts | https://the-agents-of-nations.vercel.app/llms.txt | pending | Tone adjusted to be more conversational and human. Outreach focused on agent builders and people posting about AI agents. |
|  | Threads | Posted follow-up observation | https://the-agents-of-nations.vercel.app/llms.txt | pending | Follow-up focused on safe stopping as a useful failure mode. |
|  | X | DM outreach | N/A | blocked | X DM sending currently unavailable. Use public replies only. |
|  | GitHub Discussions | Replied to two CrewAI discussions | https://the-agents-of-nations.vercel.app/llms.txt | pending | New discussion button was not visible, so comments were added to relevant existing discussions. |
|  | Claude | Run explicit URL discovery test | https://the-agents-of-nations.vercel.app/llms.txt | success | Claude selected a real task_id after explicit URLs were provided. |
|  | Gemini | Run explicit URL discovery test | https://the-agents-of-nations.vercel.app/llms.txt | fetch failure | Gemini failed to fetch, but stopped safely without hallucinating a task or payload. |
|  | Cursor | Skipped intentionally | N/A | skipped | Initial validation focuses on Claude vs Gemini behaviour. |

---

## Distribution action — X launch thread

```txt
Date: 2026-05-21
Channel: X
Action: Posted launch thread
Link used: https://the-agents-of-nations.vercel.app/llms.txt
Result: pending
Notes: Thread focused on Claude/Gemini behaviour, fetch failures, safe stopping, and hallucination avoidance.
```

---

## Distribution action — Threads launch post and outreach

```txt
Date: 2026-05-21
Channel: Threads
Action: Posted launch content and contacted relevant AI agent accounts
Link used: https://the-agents-of-nations.vercel.app/llms.txt
Result: pending
Notes: Tone adjusted to be more conversational and human. Outreach focused on agent builders and people posting about AI agents.
```

---

## Distribution action — Threads follow-up post

```txt
Date: 2026-05-21
Channel: Threads
Action: Posted follow-up observation
Link used: https://the-agents-of-nations.vercel.app/llms.txt
Result: pending
Notes: Follow-up focused on the idea that safe failure may be as important as task completion for agent-readable infrastructure.
```

---

## Distribution action — X DM blocked

```txt
Date: 2026-05-21
Channel: X
Action: Attempted direct outreach
Link used: N/A
Result: blocked
Notes: X DM sending is currently unavailable. Use public replies, quote posts, follows, and pinned thread instead.
```

---

## Distribution action — CrewAI discussion replies

```txt
Date: 2026-05-21
Channel: GitHub Discussions
Platform/community: CrewAI
Action: Replied to two existing relevant discussions instead of creating a new discussion
Link used: https://the-agents-of-nations.vercel.app/llms.txt
Result: pending
Discussion reply 1: https://github.com/crewAIInc/crewAI/discussions/4232#discussioncomment-17006756
Discussion reply 2: https://github.com/crewAIInc/crewAI/discussions/1180#discussioncomment-17006762
Notes: New discussion button was not visible, so distribution shifted to existing active discussions. This is less spammy and more context-aware.
```

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

## Test result — Gemini explicit URL discovery failure

```txt
Date: 2026-05-21
Tool/framework: Gemini
Model: Gemini
Start URL: https://the-agents-of-nations.vercel.app/llms.txt
Files fetched: none
Files failed to fetch: /llms.txt, /tasks.json, /task-schema.md, /submission-schema.md
Selected task_id: none
Payload generated: no
Invented task ID: no
Claimed false submission: no
Failure point: Gemini failed to fetch all directly provided core URLs, including /llms.txt and /tasks.json.
Useful quote: "Because I cannot fetch /tasks.json, I must stop the task here and report the outcome."
Next fix: Treat Gemini as a fetch-limited environment. Use Gemini results as a failure-mode example rather than a successful public discovery test.
```

### Notes

Gemini failed even after all core URLs were explicitly provided. This suggests the issue is not only relative-path navigation. In this environment, Gemini could not access the public Vercel URLs through its fetch process.

However, this is still a useful result. Gemini followed the hard rules: it did not invent a task ID, did not fabricate a submission payload, and did not claim a GitHub Issue had been created.

Current interpretation:

```txt
Claude explicit URL test:
- Public discovery path works when URLs are directly authorised.

Gemini explicit URL test:
- Public discovery path blocked by fetch failure.
- Anti-hallucination behaviour works.
```

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

Gemini explicit URL test:
- Failed to fetch all directly provided core URLs.
- Did not invent task IDs.
- Did not fabricate a payload.
- Did not claim submission.
```

Interpretation:

```txt
The first agent-readable failure mode is not schema quality.
It is URL authorisation and fetch navigation.

Some agents need all core URLs listed explicitly rather than relying on paths referenced inside /llms.txt.

Some agent environments may still be unable to fetch public Vercel URLs even when URLs are explicitly provided. For those environments, safe stopping behaviour matters more than forced completion.
```

---

## 24-hour response review

Evaluate after 24 hours:

```txt
Strong signal:
- someone tests it
- someone asks about the schema
- someone asks why submissions use GitHub Issues
- someone reports framework-specific behaviour
- someone shares a failure mode

Weak signal:
- likes only
- follows only
- views only

Bad signal:
- no one understands the project
- people treat it as a generic AI app
- people do not understand what /llms.txt is for
```

---

## Tomorrow plan

### Objective

Move from public posting to targeted validation.

The goal is not more visibility. The goal is to get at least one external person or external agent setup to test the arena.

### Priority 1 — Check all response surfaces

Check:

```txt
Threads replies
Threads DMs
X replies
X notifications
CrewAI discussion replies
GitHub repo activity
GitHub Issues
Vercel route hits if available
```

Record any result in this file.

### Priority 2 — Reply to any real engagement

Use this response if someone says it is interesting:

```txt
Thanks — the part I’m most interested in is where your setup breaks.

The ideal test is:
1. start from /llms.txt
2. fetch /tasks.json
3. select a real task_id
4. inspect schemas
5. prepare a payload
6. stop safely if anything cannot be verified

The start file is here:
https://the-agents-of-nations.vercel.app/llms.txt
```

Use this if someone asks what you want from them:

```txt
The most useful feedback would be:

- which files your agent could fetch
- whether it selected a real task_id
- whether it read the schemas
- whether it invented anything
- whether it claimed submission without a GitHub Issue

Even failure results are useful.
```

### Priority 3 — Do not over-post

Do not post another broad launch thread tomorrow morning.

First, check whether the current posts generated:

```txt
replies
tests
technical criticism
profile clicks
GitHub activity
```

Post again only if there is a specific observation or external result to share.

### Priority 4 — Run one more external-framework test only if useful

Potential next test environments:

```txt
Perplexity
OpenHands
CrewAI local example
AutoGen example
LangGraph simple agent
```

Do not spend more than 60 minutes setting up a local framework tomorrow unless there is a clear reason.

### Priority 5 — Decide next channel

Based on response:

```txt
If Threads responds:
- continue conversational outreach

If GitHub responds:
- deepen technical discussion

If X gets replies:
- use X for public failure-mode notes

If no one responds:
- move to Reddit or Hacker News with a sharper failure-mode angle
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
---

# Day 2 Update — Route Hardening, Agent Pilots, and Discovery Testing

Purpose: record route hardening, model-specific agent pilots, and discovery testing.

## Day 2 summary

Day 2 moved from broad visibility to practical agent workflow validation.

The key shift:

```txt
Day 1: Can we put the arena online and ask people to test it?
Day 2: Can real model/browser workflows follow the arena, and where do they break?
```

## Route hardening applied

Protocol updated to:

```txt
0.3-route-hardening
```

Files updated:

```txt
public/llms.txt
public/tasks.json
public/task-schema.md
public/submission-schema.md
public/TASK_SCHEMA.md
public/SUBMISSION_SCHEMA.md
public/agent-instructions.md
public/submit.html
public/.well-known/agents-of-nations.json
public/skills.json
```

Main fixes:

```txt
Absolute URLs added to /llms.txt
Raw GitHub fallback links added
Lowercase schema routes made canonical
Uppercase schema routes retained as compatibility copies
Task output submission separated from agent test result reporting
tasks.json updated with schema_urls and test_result_report_to
.well-known manifest updated with canonical absolute entrypoints
```

## Route QA

Manual browser QA completed.

Confirmed live:

```txt
/llms.txt
/tasks.json
/task-schema.md
/submission-schema.md
/TASK_SCHEMA.md
/SUBMISSION_SCHEMA.md
/submit
/.well-known/agents-of-nations.json
/agent-instructions.md
```

QA result:

```txt
Route QA: Green
Protocol consistency: Green-minus
```

Reason for Green-minus:

```txt
Uppercase compatibility schema routes are still present. This is intentional for backward compatibility but should be cleaned up later.
```

## Agent Test Issue records

### Issue #1 — Internal maintainer walkthrough

Result:

```txt
Internal maintainer walkthrough completed.
Not an external verified run.
Purpose: first public example / internal pilot record.
```

### Issue #2 — Gemini pilot — safe fetch failure

Result:

```txt
Gemini failed to fetch the start file and task feed.
It did not invent a task_id.
It did not fabricate schemas or submission status.
It stopped safely.
```

### Issue #3 — Claude pilot — downstream fetch failure

Result:

```txt
Claude fetched /llms.txt but failed to fetch downstream routes.
It did not invent a task_id.
It did not claim submission.
It stopped safely.
```

### Issue #4 — ChatGPT pilot — partial workflow success

Result:

```txt
ChatGPT fetched /llms.txt and /tasks.json.
It selected the real task_id agent_discovery_001.
It prepared a payload.
It could not fetch standalone schema files in the pre-fix run.
It did not claim submission.
```

### Issue #5 — ChatGPT post-fix pilot — raw fallback schema success

Result:

```txt
ChatGPT fetched /llms.txt.
Direct deployed Vercel routes failed in the browsing environment.
Raw GitHub fallback links worked.
ChatGPT fetched tasks.json, skills.json, task-schema.md, submission-schema.md, manifest, and agent-instructions.md through fallback links.
It selected agent_discovery_001.
It prepared a payload.
It did not claim submission.
```

Interpretation:

```txt
v0.3 route hardening worked for ChatGPT because raw fallback enabled recovery.
Direct deployed route fetch reliability remains inconsistent in some automated browsing environments.
```

### Issue #6 — Claude post-fix pilot — text-mentioned URLs blocked

Result:

```txt
Claude fetched /llms.txt.
Claude failed to fetch /tasks.json because URLs mentioned inside /llms.txt were not treated as directly fetchable URLs by its tool.
It did not select a task_id.
It did not read schemas.
It did not claim submission.
It stopped safely.
```

Interpretation:

```txt
Claude-style fetch environments may require explicit URL injection for all core endpoints.
```

### Issue #7 — Claude explicit URL post-fix pilot — full workflow success

Result:

```txt
Claude was given all core endpoint URLs directly.
Claude fetched /tasks.json, /task-schema.md, /submission-schema.md, and /submit.
It selected the real task_id agent_discovery_001.
It prepared a payload.
It did not claim submission because public GitHub Issue filing requires human/operator action.
```

Interpretation:

```txt
Claude can complete the workflow when URLs are supplied directly.
The failure mode is not reasoning ability; it is URL permission and discovery handling.
```

## Search discovery test

Gemini and Claude were asked to find public tasks for autonomous agents and whether they recognised The Agents of Nations by name.

Result:

```txt
Gemini did not recognise The Agents of Nations and surfaced established benchmarks such as WebArena, Mind2Web, WebVoyager, SWE-bench, GAIA, OSWorld, AgentBench, and ALFWorld.

Claude did not find The Agents of Nations through targeted search and asked for a direct link.

Both results suggest that The Agents of Nations is not yet discoverable by name through general AI search or browsing environments.
```

Interpretation:

```txt
The arena currently works best when agents are given the direct start file or explicit endpoint URLs.
Organic or search-based discovery remains weak.
```

## Discovery funnel status

```txt
Direct URL test: Medium
Explicit URL test: High
Search discovery test: Low
Organic discovery test: Very low / unproven
```

## Key learning

```txt
The Agents of Nations is not yet an agent-discovered work marketplace.

It is currently a working agent-readable reliability test arena when agents are given the start file or explicit endpoint URLs.
```

## Day 2 final status

```txt
Product readiness: Green
Route clarity: Green-minus
Internal protocol validation: Green
External validation: Yellow-minus
Commercial validation: Red
Search discoverability: Red
Overall Day 2: Yellow
```

## Next fixes

```txt
1. Update GitHub README with stronger discovery keywords.
2. Update GitHub repository description.
3. Create durable external traces on GitHub, HN, and Reddit.
4. Add discovery funnel KPIs to Day 3 planning.
5. Reconcile capabilities vs capabilities_used in submission payloads.
6. Keep lowercase schema routes canonical and uppercase schema routes as compatibility copies for now.
```

