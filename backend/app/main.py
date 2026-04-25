from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, AsyncSessionLocal
from app.routers import auth, events, calendars, sync, participants, categories, tags
from app.middleware.exceptions import register_handlers
from app.models import AuditLog
from datetime import datetime
import os

app = FastAPI()
register_handlers(app)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    os.makedirs("logs", exist_ok=True)
    from app.core.logging_config import init_logging
    init_logging()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    duration = (datetime.utcnow() - start_time).total_seconds()
    if "/auth/" not in request.url.path:
        async with AsyncSessionLocal() as session:
            audit = AuditLog(
                user_id=getattr(request.state, "user_id", None),
                action=request.method,
                entity=request.url.path.split("/")[1] if len(request.url.path) > 1 else "unknown",
                entity_id=0,
                payload={"path": request.url.path, "duration": duration, "status": response.status_code}
            )
            session.add(audit)
            await session.commit()
    return response

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(calendars.router, prefix="/calendars", tags=["calendars"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(sync.router, prefix="/sync", tags=["sync"])
app.include_router(participants.router, prefix="/participants", tags=["participants"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])