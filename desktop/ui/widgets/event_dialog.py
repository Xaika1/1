import customtkinter as ctk
from datetime import datetime, timedelta

class EventDialog(ctk.CTkToplevel):
    def __init__(self, parent, event_id=None, initial_data=None):
        super().__init__(parent)
        self.geometry("400x350")
        self.title("Событие")
        self.resizable(False, False)
        self.event_id = event_id
        self.data = initial_data or {}
        ctk.CTkLabel(self, text="Название").pack(pady=(10,0), padx=10, fill="x")
        self.title_entry = ctk.CTkEntry(self)
        self.title_entry.pack(padx=10, pady=5, fill="x")
        self.title_entry.insert(0, self.data.get("title", ""))
        ctk.CTkLabel(self, text="Начало").pack(pady=(5,0), padx=10, fill="x")
        self.start_entry = ctk.CTkEntry(self)
        self.start_entry.pack(padx=10, pady=5, fill="x")
        self.start_entry.insert(0, self.data.get("start_time", datetime.now().isoformat(timespec="minutes")))
        ctk.CTkLabel(self, text="Конец").pack(pady=(5,0), padx=10, fill="x")
        self.end_entry = ctk.CTkEntry(self)
        self.end_entry.pack(padx=10, pady=5, fill="x")
        self.end_entry.insert(0, self.data.get("end_time", (datetime.now()+timedelta(hours=1)).isoformat(timespec="minutes")))
        ctk.CTkLabel(self, text="Описание").pack(pady=(5,0), padx=10, fill="x")
        self.desc_text = ctk.CTkTextbox(self, height=80)
        self.desc_text.pack(padx=10, pady=5, fill="x")
        self.desc_text.insert("1.0", self.data.get("description", ""))
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(btn_frame, text="Отмена", command=self.destroy).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Сохранить", command=self.save).pack(side="right", padx=5)

    def save(self):
        start = self.start_entry.get()
        end = self.end_entry.get()
        title = self.title_entry.get()
        desc = self.desc_text.get("1.0", "end").strip()
        self.parent.parent.db.queue_change("UPDATE" if self.event_id else "CREATE",
                                           {"id": self.event_id or 0, "title": title, "start_time": start, "end_time": end, "version": self.data.get("version", 1) + 1})
        self.destroy()
        if hasattr(self.parent.parent, "refresh"):
            self.parent.parent.refresh()