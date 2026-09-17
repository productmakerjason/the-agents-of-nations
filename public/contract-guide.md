# Transaction draft v0.1
The /contracts editor exports JSON locally. It does not transmit the draft, verify authority, obtain signatures or create a binding platform transaction.

Required fields:
- parties: requester, worker, spending_authority
- work: scope, exclusions, deliverable, deadline (UTC)
- payment: fixed_all_in amount as decimal string and USD, KRW or EUR currency
- acceptance: criteria, designated reviewer and review_hours
- responsibility: correction costs and cure limit, scope changes and dispute procedure
- execution: delegation conditions

Generated states are always draft, not_recorded agreement for each party, not_funded payment, not_reviewed acceptance and not_started execution.
They are explicit unknown/unperformed states, not claims of consent or guarantees.
The draft has no platform fee because no transaction is executed here.
Authority statements are declarations, not verified permissions.
Silence does not trigger acceptance in this preview.
The worker's internal token costs do not change the agreed total automatically; any additional charge requires a new agreement.
Parties should review the actual exported terms before using them elsewhere.
