import customtkinter as ctk
import threading
import os
import sys
from datetime import datetime
from core.sync_engine import SyncEngine
from core.scheduler import ReminderScheduler
from ui.auth_window import AuthWindow
from ui.main_window import MainWindow

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class CalendarApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Календарь")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        os.makedirs(cache_dir, exist_ok=True)
        self.db = SyncEngine(os.path.join(cache_dir, "calendar_cache.db"), "http://138.124.85.61:8000")
        self.scheduler = ReminderScheduler(self.db)
        self.auth_window = None
        self.main_ui = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.check_auth()
        self.bind("<Configure>", self.on_resize)
        self.after(30000, self.auto_sync)

    def check_auth(self):
        token = self.db.get_meta("auth_token")
        if token:
            self.db.token = token
            self.main_ui = MainWindow(self)
            self.main_ui.pack(fill="both", expand=True)
        else:
            self.auth_window = AuthWindow(self)
            self.auth_window.transient(self)
            self.auth_window.focus_set()

    def on_close(self):
        self.scheduler.scheduler.shutdown()
        self.destroy()

    def on_resize(self, event):
        if self.main_ui:
            self.main_ui.update_layout()

    def auto_sync(self):
        threading.Thread(target=self.db.pull, daemon=True).start()
        self.after(30000, self.auto_sync)

if __name__ == "__main__":
    app = CalendarApp()
    app.mainloop()