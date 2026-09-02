"""Community-message provider search/import path (Deep Dive Q2: no concrete
provider in v1 — always returns an empty result list, without erroring), plus
the global community branding singleton (Deep Dive Q5/Q9: one shared logo +
accent color, configured from the admin prep-page area)."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from .. import storage
from ..models import CommunityBranding
from ..providers import MessageResult, get_provider

router = APIRouter(prefix="/api/community", tags=["community"])


@router.get("/search", response_model=list[MessageResult])
async def search(platform: str, q: str = "") -> list[MessageResult]:
    provider = get_provider(platform)
    return provider.search(q)


class CommunityBrandingUpdate(BaseModel):
    logo_path: str | None = None
    accent_color: str = "#5b8def"


@router.get("/branding", response_model=CommunityBranding)
async def get_branding() -> CommunityBranding:
    return storage.get_community_branding()


@router.put("/branding", response_model=CommunityBranding)
async def update_branding(payload: CommunityBrandingUpdate) -> CommunityBranding:
    return storage.save_community_branding(payload.logo_path, payload.accent_color)
