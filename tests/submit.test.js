import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POST, GET, OPTIONS } from '../api/submit/index.js';

const valid = { agent_name: 'test-agent', task_id: 'agent_discovery_001', output_format: 'structured_markdown', output: 'Operator supplied the URL.', confidence: 0.9 };
const request = (value) => new Request('https://example.test/api/submit', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(value) });

test('unknown task cannot receive passed validation', async () => {
  const result = await POST(request({ ...valid, task_id: 'invented_123' }));
  assert.equal(result.status, 400);
  assert.equal((await result.json()).validation.task_id_exists, false);
});
test('non-object JSON is rejected without crashing', async () => {
  for (const value of [null, [], 'hello', 42]) {
    assert.equal((await POST(request(value))).status, 400);
  }
});
test('required field types and confidence bounds are enforced', async () => {
  for (const patch of [{ agent_name: '  ' }, { output: {} }, { output_format: 1 }, { confidence: '1' }, { confidence: -1 }, { confidence: 1.1 }]) {
    assert.equal((await POST(request({ ...valid, ...patch }))).status, 400, JSON.stringify(patch));
  }
});
test('valid payload only acknowledges transient validation, not stored or accepted work', async () => {
  const result = await POST(request(valid));
  assert.equal(result.status, 200);
  const body = await result.json();
  assert.equal(body.submission_status, 'validated_not_stored');
  assert.equal(body.stored, false);
  assert.equal(body.completion_status, 'not_verified');
  assert.equal(body.acceptance_status, 'not_reviewed');
  assert.equal(body.receipt_id, undefined);
  assert.equal(body.validation.task_id_exists, true);
  assert.equal(body.validation.scope, 'payload_structure_and_task_membership');
});
test('zero confidence is valid and malformed JSON is rejected', async () => {
  assert.equal((await POST(request({ ...valid, confidence: 0 }))).status, 200);
  assert.equal((await POST(new Request('https://example.test', { method: 'POST', body: '{' }))).status, 400);
});
test('oversized input is rejected before validation', async () => {
  const result = await POST(request({ ...valid, output: 'a'.repeat(70_000) }));
  assert.equal(result.status, 413);
});
test('GET explains allowed methods and responses are not cached', () => {
  assert.equal(GET().status, 405);
  assert.equal(GET().headers.get('Allow'), 'POST, OPTIONS');
  assert.equal(GET().headers.get('Cache-Control'), 'no-store');
  assert.equal(OPTIONS().status, 204);
});
