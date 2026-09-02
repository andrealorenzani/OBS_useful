(function () {
  const createForm = document.getElementById("conversation-form");
  const list = document.getElementById("conversation-list");

  createForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(createForm);
    const res = await fetch("/api/whatsapp/conversations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: data.get("name") }),
    });
    if (res.ok) {
      window.location.reload();
    } else {
      alert("Could not create conversation.");
    }
  });

  list.addEventListener("click", async (event) => {
    const deleteConvoBtn = event.target.closest("button[data-action='delete-conversation']");
    if (deleteConvoBtn) {
      event.preventDefault();
      const details = deleteConvoBtn.closest("details[data-id]");
      if (!confirm("Delete this conversation?")) return;
      const res = await fetch(`/api/whatsapp/conversations/${details.dataset.id}`, { method: "DELETE" });
      if (res.ok) window.location.reload();
      else alert("Could not delete conversation.");
      return;
    }

    const deleteMsgBtn = event.target.closest("button[data-action='delete-message']");
    if (deleteMsgBtn) {
      const details = deleteMsgBtn.closest("details[data-id]");
      const li = deleteMsgBtn.closest("li[data-id]");
      const res = await fetch(
        `/api/whatsapp/conversations/${details.dataset.id}/messages/${li.dataset.id}`,
        { method: "DELETE" }
      );
      if (res.ok) window.location.reload();
      else alert("Could not delete message.");
    }
  });

  list.addEventListener("submit", async (event) => {
    const form = event.target.closest(".add-message-form");
    if (!form) return;
    event.preventDefault();
    const data = new FormData(form);
    const res = await fetch(`/api/whatsapp/conversations/${form.dataset.conversationId}/messages`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        direction: data.get("direction"),
        sender_name: data.get("sender_name") || null,
        body: data.get("body"),
        timestamp_label: data.get("timestamp_label") || null,
      }),
    });
    if (res.ok) window.location.reload();
    else alert("Could not add message.");
  });
})();
