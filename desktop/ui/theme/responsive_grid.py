import customtkinter as ctk
from datetime import datetime, timedelta
from typing import Callable, Optional

class ResponsiveGrid:
    def __init__(self, parent_frame, start_date: datetime, start_hour: int = 0, hours: int = 24, cell_height: int = 30):
        self.parent = parent_frame
        self.start_date = start_date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
        self.start_hour = start_hour
        self.hours = hours
        self.cell_height = cell_height
        self.highlighted = None
        self.drop_callback = None
        self.parent.bind("<Motion>", self._on_hover)
        self.parent.bind("<Leave>", self._clear_highlight)

    def set_drop_callback(self, callback: Callable[[datetime], None]):
        self.drop_callback = callback

    def calculate_time_from_coords(self, x: int, y: int) -> Optional[datetime]:
        hour_offset = y // self.cell_height
        if hour_offset < 0 or hour_offset >= self.hours:
            return None
        return self.start_date + timedelta(hours=hour_offset)

    def _on_hover(self, event):
        row = event.y // self.cell_height
        if row < 0 or row >= self.hours:
            return
        self.parent.update_idletasks()
        self.parent.configure(cursor="hand2")

    def _clear_highlight(self, event):
        self.parent.configure(cursor="arrow")

    def attach_draggable(self, widget, event_id, on_release_callback: Callable):
        def on_press(e):
            widget.lift()
            widget._drag_start = (e.x, e.y)

        def on_motion(e):
            new_y = e.y_root - widget._drag_start[1]
            new_x = e.x_root - widget._drag_start[0]
            widget.place(x=new_x, y=new_y)

        def on_release(e):
            target = self.calculate_time_from_coords(e.x_root - self.parent.winfo_rootx(), e.y_root - self.parent.winfo_rooty())
            if target and self.drop_callback:
                self.drop_callback(event_id, target)
            widget.place_forget()
            widget.parent.refresh() if hasattr(widget, "parent") else None

        widget.bind("<ButtonPress-1>", on_press)
        widget.bind("<B1-Motion>", on_motion)
        widget.bind("<ButtonRelease-1>", on_release)