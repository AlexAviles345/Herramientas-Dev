# Limpiador de Metadatos de Imágenes

Una herramienta web pura (sin backend) para eliminar metadatos ocultos de tus imágenes (como datos EXIF, coordenadas GPS, tipo de cámara, fechas de captura, etc.).

Al utilizar el API nativa de `<canvas>` de HTML5, la imagen se dibuja en memoria dentro del navegador y se re-exporta, destruyendo automáticamente cualquier metadato embebido en el archivo original sin necesidad de enviarla a un servidor. Tu privacidad está 100% garantizada.

## 🛠️ Tecnologías

- HTML5
- CSS3 (Diseño Glassmorphism Premium, oscuro)
- JavaScript (Vanilla, Canvas API)
- [Exif.js](https://github.com/exif-js/exif-js) (Vía CDN, solo para *leer* y mostrar los metadatos al usuario antes de borrarlos).

## 🚀 Cómo Utilizarlo

Este proyecto no requiere instalación, dependencias de Node.js ni servidor de backend.

1. Navega a la carpeta `limpiador-metadatos/limpiador-metadatos-imagenes`.
2. Haz doble clic en el archivo `index.html` para abrirlo en tu navegador.
3. Arrastra una imagen o haz clic para subirla.
4. Presiona el botón **"Descargar Imagen Limpia"**.
5. ¡Listo! Tu nueva imagen descargada no tiene ningún rastro de metadatos.


