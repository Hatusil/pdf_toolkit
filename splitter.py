"""
Módulo para dividir archivos PDF de diferentes maneras
"""
from pypdf import PdfReader, PdfWriter
import os

class PDFSplitter:
    def __init__(self, pdf_path):
        """
        Inicializa el divisor con un archivo PDF
        
        Args:
            pdf_path (str): Ruta del archivo PDF a dividir
        """
        self.pdf_path = pdf_path
        self.reader = PdfReader(pdf_path)
        self.total_pages = len(self.reader.pages)
        print(f"📖 PDF cargado: {pdf_path} ({self.total_pages} páginas)")
    
    def split_by_page(self, output_folder="split_output"):
        """
        Divide el PDF en archivos individuales (una página por archivo)
        
        Args:
            output_folder (str): Carpeta donde guardar los archivos
        """
        try:
            os.makedirs(output_folder, exist_ok=True)
            
            for page_num in range(self.total_pages):
                writer = PdfWriter()
                writer.add_page(self.reader.pages[page_num])
                
                output_filename = f"{output_folder}/pagina_{page_num + 1}.pdf"
                with open(output_filename, "wb") as output_file:
                    writer.write(output_file)
                
                print(f"✅ Página {page_num + 1} guardada")
            
            print(f"🎉 Todas las páginas divididas en: {output_folder}")
            return True
            
        except Exception as e:
            print(f"❌ Error al dividir: {str(e)}")
            return False
    
    def split_by_range(self, ranges, output_folder="split_ranges"):
        """
        Divide el PDF según rangos específicos
        
        Args:
            ranges (list): Lista de tuplas (inicio, fin, nombre)
                Ejemplo: [(0, 3, "introduccion"), (3, 10, "capitulo1")]
            output_folder (str): Carpeta de salida
        """
        try:
            os.makedirs(output_folder, exist_ok=True)
            
            for start, end, name in ranges:
                writer = PdfWriter()
                
                # Agregar páginas del rango
                for page_num in range(start, min(end, self.total_pages)):
                    writer.add_page(self.reader.pages[page_num])
                
                output_filename = f"{output_folder}/{name}.pdf"
                with open(output_filename, "wb") as output_file:
                    writer.write(output_file)
                
                print(f"✅ Rango {start}-{end} guardado como: {name}.pdf")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def split_by_chunks(self, pages_per_chunk, output_folder="split_chunks"):
        """
        Divide el PDF en fragmentos de N páginas
        
        Args:
            pages_per_chunk (int): Número de páginas por fragmento
            output_folder (str): Carpeta de salida
        """
        try:
            os.makedirs(output_folder, exist_ok=True)
            
            chunk_num = 1
            for i in range(0, self.total_pages, pages_per_chunk):
                writer = PdfWriter()
                
                # Agregar páginas del fragmento actual
                for page_num in range(i, min(i + pages_per_chunk, self.total_pages)):
                    writer.add_page(self.reader.pages[page_num])
                
                output_filename = f"{output_folder}/fragmento_{chunk_num}.pdf"
                with open(output_filename, "wb") as output_file:
                    writer.write(output_file)
                
                print(f"✅ Fragmento {chunk_num} guardado ({i+1}-{min(i+pages_per_chunk, self.total_pages)})")
                chunk_num += 1
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def extract_pages(self, page_numbers, output_path):
        """
        Extrae páginas específicas a un nuevo PDF
        
        Args:
            page_numbers (list): Lista de números de página (empezando en 1)
            output_path (str): Ruta del archivo de salida
        """
        try:
            writer = PdfWriter()
            
            for page_num in page_numbers:
                if 1 <= page_num <= self.total_pages:
                    writer.add_page(self.reader.pages[page_num - 1])
                    print(f"📄 Página {page_num} agregada")
                else:
                    print(f"⚠️  Página {page_num} fuera de rango")
            
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            
            print(f"✅ Páginas extraídas guardadas en: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False


# Ejemplo de uso
if __name__ == "__main__":
    splitter = PDFSplitter("documento_grande.pdf")
    
    # Opción 1: Dividir en páginas individuales
    # splitter.split_by_page("paginas_individuales")
    
    # Opción 2: Dividir por rangos personalizados
    rangos = [
        (0, 5, "introduccion"),
        (5, 15, "desarrollo"),
        (15, 20, "conclusion")
    ]
    # splitter.split_by_range(rangos, "secciones")
    
    # Opción 3: Dividir en fragmentos de 3 páginas
    splitter.split_by_chunks(3, "fragmentos")
    
    # Opción 4: Extraer páginas específicas
    # splitter.extract_pages([1, 3, 5, 7], "paginas_impares.pdf")