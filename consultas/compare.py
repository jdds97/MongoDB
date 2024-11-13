from mongoengine import Document, StringField, ListField, EmbeddedDocument, EmbeddedDocumentField, connect
from pathlib import Path
import sys
import time
from pymongo import MongoClient

sys.path.append(str(Path(__file__).parent.parent))
from config.mongodb_connection import get_database

# Configuración
db = get_database
connect(db='practica2', alias='default', host='mongodb+srv://jesusdediossanchez:Y2vwkp89iFv8d7qk@clusterjdds.pbckg.mongodb.net/?retryWrites=true&w=majority&appName=ClusterJdds')


# Modelos MongoEngine
class Intent(EmbeddedDocument):
    tag = StringField(required=True)
    patterns = ListField(StringField())
    responses = ListField(StringField())

class MentalHealthCollection(Document):
    intents = ListField(EmbeddedDocumentField(Intent))
    meta = {
        'collection': 'mental_health',
        'indexes': ['intents.tag']
    }

def compare_simple_queries():
    print("\n=== Comparación de Consultas Simples (Buscar greeting) ===")
    
    # PyMongo directo
    start_time = time.time()
    pymongo_doc = db.mental_health.find_one({"intents": {
        "$elemMatch": {"tag": "greeting"}
    }})
    pymongo_time = time.time() - start_time
    
    if pymongo_doc:
        greeting_intent = next((i for i in pymongo_doc['intents'] if i['tag'] == 'greeting'), None)
        print(f"PyMongo encontró greeting en {pymongo_time:.4f} segundos")
        print(f"Ejemplo PyMongo - Tag: {greeting_intent['tag']}")
    
    # MongoEngine
    start_time = time.time()
    mongoengine_doc = MentalHealthCollection.objects(intents__tag="greeting").first()
    mongoengine_time = time.time() - start_time
    
    if mongoengine_doc:
        intent = next((i for i in mongoengine_doc.intents if i.tag == "greeting"), None)
        print(f"\nMongoEngine encontró greeting en {mongoengine_time:.4f} segundos")
        print(f"Ejemplo MongoEngine - Tag: {intent.tag}")

def compare_filtered_queries():
    print("\n=== Comparación de Consultas con Filtros (Buscar 'help' en patterns) ===")
    
    # PyMongo directo
    start_time = time.time()
    pymongo_docs = db.mental_health.find({
        "intents": {
            "$elemMatch": {
                "patterns": {"$regex": "help", "$options": "i"}
            }
        }
    })
    pymongo_results = []
    for doc in pymongo_docs:
        help_intents = [i for i in doc['intents'] 
                       if any("help" in p.lower() for p in i['patterns'])]
        pymongo_results.extend(help_intents)
    pymongo_time = time.time() - start_time
    
    print(f"PyMongo encontró {len(pymongo_results)} resultados en {pymongo_time:.4f} segundos")
    
    # MongoEngine
    start_time = time.time()
    mongoengine_docs = MentalHealthCollection.objects(intents__patterns__icontains="help")
    mongoengine_results = []
    for doc in mongoengine_docs:
        help_intents = [i for i in doc.intents 
                       if any("help" in p.lower() for p in i.patterns)]
        mongoengine_results.extend(help_intents)
    mongoengine_time = time.time() - start_time
    
    print(f"MongoEngine encontró {len(mongoengine_results)} resultados en {mongoengine_time:.4f} segundos")

def compare_complex_queries():
    print("\n=== Comparación de Consultas Complejas (Intents con más de 5 patrones) ===")
    
    # PyMongo directo
    start_time = time.time()
    pymongo_results = list(db.mental_health.aggregate([
        {"$unwind": "$intents"},
        {"$match": {
            "$expr": {"$gt": [{"$size": "$intents.patterns"}, 5]}
        }},
        {"$project": {
            "tag": "$intents.tag",
            "patterns": "$intents.patterns"
        }}
    ]))
    pymongo_time = time.time() - start_time
    
    print(f"PyMongo procesó la agregación en {pymongo_time:.4f} segundos")
    print(f"Encontró {len(pymongo_results)} intents")
    
    # MongoEngine
    start_time = time.time()
    mongoengine_results = list(MentalHealthCollection.objects.aggregate([
        {"$unwind": "$intents"},
        {"$match": {
            "$expr": {"$gt": [{"$size": "$intents.patterns"}, 5]}
        }},
        {"$project": {
            "tag": "$intents.tag",
            "patterns": "$intents.patterns"
        }}
    ]))
    mongoengine_time = time.time() - start_time
    
    print(f"MongoEngine procesó la agregación en {mongoengine_time:.4f} segundos")
    print(f"Encontró {len(mongoengine_results)} intents")

if __name__ == "__main__":
    try:
        print(f"Usando base de datos: {db.name}")
        compare_simple_queries()
        compare_filtered_queries()
        compare_complex_queries()
    except Exception as e:
        print(f"Error: {e}")