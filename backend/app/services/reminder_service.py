from datetime import datetime, timedelta
from typing import List, Dict
import sqlite3
import os

def get_upcoming_reminders(db_path: str, window_minutes: int = 15) -> List[Dict]:
    if not os.path.exists(db_path): return []
    with sqlite3.connect(db_path) as conn:
        now = datetime.utcnow()
        end = now + timedelta(minutes=window_minutes)
        query = """
            SELECT e.id, e.title, e.start_time, er.offset_minutes 
            FROM events e 
            JOIN event_reminders er ON e.id = er.event_id 
            WHERE e.start_time BETWEEN ? AND ? AND e.start_time > ?
        """
        cursor = conn.execute(query, (now.isoformat(), end.isoformat(), now.isoformat()))
        return [{"id": r[0], "title": r[1], "start": r[2], "offset": r[3]} for r in cursor.fetchall()]