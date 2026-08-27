from fastapi import HTTPException
def require_role(*roles):
    def checker(user):
        if user.role not in roles:
            raise HTTPException(403, "Insufficient role")
        return user
    return checker
