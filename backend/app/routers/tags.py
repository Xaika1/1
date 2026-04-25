from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Tag, EventTag
from sqlalchemy import select
from app.schemas import TagCreate

router = APIRouter()

@router.get("/", response_model=list)
async def get_tags(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Tag))
    return [{"id": t.id, "name": t.name} for t in res.scalars().all()]

@router.post("/", response_model=dict)
async def create_tag(tag: TagCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Tag).where(Tag.name == tag.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Уже существует")
    new = Tag(name=tag.name)
    db.add(new)
    await db.commit()
    return {"id": new.id}

@router.post("/events/{event_id}/{tag_id}")
async def link_tag(event_id: int, tag_id: int, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(EventTag).where(EventTag.event_id == event_id, EventTag.tag_id == tag_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Уже привязано")
    db.add(EventTag(event_id=event_id, tag_id=tag_id))
    await db.commit()
    return {"status": "привязано"}

@router.delete("/events/{event_id}/{tag_id}")
async def unlink_tag(event_id: int, tag_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(EventTag).where(EventTag.event_id == event_id, EventTag.tag_id == tag_id))
    et = res.scalar_one_or_none()
    if et:
        await db.delete(et)
        await db.commit()
    return {"status": "отвязано"}