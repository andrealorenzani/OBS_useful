(function () {
  const form = document.getElementById("speaker-form");
  const list = document.getElementById("speaker-list");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const res = await fetch("/api/speakers", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: data.get("name"),
        description: data.get("description") || null,
      }),
    });
    if (res.ok) {
      window.location.reload();
    } else {
      alert("Could not add speaker.");
    }
  });

  list.addEventListener("click", async (event) => {
    const button = event.target.closest("button[data-action='delete']");
    if (!button) return;
    const li = button.closest("li[data-id]");
    const id = li.dataset.id;
    if (!confirm("Delete this speaker?")) return;
    const res = await fetch(`/api/speakers/${id}`, { method: "DELETE" });
    if (res.ok) {
      window.location.reload();
    } else {
      alert("Could not delete speaker.");
    }
  });
})();
