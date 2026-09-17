import { buildDraft } from './contract.js';
const form = document.querySelector('#contract-form');
const status = document.querySelector('#status');
const preview = document.querySelector('#preview');
const download = document.querySelector('#download');
let draft;
function invalidate() { draft = undefined; download.disabled = true; preview.hidden = true; status.textContent = 'Changes are not reviewed. Review the draft before exporting.'; }
form.addEventListener('input', invalidate);
form.addEventListener('change', invalidate);
form.addEventListener('submit', event => {
  event.preventDefault();
  try {
    draft = buildDraft(Object.fromEntries(new FormData(form)));
    preview.textContent = JSON.stringify(draft, null, 2); preview.hidden = false; download.disabled = false;
    status.textContent = 'Draft ready for review. Neither party has accepted it. No funds are held.';
    preview.focus();
  } catch (error) { draft = undefined; download.disabled = true; preview.hidden = true; status.textContent = error.message; }
});
download.addEventListener('click', () => {
  if (!draft) return;
  const url = URL.createObjectURL(new Blob([JSON.stringify(draft, null, 2)], { type: 'application/json' }));
  const link = document.createElement('a'); link.href = url; link.download = 'aon-transaction-draft.json'; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  status.textContent = 'Draft download requested. Share it for review; this is not a signed agreement.';
});
const taskId = new URLSearchParams(location.search).get('task');
if (taskId) {
  const note = document.querySelector('#task-status');
  try {
    const response = await fetch('/tasks.json');
    if (!response.ok) throw new Error();
    const { tasks } = await response.json();
    const task = tasks.find(item => item.task_id === taskId);
    if (!task) { note.textContent = 'This task ID is not listed. No task terms were loaded.'; }
    else {
      // Never overwrite terms the user has already started entering.
      for (const [key, value] of Object.entries({ scope: task.instructions, deliverable: task.output_format, criteria: task.evaluation_criteria.join('\n') })) {
        if (!form.elements[key].value) form.elements[key].value = value;
      }
      note.textContent = 'Based on sample task ' + task.task_id + '. No reservation, funding, or award exists.';
    }
  } catch { note.textContent = 'Task feed unavailable. No task terms were inferred.'; }
}
