# 🎓 Maestra Pro v3.0 (CLI)

Una herramienta de línea de comandos robusta y eficiente desarrollada en Python para facilitar a los docentes la administración de calificaciones, asistencias y ciclos escolares. Diseñada para maximizar la productividad con flujos de trabajo rápidos y persistencia de datos local.

## 🚀 Características Principales

* **Gestión de Ciclos Escolares:** Creación, carga y guardado de múltiples grupos o ciclos escolares.
* **Persistencia de Datos:** Todo se guarda localmente en archivos JSON estructurados, permitiendo recuperar el trabajo en cualquier momento.
* **Encuadre Personalizable:** El docente define los porcentajes de evaluación al inicio (Tareas, Trabajos, Proyectos, Valores, Examen).
* **Control de Asistencias:** Registro diario de asistencias con validación de fechas para evitar duplicados.
* **Sistema de Calificaciones Ágil:**
    * Soporte para 3 Periodos (P1, P2, P3).
    * Cálculo automático de promedios basado en el encuadre.
    * **Modo de Captura Rápida:** Bucle de ingreso de datos para calificar múltiples criterios sin salir del menú.
* **Seguridad Básica:** Sistema de Login y Registro de usuarios (docentes) local.
* **Interfaz Visual:** Uso de códigos de color ANSI para una experiencia de usuario clara y legible en la terminal.

## 🛠️ Requisitos del Sistema

* **Python 3.6** o superior.
* Sistema Operativo: Windows, macOS o Linux.
* No requiere librerías externas (usa solo la librería estándar de Python).

## 📂 Estructura del Proyecto

El sistema generará automáticamente las carpetas necesarias al ejecutarse por primera vez:

```text
/
├── final.py                  # Script principal del sistema
├── usuarios_registrados.txt  # Base de datos local de usuarios (se crea al registrarse)
└── datos_clases/             # Carpeta donde se guardan los JSON de cada ciclo escolar
    ├── Ciclo_2025_A.txt
    └── ...
```
## ⚡ Guía de Inicio Rápido

Sigue estos pasos para poner en marcha el sistema en tu entorno local:

1.  **Pre-requisitos:**
    Asegúrate de tener Python instalado. Puedes verificarlo escribiendo en tu terminal:
    ```bash
    python --version
    ```

2.  **Instalación:**
    Simplemente descarga el archivo `final.py` en una carpeta de tu preferencia.

3.  **Ejecución:**
    Abre tu terminal en la carpeta del proyecto y ejecuta:
    ```bash
    python final.py
    ```

4.  **Primeros Pasos en el Sistema:**
    * **Paso 1:** Selecciona **[2] Registrarse** para crear tu cuenta de docente (Usuario/Contraseña).
    * **Paso 2:** Inicia sesión.
    * **Paso 3:** Crea tu primer grupo con **[1] Nuevo Ciclo Escolar** y define tus porcentajes de evaluación.
    * **Paso 4:** Registra alumnos con la opción **[5]**.
    * **Paso 5:** ¡Empieza a calificar! Ve a **[7] Capturar Calif.** y sigue el flujo interactivo.

---

## 📸 Capturas de Funcionalidad

El sistema opera completamente en la terminal con una interfaz limpia y colorida.

**1. Menú Principal (Dashboard):**
El centro de control donde gestionas todo el ciclo escolar.
```text
Usuario: BETO | Ciclo Escolar: Ciclo_2025_A (SIN GUARDAR)
Fecha Op: 01/12/2025
------------------------------------------------------------
[1] Nuevo Ciclo Escolar   |   [2] Cargar Ciclo      
[3] Guardar Cambios       |   [4] Cerrar Sesión     
[5] Registrar Alumno      |   [6] Ver Lista Alumnos 
[7] Capturar Calif.       |   [8] Tomar Asistencia  
[9] Consultar Alumno      |   [0] Salir del Sistema 
------------------------------------------------------------
```
