import tkinter as tk
from tkinter import messagebox
import logica_db as logica
import app

logica.crear_tablas()

def entrar():
    user = entry_user.get().strip()
    pwd = entry_pass.get().strip()

    if logica.validar_login(user, pwd):
        ventana.destroy()
        app.iniciar_app()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

ventana = tk.Tk()
ventana.title("Login")
ventana.geometry("350x300")
ventana.resizable(False, False)

tk.Label(ventana, text="LOGIN", font=("Segoe UI", 18, "bold")).pack(pady=20)

tk.Label(ventana, text="Usuario").pack()
entry_user = tk.Entry(ventana)
entry_user.pack()

tk.Label(ventana, text="Contraseña").pack()
entry_pass = tk.Entry(ventana, show="*")
entry_pass.pack()

tk.Button(
    ventana, text="Entrar",
    bg="#1e88e5", fg="white",
    width=20, command=entrar
).pack(pady=20)

ventana.mainloop()
