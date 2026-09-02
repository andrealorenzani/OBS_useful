// WhatsApp discussion simulator — takes over the full screen while active
// (Deep Dive Q8: other effects' regions are simply covered by z-index, their
// state is untouched and they reappear once this region is cleared).
//
// Playback position is always derived from elapsed wall-clock time since
// `started_at_epoch_ms`, never from a client-side counter, so a reconnect
// resumes at the correct point instead of restarting (mirrors
// effects/whatsapp.py::reveal_count).
(function () {
  const region = document.getElementById("whatsapp-region");
  let activeConversationId = null;
  let tickHandle = null;

  function revealCount(elapsedMs, intervalMs, total) {
    if (total <= 0) return 0;
    if (intervalMs <= 0) return total;
    const elapsed = Math.max(0, elapsedMs);
    const count = Math.floor(elapsed / intervalMs) + 1;
    return Math.min(count, total);
  }

  function renderMessages(slot, count) {
    region.innerHTML = "";
    const panel = document.createElement("div");
    panel.className = "whatsapp-panel";

    const list = document.createElement("div");
    list.className = "whatsapp-panel__messages";
    for (let i = 0; i < count; i++) {
      const message = slot.messages[i];
      const bubble = document.createElement("div");
      bubble.className = `whatsapp-message whatsapp-message--${message.direction}`;

      if (message.direction === "left" && message.sender_name) {
        const sender = document.createElement("div");
        sender.className = "whatsapp-message__sender";
        sender.textContent = message.sender_name;
        bubble.appendChild(sender);
      }

      const body = document.createElement("div");
      body.className = "whatsapp-message__body";
      body.textContent = message.body;
      bubble.appendChild(body);

      if (message.direction === "right") {
        const meta = document.createElement("div");
        meta.className = "whatsapp-message__meta";
        meta.textContent = (message.timestamp_label || "") + " ✓✓";
        bubble.appendChild(meta);
      }

      list.appendChild(bubble);
    }
    panel.appendChild(list);
    region.appendChild(panel);

    // Keep the latest message visible for long conversations.
    list.scrollTop = list.scrollHeight;
  }

  function stopTicking() {
    if (tickHandle) {
      clearInterval(tickHandle);
      tickHandle = null;
    }
  }

  function startTicking(slot) {
    stopTicking();
    const total = slot.messages.length;
    function tick() {
      const elapsed = Date.now() - slot.started_at_epoch_ms;
      const count = revealCount(elapsed, slot.message_interval_ms, total);
      renderMessages(slot, count);
      if (count >= total) {
        stopTicking();
      }
    }
    tick();
    tickHandle = setInterval(tick, 200);
  }

  function update(state) {
    const slot = state.whatsapp;
    if (!slot) {
      if (activeConversationId !== null) {
        stopTicking();
        region.innerHTML = "";
        activeConversationId = null;
      }
      return;
    }

    if (slot.conversation_id !== activeConversationId || slot.started_at_epoch_ms !== update._lastStart) {
      activeConversationId = slot.conversation_id;
      update._lastStart = slot.started_at_epoch_ms;
      startTicking(slot);
    }
  }

  window.OBSDirector = window.OBSDirector || {};
  window.OBSDirector.effects = window.OBSDirector.effects || {};
  window.OBSDirector.effects.whatsapp = { update, revealCount };
})();
