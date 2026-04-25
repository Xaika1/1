import httpx
from datetime import datetime
from typing import List, Dict, Optional
from core.db_manager import LocalDB

class SyncEngine:
    def __init__(self, db_path: str, api_url: str):
        self.db_path = db_path
        self.api_url = api_url
        self.token = None
        self.db = LocalDB(db_path)

    def queue_change(self, action: str, payload: Dict):
        with open(self.db_path, "a") as f: pass
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO sync_queue (action, payload, timestamp) VALUES (?, ?, ?)",
                         (action, str(payload), datetime.utcnow().isoformat()))
            conn.commit()

    def pull(self, token: Optional[str] = None):
        self.token = token or self.token
        if not self.token: return
        headers = {"Authorization": f"Bearer {self.token}"}
        last_sync = self.db.get_meta("last_sync") or "1970-01-01T00:00:00"
        try:
            with httpx.Client() as client:
                res = client.get(f"{self.api_url}/sync/delta", headers=headers, params={"since": last_sync})
                if res.status_code == 200:
                    self._apply_server_changes(res.json())
                    self.db.set_meta("last_sync", datetime.utcnow().isoformat())
        except Exception:
            pass

    def push(self, token: Optional[str] = None):
        self.token = token or self.token
        if not self.token: return
        headers = {"Authorization": f"Bearer {token}"}
        queue = self.db.get_queue()
        for q_id, action, payload_str in queue:
            payload = eval(payload_str)
            try:
                res = httpx.post(f"{self.api_url}/sync/push", headers=headers, json={"action": action, "data": payload})
                if res.status_code == 200:
                    self.db.remove_queue_item(q_id)
                elif res.status_code == 409:
                    server_ver = res.json().get("version")
                    self._resolve_conflict(payload["id"], server_ver)
            except Exception:
                pass

    def _apply_server_changes(self, events: List[Dict]):
        with sqlite3.connect(self.db_path) as conn:
            for e in events:
                conn.execute("""INSERT OR REPLACE INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)""",
                             (e["id"], e["calendar_id"], e["title"], e.get("description",""),
                              e["start_time"], e["end_time"], e.get("is_all_day",0),
                              e.get("recurring",0), e.get("recurring_rule",""),
                              e["version"], e.get("color","#4285F4")))
            conn.commit()

    def _resolve_conflict(self, event_id: int, server_version: int):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE events SET version = ? WHERE id = ?", (server_version, event_id))
            conn.commit()

    def get_meta(self, key):
        return self.db.get_meta(key)

    def set_meta(self, key, value):
        self.db.set_meta(key, value)