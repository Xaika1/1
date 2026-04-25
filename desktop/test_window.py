import customtkinter as ctk
import sys

print("1. Запуск теста CustomTkinter...")
try:
    app = ctk.CTk()
    print("2. Объект приложения создан.")
    app.geometry("400x300")
    app.title("Тестовое окно")

    label = ctk.CTkLabel(app, text="Если вы видите этот текст — GUI работает!")
    label.pack(pady=100)

    print("3. Вызов mainloop()...")
    app.mainloop()
    print("4. Mainloop завершен.")
except Exception as e:
    print(f"ОШИБКА: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)