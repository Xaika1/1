import customtkinter as ctk
from datetime import datetime, timedelta
from calendar import monthcalendar
from ui.widgets.event_card import EventCard
from ui.widgets.event_dialog import EventDialog

class MonthView(ctk.CTkFrame):
    def __init__(self, parent, app_instance, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.app = app_instance
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(self.header_frame, text="<", width=30, command=self.prev_month).pack(side="left")
        self.month_label = ctk.CTkLabel(self.header_frame, text="", font=("", 16, "bold"))
        self.month_label.pack(side="left", expand=True)
        ctk.CTkButton(self.header_frame, text=">", width=30, command=self.next_month).pack(side="right")
        self.calendar_frame = ctk.CTkScrollableFrame(self, label_text="")
        self.calendar_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.refresh()

    def refresh(self):
        for w in self.calendar_frame.winfo_children():
            w.destroy()
        self.month_label.configure(text=f"{self.current_year}-{self.current_month:02d}")
        days = monthcalendar(self.current_year, self.current_month)
        header_row = ctk.CTkFrame(self.calendar_frame, fg_color="transparent")
        header_row.pack(fill="x", pady=2)
        for day_name in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
            ctk.CTkLabel(header_row, text=day_name, width=40, anchor="center").pack(side="left", fill="x", expand=True)
        for week in days:
            week_frame = ctk.CTkFrame(self.calendar_frame, fg_color="transparent")
            week_frame.pack(fill="x", pady=1)
            for day in week:
                cell = ctk.CTkFrame(week_frame, fg_color="#1f2328", corner_radius=4)
                cell.pack(side="left", fill="x", expand=True, padx=1, pady=1, ipady=10)
                if day == 0:
                    continue
                ctk.CTkLabel(cell, text=str(day), font=("", 10, "bold")).pack(anchor="nw", padx=2, pady=2)
                cell.bind("<Button-1>", lambda e, d=day: self.on_day_click(d))
                self.render_events_for_day(cell, day)

    def render_events_for_day(self, cell, day):
        date = datetime(self.current_year, self.current_month, day)
        events = self.app.db.db.get_events(1, date, date + timedelta(days=1))
        for ev in events:
            card = EventCard(cell, {"id": ev[0], "title": ev[2], "color": ev[11] or "#3a7ca5"},
                             on_drop=lambda eid, t: self.app.db.queue_change("UPDATE", {"id": eid, "start_time": t.isoformat(), "end_time": (t+timedelta(hours=1)).isoformat(), "version": 2}))
            card.pack(fill="x", padx=2, pady=1)

    def on_day_click(self, day):
        EventDialog(self, initial_data={"start_time": datetime(self.current_year, self.current_month, day).isoformat(), "end_time": (datetime(self.current_year, self.current_month, day)+timedelta(hours=1)).isoformat()})

    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.refresh()

    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.refresh()