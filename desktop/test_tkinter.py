import tkinter as tk

print("1. Импорт tkinter")
root = tk.Tk()
root.title("Pure Tkinter Test")
root.geometry("300x200")
tk.Label(root, text="Если видите это - Python GUI работает").pack(expand=True)
print("2. Окно создано. Запуск цикла...")
try:
    root.mainloop()
except KeyboardInterrupt:
    print("3. Цикл прерван вручную")
print("4. Программа завершена")