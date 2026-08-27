from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.neelastack.database.session import get_db
from packages.neelastack.database.models import Conversation, Message
from packages.neelastack.auth.dependencies import current_user

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/{conversation_id}/history")
def get_history(
    conversation_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    conversation = db.scalar(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user.id,
        )
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    messages = db.scalars(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.id)
    ).all()

    return {
        "conversation_id": conversation.id,
        "title": conversation.title,
        "messages": [
            {
                "id": message.id,
                "role": message.role,
                "content": message.content,
                "created_at": message.created_at,
            }
            for message in messages
        ],
    }
