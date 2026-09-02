from __future__ import annotations

from .base import MessageProvider, MessageResult


class NoOpProvider(MessageProvider):
    """v1 stand-in for a real social-platform provider (Deep Dive Q2).

    Always returns no results; the free-text + platform-style path is the
    fully functional way to post a community message in v1.
    """

    def search(self, query: str) -> list[MessageResult]:
        return []
