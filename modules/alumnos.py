# modulos/alumnos.py
import sqlite3
import os
from .ciclos import obtener_max_trabajos # Importamos para hacer cálculos

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "sistema_escolar.db")

def conectar_db():
    return sqlite3.connect(DB_PATH)

def agregar_alumno(ciclo_id, nombre):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alumnos (ciclo_id, nombre) VALUES (?, ?)", (ciclo_id, nombre))
    conn.commit()
    conn.close()
    return True

def obtener_alumnos(ciclo_id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM alumnos WHERE ciclo_id = ?", (ciclo_id,))
    alumnos = cursor.fetchall()
    conn.close()
    return alumnos

def registrar_calificacion(alumno_id, campo, periodo, criterio, valor):
    """
    Guarda una calificación.
    OJO: Si el criterio es 'trabajos', 'valor' debe ser la cantidad ENTREGADA, no el porcentaje.
    """
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Borramos si existía una anterior para ese mismo rubro (para evitar duplicados y ensuciar la DB)
    cursor.execute('''
        DELETE FROM calificaciones 
        WHERE alumno_id=? AND campo_formativo=? AND periodo=? AND criterio=?
    ''', (alumno_id, campo, periodo, criterio))
    
    cursor.execute('''
        INSERT INTO calificaciones (alumno_id, campo_formativo, periodo, criterio, valor)
        VALUES (?, ?, ?, ?, ?)
    ''', (alumno_id, campo, periodo, criterio, valor))
    
    conn.commit()
    conn.close()

def calcular_promedio_periodo(alumno_id, ciclo_id, campo, periodo, encuadre_dict):
    """
    Calcula la calificación final del periodo usando SQL y Python.
    encuadre_dict: {'pct_tareas': 10, ...} que viene de la tabla ciclos.
    """
    conn = conectar_db()
    cursor = conn.cursor()
    
    # 1. Obtenemos todas las notas de ese alumno/campo/periodo
    cursor.execute('''
        SELECT criterio, valor FROM calificaciones
        WHERE alumno_id=? AND campo_formativo=? AND periodo=?
    ''', (alumno_id, campo, periodo))
    datos = dict(cursor.fetchall()) # Convertimos a diccionario: {'tareas': 10, 'trabajos': 15...}
    conn.close()
    
    if not datos:
        return 0.0

    suma_final = 0.0
    
    # --- CÁLCULO DE TAREAS, PROYECTO, VALORES, EXAMEN ---
    suma_final += datos.get('tareas', 0) * (encuadre_dict['tareas'] / 100)
    suma_final += datos.get('proyecto', 0) * (encuadre_dict['proyecto'] / 100)
    suma_final += datos.get('valores', 0) * (encuadre_dict['valores'] / 100)
    suma_final += datos.get('examen', 0) * (encuadre_dict['examen'] / 100)
    
    # --- CÁLCULO ESPECIAL DE TRABAJOS ---
    entregados = datos.get('trabajos', 0)
    maximos = obtener_max_trabajos(ciclo_id, campo, periodo)
    
    if maximos > 0:
        porcentaje_obtenido = (entregados / maximos) * 100
        if porcentaje_obtenido > 100: porcentaje_obtenido = 100 # Tope de 100%
    else:
        porcentaje_obtenido = 100.0 if entregados > 0 else 0.0 # Si no se configuró máximo pero entregó algo, damos el punto.
        
    suma_final += porcentaje_obtenido * (encuadre_dict['trabajos'] / 100)
    
    return round(suma_final, 2)

# --- AGREGAR ESTO AL FINAL DE modulos/alumnos.py ---

def obtener_calificaciones_alumno(alumno_id, campo, periodo):
    """
    Devuelve un diccionario con las notas guardadas.
    Ej: {'tareas': 10.0, 'examen': 8.5, ...}
    """
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT criterio, valor FROM calificaciones
        WHERE alumno_id=? AND campo_formativo=? AND periodo=?
    ''', (alumno_id, campo, periodo))
    datos = dict(cursor.fetchall())
    conn.close()
    return datos