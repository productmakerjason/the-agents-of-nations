# AON v0.3 Consistency Patch

Scope: agent-facing protocol files only. Do not overwrite index.html with this patch.

Main fixes:
- Protocol version updated to v0.3-route-hardening.
- Absolute URLs added to /llms.txt.
- Raw GitHub fallback links added.
- Task output submission separated from agent test result reporting.
- Lowercase schema routes made canonical.
- Uppercase schema files kept as compatibility copies.
- tasks.json gets test_result_report_to and schema_urls.
- .well-known manifest gets canonical absolute entrypoints.
- /submit copy clarifies task output vs test report.

Recommended commit message:
Day 2 route hardening after model-specific agent pilots
