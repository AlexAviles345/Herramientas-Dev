# Generador de PDF por tamaño

Herramienta gráfica (GUI) que permite generar archivos PDF de un tamaño específico (en MB) o de un número de páginas fijas.

## 🛠️ Tecnologías

- Python 3
- Tkinter (Interfaz Gráfica)
- ReportLab (Generación y Encriptación de PDFs)

## Requisitos

Instalar las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## Uso

Ejecuta el script principal para abrir la ventana de la aplicación:

```bash
python generador_pdf.py
```

### Modos de Generación:
1. **Modo Texto (Clásico)**: Utiliza una calibración matemática para calcular exactamente cuántas líneas de texto se necesitan para alcanzar el peso deseado. Es muy preciso pero puede tardar un poco para archivos de cientos de MB.
2. **Modo Inflador (Rápido)**: Ingresas el número de páginas que quieres y el peso final. El sistema genera el PDF base e inyecta bytes transparentes (padding) al final del archivo para inflarlo instantáneamente al peso exacto deseado sin tener que escribir millones de líneas.

### Seguridad
Incluye una opción para **Proteger con contraseña** el PDF generado mediante encriptación nativa. Ideal para probar validaciones de seguridad y subidas de archivos bloqueados.
