import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_recurring_expansion():
    reg = client.post("/auth/register", json={"email": "recur@test.com", "password": "pass", "timezone": "UTC"})
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    cal = client.post("/calendars/", json={"name": "RecCal"}, headers=headers)
    cal_id = cal.json()["id"]
    evt = client.post("/events/", json={"calendar_id": cal_id, "title": "Weekly", "start_time": "2026-04-27T09:00:00Z", "end_time": "2026-04-27T10:00:00Z", "recurring": True, "recurring_rule": "FREQ=WEEKLY;COUNT=3"}, headers=headers)
    events = client.get("/events/", headers=headers, params={"start": "2026-04-01T00:00:00Z", "end": "2026-06-01T00:00:00Z"})
    assert len(events.json()) == 3