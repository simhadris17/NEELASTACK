from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from packages.neelastack.auth.dependencies import current_user
from packages.neelastack.database.models import Document
from packages.neelastack.database.session import get_db

router = APIRouter(prefix="/rag", tags=["rag"])


@router.get("/search")
def search(
    q: str = Query(..., min_length=1, max_length=200),
    db: Session = Depends(get_db),
    user=Depends(current_user),
):
    term = q.strip()
    escaped = term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    documents = db.scalars(
        select(Document)
        .where(
            Document.user_id == user.id,
            or_(
                Document.name.ilike(f"%{escaped}%", escape="\\"),
                Document.content.ilike(f"%{escaped}%", escape="\\"),
            ),
        )
        .order_by(Document.id.desc())
        .limit(20)
    ).all()
    def score(document):
        content = document.content.lower()
        needle = term.lower()
        return content.count(needle) * 3 + document.name.lower().count(needle)

    ranked = sorted(documents, key=score, reverse=True)
    results = []
    for document in ranked:
        content = document.content
        offset = content.lower().find(term.lower())
        start = max(0, offset - 120) if offset >= 0 else 0
        snippet = content[start : start + 500]
        results.append(
            {
                "id": document.id,
                "name": document.name,
                "snippet": snippet,
                "score": score(document),
                "created_at": document.created_at,
            }
        )
    return {
        "query": term,
        "results": results,
    }
