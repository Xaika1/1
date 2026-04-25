from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.security import get_current_user
from app.models import CalendarEvent
from app.services.conflict_resolver import resolve_conflict
from app.schemas import SyncRequest, SyncResponse
from sqlalchemy import select
from datetime import datetime

router = APIRouter()

@router.get("/delta", response_model=dict)
async def sync_delta(since: str, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    dt_since = datetime.fromisoformat(since)
    result = await db.execute(select(CalendarEvent).where(
        CalendarEvent.user_id == user.id,
        CalendarEvent.updated_at > dt_since,
        CalendarEvent.deleted_at.is_(None)
    ))
    events = result.scalars().all()
    return [{"id": e.id, "title": e.title, "start_time": e.start_time.isoformat(), "end_time": e.end_time.isoformat(), "calendar_id": e.calendar_id, "version": e.version} for e in events]

@router.post("/push", response_model=dict)
async def sync_push(request: dict, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    action = request.get("action")
    data = request.get("data", {})
    event_id = data.get("id")
    if action == "UPDATE":
        return await resolve_conflict(db, event_id, data.get("version", 0), data)
    elif action == "CREATE":
        new_event = CalendarEvent(user_id=user.id, **data)
        db.add(new_event)
        await db.commit()
        await db.refresh(new_event)
        return {"status": "создано", "id": new_event.id}
    elif action == "DELETE":
        result = await db.execute(select(CalendarEvent).where(CalendarEvent.id == event_id, CalendarEvent.user_id == user.id))
        evt = result.scalar_one_or_none()
        if evt:
            evt.deleted_at = datetime.utcnow()
            evt.version += 1
            await db.commit()
        return {"status": "удалено"}
    raise HTTPException(status_code=400, detail="Неверное действие")