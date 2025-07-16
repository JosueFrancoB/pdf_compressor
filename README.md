# Servicio de Compresión de PDF

Un servicio web desarrollado en Python con Flask que permite comprimir archivos PDF usando Ghostscript con tres niveles de compresión diferentes.

## Características

- **Tres niveles de compresión**:
  - **Nivel 1 (Prepress)**: Alta calidad, compresión moderada
  - **Nivel 2 (Ebook)**: Calidad media, compresión equilibrada
  - **Nivel 3 (Screen)**: Calidad baja, máxima compresión

- **API REST** para subir y comprimir archivos PDF
- **Contenerización** con Docker
- **Gestión automática** de archivos temporales
- **Métricas de compresión** (tamaño original vs comprimido)

## Requisitos

- Docker
- Docker Compose (opcional)

## Instalación y Uso

### Opción 1: Usando Docker Compose (Recomendado)

1. **Clonar o descargar el proyecto**
2. **Construir y ejecutar el servicio**:
   ```bash
   docker-compose up --build
   ```

### Opción 2: Usando Docker directamente

1. **Construir la imagen**:
   ```bash
   docker build -t pdf-compressor .
   ```

2. **Ejecutar el contenedor**:
   ```bash
   docker run -p 5000:5000 -v $(pwd)/uploads:/tmp/uploads -v $(pwd)/compressed:/tmp/compressed pdf-compressor
   ```

## API Endpoints

### 1. Health Check
```bash
GET /health
```
Verifica el estado del servicio.

**Respuesta**:
```json
{
  "status": "healthy",
  "service": "PDF Compressor",
  "version": "1.0.0"
}
```

### 2. Comprimir PDF
```bash
POST /compress
```

**Parámetros**:
- `file`: Archivo PDF a comprimir (multipart/form-data)
- `level`: Nivel de compresión (1, 2, o 3) - opcional, por defecto 1

**Ejemplo con curl**:
```bash
curl -X POST \
  -F "file=@documento.pdf" \
  -F "level=2" \
  http://localhost:5000/compress
```

**Respuesta exitosa**:
```json
{
  "success": true,
  "message": "PDF comprimido exitosamente con nivel 2",
  "original_filename": "documento.pdf",
  "compressed_filename": "compressed_level_2_documento.pdf",
  "original_size_mb": 5.2,
  "compressed_size_mb": 2.1,
  "compression_ratio_percent": 59.62,
  "file_id": "uuid-del-archivo"
}
```

### 3. Descargar PDF Comprimido
```bash
GET /download/<file_id>
```

**Ejemplo**:
```bash
curl -O -J http://localhost:5000/download/uuid-del-archivo
```

### 4. Limpiar Archivos Temporales
```bash
POST /cleanup
```

Elimina archivos comprimidos más antiguos de 1 hora.

## Niveles de Compresión

### Nivel 1 (Prepress)
- **Configuración**: `/prepress`
- **Uso**: Para impresión de alta calidad
- **Compresión**: Moderada
- **Calidad**: Muy alta

### Nivel 2 (Ebook)
- **Configuración**: `/ebook`
- **Uso**: Para libros electrónicos y documentos web
- **Compresión**: Equilibrada
- **Calidad**: Alta

### Nivel 3 (Screen)
- **Configuración**: `/screen`
- **Uso**: Para visualización en pantalla
- **Compresión**: Máxima
- **Calidad**: Baja

## Límites y Configuración

- **Tamaño máximo de archivo**: 50MB
- **Timeout de compresión**: 5 minutos
- **Almacenamiento temporal**: `/tmp/uploads` y `/tmp/compressed`
- **Limpieza automática**: Archivos más antiguos de 1 hora

## Estructura del Proyecto

```
pdf_compressor/
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias de Python
├── Dockerfile            # Configuración de Docker
├── docker-compose.yml    # Configuración de Docker Compose
├── project_context.json  # Contexto del proyecto (automático)
├── project_manager.py    # Gestor del contexto del proyecto
├── context_example.py    # Ejemplo de uso del gestor
├── test_service.py       # Script de pruebas
└── README.md             # Documentación
```

## Desarrollo Local

Si quieres ejecutar el servicio sin Docker:

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Instalar Ghostscript**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ghostscript
   
   # CentOS/RHEL
   sudo yum install ghostscript
   
   # macOS
   brew install ghostscript
   ```

3. **Ejecutar la aplicación**:
   ```bash
   python app.py
   ```

## Gestión de Contexto del Proyecto

El proyecto incluye un sistema automático de gestión de contexto que permite:

### Archivos de Contexto
- **`project_context.json`**: Contiene toda la información del proyecto
- **`project_manager.py`**: Gestor automático del contexto
- **`context_example.py`**: Ejemplo de uso del sistema

### Funcionalidades
- **Lectura automática**: Carga el contexto al iniciar el proyecto
- **Actualización automática**: Guarda cambios en tiempo real
- **Resumen del proyecto**: Muestra información clave del proyecto
- **Gestión de archivos**: Actualiza información de archivos automáticamente
- **Gestión de endpoints**: Mantiene registro de la API
- **Configuración de compresión**: Actualiza niveles de compresión

### Uso
```bash
# Ejecutar ejemplo de gestión de contexto
python context_example.py

# Cargar y mostrar resumen del proyecto
python -c "from project_manager import ProjectContextManager; print(ProjectContextManager().get_project_summary())"
```

## Monitoreo y Logs

El servicio incluye logging detallado para monitorear:
- Subida de archivos
- Proceso de compresión
- Errores y excepciones
- Métricas de compresión

## Seguridad

- Validación de tipos de archivo (solo PDF)
- Sanitización de nombres de archivo
- Límites de tamaño de archivo
- Timeout en operaciones de compresión
- Limpieza automática de archivos temporales

## Troubleshooting

### Error: "Ghostscript no está instalado"
- Verificar que Ghostscript esté instalado en el contenedor
- Reconstruir la imagen Docker

### Error: "Timeout al comprimir el PDF"
- El archivo PDF es muy grande o complejo
- Aumentar el timeout en el código si es necesario

### Error: "No se proporcionó ningún archivo"
- Verificar que el archivo se esté enviando correctamente
- Verificar el nombre del campo (`file`)

## Contribuciones

Para contribuir al proyecto:
1. Fork el repositorio
2. Crear una rama para tu feature
3. Hacer commit de tus cambios
4. Crear un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. 