"""
PDF Toolkit - Interfaz Gráfica con tkinter
Sistema completo de manipulación de PDFs con GUI moderna
Requiere: pip install pypdf PyMuPDF pdf2image Pillow reportlab
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
from pathlib import Path
import threading

# Importar módulos personalizados
try:
    from pypdf import PdfMerger, PdfReader, PdfWriter
    import fitz  # PyMuPDF
    from pdf2image import convert_from_path
    from PIL import Image
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
except ImportError as e:
    print(f"Error: {e}")
    print("Instala las dependencias: pip install pypdf PyMuPDF pdf2image Pillow reportlab")


class PDFToolkitGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Toolkit - Manipulación de PDFs")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variables
        self.selected_files = []
        self.current_pdf = None
        
        # Configurar estilo
        self.setup_style()
        
        # Crear interfaz
        self.create_widgets()
        
    def setup_style(self):
        """Configura el estilo visual"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores personalizados
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Helvetica', 10), foreground='#7f8c8d')
        style.configure('Action.TButton', font=('Helvetica', 10, 'bold'), padding=10)
        
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Frame principal con scroll
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="📄 PDF Toolkit", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        subtitle_label = ttk.Label(main_frame, 
                                    text="Herramientas profesionales para manipular archivos PDF",
                                    style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=0, pady=(0, 20))
        
        # Notebook con pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        main_frame.rowconfigure(2, weight=1)
        
        # Crear pestañas
        self.create_merge_tab()
        self.create_split_tab()
        self.create_convert_tab()
        self.create_edit_tab()
        self.create_compress_tab()
        
        # Área de log/consola
        self.create_log_area(main_frame)
        
    def create_merge_tab(self):
        """Pestaña para fusionar PDFs"""
        merge_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(merge_frame, text="📎 Fusionar")
        
        # Instrucciones
        ttk.Label(merge_frame, text="Combina múltiples archivos PDF en uno solo", 
                  font=('Helvetica', 10, 'italic')).grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # Lista de archivos
        ttk.Label(merge_frame, text="Archivos seleccionados:", 
                  font=('Helvetica', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        # Listbox con scrollbar
        list_frame = ttk.Frame(merge_frame)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.merge_listbox = tk.Listbox(list_frame, height=8, yscrollcommand=scrollbar.set,
                                        font=('Courier', 9))
        self.merge_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.merge_listbox.yview)
        
        merge_frame.rowconfigure(2, weight=1)
        merge_frame.columnconfigure(0, weight=1)
        
        # Botones
        button_frame = ttk.Frame(merge_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="➕ Agregar PDFs", 
                   command=self.add_pdfs_to_merge).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔼 Subir", 
                  command=self.move_up_merge).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔽 Bajar", 
                  command=self.move_down_merge).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Quitar", 
                  command=self.remove_from_merge).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Limpiar", 
                  command=self.clear_merge_list).pack(side=tk.LEFT, padx=5)
        
        # Botón de fusionar
        ttk.Button(merge_frame, text="🔗 FUSIONAR PDFs", 
                  command=self.execute_merge, 
                  style='Action.TButton').grid(row=4, column=0, columnspan=3, pady=20)
        
    def create_split_tab(self):
        """Pestaña para dividir PDFs"""
        split_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(split_frame, text="✂️ Dividir")
        
        ttk.Label(split_frame, text="Divide un PDF en múltiples archivos", 
                 font=('Helvetica', 10, 'italic')).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Seleccionar archivo
        ttk.Label(split_frame, text="Archivo PDF:", 
                 font=('Helvetica', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(split_frame)
        file_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.split_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.split_file_var, 
                 width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(file_frame, text="📁 Buscar", 
                  command=self.select_pdf_to_split).pack(side=tk.RIGHT)
        
        split_frame.columnconfigure(0, weight=1)
        
        # Opciones de división
        ttk.Label(split_frame, text="Modo de división:", 
                 font=('Helvetica', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        self.split_mode = tk.StringVar(value="pages")
        modes = [
            ("Por página individual", "pages"),
            ("Por rango de páginas", "range"),
            ("Cada N páginas", "chunks"),
            ("Páginas específicas", "specific")
        ]
        
        for i, (text, value) in enumerate(modes):
            ttk.Radiobutton(split_frame, text=text, variable=self.split_mode, 
                           value=value).grid(row=4+i, column=0, sticky=tk.W, padx=20)
        
        # Parámetros según modo
        param_frame = ttk.LabelFrame(split_frame, text="Parámetros", padding="10")
        param_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        ttk.Label(param_frame, text="Rango (ej: 1-5):").grid(row=0, column=0, sticky=tk.W)
        self.split_range_var = tk.StringVar(value="1-5")
        ttk.Entry(param_frame, textvariable=self.split_range_var, width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(param_frame, text="Páginas por fragmento:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.split_chunk_var = tk.IntVar(value=3)
        ttk.Spinbox(param_frame, from_=1, to=100, textvariable=self.split_chunk_var, 
                   width=13).grid(row=1, column=1, padx=5)
        
        ttk.Label(param_frame, text="Páginas específicas (ej: 1,3,5):").grid(row=2, column=0, sticky=tk.W)
        self.split_specific_var = tk.StringVar(value="1,3,5")
        ttk.Entry(param_frame, textvariable=self.split_specific_var, width=15).grid(row=2, column=1, padx=5)
        
        # Botón ejecutar
        ttk.Button(split_frame, text="✂️ DIVIDIR PDF", 
                  command=self.execute_split,
                  style='Action.TButton').grid(row=9, column=0, columnspan=2, pady=20)
        
    def create_convert_tab(self):
        """Pestaña para convertir PDFs"""
        convert_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(convert_frame, text="🔄 Convertir")
        
        ttk.Label(convert_frame, text="Convierte PDFs a otros formatos y viceversa", 
                 font=('Helvetica', 10, 'italic')).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Modo de conversión
        ttk.Label(convert_frame, text="Tipo de conversión:", 
                 font=('Helvetica', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.convert_mode = tk.StringVar(value="pdf_to_images")
        conversions = [
            ("PDF → Imágenes", "pdf_to_images"),
            ("Imágenes → PDF", "images_to_pdf"),
            ("PDF → Texto", "pdf_to_text"),
            ("Texto → PDF", "text_to_pdf")
        ]
        
        for i, (text, value) in enumerate(conversions):
            ttk.Radiobutton(convert_frame, text=text, variable=self.convert_mode, 
                           value=value, command=self.update_convert_ui).grid(
                               row=2+i, column=0, sticky=tk.W, padx=20, pady=2)
        
        # Frame para parámetros
        self.convert_param_frame = ttk.LabelFrame(convert_frame, text="Parámetros", padding="10")
        self.convert_param_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        convert_frame.columnconfigure(0, weight=1)
        
        # Archivo de entrada
        ttk.Label(self.convert_param_frame, text="Archivo de entrada:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        input_frame = ttk.Frame(self.convert_param_frame)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.convert_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.convert_input_var, 
                 width=40).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(input_frame, text="📁", 
                  command=self.select_convert_input).pack(side=tk.RIGHT)
        
        self.convert_param_frame.columnconfigure(0, weight=1)
        
        # Formato de imagen
        ttk.Label(self.convert_param_frame, text="Formato de imagen:").grid(row=2, column=0, sticky=tk.W)
        self.image_format_var = tk.StringVar(value="PNG")
        ttk.Combobox(self.convert_param_frame, textvariable=self.image_format_var, 
                    values=["PNG", "JPEG", "BMP", "TIFF"], width=10, 
                    state='readonly').grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # DPI
        ttk.Label(self.convert_param_frame, text="DPI (calidad):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.dpi_var = tk.IntVar(value=200)
        ttk.Spinbox(self.convert_param_frame, from_=72, to=600, increment=50,
                   textvariable=self.dpi_var, width=8).grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # Botón ejecutar
        ttk.Button(convert_frame, text="🔄 CONVERTIR", 
                  command=self.execute_convert,
                  style='Action.TButton').grid(row=7, column=0, columnspan=2, pady=20)
        
    def create_edit_tab(self):
        """Pestaña para editar PDFs"""
        edit_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(edit_frame, text="✏️ Editar")
        
        ttk.Label(edit_frame, text="Añade marcas de agua, texto e imágenes a tus PDFs", 
                 font=('Helvetica', 10, 'italic')).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Archivo PDF
        ttk.Label(edit_frame, text="Archivo PDF:", 
                 font=('Helvetica', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(edit_frame)
        file_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.edit_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.edit_file_var, 
                 width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(file_frame, text="📁 Buscar", 
                  command=self.select_pdf_to_edit).pack(side=tk.RIGHT)
        
        edit_frame.columnconfigure(0, weight=1)
        
        # Operación
        ttk.Label(edit_frame, text="Operación:", 
                 font=('Helvetica', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.edit_operation = tk.StringVar(value="watermark")
        operations = [
            ("Agregar marca de agua", "watermark"),
            ("Agregar texto", "text"),
            ("Rotar páginas", "rotate"),
            ("Proteger con contraseña", "protect")
        ]
        
        for i, (text, value) in enumerate(operations):
            ttk.Radiobutton(edit_frame, text=text, variable=self.edit_operation, 
                           value=value).grid(row=4+i, column=0, sticky=tk.W, padx=20)
        
        # Parámetros
        param_frame = ttk.LabelFrame(edit_frame, text="Parámetros", padding="10")
        param_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=15)
        
        ttk.Label(param_frame, text="Texto/Marca de agua:").grid(row=0, column=0, sticky=tk.W)
        self.watermark_text_var = tk.StringVar(value="CONFIDENCIAL")
        ttk.Entry(param_frame, textvariable=self.watermark_text_var, width=20).grid(row=0, column=1, padx=5)
        
        ttk.Label(param_frame, text="Opacidad (0.0-1.0):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.opacity_var = tk.DoubleVar(value=0.3)
        ttk.Scale(param_frame, from_=0.0, to=1.0, variable=self.opacity_var, 
                 orient=tk.HORIZONTAL, length=150).grid(row=1, column=1, padx=5)
        
        ttk.Label(param_frame, text="Rotación (grados):").grid(row=2, column=0, sticky=tk.W)
        self.rotation_var = tk.IntVar(value=90)
        ttk.Combobox(param_frame, textvariable=self.rotation_var, 
                    values=[90, 180, 270], width=8, state='readonly').grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(param_frame, text="Contraseña:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(param_frame, textvariable=self.password_var, show="*", width=20).grid(row=3, column=1, padx=5)
        
        # Botón ejecutar
        ttk.Button(edit_frame, text="✏️ APLICAR EDICIÓN", 
                  command=self.execute_edit,
                  style='Action.TButton').grid(row=9, column=0, columnspan=2, pady=20)
        
    def create_compress_tab(self):
        """Pestaña para comprimir PDFs"""
        compress_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(compress_frame, text="📦 Comprimir")
        
        ttk.Label(compress_frame, text="Reduce el tamaño de tus archivos PDF", 
                 font=('Helvetica', 10, 'italic')).grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # Archivo
        ttk.Label(compress_frame, text="Archivo PDF:", 
                 font=('Helvetica', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(compress_frame)
        file_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.compress_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.compress_file_var, 
                 width=50).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(file_frame, text="📁 Buscar", 
                  command=self.select_pdf_to_compress).pack(side=tk.RIGHT)
        
        compress_frame.columnconfigure(0, weight=1)
        
        # Nivel de compresión
        ttk.Label(compress_frame, text="Nivel de compresión:", 
                 font=('Helvetica', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=15)
        
        self.compression_level = tk.IntVar(value=1)
        levels = [
            ("Baja compresión (mejor calidad)", 2),
            ("Compresión media (equilibrado)", 1),
            ("Alta compresión (menor tamaño)", 0)
        ]
        
        for i, (text, value) in enumerate(levels):
            ttk.Radiobutton(compress_frame, text=text, variable=self.compression_level, 
                           value=value).grid(row=4+i, column=0, sticky=tk.W, padx=20, pady=2)
        
        # Info
        info_text = "💡 La compresión puede tomar tiempo en archivos grandes"
        ttk.Label(compress_frame, text=info_text, 
                 font=('Helvetica', 9, 'italic'), foreground='#7f8c8d').grid(
                     row=7, column=0, columnspan=2, pady=15)
        
        # Botón ejecutar
        ttk.Button(compress_frame, text="📦 COMPRIMIR PDF", 
                  command=self.execute_compress,
                  style='Action.TButton').grid(row=8, column=0, columnspan=2, pady=20)
        
    def create_log_area(self, parent):
        """Crea el área de log/consola"""
        log_frame = ttk.LabelFrame(parent, text="📋 Registro de operaciones", padding="10")
        log_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        parent.rowconfigure(3, weight=0, minsize=150)
        
        # Text widget con scroll
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, 
                                                  font=('Courier', 9), 
                                                  wrap=tk.WORD, 
                                                  state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Botón limpiar log
        ttk.Button(log_frame, text="🗑️ Limpiar log", 
                  command=self.clear_log).pack(pady=(5, 0))
        
    # ==================== FUNCIONES DE UTILIDAD ====================
    
    def log(self, message):
        """Añade un mensaje al log"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()
        
    def clear_log(self):
        """Limpia el log"""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
    def run_in_thread(self, func):
        """Ejecuta una función en un hilo separado"""
        thread = threading.Thread(target=func, daemon=True)
        thread.start()
        
    # ==================== FUNCIONES DE FUSIONAR ====================
    
    def add_pdfs_to_merge(self):
        """Agrega PDFs a la lista para fusionar"""
        files = filedialog.askopenfilenames(
            title="Selecciona archivos PDF",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
                self.merge_listbox.insert(tk.END, os.path.basename(file))
                self.log(f"✅ Agregado: {os.path.basename(file)}")
                
    def move_up_merge(self):
        """Mueve un archivo hacia arriba en la lista"""
        try:
            index = self.merge_listbox.curselection()[0]
            if index > 0:
                # Intercambiar en lista
                self.selected_files[index], self.selected_files[index-1] = \
                    self.selected_files[index-1], self.selected_files[index]
                
                # Actualizar listbox
                item = self.merge_listbox.get(index)
                self.merge_listbox.delete(index)
                self.merge_listbox.insert(index-1, item)
                self.merge_listbox.selection_set(index-1)
        except:
            messagebox.showwarning("Aviso", "Selecciona un archivo de la lista")
            
    def move_down_merge(self):
        """Mueve un archivo hacia abajo en la lista"""
        try:
            index = self.merge_listbox.curselection()[0]
            if index < len(self.selected_files) - 1:
                # Intercambiar en lista
                self.selected_files[index], self.selected_files[index+1] = \
                    self.selected_files[index+1], self.selected_files[index]
                
                # Actualizar listbox
                item = self.merge_listbox.get(index)
                self.merge_listbox.delete(index)
                self.merge_listbox.insert(index+1, item)
                self.merge_listbox.selection_set(index+1)
        except:
            messagebox.showwarning("Aviso", "Selecciona un archivo de la lista")
            
    def remove_from_merge(self):
        """Elimina un archivo de la lista"""
        try:
            index = self.merge_listbox.curselection()[0]
            removed = self.selected_files.pop(index)
            self.merge_listbox.delete(index)
            self.log(f"❌ Eliminado: {os.path.basename(removed)}")
        except:
            messagebox.showwarning("Aviso", "Selecciona un archivo de la lista")
            
    def clear_merge_list(self):
        """Limpia toda la lista"""
        self.selected_files.clear()
        self.merge_listbox.delete(0, tk.END)
        self.log("🗑️ Lista limpiada")
        
    def execute_merge(self):
        """Ejecuta la fusión de PDFs"""
        if len(self.selected_files) < 2:
            messagebox.showwarning("Aviso", "Debes seleccionar al menos 2 archivos PDF")
            return
            
        output_file = filedialog.asksaveasfilename(
            title="Guardar PDF fusionado",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if not output_file:
            return
            
        def merge():
            try:
                self.log("🔗 Iniciando fusión de PDFs...")
                merger = PdfMerger()
                
                for pdf_file in self.selected_files:
                    self.log(f"📄 Procesando: {os.path.basename(pdf_file)}")
                    merger.append(pdf_file)
                
                merger.write(output_file)
                merger.close()
                
                self.log(f"✅ ¡PDFs fusionados exitosamente!")
                self.log(f"💾 Guardado en: {output_file}")
                messagebox.showinfo("Éxito", "PDFs fusionados correctamente")
                
            except Exception as e:
                self.log(f"❌ Error: {str(e)}")
                messagebox.showerror("Error", f"Error al fusionar: {str(e)}")
                
        self.run_in_thread(merge)
        
    # ==================== FUNCIONES DE DIVIDIR ====================
    
    def select_pdf_to_split(self):
        """Selecciona PDF para dividir"""
        file = filedialog.askopenfilename(
            title="Selecciona un PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if file:
            self.split_file_var.set(file)
            
    def execute_split(self):
        """Ejecuta la división del PDF"""
        pdf_path = self.split_file_var.get()
        
        if not pdf_path or not os.path.exists(pdf_path):
            messagebox.showwarning("Aviso", "Selecciona un archivo PDF válido")
            return
            
        output_folder = filedialog.askdirectory(title="Selecciona carpeta de salida")
        if not output_folder:
            return
            
        mode = self.split_mode.get()
        
        def split():
            try:
                self.log(f"✂️ Dividiendo PDF: {os.path.basename(pdf_path)}")
                reader = PdfReader(pdf_path)
                total_pages = len(reader.pages)
                
                if mode == "pages":
                    # Dividir en páginas individuales
                    for i in range(total_pages):
                        writer = PdfWriter()
                        writer.add_page(reader.pages[i])
                        output_path = os.path.join(output_folder, f"pagina_{i+1}.pdf")
                        with open(output_path, "wb") as f:
                            writer.write(f)
                        self.log(f"✅ Página {i+1} guardada")
                        
                elif mode == "chunks":
                    # Dividir en fragmentos
                    chunk_size = self.split_chunk_var.get()
                    chunk_num = 1
                    
                    for i in range(0, total_pages, chunk_size):
                        writer = PdfWriter()
                        for j in range(i, min(i + chunk_size, total_pages)):
                            writer.add_page(reader.pages[j])
                        
                        output_path = os.path.join(output_folder, f"fragmento_{chunk_num}.pdf")
                        with open(output_path, "wb") as f:
                            writer.write(f)
                        self.log(f"✅ Fragmento {chunk_num} guardado (páginas {i+1}-{min(i+chunk_size, total_pages)})")
                        chunk_num += 1
                        
                elif mode == "range":
                    # Dividir por rango
                    range_str = self.split_range_var.get()
                    start, end = map(int, range_str.split('-'))
                    
                    writer = PdfWriter()
                    for i in range(start-1, min(end, total_pages)):
                        writer.add_page(reader.pages[i])
                    
                    output_path = os.path.join(output_folder, f"paginas_{start}-{end}.pdf")
                    with open(output_path, "wb") as f:
                        writer.write(f)
                    self.log(f"✅ Rango {start}-{end} guardado")
                    
                elif mode == "specific":
                    # Páginas específicas
                    pages_str = self.split_specific_var.get()
                    pages = [int(p.strip()) for p in pages_str.split(',')]
                    
                    writer = PdfWriter()
                    for page_num in pages:
                        if 1 <= page_num <= total_pages:
                            writer.add_page(reader.pages[page_num-1])
                            self.log(f"📄 Página {page_num} agregada")
                    
                    output_path = os.path.join(output_folder, "paginas_especificas.pdf")
                    with open(output_path, "wb") as f:
                        writer.write(f)
                    self.log(f"✅ Páginas específicas guardadas")
                
                self.log(f"🎉 División completada en: {output_folder}")
                messagebox.showinfo("Éxito", "PDF dividido correctamente")
                
            except Exception as e:
                self.log(f"❌ Error: {str(e)}")
                messagebox.showerror("Error", f"Error al dividir: {str(e)}")
                
        self.run_in_thread(split)
        
    # ==================== FUNCIONES DE CONVERTIR ====================
    
    def select_convert_input(self):
        """Selecciona archivo de entrada para conversión"""
        mode = self.convert_mode.get()
        
        if mode in ["pdf_to_images", "pdf_to_text"]:
            file = filedialog.askopenfilename(
                title="Selecciona un PDF",
                filetypes=[("PDF files", "*.pdf")]
            )
        elif mode == "images_to_pdf":
            file = filedialog.askopenfilenames(
                title="Selecciona imágenes",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
            )
            if file:
                file = ";".join(file)  # Unir múltiples archivos
        else:  # text_to_pdf
            file = filedialog.askopenfilename(
                title="Selecciona archivo de texto",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
        if file:
            self.convert_input_var.set(file)
            
    def update_convert_ui(self):
        """Actualiza la UI según el modo de conversión seleccionado"""
        # Esta función se puede expandir para mostrar/ocultar widgets
        pass
        
    def execute_convert(self):
        """Ejecuta la conversión"""
        input_file = self.convert_input_var.get()
        
        if not input_file:
            messagebox.showwarning("Aviso", "Selecciona un archivo de entrada")
            return
            
        mode = self.convert_mode.get()
        
        def convert():
            try:
                if mode == "pdf_to_images":
                    # PDF a imágenes
                    output_folder = filedialog.askdirectory(title="Carpeta de salida")
                    if not output_folder:
                        return
                        
                    self.log("🔄 Convirtiendo PDF a imágenes...")
                    os.makedirs(output_folder, exist_ok=True)
                    
                    format_type = self.image_format_var.get()
                    dpi = self.dpi_var.get()
                    
                    images = convert_from_path(input_file, dpi=dpi)
                    
                    for i, image in enumerate(images, 1):
                        output_path = os.path.join(output_folder, f"pagina_{i}.{format_type.lower()}")
                        image.save(output_path, format_type)
                        self.log(f"✅ Página {i} convertida a {format_type}")
                    
                    self.log(f"🎉 {len(images)} imágenes guardadas en: {output_folder}")
                    messagebox.showinfo("Éxito", f"PDF convertido a {len(images)} imágenes")
                    
                elif mode == "images_to_pdf":
                    # Imágenes a PDF
                    output_file = filedialog.asksaveasfilename(
                        title="Guardar PDF",
                        defaultextension=".pdf",
                        filetypes=[("PDF files", "*.pdf")]
                    )
                    if not output_file:
                        return
                        
                    self.log("🔄 Convirtiendo imágenes a PDF...")
                    image_paths = input_file.split(';')
                    images = []
                    
                    for img_path in image_paths:
                        img = Image.open(img_path)
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        images.append(img)
                        self.log(f"📷 Imagen cargada: {os.path.basename(img_path)}")
                    
                    images[0].save(output_file, save_all=True, append_images=images[1:])
                    self.log(f"✅ PDF creado: {output_file}")
                    messagebox.showinfo("Éxito", "Imágenes convertidas a PDF")
                    
                elif mode == "pdf_to_text":
                    # PDF a texto
                    output_file = filedialog.asksaveasfilename(
                        title="Guardar texto",
                        defaultextension=".txt",
                        filetypes=[("Text files", "*.txt")]
                    )
                    if not output_file:
                        return
                        
                    self.log("🔄 Extrayendo texto del PDF...")
                    doc = fitz.open(input_file)
                    full_text = []
                    
                    for page_num in range(len(doc)):
                        page = doc[page_num]
                        text = page.get_text()
                        full_text.append(f"--- Página {page_num + 1} ---\n{text}\n")
                        self.log(f"📄 Página {page_num + 1} procesada")
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(full_text))
                    
                    doc.close()
                    self.log(f"✅ Texto extraído: {output_file}")
                    messagebox.showinfo("Éxito", "Texto extraído del PDF")
                    
                elif mode == "text_to_pdf":
                    # Texto a PDF
                    output_file = filedialog.asksaveasfilename(
                        title="Guardar PDF",
                        defaultextension=".pdf",
                        filetypes=[("PDF files", "*.pdf")]
                    )
                    if not output_file:
                        return
                        
                    self.log("🔄 Creando PDF desde texto...")
                    
                    with open(input_file, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                    
                    c = canvas.Canvas(output_file, pagesize=letter)
                    width, height = letter
                    c.setFont("Helvetica", 12)
                    y_position = height - 50
                    line_height = 15
                    
                    for line in text_content.split('\n'):
                        if y_position < 50:
                            c.showPage()
                            c.setFont("Helvetica", 12)
                            y_position = height - 50
                        
                        c.drawString(50, y_position, line[:90])
                        y_position -= line_height
                    
                    c.save()
                    self.log(f"✅ PDF creado: {output_file}")
                    messagebox.showinfo("Éxito", "PDF creado desde texto")
                
            except Exception as e:
                self.log(f"❌ Error: {str(e)}")
                messagebox.showerror("Error", f"Error al convertir: {str(e)}")
                
        self.run_in_thread(convert)
        
    # ==================== FUNCIONES DE EDITAR ====================
    
    def select_pdf_to_edit(self):
        """Selecciona PDF para editar"""
        file = filedialog.askopenfilename(
            title="Selecciona un PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if file:
            self.edit_file_var.set(file)
            
    def execute_edit(self):
        """Ejecuta la edición del PDF"""
        pdf_path = self.edit_file_var.get()
        
        if not pdf_path or not os.path.exists(pdf_path):
            messagebox.showwarning("Aviso", "Selecciona un archivo PDF válido")
            return
            
        output_file = filedialog.asksaveasfilename(
            title="Guardar PDF editado",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if not output_file:
            return
            
        operation = self.edit_operation.get()
        
        def edit():
            try:
                doc = fitz.open(pdf_path)
                
                if operation == "watermark":
                    # Agregar marca de agua
                    watermark_text = self.watermark_text_var.get()
                    opacity = self.opacity_var.get()
                    
                    self.log(f"💧 Agregando marca de agua: {watermark_text}")
                    
                    for page_num in range(len(doc)):
                        page = doc[page_num]
                        rect = page.rect
                        text_point = fitz.Point(rect.width / 2, rect.height / 2)
                        
                        page.insert_text(
                            text_point,
                            watermark_text,
                            fontsize=60,
                            rotate=45,
                            color=(0.7, 0.7, 0.7),
                            opacity=opacity,
                            overlay=True
                        )
                        self.log(f"✅ Marca agregada a página {page_num + 1}")
                    
                elif operation == "text":
                    # Agregar texto
                    text = self.watermark_text_var.get()
                    self.log(f"✏️ Agregando texto: {text}")
                    
                    page = doc[0]  # Primera página
                    page.insert_text((100, 100), text, fontsize=12, color=(0, 0, 0))
                    self.log("✅ Texto agregado")
                    
                elif operation == "rotate":
                    # Rotar páginas
                    rotation = self.rotation_var.get()
                    self.log(f"🔄 Rotando páginas {rotation}°")
                    
                    for page in doc:
                        page.set_rotation(rotation)
                    self.log("✅ Páginas rotadas")
                    
                elif operation == "protect":
                    # Proteger con contraseña
                    password = self.password_var.get()
                    
                    if not password:
                        messagebox.showwarning("Aviso", "Ingresa una contraseña")
                        return
                    
                    self.log("🔒 Protegiendo PDF con contraseña...")
                    
                    perm = int(
                        fitz.PDF_PERM_ACCESSIBILITY |
                        fitz.PDF_PERM_PRINT |
                        fitz.PDF_PERM_COPY
                    )
                    
                    doc.save(
                        output_file,
                        encryption=fitz.PDF_ENCRYPT_AES_256,
                        user_pw=password,
                        owner_pw=password,
                        permissions=perm
                    )
                    doc.close()
                    self.log(f"✅ PDF protegido guardado: {output_file}")
                    messagebox.showinfo("Éxito", "PDF protegido con contraseña")
                    return
                
                doc.save(output_file)
                doc.close()
                
                self.log(f"✅ PDF editado guardado: {output_file}")
                messagebox.showinfo("Éxito", "PDF editado correctamente")
                
            except Exception as e:
                self.log(f"❌ Error: {str(e)}")
                messagebox.showerror("Error", f"Error al editar: {str(e)}")
                
        self.run_in_thread(edit)
        
    # ==================== FUNCIONES DE COMPRIMIR ====================
    
    def select_pdf_to_compress(self):
        """Selecciona PDF para comprimir"""
        file = filedialog.askopenfilename(
            title="Selecciona un PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if file:
            self.compress_file_var.set(file)
            
    def execute_compress(self):
        """Ejecuta la compresión del PDF"""
        pdf_path = self.compress_file_var.get()
        
        if not pdf_path or not os.path.exists(pdf_path):
            messagebox.showwarning("Aviso", "Selecciona un archivo PDF válido")
            return
            
        output_file = filedialog.asksaveasfilename(
            title="Guardar PDF comprimido",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if not output_file:
            return
            
        def compress():
            try:
                self.log("📦 Comprimiendo PDF...")
                
                doc = fitz.open(pdf_path)
                
                doc.save(
                    output_file,
                    garbage=4,
                    deflate=True,
                    clean=True
                )
                doc.close()
                
                # Calcular reducción
                original_size = os.path.getsize(pdf_path)
                compressed_size = os.path.getsize(output_file)
                reduction = (1 - compressed_size/original_size) * 100
                
                self.log(f"✅ PDF comprimido guardado: {output_file}")
                self.log(f"📉 Reducción: {reduction:.1f}%")
                self.log(f"   Original: {original_size/1024:.1f} KB")
                self.log(f"   Comprimido: {compressed_size/1024:.1f} KB")
                
                messagebox.showinfo("Éxito", 
                    f"PDF comprimido correctamente\n"
                    f"Reducción: {reduction:.1f}%\n"
                    f"Original: {original_size/1024:.1f} KB\n"
                    f"Comprimido: {compressed_size/1024:.1f} KB")
                
            except Exception as e:
                self.log(f"❌ Error: {str(e)}")
                messagebox.showerror("Error", f"Error al comprimir: {str(e)}")
                
        self.run_in_thread(compress)


# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    """Función principal para iniciar la aplicación"""
    root = tk.Tk()
    app = PDFToolkitGUI(root)
    
    # Centrar ventana
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()