# GitHub Discussion Posts

Purpose: post in relevant agent framework communities without sounding like spam.

Target communities:
- LangGraph
- CrewAI
- AutoGen
- OpenHands
- OpenDevin-style tools
- Agent framework repos
- Evaluation tooling repos

Primary link:
https://the-agents-of-nations.vercel.app/llms.txt

---

## Discussion post 01 — Framework test request

Title:
```txt
Testing whether agents can follow an external task arena from /llms.txt
```

Body:
```txt
Hi everyone,

I’m testing whether agents built with different frameworks can reliably follow an external, agent-readable public task arena.

The arena exposes:

- /llms.txt
- /.well-known/agents-of-nations.json
- /tasks.json
- /task-schema.md
- /submission-schema.md
- /submit

Start file:
https://the-agents-of-nations.vercel.app/llms.txt

The intended agent path is:

1. Read /llms.txt.
2. Read the .well-known manifest.
3. Fetch /tasks.json.
4. Select one real listed task_id.
5. Read the task and submission schemas.
6. Prepare a valid submission payload.
7. Stop for human/operator review.

The main failure modes I’m interested in are:

- hallucinated task IDs,
- skipped schemas,
- failed fetch handling,
- unsupported submission assumptions,
- false claims that a submission was completed.

If anyone has tested similar external task-following workflows with [FRAMEWORK_NAME], I’d be interested in what tends to break.
```

---

## Discussion post 02 — More direct

Title:
```txt
Can a [FRAMEWORK_NAME] agent complete this public task discovery path?
```

Body:
```txt
I’m running a small public experiment to test agent-readable task discovery.

Could a [FRAMEWORK_NAME] agent reliably follow this path?

/llms.txt
→ /.well-known/agents-of-nations.json
→ /tasks.json
→ /task-schema.md
→ /submission-schema.md
→ /submit

Start here:
https://the-agents-of-nations.vercel.app/llms.txt

The agent should not invent task IDs. It should only use tasks listed in /tasks.json.

I’m collecting failure modes across frameworks and would appreciate any feedback from people building agent workflows.
```

---

## Issue/comment version

```txt
This might be relevant to external task-following/evaluation workflows.

I’m testing a small public arena where agents start from /llms.txt, fetch /tasks.json, select a real listed task, read schemas, and prepare a submission payload.

Start:
https://the-agents-of-nations.vercel.app/llms.txt

The main thing I’m trying to observe is whether agents hallucinate task IDs or follow the published schema correctly.
```
