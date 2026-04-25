from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.security import get_current_user
from app.models import EventParticipant, User
from sqlalchemy import select
from app.schemas import ParticipantInvite, ParticipantStatusUpdate

router = APIRouter()

@router.get("/{event_id}/participants")
async def get_participants(event_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(EventParticipant).where(EventParticipant.event_id == event_id))
    parts = result.scalars().all()
    return [{"user_id": p.user_id, "role": p.role, "status": p.status} for p in parts]

@router.post("/{event_id}/participants")
async def invite_participant(event_id: int, payload: ParticipantInvite, db: AsyncSession = Depends(get_db)):
    user_res = await db.execute(select(User).where(User.email == payload.email))
    target = user_res.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    exist = await db.execute(select(EventParticipant).where(EventParticipant.event_id == event_id, EventParticipant.user_id == target.id))
    if exist.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Уже приглашён")
    db.add(EventParticipant(event_id=event_id, user_id=target.id, role="invitee", status="pending"))
    await db.commit()
    return {"status": "приглашён"}

@router.put("/{event_id}/participants/{user_id}/status")
async def update_participant_status(event_id: int, user_id: int, payload: ParticipantStatusUpdate, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Запрещено")
    res = await db.execute(select(EventParticipant).where(EventParticipant.event_id == event_id, EventParticipant.user_id == user_id))
    participant = res.scalar_one_or_none()
    if not participant:
        raise HTTPException(status_code=404, detail="Не найдено")
    if payload.status not in ["accepted", "declined", "pending"]:
        raise HTTPException(status_code=400, detail="Неверный статус")
    participant.status = payload.status
    await db.commit()
    return {"status": "обновлено"}

@router.delete("/{event_id}/participants/{user_id}")
async def remove_participant(event_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(EventParticipant).where(EventParticipant.event_id == event_id, EventParticipant.user_id == user_id))
    p = res.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Не найдено")
    await db.delete(p)
    await db.commit()
    return {"status": "удалён"}