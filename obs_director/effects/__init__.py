"""Effect modules — one per effect family.

Per Deep Dive Q10, there is no generic dynamic dispatcher / registry. Each
module owns its Pydantic action-payload model(s) and pure ``apply_*`` state
mutation function(s); the explicit REST routes in ``obs_director.routers``
import directly from here. This module just re-exports everything for
convenience.
"""

from .alarm import AlarmTriggerPayload, apply_alarm_dismiss, apply_alarm_trigger
from .community_message import (
    PLATFORMS,
    CommunityMessagePayload,
    apply_community_message,
    apply_community_message_clear,
)
from .speaker import (
    SpeakerSelectPayload,
    apply_speaker_clear,
    apply_speaker_select,
    banner_width,
    default_description,
)
from .timer import (
    TimerStartPayload,
    apply_timer_clear,
    apply_timer_pause,
    apply_timer_reset,
    apply_timer_start,
    is_complete,
    value_at,
)
from .whatsapp import (
    WhatsAppPlayPayload,
    apply_whatsapp_play,
    apply_whatsapp_stop,
    reveal_count,
)

__all__ = [
    "AlarmTriggerPayload",
    "apply_alarm_dismiss",
    "apply_alarm_trigger",
    "PLATFORMS",
    "CommunityMessagePayload",
    "apply_community_message",
    "apply_community_message_clear",
    "SpeakerSelectPayload",
    "apply_speaker_clear",
    "apply_speaker_select",
    "banner_width",
    "default_description",
    "TimerStartPayload",
    "apply_timer_clear",
    "apply_timer_pause",
    "apply_timer_reset",
    "apply_timer_start",
    "is_complete",
    "value_at",
    "WhatsAppPlayPayload",
    "apply_whatsapp_play",
    "apply_whatsapp_stop",
    "reveal_count",
]
