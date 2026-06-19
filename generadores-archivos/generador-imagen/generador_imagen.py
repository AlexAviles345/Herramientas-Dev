import tkinter as tk
from tkinter import ttk, messagebox
import os
import math
from PIL import Image, ImageDraw, ImageFont

class ImageGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Imágenes de Prueba")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

        os.makedirs("salida", exist_ok=True)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both", padx=10, pady=10)

        self.tab_libre = ttk.Frame(self.notebook)
        self.tab_peso = ttk.Frame(self.notebook)
        self.tab_inflador = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_libre, text="Modo Libre")
        self.notebook.add(self.tab_peso, text="Modo Peso (BMP)")
        self.notebook.add(self.tab_inflador, text="Modo Inflador")

        self.setup_tab_libre()
        self.setup_tab_peso()
        self.setup_tab_inflador()

    def draw_centered_text(self, img, text):
        draw = ImageDraw.Draw(img)
        width, height = img.size
        try:
            # Tamaño de letra dinámico basado en la altura
            font_size = max(20, int(height / 15))
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Medir texto
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
        except AttributeError:
            # Para versiones antiguas de Pillow
            text_w, text_h = draw.textsize(text, font=font)

        x = (width - text_w) / 2
        y = (height - text_h) / 2

        # Sombra / Borde
        offset = max(2, int(font_size / 20))
        draw.text((x - offset, y - offset), text, font=font, fill="black")
        draw.text((x + offset, y + offset), text, font=font, fill="black")
        
        # Texto principal
        draw.text((x, y), text, font=font, fill="white")
        return img

    def get_extension(self, fmt):
        if fmt == "JPEG": return ".jpg"
        return "." + fmt.lower()

    # ==========================
    # MODO LIBRE
    # ==========================
    def setup_tab_libre(self):
        frame = self.tab_libre
        
        ttk.Label(frame, text="Genera una imagen con resolución y formato fijos.\nEl peso dependerá del formato.").pack(pady=10)
        
        # Ancho
        ttk.Label(frame, text="Ancho (px):").pack()
        self.libre_width = ttk.Entry(frame)
        self.libre_width.insert(0, "1920")
        self.libre_width.pack(pady=5)
        
        # Alto
        ttk.Label(frame, text="Alto (px):").pack()
        self.libre_height = ttk.Entry(frame)
        self.libre_height.insert(0, "1080")
        self.libre_height.pack(pady=5)
        
        # Formato
        ttk.Label(frame, text="Formato:").pack()
        self.libre_format = ttk.Combobox(frame, values=["JPEG", "PNG", "BMP", "WEBP"], state="readonly")
        self.libre_format.current(0)
        self.libre_format.pack(pady=5)
        
        ttk.Button(frame, text="Generar Imagen", command=self.generate_libre).pack(pady=20)

    def generate_libre(self):
        try:
            w = int(self.libre_width.get())
            h = int(self.libre_height.get())
            fmt = self.libre_format.get()
            
            img = Image.new('RGB', (w, h), color=(73, 109, 137))
            texto = f"Modo Libre\n{w}x{h} - {fmt}"
            self.draw_centered_text(img, texto)
            
            filename = f"salida/libre_{w}x{h}{self.get_extension(fmt)}"
            img.save(filename, format=fmt)
            
            size_mb = os.path.getsize(filename) / (1024 * 1024)
            messagebox.showinfo("Éxito", f"Imagen guardada: {filename}\nPeso real: {size_mb:.2f} MB")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==========================
    # MODO PESO (BMP)
    # ==========================
    def setup_tab_peso(self):
        frame = self.tab_peso
        
        ttk.Label(frame, text="Genera un archivo BMP sin compresión calculando\nla resolución exacta para alcanzar el peso deseado.").pack(pady=10)
        
        # Peso
        ttk.Label(frame, text="Peso Deseado (MB):").pack()
        self.peso_mb = ttk.Entry(frame)
        self.peso_mb.insert(0, "5")
        self.peso_mb.pack(pady=5)
        
        ttk.Button(frame, text="Generar Imagen BMP", command=self.generate_peso).pack(pady=20)

    def generate_peso(self):
        try:
            target_mb = float(self.peso_mb.get())
            target_bytes = target_mb * 1024 * 1024
            
            # En BMP 24-bits, cada pixel son 3 bytes. La cabecera es aprox 54 bytes.
            pixels_needed = (target_bytes - 54) / 3
            if pixels_needed <= 0:
                raise ValueError("El tamaño es demasiado pequeño.")
                
            # Hacerlo un cuadrado
            side = int(math.sqrt(pixels_needed))
            
            img = Image.new('RGB', (side, side), color=(137, 73, 109))
            texto = f"Modo Peso\n~ {target_mb} MB"
            self.draw_centered_text(img, texto)
            
            filename = f"salida/peso_{str(target_mb).replace('.', '_')}MB.bmp"
            img.save(filename, format="BMP")
            
            size_mb = os.path.getsize(filename) / (1024 * 1024)
            messagebox.showinfo("Éxito", f"Imagen guardada: {filename}\nPeso real: {size_mb:.2f} MB")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==========================
    # MODO INFLADOR
    # ==========================
    def setup_tab_inflador(self):
        frame = self.tab_inflador
        
        ttk.Label(frame, text="Genera una imagen normal y luego le inyecta bytes invisibles\npara alcanzar un peso final exacto sin corromperla.").pack(pady=10)
        
        # Resolucion
        ttk.Label(frame, text="Ancho (px):").pack()
        self.infl_width = ttk.Entry(frame)
        self.infl_width.insert(0, "1920")
        self.infl_width.pack(pady=2)
        
        ttk.Label(frame, text="Alto (px):").pack()
        self.infl_height = ttk.Entry(frame)
        self.infl_height.insert(0, "1080")
        self.infl_height.pack(pady=2)
        
        # Formato
        ttk.Label(frame, text="Formato Base:").pack()
        self.infl_format = ttk.Combobox(frame, values=["JPEG", "PNG", "WEBP"], state="readonly")
        self.infl_format.current(0)
        self.infl_format.pack(pady=2)
        
        # Peso final
        ttk.Label(frame, text="Peso Final Deseado (MB):").pack()
        self.infl_mb = ttk.Entry(frame)
        self.infl_mb.insert(0, "15")
        self.infl_mb.pack(pady=2)
        
        ttk.Button(frame, text="Generar e Inflar Imagen", command=self.generate_inflador).pack(pady=15)

    def generate_inflador(self):
        try:
            w = int(self.infl_width.get())
            h = int(self.infl_height.get())
            fmt = self.infl_format.get()
            target_mb = float(self.infl_mb.get())
            target_bytes = int(target_mb * 1024 * 1024)
            
            img = Image.new('RGB', (w, h), color=(73, 137, 109))
            texto = f"Modo Inflador\n{w}x{h}\nTarget: {target_mb} MB"
            self.draw_centered_text(img, texto)
            
            filename = f"salida/inflado_{str(target_mb).replace('.', '_')}MB{self.get_extension(fmt)}"
            img.save(filename, format=fmt)
            
            current_bytes = os.path.getsize(filename)
            
            if current_bytes >= target_bytes:
                messagebox.showwarning("Aviso", "La imagen base ya es más pesada que el objetivo.")
                return
                
            # Inflar el archivo añadiendo ceros al final
            bytes_to_add = target_bytes - current_bytes
            with open(filename, 'ab') as f:
                # Escribimos en bloques para no saturar RAM si es muy grande
                chunk_size = 1024 * 1024 # 1 MB
                while bytes_to_add > 0:
                    write_size = min(chunk_size, bytes_to_add)
                    f.write(b'\0' * write_size)
                    bytes_to_add -= write_size
                    
            size_mb = os.path.getsize(filename) / (1024 * 1024)
            messagebox.showinfo("Éxito", f"Imagen inflada guardada: {filename}\nPeso real exacto: {size_mb:.2f} MB")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageGeneratorApp(root)
    root.mainloop()
