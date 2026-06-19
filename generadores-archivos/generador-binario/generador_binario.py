import tkinter as tk
from tkinter import ttk, messagebox
import os
import time

class BinaryGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Archivos Binarios")
        self.root.geometry("450x380")
        self.root.resizable(False, False)

        os.makedirs("salida", exist_ok=True)

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Generador de Datos Crudos", font=("Helvetica", 14, "bold")).pack(pady=(0, 15))

        # Tamaño
        size_frame = ttk.Frame(main_frame)
        size_frame.pack(fill="x", pady=5)
        ttk.Label(size_frame, text="Tamaño Objetivo:").pack(side="left")
        
        self.size_var = tk.StringVar(value="10")
        ttk.Entry(size_frame, textvariable=self.size_var, width=15).pack(side="left", padx=10)
        
        self.unit_var = tk.StringVar(value="MB")
        ttk.Combobox(size_frame, textvariable=self.unit_var, values=["KB", "MB", "GB"], state="readonly", width=5).pack(side="left")

        # Tipo de Contenido
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="x", pady=15)
        ttk.Label(content_frame, text="Tipo de Contenido:").pack(anchor="w")
        
        self.content_var = tk.StringVar(value="Ceros (\\0)")
        content_cb = ttk.Combobox(content_frame, textvariable=self.content_var, 
                                  values=["Ceros (\\0)", "Aleatorio (urandom)", "Patrón Repetitivo"], 
                                  state="readonly", width=25)
        content_cb.pack(anchor="w", pady=5)
        content_cb.bind("<<ComboboxSelected>>", self.on_content_change)

        # Etiqueta de ayuda (Hint) dinámica
        self.hint_var = tk.StringVar()
        self.hint_label = ttk.Label(content_frame, textvariable=self.hint_var, foreground="gray", wraplength=410, justify="left")
        self.hint_label.pack(anchor="w", pady=(2, 5))

        # Entrada para Patrón (Oculto por defecto)
        self.pattern_frame = ttk.Frame(main_frame)
        ttk.Label(self.pattern_frame, text="Palabra / Patrón:").pack(side="left")
        self.pattern_var = tk.StringVar(value="TEST")
        ttk.Entry(self.pattern_frame, textvariable=self.pattern_var, width=15).pack(side="left", padx=10)

        # Extensión
        ext_frame = ttk.Frame(main_frame)
        ext_frame.pack(fill="x", pady=5)
        ttk.Label(ext_frame, text="Extensión de archivo:").pack(side="left")
        self.ext_var = tk.StringVar(value=".bin")
        ttk.Entry(ext_frame, textvariable=self.ext_var, width=10).pack(side="left", padx=10)

        # Botón Generar
        ttk.Button(main_frame, text="Generar Archivo", command=self.generate_file).pack(pady=25)

        # Inicializar la etiqueta de ayuda
        self.update_hint()

    def update_hint(self):
        modo = self.content_var.get()
        if modo == "Ceros (\\0)":
            self.hint_var.set("Útil para máxima velocidad. Ojo: los sistemas modernos pueden comprimir este archivo casi a 0 bytes durante una transferencia de red.")
        elif modo == "Aleatorio (urandom)":
            self.hint_var.set("Ruido criptográficamente seguro. Es imposible de comprimir, ideal para probar velocidad real (throughput) en redes y discos.")
        elif modo == "Patrón Repetitivo":
            self.hint_var.set("Escribe una palabra y se repetirá infinitamente hasta llenar el archivo. Útil para depurar y verificar con un editor hexadecimal.")

    def on_content_change(self, event):
        self.update_hint()
        if self.content_var.get() == "Patrón Repetitivo":
            self.pattern_frame.pack(fill="x", pady=5, after=event.widget.master)
        else:
            self.pattern_frame.pack_forget()

    def generate_file(self):
        try:
            size_val = float(self.size_var.get())
            unit = self.unit_var.get()
            
            multiplier = {"KB": 1024, "MB": 1024**2, "GB": 1024**3}
            target_bytes = int(size_val * multiplier[unit])
            
            if target_bytes <= 0:
                raise ValueError("El tamaño debe ser mayor a 0.")

            content_type = self.content_var.get()
            ext = self.ext_var.get()
            if not ext.startswith("."):
                ext = "." + ext

            filename = f"salida/archivo_{content_type.split()[0].lower()}_{str(size_val).replace('.', '_')}{unit}{ext}"
            
            # Tamaño del bloque para escribir en memoria (1 MB)
            chunk_size = 1024 * 1024
            bytes_written = 0
            
            start_time = time.time()
            
            with open(filename, 'wb') as f:
                while bytes_written < target_bytes:
                    write_size = min(chunk_size, target_bytes - bytes_written)
                    
                    if content_type == "Ceros (\\0)":
                        chunk = b'\0' * write_size
                    elif content_type == "Aleatorio (urandom)":
                        chunk = os.urandom(write_size)
                    elif content_type == "Patrón Repetitivo":
                        pattern = self.pattern_var.get().encode('utf-8')
                        if not pattern:
                            raise ValueError("El patrón no puede estar vacío.")
                        # Rellenar el chunk con el patrón repetido
                        repeats = (write_size // len(pattern)) + 1
                        chunk = (pattern * repeats)[:write_size]
                    
                    f.write(chunk)
                    bytes_written += write_size
            
            elapsed = time.time() - start_time
            actual_size = os.path.getsize(filename) / (1024 * 1024)
            
            messagebox.showinfo("Completado", 
                                f"Archivo generado exitosamente.\n\n"
                                f"Ubicación: {filename}\n"
                                f"Peso final: {actual_size:.2f} MB\n"
                                f"Tiempo: {elapsed:.2f} segundos")

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryGeneratorApp(root)
    root.mainloop()
