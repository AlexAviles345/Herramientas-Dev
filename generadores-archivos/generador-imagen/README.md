# Generador de Imágenes de Prueba (GUI)

Esta es una herramienta visual (interfaz de escritorio) para generar imágenes de prueba configurables. Es ideal para pruebas de estrés, validación de formatos, o para probar límites de almacenamiento y ancho de banda al subir archivos grandes.

## 🛠️ Tecnologías

- Python 3
- Tkinter (Interfaz Gráfica Integrada)
- Pillow / PIL (Manipulación y generación de imágenes)

## Requisitos

Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## Uso

Ejecuta el script principal para abrir la interfaz:

```bash
python generador_imagen.py
```

La herramienta cuenta con 3 modos de operación accesibles mediante pestañas:

1. **Modo Libre**: Tú eliges la resolución (ej. 1920x1080) y el formato (JPG, PNG, BMP, WEBP). El script genera una imagen simple con esas características. El peso dependerá de la compresión del formato elegido.
2. **Modo Peso (BMP)**: Ideal para pesos exactos. Solicitas un peso objetivo en MB (ej. 5 MB) y el sistema calcula la resolución exacta necesaria para que la imagen pese esa cantidad matemáticamente usando el formato BMP sin compresión.
3. **Modo Inflador**: Para casos especiales donde necesitas una imagen válida (en resolución y formato) pero con un peso gigantesco. La herramienta genera una imagen base y luego le inyecta padding (bytes basura) al final del archivo para alcanzar el peso exacto deseado sin corromper la imagen.

*Nota: Todas las imágenes generadas se guardan automáticamente en la carpeta `salida/`.*
