# **Projet Kafka - Streaming et Traitement des Données de Films**

## 📌 **Description**
Ce projet met en place une architecture de streaming de données avec **Apache Kafka** pour la collecte et le traitement des films obtenus depuis l’API **IMDb (The Movie Database)**.  
Les données sont produites par un **Kafka Producer**, consommées par un **Kafka Consumer** et stockées dans une base de données **SQLite**.  
Un serveur **Flask** permet d’interagir avec ces données.

## 💁 **Architecture**
Le projet est structuré en plusieurs services :

1. **Kafka Producer** : Récupère les données de films via l’API TMDb et les envoie à Kafka.
2. **Kafka Consumer** : Lit les données de Kafka et les stocke dans une base de données.
3. **Base de données SQLite** : Stocke les informations des films.
4. **Flask Web App** : Fournit une interface pour interroger les données stockées.
5. **Zookeeper & Kafka** : Infrastructures nécessaires pour Kafka.

---

## 🚀 **Installation et Exécution**

### **1️⃣ Prérequis**
- Docker & Docker Compose
- Python 3.8+ (si exécution en local)

### **2️⃣ Cloner le dépôt**
```bash
git clone https://github.com/MounjidAmine/Kafka_IMDB.git
cd Kafka_IMDB
```

### **3️⃣ Construire et Lancer les Conteneurs**
```bash
docker-compose up --build
```
Cela va :
- Démarrer **Zookeeper** et **Kafka**.
- Construire et lancer **Flask**, **Kafka Producer** et **Kafka Consumer**.

---

## ⚙️ **Détails Techniques**

### **Kafka Producer**
- Situé dans `kafka_producer.py`.
- Se connecte à **IMDb API**.
- Envoie les films sous forme de messages JSON dans le topic Kafka `tmdb_movies`.

### **Kafka Consumer**
- Situé dans `kafka_consumer.py`.
- Écoute les messages du topic `tmdb_movies`.
- Stocke les films dans une base **SQLite** (`movies.db`).

### **Flask Web App**
- Fournit une API REST pour récupérer les films stockés.
- Accessible sur **http://localhost:5000**.

---

## 🛠 **Configurations**
Les paramètres sont définis dans `kafka_config.py` :
```python
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'tmdb_movies'
DATABASE = '/app/data/movies.db'
```

---

## 🛠️ **Dépendances**
Les dépendances sont listées dans `requirements.txt` :
```txt
Flask==2.2.5
kafka-python==2.0.2
requests==2.26.0
pandas
```

---

## 🏗 **Améliorations Futures**
- Ajouter une interface web pour afficher les films.
- Déployer sur **Kubernetes**.
- Stocker les données dans **PostgreSQL** au lieu de SQLite.

---

## 📝 **Auteur**
- **Amine Mounjid**  

