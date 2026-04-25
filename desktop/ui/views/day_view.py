import customtkinter as ctk
from datetime import datetime, timedelta
from ui.widgets.event_card import EventCard
from ui.widgets.event_dialog import EventDialog

class DayView(ctk.CTkFrame):
    def __init__(self, parent, app_instance, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app_instance
        self.current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(self.header, text="<", width=30, command=self.prev_day).pack(side="left")
        self.label = ctk.CTkLabel(self.header, text="", font=("", 16, "bold"))
        self.label.pack(side="left", expand=True)
        ctk.CTkButton(self.header, text=">", width=30, command=self.next_day).pack(side="right")
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.refresh()

    def refresh(self):
        for w in self.scroll.winfo_children():
            w.destroy()
        self.label.configure(text=self.current_date.strftime("%d %B %Y"))
        events = self.app.db.db.get_events(1, self.current_date, self.current_date + timedelta(days=1))
        sorted_events = sorted(events, key=lambda x: x[4])
        for ev in sorted_events:
            card = EventCard(self.scroll, {"id": ev[0], "title": ev[2], "color": ev[11] or "#3a7ca5"},
                             on_drop=lambda eid, t: self.app.db.queue_change("UPDATE", {"id": eid, "start_time": t.isoformat(), "end_time": (t+timedelta(hours=1)).isoformat(), "version": 2}))
            card.pack(fill="x", padx=5, pady=3)
        for h in range(24):
            slot = ctk.CTkFrame(self.scroll, fg_color="#1f2328", height=40, corner_radius=4)
            slot.pack(fill="x", padx=5, pady=2)
            ctk.CTkLabel(slot, text=f"{h:02d}:00", anchor="w").pack(side="left", padx=5)
            slot.bind("<Button-1>", lambda e, hour=h: self.create_event_at(hour))

    def prev_day(self):
        self.current_date -= timedelta(days=1)
        self.refresh()

    def next_day(self):
        self.current_date += timedelta(days=1)
        self.refresh()

    def create_event_at(self, hour):
        EventDialog(self, initial_data={"start_time": self.current_date.replace(hour=hour).isoformat(), "end_time": self.current_date.replace(hour=hour+1).isoformat()})