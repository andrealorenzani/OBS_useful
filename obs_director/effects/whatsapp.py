"""WhatsApp discussion simulator effect.

The server snapshots a saved conversation's messages into the slot along with
a launch timestamp (``started_at_epoch_ms``) and a fixed reveal interval
(``message_interval_ms``, default 1500ms per Deep Dive Q11). Screen clients
(and this module's ``reveal_count`` helper, mirrored in
``static/screen/effects/whatsapp.js``) derive *how many* messages are
currently visible purely from elapsed wall-clock time — never from a
client-accumulated counter — so a reconnecting screen resumes at the correct
point instead of restarting.
"""

from __future__ import annotations

from pydantic import BaseModel

from ..models import WhatsAppConversation, WhatsAppMessageView, WhatsAppSlot
from ..state import ScreenState

DEFAULT_MESSAGE_INTERVAL_MS = 1500


class WhatsAppPlayPayload(BaseModel):
    conversation_id: str


def reveal_count(elapsed_ms: int | float, interval_ms: int, total_messages: int) -> int:
    """How many messages (from the start) should be visible right now.

    ``min(len(messages), floor(elapsed_ms / interval_ms) + 1)`` per the plan,
    clamped so it never goes negative and never exceeds the total.
    """

    if total_messages <= 0:
        return 0
    if interval_ms <= 0:
        return total_messages
    elapsed_ms = max(0, elapsed_ms)
    count = int(elapsed_ms // interval_ms) + 1
    return min(count, total_messages)


def apply_whatsapp_play(
    state: ScreenState,
    conversation: WhatsAppConversation,
    now_ms: int,
    interval_ms: int = DEFAULT_MESSAGE_INTERVAL_MS,
) -> ScreenState:
    ordered = sorted(conversation.messages, key=lambda m: m.order_index)
    messages = [
        WhatsAppMessageView(
            direction=m.direction,
            sender_name=m.sender_name,
            body=m.body,
            timestamp_label=m.timestamp_label,
        )
        for m in ordered
    ]
    state.whatsapp = WhatsAppSlot(
        conversation_id=conversation.id,
        messages=messages,
        started_at_epoch_ms=now_ms,
        message_interval_ms=interval_ms,
    )
    return state


def apply_whatsapp_stop(state: ScreenState) -> ScreenState:
    state.whatsapp = None
    return state
