from datetime import datetime, timedelta, timezone
from jose import jwt
from packages.neelastack.core.config import settings
ALGORITHM = "HS256"
def create_token(user_id: int) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    return jwt.encode({"sub": str(user_id), "exp": exp}, settings.secret_key, algorithm=ALGORITHM)
def decode_token(token: str) -> int:
    return int(jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])["sub"])
