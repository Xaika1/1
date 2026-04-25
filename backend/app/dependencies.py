from fastapi import Request
from app.core.security import get_current_user

async def get_user_from_header(request: Request):
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return None
    try:
        return await get_current_user(token.replace("Bearer ", ""))
    except Exception:
        return None