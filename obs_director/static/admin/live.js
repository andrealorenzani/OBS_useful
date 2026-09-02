// The single live-control page's client logic: every action here is a
// plain fetch() POST/DELETE to /api/live/... — no navigation required.
(function () {
  async function post(url, body) {
    const res = await fetch(url, {
      method: "POST",
      headers: body ? { "Content-Type": "application/json" } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) {
      const detail = await res.text();
      alert(`Action failed: ${detail}`);
    }
  }

  async function del(url) {
    const res = await fetch(url, { method: "DELETE" });
    if (!res.ok) {
      const detail = await res.text();
      alert(`Action failed: ${detail}`);
    }
  }

  // --- Speaker ---------------------------------------------------------

  document.querySelectorAll("button[data-action='speaker-show']").forEach((btn) => {
    btn.addEventListener("click", () => {
      const side = btn.dataset.side;
      const block = document.querySelector(`.live-block[data-side='${side}']`);
      const select = block.querySelector("select[data-role='speaker-select']");
      if (!select.value) {
        alert("Choose a speaker first.");
        return;
      }
      post(`/api/live/speaker/${side}`, { speaker_id: select.value });
    });
  });

  document.querySelectorAll("button[data-action='speaker-clear']").forEach((btn) => {
    btn.addEventListener("click", () => del(`/api/live/speaker/${btn.dataset.side}`));
  });

  // --- Community message -------------------------------------------------

  document.getElementById("community-search-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(event.target);
    const params = new URLSearchParams({ platform: data.get("platform"), q: data.get("q") || "" });
    const res = await fetch(`/api/community/search?${params}`);
    const results = await res.json();
    const container = document.getElementById("community-search-results");
    container.textContent = results.length
      ? `${results.length} result(s)`
      : "No results (v1 ships no live provider — use the compose form below).";
  });

  document.getElementById("community-custom-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(event.target);
    const text = (data.get("text") || "").toString().trim();
    if (!text) {
      alert("Message text is required.");
      return;
    }
    await post("/api/live/community-message", {
      platform: data.get("platform"),
      text,
      author: data.get("author") || "You",
    });
  });

  document.querySelector("button[data-action='community-clear']").addEventListener("click", () => {
    del("/api/live/community-message");
  });

  // --- WhatsApp ------------------------------------------------------------

  document.querySelector("button[data-action='whatsapp-play']").addEventListener("click", () => {
    const select = document.getElementById("whatsapp-conversation-select");
    if (!select.value) {
      alert("Choose a conversation first.");
      return;
    }
    post("/api/live/whatsapp/play", { conversation_id: select.value });
  });

  document.querySelector("button[data-action='whatsapp-stop']").addEventListener("click", () => {
    post("/api/live/whatsapp/stop");
  });

  // --- Timers ----------------------------------------------------------------

  document.querySelectorAll("button[data-action='timer-start']").forEach((btn) => {
    btn.addEventListener("click", () => {
      const which = btn.dataset.timer;
      const block = document.querySelector(`.live-block[data-timer='${which}']`);
      const start = parseFloat(block.querySelector("[data-role='timer-start']").value);
      const end = parseFloat(block.querySelector("[data-role='timer-end']").value);
      const positionEl = block.querySelector("[data-role='timer-position']");
      const position = positionEl ? positionEl.value : "center";
      post(`/api/live/timer/${which}/start`, { start_seconds: start, end_seconds: end, position });
    });
  });

  document.querySelectorAll("button[data-action='timer-pause']").forEach((btn) => {
    btn.addEventListener("click", () => post(`/api/live/timer/${btn.dataset.timer}/pause`));
  });

  document.querySelectorAll("button[data-action='timer-reset']").forEach((btn) => {
    btn.addEventListener("click", () => post(`/api/live/timer/${btn.dataset.timer}/reset`));
  });

  document.querySelectorAll("button[data-action='timer-clear']").forEach((btn) => {
    btn.addEventListener("click", () => del(`/api/live/timer/${btn.dataset.timer}`));
  });

  // --- Alarm -----------------------------------------------------------------

  document.querySelector("button[data-action='alarm-trigger']").addEventListener("click", () => {
    const presetSelect = document.getElementById("alarm-preset-select");
    const customLabel = document.getElementById("alarm-custom-label").value.trim();
    const position = document.getElementById("alarm-position").value;
    const label = customLabel || presetSelect.value || null;
    post("/api/live/alarm/trigger", { label, position });
  });

  document.querySelector("button[data-action='alarm-dismiss']").addEventListener("click", () => {
    post("/api/live/alarm/dismiss");
  });
})();
