from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import sqlite3
import os

class ReminderScheduler:
    def __init__(self, sync_engine):
        self.scheduler = BackgroundScheduler()
        self.sync_engine = sync_engine
        self.scheduler.add_job(self.check_reminders, 'interval', minutes=1)
        self.scheduler.start()

    def check_reminders(self):
        if not os.path.exists(self.sync_engine.db.db_path): return
        try:
            with sqlite3.connect(self.sync_engine.db.db_path) as conn:
                now = datetime.utcnow()
                window = (now + timedelta(minutes=5)).isoformat()
                cursor = conn.execute("SELECT id, title, start_time FROM events WHERE start_time BETWEEN ? AND ? AND start_time > ?",
                                      (now.isoformat(), window, now.isoformat()))
                for event in cursor.fetchall():
                    self.trigger_notification(event[1])
        except Exception:
            pass

    def trigger_notification(self, title):
        try:
            import plyer
            plyer.notification.notify(title="Напоминание", message=f"{title} скоро начнётся.", app_name="Календарь", timeout=10)
        except ImportError:
            pass