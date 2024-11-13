from mongoengine import Document, StringField, ListField, connect
from pathlib import Path
import sys
from mongoengine import get_db
# Añade el directorio padre al path de Python
sys.path.append(str(Path(__file__).parent.parent))
connect(db='practica2', alias='default', host='mongodb+srv://jesusdediossanchez:Y2vwkp89iFv8d7qk@clusterjdds.pbckg.mongodb.net/?retryWrites=true&w=majority&appName=ClusterJdds')

from mongoengine import Document, StringField, ListField, DictField, EmbeddedDocument, EmbeddedDocumentField, ListField
connection_settings = connect(db='practica2', alias='default', host='mongodb+srv://jesusdediossanchez:Y2vwkp89iFv8d7qk@clusterjdds.pbckg.mongodb.net/?retryWrites=true&w=majority&appName=ClusterJdds')
db = get_db()

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
def demonstrate_basic_queries():
    try:
        # 1. Consulta simple
        print("\n=== Consulta Simple ===")
        greeting_doc = MentalHealthCollection.objects(intents__tag="greeting").first()
        if greeting_doc and greeting_doc.intents:
            intent = next((i for i in greeting_doc.intents if i.tag == "greeting"), None)
            if intent:
                print("Encontrado intent de tipo greeting:")
                print(f"Tag: {intent.tag}")
                print(f"Patrones: {intent.patterns}")
        
        # 2. Consulta con filtros
        print("\n=== Consulta con Filtros ===")
        help_docs = MentalHealthCollection.objects(intents__patterns__icontains="help")
        for doc in help_docs:
            help_intents = [i for i in doc.intents if any("help" in p.lower() for p in i.patterns)]
            for intent in help_intents:
                print(f"Tag: {intent.tag}")
                print(f"Patrones: {intent.patterns}\n")
           
        # 3. Consulta con filtros y ordenación
        print("\n=== Consulta con Filtros y Ordenación ===")
        sorted_help_docs = MentalHealthCollection.objects(intents__patterns__icontains="help").order_by('intents.tag')
        for doc in sorted_help_docs:
            help_intents = [i for i in doc.intents if any("help" in p.lower() for p in i.patterns)]
            for intent in help_intents:
                print(f"Tag: {intent.tag}")
                print(f"Patrones: {intent.patterns}\n")

        # 4. Consulta con filtros, ordenación y proyección
        print("\n=== Consulta con Filtros, Ordenación y Proyección ===")
        sorted_docs = MentalHealthCollection.objects(intents__tag__exists=True).order_by('intents.tag').only('intents.tag', 'intents.patterns')
        for doc in sorted_docs:
            for intent in doc.intents:
                print(f"Tag: {intent.tag}")
                print(f"Patrones: {intent.patterns}\n")
    
    except Exception as e:
        print(f"Error en consultas básicas: {e}")

def demonstrate_query_examples():
    try:
        print("\n=== Ejemplos Adicionales de Queries ===")
        
        # Ejemplo 1: Buscar documentos que cumplan múltiples condiciones
        print("\nIntenciones o propósitos para entrenamiento para la IA con respuestas largas y múltiples patrones:")
        complex_docs = MentalHealthCollection.objects.aggregate([
            {"$unwind": "$intents"},
            {"$match": {
                "intents.responses.0": {"$exists": True},
                "$expr": {"$gt": [{"$size": "$intents.patterns"}, 2]},
                "intents.responses": {"$elemMatch": {"$regex": ".{100,}"}}
            }},
            {"$project": {"tag": "$intents.tag"}}
        ])
        
        for doc in complex_docs:
            print(f"Tag: {doc['tag']}")
        
        # Ejemplo 2: Intenciones o propósitos para entrenamiento para la IA con más de 5 patrones
        print("\nIntenciones o propósitos para entrenamiento para la IA con más de 5 patrones:")
        many_patterns_docs = MentalHealthCollection.objects.aggregate([
            {"$unwind": "$intents"},
            {"$match": {
                "$expr": {"$gt": [{"$size": "$intents.patterns"}, 5]}
            }},
            {"$project": {
                "tag": "$intents.tag",
                "patterns": "$intents.patterns"
            }}
        ])
        
        for doc in many_patterns_docs:
            print(f"Tag: {doc['tag']}, Número de patrones: {len(doc['patterns'])}")

        # Ejemplo 3: Intenciones o propósitos con patrones que contienen una palabra específica
        print("\nIntenciones o propósitos para entrenamiento para la IA con patrones que contienen la palabra 'stress':")
        stress_docs = MentalHealthCollection.objects(intents__patterns__icontains="stress")
        for doc in stress_docs:
            stress_intents = [i for i in doc.intents if any("stress" in p.lower() for p in i.patterns)]
            for intent in stress_intents:
                print(f"Tag: {intent.tag}")
                print(f"Patrones: {intent.patterns}\n")

        
    
    except Exception as e:
        print(f"Error en consultas de ejemplo: {e}")



if __name__ == "__main__":
    try:
        print("Ejecutando queries básicas en MongoDB...")
        print(f"Usando base de datos: {db.name}")
        print(f"Número total de documentos: {MentalHealthCollection.objects.count()}")
        
        demonstrate_basic_queries()
        demonstrate_query_examples()
    
    except Exception as e:
        print(f"Error general: {e}")