import customtkinter as ctk


class ScaledFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.scale = parent.scale

    def scale_size(self, val: int) -> int:
        return int(val * self.scale)

    def scale_font(self, size: int) -> int:
        return int(size * self.scale)
