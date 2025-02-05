FROM python:3.9-slim

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    && apt-get clean

# Copier les fichiers et installer les dépendances Python
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Point d'entrée
CMD ["airflow", "webserver", "--port", "8080"]
