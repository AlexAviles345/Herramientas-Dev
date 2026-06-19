from reportlab.pdfgen import canvas
import os
import math

os.makedirs("salida", exist_ok=True)

ARCHIVO_TEMP = "salida/pdf_temporal.pdf"

# Datos obtenidos de pruebas previas
MB_POR_LINEA_ESTIMADO = 70.07 / 290000

# Solo para calibración
MUESTRA_LINEAS = 20000


def generar_pdf(nombre_archivo, total_lineas):
    pdf = canvas.Canvas(nombre_archivo, pageCompression=0)

    y = 800
    pagina = 1

    for i in range(total_lineas):

        texto = (
            f"Pagina {pagina} Registro {i} "
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
            "abcdefghijklmnopqrstuvwxyz "
            "0123456789 "
            "Lorem ipsum dolor sit amet consectetur adipiscing elit "
            "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        )

        pdf.drawString(20, y, texto)

        y -= 15

        if y < 50:
            pdf.showPage()
            pagina += 1
            y = 800

        if i % 10000 == 0 and i > 0:
            print(f"Procesadas {i:,} lineas...")

    pdf.save()


def mostrar_resultado(objetivo_mb, archivo):
    tamano_real = os.path.getsize(archivo) / (1024 * 1024)

    print("\n=== RESULTADO ===")
    print("Archivo:", os.path.abspath(archivo))
    print(f"Tamaño solicitado: {objetivo_mb:.2f} MB")
    print(f"Tamaño obtenido:   {tamano_real:.2f} MB")
    print(f"Diferencia:        {tamano_real - objetivo_mb:+.2f} MB")


def modo_rapido(objetivo_mb):
    print("\n=== MODO RÁPIDO ===")

    tamano_str = f"{objetivo_mb:g}".replace(".", "_")
    archivo_final = f"salida/pdf_generado_{tamano_str}MB.pdf"

    total_lineas = int(objetivo_mb / MB_POR_LINEA_ESTIMADO)

    print(f"Líneas estimadas: {total_lineas:,}")
    print("Generando PDF...\n")

    generar_pdf(archivo_final, total_lineas)

    mostrar_resultado(objetivo_mb, archivo_final)


def modo_preciso(objetivo_mb):
    print("\n=== MODO PRECISO ===")

    tamano_str = f"{objetivo_mb:g}".replace(".", "_")
    archivo_final = f"salida/pdf_generado_{tamano_str}MB.pdf"

    print("\n[1/4] Generando muestra de calibración...")

    generar_pdf(ARCHIVO_TEMP, MUESTRA_LINEAS)

    tamano_muestra = os.path.getsize(ARCHIVO_TEMP) / (1024 * 1024)

    print(f"Muestra: {MUESTRA_LINEAS:,} líneas")
    print(f"Tamaño muestra: {tamano_muestra:.4f} MB")

    mb_por_linea = tamano_muestra / MUESTRA_LINEAS

    lineas_estimadas = math.ceil(objetivo_mb / mb_por_linea)

    print("\n[2/4] Primera estimación...")
    print(f"Líneas estimadas: {lineas_estimadas:,}")

    os.remove(ARCHIVO_TEMP)

    print("\n[3/4] Generando PDF de prueba...")

    generar_pdf(ARCHIVO_TEMP, lineas_estimadas)

    tamano_prueba = os.path.getsize(ARCHIVO_TEMP) / (1024 * 1024)

    print(f"Tamaño obtenido: {tamano_prueba:.2f} MB")

    factor_correccion = objetivo_mb / tamano_prueba

    lineas_corregidas = math.ceil(
        lineas_estimadas * factor_correccion
    )

    print("\nCorrección aplicada")
    print(f"Factor: {factor_correccion:.6f}")
    print(f"Líneas corregidas: {lineas_corregidas:,}")

    os.remove(ARCHIVO_TEMP)

    print("\n[4/4] Generando PDF final...")

    generar_pdf(archivo_final, lineas_corregidas)

    mostrar_resultado(objetivo_mb, archivo_final)


# ---------------------------
# MENÚ PRINCIPAL
# ---------------------------

print("===================================")
print(" GENERADOR DE PDF POR TAMAÑO")
print("===================================")

objetivo_mb = float(input("\nTamaño deseado (MB): "))

print("\nSeleccione el modelo:")
print("1 - Rápido (menos uso de disco)")
print("2 - Preciso (doble calibración)")

opcion = input("\nOpción: ").strip()

if opcion == "1":
    modo_rapido(objetivo_mb)

elif opcion == "2":
    modo_preciso(objetivo_mb)

else:
    print("\nOpción no válida.")
