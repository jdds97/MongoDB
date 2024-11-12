import subprocess
import os
from datetime import datetime

class MongoDBTools:
    def __init__(self):
        self.data_dir = "data"
        self.backup_dir = "backup"
        self.ensure_directories()

    def ensure_directories(self):
        """Crear directorios necesarios"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

    def import_json_to_mongodb(self, uri):
        """Importar JSON a MongoDB"""
        json_path = os.path.join(self.data_dir, "mental_health_conversation.json")
        
        print("\n1. Importando JSON a MongoDB...")
        command = [
            "mongoimport",
            f"--uri={uri}",
            "--db=practica2",
            "--collection=mental_health",
            f"--file={json_path}",
            "--jsonArray",
            "--drop"
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Datos importados exitosamente a MongoDB")
        else:
            print(f"Error al importar datos: {result.stderr}")
            return False
        return True

    def create_bson_backup(self, uri):
        """Crear backup en formato BSON usando mongodump"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(self.backup_dir, timestamp)
        
        print("\n2. Creando backup BSON...")
        command = [
            "mongodump",
            f"--uri={uri}",
            "--db=practica2",
            "--collection=mental_health",
            f"--out={backup_path}"
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            bson_path = os.path.join(backup_path, "practica2", "mental_health.bson")
            print(f"✓ Backup BSON creado en: {bson_path}")
            return bson_path
        else:
            print(f"Error al crear backup: {result.stderr}")
            return None

    def restore_from_bson(self, uri, bson_path):
        """Restaurar datos desde backup BSON"""
        if not bson_path or not os.path.exists(bson_path):
            print("No se encontró el archivo BSON para restaurar")
            return False

        print("\n3. Restaurando datos desde BSON...")
        command = [
            "mongorestore",
            f"--uri={uri}",
            "--db=practica2",
            "--collection=mental_health",
            bson_path,
            "--drop"
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Datos restaurados exitosamente desde BSON")
            return True
        else:
            print(f"Error al restaurar datos: {result.stderr}")
            return False

def main():
    # URI de conexión a MongoDB
    uri = "mongodb+srv://jesusdediossanchez:Y2vwkp89iFv8d7qk@clusterjdds.pbckg.mongodb.net/?retryWrites=true&w=majority&appName=ClusterJdds"
    
    # Crear instancia de las herramientas
    tools = MongoDBTools()
    
    print("=== Iniciando proceso de gestión de datos ===")
    
    # 1. Importar JSON a MongoDB
    if not tools.import_json_to_mongodb(uri):
        return
    
    # 2. Crear backup en BSON
    bson_path = tools.create_bson_backup(uri)
    if not bson_path:
        return
    
    # 3. Restaurar desde BSON (para verificar)
    tools.restore_from_bson(uri, bson_path)
    
    print("\n=== Proceso completado exitosamente ===")

if __name__ == "__main__":
    main()