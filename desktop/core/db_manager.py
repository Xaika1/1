import sqlite3
import os
from datetime import datetime

class LocalDB:
    def __init__(self, path):
        self.db_path = path
        self._init()

    def _init(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY, calendar_id INTEGER, title TEXT, description TEXT,
                start_time TEXT, end_time TEXT, is_all_day INTEGER, recurring INTEGER,
                recurring_rule TEXT, version INTEGER, is_dirty INTEGER DEFAULT 0, color TEXT)""")
            conn.execute("CREATE TABLE IF NOT EXISTS sync_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT, action TEXT, payload TEXT, timestamp TEXT)")
            conn.execute("CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT)")
            conn.commit()

    def get_events(self, calendar_id, start, end):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("""SELECT id, calendar_id, title, description, start_time, end_time, is_all_day, recurring, recurring_rule, version, is_dirty, color
                FROM events WHERE calendar_id = ? AND start_time <= ? AND end_time >= ? ORDER BY start_time""",
                (calendar_id, end.isoformat(), start.isoformat()))
            return cur.fetchall()

    def save_event(self, data):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""INSERT OR REPLACE INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)""",
                (data["id"], data["calendar_id"], data["title"], data.get("description",""),
                 data["start_time"], data["end_time"], data.get("is_all_day",0),
                 data.get("recurring",0), data.get("recurring_rule",""),
                 data.get("version",1), data.get("color","#4285F4")))
            conn.commit()

    def get_dirty(self):
        with sqlite3.connect(self.db_path) as conn:
            return [{"id": r[0], "calendar_id": r[1], "title": r[2], "description": r[3],
                     "start_time": r[4], "end_time": r[5], "is_all_day": r[6],
                     "recurring": r[7], "recurring_rule": r[8], "version": r[9],
                     "color": r[11]} for r in conn.execute("SELECT * FROM events WHERE is_dirty = 1").fetchall()]

    def mark_clean(self, event_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE events SET is_dirty = 0 WHERE id = ?", (event_id,))
            conn.commit()

    def get_meta(self, key):
        with sqlite3.connect(self.db_path) as conn:
            res = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
            return res[0] if res else None

    def set_meta(self, key, value):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO meta VALUES (?, ?)", (key, value))
            conn.commit()

    def get_event_title(self, event_id):
        with sqlite3.connect(self.db_path) as conn:
            res = conn.execute("SELECT title FROM events WHERE id = ?", (event_id,)).fetchone()
            return res[0] if res else "Новое событие"

    def get_queue(self):
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT id, action, payload FROM sync_queue ORDER BY timestamp ASC").fetchall()

    def remove_queue_item(self, q_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM sync_queue WHERE id = ?", (q_id,))
            conn.commit()