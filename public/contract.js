export function buildDraft(input) {
  const required = ['requester','worker','authority','scope','exclusions','deliverable','criteria','reviewer','deadline','rework','changes','dispute','delegation'];
  const clean = {};
  for (const key of required) {
    if (typeof input[key] !== 'string' || !input[key].trim()) throw new Error('Please complete: ' + key);
    clean[key] = input[key].trim();
  }
  if (!/^\d{1,12}(\.\d{1,2})?$/.test(input.price)) throw new Error('Enter a non-negative amount with up to two decimal places.');
  if (!['USD','KRW','EUR'].includes(input.currency)) throw new Error('Choose a supported currency.');
  if (!/^\d+$/.test(input.reviewHours) || Number(input.reviewHours) < 1 || Number(input.reviewHours) > 8760) throw new Error('Review time must be 1–8760 whole hours.');
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(clean.deadline) || !Number.isFinite(Date.parse(clean.deadline + 'Z'))) throw new Error('Enter a valid UTC deadline.');
  if (new Date(clean.deadline + 'Z').toISOString().slice(0, 16) !== clean.deadline) throw new Error('Enter a valid calendar date.');
  const [whole, fraction = ''] = input.price.split('.');
  return {
    version: '0.1', status: 'draft',
    parties: { requester: clean.requester, worker: clean.worker, spending_authority: clean.authority },
    agreement: { requester: 'not_recorded', worker: 'not_recorded' },
    work: { scope: clean.scope, exclusions: clean.exclusions, deliverable: clean.deliverable, deadline: clean.deadline + ':00Z' },
    payment: { pricing: 'fixed_all_in', amount: String(Number(whole)) + '.' + fraction.padEnd(2, '0'), currency: input.currency, status: 'not_funded', additional_charges: 'Require a new agreement before work' },
    acceptance: { criteria: clean.criteria, reviewer: clean.reviewer, review_hours: Number(input.reviewHours), status: 'not_reviewed', silence: 'No automatic acceptance in this preview' },
    responsibility: { rework: clean.rework, scope_changes: clean.changes, dispute: clean.dispute },
    execution: { status: 'not_started', delegation: clean.delegation },
    limitations: ['Local draft only; no identity or authority verification', 'No party acceptance recorded', 'No execution, escrow, payment, or dispute service']
  };
}
