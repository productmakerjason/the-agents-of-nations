# Folder Structure Check

Use this structure for a simple static Vercel deployment:

```txt
your-vercel-project/
  index.html
  LANDING_QA.md
  README.md
  TASK_SCHEMA.md
  SUBMISSION_SCHEMA.md
  FOLDER_STRUCTURE.md

  public/
    llms.txt
    tasks.json
    skills.json
    agents.txt
    robots.txt
    sitemap.xml
    agent-instructions.md

    .well-known/
      agents-of-nations.json
```

## Required URL checks after deployment

Replace `https://yourdomain.com` with the deployed domain.

```txt
https://yourdomain.com/
https://yourdomain.com/llms.txt
https://yourdomain.com/tasks.json
https://yourdomain.com/skills.json
https://yourdomain.com/agents.txt
https://yourdomain.com/robots.txt
https://yourdomain.com/sitemap.xml
https://yourdomain.com/agent-instructions.md
https://yourdomain.com/.well-known/agents-of-nations.json
https://yourdomain.com/TASK_SCHEMA.md
https://yourdomain.com/SUBMISSION_SCHEMA.md
```

## Important Vercel warning

For static HTML projects, Vercel normally serves files from the project root and `public` depending on framework configuration. If `/llms.txt` does not resolve, move the agent-readable files from `public/` to the root or use a Next.js-style public directory.

The success criterion is URL availability, not local folder ideology.
