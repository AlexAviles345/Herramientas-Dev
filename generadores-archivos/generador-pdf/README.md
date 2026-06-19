# Generador de PDF por tamaño

Esta herramienta permite generar archivos PDF de un tamaño específico (en MB).

## Requisitos

Instalar las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## Uso

Ejecutar el script principal:

```bash
python generador_pdf.py
```

El script solicitará el tamaño deseado en MB y el modo de generación:
1. **Rápido**: Utiliza una estimación precalculada. Usa menos disco y es más rápido, pero puede ser menos preciso.
2. **Preciso**: Realiza una calibración doble. Genera muestras temporales para calcular con mayor exactitud el tamaño final.
