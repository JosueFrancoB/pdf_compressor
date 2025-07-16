import json
import os
import subprocess
import uuid
from flask_cors import CORS
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import logging
import threading
import time

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

with open('config.json', 'r') as f:
    config = json.load(f)

if not config:
    logger.error('\033[91mconfig.json is not valid\033[0m')
    exit(1)

if not config.get('port'):
    # warning in yellow
    logger.warning('\033[93mPort is not set in config.json, using default port 5000\033[0m')
if not config.get('max_file_size_mb'):
    logger.warning('\033[93mMax file size is not set in config.json, using default max file size 50MB\033[0m')
if not config.get('allowed_extensions'):
    logger.warning('\033[93mAllowed extensions are not set in config.json, using default allowed extensions [pdf]\033[0m')

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = config.get('max_file_size_mb', 50) * 1024 * 1024  # 50MB max file size
# redoc = Redoc(app, 'doc.yml')  # Eliminado
cors = CORS(app, resources={r"/*":{'origins':"*"}})

# Configuración de directorios
UPLOAD_FOLDER = '/tmp/uploads'
COMPRESSED_FOLDER = '/tmp/compressed'
ALLOWED_EXTENSIONS = config.get('allowed_extensions', ['pdf'])

# Crear directorios si no existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)



def allowed_file(filename):
    """Verificar si el archivo tiene una extensión permitida"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def compress_pdf(input_path, output_path, level):
    """Comprimir PDF usando Ghostscript con diferentes niveles"""
    commands = {
        1: [
            'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/prepress', '-dNOPAUSE', '-dQUIET', '-dBATCH',
            '-sOutputFile=' + output_path, input_path
        ],
        2: [
            'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/ebook', '-dNOPAUSE', '-dQUIET', '-dBATCH',
            '-sOutputFile=' + output_path, input_path
        ],
        3: [
            'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/screen', '-dNOPAUSE', '-dQUIET', '-dBATCH',
            '-sOutputFile=' + output_path, input_path
        ]
    }
    
    if level not in commands:
        raise ValueError(f"Nivel de compresión {level} no válido. Use 1, 2 o 3.")
    
    try:
        result = subprocess.run(commands[level], capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            logger.error(f"Error en Ghostscript: {result.stderr}")
            raise Exception(f"Error al comprimir PDF: {result.stderr}")
        return True
    except subprocess.TimeoutExpired:
        raise Exception("Timeout al comprimir el PDF")
    except FileNotFoundError:
        raise Exception("Ghostscript no está instalado")

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud del servicio"""
    return jsonify({
        'status': 'healthy',
        'service': 'PDF Compressor',
        'version': '1.0.0'
    })

@app.route('/compress', methods=['POST'])
def compress_pdf_endpoint():
    """Endpoint para comprimir un archivo PDF"""
    try:
        # Verificar si se envió un archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No se proporcionó ningún archivo'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        # Verificar extensión del archivo
        if not allowed_file(file.filename):
            return jsonify({'error': 'Solo se permiten archivos PDF'}), 400
        
        # Obtener nivel de compresión
        level = request.form.get('level', '1')
        try:
            level = int(level)
            if level not in [1, 2, 3]:
                return jsonify({'error': 'Nivel debe ser 1, 2 o 3'}), 400
        except ValueError:
            return jsonify({'error': 'Nivel debe ser un número entero'}), 400
        
        # Generar nombres únicos para los archivos
        original_filename = secure_filename(file.filename)
        file_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_FOLDER, f"{file_id}_{original_filename}")
        output_filename = f"compressed_level_{level}_{original_filename}"
        output_path = os.path.join(COMPRESSED_FOLDER, f"{file_id}_{output_filename}")
        
        # Guardar archivo original
        file.save(input_path)
        logger.info(f"Archivo guardado: {input_path}")
        
        # Comprimir PDF
        compress_pdf(input_path, output_path, level)
        logger.info(f"PDF comprimido exitosamente: {output_path}")
        
        # Verificar que el archivo comprimido existe
        if not os.path.exists(output_path):
            return jsonify({'error': 'Error al generar archivo comprimido'}), 500
        
        # Obtener tamaños de archivo
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        compression_ratio = ((original_size - compressed_size) / original_size) * 100
        
        # Limpiar archivo original
        os.remove(input_path)
        
        return jsonify({
            'success': True,
            'message': f'PDF comprimido exitosamente con nivel {level}',
            'original_filename': original_filename,
            'compressed_filename': output_filename,
            'original_size_mb': round(original_size / (1024 * 1024), 2),
            'compressed_size_mb': round(compressed_size / (1024 * 1024), 2),
            'compression_ratio_percent': round(compression_ratio, 2),
            'file_id': file_id
        })
        
    except Exception as e:
        logger.error(f"Error en compresión: {str(e)}")
        return jsonify({'error': f'Error al procesar el archivo: {str(e)}'}), 500

@app.route('/download/<file_id>', methods=['GET'])
def download_compressed_file(file_id):
    """Endpoint para descargar archivo comprimido"""
    try:
        # Buscar archivo comprimido por file_id
        for filename in os.listdir(COMPRESSED_FOLDER):
            if filename.startswith(file_id):
                file_path = os.path.join(COMPRESSED_FOLDER, filename)
                return send_file(file_path, as_attachment=True, download_name=filename)
        
        return jsonify({'error': 'Archivo no encontrado'}), 404
        
    except Exception as e:
        logger.error(f"Error al descargar archivo: {str(e)}")
        return jsonify({'error': f'Error al descargar archivo: {str(e)}'}), 500

@app.route('/cleanup', methods=['POST'])
def cleanup_files():
    """Endpoint para limpiar archivos temporales (opcional)"""
    try:
        # Limpiar archivos comprimidos más antiguos de 1 hora
        import time
        current_time = time.time()
        cleaned_count = 0
        
        for filename in os.listdir(COMPRESSED_FOLDER):
            file_path = os.path.join(COMPRESSED_FOLDER, filename)
            if os.path.getctime(file_path) < (current_time - 3600):  # 1 hora
                os.remove(file_path)
                cleaned_count += 1
        
        return jsonify({
            'success': True,
            'message': f'Se limpiaron {cleaned_count} archivos temporales'
        })
        
    except Exception as e:
        logger.error(f"Error en limpieza: {str(e)}")
        return jsonify({'error': f'Error en limpieza: {str(e)}'}), 500

def cleanup_files_periodically():
    """Limpia archivos temporales cada 2 horas en segundo plano"""
    while True:
        try:
            logger.info("Limpieza automática de archivos temporales iniciada")
            current_time = time.time()
            cleaned_count = 0
            for filename in os.listdir(COMPRESSED_FOLDER):
                file_path = os.path.join(COMPRESSED_FOLDER, filename)
                if os.path.getctime(file_path) < (current_time - 3600):  # 1 hora
                    os.remove(file_path)
                    cleaned_count += 1
            if cleaned_count > 0:
                logger.info(f"Limpieza automática: Se limpiaron {cleaned_count} archivos temporales")
        except Exception as e:
            logger.error(f"Error en limpieza automática: {str(e)}")
        time.sleep(7200)  # Esperar 2 horas (ajusta a 7200 para producción)

# Lanzar el hilo de limpieza automática SIEMPRE, incluso bajo Gunicorn
cleanup_thread = threading.Thread(target=cleanup_files_periodically, daemon=True)
cleanup_thread.start()

@app.route('/openapi.yml')
def openapi_spec():
    return send_file('doc.yml', mimetype='text/yaml')

@app.route('/docs')
def redoc_ui():
    return '''
    <!DOCTYPE html>
    <html>
      <head>
        <title>API Docs</title>
        <meta charset="utf-8"/>
        <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"></script>
      </head>
      <body>
        <redoc spec-url='/openapi.yml'></redoc>
      </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config.get('port', 5000), debug=False)