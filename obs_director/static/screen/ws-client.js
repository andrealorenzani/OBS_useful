// Shared WebSocket client for the `screen` page. Connects to /ws/screen,
// reconnects with a short backoff on drop (so an OBS Browser Source refresh
// or a transient network blip recovers on its own), and hands every full
// state snapshot to the provided callback.
(function () {
  function connectScreenSocket(onState) {
    const proto = window.location.protocol === "https:" ? "wss" : "ws";
    const url = `${proto}://${window.location.host}/ws/screen`;

    function open() {
      const socket = new WebSocket(url);
      socket.addEventListener("message", (event) => {
        try {
          const state = JSON.parse(event.data);
          onState(state);
        } catch (err) {
          console.error("obs_director: failed to parse state message", err);
        }
      });
      socket.addEventListener("close", () => {
        setTimeout(open, 1000);
      });
      socket.addEventListener("error", () => {
        socket.close();
      });
    }

    open();
  }

  window.OBSDirector = window.OBSDirector || {};
  window.OBSDirector.connectScreenSocket = connectScreenSocket;
})();
