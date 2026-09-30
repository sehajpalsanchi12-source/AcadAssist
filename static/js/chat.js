/**
 * AcadAssist AI Chat Widget — Powered by Google Gemini 2.0 Flash
 * Floating study assistant for LPU Verto students
 */
const AcadChat = {
  isOpen: false,
  history: [],
  currentSubject: null,
  currentSubjectName: null,

  init() {
    this.injectChatUI();
  },

  injectChatUI() {
    const html = `
      <!-- Floating Chat Button -->
      <button id="chat-fab" onclick="AcadChat.toggle()" title="Chat with AcadAssist AI"
        style="position:fixed;bottom:24px;right:24px;z-index:9000;width:56px;height:56px;border-radius:50%;
               background:linear-gradient(135deg,#ec4899,#f97316);color:white;border:none;cursor:pointer;
               box-shadow:0 8px 32px rgba(236,72,153,0.40);display:flex;align-items:center;
               justify-content:center;transition:transform 0.2s,box-shadow 0.2s;"
        onmouseover="this.style.transform='scale(1.12)';this.style.boxShadow='0 12px 40px rgba(236,72,153,0.5)'"
        onmouseout="this.style.transform='scale(1)';this.style.boxShadow='0 8px 32px rgba(236,72,153,0.40)'">
        <svg id="chat-icon-open" width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
        </svg>
        <span id="chat-icon-close" style="display:none;font-size:20px;font-weight:900;">✕</span>
      </button>

      <!-- Chat Window -->
      <div id="acad-chat-window"
        style="display:none;position:fixed;bottom:92px;right:24px;z-index:8999;width:360px;
               max-width:calc(100vw - 24px);height:530px;border-radius:24px;
               background:#fff;border:1px solid rgba(0,0,0,0.1);
               box-shadow:0 24px 64px rgba(0,0,0,0.18);flex-direction:column;overflow:hidden;">

        <!-- Header -->
        <div style="padding:14px 16px;background:linear-gradient(135deg,#ec4899,#f97316);color:white;
                    display:flex;align-items:center;justify-content:space-between;flex-shrink:0;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,0.22);
                        display:flex;align-items:center;justify-content:center;font-size:17px;">🤖</div>
            <div>
              <div style="font-weight:900;font-size:14px;letter-spacing:-0.2px;">AcadAssist AI</div>
              <div style="font-size:10px;opacity:0.85;">Powered by Gemini · LPU Study Expert</div>
            </div>
          </div>
          <button onclick="AcadChat.toggle()" style="background:none;border:none;color:white;font-size:20px;cursor:pointer;opacity:0.8;line-height:1;">✕</button>
        </div>

        <!-- Messages -->
        <div id="acad-chat-messages"
          style="flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;
                 background:#f9fafb;"></div>

        <!-- Subject Context -->
        <div style="padding:8px 12px;border-top:1px solid rgba(0,0,0,0.07);background:#f3f4f6;flex-shrink:0;">
          <div style="display:flex;align-items:center;gap:7px;">
            <span style="font-size:10px;color:#9ca3af;white-space:nowrap;font-weight:700;">📚 Subject:</span>
            <select id="acad-chat-subject"
              onchange="AcadChat.setSubject(this.value, this.options[this.selectedIndex].text)"
              style="flex:1;font-size:11px;padding:4px 8px;border-radius:8px;border:1px solid #e5e7eb;
                     background:white;color:#374151;outline:none;">
              <option value="">General LPU Help</option>
              <option value="MTH166">MTH166 — Differential Equations</option>
              <option value="CSE101">CSE101 — Computer Programming</option>
              <option value="CSE205">CSE205 — Data Structures</option>
              <option value="CSE316">CSE316 — Operating Systems</option>
              <option value="CSE306">CSE306 — Software Engineering</option>
              <option value="PHY109">PHY109 — Engineering Physics</option>
              <option value="ECE131">ECE131 — Basic Electronics</option>
              <option value="CHE110">CHE110 — Engineering Chemistry</option>
              <option value="INT213">INT213 — Machine Learning</option>
              <option value="CSE325">CSE325 — Computer Networks</option>
            </select>
          </div>
        </div>

        <!-- Quick prompts -->
        <div id="acad-quick-prompts" style="padding:6px 12px;border-top:1px solid rgba(0,0,0,0.05);background:#f3f4f6;display:flex;gap:6px;overflow-x:auto;flex-shrink:0;">
          <button onclick="AcadChat.quickSend('Explain in simple words for LPU exam')" style="white-space:nowrap;font-size:10px;padding:4px 10px;border-radius:20px;border:1px solid #e5e7eb;background:white;color:#374151;cursor:pointer;">💡 Explain this</button>
          <button onclick="AcadChat.quickSend('Give me 5 MCQs on this topic for LPU CA exam')" style="white-space:nowrap;font-size:10px;padding:4px 10px;border-radius:20px;border:1px solid #e5e7eb;background:white;color:#374151;cursor:pointer;">📝 Practice MCQs</button>
          <button onclick="AcadChat.quickSend('What are the most important topics for LPU MTE exam?')" style="white-space:nowrap;font-size:10px;padding:4px 10px;border-radius:20px;border:1px solid #e5e7eb;background:white;color:#374151;cursor:pointer;">🎯 Key Topics</button>
          <button onclick="AcadChat.quickSend('Write a 5-mark answer for LPU exam on this')" style="white-space:nowrap;font-size:10px;padding:4px 10px;border-radius:20px;border:1px solid #e5e7eb;background:white;color:#374151;cursor:pointer;">✍️ 5-mark Answer</button>
        </div>

        <!-- Input -->
        <div style="display:flex;gap:8px;padding:10px 12px;border-top:1px solid rgba(0,0,0,0.08);background:#fff;flex-shrink:0;">
          <input id="acad-chat-input" type="text"
            placeholder="Ask anything about LPU exams..."
            style="flex:1;font-size:12px;padding:9px 12px;border-radius:12px;border:1.5px solid #e5e7eb;
                   outline:none;background:white;color:#111;"
            onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();AcadChat.send();}"
            onfocus="this.style.borderColor='#ec4899'"
            onblur="this.style.borderColor='#e5e7eb'" />
          <button onclick="AcadChat.send()"
            style="width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,#ec4899,#f97316);
                   border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;
                   color:white;flex-shrink:0;transition:transform 0.15s;"
            onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
            <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
            </svg>
          </button>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', html);
    // Show welcome message
    this.addMessage('bot',
      '👋 Hi! I\'m <strong>AcadAssist AI</strong> powered by Gemini.<br><br>' +
      'Ask me anything:<br>' +
      '• Explain a concept for LPU exams<br>' +
      '• Practice MCQs with explanations<br>' +
      '• 5-mark / 10-mark model answers<br>' +
      '• Study schedule & exam strategy<br><br>' +
      'Select your subject above for focused help! 📚'
    );
  },

  toggle() {
    this.isOpen = !this.isOpen;
    const win = document.getElementById('acad-chat-window');
    const iconOpen = document.getElementById('chat-icon-open');
    const iconClose = document.getElementById('chat-icon-close');
    if (this.isOpen) {
      win.style.display = 'flex';
      win.style.flexDirection = 'column';
      if (iconOpen) iconOpen.style.display = 'none';
      if (iconClose) iconClose.style.display = 'block';
      setTimeout(() => document.getElementById('acad-chat-input')?.focus(), 120);
    } else {
      win.style.display = 'none';
      if (iconOpen) iconOpen.style.display = 'block';
      if (iconClose) iconClose.style.display = 'none';
    }
  },

  setSubject(code, name) {
    this.currentSubject = code || null;
    const label = name.includes('—') ? name.split('—')[1].trim() : name;
    this.currentSubjectName = code ? label : null;
    if (code) {
      this.addMessage('bot', `📚 Context set to <strong>${name.trim()}</strong>. Ask me anything about this subject for your LPU exam!`);
    }
  },

  addMessage(role, html) {
    const container = document.getElementById('acad-chat-messages');
    if (!container) return;
    const isBot = role === 'bot';
    // Convert **bold** markdown
    const formatted = html
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br>');
    const wrapper = document.createElement('div');
    wrapper.style.cssText = `display:flex;justify-content:${isBot ? 'flex-start' : 'flex-end'};`;
    wrapper.innerHTML = `
      <div style="max-width:87%;padding:9px 13px;font-size:12px;line-height:1.65;
                  border-radius:${isBot ? '16px 16px 16px 4px' : '16px 16px 4px 16px'};
                  ${isBot
                    ? 'background:#fff;color:#1f2937;border:1px solid rgba(0,0,0,0.08);box-shadow:0 1px 4px rgba(0,0,0,0.06);'
                    : 'background:linear-gradient(135deg,#ec4899,#f97316);color:white;'
                  }">${formatted}</div>
    `;
    container.appendChild(wrapper);
    container.scrollTop = container.scrollHeight;
  },

  addTyping() {
    const container = document.getElementById('acad-chat-messages');
    if (!container) return;
    const div = document.createElement('div');
    div.id = 'acad-typing';
    div.style.cssText = 'display:flex;justify-content:flex-start;';
    div.innerHTML = `<div style="padding:9px 14px;border-radius:16px 16px 16px 4px;background:#fff;border:1px solid rgba(0,0,0,0.08);font-size:12px;color:#9ca3af;">
      <span style="display:inline-flex;gap:3px;align-items:center;">
        <span style="width:6px;height:6px;border-radius:50%;background:#ec4899;animation:acad-bounce 1s infinite 0s;"></span>
        <span style="width:6px;height:6px;border-radius:50%;background:#f97316;animation:acad-bounce 1s infinite 0.2s;"></span>
        <span style="width:6px;height:6px;border-radius:50%;background:#ec4899;animation:acad-bounce 1s infinite 0.4s;"></span>
      </span>
    </div>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;

    // Inject keyframe if not present
    if (!document.getElementById('acad-chat-style')) {
      const style = document.createElement('style');
      style.id = 'acad-chat-style';
      style.textContent = `
        @keyframes acad-bounce {
          0%, 80%, 100% { transform: translateY(0); }
          40% { transform: translateY(-5px); }
        }
      `;
      document.head.appendChild(style);
    }
  },

  removeTyping() {
    document.getElementById('acad-typing')?.remove();
  },

  quickSend(msg) {
    const input = document.getElementById('acad-chat-input');
    if (input) input.value = msg;
    this.send();
  },

  async send() {
    const input = document.getElementById('acad-chat-input');
    const message = input?.value.trim();
    if (!message) return;
    input.value = '';
    this.addMessage('user', message);
    this.history.push({ role: 'user', text: message });
    this.addTyping();
    try {
      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          subject_code: this.currentSubject,
          subject_name: this.currentSubjectName,
          history: this.history.slice(-8)
        })
      });
      const data = await res.json();
      this.removeTyping();
      this.addMessage('bot', data.reply || 'Sorry, no response received.');
      this.history.push({ role: 'model', text: data.reply || '' });
    } catch (e) {
      this.removeTyping();
      this.addMessage('bot', '⚠️ Network error. Please check your connection and try again!');
    }
  }
};

window.AcadChat = AcadChat;
document.addEventListener('DOMContentLoaded', () => AcadChat.init());
