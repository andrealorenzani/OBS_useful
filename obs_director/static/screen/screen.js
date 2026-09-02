// Orchestrator for the `screen` page: owns the WebSocket connection and
// fans out every full-state snapshot to each effect module. Each module
// only looks at its own slice of state and independently drives its own
// enter/exit sequencing — this file does no animation logic itself.
//
// Documented exception (Code changes §2b): `effects.speaker.update(state)`
// also reads `state.community_message` (not just its own speaker_left/right
// slice) purely to toggle a client-side opacity fade while a community
// message is showing — mirroring the WhatsApp full-takeover
// preserve-but-cover pattern, just scoped to the speaker regions instead of
// the whole screen. No server-side state is touched by this.
(function () {
  function applyState(state) {
    const effects = window.OBSDirector.effects;
    effects.speaker.update(state);
    effects.communityMessage.update(state);
    effects.whatsapp.update(state);
    effects.timer.update(state);
    effects.alarm.update(state);
  }

  window.OBSDirector.connectScreenSocket(applyState);
})();
