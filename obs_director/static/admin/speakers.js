(function () {
  const form = document.getElementById("speaker-form");
  const list = document.getElementById("speaker-list");
  const brandingForm = document.getElementById("community-branding-form");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const res = await fetch("/api/speakers", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: data.get("name"),
        description: data.get("description") || null,
        banner_style: data.get("banner_style") || "classic",
        image_path: data.get("image_path") || null,
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

  if (brandingForm) {
    brandingForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const data = new FormData(brandingForm);
      const res = await fetch("/api/community/branding", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          logo_path: data.get("logo_path") || null,
          accent_color: data.get("accent_color") || "#5b8def",
        }),
      });
      if (res.ok) {
        window.location.reload();
      } else {
        alert("Could not save branding.");
      }
    });
  }
})();
