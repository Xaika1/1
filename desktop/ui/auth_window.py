import customtkinter as ctk
import httpx

class AuthWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.geometry("300x350")
        self.title("Вход")
        self.resizable(False, False)
        self.grab_set()

        ctk.CTkLabel(self, text="Email").pack(pady=(20, 5), padx=20, fill="x")
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(self, text="Пароль").pack(pady=(10, 5), padx=20, fill="x")
        self.pass_entry = ctk.CTkEntry(self, show="*")
        self.pass_entry.pack(padx=20, pady=5, fill="x")

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.pack(pady=5)

        ctk.CTkButton(self, text="Войти", command=self.login).pack(pady=10)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not email or not password:
            self.status_label.configure(text="Заполните все поля", text_color="red")
            return

        try:
            self.status_label.configure(text="Подключение...", text_color="yellow")
            self.update()

            with httpx.Client(timeout=10.0) as client:
                res = client.post(
                    "http://138.124.85.61:8000/auth/token",
                    data={"email": email, "password": password}
                )
                if res.status_code == 200:
                    token_data = res.json()
                    self.parent.db.set_meta("auth_token", token_data["access_token"])
                    self.parent.db.token = token_data["access_token"]
                    self.destroy()
                    self.parent.show_main_window()
                else:
                    self.status_label.configure(text=f"Ошибка {res.status_code}: Неверные данные", text_color="red")
        except httpx.ConnectError:
            self.status_label.configure(text="Нет подключения к серверу", text_color="red")
        except Exception as e:
            self.status_label.configure(text=f"Ошибка: {str(e)}", text_color="red")