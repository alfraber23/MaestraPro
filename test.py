# test_auth.py
from modules.auth import registrar_usuario, login_usuario

# 1. Intentamos registrar a Beto
print("--- PRUEBA DE REGISTRO ---")
exito, mensaje = registrar_usuario("Beto", "12345")
print(f"Intento 1: {mensaje}")

# 2. Intentamos registrar a Beto OTRA VEZ (debería fallar)
exito, mensaje = registrar_usuario("Beto", "otra_pass")
print(f"Intento 2 (Duplicado): {mensaje}")

# 3. Prueba de Login Incorrecto
print("\n--- PRUEBA DE LOGIN ---")
user_id = login_usuario("Beto", "pass_incorrecta")
if user_id:
    print("ERROR: Login exitoso con contraseña mala.")
else:
    print("CORRECTO: Login falló con contraseña mala.")

# 4. Prueba de Login Correcto
user_id = login_usuario("Beto", "12345")
if user_id:
    print(f"CORRECTO: Bienvenido usuario ID {user_id}")
else:
    print("ERROR: Login falló con contraseña buena.")