import customtkinter as ctk
import httpx
from ui.main_window import MainWindow

class AuthWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("300x350")
        self.title("Вход")
        self.resizable(False, False)
        ctk.CTkLabel(self, text="Email").pack(pady=(20,5), padx=20, fill="x")
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack(padx=20, pady=5, fill="x")
        ctk.CTkLabel(self, text="Пароль").pack(pady=(10,5), padx=20, fill="x")
        self.pass_entry = ctk.CTkEntry(self, show="*")
        self.pass_entry.pack(padx=20, pady=5, fill="x")
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=5)
        ctk.CTkButton(self, text="Войти", command=self.login).pack(pady=10)

    def login(self):
        try:
            with httpx.Client() as client:
                res = client.post("http://138.124.85.61:8000/auth/token", data={"email": self.email_entry.get(), "password": self.pass_entry.get()})
                if res.status_code == 200:
                    self.parent.db.set_meta("auth_token", res.json()["access_token"])
                    self.parent.db.token = res.json()["access_token"]
                    self.destroy()
                    self.parent.main_ui = MainWindow(self.parent)
                    self.parent.main_ui.pack(fill="both", expand=True)
                else:
                    self.status_label.configure(text="Неверные данные", text_color="red")
        except Exception:
            self.status_label.configure(text="Ошибка сервера", text_color="red")