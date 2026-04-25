from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.security import get_current_user
from app.models import CalendarEvent, EventReminder, AuditLog
from app.schemas import EventCreate, EventUpdate
from sqlalchemy import select
from datetime import datetime
from dateutil.rrule import rrulestr
from typing import List

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_event(event_data: EventCreate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_event = CalendarEvent(user_id=user.id, **event_data.model_dump(exclude={"reminders", "tags", "categories"}))
    db.add(db_event)
    await db.flush()
    if event_data.reminders:
        for offset in event_data.reminders:
            db.add(EventReminder(event_id=db_event.id, offset_minutes=offset))
    await db.commit()
    await db.refresh(db_event)
    audit = AuditLog(user_id=user.id, action="CREATE", entity="calendar_events", entity_id=db_event.id, payload={"title": db_event.title})
    db.add(audit)
    await db.commit()
    return {"id": db_event.id, "version": db_event.version}

@router.put("/{event_id}")
async def update_event(event_id: int, event_data: EventUpdate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CalendarEvent).where(CalendarEvent.id == event_id, CalendarEvent.user_id == user.id))
    db_event = result.scalar_one_or_none()
    if not db_event:
        raise HTTPException(status_code=404, detail="Не найдено")
    if event_data.version and db_event.version != event_data.version:
        raise HTTPException(status_code=409, detail="Конфликт версий")
    update_data = event_data.model_dump(exclude_unset=True, exclude={"version"})
    for k, v in update_data.items():
        setattr(db_event, k, v)
    db_event.version += 1
    db_event.updated_at = datetime.utcnow()
    await db.commit()
    return {"status": "обновлено", "version": db_event.version}

@router.get("/", response_model=List[dict])
async def get_events(start: str, end: str, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    dt_start = datetime.fromisoformat(start)
    dt_end = datetime.fromisoformat(end)
    result = await db.execute(select(CalendarEvent).where(
        CalendarEvent.user_id == user.id,
        CalendarEvent.start_time <= dt_end,
        CalendarEvent.end_time >= dt_start,
        CalendarEvent.deleted_at.is_(None)
    ))
    events = result.scalars().all()
    response = []
    for e in events:
        if e.recurring and e.recurring_rule:
            try:
                rule = rrulestr(e.recurring_rule, dtstart=e.start_time, ignoretz=True)
                for occ in rule.between(dt_start, dt_end, inc=True):
                    response.append({
                        "id": e.id, "title": e.title, "start_time": occ.isoformat(),
                        "end_time": (occ + (e.end_time - e.start_time)).isoformat(),
                        "calendar_id": e.calendar_id, "version": e.version
                    })
            except Exception:
                response.append({"id": e.id, "title": e.title, "start_time": e.start_time.isoformat(), "end_time": e.end_time.isoformat(), "calendar_id": e.calendar_id, "version": e.version})
        else:
            response.append({"id": e.id, "title": e.title, "start_time": e.start_time.isoformat(), "end_time": e.end_time.isoformat(), "calendar_id": e.calendar_id, "version": e.version})
    return response