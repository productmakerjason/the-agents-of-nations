const form = document.querySelector('#validator');
form.addEventListener('submit', async event => {
  event.preventDefault();
  const button = form.querySelector('button');
  const status = document.querySelector('#status');
  const result = document.querySelector('#result');
  const payload = document.querySelector('#payload').value;
  result.hidden = true;
  try { JSON.parse(payload); } catch { status.textContent = 'Enter valid JSON before sending.'; return; }
  if (new TextEncoder().encode(payload).length > 65536) { status.textContent = 'Payload exceeds 65,536 bytes.'; return; }
  button.disabled = true; status.textContent = 'Checking payload…';
  try {
    const response = await fetch('/api/submit', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: payload, signal: AbortSignal.timeout(15000) });
    const body = await response.json();
    result.textContent = JSON.stringify(body, null, 2); result.hidden = false;
    status.textContent = response.ok && body.submission_status === 'validated_not_stored' && body.stored === false ? 'Payload validated. Not stored, accepted, or completed.' : 'Payload not validated. Review the response below.';
  } catch { status.textContent = 'No usable response received. Outcome unknown; no completion is claimed.'; }
  finally { button.disabled = false; }
});
