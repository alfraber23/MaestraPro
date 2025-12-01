# final.py
import sys
import time
import os
import json
from datetime import datetime

# --- Configuración Global y Constantes ---
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# --- SOLUCIÓN AL ERROR DE PERMISOS (Rutas Absolutas) ---
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_USUARIOS = os.path.join(DIRECTORIO_BASE, "usuarios_registrados.txt")
DIR_DATOS = os.path.join(DIRECTORIO_BASE, "datos_clases")
# -------------------------------------------------------

# Valores por defecto del encuadre (si carga archivos viejos y no tiene encuadre)
ENCUADRE_POR_DEFECTO = {
    "tareas": 10.0,
    "trabajos": 45.0,
    "proyecto": 5.0,
    "valores": 20.0,
    "examen": 20.0
}

# Campos formativos por defecto (los conservamos tal como pediste)
CAMPOS_FORMATIVOS_POR_DEFECTO = [
    "Lenguajes",
    "Saberes y Pensamiento",
    "Etica Naturaleza",
    "De lo Humano"
]

# --- Funciones de Utilidad ---
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def animacion_carga(mensaje="Cargando sistema"):
    print(f"\n{Color.YELLOW}{mensaje}", end="")
    for _ in range(5):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.2)
    print(f"{Color.END}\n")

def mostrar_bienvenida(nickname):
    limpiar_pantalla()
    borde = "*" * 60
    mensaje = f"¡Hola, {nickname.upper()}! Bienvenido al Sistema v3.0"
    print(f"{Color.CYAN}{borde}")
    print(f"{mensaje.center(60)}")
    print(f"{borde}{Color.END}")
    print("\nPreparando entorno de trabajo...")
    time.sleep(1.2)

def asegurar_directorios():
    if not os.path.exists(DIR_DATOS):
        try:
            os.makedirs(DIR_DATOS, exist_ok=True)
        except PermissionError:
            print(f"{Color.RED}ERROR CRÍTICO: No hay permisos para crear carpetas aquí.{Color.END}")
            input("Enter para salir...")
            sys.exit()

    # crear demos solo si no existen
    demos = ["Ciclo_2024_2025_GrupoA", "Ciclo_2023_2024_GrupoB"]
    for nombre in demos:
        ruta = os.path.join(DIR_DATOS, f"{nombre}.txt")
        if not os.path.exists(ruta):
            # Estructura nueva mínima: meta_fecha_modificacion, meta_encuadre, meta_trabajos, alumnos
            alumno_demo = {
                "id": 1,
                "nombre": "Alumno Demo",
                "calificaciones": {}
            }
            # Inicializar campos formativos en estructura nueva
            for campo in CAMPOS_FORMATIVOS_POR_DEFECTO:
                alumno_demo["calificaciones"][campo] = {
                    "p1": {"tareas": 0.0, "trabajos": {"entregados": 0, "porcentaje": 0.0}, "proyecto": 0.0, "valores": 0.0, "examen": 0.0, "final": 0.0},
                    "p2": {"tareas": 0.0, "trabajos": {"entregados": 0, "porcentaje": 0.0}, "proyecto": 0.0, "valores": 0.0, "examen": 0.0, "final": 0.0},
                    "p3": {"tareas": 0.0, "trabajos": {"entregados": 0, "porcentaje": 0.0}, "proyecto": 0.0, "valores": 0.0, "examen": 0.0, "final": 0.0}
                }
            data_dummy = {
                "meta_fecha_modificacion": formatear_fecha_tupla((1,1,2024)),
                "meta_encuadre": ENCUADRE_POR_DEFECTO,
                "meta_trabajos": {"p1_max": 40, "p2_max": 26, "p3_max": 0},
                "alumnos": [alumno_demo]
            }
            try:
                with open(ruta, 'w', encoding='utf-8') as f:
                    json.dump(data_dummy, f, indent=4)
            except IOError:
                pass

# --- Gestión de Fechas ---
def pedir_fecha_tupla():
    while True:
        fecha_str = input(f"{Color.BOLD}Ingrese la fecha de operación (DD/MM/AAAA): {Color.END}")
        try:
            fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y")
            hoy = datetime.now()
            if fecha_obj.date() > hoy.date():
                print(f"{Color.RED}Error: No puedes registrar datos en el futuro.{Color.END}")
                continue
            return (fecha_obj.day, fecha_obj.month, fecha_obj.year)
        except ValueError:
            print(f"{Color.RED}Error: Formato incorrecto, usa DD/MM/AAAA.{Color.END}")

def formatear_fecha_tupla(tupla_fecha):
    return f"{tupla_fecha[0]:02d}/{tupla_fecha[1]:02d}/{tupla_fecha[2]}"

# --- Sistema de Login ---
def cargar_usuarios():
    usuarios = {}
    if os.path.exists(ARCHIVO_USUARIOS):
        try:
            with open(ARCHIVO_USUARIOS, 'r') as f:
                for linea in f:
                    partes = linea.strip().split(',')
                    if len(partes) == 2:
                        usuarios[partes[0]] = partes[1]
        except Exception:
            pass
    return usuarios

def guardar_usuario_archivo(usuario, password):
    with open(ARCHIVO_USUARIOS, 'a') as f:
        f.write(f"{usuario},{password}\n")

def sistema_login():
    usuarios = cargar_usuarios()
    while True:
        limpiar_pantalla()
        print(f"{Color.PURPLE}========================================{Color.END}")
        print(f"{Color.PURPLE}      SISTEMA DE GESTIÓN ESCOLAR        {Color.END}")
        print(f"{Color.PURPLE}========================================{Color.END}")
        print("1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir del Programa")
        print("-" * 40)

        opcion = input("Opción: ")

        if opcion == "1":
            u = input("Usuario: ")
            p = input("Contraseña: ")
            if u in usuarios and usuarios[u] == p:
                animacion_carga("Validando credenciales")
                return u
            else:
                print(f"{Color.RED}Usuario o contraseña incorrectos.{Color.END}")
                time.sleep(1.2)
        elif opcion == "2":
            u = input("Nuevo Usuario: ")
            if u in usuarios:
                print(f"{Color.RED}El usuario ya existe.{Color.END}")
                time.sleep(1.2)
                continue
            p = input("Nueva Contraseña: ")
            guardar_usuario_archivo(u, p)
            usuarios[u] = p
            print(f"{Color.GREEN}Registro exitoso. Por favor inicie sesión.{Color.END}")
            time.sleep(1.2)
        elif opcion == "3":
            print("Hasta luego.")
            input("Presione Enter para cerrar...")
            sys.exit()

# --- Manejo de Archivos de Ciclo Escolar ---
def guardar_clase(nombre_archivo, lista_alumnos, fecha_modificacion, meta_encuadre=None, meta_trabajos=None):
    ruta = os.path.join(DIR_DATOS, f"{nombre_archivo}.txt")
    data = {
        "meta_fecha_modificacion": formatear_fecha_tupla(fecha_modificacion),
        "meta_encuadre": meta_encuadre if meta_encuadre is not None else ENCUADRE_POR_DEFECTO,
        "meta_trabajos": meta_trabajos if meta_trabajos is not None else {"p1_max": 0, "p2_max": 0, "p3_max": 0},
        "alumnos": lista_alumnos
    }
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"{Color.GREEN}Ciclo Escolar '{nombre_archivo}' guardado exitosamente.{Color.END}")
        time.sleep(1.0)
        return True
    except IOError as e:
        print(f"{Color.RED}Error al guardar: {e}{Color.END}")
        return False

def leer_archivo_clase(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = json.load(f)
            # Si es lista (antiguo formato), los convertimos a la nueva estructura mínima
            if isinstance(contenido, list):
                return {
                    "meta_fecha_modificacion": formatear_fecha_tupla((1,1,2024)),
                    "meta_encuadre": ENCUADRE_POR_DEFECTO,
                    "meta_trabajos": {"p1_max": 0, "p2_max": 0, "p3_max": 0},
                    "alumnos": contenido
                }
            elif isinstance(contenido, dict):
                # Aseguramos claves necesarias
                if "meta_encuadre" not in contenido:
                    contenido["meta_encuadre"] = ENCUADRE_POR_DEFECTO
                if "meta_trabajos" not in contenido:
                    contenido["meta_trabajos"] = {"p1_max": 0, "p2_max": 0, "p3_max": 0}
                if "alumnos" not in contenido:
                    contenido["alumnos"] = []
                return contenido
    except Exception:
        return {
            "meta_fecha_modificacion": formatear_fecha_tupla((1,1,2024)),
            "meta_encuadre": ENCUADRE_POR_DEFECTO,
            "meta_trabajos": {"p1_max": 0, "p2_max": 0, "p3_max": 0},
            "alumnos": []
        }

#Lectura de archivos
def cargar_clase():
    if not os.path.exists(DIR_DATOS):
        print(f"{Color.RED}Error: La carpeta de datos no existe.{Color.END}")
        return None, None, None, None, []

    archivos = [f for f in os.listdir(DIR_DATOS) if f.endswith('.txt')]
    if not archivos:
        print(f"{Color.RED}No hay ciclos escolares guardados.{Color.END}")
        return None, None, None, None, []

    print(f"\n{Color.CYAN}Ciclos Escolares Disponibles:{Color.END}")
    dict_archivos = {str(i+1): archivo for i, archivo in enumerate(archivos)}
    for k, v in dict_archivos.items():
        print(f" {k}. {v}")

    seleccion = input("Seleccione número de archivo: ")
    nombre_archivo = dict_archivos.get(seleccion)

    if not nombre_archivo:
        print(f"{Color.RED}Opción inválida.{Color.END}")
        return None, None, None, None, []

    ruta = os.path.join(DIR_DATOS, nombre_archivo)
    contenido = leer_archivo_clase(ruta)
    animacion_carga("Leyendo Ciclo Escolar")
    nombre_sin_ext = nombre_archivo.replace(".txt", "")
    return nombre_sin_ext, contenido.get("meta_encuadre"), contenido.get("meta_trabajos"), contenido.get("meta_fecha_modificacion"), contenido.get("alumnos")

# --- Utilidades para estructura de calificaciones ---
def crear_estructura_calificaciones_vacia():
    estructura = {}
    for campo in CAMPOS_FORMATIVOS_POR_DEFECTO:
        estructura[campo] = {
            "p1": {"tareas": 0.0, "trabajos": {"entregados": 0, "porcentaje": 0.0}, "proyecto": 0.0, "valores": 0.0, "examen": 0.0, "final": 0.0},
            "p2": {"tareas": 0.0, "trabajos": {"entregados": 0, "porcentaje": 0.0}, "proyecto": 0.0, "valores": 0.0, "examen": 0.0, "final": 0.0},
            "p3": {"tareas": 0.0, "trabajos": {"entregados": 0, "porcentaje": 0.0}, "proyecto": 0.0, "valores": 0.0, "examen": 0.0, "final": 0.0}
        }
    return estructura

def migrar_alumno_si_necesario(alumno):
    # Si el alumno tiene la estructura antigua (calificaciones como listas), la migramos
    if isinstance(alumno.get("calificaciones"), dict):
        # Detectar si ya está en nuevo formato (valores anidados por periodo)
        ejemplo_campos = alumno["calificaciones"]
        # Si sus valores son listas -> migrar
        need_migrate = False
        for v in ejemplo_campos.values():
            if isinstance(v, list):
                need_migrate = True
                break
        if need_migrate:
            nueva = crear_estructura_calificaciones_vacia()
            for campo, listas in alumno["calificaciones"].items():
                if campo not in nueva:
                    # Agregar campo nuevo si aparece
                    nueva[campo] = {
                        "p1": {"tareas": 0.0, "trabajos": {"entregados": 0, "porcentaje": 0.0}, "proyecto": 0.0, "valores": 0.0, "examen": 0.0, "final": 0.0},
                        "p2": {"tareas": 0.0, "trabajos": {"entregados": 0, "porcentaje": 0.0}, "proyecto": 0.0, "valores": 0.0, "examen": 0.0, "final": 0.0},
                        "p3": {"tareas": 0.0, "trabajos": {"entregados": 0, "porcentaje": 0.0}, "proyecto": 0.0, "valores": 0.0, "examen": 0.0, "final": 0.0}
                    }
                vals = listas
                # Llenar p1,p2,p3 con la lista (si la lista está cortada se llenan con 0)
                for i, periodo in enumerate(["p1","p2","p3"]):
                    try:
                        nueva[campo][periodo]["tareas"] = float(vals[i])
                        # los otros criterios quedan en 0
                    except Exception:
                        pass
            alumno["calificaciones"] = nueva
    else:
        # Si no existe o es lista vacía, crear estructura vacía
        alumno["calificaciones"] = crear_estructura_calificaciones_vacia()

# --- Gestión de Alumnos ---
def registrar_alumno(lista_alumnos):
    nombre = input("Nombre completo: ").strip()
    if not nombre:
        return False

    existe = any(alumno['nombre'].strip().lower() == nombre.strip().lower() for alumno in lista_alumnos)
    if existe:
        print(f"{Color.YELLOW}¡ALERTA! Ya existe un alumno registrado con el nombre '{nombre}' en la sesión actual.{Color.END}")
        confirmacion = input("¿Es un homónimo (persona diferente con mismo nombre)? (s/n): ").lower()
        if confirmacion != 's':
            print(f"{Color.RED}Registro cancelado.{Color.END}")
            time.sleep(1.0)
            return False

    if lista_alumnos:
        nuevo_id = max(alumno['id'] for alumno in lista_alumnos) + 1
    else:
        nuevo_id = 1

    nuevo_alumno = {
        "id": nuevo_id,
        "nombre": nombre,
        "calificaciones": crear_estructura_calificaciones_vacia(),
        "historial_asistencia": {}
    }
    lista_alumnos.append(nuevo_alumno)
    print(f"{Color.GREEN}Alumno agregado exitosamente (ID: {nuevo_id}).{Color.END}")
    time.sleep(0.8)
    return True

def modificar_alumno(lista_alumnos, alumno_directo=None):
    if not lista_alumnos:
        return False

    if alumno_directo is None:
        print(f"\n{Color.CYAN}--- Modificar Datos de Alumno ---{Color.END}")
        try:
            id_str = input("Ingrese el ID del alumno a modificar: ")
            id_buscado = int(id_str)
            alumno = next((a for a in lista_alumnos if a["id"] == id_buscado), None)
        except ValueError:
            print("ID inválido.")
            return False
    else:
        alumno = alumno_directo

    if not alumno:
        print(f"{Color.RED}Alumno no encontrado.{Color.END}")
        return False

    print(f"\nEditando a: {Color.BOLD}{alumno['nombre']}{Color.END}")
    print("Deje en blanco si no desea cambiar el nombre.")
    nuevo_nombre = input("Nuevo nombre: ").strip()

    if nuevo_nombre:
        existe = any(a['nombre'].strip().lower() == nuevo_nombre.strip().lower() for a in lista_alumnos if a['id'] != alumno['id'])
        if existe:
            print(f"{Color.YELLOW}Cuidado: Ese nombre ya existe en otro alumno.{Color.END}")
            if input("¿Continuar? (s/n): ").lower() != 's':
                return False

        alumno['nombre'] = nuevo_nombre
        print(f"{Color.GREEN}Nombre actualizado correctamente.{Color.END}")
        time.sleep(0.8)
        return True

    print("No se realizaron cambios.")
    time.sleep(0.6)
    return False

def eliminar_alumno(lista_alumnos, alumno_directo=None):
    if not lista_alumnos:
        print("No hay alumnos registrados.")
        time.sleep(0.6)
        return False

    if alumno_directo is None:
        print(f"\n{Color.RED}--- Eliminar Alumno (BAJA DEFINTIVA) ---{Color.END}")
        try:
            id_str = input("Ingrese el ID del alumno a dar de BAJA: ")
            id_buscado = int(id_str)
            alumno = next((a for a in lista_alumnos if a["id"] == id_buscado), None)
        except ValueError:
            print("ID inválido.")
            return False
    else:
        alumno = alumno_directo

    if not alumno:
        print(f"{Color.RED}Alumno no encontrado.{Color.END}")
        return False

    print(f"{Color.YELLOW}Va a eliminar a: {Color.BOLD}{alumno['nombre']}{Color.END}")
    print("Esta acción borrará sus calificaciones y asistencias. NO SE PUEDE DESHACER.")
    confirmacion = input(f"Escriba 'ELIMINAR' para confirmar: ")

    if confirmacion == "ELIMINAR":
        lista_alumnos.remove(alumno)
        print(f"{Color.GREEN}Alumno eliminado del sistema.{Color.END}")
        time.sleep(0.8)
        return True
    else:
        print("Operación cancelada.")
        time.sleep(0.6)
        return False

# --- Asistencia ---
def tomar_lista_por_fecha(lista_alumnos, tupla_fecha):
    fecha_str = formatear_fecha_tupla(tupla_fecha)
    ya_tomada = any(fecha_str in a.get("historial_asistencia", {}) for a in lista_alumnos)

    if ya_tomada:
        print(f"\n{Color.YELLOW}¡ALERTA DE INTEGRIDAD!{Color.END}")
        print(f"La asistencia del día {Color.BOLD}{fecha_str}{Color.END} ya fue registrada previamente.")
        print(" [1] Modificar asistencia de UN alumno (Modo Seguro)")
        print(" [2] Cancelar")

        opcion = input("Opción: ")

        if opcion == "1":
            try:
                ver_lista_completa(lista_alumnos)
                id_mod = int(input("Ingrese el ID del alumno a corregir: "))
                alumno = next((a for a in lista_alumnos if a["id"] == id_mod), None)

                if alumno:
                    estado_actual = alumno["historial_asistencia"].get(fecha_str, "No registrado")
                    print(f"Alumno: {Color.BOLD}{alumno['nombre']}{Color.END} | Estado Actual: {estado_actual}")
                    nuevo_resp = input("Nuevo estado (Enter=Sí / N=No): ").upper()
                    nuevo_estado = "N" if nuevo_resp == "N" else "S"
                    alumno["historial_asistencia"][fecha_str] = nuevo_estado
                    print(f"{Color.GREEN}Corregido.{Color.END}")
                    return True
            except ValueError:
                return False
        return False

    print(f"\nPasando lista ({fecha_str}):")
    hubo_cambios = False
    for alumno in lista_alumnos:
        resp = input(f" - {alumno['nombre']}: ¿Asistió? (Enter=Sí / N=No): ").upper()
        estado = "N" if resp == "N" else "S"
        if "historial_asistencia" not in alumno:
            alumno["historial_asistencia"] = {}
        if alumno["historial_asistencia"].get(fecha_str) != estado:
            alumno["historial_asistencia"][fecha_str] = estado
            hubo_cambios = True
    print("Asistencia local registrada.")
    time.sleep(0.6)
    return hubo_cambios

def ver_lista_completa(lista_alumnos):
    print(f"\n{Color.CYAN}--- Lista de Alumnos en el Ciclo Actual ---{Color.END}")
    if not lista_alumnos:
        print(f"{Color.YELLOW}No hay alumnos registrados.{Color.END}")
        return

    print(f"{'ID':<5} | {'Nombre':<30}")
    print("-" * 40)
    for alumno in lista_alumnos:
        print(f"{str(alumno['id']):<5} | {alumno['nombre']}")
    print("-" * 40)
    input("Presione Enter para continuar...")

# --- Calcular final de periodo (sin redondeo) ---
def calcular_final_periodo(periodo_data, meta_encuadre):
    # periodo_data: dict con keys tareas(float), trabajos:{"porcentaje": float}, proyecto, valores, examen
    t = float(periodo_data.get("tareas", 0.0) or 0.0)
    trabajos_por = float(periodo_data.get("trabajos", {}).get("porcentaje", 0.0) or 0.0)
    proj = float(periodo_data.get("proyecto", 0.0) or 0.0)
    val = float(periodo_data.get("valores", 0.0) or 0.0)
    ex = float(periodo_data.get("examen", 0.0) or 0.0)

    enc = meta_encuadre or ENCUADRE_POR_DEFECTO
    final = (t * (enc["tareas"]/100.0) +
             trabajos_por * (enc["trabajos"]/100.0) +
             proj * (enc["proyecto"]/100.0) +
             val * (enc["valores"]/100.0) +
             ex * (enc["examen"]/100.0))
    return final

# --- Captura de Calificaciones (Nuevo flujo: Manual y en Bucle) ---
def capturar_calificaciones(lista_alumnos, meta_encuadre, meta_trabajos):
    print(f"\n{Color.CYAN}--- Capturar Calificaciones ---{Color.END}")
    if not lista_alumnos:
        print("No hay alumnos registrados.")
        time.sleep(1.0)
        return False

    try:
        id_str = input("Ingrese el ID del alumno: ")
        id_buscado = int(id_str)
        alumno = next((a for a in lista_alumnos if a["id"] == id_buscado), None)
    except ValueError:
        print("ID inválido.")
        time.sleep(0.6)
        return False

    if not alumno:
        print(f"{Color.RED}Alumno no encontrado.{Color.END}")
        time.sleep(0.6)
        return False

    # Asegurar estructura nueva
    migrar_alumno_si_necesario(alumno)

    print(f"Alumno seleccionado: {Color.BOLD}{alumno['nombre']}{Color.END}")
    campos = list(alumno["calificaciones"].keys())
    for i, campo in enumerate(campos):
        print(f" {i+1}. {campo}")

    try:
        opcion = int(input("Seleccione campo formativo: "))
        if opcion < 1 or opcion > len(campos): raise ValueError
        campo_seleccionado = campos[opcion-1]
    except ValueError:
        print("Entrada inválida.")
        time.sleep(0.6)
        return False

    # --- SELECCIÓN MANUAL DE PERIODO ---
    print(f"\n{Color.CYAN}Seleccione el Periodo a calificar:{Color.END}")
    print(" [1] Primer Periodo (P1)")
    print(" [2] Segundo Periodo (P2)")
    print(" [3] Tercer Periodo (P3)")
    
    try:
        op_p = int(input("Opción: "))
        if op_p not in [1, 2, 3]: raise ValueError
        periodo_elegido = f"p{op_p}"
    except ValueError:
        print("Periodo inválido.")
        time.sleep(0.6)
        return False

    print(f"Editando: {Color.BOLD}{campo_seleccionado} - {periodo_elegido.upper()}{Color.END}")

    # --- BUCLE PARA CAPTURAR TODO DE GOLPE ---
    criterios_disponibles = ["tareas", "trabajos", "proyecto", "valores", "examen"]
    hubo_cambios = False

    while True:
        # Mostramos estado actual para referencia rápida
        datos_actuales = alumno["calificaciones"][campo_seleccionado][periodo_elegido]
        print(f"\n{Color.YELLOW}--- Seleccione Criterio para {periodo_elegido.upper()} ---{Color.END}")
        print(f" [1] Tareas   (Actual: {datos_actuales.get('tareas', 0)})")
        # Mostrar trabajos de forma especial
        info_trabs = datos_actuales.get('trabajos', {})
        print(f" [2] Trabajos (Entregados: {info_trabs.get('entregados', 0)} -> {info_trabs.get('porcentaje', 0):.1f}%)")
        print(f" [3] Proyecto (Actual: {datos_actuales.get('proyecto', 0)})")
        print(f" [4] Valores  (Actual: {datos_actuales.get('valores', 0)})")
        print(f" [5] Examen   (Actual: {datos_actuales.get('examen', 0)})")
        print(f"{Color.GREEN} [0] GUARDAR Y SALIR{Color.END}")

        try:
            op_crit = int(input("Opción: "))
            if op_crit == 0:
                break # Rompe el bucle y termina la función
            if not (1 <= op_crit <= 5): raise ValueError
            criterio = criterios_disponibles[op_crit-1]
        except ValueError:
            print("Opción inválida.")
            continue

        # Lógica de 'trabajos'
        periodo_max_key = {"p1":"p1_max","p2":"p2_max","p3":"p3_max"}[periodo_elegido]
        
        if criterio == "trabajos":
            # Validar máximo si no existe
            if meta_trabajos is None:
                meta_trabajos = {"p1_max":0,"p2_max":0,"p3_max":0}
            if meta_trabajos.get(periodo_max_key, 0) == 0:
                try:
                    max_trab = int(input(f"Defina el TOTAL de trabajos para {periodo_elegido.upper()} (para todo el grupo): "))
                    if max_trab <= 0: raise ValueError
                    meta_trabajos[periodo_max_key] = max_trab
                except ValueError:
                    print("Valor inválido.")
                    continue
            
            # Pedir entregados
            try:
                max_actual = meta_trabajos[periodo_max_key]
                print(f"Total de trabajos del periodo: {max_actual}")
                entregados = int(input("¿Cuántos entregó el alumno?: "))
                if entregados < 0: raise ValueError
            except ValueError:
                print("Entrada inválida.")
                continue

            # Calcular porcentaje
            porcentaje = 0.0
            if max_actual > 0:
                porcentaje = (entregados / float(max_actual)) * 100.0
                if porcentaje > 100.0: porcentaje = 100.0
            
            alumno["calificaciones"][campo_seleccionado][periodo_elegido]["trabajos"]["entregados"] = entregados
            alumno["calificaciones"][campo_seleccionado][periodo_elegido]["trabajos"]["porcentaje"] = porcentaje
            print(f"{Color.GREEN}Registrado: {porcentaje:.2f}%{Color.END}")

        else:
            # Criterios normales 0-100
            try:
                val = float(input(f"Calificación para {criterio.upper()} (0-100): "))
                if val < 0 or val > 100: raise ValueError
            except ValueError:
                print("Entrada inválida.")
                continue
            
            alumno["calificaciones"][campo_seleccionado][periodo_elegido][criterio] = val
            print(f"{Color.GREEN}Dato actualizado.{Color.END}")

        # Recalcular final AUTOMÁTICAMENTE en cada cambio dentro del bucle
        nuevo_final = calcular_final_periodo(
            alumno["calificaciones"][campo_seleccionado][periodo_elegido],
            meta_encuadre or ENCUADRE_POR_DEFECTO
        )
        alumno["calificaciones"][campo_seleccionado][periodo_elegido]["final"] = nuevo_final
        print(f"--> Promedio Parcial {periodo_elegido.upper()}: {Color.BOLD}{nuevo_final:.2f}{Color.END}")
        hubo_cambios = True

    # Al salir del bucle (opción 0)
    if hubo_cambios:
        print("Guardando datos...")
        time.sleep(0.5)
        return True, meta_trabajos
    else:
        return False
    
# --- Consultar alumno con detalle por campos, periodos y promedios ---
def consultar_alumno_completo(lista_alumnos):
    try:
        id_buscado = int(input("Ingrese ID del alumno a consultar: "))
    except ValueError:
        print("ID inválido.")
        return False

    alumno = next((a for a in lista_alumnos if a["id"] == id_buscado), None)
    if not alumno:
        print(f"{Color.RED}Alumno no encontrado.{Color.END}")
        time.sleep(0.6)
        return False

    migrar_alumno_si_necesario(alumno)

    while True:
        limpiar_pantalla()
        print(f"{Color.BOLD}>>> EXPEDIENTE DEL ALUMNO <<<{Color.END}")
        print(f"ID: {alumno['id']}  |  Nombre: {Color.CYAN}{alumno['nombre']}{Color.END}")
        print("-" * 70)

        historial = alumno.get("historial_asistencia", {})
        total = len(historial)
        asistencias = sum(1 for v in historial.values() if v == "S")
        if total > 0:
            promedio_asistencia = (asistencias / total) * 100
            print(f"Asistencia Global: {promedio_asistencia:.1f}% ({asistencias}/{total})")
        else:
            print("Asistencia: Sin registros.")

        print("-" * 70)
        print("DETALLE DE CALIFICACIONES POR CAMPO FORMATIVO:")

        promedios_periodos = {"p1":[], "p2":[], "p3":[]}
        for campo, data in alumno["calificaciones"].items():
            print(f"\n{Color.UNDERLINE}{campo}{Color.END}")
            for p in ["p1","p2","p3"]:
                pd = data.get(p, {})
                tareas = pd.get("tareas", 0.0)
                trabajos_ent = pd.get("trabajos", {}).get("entregados", 0)
                trabajos_por = pd.get("trabajos", {}).get("porcentaje", 0.0)
                proyecto = pd.get("proyecto", 0.0)
                valores = pd.get("valores", 0.0)
                examen = pd.get("examen", 0.0)
                final = pd.get("final", 0.0)
                # Mostrar solo si hay algo registrado
                if any([tareas!=0.0, trabajos_ent!=0, proyecto!=0.0, valores!=0.0, examen!=0.0]):
                    print(f" {p.upper()} -> tareas: {tareas}, trabajos: {trabajos_ent} ({trabajos_por:.2f}%), proyecto: {proyecto}, valores: {valores}, examen: {examen} | final: {final:.2f}")
                    promedios_periodos[p].append(final)
                else:
                    print(f" {p.upper()} -> Sin registros.")

        # calcular promedio por periodo (promedio entre campos)
        print("\nRESUMEN DE PROMEDIOS:")
        promedios_periodo_val = {}
        for p in ["p1","p2","p3"]:
            vals = promedios_periodos[p]
            if vals:
                promedios_periodo_val[p] = sum(vals) / len(vals)
                print(f" {p.upper()} PROMEDIO DE CAMPOS: {promedios_periodo_val[p]:.2f}")
            else:
                promedios_periodo_val[p] = None
                print(f" {p.upper()} PROMEDIO DE CAMPOS: ---")

        # Promedio general de los 3 periodos (solo periodos con valor)
        periodos_validos = [v for v in promedios_periodo_val.values() if v is not None]
        if periodos_validos:
            promedio_general = sum(periodos_validos) / len(periodos_validos)
            print(f"\n{Color.BOLD}PROMEDIO GENERAL DE LOS PERIODOS: {promedio_general:.2f}{Color.END}")
        else:
            print(f"\n{Color.BOLD}PROMEDIO GENERAL DE LOS PERIODOS: ---{Color.END}")

        print("-" * 70)
        print(f"\n{Color.YELLOW}Opciones de Expediente:{Color.END}")
        print(" [M] Modificar Nombre")
        print(" [E] Eliminar Alumno (Baja)")
        print(" [V] Volver al Menú Principal")

        opcion = input("\nSeleccione acción: ").upper()
        if opcion == "M":
            if modificar_alumno(lista_alumnos, alumno_directo=alumno):
                return True
        elif opcion == "E":
            if eliminar_alumno(lista_alumnos, alumno_directo=alumno):
                return True
        elif opcion == "V":
            return False
        else:
            print("Opción no válida.")
            time.sleep(0.6)

# --- Menú Principal ---
def menu_matriz(usuario_actual):
    lista_actual = []
    archivo_actual = None
    cambios_sin_guardar = False
    fecha_operacion = pedir_fecha_tupla()
    meta_encuadre = None
    meta_trabajos = {"p1_max":0,"p2_max":0,"p3_max":0}
    meta_fecha_mod = formatear_fecha_tupla(fecha_operacion)

    while True:
        limpiar_pantalla()
        estado_guardado = f"{Color.RED}(SIN GUARDAR){Color.END}" if cambios_sin_guardar else ""
        archivo_display = archivo_actual if archivo_actual else "Ninguno (Memoria)"
        print(f"Usuario: {Color.BLUE}{usuario_actual}{Color.END} | Ciclo Escolar: {archivo_display} {estado_guardado}")
        print(f"Fecha Op: {formatear_fecha_tupla(fecha_operacion)}")
        print("-" * 60)
        matriz = [
            ["[1] Nuevo Ciclo Escolar", "[2] Cargar Ciclo      "],
            ["[3] Guardar Cambios    ", "[4] Cerrar Sesión     "],
            ["[5] Registrar Alumno   ", "[6] Ver Lista Alumnos "],
            ["[7] Capturar Calif.    ", "[8] Tomar Asistencia  "],
            ["[9] Consultar Alumno   ", "[0] Salir del Sistema "]
        ]
        for fila in matriz:
            print(f"{fila[0]}   |   {fila[1]}")
        print("-" * 60)

        inicio = time.time()
        seleccion = input("Opción: ")
        if (time.time() - inicio) > 600:
            if input("¿Seguir? (si/no): ").lower() != "si": return

        if seleccion == "1":
            # Crear nuevo ciclo y pedir encuadre (una sola vez por ciclo)
            if cambios_sin_guardar:
                if input("¿Perder cambios? (s/n): ").lower() != 's':
                    continue
            nombre = input("Nombre del Ciclo (ej: Ciclo_2025_GrupoA): ").strip()
            if not nombre:
                print("Nombre inválido.")
                time.sleep(0.6)
                continue

            # Pedir encuadre y validar suma 100
            print("Define el ENCUADRE (porcentajes) para este ciclo. La suma debe ser 100.")
            enc_temp = {}
            try:
                enc_temp["tareas"] = float(input("Tareas (%): ") or ENCUADRE_POR_DEFECTO["tareas"])
                enc_temp["trabajos"] = float(input("Trabajos (%): ") or ENCUADRE_POR_DEFECTO["trabajos"])
                enc_temp["proyecto"] = float(input("Proyecto final (%): ") or ENCUADRE_POR_DEFECTO["proyecto"])
                enc_temp["valores"] = float(input("Valores y actitudes (%): ") or ENCUADRE_POR_DEFECTO["valores"])
                enc_temp["examen"] = float(input("Examen (%): ") or ENCUADRE_POR_DEFECTO["examen"])
            except ValueError:
                print("Entradas inválidas. Se canceló la creación.")
                time.sleep(0.6)
                continue
            total = sum(enc_temp.values())
            if abs(total - 100.0) > 0.001:
                print(f"{Color.RED}Error: La suma de porcentajes es {total}, debe ser 100.{Color.END}")
                time.sleep(1.0)
                continue

            archivo_actual = nombre
            lista_actual = []
            cambios_sin_guardar = True
            meta_encuadre = enc_temp
            meta_trabajos = {"p1_max":0,"p2_max":0,"p3_max":0}
            meta_fecha_mod = formatear_fecha_tupla(fecha_operacion)
            print(f"{Color.GREEN}Ciclo '{archivo_actual}' creado con encuadre definido.{Color.END}")
            time.sleep(1.0)

        elif seleccion == "2":
            if cambios_sin_guardar:
                if input("¿Perder cambios? (s/n): ").lower() != 's':
                    continue
            nom, enc, trabs, fecha_mod, lst = cargar_clase()
            if nom:
                archivo_actual = nom
                meta_encuadre = enc
                meta_trabajos = trabs
                meta_fecha_mod = fecha_mod
                lista_actual = lst
                # Migrar alumnos si necesitan estructura nueva
                for a in lista_actual:
                    migrar_alumno_si_necesario(a)
                cambios_sin_guardar = False

        elif seleccion == "3":
            if archivo_actual:
                if guardar_clase(archivo_actual, lista_actual, fecha_operacion, meta_encuadre, meta_trabajos):
                    cambios_sin_guardar = False
            else:
                print(f"\n{Color.YELLOW}Guardar como:{Color.END}")
                if os.path.exists(DIR_DATOS):
                    archivos = [f for f in os.listdir(DIR_DATOS) if f.endswith('.txt')]
                else:
                    archivos = []
                dict_archivos = {str(i+1): archivo for i, archivo in enumerate(archivos)}
                print(" [0] Crear NUEVO")
                for k, v in dict_archivos.items(): print(f" [{k}] Fusionar en '{v.replace('.txt', '')}'")
                opcion_guardar = input("Opción: ")
                if opcion_guardar == "0":
                    nombre_nuevo = input("Nombre nuevo: ")
                    if os.path.exists(os.path.join(DIR_DATOS, f"{nombre_nuevo}.txt")):
                        print("Existe.")
                    else:
                        archivo_actual = nombre_nuevo
                        if guardar_clase(archivo_actual, lista_actual, fecha_operacion, meta_encuadre, meta_trabajos):
                            cambios_sin_guardar = False
                elif opcion_guardar in dict_archivos:
                    archivo_destino = dict_archivos[opcion_guardar]
                    nombre_destino = archivo_destino.replace(".txt", "")
                    contenido_existente = leer_archivo_clase(os.path.join(DIR_DATOS, archivo_destino))
                    lista_existente = contenido_existente.get("alumnos", [])
                    ultimo_id = max([a['id'] for a in lista_existente]) if lista_existente else 0
                    for alumno_mem in lista_actual:
                        coincidencia = next((a for a in lista_existente if a['nombre'].strip().lower() == alumno_mem['nombre'].strip().lower()), None)
                        if coincidencia:
                            if input(f"¿Actualizar a {alumno_mem['nombre']}? (s/n): ").lower() == 's':
                                if "historial_asistencia" in alumno_mem:
                                    coincidencia.setdefault("historial_asistencia", {}).update(alumno_mem["historial_asistencia"])
                                coincidencia.setdefault("calificaciones", {}).update(alumno_mem.get("calificaciones", {}))
                                continue
                        ultimo_id += 1
                        alumno_mem['id'] = ultimo_id
                        lista_existente.append(alumno_mem)
                    # Guardar fusionado usando el encuadre existente del archivo destino si existe
                    if guardar_clase(nombre_destino, lista_existente, fecha_operacion, contenido_existente.get("meta_encuadre"), contenido_existente.get("meta_trabajos")):
                        lista_actual = lista_existente
                        archivo_actual = nombre_destino
                        cambios_sin_guardar = False
                else:
                    print("Cancelado.")

        elif seleccion == "4":
            if cambios_sin_guardar:
                if input("¿Salir sin guardar? (s/n): ").lower() != 's':
                    continue
            return

        elif seleccion == "5":
            if registrar_alumno(lista_actual):
                cambios_sin_guardar = True
            else:
                time.sleep(0.6)

        elif seleccion == "6":
            if lista_actual:
                ver_lista_completa(lista_actual)
            else:
                print("Cargue ciclo.")
                time.sleep(0.6)

        elif seleccion == "7":
            if lista_actual:
                ver_lista_completa(lista_actual)
                result = capturar_calificaciones(lista_actual, meta_encuadre, meta_trabajos)
                if result:
                    # capturar_calificaciones devuelve tuple cuando éxito con posible meta_trabajos actualizado
                    if isinstance(result, tuple):
                        success, mt = result
                        if success:
                            meta_trabajos = mt or meta_trabajos
                            cambios_sin_guardar = True
                    elif result is True:
                        cambios_sin_guardar = True
            else:
                print("Cargue ciclo.")
                time.sleep(0.6)

        elif seleccion == "8":
            if lista_actual:
                if tomar_lista_por_fecha(lista_actual, fecha_operacion):
                    cambios_sin_guardar = True
            else:
                print("Cargue ciclo.")
                time.sleep(0.6)

        elif seleccion == "9":
            if lista_actual:
                if consultar_alumno_completo(lista_actual):
                    cambios_sin_guardar = True
            else:
                print("Cargue ciclo.")
                time.sleep(0.6)

        elif seleccion == "0":
            if cambios_sin_guardar:
                if input("¿Guardar cambios antes de salir? (s/n): ").lower() == 's':
                    if not archivo_actual:
                        archivo_actual = input("Nombre: ")
                    guardar_clase(archivo_actual, lista_actual, fecha_operacion, meta_encuadre, meta_trabajos)
            print("Saliendo...")
            input("Presione Enter para cerrar...")
            sys.exit()

        else:
            print("Opción inválida.")
            time.sleep(0.6)

def main():
    asegurar_directorios()
    while True:
        usuario_logueado = sistema_login()
        mostrar_bienvenida(usuario_logueado)
        menu_matriz(usuario_logueado)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n{Color.RED}ERROR CRÍTICO DEL SISTEMA:{Color.END}")
        print(e)
        input("\nPresione Enter para salir...")
