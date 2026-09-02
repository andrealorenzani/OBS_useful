from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel


class MessageResult(BaseModel):
    id: str
    platform: str
    author: str
    avatar_url: str | None = None
    text: str
    timestamp_label: str | None = None


class MessageProvider(ABC):
    @abstractmethod
    def search(self, query: str) -> list[MessageResult]:
        """Search this provider's platform for importable messages."""
        raise NotImplementedError
