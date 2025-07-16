#!/usr/bin/env python3
"""
Gestor del contexto del proyecto PDF Compressor
Permite leer y actualizar automáticamente el project_context.json
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

class ProjectContextManager:
    def __init__(self, context_file: str = "project_context.json"):
        self.context_file = context_file
        self.context = None
    
    def load_context(self) -> Dict[str, Any]:
        """Cargar el contexto del proyecto desde el archivo JSON"""
        try:
            if os.path.exists(self.context_file):
                with open(self.context_file, 'r', encoding='utf-8') as f:
                    self.context = json.load(f)
                    print(f"✅ Contexto del proyecto cargado: {self.context.get('project_name', 'PDF Compressor')}")
                    print(f"   Versión: {self.context.get('version', 'N/A')}")
                    print(f"   Última actualización: {self.context.get('last_updated', 'N/A')}")
                    return self.context
            else:
                print(f"❌ Archivo de contexto no encontrado: {self.context_file}")
                return {}
        except Exception as e:
            print(f"❌ Error al cargar el contexto: {str(e)}")
            return {}
    
    def update_context(self, updates: Dict[str, Any]) -> bool:
        """Actualizar el contexto del proyecto con nuevos datos"""
        try:
            # Cargar contexto actual si no está cargado
            if self.context is None:
                self.load_context()
            
            # Verificar que el contexto se cargó correctamente
            if self.context is None:
                print("❌ No se pudo cargar el contexto del proyecto")
                return False
            
            # Aplicar actualizaciones
            self._merge_updates(self.context, updates)
            
            # Actualizar timestamp
            self.context['last_updated'] = datetime.now().isoformat() + 'Z'
            
            # Guardar en archivo
            with open(self.context_file, 'w', encoding='utf-8') as f:
                json.dump(self.context, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Contexto del proyecto actualizado: {self.context_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error al actualizar el contexto: {str(e)}")
            return False
    
    def _merge_updates(self, target: Dict[str, Any], updates: Dict[str, Any]):
        """Fusionar actualizaciones en el contexto existente"""
        for key, value in updates.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._merge_updates(target[key], value)
            else:
                target[key] = value
    
    def get_project_summary(self) -> str:
        """Obtener un resumen del proyecto"""
        if self.context is None:
            self.load_context()
        
        if not self.context:
            return "No hay contexto del proyecto disponible"
        
        summary = f"""
📋 RESUMEN DEL PROYECTO: {self.context.get('project_name', 'PDF Compressor')}

🏗️  ARQUITECTURA:
   - Tipo: {self.context.get('architecture', {}).get('type', 'N/A')}
   - Framework: {self.context.get('technology_stack', {}).get('framework', 'N/A')}
   - Backend: {self.context.get('technology_stack', {}).get('backend', 'N/A')}

📊 NIVELES DE COMPRESIÓN:
"""
        
        compression_levels = self.context.get('compression_levels', {})
        for level, config in compression_levels.items():
            summary += f"   - {level.replace('_', ' ').title()}: {config.get('name', 'N/A')} ({config.get('quality', 'N/A')})\n"
        
        summary += f"""
🔗 ENDPOINTS API:
"""
        endpoints = self.context.get('api_endpoints', {})
        for name, endpoint in endpoints.items():
            summary += f"   - {endpoint.get('method', 'N/A')} {endpoint.get('path', 'N/A')}: {endpoint.get('description', 'N/A')}\n"
        
        summary += f"""
📁 ARCHIVOS PRINCIPALES:
"""
        files = self.context.get('file_structure', {})
        for filename, file_info in files.items():
            summary += f"   - {filename}: {file_info.get('description', 'N/A')}\n"
        
        summary += f"""
🚀 DESPLIEGUE:
   - Docker Compose: docker-compose up --build
   - Puerto: 5000
   - Health Check: GET /health
"""
        
        return summary
    
    def update_file_info(self, filename: str, info: Dict[str, Any]):
        """Actualizar información de un archivo específico"""
        if self.context is None:
            self.load_context()
        
        if self.context is None:
            print("❌ No se pudo cargar el contexto del proyecto")
            return
        
        if 'file_structure' not in self.context:
            self.context['file_structure'] = {}
        
        self.context['file_structure'][filename] = info
        self.update_context({})
    
    def add_endpoint(self, name: str, endpoint_info: Dict[str, Any]):
        """Agregar o actualizar un endpoint de la API"""
        if self.context is None:
            self.load_context()
        
        if self.context is None:
            print("❌ No se pudo cargar el contexto del proyecto")
            return
        
        if 'api_endpoints' not in self.context:
            self.context['api_endpoints'] = {}
        
        self.context['api_endpoints'][name] = endpoint_info
        self.update_context({})
    
    def update_compression_level(self, level: int, config: Dict[str, Any]):
        """Actualizar configuración de un nivel de compresión"""
        if self.context is None:
            self.load_context()
        
        if self.context is None:
            print("❌ No se pudo cargar el contexto del proyecto")
            return
        
        level_key = f"level_{level}"
        if 'compression_levels' not in self.context:
            self.context['compression_levels'] = {}
        
        self.context['compression_levels'][level_key] = config
        self.update_context({})

def main():
    """Función principal para pruebas"""
    manager = ProjectContextManager()
    
    # Cargar contexto
    context = manager.load_context()
    
    if context:
        # Mostrar resumen
        print(manager.get_project_summary())
        
        # Ejemplo de actualización
        print("\n🔄 Actualizando contexto...")
        manager.update_context({
            "development_notes": {
                "last_test_run": datetime.now().isoformat(),
                "test_status": "passed"
            }
        })
    else:
        print("❌ No se pudo cargar el contexto del proyecto")

if __name__ == "__main__":
    main() 