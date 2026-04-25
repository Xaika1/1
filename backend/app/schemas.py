from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    timezone: str = "UTC"

class Token(BaseModel):
    access_token: str
    token_type: str

class CalendarCreate(BaseModel):
    name: str
    color_hex: str = "#4285F4"
    is_default: bool = False

class EventCreate(BaseModel):
    calendar_id: int
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    is_all_day: bool = False
    recurring: bool = False
    recurring_rule: Optional[str] = None
    reminders: Optional[List[int]] = []
    tags: Optional[List[int]] = []
    categories: Optional[List[int]] = []

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_all_day: Optional[bool] = None
    recurring: Optional[bool] = None
    recurring_rule: Optional[str] = None
    version: Optional[int] = None

class SyncRequest(BaseModel):
    last_sync_timestamp: datetime
    dirty_events: List[dict] = []

class SyncResponse(BaseModel):
    updated_events: List[dict]
    server_timestamp: datetime

class ParticipantInvite(BaseModel):
    email: str

class ParticipantStatusUpdate(BaseModel):
    status: str

class CategoryCreate(BaseModel):
    name: str

class TagCreate(BaseModel):
    name: str