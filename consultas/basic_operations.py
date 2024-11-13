from pathlib import Path
import sys

# Añade el directorio padre al path de Python (una sola línea)
sys.path.append(str(Path(__file__).parent.parent))

from config.mongodb_connection import get_database

def demonstrate_basic_operations():
    db = get_database
    
    # 1. Listar bases de datos
    print("Bases de datos disponibles:")
    for db_name in db.client.list_database_names():
        print(f"- {db_name}")
    
    # 2. Listar colecciones
    print("\nColecciones en la base de datos:")
    for collection in db.list_collection_names():
        print(f"- {collection}")
    
    # 3. Crear colección
    db.create_collection("new_collection")
    print("\nColección creada")
    
    
    # 4. Eliminar colección
    db.new_collection.drop()
    print("\nColección eliminada")
    
    # 5. Listar colecciones después del eliminado
    print("\nColecciones en la base de datos:")
    for collection in db.list_collection_names():
        print(f"- {collection}")
    

if __name__ == "__main__":
    demonstrate_basic_operations()