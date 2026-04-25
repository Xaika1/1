import customtkinter as ctk
from ui.views.month_view import MonthView
from ui.views.week_view import WeekView
from ui.views.day_view import DayView
from ui.widgets.toolbar import Toolbar

class MainWindow(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.toolbar = Toolbar(self, self.parent)
        self.toolbar.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        self.active_view = None
        self.set_view("month")

    def set_view(self, view_type):
        if self.active_view:
            self.active_view.destroy()
        if view_type == "month":
            self.active_view = MonthView(self, self.parent)
        elif view_type == "week":
            self.active_view = WeekView(self, self.parent)
        elif view_type == "day":
            self.active_view = DayView(self, self.parent)
        self.active_view.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    def update_layout(self):
        if self.active_view:
            self.active_view.refresh()