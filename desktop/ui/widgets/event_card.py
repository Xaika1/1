import customtkinter as ctk

class EventCard(ctk.CTkFrame):
    def __init__(self, parent, event_data, on_drop, **kwargs):
        super().__init__(parent, **kwargs)
        self.event_id = event_data.get("id")
        self.event_data = event_data
        self.on_drop = on_drop
        self.configure(fg_color=event_data.get("color", "#3a7ca5"), corner_radius=6)
        self.label = ctk.CTkLabel(self, text=event_data["title"], text_color="white")
        self.label.pack(fill="both", expand=True, padx=4, pady=2)
        self.dragging = False
        self.start_x = 0
        self.start_y = 0
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.label.bind("<ButtonPress-1>", self.on_press)
        self.label.bind("<B1-Motion>", self.on_drag)
        self.label.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.dragging = True
        self.start_x = event.x_root
        self.start_y = event.y_root
        self.lift()

    def on_drag(self, event):
        if not self.dragging: return
        dx = event.x_root - self.start_x
        dy = event.y_root - self.start_y
        self.place_configure(x=self.winfo_x() + dx, y=self.winfo_y() + dy)
        self.start_x = event.x_root
        self.start_y = event.y_root

    def on_release(self, event):
        self.dragging = False
        target_time = self.parent.parent.calculate_time_from_coords(event.x_root, event.y_root) if hasattr(self.parent.parent, "calculate_time_from_coords") else None
        if target_time and self.on_drop:
            self.on_drop(self.event_data["id"], target_time)
        self.place_forget()
        if hasattr(self.parent.parent, "refresh"):
            self.parent.parent.refresh()