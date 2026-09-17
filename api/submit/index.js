import { readFileSync } from 'node:fs';

const taskIds = new Set(JSON.parse(readFileSync(new URL('../../public/tasks.json', import.meta.url), 'utf8')).tasks.map(task => task.task_id));
const headers = {
  'Content-Type': 'application/json; charset=utf-8',
  'Cache-Control': 'no-store',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Allow': 'POST, OPTIONS'
};
const json = (body, status = 200) => new Response(JSON.stringify({
  stored: false, completion_status: 'not_verified', acceptance_status: 'not_reviewed', ...body
}), { status, headers });
const rejected = (error, status = 400, extra = {}) => json({ status: 'rejected', submission_status: 'invalid_payload', error, ...extra }, status);

export function OPTIONS() { return new Response(null, { status: 204, headers }); }
export function GET() { return json({ status: 'error', error: 'method_not_allowed', message: 'POST validates a payload only. No durable storage, acceptance or settlement is provided.' }, 405); }

export async function POST(request) {
  // Bound bytes while reading instead of trusting Content-Length.
  const reader = request.body?.getReader();
  const chunks = [];
  let size = 0;
  if (reader) {
    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        size += value.byteLength;
        if (size > 65_536) {
          await reader.cancel();
          return rejected('payload_too_large', 413);
        }
        chunks.push(value);
      }
    } catch { return rejected('unreadable_body'); }
  }
  let payload;
  try { payload = JSON.parse(Buffer.concat(chunks).toString('utf8')); }
  catch { return rejected('invalid_json'); }
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) return rejected('object_required');

  const invalidFields = ['agent_name', 'task_id', 'output_format', 'output'].filter(key => typeof payload[key] !== 'string' || !payload[key].trim());
  if (typeof payload.confidence !== 'number' || !Number.isFinite(payload.confidence) || payload.confidence < 0 || payload.confidence > 1) invalidFields.push('confidence');
  const exists = taskIds.has(payload.task_id);
  const validation = {
    status: invalidFields.length || !exists ? 'failed' : 'passed',
    required_fields_present: ['agent_name', 'task_id', 'output_format', 'output', 'confidence'].every(key => payload[key] !== undefined && payload[key] !== null),
    invalid_fields: invalidFields, task_id_exists: exists,
    schema_version: '0.4-contract-preview', scope: 'payload_structure_and_task_membership'
  };
  if (invalidFields.length || !exists) return rejected(exists ? 'invalid_fields' : 'unknown_task', 400, { validation });
  return json({
    status: 'validated', submission_status: 'validated_not_stored', task_id: payload.task_id, validation,
    message: 'Payload structure and task membership checked. Output quality was not reviewed. Nothing was stored; this is not a submission receipt, contract acceptance, or completion proof.'
  });
}
