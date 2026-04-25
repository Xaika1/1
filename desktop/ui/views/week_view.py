import customtkinter as ctk
from datetime import datetime, timedelta
from ui.widgets.event_dialog import EventDialog

class WeekView(ctk.CTkFrame):
    def __init__(self, parent, app_instance, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.app = app_instance
        self.current_date = datetime.now()
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(self.header, text="<", width=30, command=self.prev_week).pack(side="left")
        self.label = ctk.CTkLabel(self.header, text="", font=("", 16, "bold"))
        self.label.pack(side="left", expand=True)
        ctk.CTkButton(self.header, text=">", width=30, command=self.next_week).pack(side="right")
        self.canvas_frame = ctk.CTkScrollableFrame(self)
        self.canvas_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.refresh()

    def refresh(self):
        for w in self.canvas_frame.winfo_children():
            w.destroy()
        start = self.current_date - timedelta(days=self.current_date.weekday())
        days = [start + timedelta(days=i) for i in range(7)]
        header_row = ctk.CTkFrame(self.canvas_frame, fg_color="transparent")
        header_row.pack(fill="x", pady=2)
        day_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for i, d in enumerate(days):
            f = ctk.CTkFrame(header_row, fg_color="transparent")
            f.pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(f, text=f"{day_names[i]} {d.day}", font=("", 12, "bold")).pack()
        for hour in range(0, 24):
            row = ctk.CTkFrame(self.canvas_frame, fg_color="transparent")
            row.pack(fill="x", pady=1)
            ctk.CTkLabel(row, text=f"{hour:02d}:00", width=50, anchor="w").pack(side="left")
            for d in days:
                cell = ctk.CTkFrame(row, fg_color="#1f2328", height=30)
                cell.pack(side="left", fill="x", expand=True, padx=1)
                cell.bind("<Button-1>", lambda e, dt=datetime(d.year, d.month, d.day, hour): self.app.db.queue_change("CREATE", {"title": "Новое", "start_time": dt.isoformat(), "end_time": (dt+timedelta(hours=1)).isoformat(), "version": 1}))
        self.label.configure(text=start.strftime("%B %Y"))

    def prev_week(self):
        self.current_date -= timedelta(weeks=1)
        self.refresh()

    def next_week(self):
        self.current_date += timedelta(weeks=1)
        self.refresh()