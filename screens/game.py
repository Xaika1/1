import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from widgets import ScaledFrame
from config import THEME, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, TIMER_INTERVAL_MS, SCORE_MULTIPLIERS, ERROR_PENALTY
from models import GameResult
from utils import check_char_match, calc_rank


class GameScreen(ScaledFrame):
    def __init__(self, parent, text_data: dict, difficulty: str, on_finish, on_back, on_give_up):
        super().__init__(parent, fg_color=THEME['bg'])
        self.text = text_data['text']
        self.title = text_data['title']
        self.difficulty = difficulty
        self.on_finish = on_finish
        self.on_back = on_back
        self.on_give_up = on_give_up
        self.user_input = ""
        self.errors = 0
        self.start_time = datetime.now()
        self.finished = False
        self.give_up_mode = False

        min_width = int(MIN_WINDOW_WIDTH * self.scale)
        min_height = int(MIN_WINDOW_HEIGHT * self.scale)
        parent.minsize(min_width, min_height)

        curr_width = parent.winfo_width()
        curr_height = parent.winfo_height()
        if curr_width < min_width or curr_height < min_height:
            parent.geometry(f"{min_width}x{min_height}")

        self.create_widgets()
        self.update_display()
        self.update_timer()
        self.after(TIMER_INTERVAL_MS, self.set_input_focus)

    def set_input_focus(self) -> None:
        self.input_entry.focus_set()

    def create_widgets(self):
        header = ctk.CTkFrame(self, fg_color=THEME['card'], height=self.scale_size(70), corner_radius=0)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        header.bind('<Double-Button-1>', self.on_header_double_click)

        ctk.CTkButton(header, text="← Назад", width=self.scale_size(100), height=self.scale_size(35),
                      fg_color=THEME['light'], hover_color=THEME['red'],
                      text_color=THEME['text'], font=ctk.CTkFont('Segoe UI', self.scale_font(10)),
                      command=self.on_back).pack(side=tk.LEFT, padx=self.scale_size(20), pady=self.scale_size(17))

        info_left = ctk.CTkFrame(header, fg_color='transparent')
        info_left.pack(side=tk.LEFT, fill=tk.Y, padx=(self.scale_size(10), self.scale_size(20)), pady=self.scale_size(15))

        ctk.CTkLabel(info_left, text=self.title, font=ctk.CTkFont('Segoe UI', self.scale_font(14), 'bold'),
                    text_color=THEME['text'], anchor='w').pack(fill=tk.X)
        ctk.CTkLabel(info_left, text=THEME['diff_names'].get(self.difficulty, ''),
                    font=ctk.CTkFont('Segoe UI', self.scale_font(11)), text_color=THEME['text_muted'],
                    anchor='w').pack(fill=tk.X)

        self.time_label = ctk.CTkLabel(header, text="0:00", font=ctk.CTkFont('Segoe UI', self.scale_font(20), 'bold'),
                                       text_color=THEME['red'])
        self.time_label.pack(side=tk.RIGHT, padx=self.scale_size(25), pady=self.scale_size(20))

        self.give_up_btn = ctk.CTkButton(header, text="Сдаться", width=self.scale_size(100), height=self.scale_size(35),
                      fg_color=THEME['light'], hover_color='#8b0000',
                      text_color=THEME['text'], font=ctk.CTkFont('Segoe UI', self.scale_font(10)),
                      command=self.init_give_up)
        self.give_up_btn.pack(side=tk.RIGHT, padx=self.scale_size(20), pady=self.scale_size(17))

        self.confirm_give_up_btn = ctk.CTkButton(header, text="✓ Подтвердить", width=self.scale_size(130), height=self.scale_size(35),
                      fg_color='#8b0000', hover_color='#a52a2a',
                      text_color=THEME['text'], font=ctk.CTkFont('Segoe UI', self.scale_font(10), 'bold'),
                      command=self.give_up)

        progress_frame = ctk.CTkFrame(self, fg_color=THEME['card'])
        progress_frame.pack(fill=tk.X, padx=self.scale_size(30), pady=(self.scale_size(15), 0))

        ctk.CTkLabel(progress_frame, text="Прогресс", font=ctk.CTkFont('Segoe UI', self.scale_font(10)),
                    text_color=THEME['text_muted']).pack(anchor='w', padx=self.scale_size(20), pady=(self.scale_size(10), self.scale_size(5)))

        self.progress = ctk.CTkProgressBar(progress_frame, height=self.scale_size(12), corner_radius=self.scale_size(6),
                                           fg_color=THEME['light'], progress_color=THEME['green'])
        self.progress.pack(fill=tk.X, padx=self.scale_size(20), pady=(0, self.scale_size(10)))
        self.progress.set(0)

        self.progress_label = ctk.CTkLabel(progress_frame, text="0 / 0 символов",
                                          font=ctk.CTkFont('Segoe UI', self.scale_font(10)),
                                          text_color=THEME['text_muted'])
        self.progress_label.pack(anchor='e', padx=self.scale_size(20), pady=(0, self.scale_size(8)))

        text_container = ctk.CTkFrame(self, fg_color=THEME['card'])
        text_container.pack(fill=tk.BOTH, expand=True, padx=self.scale_size(30), pady=self.scale_size(15))

        ctk.CTkLabel(text_container, text="Наберите текст:", font=ctk.CTkFont('Segoe UI', self.scale_font(11)),
                    text_color=THEME['text_muted']).pack(anchor='w', padx=self.scale_size(20), pady=(self.scale_size(15), self.scale_size(5)))

        self.text_display = tk.Text(text_container, height=12,
                                    font=('Consolas', self.scale_font(15)),
                                    bg=THEME['light'], fg=THEME['text'],
                                    wrap='word', state='disabled',
                                    borderwidth=0, highlightthickness=0)
        self.text_display.pack(fill=tk.BOTH, expand=True, padx=self.scale_size(20), pady=(0, self.scale_size(15)))

        self.text_display.tag_configure('correct', foreground=THEME['green'])
        self.text_display.tag_configure('incorrect', foreground=THEME['red_light'], background='#4a1a1a')
        self.text_display.tag_configure('pending', foreground=THEME['text_muted'])
        self.text_display.tag_configure('current', foreground=THEME['bg'], background=THEME['red'])

        input_frame = ctk.CTkFrame(self, fg_color=THEME['card'])
        input_frame.pack(fill=tk.X, padx=self.scale_size(30), pady=(0, self.scale_size(30)))

        ctk.CTkLabel(input_frame, text="Ввод:", font=ctk.CTkFont('Segoe UI', self.scale_font(11)),
                    text_color=THEME['text_muted']).pack(anchor='w', padx=self.scale_size(20), pady=(self.scale_size(10), self.scale_size(5)))

        self.input_entry = ctk.CTkEntry(input_frame, height=self.scale_size(55), font=('Consolas', self.scale_font(16)),
                                        fg_color=THEME['light'], text_color=THEME['text'],
                                        border_width=2, border_color=THEME['red'])
        self.input_entry.pack(fill=tk.X, padx=self.scale_size(20), pady=(0, self.scale_size(15)))
        self.input_entry.bind('<Key>', self.on_key)

    def on_header_double_click(self, event) -> None:
        self.master.toggle_fullscreen()

    def update_display(self) -> None:
        self.update_text_display()
        self.update_progress()

    def update_text_display(self) -> None:
        self.text_display.configure(state='normal')
        self.text_display.delete('1.0', tk.END)
        for i, char in enumerate(self.text):
            if i < len(self.user_input):
                tag = 'correct' if self.user_input[i] == char else 'incorrect'
            else:
                tag = 'current' if i == len(self.user_input) else 'pending'
            self.text_display.insert(tk.END, char, tag)
        self.text_display.configure(state='disabled')

    def update_progress(self) -> None:
        progress = len(self.user_input) / len(self.text)
        self.progress.set(progress)
        self.progress_label.configure(text=f"{len(self.user_input)} / {len(self.text)} символов")

    def update_time(self) -> None:
        elapsed = (datetime.now() - self.start_time).total_seconds()
        m, s = int(elapsed // 60), int(elapsed % 60)
        self.time_label.configure(text=f"{m}:{s:02d}")

    def update_timer(self) -> None:
        if not self.finished:
            self.update_text_display()
            self.update_progress()
            self.update_time()
            self.after(TIMER_INTERVAL_MS, self.update_timer)

    def on_key(self, event) -> str:
        if self.finished:
            return 'break'
        if event.keysym in ('Shift_L', 'Shift_R', 'Control_L', 'Control_R',
                           'Alt_L', 'Alt_R', 'Caps_Lock', 'Escape'):
            return None
        if event.keysym == 'BackSpace':
            if self.user_input:
                self.user_input = self.user_input[:-1]
                self.update_display()
            return 'break'
        if len(event.char) >= 1:
            pos = len(self.user_input)
            if pos >= len(self.text):
                return 'break'
            expected = self.text[pos]
            actual = event.char
            if check_char_match(expected, actual):
                self.user_input += expected
                self.update_display()
                if len(self.user_input) == len(self.text):
                    self.finish_game()
            else:
                self.errors += 1
                self.update_display()
            return 'break'
        return None

    def init_give_up(self) -> None:
        if not self.give_up_mode:
            self.give_up_mode = True
            self.give_up_btn.pack_forget()
            self.confirm_give_up_btn.pack(side=tk.RIGHT, padx=self.scale_size(20), pady=self.scale_size(17))
            self.after(3000, self.cancel_give_up)
        else:
            self.give_up()

    def cancel_give_up(self) -> None:
        if self.give_up_mode and not self.finished:
            self.give_up_mode = False
            self.confirm_give_up_btn.pack_forget()
            self.give_up_btn.pack(side=tk.RIGHT, padx=self.scale_size(20), pady=self.scale_size(17))

    def give_up(self) -> None:
        self.finished = True
        self.input_entry.configure(state='disabled')
        self.master.minsize(int(MIN_WINDOW_WIDTH * self.scale), int(MIN_WINDOW_HEIGHT * self.scale))
        result = GameResult(
            score=0, accuracy=0, errors=self.errors,
            time=(datetime.now() - self.start_time).total_seconds(),
            rank='E', difficulty=self.difficulty, text_title=self.title,
            characters=len(self.text)
        )
        self.on_finish(result)

    def finish_game(self) -> None:
        self.finished = True
        self.input_entry.configure(state='disabled')
        self.master.minsize(int(MIN_WINDOW_WIDTH * self.scale), int(MIN_WINDOW_HEIGHT * self.scale))
        elapsed = (datetime.now() - self.start_time).total_seconds()
        total = len(self.user_input) + self.errors
        accuracy = (len(self.user_input) / total * 100) if total > 0 else 100
        multiplier = SCORE_MULTIPLIERS.get(self.difficulty, 1)
        score = max(0, int(len(self.user_input) * multiplier - self.errors * ERROR_PENALTY))
        rank = calc_rank(accuracy, self.errors)
        result = GameResult(
            score=score, accuracy=accuracy, errors=self.errors, time=elapsed,
            rank=rank, difficulty=self.difficulty, text_title=self.title,
            characters=len(self.text)
        )
        self.on_finish(result)
