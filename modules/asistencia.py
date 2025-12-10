# modulos/asistencia.py
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "sistema_escolar.db")

def conectar_db():
    return sqlite3.connect(DB_PATH)

def obtener_asistencia_fecha(ciclo_id, fecha):
    """
    Devuelve un diccionario {alumno_id: estado} para una fecha específica.
    Estado: 1 (Presente), 0 (Ausente).
    """
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Hacemos un JOIN para asegurarnos de traer solo alumnos de ese ciclo
    cursor.execute('''
        SELECT a.alumno_id, a.presente 
        FROM asistencia a
        JOIN alumnos al ON a.alumno_id = al.id
        WHERE al.ciclo_id = ? AND a.fecha = ?
    ''', (ciclo_id, fecha))
    
    datos = dict(cursor.fetchall())
    conn.close()
    return datos

def guardar_asistencia_bloque(fecha, lista_datos):
    """
    Guarda la asistencia de múltiples alumnos.
    lista_datos es una lista de tuplas: [(alumno_id, estado), (alumno_id, estado)...]
    """
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
        # Usamos una transacción para que sea rápido y seguro
        for alumno_id, estado in lista_datos:
            # 1. Borramos registro previo de ese día para evitar duplicados
            cursor.execute('''
                DELETE FROM asistencia 
                WHERE alumno_id = ? AND fecha = ?
            ''', (alumno_id, fecha))
            
            # 2. Insertamos el nuevo estado
            cursor.execute('''
                INSERT INTO asistencia (alumno_id, fecha, presente)
                VALUES (?, ?, ?)
            ''', (alumno_id, fecha, estado))
            
        conn.commit()
        return True
    except Exception as e:
        print(f"Error guardando asistencia: {e}")
        return False
    finally:
        conn.close()