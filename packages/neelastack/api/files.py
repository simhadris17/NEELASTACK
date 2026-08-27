from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from packages.neelastack.auth.dependencies import current_user
from packages.neelastack.database.models import Document
from packages.neelastack.database.session import get_db
from packages.neelastack.security.audit import record_audit

router = APIRouter(prefix="/files", tags=["files"])

ALLOWED_EXTENSIONS = {".txt", ".md", ".json", ".csv", ".py", ".ts", ".tsx"}
MAX_FILE_SIZE = 2 * 1024 * 1024


def _document_response(document: Document) -> dict:
    return {
        "id": document.id,
        "name": document.name,
        "size": len(document.content.encode("utf-8")),
        "preview": document.content[:240],
        "created_at": document.created_at,
    }


@router.get("")
def list_files(
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    documents = db.scalars(
        select(Document)
        .where(Document.user_id == user.id)
        .order_by(Document.id.desc())
    ).all()
    return {"files": [_document_response(document) for document in documents]}


@router.get("/{document_id}")
def get_file(
    document_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    document = db.scalar(select(Document).where(Document.id == document_id, Document.user_id == user.id))
    if document is None:
        raise HTTPException(status_code=404, detail="File not found")
    return {**_document_response(document), "content": document.content}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    name = file.filename or ""
    if len(name) > 255:
        raise HTTPException(status_code=422, detail="Filename must be 255 characters or fewer")
    suffix = "." + name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail="Supported files: TXT, MD, JSON, CSV, PY, TS and TSX",
        )

    content_bytes = await file.read(MAX_FILE_SIZE + 1)
    if len(content_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File exceeds the 2 MB limit")

    try:
        content = content_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=415, detail="File must be UTF-8 text") from exc

    document = Document(user_id=user.id, name=name, content=content)
    db.add(document)
    record_audit(db, "file.uploaded", user.id, "document", document.id, {"name": name})
    db.commit()
    db.refresh(document)
    return _document_response(document)


@router.delete("/{document_id}")
def delete_file(
    document_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    document = db.scalar(
        select(Document).where(
            Document.id == document_id,
            Document.user_id == user.id,
        )
    )
    if document is None:
        raise HTTPException(status_code=404, detail="File not found")
    db.delete(document)
    record_audit(db, "file.deleted", user.id, "document", document_id)
    db.commit()
    return {"deleted": True, "file_id": document_id}
