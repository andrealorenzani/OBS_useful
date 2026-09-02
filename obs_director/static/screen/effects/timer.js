// Timer effect — one generalized "range timer" model, mirrored from
// effects/timer.py::value_at. Server only pushes state on Start/Pause/Reset;
// this module ticks locally every animation frame for smooth display,
// resyncing off anchor_epoch_ms/paused_offset_seconds on every state push
// (so a reload mid-countdown resumes at the correct value).
(function () {
  const regionsByWhich = {
    big: document.getElementById("timer-big-region"),
    corner: document.getElementById("timer-corner-region"),
  };

  const runtime = {
    big: { slot: null, completed: false, raf: null },
    corner: { slot: null, completed: false, raf: null },
  };

  function direction(slot) {
    return slot.end_seconds >= slot.start_seconds ? 1 : -1;
  }

  function valueAt(nowMs, slot) {
    const dir = direction(slot);
    let elapsed;
    if (slot.running) {
      elapsed = slot.paused_offset_seconds + Math.max(0, (nowMs - slot.anchor_epoch_ms) / 1000);
    } else {
      elapsed = slot.paused_offset_seconds;
    }
    let value = slot.start_seconds + dir * elapsed;
    value = dir === 1 ? Math.min(value, slot.end_seconds) : Math.max(value, slot.end_seconds);
    return value;
  }

  function formatSeconds(totalSeconds) {
    const sign = totalSeconds < 0 ? "-" : "";
    const abs = Math.abs(totalSeconds);
    const mins = Math.floor(abs / 60);
    const secs = Math.floor(abs % 60);
    return `${sign}${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
  }

  function ensureElement(which, positionClass) {
    const region = regionsByWhich[which];
    let el = region.querySelector(".timer-display");
    if (!el) {
      region.innerHTML = "";
      el = document.createElement("div");
      el.className = "timer-display";
      region.appendChild(el);
    }
    region.className = `region region--timer-${which} ${positionClass || ""}`.trim();
    return el;
  }

  function tick(which) {
    const rt = runtime[which];
    const slot = rt.slot;
    if (!slot) return;

    const positionClass = which === "corner" ? `pos-${slot.position}` : "";
    const el = ensureElement(which, positionClass);
    const value = valueAt(Date.now(), slot);
    el.textContent = formatSeconds(value);

    const complete = Math.abs(value - slot.end_seconds) < 1e-9;
    if (complete && !rt.completed) {
      rt.completed = true;
      el.classList.add("timer-display--complete");
    } else if (!complete && rt.completed) {
      rt.completed = false;
      el.classList.remove("timer-display--complete");
    }

    rt.raf = requestAnimationFrame(() => tick(which));
  }

  function stopTicking(which) {
    const rt = runtime[which];
    if (rt.raf) {
      cancelAnimationFrame(rt.raf);
      rt.raf = null;
    }
  }

  function updateWhich(which, slot) {
    const rt = runtime[which];
    rt.slot = slot;
    if (!slot) {
      stopTicking(which);
      regionsByWhich[which].innerHTML = "";
      rt.completed = false;
      return;
    }
    rt.completed = false;
    if (!rt.raf) {
      tick(which);
    }
  }

  function update(state) {
    updateWhich("big", state.timer_big);
    updateWhich("corner", state.timer_corner);
  }

  window.OBSDirector = window.OBSDirector || {};
  window.OBSDirector.effects = window.OBSDirector.effects || {};
  window.OBSDirector.effects.timer = { update, valueAt, formatSeconds };
})();
