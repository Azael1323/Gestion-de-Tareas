import os
import tkinter as tk
from tkinter import messagebox
import datetime

class Tarea:
    def __init__(self, nombre, estado, fecha_limite=None):
        self.nombre=nombre
        self.estado=estado
        self.fecha_limite=fecha_limite

    def __str__(self):
        return f"Tarea: {self.nombre}\nEstado: {self.estado}\nFecha limite: {self.fecha_limite}"

class GestorTareas:
    def __init__(self, archivo_tareas="tareas.txt"):
        self.archivo_tareas=archivo_tareas
    
    def agregar_tarea(self, tarea):
        with open(self.archivo_tareas, "a", encoding="utf-8") as archivo:
            archivo.write(f"{tarea.nombre},{tarea.estado},{tarea.fecha_limite}\n")

    def listar_tareas(self):
        if not os.path.exists(self.archivo_tareas):
            return "No hay tareas registradas."

        tareas_str = ""
        with open(self.archivo_tareas, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                nombre, estado, fecha_limite = linea.strip().split(",")
                tarea=Tarea(nombre, estado, fecha_limite)
                tareas_str+=str(tarea) + "\n" + "------------------------" + "\n"
        return tareas_str

    def buscar_tarea(self, nombre):
        if not os.path.exists(self.archivo_tareas):
            return None

        with open(self.archivo_tareas, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                nombre_tarea, estado, fecha_limite = linea.strip().split(",")
                if nombre_tarea.lower()==nombre.lower():
                    return Tarea(nombre_tarea, estado, fecha_limite)
        return None

    def borrar_tarea(self, nombre):
        tareas=[]
        if os.path.exists(self.archivo_tareas):
            with open(self.archivo_tareas, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    nombre_tarea, estado, fecha_limite=linea.strip().split(",")
                    if nombre_tarea!=nombre:
                        tareas.append((nombre_tarea, estado, fecha_limite))

        with open(self.archivo_tareas, "w", encoding="utf-8") as archivo:
            for tarea in tareas:
                archivo.write(f"{tarea[0]},{tarea[1]},{tarea[2]}\n")

    def tareas_proximas_a_vencer(self):
        if not os.path.exists(self.archivo_tareas):
            print("No hay tareas registradas.")
            return

        tareas_a_vencer = []
        hoy = datetime.datetime.now()

        with open(self.archivo_tareas, "r") as archivo:
            for linea in archivo:
                nombre, estado, fecha_limite = linea.strip().split(",")
                try:
                    fecha_limite = datetime.datetime.strptime(fecha_limite, "%d/%m/%Y")
                    # Verificar si la tarea está próxima a vencer (por ejemplo, en los próximos 7 días)
                    dias_hasta_vencimiento = (fecha_limite - hoy).days
                    if 0 <= dias_hasta_vencimiento <= 7:
                        tareas_a_vencer.append(Tarea(nombre, estado, fecha_limite))
                except ValueError:
                    # Manejar las fechas que no coinciden con el formato esperado
                    print(f"Fecha inválida para la tarea: {nombre}. Se omitirá esta tarea.")

        if tareas_a_vencer:
            mensaje_tareas = "----- TAREAS PRÓXIMAS A VENCER EN LOS PRÓXIMOS 7 DÍAS -----\n"
            for tarea in tareas_a_vencer:
                mensaje_tareas += str(tarea) + "\n" + "------------------------" + "\n"
            messagebox.showinfo("Tareas Próximas a Vencer", mensaje_tareas)
        else:
            messagebox.showinfo("Tareas Próximas a Vencer", "No hay tareas próximas a vencer en los próximos 7 días.")

def agregar_tarea_click(event=None):
    nombre_tarea = entry_nombre.get()
    estado_tarea = entry_estado.get()
    fecha_limite = entry_fecha.get()

    if nombre_tarea and estado_tarea and fecha_limite:
        nueva_tarea = Tarea(nombre_tarea, estado_tarea, fecha_limite)
        gestor_tareas.agregar_tarea(nueva_tarea)
        actualizar_listbox()
    else:
        campos_vacios = ""
        if not nombre_tarea:
            campos_vacios += "Nombre, "
        if not estado_tarea:
            campos_vacios += "Estado, "
        if not fecha_limite:
            campos_vacios += "Fecha"
        messagebox.showwarning("Campos vacíos", f"Por favor completa los siguientes campos: {campos_vacios}")

def listar_tareas_click():
    tareas=gestor_tareas.listar_tareas()
    text_tareas.delete("1.0", tk.END)
    text_tareas.insert(tk.END, tareas)

def buscar_tarea_click(event=None):
    nombre_buscar=entry_buscar.get()
    tarea_encontrada=gestor_tareas.buscar_tarea(nombre_buscar)
    if tarea_encontrada:
        messagebox.showinfo("Tarea encontrada", str(tarea_encontrada))
    else:
        messagebox.showinfo("Tarea no encontrada", "No se encontro la tarea con ese nombre.")

def borrar_tarea_click(event=None):
    nombre_borrar=entry_borrar.get()
    gestor_tareas.borrar_tarea(nombre_borrar)
    actualizar_listbox()
    messagebox.showinfo("Tarea borrada", "La tarea se ha borrado con exito.")

def actualizar_listbox():
    text_tareas.delete("1.0", tk.END)
    for tarea in gestor_tareas.tareas:
        text_tareas.insert(tk.END, str(tarea) + "\n------------------------\n")

def mostrar_tareas_proximas_a_vencer():
    gestor_tareas.tareas_proximas_a_vencer()

def actualizar_listbox():
    listar_tareas_click()

if __name__=="__main__":
    gestor_tareas=GestorTareas()

    ventana=tk.Tk()
    ventana.title("Gestion de Tareas")

    
    
    label_nombre=tk.Label(ventana, text="Nombre de la tarea:")
    entry_nombre=tk.Entry(ventana)
    label_estado=tk.Label(ventana, text="Estado de la tarea:")
    entry_estado=tk.Entry(ventana)
    label_fecha=tk.Label(ventana, text="Fecha limite (dd-mm-yyyy):")
    entry_fecha=tk.Entry(ventana)
    btn_agregar=tk.Button(ventana, text="Agregar tarea", command=agregar_tarea_click)

    label_buscar=tk.Label(ventana, text="Buscar tarea por nombre:")
    entry_buscar=tk.Entry(ventana)
    btn_buscar=tk.Button(ventana, text="Buscar tarea", command=buscar_tarea_click)

    label_borrar=tk.Label(ventana, text="Borrar tarea por nombre:")
    entry_borrar=tk.Entry(ventana)
    btn_borrar=tk.Button(ventana, text="Borrar tarea", command=borrar_tarea_click)

    text_tareas=tk.Text(ventana, width=50, height=10)
    
    btn_mostrar_tareas_vencer = tk.Button(ventana, text="Mostrar Tareas Próximas a Vencer", command=mostrar_tareas_proximas_a_vencer)
    btn_mostrar_tareas_vencer.grid(row=9, column=0, columnspan=2)

    # Asociar Enter con la función agregar_tarea_click
    entry_nombre.bind("<Return>", agregar_tarea_click)
    entry_estado.bind("<Return>", agregar_tarea_click)
    entry_fecha.bind("<Return>", agregar_tarea_click)  
    entry_buscar.bind("<Return>", buscar_tarea_click)
    entry_borrar.bind("<Return>", borrar_tarea_click)


    # Posicionar widgets
    label_nombre.grid(row=0, column=0)
    entry_nombre.grid(row=0, column=1)
    label_estado.grid(row=1, column=0)
    entry_estado.grid(row=1, column=1)
    label_fecha.grid(row=2, column=0)
    entry_fecha.grid(row=2, column=1)
    btn_agregar.grid(row=3, column=0, columnspan=2)

    label_buscar.grid(row=4, column=0)
    entry_buscar.grid(row=4, column=1)
    btn_buscar.grid(row=5, column=0, columnspan=2)

    label_borrar.grid(row=6, column=0)
    entry_borrar.grid(row=6, column=1)
    btn_borrar.grid(row=7, column=0, columnspan=2)

    text_tareas.grid(row=8, column=0, columnspan=2)



    # Mostrar las tareas existentes al inicio
    actualizar_listbox()

    ventana.mainloop()
