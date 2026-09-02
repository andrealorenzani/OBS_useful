(function () {
  const form = document.getElementById("alarm-preset-form");
  const list = document.getElementById("alarm-preset-list");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const res = await fetch("/api/alarm-presets", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ label: data.get("label") }),
    });
    if (res.ok) window.location.reload();
    else alert("Could not save preset.");
  });

  list.addEventListener("click", async (event) => {
    const button = event.target.closest("button[data-action='delete']");
    if (!button) return;
    const li = button.closest("li[data-id]");
    const res = await fetch(`/api/alarm-presets/${li.dataset.id}`, { method: "DELETE" });
    if (res.ok) window.location.reload();
    else alert("Could not delete preset.");
  });
})();
