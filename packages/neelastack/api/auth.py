from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session
from sqlalchemy import delete, select

from packages.neelastack.database.session import get_db
from packages.neelastack.database.models import (
    Agent,
    AuditEvent,
    Conversation,
    Document,
    Job,
    Memory,
    Project,
    User,
    Workflow,
    WorkflowRun,
    Message,
)
from packages.neelastack.auth import (
    hash_password,
    verify_password,
    create_token,
    decode_token,
)
from packages.neelastack.models.requests import RegisterRequest, LoginRequest
from packages.neelastack.security.audit import record_audit


router = APIRouter(prefix="/auth", tags=["auth"])

bearer = HTTPBearer()


@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
    )

    db.add(user)
    db.flush()
    record_audit(db, "auth.registered", user.id, "user", user.id)
    db.commit()
    db.refresh(user)

    record_audit(db, "auth.logged_in", user.id, "user", user.id)
    db.commit()
    return {
        "access_token": create_token(user.id),
        "token_type": "bearer",
    }


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.scalar(
        select(User).where(User.email == data.email)
    )

    if not user or not verify_password(
        data.password,
        user.password_hash,
    ):
        record_audit(db, "auth.login_failed", None, "user", None, {"email": data.email})
        db.commit()
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    record_audit(db, "auth.logged_in", user.id, "user", user.id)
    db.commit()
    return {
        "access_token": create_token(user.id),
        "token_type": "bearer",
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        user_id = decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user


@router.get("/me")
def me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }


@router.delete("/account")
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_id = current_user.id
    conversation_ids = select(Conversation.id).where(Conversation.user_id == user_id)
    workflow_ids = select(Workflow.id).where(Workflow.user_id == user_id)

    db.execute(delete(Message).where(Message.conversation_id.in_(conversation_ids)))
    db.execute(delete(Conversation).where(Conversation.user_id == user_id))
    db.execute(delete(WorkflowRun).where(WorkflowRun.user_id == user_id))
    db.execute(delete(Workflow).where(Workflow.user_id == user_id))
    for model in (Agent, Document, Job, Memory, Project):
        db.execute(delete(model).where(model.user_id == user_id))
    db.execute(delete(AuditEvent).where(AuditEvent.actor_id == str(user_id)))

    db.delete(current_user)
    db.commit()
    return {"deleted": True}