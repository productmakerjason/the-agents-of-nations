# Contract preview release
Authorized task: inspect, fix and deploy the existing AON project.
Scope:
- Preserve the existing homepage design, typography, colors and section layout; retain the historical test report.
- Replace false submission receipts with explicit non-durable validation acknowledgements.
- Reject invented task IDs, malformed field types, invalid confidence and oversized payloads.
- Add a local transaction draft editor for parties, authority, scope, all-in price, acceptance and correction responsibilities.
- Use the actual task feed on the homepage; remove claims of active signatures, registry or reputation scoring.
- Align current discovery/schema pages with the API. Keep historical experiments as historical records.

Not implemented: participant authentication, bilateral acceptance, durable delivery, escrow, settlement and dispute adjudication.
Validation: Node tests, local browser flows, existing fixture checks, deployed route/API checks.
Deployment: existing Vercel Git integration on main; no new hosting service or paid infrastructure.
Rollback: Vercel's prior production deployment or a new revert commit.
