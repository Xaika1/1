import customtkinter as ctk
from datetime import datetime, timedelta

class DragDropHandler:
    def __init__(self, grid_frame, on_drop_callback):
        self.grid_frame = grid_frame
        self.on_drop = on_drop_callback
        self.dragged_widget = None
        self.original_pos = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.grid_frame.bind("<Button-1>", self.on_press)
        self.grid_frame.bind("<B1-Motion>", self.on_motion)
        self.grid_frame.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        widget = event.widget.master if event.widget.master != self.grid_frame else event.widget
        if not isinstance(widget, ctk.CTkFrame): return
        self.dragged_widget = widget
        self.original_pos = (self.dragged_widget.winfo_x(), self.dragged_widget.winfo_y())
        self.drag_offset_x = event.x
        self.drag_offset_y = event.y
        self.dragged_widget.lift()

    def on_motion(self, event):
        if not self.dragged_widget: return
        new_x = self.grid_frame.winfo_pointerx() - self.grid_frame.winfo_rootx() - self.drag_offset_x
        new_y = self.grid_frame.winfo_pointery() - self.grid_frame.winfo_rooty() - self.drag_offset_y
        self.dragged_widget.place(x=new_x, y=new_y)

    def on_release(self, event):
        if not self.dragged_widget: return
        target_time = self.calculate_time_from_coords(event.x_root, event.y_root)
        if target_time and self.on_drop:
            self.on_drop(self.dragged_widget.event_id, target_time)
        self.dragged_widget.place(x=self.original_pos[0], y=self.original_pos[1])
        self.dragged_widget = None
        self.original_pos = None

    def calculate_time_from_coords(self, x, y):
        root_y = self.grid_frame.winfo_rooty()
        rel_y = y - root_y
        hour_offset = rel_y // 30
        if 0 <= hour_offset < 24:
            base = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            return base + timedelta(hours=hour_offset)
        return None