from mongodb_connection import get_database

def demonstrate_basic_operations():
    db = get_database()
    
    # 1. Listar bases de datos
    print("Bases de datos disponibles:")
    for db_name in db.client.list_database_names():
        print(f"- {db_name}")
    
    # 2. Crear colección
    db.create_collection("new_collection")
    print("\nColección creada")
    
    # 3. Listar colecciones
    print("\nColecciones en la base de datos:")
    for collection in db.list_collection_names():
        print(f"- {collection}")
    
    # 4. Eliminar colección
    db.new_collection.drop()
    print("\nColección eliminada")

if __name__ == "__main__":
    demonstrate_basic_operations()