import customtkinter as ctk
import threading

class Toolbar(ctk.CTkFrame):
    def __init__(self, parent, app_instance, **kwargs):
        super().__init__(parent, fg_color="#2b2d31", **kwargs)
        self.parent = parent
        self.app = app_instance
        self.grid_columnconfigure(0, weight=1)
        self.logo = ctk.CTkLabel(self, text="📅 Календарь", font=("", 18, "bold"))
        self.logo.grid(row=0, column=0, padx=15, sticky="w")
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=0, column=1, sticky="e")
        ctk.CTkButton(btn_frame, text="День", width=60, command=lambda: self.set_view("day")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Неделя", width=60, command=lambda: self.set_view("week")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Месяц", width=60, command=lambda: self.set_view("month")).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Синхронизировать", command=self.sync).pack(side="left", padx=10)

    def set_view(self, view):
        self.parent.set_view(view)

    def sync(self):
        threading.Thread(target=self.app.db.pull, daemon=True).start()