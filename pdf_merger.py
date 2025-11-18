"""
Módulo para fusionar múltiples archivos PDF en uno solo
"""
from pypdf import PdfMerger, PdfReader
import os

class PDFMerger:
    def __init__(self):
        self.merger = PdfMerger()
    
    def merge_pdfs(self, pdf_list, output_path):
        """
        Fusiona múltiples PDFs en uno solo
        
        Args:
            pdf_list (list): Lista de rutas de archivos PDF a fusionar
            output_path (str): Ruta del archivo de salida
            
        Returns:
            bool: True si fue exitoso, False en caso contrario
        """
        try:
            for pdf_file in pdf_list:
                if not os.path.exists(pdf_file):
                    print(f"⚠️  Archivo no encontrado: {pdf_file}")
                    continue
                    
                print(f"📄 Agregando: {pdf_file}")
                self.merger.append(pdf_file)
            
            # Guardar el PDF fusionado
            self.merger.write(output_path)
            self.merger.close()
            
            print(f"✅ PDF fusionado guardado en: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error al fusionar PDFs: {str(e)}")
            return False
    
    def merge_specific_pages(self, pdf_files_with_pages, output_path):
        """
        Fusiona páginas específicas de múltiples PDFs
        
        Args:
            pdf_files_with_pages (list): Lista de tuplas (archivo, inicio, fin)
                Ejemplo: [("doc1.pdf", 0, 2), ("doc2.pdf", 1, 3)]
            output_path (str): Ruta del archivo de salida
        """
        try:
            for pdf_file, start_page, end_page in pdf_files_with_pages:
                print(f"📄 Agregando páginas {start_page}-{end_page} de {pdf_file}")
                self.merger.append(pdf_file, pages=(start_page, end_page))
            
            self.merger.write(output_path)
            self.merger.close()
            
            print(f"✅ PDF con páginas específicas guardado en: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False


# Ejemplo de uso
if __name__ == "__main__":
    merger = PDFMerger()
    
    # Ejemplo 1: Fusionar PDFs completos
    pdfs_to_merge = ["documento1.pdf", "documento2.pdf", "documento3.pdf"]
    merger.merge_pdfs(pdfs_to_merge, "resultado_fusionado.pdf")
    
    # Ejemplo 2: Fusionar páginas específicas
    # merger_specific = PDFMerger()
    # pages_config = [
    #     ("doc1.pdf", 0, 2),  # Páginas 0-1 del doc1
    #     ("doc2.pdf", 1, 4)   # Páginas 1-3 del doc2
    # ]
    # merger_specific.merge_specific_pages(pages_config, "paginas_especificas.pdf")