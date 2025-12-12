# modulos/ciclos.py
import sqlite3
import os
import sys
from config import DB_PATH
# Truco para importar config desde subcarpetas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def conectar_db():
    return sqlite3.connect(DB_PATH)


def crear_ciclo(usuario_id, nombre, encuadre):
    """
    Crea un nuevo grupo con un encuadre (porcentajes) específico.
    encuadre debe ser un dict: {'tareas': 10, 'trabajos': 45...}
    """
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO ciclos (usuario_id, nombre, pct_tareas, pct_trabajos, pct_proyecto, pct_valores, pct_examen)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (usuario_id, nombre, encuadre['tareas'], encuadre['trabajos'],
              encuadre['proyecto'], encuadre['valores'], encuadre['examen']))
        conn.commit()
        ciclo_id = cursor.lastrowid
        conn.close()
        return ciclo_id
    except Exception as e:
        conn.close()
        print(f"Error al crear ciclo: {e}")
        return None


def obtener_ciclos_por_usuario(usuario_id):
    conn = conectar_db()
    cursor = conn.cursor()
    # Traemos ID, Nombre y el Encuadre completo
    cursor.execute('''
        SELECT id, nombre, pct_tareas, pct_trabajos, pct_proyecto, pct_valores, pct_examen 
        FROM ciclos WHERE usuario_id = ?
    ''', (usuario_id,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# --- AQUÍ ESTÁ LA SOLUCIÓN A TU PROBLEMA DE TRABAJOS ---


def establecer_max_trabajos(ciclo_id, campo, periodo, cantidad):
    """
    Guarda cuántos trabajos valen el 100% para UNA materia y UN periodo específico.
    Ej: Matemáticas, P1 = 20 trabajos.
    """
    conn = conectar_db()
    cursor = conn.cursor()
    try:
        # Usamos INSERT OR REPLACE para que si ya existe, lo actualice
        cursor.execute('''
            INSERT INTO config_trabajos (ciclo_id, campo_formativo, periodo, max_trabajos)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(ciclo_id, campo_formativo, periodo) 
            DO UPDATE SET max_trabajos=excluded.max_trabajos
        ''', (ciclo_id, campo, periodo, cantidad))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error config trabajos: {e}")
        return False
    finally:
        conn.close()


def obtener_max_trabajos(ciclo_id, campo, periodo):
    """Devuelve el número de trabajos configurados. Si no existe, devuelve 0."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT max_trabajos FROM config_trabajos 
        WHERE ciclo_id=? AND campo_formativo=? AND periodo=?
    ''', (ciclo_id, campo, periodo))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0
