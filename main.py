# main.py ACTUALIZADO
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
# Importamos los módulos de lógica
from modules.auth import login_usuario, registrar_usuario
from modules.ciclos import obtener_ciclos_por_usuario, crear_ciclo
from modules.alumnos import agregar_alumno, obtener_alumnos # <--- NUEVO

# --- CONSTANTES DE DISEÑO ---
FONT_TITLE = ("Arial", 16, "bold")
FONT_SUBTITLE = ("Arial", 14, "bold")
FONT_LABEL = ("Arial", 11)
PAD_X = 10
PAD_Y = 5
COLOR_PRIMARY = "#2196F3"    # Azul
COLOR_SUCCESS = "#4CAF50"    # Verde
COLOR_DANGER = "#F44336"     # Rojo
COLOR_BG_DARK = "#333333"    # Gris oscuro

class SistemaEscolarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Escolar v3.1")
        self.root.geometry("400x350")
        self.usuario_id = None 
        
        # Variables de estado para la navegación
        self.ciclo_actual_id = None
        self.ciclo_actual_nombre = None
        
        self.mostrar_login()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==========================================
    # PANTALLA DE LOGIN
    # ==========================================
    def mostrar_login(self):
        self.limpiar_ventana()
        self.root.geometry("400x350")
        
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Iniciar Sesión", font=FONT_TITLE).pack(pady=10)

        tk.Label(frame, text="Usuario:", font=FONT_LABEL).pack(anchor="w")
        self.entry_user = tk.Entry(frame, font=FONT_LABEL)
        self.entry_user.pack(fill="x", pady=PAD_Y)

        tk.Label(frame, text="Contraseña:", font=FONT_LABEL).pack(anchor="w")
        self.entry_pass = tk.Entry(frame, font=FONT_LABEL, show="*")
        self.entry_pass.pack(fill="x", pady=PAD_Y)

        tk.Button(frame, text="Entrar", bg=COLOR_SUCCESS, fg="white", font=FONT_LABEL, 
                  command=self.accion_login).pack(fill="x", pady=20)
        
        tk.Button(frame, text="Registrarse", fg="blue", relief="flat",
                  command=self.mostrar_registro).pack()

    def mostrar_registro(self):
        self.limpiar_ventana()
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Registro Docente", font=FONT_TITLE).pack(pady=10)
        
        tk.Label(frame, text="Usuario:", font=FONT_LABEL).pack(anchor="w")
        self.entry_user_reg = tk.Entry(frame, font=FONT_LABEL)
        self.entry_user_reg.pack(fill="x", pady=PAD_Y)
        
        tk.Label(frame, text="Contraseña:", font=FONT_LABEL).pack(anchor="w")
        self.entry_pass_reg = tk.Entry(frame, font=FONT_LABEL, show="*")
        self.entry_pass_reg.pack(fill="x", pady=PAD_Y)

        tk.Button(frame, text="Registrar", bg=COLOR_PRIMARY, fg="white", font=FONT_LABEL, 
                  command=self.accion_registro).pack(fill="x", pady=20)
        tk.Button(frame, text="Cancelar", command=self.mostrar_login).pack()

    def accion_login(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()
        user_id = login_usuario(u, p)
        if user_id:
            self.usuario_id = user_id
            self.mostrar_dashboard()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def accion_registro(self):
        u = self.entry_user_reg.get()
        p = self.entry_pass_reg.get()
        exito, msg = registrar_usuario(u, p)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.mostrar_login()
        else:
            messagebox.showerror("Error", msg)

    # ==========================================
    # PANTALLA PRINCIPAL (DASHBOARD)
    # ==========================================
    def mostrar_dashboard(self):
        self.limpiar_ventana()
        self.root.title("Dashboard - Mis Grupos")
        self.root.geometry("800x600")
        
        # Barra Superior
        top_bar = tk.Frame(self.root, bg=COLOR_BG_DARK, height=50)
        top_bar.pack(fill="x", side="top")
        tk.Label(top_bar, text="Mis Ciclos Escolares", fg="white", bg=COLOR_BG_DARK, font=FONT_SUBTITLE).pack(side="left", padx=10, pady=10)
        tk.Button(top_bar, text="Cerrar Sesión", command=self.mostrar_login, bg=COLOR_DANGER, fg="white").pack(side="right", padx=10, pady=5)

        # Contenido
        content = tk.Frame(self.root, padx=20, pady=20)
        content.pack(fill="both", expand=True)
        
        tk.Button(content, text="+ Nuevo Grupo", bg=COLOR_PRIMARY, fg="white", font=FONT_LABEL, 
                  command=self.popup_crear_ciclo).pack(anchor="w", pady=10)
        
        tk.Label(content, text="Doble clic en un grupo para gestionarlo:", fg="gray").pack(anchor="w")

        # Tabla de Ciclos
        cols = ("ID", "Nombre", "Tareas", "Trabajos", "Examen")
        self.tree_ciclos = ttk.Treeview(content, columns=cols, show='headings')
        for col in cols:
            self.tree_ciclos.heading(col, text=col)
            self.tree_ciclos.column(col, width=100)
        self.tree_ciclos.column("ID", width=40)
        self.tree_ciclos.pack(fill="both", expand=True)
        
        # --- BINDING: EVENTO DOBLE CLIC ---
        self.tree_ciclos.bind("<Double-1>", self.abrir_ciclo_seleccionado)

        self.cargar_lista_ciclos()

    def cargar_lista_ciclos(self):
        for item in self.tree_ciclos.get_children():
            self.tree_ciclos.delete(item)
        ciclos = obtener_ciclos_por_usuario(self.usuario_id)
        for c in ciclos:
            # c = (id, nombre, tareas, trabajos, proyecto, valores, examen)
            self.tree_ciclos.insert("", "end", values=(c[0], c[1], f"{c[2]}%", f"{c[3]}%", f"{c[6]}%"))

    def popup_crear_ciclo(self):
        nombre = simpledialog.askstring("Nuevo", "Nombre del Grupo:")
        if nombre:
            # Por defecto usamos este encuadre, luego haremos que se pueda editar
            encuadre = {'tareas':10, 'trabajos':45, 'proyecto':5, 'valores':20, 'examen':20}
            crear_ciclo(self.usuario_id, nombre, encuadre)
            self.cargar_lista_ciclos()

    def abrir_ciclo_seleccionado(self, event):
        item = self.tree_ciclos.selection()
        if not item: return
        valores = self.tree_ciclos.item(item, "values")
        
        self.ciclo_actual_id = valores[0]
        self.ciclo_actual_nombre = valores[1]
        
        self.mostrar_detalle_ciclo()

    # ==========================================
    # VISTA DE DETALLE DE CICLO (ALUMNOS)
    # ==========================================
    def mostrar_detalle_ciclo(self):
        self.limpiar_ventana()
        self.root.title(f"Gestionando: {self.ciclo_actual_nombre}")
        
        # Barra Superior
        top_bar = tk.Frame(self.root, bg=COLOR_PRIMARY, height=50)
        top_bar.pack(fill="x", side="top")
        
        tk.Button(top_bar, text="< Volver", command=self.mostrar_dashboard, bg="#1976D2", fg="white", relief="flat").pack(side="left", padx=10, pady=10)
        tk.Label(top_bar, text=f"Grupo: {self.ciclo_actual_nombre}", fg="white", bg=COLOR_PRIMARY, font=FONT_SUBTITLE).pack(side="left", padx=10)

        # Contenido Principal
        content = tk.Frame(self.root, padx=20, pady=20)
        content.pack(fill="both", expand=True)

        # Botonera de Acciones
        frame_acciones = tk.Frame(content)
        frame_acciones.pack(fill="x", pady=10)
        
        tk.Button(frame_acciones, text="+ Agregar Alumno", bg=COLOR_SUCCESS, fg="white", 
                  command=self.popup_agregar_alumno).pack(side="left", padx=5)
        
        tk.Button(frame_acciones, text="Capturar Calificaciones", bg="#FF9800", fg="black",
                  command=self.placeholder_calificar).pack(side="left", padx=5)

        # Tabla de Alumnos
        tk.Label(content, text="Lista de Alumnos", font=FONT_SUBTITLE).pack(anchor="w", pady=(15, 5))
        
        cols_al = ("ID", "Nombre Completo")
        self.tree_alumnos = ttk.Treeview(content, columns=cols_al, show='headings')
        self.tree_alumnos.heading("ID", text="ID")
        self.tree_alumnos.heading("Nombre Completo", text="Nombre del Alumno")
        self.tree_alumnos.column("ID", width=50)
        self.tree_alumnos.column("Nombre Completo", width=400)
        
        self.tree_alumnos.pack(fill="both", expand=True)
        
        self.cargar_lista_alumnos()

    def cargar_lista_alumnos(self):
        for item in self.tree_alumnos.get_children():
            self.tree_alumnos.delete(item)
        
        # Llamamos a la BD
        alumnos = obtener_alumnos(self.ciclo_actual_id)
        for al in alumnos:
            # al = (id, nombre)
            self.tree_alumnos.insert("", "end", values=(al[0], al[1]))

    def popup_agregar_alumno(self):
        nombre = simpledialog.askstring("Nuevo Alumno", "Nombre completo:")
        if nombre:
            agregar_alumno(self.ciclo_actual_id, nombre)
            self.cargar_lista_alumnos() # Recargamos la lista al instante
            messagebox.showinfo("Listo", "Alumno agregado.")

    def placeholder_calificar(self):
        messagebox.showinfo("Próximamente", "¡Aquí conectaremos la ventana de captura de calificaciones!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEscolarApp(root)
    root.mainloop()