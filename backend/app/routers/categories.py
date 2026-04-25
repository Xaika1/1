from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Category, EventCategory
from sqlalchemy import select
from app.schemas import CategoryCreate

router = APIRouter()

@router.get("/", response_model=list)
async def get_categories(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Category))
    return [{"id": c.id, "name": c.name} for c in res.scalars().all()]

@router.post("/", response_model=dict)
async def create_category(cat: CategoryCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Category).where(Category.name == cat.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Уже существует")
    new = Category(name=cat.name)
    db.add(new)
    await db.commit()
    return {"id": new.id}

@router.post("/events/{event_id}/{category_id}")
async def link_category(event_id: int, category_id: int, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(EventCategory).where(EventCategory.event_id == event_id, EventCategory.category_id == category_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Уже привязано")
    db.add(EventCategory(event_id=event_id, category_id=category_id))
    await db.commit()
    return {"status": "привязано"}

@router.delete("/events/{event_id}/{category_id}")
async def unlink_category(event_id: int, category_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(EventCategory).where(EventCategory.event_id == event_id, EventCategory.category_id == category_id))
    ec = res.scalar_one_or_none()
    if ec:
        await db.delete(ec)
        await db.commit()
    return {"status": "отвязано"}