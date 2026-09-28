// static/script.js
// Frontend logic for the Digital Marketing FAQ Chatbot.
// Handles sending messages to the Flask backend (/api/chat), rendering
// chat bubbles, the typing indicator, suggested questions, and clearing
// the chat.

(function () {
  "use strict";

  const chatWindow = document.getElementById("chatWindow");
  const userInput = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");
  const typingIndicator = document.getElementById("typingIndicator");
  const suggestions = document.getElementById("suggestions");
  const clearChatBtn = document.getElementById("clearChatBtn");

  const WELCOME_HTML = chatWindow.innerHTML;

  function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  function appendUserMessage(text) {
    const wrapper = document.createElement("div");
    wrapper.className = "message user-message";
    wrapper.innerHTML = `<div class="bubble">${escapeHtml(text)}</div>`;
    chatWindow.appendChild(wrapper);
    scrollToBottom();
  }

  function appendBotMessage(answer, category, similarity) {
    const wrapper = document.createElement("div");
    wrapper.className = "message bot-message";

    let metaLine = "";
    if (category) {
      const pct = Math.round((similarity || 0) * 100);
      metaLine = `<div class="meta-line">Category: ${escapeHtml(category)} &middot; Match confidence: ${pct}%</div>`;
    }

    wrapper.innerHTML = `
      <div class="avatar bot-avatar-sm">DM</div>
      <div class="bubble">${escapeHtml(answer)}${metaLine}</div>
    `;
    chatWindow.appendChild(wrapper);
    scrollToBottom();
  }

  function appendErrorMessage(text) {
    appendBotMessage(text, null, 0);
  }

  function showTyping() {
    typingIndicator.style.display = "flex";
    scrollToBottom();
  }

  function hideTyping() {
    typingIndicator.style.display = "none";
  }

  async function sendMessage(message) {
    const trimmed = message.trim();
    if (!trimmed) return;

    appendUserMessage(trimmed);
    userInput.value = "";
    sendBtn.disabled = true;
    showTyping();

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed }),
      });

      const data = await response.json();

      // Small artificial delay so the typing indicator feels natural,
      // even when the backend responds almost instantly.
      await new Promise((resolve) => setTimeout(resolve, 350));

      hideTyping();

      if (!response.ok) {
        appendErrorMessage(data.error || "Something went wrong. Please try again.");
        return;
      }

      appendBotMessage(data.answer, data.category, data.similarity);
    } catch (err) {
      hideTyping();
      appendErrorMessage(
        "I couldn't reach the server. Please check your connection and try again."
      );
    } finally {
      sendBtn.disabled = false;
      userInput.focus();
    }
  }

  // --- Event listeners -----------------------------------------------

  sendBtn.addEventListener("click", () => sendMessage(userInput.value));

  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage(userInput.value);
    }
  });

  suggestions.addEventListener("click", (e) => {
    const chip = e.target.closest(".suggestion-chip");
    if (!chip) return;
    sendMessage(chip.textContent);
  });

  clearChatBtn.addEventListener("click", () => {
    chatWindow.innerHTML = WELCOME_HTML;
    hideTyping();
    userInput.value = "";
    userInput.focus();
  });

  // Focus the input on load for a smoother first interaction.
  window.addEventListener("load", () => userInput.focus());
})();
