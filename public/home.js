const list = document.querySelector('#task-list');
try {
  const response = await fetch('/tasks.json');
  if (!response.ok) throw new Error('Task feed unavailable');
  const feed = await response.json();
  if (!Array.isArray(feed.tasks)) throw new Error('Invalid task feed');
  list.replaceChildren();
  for (const task of feed.tasks) {
    const row = document.createElement('div'); row.className = 'task';
    const id = document.createElement('div'); id.className = 'id'; id.textContent = task.task_id; id.style.overflowWrap = 'anywhere';
    const title = document.createElement('div'); title.className = 'title'; title.textContent = task.title;
    const description = document.createElement('span'); description.className = 'it'; description.textContent = task.instructions; title.append(description);
    const category = document.createElement('div'); category.className = 'meta';
    const categoryLabel = document.createElement('b'); categoryLabel.textContent = 'Capability'; category.append(categoryLabel, task.category);
    const deadline = document.createElement('div'); deadline.className = 'meta';
    const deadlineLabel = document.createElement('b'); deadlineLabel.textContent = 'Deadline'; deadline.append(deadlineLabel, 'To agree');
    const reward = document.createElement('div'); reward.className = 'bounty'; reward.textContent = '—';
    const unit = document.createElement('span'); unit.className = 'unit'; unit.textContent = 'UNFUNDED'; reward.append(unit);
    const link = document.createElement('a'); link.className = 'accept'; link.href = '/contracts?task=' + encodeURIComponent(task.task_id); link.textContent = 'Draft terms →';
    row.append(id, title, category, deadline, reward, link); list.append(row);
  }
} catch {
  list.textContent = 'Task feed unavailable. No tasks were inferred. ';
  const link = document.createElement('a'); link.href = '/tasks.json'; link.textContent = 'Open the task feed.'; list.append(link);
}
