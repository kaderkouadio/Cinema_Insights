# Utilise une image précise de Python 3.11.5
FROM python:3.11.5-slim

# Empêche Python d’écrire des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Force l'affichage des logs en temps réel
ENV PYTHONUNBUFFERED=1


# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie le fichier des dépendances dans le conteneur
COPY requirements.txt .

# Met à jour pip et Installe les dépendances Python sans mise en cache
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# Copie tous les fichiers .py et le fichier .db dans le conteneur
COPY . .

# Lance le serveur Uvicorn pour exécuter l'API FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]


