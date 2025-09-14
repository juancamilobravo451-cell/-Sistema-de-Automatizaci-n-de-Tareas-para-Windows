# AutoTask - Sistema de Automatización de Tareas para Windows

AutoTask es una aplicación de escritorio desarrollada en Python que automatiza tareas comunes de gestión de archivos en Windows mediante una interfaz intuitiva y fácil de usar.

## Características Principales

- **Renombrado Masivo**: Renombra archivos automáticamente con numeración consistente
- **Organización por Tipo**: Clasifica archivos en subcarpetas según su extensión
- **Eliminación de Duplicados**: Encuentra y elimina archivos duplicados usando hash MD5
- **Limpieza de Temporales**: Elimina archivos temporales y de backup automáticamente
- **Ejecución de Scripts**: Soporta scripts Python (.py) y AutoHotkey (.ahk)
- **Interfaz Moderna**: Diseño limpio y responsive con colores diferenciados
- **Sistema de Logging**: Registro detallado con timestamps y código de colores
- **Persistencia**: Recuerda la última carpeta utilizada entre sesiones

## Requisitos del Sistema

- Windows 7 o superior
- Python 3.6 o superior
- AutoHotkey (opcional, solo para ejecutar scripts .ahk)

## Instalación

1. Clona o descarga el proyecto
2. Asegúrate de tener Python instalado
3. Ejecuta el script principal:

```bash
python autotask.py