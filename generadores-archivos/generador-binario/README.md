# Generador de Archivos Binarios (Datos Crudos)

Herramienta gráfica diseñada para generar archivos binarios (`.bin`, `.dat`, etc.) de tamaños específicos. Es ideal para realizar pruebas de rendimiento, cuotas de almacenamiento, límites de subida en la web o pruebas de red (throughput).

## 🛠️ Tecnologías

- Python 3
- Tkinter (Interfaz Gráfica Integrada)
- Módulo `os` nativo (Generación de bytes y urandom)

## Requisitos

No requiere instalación de librerías externas. Solo necesitas tener Python instalado.

## Uso

Ejecuta el script principal para abrir la interfaz:

```bash
python generador_binario.py
```

### Modos de Relleno

La herramienta te permite elegir de qué estará lleno el archivo generado, lo cual es crítico dependiendo de tu caso de uso:

1. **Ceros (`\0`)**: El archivo se llena de bytes nulos. Es rapidísimo de generar, pero los sistemas operativos y servidores modernos (como compresión gzip/brotli en web) pueden comprimirlo casi a cero durante una transferencia.
2. **Aleatorio (`urandom`)**: Llena el archivo con ruido puro (criptográficamente seguro). Es **imposible de comprimir**, lo que lo hace perfecto para pruebas reales de ancho de banda o límites estrictos de disco.
3. **Patrón Repetitivo**: Eliges una palabra o patrón (ej. `PRUEBA`) y el archivo se llena repitiendo esa palabra infinitamente hasta alcanzar el peso. Útil para verificar integridad de datos con editores hexadecimales.

*Nota: Todos los archivos generados se guardan de forma segura en la carpeta `salida/`.*
