// Community message effect — one slot, same animate-out-then-in sequencing
// as the speaker banner (Deep Dive Q7). Both authoring paths (search-import,
// free-text+style) converge on the same CommunityMessageSlot shape, so there
// is only one render path here, with a `.platform-*` CSS modifier class for
// the "styled like that platform" look.
(function () {
  const region = document.getElementById("community-message-region");
  let current = null;
  let busy = false;

  function render(slot) {
    region.innerHTML = "";
    if (!slot) return;

    const card = document.createElement("div");
    card.className = `community-card platform-${slot.platform} community-card--enter`;

    const header = document.createElement("div");
    header.className = "community-card__header";
    header.textContent = slot.author;
    card.appendChild(header);

    const body = document.createElement("div");
    body.className = "community-card__body";
    body.textContent = slot.text;
    card.appendChild(body);

    region.appendChild(card);
  }

  function sameMessage(a, b) {
    if (!a || !b) return false;
    return a.platform === b.platform && a.text === b.text && a.author === b.author;
  }

  function update(state) {
    const newSlot = state.community_message;
    if (sameMessage(current, newSlot)) return;

    if (!current) {
      current = newSlot;
      render(newSlot);
      return;
    }

    busy = true;
    const outgoing = region.querySelector(".community-card");
    if (outgoing) {
      outgoing.classList.remove("community-card--enter");
      outgoing.classList.add("community-card--exit");
      outgoing.addEventListener(
        "animationend",
        () => {
          current = newSlot;
          render(newSlot);
          busy = false;
        },
        { once: true }
      );
    } else {
      current = newSlot;
      render(newSlot);
      busy = false;
    }
  }

  window.OBSDirector = window.OBSDirector || {};
  window.OBSDirector.effects = window.OBSDirector.effects || {};
  window.OBSDirector.effects.communityMessage = { update };
})();
