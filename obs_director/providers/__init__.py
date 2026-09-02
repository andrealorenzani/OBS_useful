"""Community-message import providers.

Per Deep Dive Q2, v1 ships no concrete platform provider — ``get_provider``
always returns the no-op provider, whose ``search`` returns an empty list.
The abstraction exists so a real platform integration can be plugged in
later without reworking the community-message rendering path.
"""

from .base import MessageProvider, MessageResult
from .manual import NoOpProvider

_NO_OP = NoOpProvider()


def get_provider(platform: str) -> MessageProvider:
    # No concrete provider is wired up in v1 for any platform.
    return _NO_OP


__all__ = ["MessageProvider", "MessageResult", "NoOpProvider", "get_provider"]
