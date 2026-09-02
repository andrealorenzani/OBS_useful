// Admin-nav "Export presets" / "Import presets" actions (Code changes §4).
// Export is a plain download link (no JS needed beyond the <a href> itself);
// this file only wires up Import, since it needs a file picker + a
// confirmation dialog that explicitly names the live-clearing risk.
(function () {
  const importLink = document.getElementById("presets-import-link");
  const importInput = document.getElementById("presets-import-input");
  if (!importLink || !importInput) return;

  importLink.addEventListener("click", (event) => {
    event.preventDefault();
    importInput.click();
  });

  importInput.addEventListener("change", async () => {
    const file = importInput.files[0];
    importInput.value = "";
    if (!file) return;

    const confirmed = confirm(
      "Importing will replace your speaker roster, conversations, alarm presets, and branding, " +
        "and may clear anything currently live on screen that referenced removed data. " +
        "A backup of your current data will be saved automatically."
    );
    if (!confirmed) return;

    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch("/api/presets/import", { method: "POST", body: formData });
    if (res.ok) {
      alert("Import complete.");
      window.location.reload();
    } else {
      const detail = await res.text();
      alert(`Import failed: ${detail}`);
    }
  });
})();
