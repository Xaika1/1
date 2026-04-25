from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from sqlalchemy import select
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    db_user = User(email=user_data.email, hash_password=get_password_hash(user_data.password), timezone=user_data.timezone)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {"access_token": create_access_token({"sub": db_user.id}, timedelta(days=7)), "token_type": "bearer"}

@router.post("/token", response_model=Token)
async def login(email: str = Form(...), password: str = Form(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hash_password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    return {"access_token": create_access_token({"sub": user.id}, timedelta(days=7)), "token_type": "bearer"}