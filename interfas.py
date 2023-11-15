import os
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
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
            archivo.seek(0, 2)  # Mover el puntero al final del archivo

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
            mensaje_tareas = "--- TAREAS PRÓXIMAS A VENCER EN LOS PRÓXIMOS 7 DÍAS ---\n"
            for tarea in tareas_a_vencer:
                mensaje_tareas += str(tarea) + "\n" + "---------------------" + "\n"
            messagebox.showinfo("Tareas Próximas a Vencer", mensaje_tareas)
        else:
            messagebox.showinfo("Tareas Próximas a Vencer", "No hay tareas próximas a vencer en los próximos 7 días.")

def actualizar_listbox():
    listbox_tareas.delete(0, tk.END)
    with open(gestor_tareas.archivo_tareas, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            try:
                nombre, estado, fecha = linea.strip().split(",")
                tarea_info = f"Nombre: {nombre}. Estado: {estado}. Fecha: {fecha}."
                listbox_tareas.insert(tk.END, tarea_info)
            except ValueError:
                print(f"Error al leer la línea: {linea}. Se omite esta tarea.")

def seleccionar_tarea(event=None):
    # Elimina la manipulación automática del campo de entrada al seleccionar una tarea
    pass

def borrar_tarea_click(event=None):
    try:
        seleccion = listbox_tareas.curselection()
        if seleccion:
            nombre_borrar = listbox_tareas.get(seleccion)
            confirmacion = messagebox.askyesno("Confirmación", f"¿Seguro que deseas borrar la tarea:\n{nombre_borrar}?", icon='warning')
            if confirmacion:
                listbox_tareas.delete(seleccion)
                gestor_tareas.borrar_tarea(nombre_borrar)
                messagebox.showinfo("Tarea borrada", "La tarea se ha borrado con éxito.")
        else:
            messagebox.showwarning("Ninguna tarea seleccionada", "Por favor, selecciona una tarea antes de borrar.")
    except tk.TclError:
        messagebox.showwarning("Error", "No hay tareas en la lista.")

def agregar_tarea_click(event=None):
    nombre_tarea = entry_nombre.get()
    estado_tarea = entry_estado.get()
    fecha_limite = cal.get_date()

    if nombre_tarea and estado_tarea and fecha_limite:
        nueva_tarea = Tarea(nombre_tarea, estado_tarea, fecha_limite)
        gestor_tareas.agregar_tarea(nueva_tarea)

        # borrar los campos de entrada
        entry_nombre.delete(0, tk.END)
        entry_estado.delete(0, tk.END)
        cal.set_date("")  # Esto establecerá la fecha en blanco
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
    listbox_tareas.delete(0, tk.END)
    listbox_tareas.insert(tk.END, tareas)

def buscar_tarea_click(event=None):
    nombre_buscar=entry_buscar.get()
    tarea_encontrada=gestor_tareas.buscar_tarea(nombre_buscar)
    if tarea_encontrada:
        messagebox.showinfo("Tarea encontrada", str(tarea_encontrada))
    else:
        messagebox.showinfo("Tarea no encontrada", "No se encontro la tarea con ese nombre.")

def mostrar_tareas_proximas_a_vencer():
    gestor_tareas.tareas_proximas_a_vencer()

def filtrar_por_estado(estado_filtrado, orden):
    tareas = []
    with open(gestor_tareas.archivo_tareas, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            nombre, estado, fecha = linea.strip().split(",")
            tarea_info = f"Nombre: {nombre}. Estado: {estado}. Fecha: {fecha}."
            tareas.append(tarea_info)

    if estado_filtrado is not None:
        tareas = [tarea for tarea in tareas if f"Estado: {estado_filtrado.lower()}" in tarea.lower()]

    clave = lambda x: x.split(".")[1].split(": ")[1]
    tareas.sort(key=clave, reverse=(orden == "Descendente"))

    listbox_tareas.delete(0, tk.END)
    for tarea in tareas:
        listbox_tareas.insert(tk.END, tarea)

def filtrar_por_fecha(orden):
    tareas = []
    with open(gestor_tareas.archivo_tareas, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            nombre, estado, fecha = linea.strip().split(",")
            tarea_info = f"Nombre: {nombre}. Estado: {estado}. Fecha: {fecha}."
            tareas.append(tarea_info)

    clave = lambda x: datetime.datetime.strptime(x.split("Fecha: ")[1].replace('.', ''), "%d/%m/%Y")
    tareas.sort(key=clave, reverse=(orden == "Descendente"))

    listbox_tareas.delete(0, tk.END)
    for tarea in tareas:
        listbox_tareas.insert(tk.END, tarea)

def filtrar_por_nombre(orden):
    tareas = []
    with open(gestor_tareas.archivo_tareas, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            nombre, estado, fecha = linea.strip().split(",")
            tarea_info = f"Nombre: {nombre}. Estado: {estado}. Fecha: {fecha}."
            tareas.append(tarea_info)

    clave = lambda x: x.split(".")[0].split(": ")[1]
    tareas.sort(key=clave, reverse=(orden == "Descendente"))

    listbox_tareas.delete(0, tk.END)
    for tarea in tareas:
        listbox_tareas.insert(tk.END, tarea)

variable_filtro = None
variable_orden = None
estado_filtrado = None

def realizar_filtrado_desde_menu(opcion_filtrar, orden):
    if opcion_filtrar == "Estado":
        filtrar_por_estado(estado_filtrado, orden)
    elif opcion_filtrar == "Fecha":
        filtrar_por_fecha(orden)
    elif opcion_filtrar == "Nombre":
        filtrar_por_nombre(orden)
    else:
        print("Filtro no válido")

def realizar_filtrado(event=None):
    global variable_filtro, variable_orden
    opcion_filtrar = variable_filtro.get() if variable_filtro else None
    orden = variable_orden.get() if variable_orden else None
    if opcion_filtrar and orden:
        if opcion_filtrar == "Estado":
            estado_filtrado = "En proceso"
            filtrar_por_estado(estado_filtrado, orden)
        else:
            filtrar_por_fecha(orden) if opcion_filtrar == "Fecha" else filtrar_por_nombre(orden)

def cambiarTema():
    # El código de cambio de tema de Azael
    if ventana.cget("bg") == "white":
        # Aplicar el tema oscuro
        ventana.configure(bg="black")
        label_estado.configure(bg="black", fg="white")
        label_buscar.configure(bg="black", fg="white")
        label_fecha.configure(bg="black", fg="white")
        label_nombre.configure(bg="black", fg="white")
        entry_buscar.configure(bg="black", fg="white")
        entry_estado.configure(bg="black", fg="white")
        entry_fecha.configure(bg="black", fg="white")
        entry_nombre.configure(bg="black", fg="white")
        listbox_tareas.configure(bg="black", fg="white")
        btn_agregar.configure(bg="black", fg="white")
        btn_borrar.configure(bg="black", fg="white")
        btn_buscar.configure(bg="black", fg="white")
        btn_mostrar_tareas_vencer.configure(bg="black", fg="white")
    else:
        # Volver al tema claro
        ventana.configure(bg="white")
        label_estado.configure(bg="white", fg="black")
        label_buscar.configure(bg="white", fg="black")
        label_fecha.configure(bg="white", fg="black")
        label_nombre.configure(bg="white", fg="black")
        entry_buscar.configure(bg="white", fg="black")
        entry_estado.configure(bg="white", fg="black")
        entry_fecha.configure(bg="white", fg="black")
        entry_nombre.configure(bg="white", fg="black")
        listbox_tareas.configure(bg="white", fg="black")
        btn_agregar.configure(bg="white", fg="black")
        btn_borrar.configure(bg="white", fg="black")
        btn_buscar.configure(bg="white", fg="black")
        btn_mostrar_tareas_vencer.configure(bg="white", fg="black")

if __name__=="__main__":
    gestor_tareas=GestorTareas()

    ventana=tk.Tk()
    ventana.title("Gestion de Tareas")
    # Establecer el tema inicial en color blanco
    ventana.configure(bg="white")

    # Crear el menú superior
    menu_superior = tk.Menu(ventana)
    ventana.config(menu=menu_superior)

    # Crear los menús desplegables para filtrar
    menu_filtrar = tk.Menu(menu_superior, tearoff=0)
    menu_superior.add_cascade(label="Filtrar", menu=menu_filtrar)

    # Crear el menú "Cambiar Tema" con dos subopciones
    menu_cambiarTema = tk.Menu(menu_superior, tearoff=0)
    menu_superior.add_cascade(label="Cambiar Tema", menu=menu_cambiarTema)

    # Subopciones para el menú "Cambiar Tema"
    menu_cambiarTema.add_command(label="Realizar cambio", command=lambda: cambiarTema())


    menu_filtrar_estado = tk.Menu(menu_filtrar, tearoff=0)
    menu_filtrar.add_cascade(label="Estado", menu=menu_filtrar_estado)
    menu_filtrar_estado.add_command(label="Ascendente", command=lambda: realizar_filtrado_desde_menu("Estado", "Ascendente"))
    menu_filtrar_estado.add_command(label="Descendente", command=lambda: realizar_filtrado_desde_menu("Estado", "Descendente"))

    menu_filtrar_fecha = tk.Menu(menu_filtrar, tearoff=0)
    menu_filtrar.add_cascade(label="Fecha", menu=menu_filtrar_fecha)
    menu_filtrar_fecha.add_command(label="Ascendente", command=lambda: realizar_filtrado_desde_menu("Fecha", "Ascendente"))
    menu_filtrar_fecha.add_command(label="Descendente", command=lambda: realizar_filtrado_desde_menu("Fecha", "Descendente"))

    menu_filtrar_nombre = tk.Menu(menu_filtrar, tearoff=0)
    menu_filtrar.add_cascade(label="Nombre", menu=menu_filtrar_nombre)
    menu_filtrar_nombre.add_command(label="Ascendente", command=lambda: realizar_filtrado_desde_menu("Nombre", "Ascendente"))
    menu_filtrar_nombre.add_command(label="Descendente", command=lambda: realizar_filtrado_desde_menu("Nombre", "Descendente"))

    menu_superior.add_command(label="Salir", command=ventana.destroy)

    #--------    
    label_nombre=tk.Label(ventana, font=("Arial", 11), text="Nombre de la tarea:")
    entry_nombre=tk.Entry(ventana, width=50)
    label_estado=tk.Label(ventana, font=("Arial", 11), text="Estado de la tarea:")
    entry_estado=tk.Entry(ventana, width=50)
    label_fecha=tk.Label(ventana, font=("Arial", 11), text="Fecha limite (dd-mm-yyyy):")
    entry_fecha=tk.Entry(ventana, width=50)
    btn_agregar=tk.Button(ventana, font=("Arial", 11), text="Agregar tarea", command=agregar_tarea_click)

    label_buscar=tk.Label(ventana, font=("Arial", 11), text="Buscar tarea por nombre:")
    entry_buscar=tk.Entry(ventana, width=50)
    btn_buscar=tk.Button(ventana,  font=("Arial", 11), text="Buscar tarea", command=buscar_tarea_click)

    btn_borrar = tk.Button(ventana, font=("Arial", 11), text="Borrar tarea", command=borrar_tarea_click)

    listbox_tareas = tk.Listbox(ventana, font=("Arial", 12), width=55, height=10)
    listbox_tareas.grid(row=8, column=0, columnspan=2)
    listbox_tareas.bind("<<ListboxSelect>>", seleccionar_tarea)

    btn_mostrar_tareas_vencer = tk.Button(ventana, font=("Arial", 11),text="Mostrar Tareas Próximas a Vencer", command=mostrar_tareas_proximas_a_vencer)
    btn_mostrar_tareas_vencer.grid(row=9, column=0, columnspan=2)

    # Establecer a todos el color tema blanco por defecto.
    label_nombre.configure(bg="white", fg="black")
    label_estado.configure(bg="white", fg="black")
    label_fecha.configure(bg="white", fg="black")
    label_buscar.configure(bg="white", fg="black")
    btn_borrar.configure(bg="white", fg="black")
    btn_agregar.configure(bg="white", fg="black")
    btn_buscar.configure(bg="white", fg="black")
    btn_mostrar_tareas_vencer.configure(bg="white", fg="black")

    # Asociar Enter con la función agregar_tarea_click
    entry_nombre.bind("<Return>", agregar_tarea_click)
    entry_estado.bind("<Return>", agregar_tarea_click)
    entry_fecha.bind("<Return>", agregar_tarea_click)  
    entry_buscar.bind("<Return>", buscar_tarea_click)
    listbox_tareas.bind("<Double-Button-1>", seleccionar_tarea)  # Seleccionar tarea al hacer doble clic

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
    btn_buscar.grid(row=5, column=0)
    btn_borrar.grid(row=5, column=1)

    # Mostrar las tareas existentes al inicio
    actualizar_listbox()

    ventana.mainloop()

