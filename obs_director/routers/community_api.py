"""Community-message provider search/import path (Deep Dive Q2: no concrete
provider in v1 — always returns an empty result list, without erroring)."""

from __future__ import annotations

from fastapi import APIRouter

from ..providers import MessageResult, get_provider

router = APIRouter(prefix="/api/community", tags=["community"])


@router.get("/search", response_model=list[MessageResult])
async def search(platform: str, q: str = "") -> list[MessageResult]:
    provider = get_provider(platform)
    return provider.search(q)
