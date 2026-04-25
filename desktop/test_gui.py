import customtkinter as ctk

app = ctk.CTk()
app.geometry("400x300")
app.title("Test")
ctk.CTkLabel(app, text="Если видите это - GUI работает!").pack(pady=20)
ctk.CTkButton(app, text="OK", command=app.destroy).pack()
app.mainloop()
print("Окно закрыто")