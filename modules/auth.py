# modulos/auth.py
import sqlite3
import hashlib
import os

# --- Configuración de Rutas ---
# Esto asegura que siempre encuentre la DB, sin importar desde dónde ejecutes el script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "sistema_escolar.db")

def conectar_db():
    return sqlite3.connect(DB_PATH)

def hashear_password(password):
    """
    Convierte la contraseña en una cadena de caracteres ilegible (hash SHA-256).
    Esto es seguridad básica: nunca guardar contraseñas reales.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def registrar_usuario(username, password):
    """
    Intenta registrar un nuevo usuario.
    Retorna (True, "Mensaje") si tuvo éxito, o (False, "Error") si falló.
    """
    if not username or not password:
        return False, "Usuario y contraseña no pueden estar vacíos."
    
    conn = conectar_db()
    cursor = conn.cursor()
    
    password_encriptada = hashear_password(password)
    
    try:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", 
                    (username, password_encriptada))
        conn.commit()
        conn.close()
        return True, f"Usuario '{username}' registrado exitosamente."
    except sqlite3.IntegrityError:
        conn.close()
        return False, f"El usuario '{username}' ya existe."
    except Exception as e:
        conn.close()
        return False, f"Error desconocido: {e}"

def login_usuario(username, password):
    """
    Verifica las credenciales.
    Retorna el ID del usuario si es correcto, o None si falla.
    """
    conn = conectar_db()
    cursor = conn.cursor()
    
    password_encriptada = hashear_password(password)
    
    # Buscamos si existe esa combinación exacta de usuario y hash
    cursor.execute("SELECT id FROM usuarios WHERE username=? AND password=?", 
                (username, password_encriptada))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return resultado[0] # Retornamos el ID (útil para saber de quién son los grupos)
    else:
        return None