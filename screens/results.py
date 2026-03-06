import customtkinter as ctk
import tkinter as tk
from widgets import ScaledFrame
from config import THEME
from models import GameResult


class ResultsScreen(ScaledFrame):
    def __init__(self, parent, result: GameResult, on_retry, on_levels, on_menu):
        super().__init__(parent, fg_color=THEME['bg'])
        self.result = result
        self.on_retry = on_retry
        self.on_levels = on_levels
        self.on_menu = on_menu
        self.create_widgets()

    def create_widgets(self):
        header = ctk.CTkFrame(self, fg_color=THEME['card'], height=self.scale_size(60), corner_radius=0)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        header.bind('<Double-Button-1>', self.on_header_double_click)

        ctk.CTkButton(header, text="← Назад", width=self.scale_size(100), height=self.scale_size(35),
                      fg_color=THEME['light'], hover_color=THEME['red'],
                      text_color=THEME['text'], font=ctk.CTkFont('Segoe UI', self.scale_font(10)),
                      command=self.on_levels).pack(side=tk.LEFT, padx=self.scale_size(20), pady=self.scale_size(12))

        ctk.CTkLabel(header, text="Результаты", font=ctk.CTkFont('Segoe UI', self.scale_font(18), 'bold'),
                    text_color=THEME['text']).pack(side=tk.LEFT, padx=self.scale_size(15), pady=self.scale_size(17))

        card = ctk.CTkFrame(self, fg_color=THEME['card'], corner_radius=self.scale_size(15))
        card.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        rank_color = THEME['ranks'].get(self.result.rank, THEME['text_muted'])
        rank_desc = THEME['rank_descs'].get(self.result.rank, '')

        ctk.CTkLabel(card, text=self.result.rank, font=ctk.CTkFont('Segoe UI', self.scale_font(56), 'bold'),
                    text_color=rank_color).pack(pady=self.scale_size(10))
        ctk.CTkLabel(card, text=rank_desc, font=ctk.CTkFont('Segoe UI', self.scale_font(13)),
                    text_color=THEME['text_muted']).pack(pady=(0, self.scale_size(20)))

        stats = ctk.CTkFrame(card, fg_color='transparent')
        stats.pack(padx=self.scale_size(30), pady=self.scale_size(10))

        data = [
            ('Очки', str(self.result.score), THEME['red']),
            ('Точность', f"{self.result.accuracy:.1f}%", THEME['text']),
            ('Ошибки', str(self.result.errors), THEME['red_light']),
            ('Время', f"{self.result.time:.1f}с", THEME['text_muted']),
            ('Символы', str(self.result.characters), THEME['text_muted']),
            ('Сложность', THEME['diff_names'].get(self.result.difficulty, ''), THEME['text_muted'])
        ]

        for i, (label, value, color) in enumerate(data):
            r, c = i // 3, i % 3
            frame = ctk.CTkFrame(stats, fg_color=THEME['light'], width=self.scale_size(140), height=self.scale_size(75))
            frame.grid(row=r, column=c, padx=self.scale_size(10), pady=self.scale_size(10))
            frame.pack_propagate(False)

            ctk.CTkLabel(frame, text=label, font=ctk.CTkFont('Segoe UI', self.scale_font(9)),
                        text_color=THEME['text_muted']).pack(pady=(self.scale_size(15), self.scale_size(2)))
            ctk.CTkLabel(frame, text=value, font=ctk.CTkFont('Segoe UI', self.scale_font(13), 'bold'),
                        text_color=color).pack()

        btns = ctk.CTkFrame(card, fg_color='transparent')
        btns.pack(pady=self.scale_size(25))

        for text, command in [("Ещё раз", self.on_retry), ("Выбрать уровень", self.on_levels), ("В меню", self.on_menu)]:
            ctk.CTkButton(btns, text=text, width=self.scale_size(130), height=self.scale_size(40),
                          fg_color=THEME['red'] if command == self.on_retry else THEME['light'],
                          hover_color=THEME['red_light'] if command == self.on_retry else THEME['red'],
                          text_color=THEME['text'], font=ctk.CTkFont('Segoe UI', self.scale_font(11)),
                          command=command).pack(side=tk.LEFT, padx=self.scale_size(5))

    def on_header_double_click(self, event) -> None:
        self.master.toggle_fullscreen()
