// Big red alarm effect — bold looping pulse + real siren audio (Deep Dive Q3).
//
// Audio is a synthesized Web Audio oscillator sweep (no bundled asset file
// needed). Playback is started/stopped keyed off the alarm slot appearing/
// disappearing in state, which is closer to a real operator-triggered event
// than page load, helping with browser autoplay-restriction policies. OBS's
// embedded Browser Source should have its audio track captured for the
// siren to be heard in the recording/stream — see docs/architecture.md.
(function () {
  const region = document.getElementById("alarm-region");
  let active = false;
  let audioCtx = null;
  let oscillator = null;
  let gainNode = null;
  let sweepInterval = null;

  function startSiren() {
    try {
      audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
      if (audioCtx.state === "suspended") {
        audioCtx.resume().catch(() => {});
      }
      oscillator = audioCtx.createOscillator();
      gainNode = audioCtx.createGain();
      oscillator.type = "sawtooth";
      gainNode.gain.value = 0.15;
      oscillator.connect(gainNode);
      gainNode.connect(audioCtx.destination);
      oscillator.start();

      let low = true;
      sweepInterval = setInterval(() => {
        const freq = low ? 880 : 660;
        oscillator.frequency.setTargetAtTime(freq, audioCtx.currentTime, 0.05);
        low = !low;
      }, 400);
    } catch (err) {
      // Autoplay-restricted or unsupported browser; visual alarm still
      // works. See docs/architecture.md for the manual-unlock workaround.
      console.warn("obs_director: siren audio could not start", err);
    }
  }

  function stopSiren() {
    if (sweepInterval) {
      clearInterval(sweepInterval);
      sweepInterval = null;
    }
    if (oscillator) {
      try {
        oscillator.stop();
      } catch (err) {
        /* already stopped */
      }
      oscillator.disconnect();
      oscillator = null;
    }
    if (gainNode) {
      gainNode.disconnect();
      gainNode = null;
    }
  }

  function render(slot) {
    region.innerHTML = "";
    region.className = `region region--alarm region--alarm-${slot.position}`;
    const banner = document.createElement("div");
    banner.className = `alarm-banner alarm-banner--${slot.position}`;
    banner.textContent = slot.label || "ALERT";
    region.appendChild(banner);
  }

  function update(state) {
    const slot = state.alarm;
    if (slot && !active) {
      active = true;
      render(slot);
      startSiren();
    } else if (slot && active) {
      // Idempotent: re-triggering while already active does not duplicate
      // the banner or restart overlapping audio.
      render(slot);
    } else if (!slot && active) {
      active = false;
      region.innerHTML = "";
      stopSiren();
    }
  }

  window.OBSDirector = window.OBSDirector || {};
  window.OBSDirector.effects = window.OBSDirector.effects || {};
  window.OBSDirector.effects.alarm = { update };
})();
