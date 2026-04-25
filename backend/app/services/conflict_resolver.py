from datetime import datetime
from typing import Dict
from app.models import CalendarEvent
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def resolve_conflict(db: AsyncSession, event_id: int, client_version: int, client_payload: Dict) -> Dict:
    result = await db.execute(select(CalendarEvent).where(CalendarEvent.id == event_id))
    server_event = result.scalar_one_or_none()
    if not server_event:
        return {"status": "не_найдено"}
    if client_version >= server_event.version:
        for k, v in client_payload.items():
            if k in ["id", "version", "updated_at"]: continue
            setattr(server_event, k, v)
        server_event.version += 1
        server_event.updated_at = datetime.utcnow()
        await db.commit()
        return {"status": "обновлено", "version": server_event.version}
    else:
        await db.refresh(server_event)
        return {"status": "конфликт", "version": server_event.version, "data": {
            "id": server_event.id, "title": server_event.title, "start_time": server_event.start_time.isoformat(), "end_time": server_event.end_time.isoformat()
        }}