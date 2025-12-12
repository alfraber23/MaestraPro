# config.py
import sys
import os


def obtener_ruta_base():
    """ Define si estamos en modo EXE o en modo CÓDIGO """
    if getattr(sys, 'frozen', False):
        # Si es .exe, usa la carpeta donde está el ejecutable
        return os.path.dirname(sys.executable)
    else:
        # Si es código normal, usa la carpeta actual
        return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = obtener_ruta_base()
DB_PATH = os.path.join(BASE_DIR, "sistema_escolar.db")
