#!/usr/bin/env python3
"""
Script de prueba para el servicio de compresión de PDF
"""

import requests
import os
import sys
import time

# Configuración
BASE_URL = "http://localhost:5000"
TEST_PDF_PATH = "test.pdf"  # Cambiar por la ruta de tu PDF de prueba

def test_health_check():
    """Probar el endpoint de health check"""
    print("🔍 Probando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check exitoso")
            print(f"   Respuesta: {response.json()}")
            return True
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servicio. ¿Está ejecutándose?")
        return False

def test_compress_pdf(level=1):
    """Probar la compresión de PDF"""
    if not os.path.exists(TEST_PDF_PATH):
        print(f"❌ Archivo de prueba no encontrado: {TEST_PDF_PATH}")
        print("   Por favor, coloca un archivo PDF llamado 'test.pdf' en el directorio actual")
        return False
    
    print(f"📄 Probando compresión con nivel {level}...")
    
    try:
        with open(TEST_PDF_PATH, 'rb') as f:
            files = {'file': (TEST_PDF_PATH, f, 'application/pdf')}
            data = {'level': str(level)}
            
            response = requests.post(f"{BASE_URL}/compress", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Compresión exitosa")
                print(f"   Archivo original: {result['original_filename']}")
                print(f"   Archivo comprimido: {result['compressed_filename']}")
                print(f"   Tamaño original: {result['original_size_mb']} MB")
                print(f"   Tamaño comprimido: {result['compressed_size_mb']} MB")
                print(f"   Ratio de compresión: {result['compression_ratio_percent']}%")
                print(f"   File ID: {result['file_id']}")
                return result['file_id']
            else:
                print(f"❌ Error en compresión: {response.status_code}")
                print(f"   Respuesta: {response.text}")
                return None
                
    except Exception as e:
        print(f"❌ Error al comprimir: {str(e)}")
        return None

def test_download(file_id):
    """Probar la descarga del archivo comprimido"""
    if not file_id:
        print("❌ No hay file_id para descargar")
        return False
    
    print(f"⬇️  Probando descarga del archivo {file_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/download/{file_id}")
        
        if response.status_code == 200:
            # Guardar el archivo descargado
            filename = f"downloaded_{file_id}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Archivo descargado exitosamente: {filename}")
            return True
        else:
            print(f"❌ Error al descargar: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en descarga: {str(e)}")
        return False

def test_cleanup():
    """Probar la limpieza de archivos temporales"""
    print("🧹 Probando limpieza de archivos temporales...")
    
    try:
        response = requests.post(f"{BASE_URL}/cleanup")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Limpieza exitosa")
            print(f"   {result['message']}")
            return True
        else:
            print(f"❌ Error en limpieza: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error en limpieza: {str(e)}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas del servicio de compresión de PDF")
    print("=" * 50)
    
    # Verificar que el servicio esté ejecutándose
    if not test_health_check():
        print("\n❌ El servicio no está disponible. Asegúrate de que esté ejecutándose.")
        print("   Comando para ejecutar: docker-compose up --build")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # Probar compresión con diferentes niveles
    for level in [1, 2, 3]:
        print(f"\n📊 Probando nivel de compresión {level}")
        file_id = test_compress_pdf(level)
        
        if file_id:
            # Probar descarga
            test_download(file_id)
        
        print("-" * 30)
    
    # Probar limpieza
    print("\n🧹 Probando limpieza de archivos")
    test_cleanup()
    
    print("\n" + "=" * 50)
    print("✅ Pruebas completadas")

if __name__ == "__main__":
    main() 