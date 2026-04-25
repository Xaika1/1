from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMPTZ
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(60), unique=True, nullable=False)
    hash_password = Column(String(256), nullable=False)
    timezone = Column(String(50), default="UTC")
    created_at = Column(TIMESTAMPTZ, server_default="NOW()")
    calendars = relationship("Calendar", back_populates="user")
    events = relationship("CalendarEvent", back_populates="user")

class Calendar(Base):
    __tablename__ = "calendars"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(50), nullable=False)
    color_hex = Column(String(7), default="#4285F4")
    is_default = Column(Boolean, default=False)
    created_at = Column(TIMESTAMPTZ, server_default="NOW()")
    user = relationship("User", back_populates="calendars")
    events = relationship("CalendarEvent", back_populates="calendar")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(TIMESTAMPTZ, server_default="NOW()")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(TIMESTAMPTZ, server_default="NOW()")

class CalendarEvent(Base):
    __tablename__ = "calendar_events"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    calendar_id = Column(Integer, ForeignKey("calendars.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    start_time = Column(TIMESTAMPTZ, nullable=False)
    end_time = Column(TIMESTAMPTZ, nullable=False)
    is_all_day = Column(Boolean, default=False)
    recurring = Column(Boolean, default=False)
    recurring_rule = Column(Text)
    version = Column(Integer, default=1)
    created_at = Column(TIMESTAMPTZ, server_default="NOW()")
    updated_at = Column(TIMESTAMPTZ, server_default="NOW()")
    deleted_at = Column(TIMESTAMPTZ)
    user = relationship("User", back_populates="events")
    calendar = relationship("Calendar", back_populates="events")
    reminders = relationship("EventReminder", back_populates="event", cascade="all, delete-orphan")
    exdates = relationship("EventExdate", back_populates="event", cascade="all, delete-orphan")
    participants = relationship("EventParticipant", back_populates="event", cascade="all, delete-orphan")
    categories = relationship("EventCategory", back_populates="event", cascade="all, delete-orphan")
    tags = relationship("EventTag", back_populates="event", cascade="all, delete-orphan")

class EventReminder(Base):
    __tablename__ = "event_reminders"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("calendar_events.id", ondelete="CASCADE"), nullable=False)
    offset_minutes = Column(Integer, nullable=False)
    method = Column(String(20), default="local")
    event = relationship("CalendarEvent", back_populates="reminders")

class EventExdate(Base):
    __tablename__ = "event_exdates"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("calendar_events.id", ondelete="CASCADE"), nullable=False)
    exdate = Column(TIMESTAMPTZ, nullable=False)
    event = relationship("CalendarEvent", back_populates="exdates")
    __table_args__ = (UniqueConstraint("event_id", "exdate"),)

class EventParticipant(Base):
    __tablename__ = "event_participants"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("calendar_events.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), default="invitee")
    status = Column(String(20), default="pending")
    event = relationship("CalendarEvent", back_populates="participants")
    __table_args__ = (UniqueConstraint("event_id", "user_id"),)

class EventCategory(Base):
    __tablename__ = "event_categories"
    event_id = Column(Integer, ForeignKey("calendar_events.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True)
    event = relationship("CalendarEvent", back_populates="categories")
    category = relationship("Category")

class EventTag(Base):
    __tablename__ = "event_tags"
    event_id = Column(Integer, ForeignKey("calendar_events.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    event = relationship("CalendarEvent", back_populates="tags")
    tag = relationship("Tag")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    action = Column(String(50), nullable=False)
    entity = Column(String(50), nullable=False)
    entity_id = Column(Integer)
    payload = Column(Text)
    created_at = Column(TIMESTAMPTZ, server_default="NOW()")