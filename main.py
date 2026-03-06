import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os

from config import THEME, MIN_TEXT_LENGTH, MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT
from models import get_session, User
from database import (
    load_window_size, save_window_size, load_session, clear_session, save_session,
    copy_default_texts, load_custom_texts, save_custom_texts
)
from widgets import ScaledFrame
from screens import AuthScreen, MainMenuScreen, LevelScreen, GameScreen, ResultsScreen


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Тренажёр ввода текста")

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        base_w, base_h = 1920, 1080
        self.scale = min(screen_w / base_w, screen_h / base_h)
        self.scale = max(0.7, min(1.5, self.scale))

        saved_w, saved_h, is_fullscreen = load_window_size()

        if saved_w and saved_h:
            self.geometry(f"{saved_w}x{saved_h}")
        else:
            width = int(950 * self.scale)
            height = int(700 * self.scale)
            self.geometry(f"{width}x{height}")

        self.minsize(int(850 * self.scale), int(600 * self.scale))

        self.is_fullscreen = is_fullscreen
        if is_fullscreen:
            self.attributes('-fullscreen', True)

        self.current_level_screen = None
        self.user_id = None
        self.username = None
        self.text_data = None
        self.difficulty = None

        self.bind('<F11>', self.on_f11_key)
        self.bind('<Escape>', self.on_escape_key)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.show_auth()

    def on_f11_key(self, event) -> None:
        self.toggle_fullscreen()

    def on_escape_key(self, event) -> None:
        self.exit_fullscreen()

    def toggle_fullscreen(self) -> None:
        self.is_fullscreen = not self.is_fullscreen
        self.attributes('-fullscreen', self.is_fullscreen)
        save_window_size(self.winfo_width(), self.winfo_height(), self.is_fullscreen)

    def exit_fullscreen(self) -> None:
        if self.is_fullscreen:
            self.toggle_fullscreen()

    def on_closing(self) -> None:
        save_window_size(self.winfo_width(), self.winfo_height(), self.is_fullscreen)
        self.destroy()

    def clear(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()

    def show_auth(self) -> None:
        self.clear()
        AuthScreen(self, self.on_auth_success).pack(fill=tk.BOTH, expand=True)

    def on_auth_success(self, user_id: int, username: str) -> None:
        self.user_id = user_id
        self.username = username
        save_session(user_id, username, '')
        self.show_menu()

    def show_menu(self) -> None:
        self.clear()
        self.current_level_screen = None
        MainMenuScreen(self, self.username, self.show_levels, self.load_custom_text, self.logout).pack(fill=tk.BOTH, expand=True)

    def logout(self) -> None:
        self.user_id = None
        self.username = None
        clear_session()
        self.show_auth()

    def load_custom_text(self) -> None:
        path = filedialog.askopenfilename(title="Выберите текстовый файл",
                                          filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if len(content) < MIN_TEXT_LENGTH:
                    messagebox.showwarning("Предупреждение", f"Текст слишком короткий (минимум {MIN_TEXT_LENGTH} символов)")
                    return
                custom_texts = load_custom_texts()
                custom_texts.append({'title': os.path.basename(path), 'text': content})
                save_custom_texts(custom_texts)
                if hasattr(self, 'current_level_screen'):
                    self.current_level_screen.custom_texts = custom_texts
                    if self.current_level_screen.difficulty == 'custom':
                        self.current_level_screen.update_list()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")

    def show_levels(self) -> None:
        self.clear()
        level_screen = LevelScreen(self, self.show_menu, self.start_game, self.load_custom_text)
        level_screen.pack(fill=tk.BOTH, expand=True)
        self.current_level_screen = level_screen

    def start_game(self, text_data: dict, difficulty: str) -> None:
        self.clear()
        self.text_data = text_data
        self.difficulty = difficulty
        GameScreen(self, text_data, difficulty, self.show_results, self.show_levels, self.give_up).pack(fill=tk.BOTH, expand=True)

    def give_up(self) -> None:
        self.show_levels()

    def show_results(self, result) -> None:
        self.clear()
        self.current_level_screen = None
        ResultsScreen(self, result, self.retry_game, self.show_levels, self.show_menu).pack(fill=tk.BOTH, expand=True)

    def retry_game(self) -> None:
        self.start_game(self.text_data, self.difficulty)


if __name__ == '__main__':
    copy_default_texts()

    user_id, username, _ = load_session()
    app = App()
    if user_id and username:
        with get_session() as session:
            user = session.query(User).filter_by(id=user_id, username=username).first()
            if user:
                app.user_id = user.id
                app.username = user.username
                app.show_menu()
            else:
                clear_session()
    app.mainloop()
