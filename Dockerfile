# Utiliser une image Python officielle légère
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances (celui à la racine)
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code du projet dans le conteneur
COPY . .

# Définir la variable d'environnement pour que Python trouve le package weather_cli
ENV PYTHONPATH=/app

# Commande par défaut pour lancer l'application
CMD ["python", "-m", "weather_cli"]
