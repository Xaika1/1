import customtkinter as ctk
import tkinter as tk
from widgets import ScaledFrame
from config import THEME


class MainMenuScreen(ScaledFrame):
    def __init__(self, parent, username: str, on_start, on_load_file, on_logout):
        super().__init__(parent, fg_color=THEME['bg'])
        self.username = username
        self.on_start = on_start
        self.on_load_file = on_load_file
        self.on_logout = on_logout
        self.create_widgets()

    def create_widgets(self):
        header = ctk.CTkFrame(self, fg_color=THEME['card'], height=self.scale_size(60), corner_radius=0)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        ctk.CTkLabel(header, text=f"Добро пожаловать, {self.username}!",
                    font=ctk.CTkFont('Segoe UI', self.scale_font(18), 'bold'),
                    text_color=THEME['text']).pack(side=tk.LEFT, padx=self.scale_size(25), pady=self.scale_size(18))

        card = ctk.CTkFrame(self, fg_color=THEME['card'], corner_radius=self.scale_size(15))
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ctk.CTkLabel(card, text="Главное меню", font=ctk.CTkFont('Segoe UI', self.scale_font(20), 'bold'),
                    text_color=THEME['text']).pack(pady=self.scale_size(30))

        btn_frame = ctk.CTkFrame(card, fg_color='transparent')
        btn_frame.pack(padx=self.scale_size(40), pady=self.scale_size(10))

        ctk.CTkButton(btn_frame, text="Начать тренировку", width=self.scale_size(280), height=self.scale_size(50),
                      fg_color=THEME['red'], hover_color=THEME['red_light'],
                      text_color=THEME['text'], font=ctk.CTkFont('Segoe UI', self.scale_font(14), 'bold'),
                      command=self.on_start).pack(pady=self.scale_size(10))

        ctk.CTkButton(btn_frame, text="Выйти из аккаунта", width=self.scale_size(280), height=self.scale_size(45),
                      fg_color=THEME['light'], hover_color=THEME['red'],
                      text_color=THEME['text'], font=ctk.CTkFont('Segoe UI', self.scale_font(13)),
                      command=self.on_logout).pack(pady=self.scale_size(10))
