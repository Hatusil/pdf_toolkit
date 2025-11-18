"""
Módulo para convertir PDFs a diferentes formatos y viceversa
Requiere: pip install pdf2image Pillow PyMuPDF reportlab
En Windows también necesitas: poppler (descarga y añade al PATH)
"""
from pdf2image import convert_from_path
from PIL import Image
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

class PDFConverter:
    def __init__(self):
        self.supported_image_formats = ['PNG', 'JPEG', 'JPG', 'BMP', 'TIFF']
    
    def pdf_to_images(self, pdf_path, output_folder="pdf_images", image_format='PNG', dpi=200):
        """
        Convierte un PDF a imágenes (una por página)
        
        Args:
            pdf_path (str): Ruta del PDF
            output_folder (str): Carpeta de salida
            image_format (str): Formato de imagen (PNG, JPEG, etc.)
            dpi (int): Resolución de la imagen (mayor = mejor calidad)
        """
        try:
            os.makedirs(output_folder, exist_ok=True)
            
            print(f"🔄 Convirtiendo PDF a imágenes (DPI: {dpi})...")
            
            # Convertir PDF a lista de imágenes
            images = convert_from_path(pdf_path, dpi=dpi)
            
            for i, image in enumerate(images, start=1):
                output_path = f"{output_folder}/pagina_{i}.{image_format.lower()}"
                image.save(output_path, image_format)
                print(f"✅ Página {i} convertida a {image_format}")
            
            print(f"🎉 {len(images)} páginas convertidas en: {output_folder}")
            return True
            
        except Exception as e:
            print(f"❌ Error al convertir a imágenes: {str(e)}")
            print("💡 Asegúrate de tener poppler instalado (Windows)")
            return False
    
    def images_to_pdf(self, image_paths, output_path="imagenes_a_pdf.pdf"):
        """
        Convierte múltiples imágenes a un PDF
        
        Args:
            image_paths (list): Lista de rutas de imágenes
            output_path (str): Ruta del PDF de salida
        """
        try:
            images = []
            
            # Cargar y validar imágenes
            for img_path in image_paths:
                if not os.path.exists(img_path):
                    print(f"⚠️  Imagen no encontrada: {img_path}")
                    continue
                
                img = Image.open(img_path)
                # Convertir a RGB si es necesario (para JPEG)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)
                print(f"📷 Imagen cargada: {img_path}")
            
            if not images:
                print("❌ No hay imágenes válidas para convertir")
                return False
            
            # Guardar todas las imágenes como PDF
            images[0].save(
                output_path, 
                save_all=True, 
                append_images=images[1:],
                resolution=100.0
            )
            
            print(f"✅ PDF creado: {output_path} ({len(images)} páginas)")
            return True
            
        except Exception as e:
            print(f"❌ Error al convertir imágenes a PDF: {str(e)}")
            return False
    
    def pdf_to_text(self, pdf_path, output_path="output.txt"):
        """
        Extrae todo el texto de un PDF
        
        Args:
            pdf_path (str): Ruta del PDF
            output_path (str): Ruta del archivo de texto de salida
        """
        try:
            doc = fitz.open(pdf_path)
            full_text = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                full_text.append(f"--- Página {page_num + 1} ---\n{text}\n")
                print(f"📄 Página {page_num + 1} procesada")
            
            # Guardar en archivo
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(full_text))
            
            doc.close()
            print(f"✅ Texto extraído y guardado en: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error al extraer texto: {str(e)}")
            return False
    
    def text_to_pdf(self, text_content, output_path="text_to_pdf.pdf"):
        """
        Crea un PDF desde texto
        
        Args:
            text_content (str): Contenido de texto
            output_path (str): Ruta del PDF de salida
        """
        try:
            c = canvas.Canvas(output_path, pagesize=letter)
            width, height = letter
            
            # Configuración de texto
            c.setFont("Helvetica", 12)
            y_position = height - 50  # Margen superior
            line_height = 15
            
            lines = text_content.split('\n')
            
            for line in lines:
                # Nueva página si no hay espacio
                if y_position < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = height - 50
                
                c.drawString(50, y_position, line[:90])  # Limitar ancho
                y_position -= line_height
            
            c.save()
            print(f"✅ PDF de texto creado: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error al crear PDF desde texto: {str(e)}")
            return False
    
    def rotate_pdf(self, pdf_path, output_path, rotation=90):
        """
        Rota todas las páginas de un PDF
        
        Args:
            pdf_path (str): PDF de entrada
            output_path (str): PDF de salida
            rotation (int): Grados de rotación (90, 180, 270)
        """
        try:
            doc = fitz.open(pdf_path)
            
            for page in doc:
                page.set_rotation(rotation)
                print(f"🔄 Página rotada {rotation}°")
            
            doc.save(output_path)
            doc.close()
            
            print(f"✅ PDF rotado guardado en: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error al rotar PDF: {str(e)}")
            return False


# Ejemplo de uso
if __name__ == "__main__":
    converter = PDFConverter()
    
    # Ejemplo 1: PDF a imágenes
    # converter.pdf_to_images("documento.pdf", dpi=300, image_format='PNG')
    
    # Ejemplo 2: Imágenes a PDF
    imagenes = ["imagen1.jpg", "imagen2.png", "imagen3.jpg"]
    # converter.images_to_pdf(imagenes, "album_fotos.pdf")
    
    # Ejemplo 3: Extraer texto
    # converter.pdf_to_text("documento.pdf", "texto_extraido.txt")
    
    # Ejemplo 4: Texto a PDF
    texto = "Este es un ejemplo de texto.\nSe convertirá en PDF.\n¡Muy útil!"
    # converter.text_to_pdf(texto, "mi_documento.pdf")
    
    # Ejemplo 5: Rotar PDF
    # converter.rotate_pdf("documento.pdf", "documento_rotado.pdf", rotation=90)