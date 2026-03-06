import customtkinter as ctk
import tkinter as tk
from widgets import ScaledFrame
from config import THEME
from database import load_texts, load_custom_texts


class LevelScreen(ScaledFrame):
    def __init__(self, parent, on_back, on_start_game, on_load_custom):
        super().__init__(parent, fg_color=THEME['bg'])
        self.on_back = on_back
        self.on_start_game = on_start_game
        self.on_load_custom = on_load_custom
        self.texts = load_texts()
        self.custom_texts = load_custom_texts()
        self.difficulty = 'easy'
        self.selected_text_index = None
        self.diff_buttons = []
        self.create_widgets()

    def create_widgets(self):
        header = ctk.CTkFrame(self, fg_color=THEME['card'], height=self.scale_size(70), corner_radius=0)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        header.bind('<Double-Button-1>', self.on_header_double_click)

        ctk.CTkButton(header, text="← Назад", width=self.scale_size(100), height=self.scale_size(35),
                      fg_color=THEME['light'], hover_color=THEME['red'],
                      text_color=THEME['text'], font=ctk.CTkFont('Segoe UI', self.scale_font(10)),
                      command=self.on_back).pack(side=tk.LEFT, padx=self.scale_size(20), pady=self.scale_size(17))

        ctk.CTkLabel(header, text="Выберите уровень", font=ctk.CTkFont('Segoe UI', self.scale_font(20), 'bold'),
                    text_color=THEME['text']).pack(side=tk.LEFT, padx=self.scale_size(20), pady=self.scale_size(20))

        info_frame = ctk.CTkFrame(self, fg_color=THEME['card'])
        info_frame.pack(fill=tk.X, padx=self.scale_size(30), pady=(self.scale_size(15), 0))

        ctk.CTkLabel(info_frame, text="Сложность:", font=ctk.CTkFont('Segoe UI', self.scale_font(11)),
                    text_color=THEME['text_muted']).pack(side=tk.LEFT, padx=self.scale_size(20), pady=self.scale_size(12))

        self.diff_label = ctk.CTkLabel(info_frame, text="● Лёгкий", font=ctk.CTkFont('Segoe UI', self.scale_font(14), 'bold'),
                                       text_color=THEME['green'])
        self.diff_label.pack(side=tk.LEFT, padx=self.scale_size(10), pady=self.scale_size(12))

        ctk.CTkLabel(info_frame, text="|", text_color=THEME['text_muted']).pack(side=tk.LEFT, padx=self.scale_size(10), pady=self.scale_size(12))

        self.text_info_label = ctk.CTkLabel(info_frame, text="5 текстов доступно",
                                        font=ctk.CTkFont('Segoe UI', self.scale_font(12)),
                                        text_color=THEME['text_muted'])
        self.text_info_label.pack(side=tk.LEFT, padx=self.scale_size(10), pady=self.scale_size(12))

        content = ctk.CTkFrame(self, fg_color='transparent')
        content.pack(fill=tk.BOTH, expand=True, padx=self.scale_size(30), pady=self.scale_size(15))

        left_panel = ctk.CTkFrame(content, fg_color=THEME['card'], corner_radius=self.scale_size(12))
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, self.scale_size(15)))

        ctk.CTkLabel(left_panel, text="Уровень сложности",
                    font=ctk.CTkFont('Segoe UI', self.scale_font(13), 'bold'),
                    text_color=THEME['text']).pack(anchor='w', padx=self.scale_size(20), pady=(self.scale_size(15), self.scale_size(10)))

        diff_info = [
            ('easy', 'Лёгкий', '300-400 символов', THEME['green']),
            ('medium', 'Средний', '400-500 символов', '#f57c00'),
            ('hard', 'Сложный', '600-800 символов', THEME['red']),
            ('custom', 'Пользовательский', 'От 50 символов', THEME['text'])
        ]

        self.diff_var = ctk.StringVar(value='easy')
        for diff_id, name, length, color in diff_info:
            btn = ctk.CTkFrame(left_panel, fg_color=THEME['light'], corner_radius=self.scale_size(8), cursor='hand2')
            btn.pack(fill=tk.X, padx=self.scale_size(15), pady=self.scale_size(4))

            inner = ctk.CTkFrame(btn, fg_color='transparent')
            inner.pack(fill=tk.BOTH, expand=True, padx=self.scale_size(15), pady=self.scale_size(10))

            icon_label = ctk.CTkLabel(inner, text='●' if diff_id == 'easy' else '○',
                                          font=ctk.CTkFont('Segoe UI', self.scale_font(16)),
                                          text_color=color if diff_id == 'easy' else THEME['text_muted'])
            icon_label.pack(side=tk.LEFT, padx=(0, self.scale_size(8)))

            ctk.CTkLabel(inner, text=name, font=ctk.CTkFont('Segoe UI', self.scale_font(12), 'bold'),
                        text_color=THEME['text']).pack(side=tk.LEFT, padx=self.scale_size(5))
            ctk.CTkLabel(inner, text=length, font=ctk.CTkFont('Segoe UI', self.scale_font(9)),
                        text_color=THEME['text_muted']).pack(side=tk.LEFT, padx=self.scale_size(5))

            btn.bind('<Button-1>', self.create_difficulty_handler(diff_id))
            inner.bind('<Button-1>', self.create_difficulty_handler(diff_id))
            for widget in inner.winfo_children():
                widget.bind('<Button-1>', self.create_difficulty_handler(diff_id))

            self.diff_buttons.append((btn, diff_id, color, inner))

        right_panel = ctk.CTkFrame(content, fg_color=THEME['card'], corner_radius=self.scale_size(12))
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_header = ctk.CTkFrame(right_panel, fg_color='transparent')
        right_header.pack(fill=tk.X, padx=self.scale_size(20), pady=(self.scale_size(15), self.scale_size(10)))

        ctk.CTkLabel(right_header, text="Доступные тексты",
                    font=ctk.CTkFont('Segoe UI', self.scale_font(13), 'bold'),
                    text_color=THEME['text']).pack(side=tk.LEFT)

        self.load_btn = ctk.CTkButton(right_header, text="+ Загрузить", width=self.scale_size(120), height=self.scale_size(30),
                                     fg_color=THEME['light'], hover_color=THEME['red'],
                                     text_color=THEME['text'],
                                     font=ctk.CTkFont('Segoe UI', self.scale_font(10)),
                                     command=self.on_load_custom)
        self.load_btn.pack(side=tk.RIGHT)

        self.list_frame = ctk.CTkScrollableFrame(right_panel, fg_color='transparent',
                                                  corner_radius=self.scale_size(8),
                                                  scrollbar_button_color=THEME['red'],
                                                  scrollbar_button_hover_color=THEME['red_light'])
        self.list_frame.pack(fill=tk.BOTH, expand=True, padx=self.scale_size(20), pady=(0, self.scale_size(15)))

        self.start_btn = ctk.CTkButton(right_panel, text="Начать тренировку", height=self.scale_size(50),
                                       fg_color=THEME['red'], hover_color=THEME['red_light'],
                                       text_color=THEME['text'],
                                       font=ctk.CTkFont('Segoe UI', self.scale_font(14), 'bold'),
                                       state='disabled', command=self.start_game,
                                       corner_radius=self.scale_size(8))
        self.start_btn.pack(fill=tk.X, padx=self.scale_size(20), pady=(0, self.scale_size(20)))

        self.highlight_difficulty()
        self.update_list()

    def on_header_double_click(self, event) -> None:
        self.master.toggle_fullscreen()

    def create_difficulty_handler(self, diff_id: str):
        def handler(event):
            self.set_difficulty(diff_id)
        return handler

    def set_difficulty(self, diff: str) -> None:
        self.diff_var.set(diff)
        self.difficulty = diff
        self.highlight_difficulty()
        self.update_list()
        self.update_start_button()

    def highlight_difficulty(self) -> None:
        icons = THEME['diff_icons']
        names = THEME['diff_names']
        colors = THEME['diff_colors']
        for btn, diff_id, color, inner in self.diff_buttons:
            is_selected = (diff_id == self.difficulty)
            if is_selected:
                btn.configure(fg_color=THEME['bg'], border_color=color, border_width=3)
            else:
                btn.configure(fg_color=THEME['light'], border_color=THEME['card'], border_width=0)
            icon = icons[diff_id] if is_selected else '○'
            icon_color = color if is_selected else THEME['text_muted']
            for widget in inner.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    text = widget.cget('text')
                    if text in ['●', '○', '★']:
                        widget.configure(text=icon, text_color=icon_color)
                    else:
                        widget.configure(text_color=THEME['text'])
        self.diff_label.configure(text=f"{icons[self.difficulty]} {names[self.difficulty]}",
                                 text_color=colors.get(self.difficulty, THEME['text']))

    def update_list(self) -> None:
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self.text_buttons = []
        if self.difficulty == 'custom':
            texts = self.custom_texts
            self.load_btn.configure(state='normal')
        else:
            texts = self.texts.get(self.difficulty, [])
            self.load_btn.configure(state='disabled')
        count = len(texts)
        self.text_info_label.configure(text=f"{count} текстов доступно")
        if not texts:
            msg = "Нет загруженных текстов\nНажмите «+ Загрузить» чтобы добавить" if self.difficulty == 'custom' else "Нет текстов для этой сложности"
            ctk.CTkLabel(self.list_frame, text=msg,
                        text_color=THEME['text_muted'],
                        font=ctk.CTkFont('Segoe UI', self.scale_font(12)),
                        justify='center').pack(pady=self.scale_size(30))
            self.update_start_button()
            return
        for i, text_data in enumerate(texts):
            text_len = len(text_data['text'])
            btn = ctk.CTkButton(self.list_frame,
                               text=f"{i+1}. {text_data['title']}  •  {text_len} симв.",
                               height=self.scale_size(50),
                               fg_color=THEME['light'],
                               hover_color=THEME['red'],
                               text_color=THEME['text'],
                               font=ctk.CTkFont('Segoe UI', self.scale_font(11)),
                               anchor='w',
                               command=self.create_text_handler(i),
                               corner_radius=self.scale_size(8))
            btn.pack(fill=tk.X, padx=self.scale_size(10), pady=self.scale_size(5))
            self.text_buttons.append(btn)
        self.update_start_button()

    def create_text_handler(self, index: int):
        def handler():
            self.select_text(index)
        return handler

    def select_text(self, index: int) -> None:
        self.selected_text_index = index
        for i, btn in enumerate(self.text_buttons):
            btn.configure(fg_color=THEME['red'] if i == index else THEME['light'])
        self.update_start_button()

    def update_start_button(self) -> None:
        texts = self.custom_texts if self.difficulty == 'custom' else self.texts.get(self.difficulty, [])
        if self.selected_text_index is not None and 0 <= self.selected_text_index < len(texts):
            self.start_btn.configure(state='normal')
            self.text_info_label.configure(text=f"✓ {texts[self.selected_text_index]['title']}")
        else:
            self.start_btn.configure(state='disabled')
            self.text_info_label.configure(text=f"{len(texts)} текстов доступно")

    def start_game(self) -> None:
        texts = self.custom_texts if self.difficulty == 'custom' else self.texts.get(self.difficulty, [])
        if self.selected_text_index is not None and 0 <= self.selected_text_index < len(texts):
            self.on_start_game(texts[self.selected_text_index], self.difficulty)
