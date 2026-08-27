from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.neelastack.auth.dependencies import current_user
from packages.neelastack.database.models import Conversation, Message
from packages.neelastack.database.session import get_db
from packages.neelastack.models.requests import ChatRequest
from packages.neelastack.providers.router import get_provider_with_fallback
from packages.neelastack.security.audit import record_audit

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


def _greeting_response(message: str) -> str | None:
    normalized = " ".join(message.lower().strip().rstrip("!?.,").split())
    greetings = {
        "hi",
        "hello",
        "hey",
        "hi neelastack",
        "hello neelastack",
        "hey neelastack",
        "good morning",
        "good afternoon",
        "good evening",
    }
    if normalized in greetings:
        return "Hi! How can I help you today?"
    return None


@router.post("")
async def chat(
    data: ChatRequest,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    if data.conversation_id:
        conv = db.scalar(
            select(Conversation).where(
                Conversation.id == data.conversation_id,
                Conversation.user_id == user.id,
            )
        )

        if conv is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found",
            )
    else:
        conv = Conversation(
            user_id=user.id,
            title=data.message[:50],
        )
        db.add(conv)
        db.commit()
        db.refresh(conv)

    db.add(
        Message(
            conversation_id=conv.id,
            role="user",
            content=data.message,
        )
    )
    db.commit()

    try:
        answer = _greeting_response(data.message)
        if answer is None:
            answer = await get_provider_with_fallback().generate(
                f"""You are NEELASTACK, a senior coding assistant. Answer like Claude and
solve the request directly without asking unnecessary clarification questions.
Give the response step by step:
1. Briefly explain the solution and assumptions.
2. Show the plan or project structure.
3. Provide complete runnable code in fenced code blocks when code is requested.
4. Give exact install, run, build, and test commands.
5. End with a short verification checklist.
Never use TODO, FIXME, placeholders, pseudo-code, unexplained ellipses, or
truncated files. Keep the explanation clear and practical.

User request:
{data.message}"""
            )
    except Exception as exc:
        record_audit(db, "chat.failed", user.id, "conversation", conv.id, {"error": str(exc)[:500]})
        db.commit()
        raise HTTPException(status_code=503, detail="No configured model provider is available") from exc

    db.add(
        Message(
            conversation_id=conv.id,
            role="assistant",
            content=answer,
        )
    )
    record_audit(db, "chat.completed", user.id, "conversation", conv.id)
    db.commit()

    return {
        "conversation_id": conv.id,
        "answer": answer,
    }
