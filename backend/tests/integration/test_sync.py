import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import AsyncSessionLocal, engine
from app.models import Base
import asyncio

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db():
    async def init():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(init())
    yield
    async def drop():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    asyncio.run(drop())

def test_sync_flow():
    reg = client.post("/auth/register", json={"email": "sync@test.com", "password": "pass", "timezone": "UTC"})
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    cal = client.post("/calendars/", json={"name": "SyncCal"}, headers=headers)
    cal_id = cal.json()["id"]
    evt = client.post("/events/", json={"calendar_id": cal_id, "title": "SyncTest", "start_time": "2026-04-26T10:00:00Z", "end_time": "2026-04-26T11:00:00Z", "reminders": [15]}, headers=headers)
    evt_id = evt.json()["id"]
    delta = client.get("/sync/delta", headers=headers, params={"since": "1970-01-01T00:00:00"})
    assert len(delta.json()) == 1
    push = client.post("/sync/push", headers=headers, json={"action": "UPDATE", "data": {"id": evt_id, "title": "Synced", "start_time": "2026-04-26T10:00:00Z", "end_time": "2026-04-26T11:00:00Z", "version": 1}})
    assert push.json()["status"] == "обновлено"