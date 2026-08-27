from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from packages.neelastack.auth.jwt import decode_token
from packages.neelastack.database.session import get_db
from packages.neelastack.database.models import User
security = HTTPBearer()

def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    try:
        user = db.get(User, decode_token(credentials.credentials))
    except Exception as exc:
        raise HTTPException(401, "Invalid token") from exc
    if not user:
        raise HTTPException(401, "User not found")
    return user
