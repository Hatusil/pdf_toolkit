"""
Script para verificar que todas las dependencias estén instaladas correctamente
"""

def test_imports():
    """Prueba la importación de todas las librerías necesarias"""
    
    print("=" * 60)
    print("🧪 VERIFICANDO INSTALACIÓN DE PDF TOOLKIT")
    print("=" * 60)
    print()
    
    # Lista de módulos a probar
    modules = [
        ("pypdf", "PdfReader, PdfWriter, PdfMerger"),
        ("fitz", "PyMuPDF (para edición avanzada)"),
        ("PIL", "Pillow (para imágenes)"),
        ("reportlab", "ReportLab (para crear PDFs)"),
        ("pdf2image", "pdf2image (para convertir PDF a imágenes)")
    ]
    
    all_ok = True
    
    for module_name, description in modules:
        try:
            if module_name == "pypdf":
                from pypdf import PdfReader, PdfWriter, PdfMerger
            elif module_name == "fitz":
                import fitz
            elif module_name == "PIL":
                from PIL import Image
            elif module_name == "reportlab":
                from reportlab.pdfgen import canvas
            elif module_name == "pdf2image":
                from pdf2image import convert_from_path
            
            print(f"✅ {description:50} OK")
        except ImportError as e:
            print(f"❌ {description:50} ERROR")
            print(f"   Detalles: {str(e)}")
            all_ok = False
    
    print()
    print("=" * 60)
    
    if all_ok:
        print("🎉 ¡TODAS LAS DEPENDENCIAS ESTÁN INSTALADAS CORRECTAMENTE!")
        print()
        print("Puedes ejecutar el programa con:")
        print("   python pdf_toolkit_gui.py")
    else:
        print("⚠️  FALTAN ALGUNAS DEPENDENCIAS")
        print()
        print("Instala las dependencias faltantes con:")
        print("   pip install -r requirements.txt")
        
        # Verificar Poppler específicamente para Windows
        try:
            from pdf2image import convert_from_path
            # Intentar una conversión de prueba
            print()
            print("⚠️  NOTA PARA WINDOWS:")
            print("   Si pdf2image da error al usarlo, necesitas instalar Poppler:")
            print("   1. Descarga desde: https://github.com/oschwartz10612/poppler-windows/releases")
            print("   2. Extrae en C:\\poppler")
            print("   3. Agrega C:\\poppler\\Library\\bin al PATH")
        except:
            pass
    
    print("=" * 60)
    
    return all_ok


def test_tkinter():
    """Verifica que tkinter esté disponible"""
    print()
    print("🔍 Verificando interfaz gráfica (tkinter)...")
    
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana
        root.destroy()
        print("✅ Tkinter está disponible")
        return True
    except ImportError:
        print("❌ Tkinter NO está disponible")
        print("   En Linux, instala con: sudo apt-get install python3-tk")
        return False


def check_python_version():
    """Verifica la versión de Python"""
    import sys
    
    print()
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    
    print(f"   Versión instalada: Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Versión de Python compatible")
        return True
    else:
        print("❌ Necesitas Python 3.8 o superior")
        return False


def main():
    """Función principal"""
    python_ok = check_python_version()
    tkinter_ok = test_tkinter()
    imports_ok = test_imports()
    
    print()
    if python_ok and tkinter_ok and imports_ok:
        print("🚀 TODO LISTO - Puedes ejecutar: python pdf_toolkit_gui.py")
    else:
        print("🔧 Revisa los errores anteriores y corrígelos")
    print()


if __name__ == "__main__":
    main()