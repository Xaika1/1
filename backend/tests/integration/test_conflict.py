import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_version_conflict():
    reg = client.post("/auth/register", json={"email": "conflict@test.com", "password": "pass", "timezone": "UTC"})
    token = reg.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    cal = client.post("/calendars/", json={"name": "ConfCal"}, headers=headers)
    cal_id = cal.json()["id"]
    evt = client.post("/events/", json={"calendar_id": cal_id, "title": "V1", "start_time": "2026-05-01T09:00:00Z", "end_time": "2026-05-01T10:00:00Z"}, headers=headers)
    evt_id = evt.json()["id"]
    client.put(f"/events/{evt_id}", json={"title": "V2", "version": 1}, headers=headers)
    res = client.put(f"/events/{evt_id}", json={"title": "V3", "version": 1}, headers=headers)
    assert res.status_code == 409
    assert res.json()["detail"] == "Конфликт версий"