# main.py
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from modules.auth import login_usuario, registrar_usuario
from modules.ciclos import obtener_ciclos_por_usuario, crear_ciclo

# --- CONSTANTES DE DISEÑO BÁSICO ---
FONT_TITLE = ("Arial", 16, "bold")
FONT_LABEL = ("Arial", 11)
PAD_X = 10
PAD_Y = 5

class SistemaEscolarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Escolar v3.1 - Login")
        self.root.geometry("400x350")
        self.usuario_id = None # Aquí guardaremos quién inició sesión
        
        # Iniciamos mostrando el frame de Login
        self.mostrar_login()

    def limpiar_ventana(self):
        """Borra todo lo que hay en la ventana para cambiar de pantalla"""
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

        tk.Button(frame, text="Entrar", bg="#4CAF50", fg="white", font=FONT_LABEL, 
                  command=self.accion_login).pack(fill="x", pady=20)
        
        tk.Button(frame, text="¿No tienes cuenta? Regístrate", fg="blue", relief="flat",
                  command=self.mostrar_registro).pack()

    def mostrar_registro(self):
        self.limpiar_ventana()
        
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Registro de Docente", font=FONT_TITLE).pack(pady=10)

        tk.Label(frame, text="Nuevo Usuario:", font=FONT_LABEL).pack(anchor="w")
        self.entry_user_reg = tk.Entry(frame, font=FONT_LABEL)
        self.entry_user_reg.pack(fill="x", pady=PAD_Y)

        tk.Label(frame, text="Contraseña:", font=FONT_LABEL).pack(anchor="w")
        self.entry_pass_reg = tk.Entry(frame, font=FONT_LABEL, show="*")
        self.entry_pass_reg.pack(fill="x", pady=PAD_Y)

        tk.Button(frame, text="Registrar y Volver", bg="#2196F3", fg="white", font=FONT_LABEL, 
                  command=self.accion_registro).pack(fill="x", pady=20)
        
        tk.Button(frame, text="Cancelar", command=self.mostrar_login).pack()

    # ==========================================
    # LÓGICA DE BOTONES (AUTH)
    # ==========================================
    def accion_login(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()
        
        user_id = login_usuario(u, p)
        if user_id:
            self.usuario_id = user_id
            messagebox.showinfo("Éxito", f"Bienvenido, {u}!")
            self.mostrar_dashboard() # <--- TRANSICIÓN AL DASHBOARD
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

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
        self.root.title("Sistema Escolar - Dashboard")
        self.root.geometry("800x600") # Hacemos la ventana más grande
        
        # -- Barra Superior --
        top_bar = tk.Frame(self.root, bg="#333", height=50)
        top_bar.pack(fill="x", side="top")
        tk.Label(top_bar, text="Mis Ciclos Escolares", fg="white", bg="#333", font=("Arial", 14)).pack(side="left", padx=10, pady=10)
        tk.Button(top_bar, text="Cerrar Sesión", command=self.mostrar_login, bg="#f44336", fg="white").pack(side="right", padx=10, pady=10)

        # -- Área de Contenido --
        self.content_frame = tk.Frame(self.root, padx=20, pady=20)
        self.content_frame.pack(fill="both", expand=True)
        
        # Botón para crear nuevo ciclo
        tk.Button(self.content_frame, text="+ Nuevo Ciclo Escolar", font=FONT_LABEL, 
                  command=self.popup_crear_ciclo).pack(anchor="w", pady=10)
        
        # Lista de Ciclos (Treeview)
        cols = ("ID", "Nombre Ciclo", "Tareas", "Trabajos", "Examen")
        self.tree_ciclos = ttk.Treeview(self.content_frame, columns=cols, show='headings')
        
        # Configurar columnas
        for col in cols:
            self.tree_ciclos.heading(col, text=col)
            self.tree_ciclos.column(col, width=100)
        self.tree_ciclos.column("ID", width=30) # ID más pequeño
        
        self.tree_ciclos.pack(fill="both", expand=True)

        # Cargar datos de la BD
        self.cargar_lista_ciclos()

    def cargar_lista_ciclos(self):
        # Limpiar tabla actual
        for item in self.tree_ciclos.get_children():
            self.tree_ciclos.delete(item)
            
        # Obtener datos reales de SQLite
        ciclos = obtener_ciclos_por_usuario(self.usuario_id)
        for c in ciclos:
            # c es una tupla: (id, nombre, tareas, trabajos, proyecto, valores, examen)
            # Insertamos solo lo relevante para la vista previa
            self.tree_ciclos.insert("", "end", values=(c[0], c[1], f"{c[2]}%", f"{c[3]}%", f"{c[6]}%"))

    def popup_crear_ciclo(self):
        # Diálogo simple para pedir nombre (Simplificado por ahora)
        nombre = simpledialog.askstring("Nuevo Ciclo", "Nombre del Grupo:")
        if nombre:
            # Creamos con el encuadre por defecto (después haremos una ventana para personalizar esto)
            encuadre_default = {'tareas':10, 'trabajos':45, 'proyecto':5, 'valores':20, 'examen':20}
            crear_ciclo(self.usuario_id, nombre, encuadre_default)
            self.cargar_lista_ciclos() # Refrescar la tabla

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEscolarApp(root)
    root.mainloop()