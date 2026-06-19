import tkinter as tk
from tkinter import ttk, messagebox
import os
import math
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pdfencrypt import StandardEncryption

os.makedirs("salida", exist_ok=True)
ARCHIVO_TEMP = "salida/pdf_temporal.pdf"
MB_POR_LINEA_ESTIMADO = 70.07 / 290000
MUESTRA_LINEAS = 20000

class PDFGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de PDF")
        self.root.geometry("450x450")
        self.root.resizable(False, False)

        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both", padx=10, pady=(10, 5))

        self.tab_texto = ttk.Frame(self.notebook)
        self.tab_inflador = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_texto, text="Modo Texto (Clásico)")
        self.notebook.add(self.tab_inflador, text="Modo Inflador (Rápido)")

        self.setup_tab_texto()
        self.setup_tab_inflador()

        # Encriptación
        enc_frame = ttk.LabelFrame(self.root, text="Seguridad", padding=10)
        enc_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.enc_var = tk.BooleanVar(value=False)
        enc_check = ttk.Checkbutton(enc_frame, text="Proteger con contraseña", variable=self.enc_var, command=self.toggle_password)
        enc_check.pack(anchor="w")

        self.pass_frame = ttk.Frame(enc_frame)
        ttk.Label(self.pass_frame, text="Contraseña:").pack(side="left")
        self.pass_var = tk.StringVar(value="")
        self.pass_entry = ttk.Entry(self.pass_frame, textvariable=self.pass_var, show="*")
        self.pass_entry.pack(side="left", padx=5)

        # Barra de Progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", padx=10, pady=(0, 10))

    def toggle_password(self):
        if self.enc_var.get():
            self.pass_frame.pack(fill="x", pady=5)
        else:
            self.pass_frame.pack_forget()

    def get_encryption(self):
        if self.enc_var.get() and self.pass_var.get():
            pwd = self.pass_var.get()
            return StandardEncryption(pwd, pwd)
        return None

    # ===============================
    # LÓGICA BASE DEL PDF
    # ===============================
    def _escribir_lineas_pdf(self, nombre_archivo, total_lineas, enc=None):
        pdf = canvas.Canvas(nombre_archivo, encrypt=enc, pageCompression=0)
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
            
            # Actualización a la UI para evitar congelamientos completos
            if i % 10000 == 0 or i == total_lineas - 1:
                if hasattr(self, 'progress_var'):
                    self.progress_var.set((i / max(1, total_lineas)) * 100)
                self.root.update()
        pdf.save()

    # ===============================
    # MODO TEXTO (Preciso/Clásico)
    # ===============================
    def setup_tab_texto(self):
        frame = self.tab_texto
        
        ttk.Label(frame, text="Genera un PDF exacto a base de millones de letras.", justify="center").pack(pady=10)
        
        ttk.Label(frame, text="Tamaño deseado (MB):").pack()
        self.texto_mb = ttk.Entry(frame)
        self.texto_mb.insert(0, "5")
        self.texto_mb.pack(pady=5)

        self.texto_modo = tk.StringVar(value="preciso")
        ttk.Radiobutton(frame, text="Modo Preciso (Doble calibración, usa espacio temporal)", variable=self.texto_modo, value="preciso").pack(anchor="w", padx=30, pady=(10, 0))
        ttk.Radiobutton(frame, text="Modo Rápido (Estimación matemática, sin temporales)", variable=self.texto_modo, value="rapido").pack(anchor="w", padx=30, pady=(0, 10))

        ttk.Button(frame, text="Generar PDF", command=self.generate_texto).pack(pady=10)

    def generate_texto(self):
        try:
            target_mb = float(self.texto_mb.get())
            if target_mb <= 0: raise ValueError("El peso debe ser mayor a 0.")
            
            tamano_str = f"{target_mb:g}".replace(".", "_")
            archivo_final = f"salida/pdf_texto_{tamano_str}MB.pdf"
            enc = self.get_encryption()

            # Calibración
            self.progress_var.set(0)
            self.root.config(cursor="wait")
            self.root.update()
            
            if self.texto_modo.get() == "rapido":
                # Modo rápido (sin temporales)
                total_lineas = int(target_mb / MB_POR_LINEA_ESTIMADO)
                self._escribir_lineas_pdf(archivo_final, total_lineas, enc)
            else:
                # Paso 1: Muestra
                self._escribir_lineas_pdf(ARCHIVO_TEMP, MUESTRA_LINEAS, enc)
                tamano_muestra = os.path.getsize(ARCHIVO_TEMP) / (1024 * 1024)
                mb_por_linea = tamano_muestra / MUESTRA_LINEAS
                lineas_estimadas = math.ceil(target_mb / mb_por_linea)
                os.remove(ARCHIVO_TEMP)

                # Paso 2: Prueba
                self._escribir_lineas_pdf(ARCHIVO_TEMP, lineas_estimadas, enc)
                tamano_prueba = os.path.getsize(ARCHIVO_TEMP) / (1024 * 1024)
                factor_correccion = target_mb / tamano_prueba
                lineas_corregidas = math.ceil(lineas_estimadas * factor_correccion)
                os.remove(ARCHIVO_TEMP)

                # Paso 3: Final
                self._escribir_lineas_pdf(archivo_final, lineas_corregidas, enc)
            
            self.root.config(cursor="")
            tamano_real = os.path.getsize(archivo_final) / (1024 * 1024)
            messagebox.showinfo("Completado", f"Archivo: {archivo_final}\nPeso final: {tamano_real:.2f} MB")
            
        except Exception as e:
            self.root.config(cursor="")
            messagebox.showerror("Error", str(e))

    # ===============================
    # MODO INFLADOR
    # ===============================
    def setup_tab_inflador(self):
        frame = self.tab_inflador
        
        ttk.Label(frame, text="Genera un PDF con un número fijo de páginas\ny lo infla inyectando bytes para alcanzar el peso.", justify="center").pack(pady=10)
        
        ttk.Label(frame, text="Número de Páginas:").pack()
        self.infl_pages = ttk.Entry(frame)
        self.infl_pages.insert(0, "5")
        self.infl_pages.pack(pady=5)

        ttk.Label(frame, text="Peso Deseado (MB):").pack()
        self.infl_mb = ttk.Entry(frame)
        self.infl_mb.insert(0, "15")
        self.infl_mb.pack(pady=5)

        ttk.Button(frame, text="Generar e Inflar", command=self.generate_inflador).pack(pady=20)

    def generate_inflador(self):
        try:
            pages = int(self.infl_pages.get())
            target_mb = float(self.infl_mb.get())
            if target_mb <= 0 or pages <= 0: raise ValueError("Páginas y peso deben ser mayores a 0.")
            
            tamano_str = f"{target_mb:g}".replace(".", "_")
            archivo_final = f"salida/pdf_inflado_{tamano_str}MB.pdf"
            enc = self.get_encryption()

            self.progress_var.set(0)
            self.root.config(cursor="wait")
            self.root.update()
            
            # Generar PDF base
            pdf = canvas.Canvas(archivo_final, encrypt=enc)
            for p in range(pages):
                pdf.drawString(200, 400, f"Pagina inflada {p+1} / {pages}")
                pdf.showPage()
            pdf.save()

            # Inflar
            current_size = os.path.getsize(archivo_final)
            target_bytes = int(target_mb * 1024 * 1024)
            
            if current_size < target_bytes:
                with open(archivo_final, 'ab') as f:
                    bytes_to_add = target_bytes - current_size
                    total_to_add = bytes_to_add
                    chunk = 1024 * 1024
                    while bytes_to_add > 0:
                        w = min(chunk, bytes_to_add)
                        f.write(b'\0' * w)
                        bytes_to_add -= w
                        
                        added = total_to_add - bytes_to_add
                        if (added // chunk) % 10 == 0 or bytes_to_add == 0:
                            self.progress_var.set((added / total_to_add) * 100)
                            self.root.update()
                        
            self.root.config(cursor="")
            tamano_real = os.path.getsize(archivo_final) / (1024 * 1024)
            messagebox.showinfo("Completado", f"Archivo: {archivo_final}\nPeso final: {tamano_real:.2f} MB")
            
        except Exception as e:
            self.root.config(cursor="")
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFGeneratorApp(root)
    root.mainloop()
