const messagesEl = document.getElementById('messages');
const form = document.getElementById('chat-form');
const input = document.getElementById('input');
const clearBtn = document.getElementById('clear');

<<<<<<< HEAD
// 🔹 Ensure session ID exists
if (!localStorage.getItem('sessionId')) {
  localStorage.setItem('sessionId', Date.now().toString());
}

function appendMessage(role, text) {
=======
function appendMessage(role, text){
>>>>>>> c286ca28f3e3124d2c7c009cf2988c7d6b8edd48
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

<<<<<<< HEAD
// 🔹 Show a temporary "typing..." indicator
function showTyping() {
  const typing = document.createElement('div');
  typing.className = 'msg assistant typing';
  typing.textContent = "Assistant is thinking...";
  typing.id = "typing-msg";
  messagesEl.appendChild(typing);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function removeTyping() {
  const typing = document.getElementById("typing-msg");
  if (typing) typing.remove();
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  appendMessage('user', text);
  input.value = '';
  form.querySelector('button').disabled = true;

  // 🔹 show "thinking..." message
  showTyping();

=======
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if(!text) return;
  appendMessage('user', text);
  input.value = '';
  form.querySelector('button').disabled = true;
>>>>>>> c286ca28f3e3124d2c7c009cf2988c7d6b8edd48
  try {
    const r = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
<<<<<<< HEAD
      body: JSON.stringify({ 
        message: text, 
        session_id: localStorage.getItem('sessionId') 
      })
    });

    const data = await r.json();

    removeTyping();

    if (data.reply) {
      appendMessage('assistant', data.reply);
    } else {
      appendMessage('assistant', '⚠️ No reply received.');
    }
  } catch (err) {
    removeTyping();
    appendMessage('assistant', '❌ Error: ' + err.message);
=======
      body: JSON.stringify({ message: text, session_id: localStorage.getItem('sessionId') })
    });
    const data = await r.json();
    appendMessage('assistant', data.reply);
  } catch (err) {
    appendMessage('assistant', 'Error: ' + err);
>>>>>>> c286ca28f3e3124d2c7c009cf2988c7d6b8edd48
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
<<<<<<< HEAD
  appendMessage('assistant', '🧹 Memory cleared for this session.');
=======
  appendMessage('assistant', 'Memory cleared for this session.');
>>>>>>> c286ca28f3e3124d2c7c009cf2988c7d6b8edd48
});
