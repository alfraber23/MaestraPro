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
