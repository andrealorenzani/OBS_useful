// Orchestrator for the `screen` page: owns the WebSocket connection and
// fans out every full-state snapshot to each effect module. Each module
// only looks at its own slice of state and independently drives its own
// enter/exit sequencing — this file does no animation logic itself.
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
