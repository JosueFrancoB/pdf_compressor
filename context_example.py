#!/usr/bin/env python3
"""
Ejemplo de uso del gestor de contexto del proyecto PDF Compressor
"""

from project_manager import ProjectContextManager
from datetime import datetime

def example_usage():
    """Ejemplo de cómo usar el gestor de contexto"""
    
    # Crear instancia del gestor
    manager = ProjectContextManager()
    
    print("🚀 EJEMPLO DE USO DEL GESTOR DE CONTEXTO")
    print("=" * 50)
    
    # 1. Cargar contexto existente
    print("\n1️⃣  Cargando contexto del proyecto...")
    context = manager.load_context()
    
    if not context:
        print("❌ No se pudo cargar el contexto")
        return
    
    # 2. Mostrar resumen del proyecto
    print("\n2️⃣  Resumen del proyecto:")
    print(manager.get_project_summary())
    
    # 3. Actualizar información de un archivo
    print("\n3️⃣  Actualizando información de archivo...")
    manager.update_file_info("app.py", {
        "description": "Aplicación Flask principal (actualizada)",
        "size": "6.8KB",
        "lines": 181,
        "last_modified": datetime.now().isoformat(),
        "status": "active"
    })
    
    # 4. Agregar un nuevo endpoint
    print("\n4️⃣  Agregando nuevo endpoint...")
    manager.add_endpoint("status", {
        "method": "GET",
        "path": "/status",
        "description": "Obtener estado detallado del servicio",
        "response": {
            "service_status": "running",
            "compression_queue": 0,
            "active_workers": 2
        }
    })
    
    # 5. Actualizar configuración de compresión
    print("\n5️⃣  Actualizando configuración de compresión...")
    manager.update_compression_level(1, {
        "name": "Prepress (Actualizado)",
        "settings": "/prepress",
        "quality": "Very High",
        "compression": "Moderate",
        "use_case": "High-quality printing",
        "last_tested": datetime.now().isoformat(),
        "success_rate": "99.5%"
    })
    
    # 6. Actualizar información general del proyecto
    print("\n6️⃣  Actualizando información general...")
    manager.update_context({
        "development_notes": {
            "last_development_session": datetime.now().isoformat(),
            "current_focus": "Context management system",
            "next_milestone": "Add authentication",
            "known_issues": [
                "Linter errors in project_manager.py (resolved)",
                "Need to add more comprehensive tests"
            ]
        },
        "statistics": {
            "total_endpoints": len(context.get('api_endpoints', {})),
            "total_files": len(context.get('file_structure', {})),
            "compression_levels": len(context.get('compression_levels', {})),
            "last_context_update": datetime.now().isoformat()
        }
    })
    
    print("\n✅ Ejemplo completado!")
    print("📝 El archivo project_context.json ha sido actualizado automáticamente")

def demonstrate_context_reading():
    """Demostrar cómo leer el contexto en futuras sesiones"""
    
    print("\n📖 DEMOSTRACIÓN DE LECTURA DE CONTEXTO")
    print("=" * 50)
    
    manager = ProjectContextManager()
    context = manager.load_context()
    
    if context:
        print("✅ Contexto cargado exitosamente")
        print(f"📋 Proyecto: {context.get('project_name')}")
        print(f"🏷️  Versión: {context.get('version')}")
        print(f"🕒 Última actualización: {context.get('last_updated')}")
        
        # Mostrar estadísticas recientes
        stats = context.get('statistics', {})
        if stats:
            print(f"📊 Estadísticas:")
            print(f"   - Endpoints: {stats.get('total_endpoints', 0)}")
            print(f"   - Archivos: {stats.get('total_files', 0)}")
            print(f"   - Niveles de compresión: {stats.get('compression_levels', 0)}")
        
        # Mostrar notas de desarrollo
        dev_notes = context.get('development_notes', {})
        if dev_notes:
            print(f"📝 Notas de desarrollo:")
            print(f"   - Enfoque actual: {dev_notes.get('current_focus', 'N/A')}")
            print(f"   - Próximo hito: {dev_notes.get('next_milestone', 'N/A')}")
    else:
        print("❌ No se pudo cargar el contexto")

if __name__ == "__main__":
    # Ejecutar ejemplo de uso
    example_usage()
    
    # Demostrar lectura de contexto
    demonstrate_context_reading()
    
    print("\n🎯 INSTRUCCIONES PARA FUTURAS SESIONES:")
    print("=" * 50)
    print("Cuando digas 'continuar proyecto', el sistema:")
    print("1. 📖 Leerá automáticamente project_context.json")
    print("2. 📋 Mostrará el resumen del proyecto")
    print("3. 🔄 Actualizará el contexto con cualquier cambio")
    print("4. 💾 Guardará automáticamente las actualizaciones")
    print("\n💡 Comando para probar: 'continuar proyecto'") 