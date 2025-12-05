# test_core.py
from modules.auth import registrar_usuario, login_usuario
from modules.ciclos import crear_ciclo, establecer_max_trabajos
from modules.alumnos import agregar_alumno, obtener_alumnos, registrar_calificacion, calcular_promedio_periodo

print("--- INICIANDO TEST DEL NÚCLEO ---")

# 1. Login rápido (usamos un usuario de prueba)
usuario = "ProfeTest"
registrar_usuario(usuario, "123") # Por si no existe
user_id = login_usuario(usuario, "123")

# 2. Crear Ciclo con Encuadre
encuadre = {
    'tareas': 10, 'trabajos': 50, 'proyecto': 20, 'valores': 10, 'examen': 10
}
ciclo_id = crear_ciclo(user_id, "Grupo Beta Testing", encuadre)
print(f"1. Ciclo creado ID: {ciclo_id}")

# 3. CONFIGURAR TRABAJOS DIFERENTES POR MATERIA (Tu requerimiento)
# Lenguajes: 20 trabajos totales
establecer_max_trabajos(ciclo_id, "Lenguajes", 1, 20)
# Saberes: 10 trabajos totales
establecer_max_trabajos(ciclo_id, "Saberes", 1, 10)
print("2. Trabajos configurados: Lenguajes=20, Saberes=10")

# 4. Agregar Alumno
agregar_alumno(ciclo_id, "Juanito Bananas")
alumnos = obtener_alumnos(ciclo_id)
alumno_id = alumnos[0][0] # Tomamos el ID del primero
print(f"3. Alumno registrado: Juanito (ID {alumno_id})")

# 5. CALIFICAR
# Juanito entregó 10 trabajos en ambas materias
registrar_calificacion(alumno_id, "Lenguajes", 1, "trabajos", 10)
registrar_calificacion(alumno_id, "Saberes", 1, "trabajos", 10)

# 6. VER RESULTADOS
print("\n--- RESULTADOS DEL CÁLCULO ---")

# Calculamos Lenguajes (Entregó 10 de 20 -> 50% de la calificación de trabajos)
# El rubro trabajos vale 50 puntos totales. Debería obtener 25 puntos.
promedio_len = calcular_promedio_periodo(alumno_id, ciclo_id, "Lenguajes", 1, encuadre)
print(f"Lenguajes (10/20 trabajos): {promedio_len} (Esperado: 25.0)")

# Calculamos Saberes (Entregó 10 de 10 -> 100% de la calificación de trabajos)
# El rubro trabajos vale 50 puntos totales. Debería obtener 50 puntos.
promedio_sab = calcular_promedio_periodo(alumno_id, ciclo_id, "Saberes", 1, encuadre)
print(f"Saberes   (10/10 trabajos): {promedio_sab} (Esperado: 50.0)")

if promedio_len == 25.0 and promedio_sab == 50.0:
    print("\n✅ ÉXITO TOTAL: El sistema maneja máximos de trabajos diferentes por materia.")
else:
    print("\n❌ ALGO FALLÓ en los cálculos.")