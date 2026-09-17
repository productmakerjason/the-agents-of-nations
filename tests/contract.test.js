import { test } from 'node:test';
import assert from 'node:assert/strict';
import { buildDraft } from '../public/contract.js';
const input = { requester: 'Requester A', worker: 'Worker B', authority: 'Up to USD 100 for research only', scope: 'Compare 5 projects', exclusions: 'No outreach', deliverable: 'Markdown report', criteria: 'Five cited primary sources', reviewer: 'Requester A', price: '50.00', currency: 'USD', deadline: '2026-10-01T12:00', reviewHours: '48', rework: 'Worker-funded correction, one cure round then dispute', changes: 'Both parties must agree before extra work', dispute: 'Pause and refer to the agreed operator', delegation: 'No delegation without consent' };
test('draft keeps price, responsibility and acceptance separate; never invents agreement', () => {
  const draft = buildDraft(input);
  assert.equal(draft.status, 'draft');
  assert.deepEqual(draft.agreement, { requester: 'not_recorded', worker: 'not_recorded' });
  assert.equal(draft.payment.amount, '50.00');
  assert.equal(draft.payment.status, 'not_funded');
  assert.equal(draft.payment.pricing, 'fixed_all_in');
  assert.equal(draft.acceptance.reviewer, 'Requester A');
  assert.equal(draft.acceptance.status, 'not_reviewed');
  assert.equal(draft.responsibility.rework, input.rework);
  assert.equal(draft.execution.status, 'not_started');
  assert.equal(draft.execution.delegation, input.delegation);
});
test('invalid or ambiguous prices and missing conditions cannot be exported as complete drafts', () => {
  for (const patch of [{ price: '-1' }, { price: 'NaN' }, { price: '1e3' }, { price: '1.001' }, { criteria: ' ' }, { requester: '' }, { authority: '' }, { reviewHours: '0' }, { reviewHours: '2.5' }, { currency: 'FAKE' }, { deadline: '' }, { deadline: 'not-a-date' }]) {
    assert.throws(() => buildDraft({ ...input, ...patch }), undefined, JSON.stringify(patch));
  }
});
test('zero price is allowed and text is kept as data, not executed', () => {
  const draft = buildDraft({ ...input, price: '0', scope: '<img src=x onerror=alert(1)>' });
  assert.equal(draft.payment.amount, '0.00');
  assert.equal(draft.work.scope, '<img src=x onerror=alert(1)>');
});
test('invalid calendar dates cannot silently roll into another day', () => {
  assert.throws(() => buildDraft({ ...input, deadline: '2026-02-30T12:00' }));
});
