# 📄 PDF Toolkit - Herramienta Profesional de Manipulación de PDFs

![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Una aplicación completa con interfaz gráfica para manipular archivos PDF: fusionar, dividir, convertir, editar, comprimir y más.

## 📑 Tabla de Contenidos

- [Características](#-características)
- [Requisitos del Sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
  - [Windows](#windows)
  - [Linux](#linux)
  - [macOS](#macos)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Uso del Programa](#-uso-del-programa)
- [Funcionalidades Detalladas](#-funcionalidades-detalladas)
- [Solución de Problemas](#-solución-de-problemas)
- [Ejemplos](#-ejemplos)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## ✨ Características

- **📎 Fusionar PDFs**: Combina múltiples archivos PDF en uno solo con control de orden
- **✂️ Dividir PDFs**: Divide PDFs por páginas individuales, rangos, fragmentos o páginas específicas
- **🔄 Convertir Formatos**: 
  - PDF → Imágenes (PNG, JPEG, BMP, TIFF)
  - Imágenes → PDF
  - PDF → Texto
  - Texto → PDF
- **✏️ Editar PDFs**:
  - Agregar marcas de agua
  - Insertar texto
  - Rotar páginas (90°, 180°, 270°)
  - Proteger con contraseña
- **📦 Comprimir PDFs**: Reduce el tamaño del archivo manteniendo la calidad
- **🎨 Interfaz Gráfica Moderna**: Fácil de usar con pestañas organizadas
- **📋 Registro en Tiempo Real**: Monitorea todas las operaciones
- **⚡ Procesamiento en Hilos**: No congela la interfaz durante operaciones largas

---

## 🖥️ Requisitos del Sistema

### Requisitos Obligatorios

- **Python 3.12** (recomendado) o Python 3.8+
- **Sistema Operativo**: Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+
- **RAM**: Mínimo 4GB (8GB recomendado para PDFs grandes)
- **Espacio en Disco**: 500MB libres

### Dependencias Python

```
pypdf==4.0.0
PyMuPDF==1.23.8
pdf2image==1.17.0
Pillow==10.2.0
reportlab==4.0.9
```

### Dependencias del Sistema

- **Windows**: Poppler (para conversión PDF → Imágenes)
- **Linux**: poppler-utils, python3-tk
- **macOS**: poppler (via Homebrew)

---

## 🚀 Instalación

### Windows

#### 1. Instalar Python 3.12

1. Descarga Python 3.12 desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación:
   - ✅ Marca "Add Python to PATH"
   - ✅ Marca "Install for all users" (opcional)
   - ✅ Incluye "tcl/tk and IDLE"
3. Verifica la instalación:
   ```cmd
   python --version
   ```
   Debería mostrar: `Python 3.12.x`

#### 2. Descargar el Proyecto

```cmd
# Opción A: Con Git
git clone https://github.com/Hatusil/pdf_toolkit.git
cd pdf_toolkit

# Opción B: Descarga manual
# Descarga el ZIP del proyecto y descomprime
cd ruta\a\pdf_toolkit
```

#### 3. Crear Entorno Virtual

```cmd
py -3.12 -m venv venv312
venv312\Scripts\activate
```

Cuando esté activo verás `(venv312)` al inicio de tu línea de comandos.

#### 4. Instalar Dependencias Python

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

#### 5. Instalar Poppler (IMPORTANTE)

**Método 1 - Descarga Manual (Recomendado):**

1. Descarga Poppler desde: [poppler-windows/releases](https://github.com/oschwartz10612/poppler-windows/releases)
2. Descarga el archivo más reciente (ej: `Release-24.02.0-0.zip`)
3. Extrae el contenido en `C:\poppler`
4. Agregar al PATH:
   - Presiona `Win + R`, escribe `sysdm.cpl` y presiona Enter
   - Ve a la pestaña "Opciones avanzadas"
   - Haz clic en "Variables de entorno"
   - En "Variables del sistema", selecciona "Path" y haz clic en "Editar"
   - Haz clic en "Nuevo" y agrega: `C:\poppler\Library\bin`
   - Haz clic en "Aceptar" en todas las ventanas
   - **Reinicia tu terminal**

5. Verifica la instalación:
   ```cmd
   where pdftoppm
   ```
   Debería mostrar la ruta a `pdftoppm.exe`

**Método 2 - Con Chocolatey:**

Si tienes Chocolatey instalado:
```cmd
choco install poppler
```

#### 6. Verificar Instalación

```cmd
python test_installation.py
```

Si todo está bien, verás: `🎉 ¡TODAS LAS DEPENDENCIAS ESTÁN INSTALADAS CORRECTAMENTE!`

#### 7. Ejecutar el Programa

```cmd
python pdf_toolkit_gui.py
```

---

### Linux

#### 1. Instalar Python 3.12

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12 python3.12-venv python3.12-tk
```

**Fedora:**
```bash
sudo dnf install python3.12 python3.12-tkinter
```

Verifica:
```bash
python3.12 --version
```

#### 2. Instalar Dependencias del Sistema

```bash
# Ubuntu/Debian
sudo apt install poppler-utils python3-tk

# Fedora
sudo dnf install poppler-utils python3-tkinter

# Arch Linux
sudo pacman -S poppler python-tk
```

#### 3. Clonar y Configurar el Proyecto

```bash
# Clonar repositorio
git clone https://github.com/Hatusil/pdf_toolkit.git
cd pdf_toolkit

# Crear entorno virtual
python3.12 -m venv venv312
source venv312/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Verificar y Ejecutar

```bash
# Verificar
python test_installation.py

# Ejecutar
python pdf_toolkit_gui.py
```

---

### macOS

#### 1. Instalar Python 3.12

**Con Homebrew (Recomendado):**
```bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python 3.12
brew install python@3.12
```

Verifica:
```bash
python3.12 --version
```

#### 2. Instalar Poppler

```bash
brew install poppler
```

#### 3. Configurar el Proyecto

```bash
# Clonar
git clone https://github.com/Hatusil/pdf_toolkit.git
cd pdf_toolkit

# Crear entorno virtual
python3.12 -m venv venv312
source venv312/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Verificar y Ejecutar

```bash
python test_installation.py
python pdf_toolkit_gui.py
```

---

## 📁 Estructura del Proyecto

```
pdf_toolkit/
│
├── 📄 README.md                    # Este archivo
├── 📄 requirements.txt             # Dependencias Python
├── 📄 LICENSE                      # Licencia del proyecto
│
├── 🐍 pdf_toolkit_gui.py          # Interfaz gráfica principal
├── 🐍 pdf_merger.py               # Módulo de fusión
├── 🐍 pdf_splitter.py             # Módulo de división
├── 🐍 pdf_converter.py            # Módulo de conversión
├── 🐍 pdf_editor.py               # Módulo de edición
├── 🐍 test_installation.py        # Script de verificación
│
├── 📁 test_pdfs/                   # PDFs de prueba (opcional)
│   ├── documento1.pdf
│   ├── documento2.pdf
│   └── documento3.pdf
│
├── 📁 output/                      # Archivos generados (se crea automáticamente)
│
├── 📁 venv/                        # Entorno virtual (no incluir en Git)
│
└── 📁 docs/                        # Documentación adicional
    ├── INSTALLATION.md
    ├── USAGE.md
    └── TROUBLESHOOTING.md
```

---

## 📖 Uso del Programa

### Inicio Rápido

1. **Activar el entorno virtual:**

   **Windows:**
   ```cmd
   venv312\Scripts\activate
   ```

   **Linux/macOS:**
   ```bash
   source venv312/bin/activate
   ```

2. **Ejecutar el programa:**
   ```bash
   python pdf_toolkit_gui.py
   ```

3. **Seleccionar la operación** en las pestañas superiores

4. **Seguir los pasos** específicos de cada funcionalidad

### Interfaz del Programa

```
┌─────────────────────────────────────────────────────┐
│           📄 PDF Toolkit                            │
│    Herramientas profesionales para manipular PDFs  │
├─────────────────────────────────────────────────────┤
│ [📎 Fusionar] [✂️ Dividir] [🔄 Convertir]           │
│ [✏️ Editar] [📦 Comprimir]                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│          [ Área de trabajo ]                        │
│                                                     │
├─────────────────────────────────────────────────────┤
│ 📋 Registro de operaciones                         │
│ ✅ Archivo procesado exitosamente...               │
│ 💾 Guardado en: resultado.pdf                      │
└─────────────────────────────────────────────────────┘
```

---

## 🔧 Funcionalidades Detalladas

### 1. 📎 Fusionar PDFs

**Propósito:** Combinar múltiples archivos PDF en un solo documento.

**Casos de uso:**
- Unir capítulos de un libro
- Combinar facturas mensuales
- Juntar reportes en un solo archivo

**Pasos:**
1. Haz clic en la pestaña **"📎 Fusionar"**
2. Presiona **"➕ Agregar PDFs"**
3. Selecciona 2 o más archivos (mantén `Ctrl` para selección múltiple)
4. **Reordena** si es necesario:
   - Selecciona un archivo
   - Usa **🔼 Subir** o **🔽 Bajar**
5. Presiona **"🔗 FUSIONAR PDFs"**
6. Elige ubicación y nombre del archivo resultante
7. Espera a que termine (verás el progreso en el log)

**Ejemplo:**
```
Entrada:
  - introduccion.pdf (10 páginas)
  - capitulo1.pdf (25 páginas)
  - capitulo2.pdf (30 páginas)
  - conclusion.pdf (5 páginas)

Salida:
  - libro_completo.pdf (70 páginas)
```

---

### 2. ✂️ Dividir PDFs

**Propósito:** Separar un PDF grande en archivos más pequeños.

**Modos disponibles:**

#### A) Por Página Individual
- Crea un archivo separado por cada página
- **Útil para:** Extraer páginas sueltas, compartir páginas individuales

**Ejemplo:**
```
Entrada: manual.pdf (50 páginas)
Salida: pagina_1.pdf, pagina_2.pdf, ..., pagina_50.pdf
```

#### B) Por Rango de Páginas
- Extrae un rango específico
- **Formato:** `inicio-fin` (ej: `5-15`)
- **Útil para:** Extraer un capítulo específico

**Ejemplo:**
```
Entrada: libro.pdf (200 páginas)
Rango: 50-75
Salida: paginas_50-75.pdf (25 páginas del capítulo 3)
```

#### C) Cada N Páginas
- Divide en fragmentos de tamaño fijo
- **Útil para:** Crear partes iguales para distribución

**Ejemplo:**
```
Entrada: documento.pdf (100 páginas)
Fragmento: 20 páginas
Salida: 
  - fragmento_1.pdf (páginas 1-20)
  - fragmento_2.pdf (páginas 21-40)
  - fragmento_3.pdf (páginas 41-60)
  - fragmento_4.pdf (páginas 61-80)
  - fragmento_5.pdf (páginas 81-100)
```

#### D) Páginas Específicas
- Extrae solo las páginas que elijas
- **Formato:** `1,5,10,15` (separadas por coma)
- **Útil para:** Extraer páginas no consecutivas

**Ejemplo:**
```
Entrada: contrato.pdf (50 páginas)
Páginas: 1,2,10,25,50
Salida: paginas_especificas.pdf (5 páginas seleccionadas)
```

---

### 3. 🔄 Convertir Formatos

#### A) PDF → Imágenes

**Parámetros:**
- **Formato:** PNG (mejor calidad, mayor tamaño) o JPEG (comprimido)
- **DPI (Resolución):**
  - 72 DPI: Vista rápida/web
  - 150 DPI: Presentaciones
  - 200 DPI: Uso general (recomendado)
  - 300 DPI: Impresión de calidad
  - 600 DPI: Impresión profesional

**Ejemplo:**
```
Entrada: presentacion.pdf (20 diapositivas)
Formato: PNG
DPI: 300
Salida: 20 archivos PNG de alta calidad
```

**Tiempo estimado:** 1-2 segundos por página

#### B) Imágenes → PDF

**Formatos soportados:** PNG, JPEG, JPG, BMP, TIFF

**Pasos:**
1. Selecciona múltiples imágenes
2. Se combinarán en el orden seleccionado
3. Cada imagen será una página del PDF

**Ejemplo:**
```
Entrada:
  - foto1.jpg
  - foto2.jpg
  - foto3.jpg
Salida: album.pdf (3 páginas)
```

**Nota:** Las imágenes se ajustan automáticamente al tamaño de página.

#### C) PDF → Texto

**Extrae** todo el texto seleccionable del PDF.

**Limitaciones:**
- No funciona con PDFs escaneados (solo imágenes)
- No extrae texto de imágenes dentro del PDF
- Mantiene la estructura por páginas

**Ejemplo:**
```
Entrada: articulo.pdf (10 páginas)
Salida: articulo.txt (texto plano con marcadores de página)
```

#### D) Texto → PDF

**Convierte** archivos de texto plano en PDF formateado.

**Características:**
- Fuente: Helvetica 12pt
- Saltos de página automáticos
- Márgenes estándar

**Ejemplo:**
```
Entrada: notas.txt
Salida: notas.pdf (texto formateado)
```

---

### 4. ✏️ Editar PDFs

#### A) Agregar Marca de Agua

**Parámetros:**
- **Texto:** El texto a mostrar (ej: "CONFIDENCIAL", "BORRADOR", "COPIA")
- **Opacidad:** 0.0 (invisible) a 1.0 (opaco)
  - Recomendado: 0.2-0.4 para marcas discretas

**Características:**
- Se añade en diagonal
- Aparece en todas las páginas
- Color gris claro
- Tamaño de fuente: 60pt

**Ejemplo:**
```
Entrada: informe.pdf
Marca: "CONFIDENCIAL"
Opacidad: 0.3
Salida: informe_marcado.pdf (con marca en todas las páginas)
```

#### B) Rotar Páginas

**Opciones:** 90°, 180°, 270°

**Útil para:**
- Corregir PDFs escaneados en orientación incorrecta
- Rotar imágenes dentro de documentos

**Nota:** Rota todas las páginas del documento.

**Ejemplo:**
```
Entrada: escaneo.pdf (horizontal)
Rotación: 90°
Salida: escaneo_rotado.pdf (vertical)
```

#### C) Proteger con Contraseña

**Seguridad:** Encriptación AES-256

**Permisos permitidos:**
- ✅ Abrir el documento (requiere contraseña)
- ✅ Imprimir
- ✅ Copiar texto
- ❌ Editar contenido (protegido)

**Ejemplo:**
```
Entrada: documento_privado.pdf
Contraseña: "MiPassword123"
Salida: documento_protegido.pdf
```

**Importante:** Guarda la contraseña en un lugar seguro. No se puede recuperar si la olvidas.

---

### 5. 📦 Comprimir PDFs

**Niveles de compresión:**

| Nivel | Calidad | Reducción | Uso Recomendado |
|-------|---------|-----------|-----------------|
| Baja | Excelente | 10-30% | Archivos importantes, impresión |
| Media | Buena | 30-50% | Uso general (recomendado) |
| Alta | Aceptable | 50-80% | Envío por email, archivos grandes |

**Técnicas aplicadas:**
- Eliminación de objetos no usados
- Compresión de streams
- Optimización de imágenes
- Limpieza de sintaxis

**Ejemplo:**
```
Entrada: presentacion.pdf (15 MB)
Nivel: Media
Salida: presentacion_comprimida.pdf (5 MB)
Reducción: 67%
```

**Tiempo:** 5-30 segundos dependiendo del tamaño

---

## 🐛 Solución de Problemas

### Problema: "No module named 'pypdf'"

**Causa:** Dependencias no instaladas

**Solución:**
```bash
pip install -r requirements.txt
```

---

### Problema: "Unable to get page count. Is poppler installed?"

**Causa:** Poppler no está instalado o no está en el PATH

**Solución Windows:**
1. Verifica que Poppler esté en `C:\poppler\Library\bin`
2. Comprueba el PATH:
   ```cmd
   where pdftoppm
   ```
3. Si no aparece, agrega `C:\poppler\Library\bin` al PATH
4. **Reinicia la terminal**

**Solución Linux:**
```bash
sudo apt install poppler-utils
```

**Solución macOS:**
```bash
brew install poppler
```

---

### Problema: "tkinter not found" o "_tkinter.TclError"

**Causa:** Tkinter no está instalado

**Solución Linux:**
```bash
sudo apt install python3-tk
```

**Solución Windows/macOS:**
Reinstala Python y asegúrate de marcar "tcl/tk and IDLE" durante la instalación.

---

### Problema: El programa se congela

**Causa:** Operación pesada en proceso

**Solución:**
- Es normal para PDFs grandes (>100 MB)
- Revisa el log para ver el progreso
- Espera pacientemente
- Si tarda >5 minutos, cierra y verifica el archivo

---

### Problema: "Permission denied" al guardar

**Causa:** El archivo de salida está abierto en otro programa

**Solución:**
1. Cierra Adobe Reader, Acrobat u otro visor de PDF
2. Intenta de nuevo
3. Guarda con un nombre diferente

---

### Problema: Error al fusionar PDFs protegidos

**Causa:** Los PDFs tienen restricciones de copia/edición

**Solución:**
- Primero desprotege los PDFs (necesitas la contraseña)
- O usa una herramienta especializada para PDFs protegidos

---

### Problema: Calidad baja en PDF → Imágenes

**Causa:** DPI muy bajo

**Solución:**
- Aumenta el DPI a 300 o más
- Usa formato PNG en lugar de JPEG
- Ten en cuenta que mayor DPI = archivos más grandes

---

### Problema: Texto extraído está desordenado

**Causa:** El PDF tiene formato complejo o múltiples columnas

**Solución:**
- Algunos PDFs no se pueden extraer correctamente
- Prueba con una herramienta OCR para PDFs escaneados
- Considera extraer manualmente

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Crear un Libro Digital

**Escenario:** Tienes 5 PDFs de diferentes capítulos y quieres crear un libro completo.

```bash
# Archivos de entrada:
capitulo_01.pdf
capitulo_02.pdf
capitulo_03.pdf
capitulo_04.pdf
capitulo_05.pdf
```

**Pasos:**
1. Abre **"📎 Fusionar"**
2. Agrega los 5 archivos en orden
3. Fusiona → `mi_libro.pdf`
4. (Opcional) Ve a **"✏️ Editar"** y agrega marca de agua "BORRADOR"
5. (Opcional) Ve a **"📦 Comprimir"** para reducir tamaño

**Resultado:** `mi_libro.pdf` (completo y listo para compartir)

---

### Ejemplo 2: Preparar Documento para Email

**Escenario:** Tu PDF es muy grande (20 MB) y necesitas enviarlo por email.

**Pasos:**
1. Abre **"📦 Comprimir"**
2. Selecciona tu PDF
3. Nivel: **Alta compresión**
4. Comprime

**Resultado:** PDF reducido a ~5 MB (aceptable para email)

---

### Ejemplo 3: Extraer Páginas Importantes de un Manual

**Escenario:** Tienes un manual de 500 páginas pero solo necesitas las páginas 10, 25, 100 y 250.

**Pasos:**
1. Abre **"✂️ Dividir"**
2. Carga `manual.pdf`
3. Modo: **Páginas específicas**
4. Escribe: `10,25,100,250`
5. Extrae → `paginas_importantes.pdf`

**Resultado:** PDF con solo las 4 páginas necesarias

---

### Ejemplo 4: Convertir Presentación para Redes Sociales

**Escenario:** Quieres compartir tu presentación como imágenes en LinkedIn.

**Pasos:**
1. Abre **"🔄 Convertir"**
2. Modo: **PDF → Imágenes**
3. Carga `presentacion.pdf`
4. Formato: **PNG**
5. DPI: **300**
6. Convierte

**Resultado:** 20 imágenes PNG de alta calidad, una por cada diapositiva

---

### Ejemplo 5: Proteger Documento Confidencial

**Escenario:** Tienes información sensible que quieres compartir de forma segura.

**Pasos:**
1. Abre **"✏️ Editar"**
2. Carga el PDF
3. Operación: **Agregar marca de agua**
4. Texto: "CONFIDENCIAL"
5. Opacidad: 0.3
6. Aplica → `documento_marca.pdf`
7. Luego, Operación: **Proteger con contraseña**
8. Contraseña: `TuPassword123`
9. Aplica → `documento_protegido.pdf`

**Resultado:** PDF con marca de agua y protegido con contraseña

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres mejorar este proyecto:

1. **Fork** el repositorio
2. **Crea una rama** para tu feature:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. **Commit** tus cambios:
   ```bash
   git commit -m "Añade nueva funcionalidad"
   ```
4. **Push** a la rama:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. **Abre un Pull Request**

### Áreas de Mejora

- [ ] Agregar vista previa de PDFs
- [ ] Implementar drag & drop de archivos
- [ ] Añadir OCR para PDFs escaneados
- [ ] Soporte para procesamiento por lotes
- [ ] Modo oscuro
- [ ] Internacionalización (i18n)
- [ ] Tests automatizados
- [ ] Documentación en inglés

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

```
MIT License

Copyright (c) 2025 PDF Toolkit

Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia
de este software y archivos de documentación asociados (el "Software"), para
utilizar el Software sin restricción, incluyendo sin limitación los derechos
de usar, copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o
vender copias del Software...
```

---

## 👤 Autor

**Hatusil**
- GitHub: [@Hatusil](https://github.com/Hatusil)
- Email: hatusil@proton.me

---

## 🙏 Agradecimientos

- [pypdf](https://github.com/py-pdf/pypdf) - Manipulación de PDFs
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF) - Edición avanzada
- [pdf2image](https://github.com/Belval/pdf2image) - Conversión de PDFs
- [Pillow](https://python-pillow.org/) - Procesamiento de imágenes
- [ReportLab](https://www.reportlab.com/) - Generación de PDFs

---

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:

1. **Revisa** la sección de [Solución de Problemas](#-solución-de-problemas)
2. **Busca** en los [Issues](https://github.com/Hatusil/pdf_toolkit/issues) existentes
3. **Crea** un nuevo Issue si no encuentras solución

---

## 📊 Estadísticas

![GitHub stars](https://img.shields.io/github/stars/Hatusil/pdf_toolkit)
![GitHub forks](https://img.shields.io/github/forks/Hatusil/pdf_toolkit)
![GitHub issues](https://img.shields.io/github/issues/Hatusil/pdf_toolkit)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Hatusil/pdf_toolkit)

---

## 🗺️ Roadmap

### Versión 1.1 (Próxima)
- [ ] Vista previa de PDFs
- [ ] Historial de operaciones
- [ ] Mejoras en la interfaz

### Versión 1.2
- [ ] OCR integrado
- [ ] Procesamiento por lotes
- [ ] API REST

### Versión 2.0
- [ ] Versión web
- [ ] Almacenamiento en la nube
- [ ] Colaboración en tiempo real

---

## 📚 Recursos Adicionales

- [Documentación de pypdf](https://pypdf.readthedocs.io/)
- [Guía de PyMuPDF](https://pymupdf.readthedocs.io/)
- [Tutorial de tkinter](https://docs.python.org/3/library/tkinter.html)
- [Python 3.12 Documentation](https://docs.python.org/3.12/)

---

## ⚠️ Disclaimer

Este software se proporciona "tal cual", sin garantía de ningún tipo. Los autores no se hacen responsables de cualquier daño o pérdida de datos que pueda ocurrir por el uso de este software.

**Siempre haz copias de seguridad de tus archivos importantes antes de procesarlos.**

---

**¿Encontraste este proyecto útil? ¡Dale una ⭐ en GitHub!**

---

*Última actualización: Noviembre 2025*
*Versión: 1.0.0*