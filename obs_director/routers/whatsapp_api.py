"""WhatsApp conversation authoring CRUD (prep).

Deviation note: message-level routes are nested under their conversation
(``/api/whatsapp/conversations/{conversation_id}/messages/{message_id}``)
rather than the plan's flatter ``/api/whatsapp/messages/{id}`` sketch, since
messages are stored nested inside their conversation's JSON record with no
separate global index — see the implementation report for details.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .. import storage
from ..models import MessageDirection, WhatsAppConversation

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])


class ConversationCreate(BaseModel):
    name: str


class MessageCreate(BaseModel):
    direction: MessageDirection
    sender_name: str | None = None
    body: str
    timestamp_label: str | None = None


class ReorderPayload(BaseModel):
    message_ids: list[str]


@router.get("/conversations", response_model=list[WhatsAppConversation])
async def list_conversations() -> list[WhatsAppConversation]:
    return storage.list_conversations()


@router.post("/conversations", response_model=WhatsAppConversation, status_code=201)
async def create_conversation(payload: ConversationCreate) -> WhatsAppConversation:
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="name is required")
    return storage.create_conversation(name)


@router.get("/conversations/{conversation_id}", response_model=WhatsAppConversation)
async def get_conversation(conversation_id: str) -> WhatsAppConversation:
    convo = storage.get_conversation(conversation_id)
    if convo is None:
        raise HTTPException(status_code=404, detail="conversation not found")
    return convo


@router.put("/conversations/{conversation_id}", response_model=WhatsAppConversation)
async def rename_conversation(conversation_id: str, payload: ConversationCreate) -> WhatsAppConversation:
    name = payload.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="name is required")
    convo = storage.rename_conversation(conversation_id, name)
    if convo is None:
        raise HTTPException(status_code=404, detail="conversation not found")
    return convo


@router.delete("/conversations/{conversation_id}", status_code=204)
async def delete_conversation(conversation_id: str) -> None:
    ok = storage.delete_conversation(conversation_id)
    if not ok:
        raise HTTPException(status_code=404, detail="conversation not found")


@router.post("/conversations/{conversation_id}/messages", response_model=WhatsAppConversation, status_code=201)
async def add_message(conversation_id: str, payload: MessageCreate) -> WhatsAppConversation:
    body = payload.body.strip()
    if not body:
        raise HTTPException(status_code=400, detail="body is required")
    convo = storage.add_message(
        conversation_id, payload.direction, payload.sender_name, body, payload.timestamp_label
    )
    if convo is None:
        raise HTTPException(status_code=404, detail="conversation not found")
    return convo


@router.put("/conversations/{conversation_id}/messages/{message_id}", response_model=WhatsAppConversation)
async def update_message(conversation_id: str, message_id: str, payload: MessageCreate) -> WhatsAppConversation:
    body = payload.body.strip()
    if not body:
        raise HTTPException(status_code=400, detail="body is required")
    convo = storage.update_message(
        conversation_id, message_id, payload.direction, payload.sender_name, body, payload.timestamp_label
    )
    if convo is None:
        raise HTTPException(status_code=404, detail="conversation or message not found")
    return convo


@router.delete("/conversations/{conversation_id}/messages/{message_id}", response_model=WhatsAppConversation)
async def delete_message(conversation_id: str, message_id: str) -> WhatsAppConversation:
    convo = storage.delete_message(conversation_id, message_id)
    if convo is None:
        raise HTTPException(status_code=404, detail="conversation or message not found")
    return convo


@router.post("/conversations/{conversation_id}/reorder", response_model=WhatsAppConversation)
async def reorder_messages(conversation_id: str, payload: ReorderPayload) -> WhatsAppConversation:
    convo = storage.reorder_messages(conversation_id, payload.message_ids)
    if convo is None:
        raise HTTPException(status_code=404, detail="conversation not found or message_ids mismatch")
    return convo
