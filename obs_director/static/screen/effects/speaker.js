// Speaker banner effect — two independent per-side slots (Deep Dive Q1).
//
// Sequencing (per side, independently): if a side already shows a speaker
// and the new value differs (by speaker_id) or is cleared, play that side's
// exit animation, wait for it to finish, then play the entrance animation
// for whatever's new. If nothing was showing on that side, entrance plays
// immediately.
//
// Width: whenever either side's occupancy changes, recompute both sides'
// width class — lone occupied side gets `.wide`, both-occupied gets
// `.narrow` — and let CSS transition the width smoothly.
(function () {
  const regions = {
    left: document.getElementById("speaker-left-region"),
    right: document.getElementById("speaker-right-region"),
  };

  const current = { left: null, right: null }; // last rendered slot per side
  const busy = { left: false, right: false }; // mid-exit-animation guard

  function render(side, slot) {
    const region = regions[side];
    region.innerHTML = "";
    if (!slot) return;

    const banner = document.createElement("div");
    banner.className = `speaker-banner speaker-banner--${side} speaker-banner--enter`;

    const name = document.createElement("div");
    name.className = "speaker-banner__name speaker-banner__name--materialize";
    name.textContent = slot.name;
    banner.appendChild(name);

    if (slot.description) {
      const desc = document.createElement("div");
      desc.className = "speaker-banner__description";
      desc.textContent = slot.description;
      banner.appendChild(desc);
    }

    region.appendChild(banner);
  }

  function recomputeWidths() {
    const bothOccupied = !!current.left && !!current.right;
    for (const side of ["left", "right"]) {
      const region = regions[side];
      region.classList.toggle("wide", !bothOccupied && !!current[side]);
      region.classList.toggle("narrow", bothOccupied);
    }
  }

  function applySide(side, newSlot) {
    const previous = current[side];
    const sameSpeaker = previous && newSlot && previous.speaker_id === newSlot.speaker_id;
    if (sameSpeaker) {
      // No visible change on this side.
      return;
    }

    if (!previous) {
      current[side] = newSlot;
      render(side, newSlot);
      recomputeWidths();
      return;
    }

    // Something was showing: play its exit animation before anything else
    // appears on this side.
    busy[side] = true;
    const region = regions[side];
    const outgoing = region.querySelector(".speaker-banner");
    if (outgoing) {
      outgoing.classList.remove("speaker-banner--enter");
      outgoing.classList.add("speaker-banner--exit");
      outgoing.addEventListener(
        "animationend",
        () => {
          current[side] = newSlot;
          render(side, newSlot);
          recomputeWidths();
          busy[side] = false;
        },
        { once: true }
      );
    } else {
      current[side] = newSlot;
      render(side, newSlot);
      recomputeWidths();
      busy[side] = false;
    }
  }

  function update(state) {
    applySide("left", state.speaker_left);
    applySide("right", state.speaker_right);
  }

  window.OBSDirector = window.OBSDirector || {};
  window.OBSDirector.effects = window.OBSDirector.effects || {};
  window.OBSDirector.effects.speaker = { update };
})();
