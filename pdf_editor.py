"""
Módulo para editar PDFs: agregar marcas de agua, texto, imágenes, comprimir, etc.
"""
import fitz  # PyMuPDF
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import io
import os

class PDFEditor:
    def __init__(self, pdf_path):
        """
        Inicializa el editor con un PDF
        
        Args:
            pdf_path (str): Ruta del PDF a editar
        """
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        print(f"📝 PDF abierto para edición: {pdf_path}")
    
    def add_watermark(self, watermark_text, output_path, opacity=0.3, fontsize=60):
        """
        Agrega una marca de agua a todas las páginas
        
        Args:
            watermark_text (str): Texto de la marca de agua
            output_path (str): Ruta del PDF de salida
            opacity (float): Opacidad (0-1)
            fontsize (int): Tamaño de fuente
        """
        try:
            for page_num in range(len(self.doc)):
                page = self.doc[page_num]
                
                # Obtener dimensiones de la página
                rect = page.rect
                
                # Agregar marca de agua en diagonal
                text_point = fitz.Point(rect.width / 2, rect.height / 2)
                
                # Configurar el texto
                page.insert_text(
                    text_point,
                    watermark_text,
                    fontsize=fontsize,
                    rotate=45,
                    color=(0.7, 0.7, 0.7),
                    opacity=opacity,
                    overlay=True
                )
                
                print(f"✅ Marca de agua agregada a página {page_num + 1}")
            
            self.doc.save(output_path)
            print(f"💧 PDF con marca de agua guardado: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error al agregar marca de agua: {str(e)}")
            return False
    
    def add_text(self, page_num, text, x, y, output_path, fontsize=12, color=(0, 0, 0)):
        """
        Agrega texto en una posición específica
        
        Args:
            page_num (int): Número de página (empieza en 0)
            text (str): Texto a agregar
            x, y (float): Coordenadas
            output_path (str): PDF de salida
            fontsize (int): Tamaño de fuente
            color (tuple): Color RGB (0-1)
        """
        try:
            page = self.doc[page_num]
            
            page.insert_text(
                (x, y),
                text,
                fontsize=fontsize,
                color=color
            )
            
            self.doc.save(output_path)
            print(f"✅ Texto agregado en página {page_num + 1}")
            return True
            
        except Exception as e:
            print(f"❌ Error al agregar texto: {str(e)}")
            return False
    
    def add_image(self, page_num, image_path, x, y, width, height, output_path):
        """
        Inserta una imagen en el PDF
        
        Args:
            page_num (int): Número de página
            image_path (str): Ruta de la imagen
            x, y (float): Posición
            width, height (float): Dimensiones
            output_path (str): PDF de salida
        """
        try:
            page = self.doc[page_num]
            
            # Crear rectángulo para la imagen
            rect = fitz.Rect(x, y, x + width, y + height)
            
            # Insertar imagen
            page.insert_image(rect, filename=image_path)
            
            self.doc.save(output_path)
            print(f"✅ Imagen agregada en página {page_num + 1}")
            return True
            
        except Exception as e:
            print(f"❌ Error al agregar imagen: {str(e)}")
            return False
    
    def delete_pages(self, pages_to_delete, output_path):
        """
        Elimina páginas específicas del PDF
        
        Args:
            pages_to_delete (list): Lista de números de página (empieza en 0)
            output_path (str): PDF de salida
        """
        try:
            # Ordenar en orden descendente para no afectar índices
            pages_to_delete.sort(reverse=True)
            
            for page_num in pages_to_delete:
                if 0 <= page_num < len(self.doc):
                    self.doc.delete_page(page_num)
                    print(f"🗑️  Página {page_num + 1} eliminada")
            
            self.doc.save(output_path)
            print(f"✅ PDF modificado guardado: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error al eliminar páginas: {str(e)}")
            return False
    
    def compress_pdf(self, output_path, quality=1):
        """
        Comprime el PDF reduciendo calidad de imágenes
        
        Args:
            output_path (str): PDF de salida
            quality (int): 0=baja, 1=media, 2=alta calidad
        """
        try:
            # quality: 0 = low, 1 = medium, 2 = high
            self.doc.save(
                output_path,
                garbage=4,  # Eliminar objetos no usados
                deflate=True,  # Comprimir streams
                clean=True  # Limpiar sintaxis
            )
            
            # Calcular reducción de tamaño
            original_size = os.path.getsize(self.pdf_path)
            compressed_size = os.path.getsize(output_path)
            reduction = (1 - compressed_size/original_size) * 100
            
            print(f"✅ PDF comprimido guardado: {output_path}")
            print(f"📉 Reducción de tamaño: {reduction:.1f}%")
            print(f"   Original: {original_size/1024:.1f} KB")
            print(f"   Comprimido: {compressed_size/1024:.1f} KB")
            return True
            
        except Exception as e:
            print(f"❌ Error al comprimir: {str(e)}")
            return False
    
    def protect_pdf(self, output_path, user_password="", owner_password=""):
        """
        Protege el PDF con contraseña
        
        Args:
            output_path (str): PDF de salida
            user_password (str): Contraseña para abrir
            owner_password (str): Contraseña para editar
        """
        try:
            # Configurar permisos
            perm = int(
                fitz.PDF_PERM_ACCESSIBILITY |  # for accessibility only
                fitz.PDF_PERM_PRINT |  # permit printing
                fitz.PDF_PERM_COPY  # permit copying
            )
            
            self.doc.save(
                output_path,
                encryption=fitz.PDF_ENCRYPT_AES_256,
                user_pw=user_password,
                owner_pw=owner_password,
                permissions=perm
            )
            
            print(f"🔒 PDF protegido guardado: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error al proteger PDF: {str(e)}")
            return False
    
    def extract_images(self, output_folder="extracted_images"):
        """
        Extrae todas las imágenes del PDF
        
        Args:
            output_folder (str): Carpeta de salida
        """
        try:
            os.makedirs(output_folder, exist_ok=True)
            image_count = 0
            
            for page_num in range(len(self.doc)):
                page = self.doc[page_num]
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = self.doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    image_count += 1
                    image_path = f"{output_folder}/imagen_{image_count}.{image_ext}"
                    
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    print(f"🖼️  Imagen {image_count} extraída")
            
            print(f"✅ Total de imágenes extraídas: {image_count}")
            return True
            
        except Exception as e:
            print(f"❌ Error al extraer imágenes: {str(e)}")
            return False
    
    def close(self):
        """Cierra el documento"""
        self.doc.close()


# Ejemplo de uso
if __name__ == "__main__":
    editor = PDFEditor("documento.pdf")
    
    # Ejemplo 1: Agregar marca de agua
    # editor.add_watermark("CONFIDENCIAL", "con_marca.pdf", opacity=0.2)
    
    # Ejemplo 2: Agregar texto personalizado
    # editor.add_text(0, "Texto añadido", 100, 100, "con_texto.pdf")
    
    # Ejemplo 3: Insertar imagen
    # editor.add_image(0, "logo.png", 50, 50, 100, 100, "con_imagen.pdf")
    
    # Ejemplo 4: Eliminar páginas
    # editor.delete_pages([0, 2, 4], "sin_paginas.pdf")
    
    # Ejemplo 5: Comprimir PDF
    editor.compress_pdf("comprimido.pdf")
    
    # Ejemplo 6: Proteger con contraseña
    # editor.protect_pdf("protegido.pdf", user_password="1234", owner_password="admin")
    
    # Ejemplo 7: Extraer imágenes
    # editor.extract_images("imagenes_del_pdf")
    
    editor.close()