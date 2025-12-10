# main.py (Versión 3.2 - Con Módulo de Calificación)
import tkinter as tk
import datetime
from tkinter import messagebox, simpledialog, ttk
# Importamos lógica
from modules.auth import login_usuario, registrar_usuario
from modules.ciclos import obtener_ciclos_por_usuario, crear_ciclo, obtener_max_trabajos, establecer_max_trabajos
from modules.alumnos import agregar_alumno, obtener_alumnos, registrar_calificacion, calcular_promedio_periodo, obtener_calificaciones_alumno
from modules.alumnos import agregar_alumno, obtener_alumnos, registrar_calificacion, calcular_promedio_periodo, obtener_calificaciones_alumno, generar_reporte_boleta # <--- AGREGADO
from modules.asistencia import obtener_asistencia_fecha, guardar_asistencia_bloque

# --- CONSTANTES VISUALES ---
FONT_TITLE = ("Arial", 16, "bold")
FONT_SUBTITLE = ("Arial", 12, "bold")
FONT_NORMAL = ("Arial", 10)
COLOR_PRIMARY = "#2196F3"
COLOR_SUCCESS = "#4CAF50"
COLOR_BG_DARK = "#333333"

# Definimos los campos formativos aquí (podrías moverlos a config.py después)
CAMPOS_FORMATIVOS = ["Lenguajes", "Saberes y P.", "Etica Nat.", "De lo Humano"]

class SistemaEscolarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Escolar v3.2")
        self.usuario_id = None 
        self.ciclo_actual_id = None
        self.ciclo_actual_nombre = None
        self.ciclo_actual_encuadre = None # Para calcular promedios
        
        self.mostrar_login()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------- LOGIN ----------------
    def mostrar_login(self):
        self.limpiar_ventana()
        self.root.geometry("400x350")
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)
        
        tk.Label(frame, text="Iniciar Sesión", font=FONT_TITLE).pack(pady=10)
        tk.Label(frame, text="Usuario:", font=FONT_NORMAL).pack(anchor="w")
        self.entry_user = tk.Entry(frame)
        self.entry_user.pack(fill="x", pady=5)
        
        tk.Label(frame, text="Contraseña:", font=FONT_NORMAL).pack(anchor="w")
        self.entry_pass = tk.Entry(frame, show="*")
        self.entry_pass.pack(fill="x", pady=5)
        
        tk.Button(frame, text="Entrar", bg=COLOR_SUCCESS, fg="white", command=self.accion_login).pack(fill="x", pady=15)
        tk.Button(frame, text="Registrarse", fg="blue", relief="flat", command=self.mostrar_registro).pack()

    def mostrar_registro(self):
        self.limpiar_ventana()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)
        tk.Label(frame, text="Registro", font=FONT_TITLE).pack(pady=10)
        
        tk.Label(frame, text="Usuario:", font=FONT_NORMAL).pack(anchor="w")
        self.entry_user_reg = tk.Entry(frame)
        self.entry_user_reg.pack(fill="x", pady=5)
        tk.Label(frame, text="Contraseña:", font=FONT_NORMAL).pack(anchor="w")
        self.entry_pass_reg = tk.Entry(frame, show="*")
        self.entry_pass_reg.pack(fill="x", pady=5)
        
        tk.Button(frame, text="Registrar", bg=COLOR_PRIMARY, fg="white", command=self.accion_registro).pack(fill="x", pady=15)
        tk.Button(frame, text="Volver", command=self.mostrar_login).pack()

    def accion_login(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()
        uid = login_usuario(u, p)
        if uid:
            self.usuario_id = uid
            self.mostrar_dashboard()
        else:
            messagebox.showerror("Error", "Datos incorrectos")

    def accion_registro(self):
        u = self.entry_user_reg.get()
        p = self.entry_pass_reg.get()
        exito, msg = registrar_usuario(u, p)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.mostrar_login()
        else:
            messagebox.showerror("Error", msg)

    # ---------------- DASHBOARD ----------------
    def mostrar_dashboard(self):
        self.limpiar_ventana()
        self.root.geometry("900x600")
        
        # Header
        header = tk.Frame(self.root, bg=COLOR_BG_DARK, height=50)
        header.pack(fill="x")
        tk.Label(header, text="Mis Ciclos Escolares", fg="white", bg=COLOR_BG_DARK, font=FONT_TITLE).pack(side="left", padx=15, pady=10)
        tk.Button(header, text="Salir", bg="#F44336", fg="white", command=self.mostrar_login).pack(side="right", padx=15)

        # Body
        body = tk.Frame(self.root, padx=20, pady=20)
        body.pack(fill="both", expand=True)
        
        tk.Button(body, text="+ Nuevo Grupo", bg=COLOR_PRIMARY, fg="white", command=self.popup_crear_ciclo).pack(anchor="w", pady=10)
        
        cols = ("ID", "Nombre", "Tareas", "Trabajos", "Examen")
        self.tree_ciclos = ttk.Treeview(body, columns=cols, show='headings')
        for c in cols: self.tree_ciclos.heading(c, text=c)
        self.tree_ciclos.column("ID", width=40)
        self.tree_ciclos.pack(fill="both", expand=True)
        self.tree_ciclos.bind("<Double-1>", self.seleccionar_ciclo)
        
        self.cargar_ciclos()

    def cargar_ciclos(self):
        for i in self.tree_ciclos.get_children(): self.tree_ciclos.delete(i)
        lista = obtener_ciclos_por_usuario(self.usuario_id)
        for c in lista:
            # c = (id, nombre, tareas, trabajos, proyecto, valores, examen)
            self.tree_ciclos.insert("", "end", values=(c[0], c[1], f"{c[2]}%", f"{c[3]}%", f"{c[6]}%"))
            # Guardamos el encuadre en memoria temporalmente (truco sucio pero efectivo)
            # Idealmente haríamos otra query, pero aquí aprovechamos que ya tenemos los datos
            if self.ciclo_actual_id == c[0]:
                self.ciclo_actual_encuadre = {
                    'tareas': c[2], 'trabajos': c[3], 'proyecto': c[4], 'valores': c[5], 'examen': c[6]
                }

    def popup_crear_ciclo(self):
        # En lugar de usar simpledialog, llamamos a nuestra nueva ventana personalizada
        VentanaNuevoCiclo(self.root, self.usuario_id, self.callback_ciclo_creado)

    def callback_ciclo_creado(self):
        # Esta función se ejecutará cuando la ventana secundaria termine con éxito
        self.cargar_ciclos()
    def seleccionar_ciclo(self, event):
        item = self.tree_ciclos.selection()
        if not item: return
        vals = self.tree_ciclos.item(item, "values")
        
        # --- CORRECCIÓN AQUÍ: Convertir a int explícitamente ---
        try:
            self.ciclo_actual_id = int(vals[0]) 
        except ValueError:
            return # Si falla la conversión, salimos para evitar errores
            
        self.ciclo_actual_nombre = vals[1]
        
        # Buscar el encuadre correcto en la lista
        self.ciclo_actual_encuadre = None # Reseteamos por seguridad
        
        lista = obtener_ciclos_por_usuario(self.usuario_id)
        for c in lista:
            # Ahora sí comparamos peras con peras (int == int)
            if c[0] == self.ciclo_actual_id:
                self.ciclo_actual_encuadre = {
                    'tareas': c[2], 'trabajos': c[3], 'proyecto': c[4], 'valores': c[5], 'examen': c[6]
                }
                break
        
        # Red de seguridad: Si por alguna razón extraña no lo encontró, poner default
        if self.ciclo_actual_encuadre is None:
            self.ciclo_actual_encuadre = {'tareas':10, 'trabajos':45, 'proyecto':5, 'valores':20, 'examen':20}

        self.mostrar_vista_grupo()
    # ---------------- VISTA GRUPO ----------------
    def mostrar_vista_grupo(self):
        self.limpiar_ventana()
        
        header = tk.Frame(self.root, bg=COLOR_PRIMARY, height=50)
        header.pack(fill="x")
        tk.Button(header, text="< Volver", bg="#1976D2", fg="white", relief="flat", command=self.mostrar_dashboard).pack(side="left", padx=10, pady=10)
        tk.Label(header, text=f"Grupo: {self.ciclo_actual_nombre}", fg="white", bg=COLOR_PRIMARY, font=FONT_TITLE).pack(side="left", padx=5)

        body = tk.Frame(self.root, padx=20, pady=20)
        body.pack(fill="both", expand=True)

        acciones = tk.Frame(body)
        acciones.pack(fill="x", pady=10)
        tk.Button(acciones, text="+ Alumno", bg=COLOR_SUCCESS, fg="white", command=self.popup_add_alumno).pack(side="left", padx=5)
        
        #BOTON PARA TOMAR ASISTENCIA
        tk.Button(acciones, text="Pasar Lista", bg="#009688", fg="white", command=self.abrir_ventana_asistencia).pack(side="left", padx=5)

        # NUEVO BOTÓN PARA VER BOLETA
        tk.Button(acciones, text="Ver Boleta", bg="#9C27B0", fg="white", command=self.abrir_ventana_boleta).pack(side="left", padx=5)

        # --- BOTÓN NARANJA CONECTADO ---
        tk.Button(acciones, text="Capturar Calificaciones", bg="#FF9800", fg="black", command=self.abrir_ventana_calificar).pack(side="left", padx=5)

        tk.Label(body, text="Selecciona un alumno para calificar:", font=("Arial", 9, "italic")).pack(anchor="w")

        cols = ("ID", "Nombre")
        self.tree_alumnos = ttk.Treeview(body, columns=cols, show='headings')
        self.tree_alumnos.heading("ID", text="ID"); self.tree_alumnos.column("ID", width=50)
        self.tree_alumnos.heading("Nombre", text="Nombre Alumno"); self.tree_alumnos.column("Nombre", width=400)
        self.tree_alumnos.pack(fill="both", expand=True)
        
        self.cargar_alumnos()

    def abrir_ventana_asistencia(self):
        VentanaAsistencia(self.root, self.ciclo_actual_id, self.ciclo_actual_nombre)

    def cargar_alumnos(self):
        for i in self.tree_alumnos.get_children(): self.tree_alumnos.delete(i)
        lista = obtener_alumnos(self.ciclo_actual_id)
        for al in lista:
            self.tree_alumnos.insert("", "end", values=al)

    def popup_add_alumno(self):
        nom = simpledialog.askstring("Alumno", "Nombre completo:")
        if nom:
            agregar_alumno(self.ciclo_actual_id, nom)
            self.cargar_alumnos()

    # ---------------- LÓGICA DE CALIFICACIÓN ----------------
    def abrir_ventana_calificar(self):
        # 0. VALIDACIÓN DE SEGURIDAD (Nuevo)
        if self.ciclo_actual_encuadre is None:
            messagebox.showerror("Error Crítico", "No se cargó la configuración del ciclo.\nIntenta volver al menú principal y entrar de nuevo.")
            return
        # 1. Validar selección
        seleccion = self.tree_alumnos.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Primero selecciona un alumno de la lista.")
            return
        
        datos_alumno = self.tree_alumnos.item(seleccion, "values") # (ID, Nombre)
        id_alumno = int(datos_alumno[0])
        nombre_alumno = datos_alumno[1]

        # 2. Abrir Ventana Popup (Toplevel)
        VentanaCalificar(self.root, id_alumno, nombre_alumno, self.ciclo_actual_id, self.ciclo_actual_encuadre)

    def abrir_ventana_boleta(self):
        seleccion = self.tree_alumnos.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un alumno para ver su boleta.")
            return

        item = self.tree_alumnos.item(seleccion, "values")
        id_alumno = int(item[0])
        nombre_alumno = item[1]

        if self.ciclo_actual_encuadre is None:
            messagebox.showerror("Error", "Error de carga de encuadre.")
            return

        VentanaBoleta(self.root, id_alumno, nombre_alumno, self.ciclo_actual_id, self.ciclo_actual_encuadre)


# =========================================================
# CLASE VENTANA ASISTENCIA (CHECKBOXES)
# =========================================================
class VentanaAsistencia:
    def __init__(self, parent, ciclo_id, nombre_ciclo):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Asistencia: {nombre_ciclo}")
        self.window.geometry("450x600")
        
        self.ciclo_id = ciclo_id
        
        # --- Cabecera con Fecha ---
        frame_top = tk.Frame(self.window, pady=10)
        frame_top.pack(fill="x")
        
        tk.Label(frame_top, text="Fecha (DD/MM/AAAA):").pack(side="left", padx=10)
        
        self.ent_fecha = tk.Entry(frame_top, width=12)
        # Poner fecha de hoy por defecto
        hoy = datetime.datetime.now().strftime("%d/%m/%Y")
        self.ent_fecha.insert(0, hoy)
        self.ent_fecha.pack(side="left")
        
        tk.Button(frame_top, text="Cargar Historial", command=self.cargar_lista).pack(side="left", padx=10)
        tk.Button(self.window, text="GUARDAR ASISTENCIA", bg="#009688", fg="white", font=("Arial", 12, "bold"), command=self.guardar_cambios).pack(fill="x", padx=20, pady=20)

        # --- Botones de Selección Rápida ---
        frame_tools = tk.Frame(self.window)
        frame_tools.pack(fill="x", padx=20)
        tk.Button(frame_tools, text="Marcar Todos", command=self.marcar_todos, font=("Arial", 8)).pack(side="left")
        tk.Button(frame_tools, text="Desmarcar Todos", command=self.desmarcar_todos, font=("Arial", 8)).pack(side="left", padx=5)

        # --- ÁREA SCROLLABLE (Truco técnico para listas largas) ---
        # 1. Creamos un Canvas (lienzo) y un Scrollbar
        self.canvas = tk.Canvas(self.window)
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        
        # 2. Creamos un Frame DENTRO del Canvas (aquí van los checkboxes)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        # 3. Configuramos el scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # 4. Empaquetamos todo
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Diccionario para guardar las variables de los checkboxes {alumno_id: IntVariable}
        self.vars_asistencia = {} 
        
        # Botón Guardar (Siempre visible abajo)
        tk.Button(self.window, text="GUARDAR ASISTENCIA", bg="#009688", fg="white", font=("Arial", 12, "bold"), command=self.guardar_cambios).pack(fill="x", padx=20, pady=20)

        # Cargar alumnos al iniciar
        self.cargar_lista()

    def cargar_lista(self):
        # 1. Limpiar lista visual anterior
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.vars_asistencia = {}

        # 2. Obtener alumnos del grupo
        alumnos = obtener_alumnos(self.ciclo_id) # [(id, nombre), ...]
        
        # 3. Obtener si ya hay asistencia guardada para esa fecha
        fecha = self.ent_fecha.get().strip()
        historial = obtener_asistencia_fecha(self.ciclo_id, fecha) # {id: 1, id: 0}
        
        # 4. Generar Checkboxes
        for al_id, al_nombre in alumnos:
            # Variable de control (1=Check, 0=Uncheck)
            var = tk.IntVar()
            
            # Lógica: Si hay historial, usamos eso. Si no, por defecto TODOS PRESENTES (1)
            if al_id in historial:
                var.set(historial[al_id])
            else:
                var.set(1) # Por defecto "Presente"
            
            self.vars_asistencia[al_id] = var
            
            # Crear el Checkbutton
            c = tk.Checkbutton(self.scrollable_frame, text=al_nombre, variable=var, font=("Arial", 10), anchor="w")
            c.pack(fill="x", pady=2)
            
    def guardar_cambios(self):
        fecha = self.ent_fecha.get().strip()
        if not fecha:
            messagebox.showwarning("Error", "La fecha es obligatoria")
            return

        # Recolectar datos
        datos_para_guardar = []
        for al_id, var in self.vars_asistencia.items():
            estado = var.get() # 1 o 0
            datos_para_guardar.append((al_id, estado))
            
        # Enviar al backend
        if guardar_asistencia_bloque(fecha, datos_para_guardar):
            messagebox.showinfo("Éxito", f"Asistencia del {fecha} guardada.")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar la asistencia.")

    def marcar_todos(self):
        for var in self.vars_asistencia.values(): var.set(1)

    def desmarcar_todos(self):
        for var in self.vars_asistencia.values(): var.set(0)

# =========================================================
# CLASE VENTANA CREAR NUEVO CICLO (CONFIGURACIÓN)
# =========================================================
class VentanaNuevoCiclo:
    def __init__(self, parent, usuario_id, callback_exito):
        self.window = tk.Toplevel(parent)
        self.window.title("Nuevo Grupo y Encuadre")
        self.window.geometry("400x450")
        
        self.usuario_id = usuario_id
        self.callback = callback_exito
        
        # --- UI ---
        tk.Label(self.window, text="Configuración del Grupo", font=("Arial", 14, "bold"), fg="#2196F3").pack(pady=15)
        
        # Nombre
        tk.Label(self.window, text="Nombre del Grupo (Ej. Matemáticas A):").pack(anchor="w", padx=20)
        self.ent_nombre = tk.Entry(self.window)
        self.ent_nombre.pack(fill="x", padx=20, pady=5)
        
        tk.Label(self.window, text="Defina los porcentajes de evaluación (Suma = 100%):", font=("Arial", 9, "bold")).pack(pady=(15, 5))
        
        # Frame para los porcentajes
        frame_pct = tk.Frame(self.window, padx=20)
        frame_pct.pack(fill="x")
        
        self.entries = {}
        criterios = [
            ("tareas", "Tareas"),
            ("trabajos", "Trabajos / Actividades"),
            ("proyecto", "Proyecto Final"),
            ("valores", "Valores / Asistencia"),
            ("examen", "Examen Escrito")
        ]
        
        # Valores por defecto para ayudar al usuario
        defaults = [10, 45, 5, 20, 20]
        
        for i, (key, label) in enumerate(criterios):
            row = tk.Frame(frame_pct)
            row.pack(fill="x", pady=2)
            
            tk.Label(row, text=f"{label}:", width=20, anchor="w").pack(side="left")
            ent = tk.Entry(row, width=5)
            ent.insert(0, str(defaults[i]))
            ent.pack(side="right")
            tk.Label(row, text="%").pack(side="right")
            
            self.entries[key] = ent
            
        # Botón Validar y Crear
        tk.Button(self.window, text="CREAR GRUPO", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
                  command=self.guardar_ciclo).pack(fill="x", padx=20, pady=20)
        
    def guardar_ciclo(self):
        nombre = self.ent_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Error", "Debes ponerle un nombre al grupo.")
            return

        # Validar porcentajes
        try:
            encuadre = {}
            total = 0
            for key, ent in self.entries.items():
                val = float(ent.get())
                if val < 0: raise ValueError
                encuadre[key] = val
                total += val
            
            # VALIDACIÓN CRÍTICA: MATEMÁTICAS
            if abs(total - 100.0) > 0.1: # Usamos tolerancia pequeña por decimales flotantes
                messagebox.showerror("Error Matemático", f"Los porcentajes suman {total}%. \nDeben sumar exactamente 100%.")
                return

            # Si llegamos aquí, todo está bien. Guardamos en BD.
            crear_ciclo(self.usuario_id, nombre, encuadre)
            
            messagebox.showinfo("Éxito", f"Grupo '{nombre}' creado correctamente.")
            self.callback() # Actualizamos la tabla de atrás
            self.window.destroy() # Cerramos esta ventana
            
        except ValueError:
            messagebox.showerror("Error", "Asegúrate de ingresar solo números en los porcentajes.")

# =========================================================
# CLASE VENTANA BOLETA (REPORTE)
# =========================================================
class VentanaBoleta:
    def __init__(self, parent, alumno_id, nombre, ciclo_id, encuadre):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Boleta: {nombre}")
        self.window.geometry("600x400")
        
        tk.Label(self.window, text=f"Boleta de Calificaciones", font=("Arial", 14, "bold"), fg="#9C27B0").pack(pady=10)
        tk.Label(self.window, text=f"Alumno: {nombre}", font=("Arial", 12)).pack()
        
        # Frame para la tabla
        frame_tabla = tk.Frame(self.window, padx=20, pady=20)
        frame_tabla.pack(fill="both", expand=True)
        
        # Usamos Treeview para mostrar la boleta
        cols = ("Materia", "Periodo 1", "Periodo 2", "Periodo 3", "Promedio Final")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show='headings', height=8)
        
        self.tree.heading("Materia", text="Campo Formativo")
        self.tree.heading("Periodo 1", text="P1")
        self.tree.heading("Periodo 2", text="P2")
        self.tree.heading("Periodo 3", text="P3")
        self.tree.heading("Promedio Final", text="Final")
        
        self.tree.column("Materia", width=150)
        self.tree.column("Periodo 1", width=50, anchor="center")
        self.tree.column("Periodo 2", width=50, anchor="center")
        self.tree.column("Periodo 3", width=50, anchor="center")
        self.tree.column("Promedio Final", width=60, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        
        # Botón Cerrar
        tk.Button(self.window, text="Cerrar", command=self.window.destroy).pack(pady=10)
        
        # Cargar datos
        self.cargar_datos(alumno_id, ciclo_id, encuadre)

    def cargar_datos(self, uid, cid, enc):
        datos = generar_reporte_boleta(uid, cid, enc)
        
        promedio_global_suma = 0
        count = 0
        
        for materia, periodos in datos.items():
            p1 = periodos['p1']
            p2 = periodos['p2']
            p3 = periodos['p3']
            final = periodos['final']
            
            self.tree.insert("", "end", values=(materia, p1, p2, p3, final))
            
            promedio_global_suma += final
            count += 1
            
        # Fila de Promedio General
        if count > 0:
            gral = round(promedio_global_suma / count, 2)
            self.tree.insert("", "end", values=("PROMEDIO GRAL", "-", "-", "-", gral), tags=('total',))
            self.tree.tag_configure('total', font=('Arial', 10, 'bold'), background='#E1BEE7')

# =========================================================
# CLASE VENTANA POPUP DE CALIFICACIÓN
# =========================================================
class VentanaCalificar:
    def __init__(self, parent, alumno_id, nombre_alumno, ciclo_id, encuadre):
        self.window = tk.Toplevel(parent)
        self.window.title(f"Calificando a: {nombre_alumno}")
        self.window.geometry("500x600")
        
        self.alumno_id = alumno_id
        self.ciclo_id = ciclo_id
        self.encuadre = encuadre # Diccionario con %
        
        # --- UI Elementos ---
        tk.Label(self.window, text=f"Alumno: {nombre_alumno}", font=FONT_SUBTITLE, fg=COLOR_PRIMARY).pack(pady=10)
        
        # Selectores
        frame_sel = tk.Frame(self.window)
        frame_sel.pack(pady=5)
        
        tk.Label(frame_sel, text="Materia:").grid(row=0, column=0, padx=5)
        self.combo_campo = ttk.Combobox(frame_sel, values=CAMPOS_FORMATIVOS, state="readonly")
        self.combo_campo.current(0)
        self.combo_campo.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_sel, text="Periodo:").grid(row=0, column=2, padx=5)
        self.combo_periodo = ttk.Combobox(frame_sel, values=["1", "2", "3"], width=5, state="readonly")
        self.combo_periodo.current(0)
        self.combo_periodo.grid(row=0, column=3, padx=5)
        
        tk.Button(frame_sel, text="Cargar Datos", command=self.cargar_datos_existentes).grid(row=0, column=4, padx=10)

        # Formulario
        self.frame_form = tk.Frame(self.window, padx=20, pady=10)
        self.frame_form.pack(fill="both", expand=True)
        
        self.entries = {}
        
        # Construimos inputs dinámicamente
        row = 0
        criterios = ["tareas", "proyecto", "valores", "examen"]
        
        for crit in criterios:
            pct = self.encuadre.get(crit, 0)
            tk.Label(self.frame_form, text=f"{crit.capitalize()} ({pct}%):", font=("Arial", 10, "bold")).grid(row=row, column=0, sticky="w", pady=5)
            ent = tk.Entry(self.frame_form)
            ent.insert(0, "0")
            ent.grid(row=row, column=1, padx=10)
            self.entries[crit] = ent
            row += 1
            
        # SECCIÓN ESPECIAL TRABAJOS
        tk.Frame(self.frame_form, height=2, bg="gray").grid(row=row, column=0, columnspan=2, sticky="ew", pady=10)
        row += 1
        
        pct_trab = self.encuadre.get("trabajos", 0)
        tk.Label(self.frame_form, text=f"TRABAJOS ({pct_trab}%):", font=("Arial", 10, "bold"), fg=COLOR_PRIMARY).grid(row=row, column=0, sticky="w")
        row += 1
        
        # Input Configuración Global
        tk.Label(self.frame_form, text="Total Trabajos (Materia/Periodo):").grid(row=row, column=0, sticky="e")
        self.ent_max_trabajos = tk.Entry(self.frame_form, bg="#FFF3E0") # Color diferente para notar que es config
        self.ent_max_trabajos.grid(row=row, column=1, padx=10)
        row += 1
        
        # Input Alumno
        tk.Label(self.frame_form, text="Entregados por Alumno:").grid(row=row, column=0, sticky="e")
        self.ent_entregados = tk.Entry(self.frame_form)
        self.ent_entregados.insert(0, "0")
        self.ent_entregados.grid(row=row, column=1, padx=10)
        row += 1
        
        # Botón Guardar
        tk.Button(self.window, text="GUARDAR CALIFICACIÓN", bg=COLOR_SUCCESS, fg="white", font=("Arial", 12, "bold"),
                command=self.guardar_datos).pack(fill="x", padx=20, pady=10)
        
        # Label Promedio
        self.lbl_resultado = tk.Label(self.window, text="Promedio: -", font=("Arial", 14, "bold"))
        self.lbl_resultado.pack(pady=10)

        # Cargar datos iniciales automáticamente
        self.cargar_datos_existentes()

    def cargar_datos_existentes(self):
        campo = self.combo_campo.get()
        periodo = int(self.combo_periodo.get())
        
        # 1. Cargar Configuración Global de Trabajos
        max_t = obtener_max_trabajos(self.ciclo_id, campo, periodo)
        self.ent_max_trabajos.delete(0, tk.END)
        self.ent_max_trabajos.insert(0, str(max_t))
        
        # 2. Cargar Notas del Alumno
        notas = obtener_calificaciones_alumno(self.alumno_id, campo, periodo)
        # notas = {'tareas': 10, 'trabajos': 5...}
        
        # Limpiar y llenar
        for crit, ent in self.entries.items():
            ent.delete(0, tk.END)
            val = notas.get(crit, 0.0)
            ent.insert(0, str(val))
            
        self.ent_entregados.delete(0, tk.END)
        val_trab = notas.get("trabajos", 0.0) # Aquí guardamos CANTIDAD entregada
        self.ent_entregados.insert(0, str(int(val_trab)))
        
        self.lbl_resultado.config(text="Datos cargados...")

    def guardar_datos(self):
        try:
            campo = self.combo_campo.get()
            periodo = int(self.combo_periodo.get())
            
            # 1. Guardar Configuración de Trabajos (Global)
            max_t = int(self.ent_max_trabajos.get())
            if max_t < 0: raise ValueError("Max trabajos no puede ser negativo")
            establecer_max_trabajos(self.ciclo_id, campo, periodo, max_t)
            
            # 2. Guardar Notas Individuales
            # Trabajos
            entregados = int(self.ent_entregados.get())
            registrar_calificacion(self.alumno_id, campo, periodo, "trabajos", entregados)
            
            # Otros criterios
            for crit, ent in self.entries.items():
                val = float(ent.get())
                if val < 0 or val > 100: raise ValueError(f"Valor incorrecto en {crit}")
                registrar_calificacion(self.alumno_id, campo, periodo, crit, val)
                
            # 3. Calcular y Mostrar Promedio
            promedio = calcular_promedio_periodo(self.alumno_id, self.ciclo_id, campo, periodo, self.encuadre)
            self.lbl_resultado.config(text=f"Promedio P{periodo}: {promedio} (Guardado)")
            
            messagebox.showinfo("Éxito", f"Calificación P{periodo}: {promedio}\nDatos guardados correctamente.")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Verifica los datos numéricos.\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEscolarApp(root)
    root.mainloop()