import json
import time
import requests
from kafka import KafkaProducer
import logging

# Configuration Kafka
KAFKA_BROKER = 'kafka:9092'
TOPIC = 'tmdb_movies'

# Configuration de l'API TMDb
API_DISCOVER_URL = "https://api.themoviedb.org/3/discover/movie"
BEARER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiOGEwYjQ0NmI2MTRkYWFhZjNiNjNjNjJkYmY4NjA1YyIsIm5iZiI6MTczNTY0MDMyNy4xNjMsInN1YiI6IjY3NzNjNTA3Y2ZlNjI2NDRkZjEzNTFjMiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Wg3LZLBDaeXmHO-w66zqN2FpAjh4tXLC3L9M1Cf12UU"

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Initialisation du producteur Kafka
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Fonction pour récupérer les films d'une page spécifique
def fetch_movies_from_page(page):
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {"page": page}
    try:
        response = requests.get(API_DISCOVER_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la récupération de la page {page}: {e}")
        return None

# Fonction principale pour parcourir toutes les pages et envoyer les données à Kafka
if __name__ == "__main__":
    logging.info("Démarrage du producteur Kafka pour TMDb...")
    try:
        page = 1
        while True:  # Parcourt les pages tant qu'il y a des résultats
            logging.info(f"Récupération des films de la page {page}...")
            movies_data = fetch_movies_from_page(page)
            if movies_data and "results" in movies_data:
                movies = movies_data["results"]
                for movie in movies:
                    producer.send(TOPIC, movie)
                    logging.info(f"Données envoyées pour le film : {movie['title']}")
                # Vérifier s'il reste d'autres pages
                if page >= movies_data.get("total_pages", 1):
                    logging.info("Toutes les pages ont été parcourues.")
                    break
                page += 1
                time.sleep(1)  # Pause pour éviter de surcharger l'API
            else:
                logging.info(f"Aucune donnée trouvée pour la page {page}. Arrêt.")
                break
    except KeyboardInterrupt:
        logging.info("Arrêt du producteur Kafka.")
    finally:
        producer.close()
