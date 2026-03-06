import customtkinter as ctk
import tkinter as tk
from widgets import ScaledFrame
from config import THEME
from models import get_session, User


class AuthScreen(ScaledFrame):
    def __init__(self, parent, on_login):
        super().__init__(parent, fg_color=THEME['bg'])
        self.on_login = on_login
        self.create_widgets()

    def create_widgets(self):
        card = ctk.CTkFrame(self, fg_color=THEME['card'], corner_radius=self.scale_size(15))
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ctk.CTkLabel(card, text="Тренажёр ввода текста", font=ctk.CTkFont('Segoe UI', self.scale_font(24), 'bold'),
                    text_color=THEME['red']).pack(pady=(self.scale_size(40), self.scale_size(10)))
        ctk.CTkLabel(card, text="Войдите или зарегистрируйтесь", font=ctk.CTkFont('Segoe UI', self.scale_font(11)),
                    text_color=THEME['text_muted']).pack(pady=(0, self.scale_size(30)))

        form = ctk.CTkFrame(card, fg_color='transparent')
        form.pack(padx=self.scale_size(40), pady=self.scale_size(10))

        ctk.CTkLabel(form, text="Имя пользователя", font=ctk.CTkFont('Segoe UI', self.scale_font(11)),
                    text_color=THEME['text_muted'], anchor='w').pack(fill=tk.X)
        self.user_entry = ctk.CTkEntry(form, width=self.scale_size(280), height=self.scale_size(40),
                                       fg_color=THEME['light'], text_color=THEME['text'])
        self.user_entry.pack(fill=tk.X, pady=(0, self.scale_size(15)))
        self.user_entry.bind('<Return>', self.on_enter_key)

        ctk.CTkLabel(form, text="Пароль", font=ctk.CTkFont('Segoe UI', self.scale_font(11)),
                    text_color=THEME['text_muted'], anchor='w').pack(fill=tk.X)
        self.pass_entry = ctk.CTkEntry(form, width=self.scale_size(280), height=self.scale_size(40),
                                       fg_color=THEME['light'], text_color=THEME['text'], show='•')
        self.pass_entry.pack(fill=tk.X, pady=(0, self.scale_size(25)))
        self.pass_entry.bind('<Return>', self.on_enter_key)

        ctk.CTkButton(form, text="Войти / Регистрация", height=self.scale_size(45),
                      fg_color=THEME['red'], hover_color=THEME['red_light'],
                      text_color=THEME['text'], font=ctk.CTkFont('Segoe UI', self.scale_font(12), 'bold'),
                      command=self.login).pack(fill=tk.X)

        self.status = ctk.CTkLabel(card, text="", font=ctk.CTkFont('Segoe UI', self.scale_font(10)),
                                   text_color=THEME['red_light'])
        self.status.pack(pady=(self.scale_size(20), self.scale_size(35)))

    def on_enter_key(self, event) -> None:
        self.login()

    def login(self) -> None:
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()
        if not username:
            self.status.configure(text="Введите имя пользователя")
            return
        if not password:
            self.status.configure(text="Введите пароль")
            return
        with get_session() as session:
            user = session.query(User).filter_by(username=username, password=password).first()
            if user:
                self.on_login(user.id, user.username)
            else:
                exists = session.query(User).filter_by(username=username).first()
                if exists:
                    self.status.configure(text="Неверный пароль")
                else:
                    try:
                        new_user = User(username=username, password=password)
                        session.add(new_user)
                        session.flush()
                        self.on_login(new_user.id, new_user.username)
                    except Exception as e:
                        self.status.configure(text=f"Ошибка: {e}")
