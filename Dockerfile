# Usar imagen base de Python
FROM python:3.11-slim

# Instalar Ghostscript y otras dependencias del sistema
RUN apt-get update && apt-get install -y \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación y config.json y doc.yml
COPY app.py .
COPY config.json .
COPY doc.yml .

# Crear directorios necesarios
RUN mkdir -p /tmp/uploads /tmp/compressed

# Exponer puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"] 