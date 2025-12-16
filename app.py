import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import logica_db as logica
from datetime import datetime

def iniciar_app():
    root = tk.Tk()
    root.title("Sistema de Citas Médicas")
    root.geometry("720x650")
    root.resizable(False, False)

    medicos = ["Dr. Perez", "Dra. Gonzalez", "Dr. Ramirez"]

    # ==========================

    def validar_fecha(fecha):
        try:
            f = datetime.strptime(fecha, "%d/%m/%Y").date()
            return f >= datetime.today().date()
        except ValueError:
            return False

    def validar_hora(hora):
        try:
            datetime.strptime(hora, "%H:%M")
            return True
        except ValueError:
            return False

    # ==========================

    tk.Label(
        root,
        text="Sistema de Citas Médicas",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=10)

    # ==========================

    frame_form = tk.Frame(root)
    frame_form.pack(pady=5)

    def campo(texto):
        tk.Label(frame_form, text=texto).grid(sticky="w")
        e = tk.Entry(frame_form, width=30)
        e.grid(pady=2)
        return e

    entry_nombre = campo("Nombre del paciente")
    entry_fecha = campo("Fecha (DD/MM/AAAA)")
    entry_hora = campo("Hora (HH:MM)")

    tk.Label(frame_form, text="Médico").grid(sticky="w")
    combo_medico = ttk.Combobox(
        frame_form, values=medicos, state="readonly", width=28
    )
    combo_medico.current(0)
    combo_medico.grid(pady=2)

    def agendar():
        nombre = entry_nombre.get().strip().title()
        fecha = entry_fecha.get().strip()
        hora = entry_hora.get().strip()
        medico = combo_medico.get()

        if not nombre or not fecha or not hora:
            messagebox.showerror("Error", "Completa todos los campos")
            return

        if not validar_fecha(fecha):
            messagebox.showerror("Error", "Fecha inválida o pasada")
            return

        if not validar_hora(hora):
            messagebox.showerror("Error", "Hora inválida")
            return

        ok, mensaje = logica.agregar_cita(nombre, fecha, hora, medico)

        if ok:
            messagebox.showinfo("Éxito", mensaje)
            entry_nombre.delete(0, tk.END)
            entry_fecha.delete(0, tk.END)
            entry_hora.delete(0, tk.END)
            cargar_tabla()
        else:
            messagebox.showerror("Error", mensaje)

    tk.Button(
        frame_form, text="Agendar cita",
        bg="#1e88e5", fg="white",
        width=25, command=agendar
    ).grid(pady=10)

    # ==========================

    frame_tabla = tk.Frame(root)
    frame_tabla.pack(pady=10)

    columnas = ("ID", "Nombre", "Fecha", "Hora", "Médico")

    tabla = ttk.Treeview(
        frame_tabla,
        columns=columnas,
        show="headings",
        height=10
    )

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=130)

    tabla.column("ID", width=50)
    tabla.pack(side="left")

    scrollbar = ttk.Scrollbar(
        frame_tabla, orient="vertical", command=tabla.yview
    )
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def cargar_tabla(datos=None):
        for fila in tabla.get_children():
            tabla.delete(fila)

        citas = datos if datos else logica.obtener_citas()
        for c in citas:
            tabla.insert("", "end", values=c)

    cargar_tabla()

    # ==========================

    def editar_cita(event):
        seleccionado = tabla.selection()
        if not seleccionado:
            return

        valores = tabla.item(seleccionado)["values"]
        id_cita, nombre, fecha, hora, medico = valores

        ventana = tk.Toplevel(root)
        ventana.title("Editar cita")
        ventana.geometry("300x350")
        ventana.resizable(False, False)

        def campo_edit(texto, valor):
            tk.Label(ventana, text=texto).pack()
            e = tk.Entry(ventana)
            e.insert(0, valor)
            e.pack()
            return e

        e_nombre = campo_edit("Nombre", nombre)
        e_fecha = campo_edit("Fecha (DD/MM/AAAA)", fecha)
        e_hora = campo_edit("Hora (HH:MM)", hora)

        tk.Label(ventana, text="Médico").pack()
        combo = ttk.Combobox(
            ventana, values=medicos, state="readonly"
        )
        combo.set(medico)
        combo.pack(pady=5)

        def guardar():
            n = e_nombre.get().strip().title()
            f = e_fecha.get().strip()
            h = e_hora.get().strip()
            m = combo.get()

            if not validar_fecha(f):
                messagebox.showerror("Error", "Fecha inválida")
                return

            if not validar_hora(h):
                messagebox.showerror("Error", "Hora inválida")
                return

            ok, msg = logica.editar_cita(id_cita, n, f, h, m)
            if ok:
                messagebox.showinfo("OK", msg)
                ventana.destroy()
                cargar_tabla()
            else:
                messagebox.showerror("Error", msg)

        tk.Button(
            ventana, text="Guardar cambios",
            bg="#1e88e5", fg="white",
            width=20, command=guardar
        ).pack(pady=15)

    tabla.bind("<Double-1>", editar_cita)

    # ==========================
    
    frame_botones = tk.Frame(root)
    frame_botones.pack(pady=10)

    def cancelar_seleccion():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Selecciona una cita")
            return

        id_cita = tabla.item(seleccionado)["values"][0]

        if messagebox.askyesno("Confirmar", "¿Cancelar la cita?"):
            logica.eliminar_cita(id_cita)
            cargar_tabla()
            messagebox.showinfo("OK", "Cita cancelada")

    def buscar_por_nombre():
        nombre = simpledialog.askstring(
            "Buscar citas", "Nombre del paciente"
        )
        if not nombre:
            return
        datos = logica.buscar_citas_por_nombre(nombre.title())
        cargar_tabla(datos)

    tk.Button(
        frame_botones,
        text="Cancelar cita seleccionada",
        bg="#e53935", fg="white",
        width=30,
        command=cancelar_seleccion
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        frame_botones,
        text="Buscar por nombre",
        width=30,
        command=buscar_por_nombre
    ).grid(row=0, column=1, padx=5)

    root.mainloop()
