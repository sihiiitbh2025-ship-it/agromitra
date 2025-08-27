const messagesEl = document.getElementById('messages');
const form = document.getElementById('chat-form');
const input = document.getElementById('input');
const clearBtn = document.getElementById('clear');

function appendMessage(role, text){
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if(!text) return;
  appendMessage('user', text);
  input.value = '';
  form.querySelector('button').disabled = true;
  try {
    const r = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, session_id: localStorage.getItem('sessionId') })
    });
    const data = await r.json();
    appendMessage('assistant', data.reply);
  } catch (err) {
    appendMessage('assistant', 'Error: ' + err);
  } finally {
    form.querySelector('button').disabled = false;
    input.focus();
  }
});

clearBtn.addEventListener('click', async () => {
  await fetch('/api/clear', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: localStorage.getItem('sessionId') })
  });
  messagesEl.innerHTML = '';
  appendMessage('assistant', 'Memory cleared for this session.');
});
