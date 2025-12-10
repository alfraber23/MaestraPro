# main.py (Versión 3.2 - Con Módulo de Calificación)
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
# Importamos lógica
from modules.auth import login_usuario, registrar_usuario
from modules.ciclos import obtener_ciclos_por_usuario, crear_ciclo, obtener_max_trabajos, establecer_max_trabajos
from modules.alumnos import agregar_alumno, obtener_alumnos, registrar_calificacion, calcular_promedio_periodo, obtener_calificaciones_alumno

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
        nom = simpledialog.askstring("Nuevo", "Nombre del Grupo:")
        if nom:
            # Encuadre default
            enc = {'tareas':10, 'trabajos':45, 'proyecto':5, 'valores':20, 'examen':20}
            crear_ciclo(self.usuario_id, nom, enc)
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
        
        # --- BOTÓN NARANJA CONECTADO ---
        tk.Button(acciones, text="Capturar Calificaciones", bg="#FF9800", fg="black", command=self.abrir_ventana_calificar).pack(side="left", padx=5)

        tk.Label(body, text="Selecciona un alumno para calificar:", font=("Arial", 9, "italic")).pack(anchor="w")

        cols = ("ID", "Nombre")
        self.tree_alumnos = ttk.Treeview(body, columns=cols, show='headings')
        self.tree_alumnos.heading("ID", text="ID"); self.tree_alumnos.column("ID", width=50)
        self.tree_alumnos.heading("Nombre", text="Nombre Alumno"); self.tree_alumnos.column("Nombre", width=400)
        self.tree_alumnos.pack(fill="both", expand=True)
        
        self.cargar_alumnos()

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