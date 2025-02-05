import json
import sqlite3
import logging
from kafka import KafkaConsumer

# Configuration Kafka et base de données
KAFKA_BROKER = 'kafka:9092'
TOPIC = 'tmdb_movies'
DATABASE = '/app/data/movies.db'

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Initialisation de la base de données
def init_db():
    try:
        logging.info(f"Connexion à la base de données : {DATABASE}")
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            logging.info("Connexion réussie. Création de la table si elle n'existe pas...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY, -- PRIMARY KEY garantit l'unicité
                    title TEXT,
                    overview TEXT,
                    release_date TEXT,
                    popularity REAL,
                    vote_average REAL,
                    vote_count INTEGER
                )
            ''')
            conn.commit()
            logging.info("Table 'movies' créée ou déjà existante.")
    except sqlite3.Error as e:
        logging.error(f"Erreur lors de la création de la table 'movies' : {e}")

# Fonction pour insérer les données des films dans la base de données
def store_movie_data(movie):
    try:
        logging.info(f"Traitement des données du film : {movie}")
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # Vérifie si le film existe déjà
            cursor.execute('SELECT id FROM movies WHERE id = ?', (movie['id'],))
            if cursor.fetchone():
                logging.info(f"Le film avec l'ID {movie['id']} existe déjà dans la base de données.")
                return  # Ne pas insérer de doublon
            
            # Insère les données si le film n'existe pas
            cursor.execute('''
                INSERT INTO movies (id, title, overview, release_date, popularity, vote_average, vote_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                movie['id'],
                movie['title'],
                movie['overview'],
                movie.get('release_date', 'N/A'),
                movie.get('popularity', 0.0),
                movie.get('vote_average', 0.0),
                movie.get('vote_count', 0)
            ))
            conn.commit()
            logging.info(f"Données insérées dans la base de données pour le film : {movie['title']}")
    except sqlite3.Error as e:
        logging.error(f"Erreur lors de l'insertion dans la base de données : {e}")
    except KeyError as e:
        logging.error(f"Clé manquante dans les données du film : {e}")

# Initialisation du consommateur Kafka
def consume_kafka_messages():
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            group_id='tmdb_group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest'
        )
        logging.info(f"Démarrage du consommateur Kafka sur le topic '{TOPIC}'...")
        for message in consumer:
            try:
                logging.info(f"Données reçues : {message.value}")
                store_movie_data(message.value)
            except Exception as e:
                logging.error(f"Erreur lors du traitement du message Kafka : {e}")
    except Exception as e:
        logging.error(f"Erreur avec le consommateur Kafka : {e}")

# Point d'entrée principal
if __name__ == "__main__":
    init_db()
    consume_kafka_messages()
