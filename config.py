# config.py
import sys
import os

def obtener_ruta_base():
    """
    Detecta si estamos corriendo como script (.py) o como ejecutable congelado (.exe/.app).
    """
    if getattr(sys, 'frozen', False):
        # Si es ejecutable, la ruta es donde está el archivo .exe
        return os.path.dirname(sys.executable)
    else:
        # Si es script, la ruta es donde está este archivo
        return os.path.dirname(os.path.abspath(__file__))

# Esta variable la importaremos en los otros archivos
BASE_DIR = obtener_ruta_base()
DB_PATH = os.path.join(BASE_DIR, "sistema_escolar.db")