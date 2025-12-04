# database.py
import sqlite3
import os

DB_NAME = "sistema_escolar.db"

def conectar_db():
    """Crea y devuelve una conexión a la base de datos."""
    return sqlite3.connect(DB_NAME)

def inicializar_db():
    """Crea las tablas necesarias si no existen."""
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
    # Guardamos el encuadre (porcentajes) aquí mismo
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
    # Guardamos todo desglosado. 
    # periodo: 1, 2, 3
    # campo: "Lenguajes", "Saberes", etc.
    # criterio: "tareas", "examen", etc.
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
            presente INTEGER, -- 1 = Si, 0 = No
            FOREIGN KEY(alumno_id) REFERENCES alumnos(id) ON DELETE CASCADE
        )
    ''')
    
    # Tabla especial para configurar el MAXIMO de trabajos por periodo y ciclo
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config_trabajos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ciclo_id INTEGER,
            periodo INTEGER,
            max_trabajos INTEGER DEFAULT 0,
            FOREIGN KEY(ciclo_id) REFERENCES ciclos(id) ON DELETE CASCADE
        )
    ''')

    conexion.commit()
    conexion.close()
    print("Base de datos inicializada correctamente: sistema_escolar.db")

# Si ejecutamos este archivo directamente, inicializa la DB
if __name__ == "__main__":
    inicializar_db()