from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.security import get_current_user
from app.models import Calendar
from app.schemas import CalendarCreate
from sqlalchemy import select

router = APIRouter()

@router.post("/", response_model=dict)
async def create_calendar(cal: CalendarCreate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Calendar).where(Calendar.user_id == user.id, Calendar.name == cal.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Календарь с таким именем уже существует")
    new_cal = Calendar(user_id=user.id, name=cal.name, color_hex=cal.color_hex, is_default=cal.is_default)
    db.add(new_cal)
    await db.commit()
    await db.refresh(new_cal)
    return {"id": new_cal.id, "name": new_cal.name}

@router.get("/", response_model=list)
async def get_calendars(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Calendar).where(Calendar.user_id == user.id))
    return [{"id": c.id, "name": c.name, "color_hex": c.color_hex, "is_default": c.is_default} for c in result.scalars().all()]

@router.put("/{calendar_id}", response_model=dict)
async def update_calendar(calendar_id: int, name: str = None, color: str = None, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Calendar).where(Calendar.id == calendar_id, Calendar.user_id == user.id))
    cal = result.scalar_one_or_none()
    if not cal:
        raise HTTPException(status_code=404, detail="Не найдено")
    if name: cal.name = name
    if color: cal.color_hex = color
    await db.commit()
    return {"status": "обновлено"}

@router.delete("/{calendar_id}")
async def delete_calendar(calendar_id: int, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Calendar).where(Calendar.id == calendar_id, Calendar.user_id == user.id))
    cal = result.scalar_one_or_none()
    if not cal or cal.is_default:
        raise HTTPException(status_code=400, detail="Нельзя удалить календарь по умолчанию")
    await db.delete(cal)
    await db.commit()
    return {"status": "удалено"}