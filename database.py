# database.py ACTUALIZADO (v3.1)
import sqlite3
import os
from config import DB_PATH  # <--- IMPORTANTE: Usamos la ruta inteligente


def conectar_db():
    return sqlite3.connect(DB_PATH)  # <--- Usamos esa variable


def inicializar_db():
    conexion = conectar_db()
    cursor = conexion.cursor()

    # 1. Tabla de USUARIOS (Profesores)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # 2. Tabla de CICLOS ESCOLARES (Grupos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ciclos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            usuario_id INTEGER,
            pct_tareas REAL DEFAULT 10.0,
            pct_trabajos REAL DEFAULT 45.0,
            pct_proyecto REAL DEFAULT 5.0,
            pct_valores REAL DEFAULT 20.0,
            pct_examen REAL DEFAULT 20.0,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')

    # 3. Tabla de ALUMNOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ciclo_id INTEGER,
            FOREIGN KEY(ciclo_id) REFERENCES ciclos(id) ON DELETE CASCADE
        )
    ''')

    # 4. Tabla de CALIFICACIONES
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calificaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumno_id INTEGER,
            campo_formativo TEXT,
            periodo INTEGER,
            criterio TEXT,
            valor REAL,
            FOREIGN KEY(alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE
        )
    ''')

    # 5. Tabla de ASISTENCIA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asistencia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumno_id INTEGER,
            fecha TEXT,
            presente INTEGER,
            FOREIGN KEY(alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE
        )
    ''')

    # --- CAMBIO IMPORTANTE AQUÍ ---
    # 6. Tabla de CONFIGURACIÓN DE TRABAJOS
    # Ahora guardamos el máximo POR CAMPO FORMATIVO
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config_trabajos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ciclo_id INTEGER,
            campo_formativo TEXT,  -- <--- Agregamos esto
            periodo INTEGER,
            max_trabajos INTEGER DEFAULT 0,
            FOREIGN KEY(ciclo_id) REFERENCES ciclos(id) ON DELETE CASCADE,
            UNIQUE(ciclo_id, campo_formativo, periodo) -- Evita duplicados
        )
    ''')

    conexion.commit()
    conexion.close()
    print("Base de datos (v3.1) inicializada correctamente.")


if __name__ == "__main__":
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Base de datos anterior eliminada para actualización.")

    inicializar_db()
