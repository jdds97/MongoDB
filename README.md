# MongoDB Administration Scripts

Este repositorio contiene una colección de scripts de administración y consulta para MongoDB, diseñados para demostrar diferentes enfoques y técnicas de gestión de bases de datos MongoDB utilizando Python.

## Objetivo

El proyecto tiene como objetivo proporcionar ejemplos prácticos y herramientas para la administración de MongoDB, incluyendo:

- Conexiones y operaciones básicas de MongoDB
- Comparación entre diferentes clientes de Python (PyMongo vs MongoEngine)
- Gestión de datos (importación, exportación, backups)
- Consultas avanzadas y aggregation pipelines
- Ejemplos con datos reales para entrenamiento de IA (conversaciones de salud mental)

## Contexto

Los scripts están orientados a desarrolladores y administradores de bases de datos que desean:

- Aprender mejores prácticas en el manejo de MongoDB con Python
- Comparar el rendimiento entre diferentes librerías de MongoDB
- Implementar sistemas de backup y restauración
- Trabajar con datasets complejos y consultas avanzadas

## Estructura del Proyecto

```
MongoDB/
├── mongodb_connection.py     # Configuración de conexión a MongoDB Atlas
├── data.json                # Dataset de ejemplo (1000+ registros de usuarios)
├── consultas/               # Scripts de consultas y operaciones
│   ├── basic_operations.py  # Operaciones básicas (CRUD, gestión de colecciones)
│   ├── basic_queries.py     # Consultas avanzadas con MongoEngine
│   └── compare.py           # Comparación de rendimiento PyMongo vs MongoEngine
└── datos/                   # Herramientas de gestión de datos
    ├── insert_data.py       # Import/export con mongoimport, mongodump, mongorestore
    ├── data/               # Directorio para archivos de datos
    └── backup/             # Directorio para backups BSON
```

## Dependencias

```bash
pip install pymongo mongoengine
```

Para las herramientas de línea de comandos, también necesitarás tener instalado MongoDB Database Tools:
- `mongoimport`
- `mongodump` 
- `mongorestore`

## Configuración

1. **Configurar conexión**: Actualiza la URI de conexión en `mongodb_connection.py` con tus credenciales de MongoDB Atlas o instancia local.

2. **Preparar datos**: El archivo `data.json` contiene datos de ejemplo. Para trabajar con datos de salud mental, asegúrate de tener el archivo correspondiente en el directorio `datos/data/`.

## Uso

### Operaciones Básicas
```bash
cd consultas
python basic_operations.py
```
Ejecuta operaciones fundamentales como crear/eliminar colecciones y listar bases de datos.

### Consultas Avanzadas
```bash
python basic_queries.py
```
Demuestra consultas complejas usando MongoEngine con datos de conversaciones de IA.

### Comparación de Rendimiento
```bash
python compare.py
```
Compara el rendimiento entre PyMongo y MongoEngine en diferentes tipos de consultas.

### Gestión de Datos
```bash
cd datos
python insert_data.py
```
Herramientas para importar JSON a MongoDB, crear backups BSON y restaurar datos.

## Características Destacadas

- **Múltiples enfoques**: Ejemplos tanto con PyMongo (driver nativo) como MongoEngine (ODM)
- **Datos reales**: Utiliza datasets de conversaciones para entrenamiento de IA en salud mental
- **Herramientas de administración**: Scripts completos para backup, restauración e importación de datos
- **Medición de rendimiento**: Comparaciones cronometradas entre diferentes librerías
- **Consultas complejas**: Aggregation pipelines y consultas con filtros avanzados

## Contribuir

Este proyecto está diseñado con fines educativos y de demostración. Las contribuciones son bienvenidas para:

- Agregar nuevos ejemplos de consultas
- Mejorar la documentación
- Optimizar el rendimiento de los scripts
- Añadir nuevas herramientas de administración

## Notas de Seguridad

⚠️ **Importante**: Los archivos de conexión contienen credenciales. En un entorno de producción:
- Usa variables de entorno para las credenciales
- No commitees credenciales al repositorio
- Implementa autenticación adecuada
