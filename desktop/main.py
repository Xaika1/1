import customtkinter as ctk
import threading
import os
import sys
import traceback
from datetime import datetime

# Сначала импорты, потом код
try:
    from core.sync_engine import SyncEngine
    from core.scheduler import ReminderScheduler
    from ui.auth_window import AuthWindow
    from ui.main_window import MainWindow

    print("[OK] Все модули импортированы")
except Exception as e:
    print(f"[ERROR] Ошибка импорта: {e}")
    traceback.print_exc()
    sys.exit(1)


class CalendarApp(ctk.CTk):
    def __init__(self):
        print("[INFO] Создание окна приложения...")
        try:
            super().__init__()
            self.geometry("1200x800")
            self.title("Календарь")
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")

            cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
            os.makedirs(cache_dir, exist_ok=True)
            print(f"[INFO] Путь к кэшу: {cache_dir}")

            self.db = SyncEngine(os.path.join(cache_dir, "calendar_cache.db"), "http://138.124.85.61:8000")
            print("[OK] Синхронизатор создан")

            self.scheduler = ReminderScheduler(self.db)
            print("[OK] Планировщик создан")

            self.main_ui = None

            self.protocol("WM_DELETE_WINDOW", self.on_close)
            print("[INFO] Проверка авторизации...")
            self.check_auth()

            self.bind("<Configure>", self.on_resize)
            self.after(30000, self.auto_sync)
            print("[OK] Приложение инициализировано")
        except Exception as e:
            print(f"[FATAL ERROR] В __init__: {e}")
            traceback.print_exc()
            sys.exit(1)

    def check_auth(self):
        try:
            token = self.db.get_meta("auth_token")
            if token:
                print("[AUTH] Токен найден.")
                self.db.token = token
                self.withdraw()
                self.after(100, self.show_main_window)
            else:
                print("[AUTH] Токен не найден.")
                AuthWindow(self)
        except Exception as e:
            print(f"[ERROR] check_auth: {e}")
            self.show_main_window()

    def show_main_window(self):
        try:
            if self.main_ui:
                self.main_ui.destroy()
            print("[UI] Создание MainWindow...")
            self.main_ui = MainWindow(self)
            self.main_ui.pack(fill="both", expand=True)
            print("[UI] MainWindow добавлен")
        except Exception as e:
            print(f"[ERROR] В show_main_window: {e}")
            traceback.print_exc()

    def on_close(self):
        print("[INFO] Закрытие приложения...")
        self.scheduler.scheduler.shutdown()
        self.destroy()

    def on_resize(self, event):
        if self.main_ui:
            self.main_ui.update_layout()

    def auto_sync(self):
        threading.Thread(target=self.db.pull, daemon=True).start()
        self.after(30000, self.auto_sync)


if __name__ == "__main__":
    print(">>> Запуск приложения <<<")
    try:
        app = CalendarApp()
        print(">>> Запуск mainloop <<<")
        app.mainloop()
        print(">>> Приложение закрыто <<<")
    except Exception as e:
        print(f"[CRASH] Приложение упало: {e}")
        traceback.print_exc()