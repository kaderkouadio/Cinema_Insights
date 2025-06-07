# Cinema_Insights : Développement Backend avec Python, FastAPI et SQLite

Bienvenue dans **Cinema_Insights**, une solution backend robuste conçue pour transformer l'expérience des données cinématographiques. Ce projet illustre la création d'une API moderne et évolutive pour centraliser et fournir des données sur les films, en utilisant des outils et pratiques de pointe en développement Python.

---

## Aperçu du Projet

**Cinema_Insights** est un système backend complet développé pour **CineData Insights**, une entreprise fictive visant à révolutionner l'accès et l'analyse des données cinématographiques. Basé sur le jeu de données **MovieLens**, ce projet propose une API performante pour les plateformes de streaming, les cinéphiles et les studios de production. Il répond au défi des données désorganisées en créant une base de données centralisée et interrogeable, accessible via une API RESTful.

### Objectifs Clés
- **Centraliser les Données MovieLens** : Transformer des fichiers CSV bruts en une base de données SQLite structurée.
- **Construire une API Évolutive** : Développer une API RESTful avec **FastAPI** pour un accès fluide aux données.
- **Créer un SDK Python** : Fournir un SDK intuitif (`cinelytics_sdk`) pour interagir facilement avec l'API, publié sur **PyPI**.
- **Déploiement Cloud** : Héberger l'API sur **Render** pour une accessibilité mondiale et démontrer une conteneurisation avec **Docker** pour un déploiement local.

---

## Technologies Utilisées

Ce projet met en avant une maîtrise des outils modernes de développement backend et d'ingénierie des données :

- **Python** : Langage principal pour le développement de l'API et du SDK.
- **FastAPI** : Framework performant pour créer des API RESTful avec documentation automatique Swagger/ReDoc.
- **SQLAlchemy** : ORM pour des interactions efficaces avec la base de données.
- **Pydantic** : Validation et sérialisation des données pour des réponses API robustes.
- **SQLite** : Base de données relationnelle légère pour stocker les données des films.
- **Docker** : Conteneurisation pour des déploiements portables et reproductibles.
- **Render** : Plateforme cloud pour héberger l'API sans coût.
- **PyPI** : Distribution du SDK Python pour une accessibilité mondiale.
- **HTTpx** : Client HTTP asynchrone pour les communications du SDK avec l'API.

---

## Phase 1 : Développement Backend & Architecture API

### 1. Conception de la Base de Données
- **Modélisation d'une Base Relationnelle** : Création d'une base SQLite pour stocker les données MovieLens (films, évaluations, tags, liens).
- **Schéma de la Base** :
  - **Movies** : Stocke les métadonnées des films (`movieId`, `title`, `genres`).
  - **Ratings** : Enregistre les évaluations des utilisateurs (`userId`, `movieId`, `rating`, `timestamp`).
  - **Tags** : Suit les tags attribués par les utilisateurs (`userId`, `movieId`, `tag`, `timestamp`).
  - **Links** : Associe les films à des identifiants externes (`movieId`, `imdbId`, `tmdbId`).
- **Contraintes** : Intégrité des données assurée par des clés primaires, clés étrangères et vérifications (ex. : notes entre 0.5 et 5.0).
- **Importation des Données** : Chargement des fichiers CSV dans les tables SQLite via des scripts Python.

### 2. Développement de l'API avec FastAPI
- **Points de Terminaison RESTful** :
  - `GET /movies/{movie_id}` : Récupérer les détails d’un film spécifique.
  - `GET /movies` : Lister les films avec pagination et filtres optionnels (`title`, `genre`).
  - `GET /ratings/{user_id}/{movie_id}` : Obtenir l’évaluation d’un utilisateur pour un film.
  - `GET /ratings` : Lister les évaluations avec filtres (`movie_id`, `user_id`, `min_rating`).
  - `GET /tags`, `GET /links`, `GET /analytics` : Récupérer les tags, liens externes et statistiques de la base.
- **Validation des Données** : Utilisation de modèles **Pydantic** pour garantir la robustesse des entrées/sorties.
- **Documentation** : Documentation interactive auto-générée via Swagger UI (`/docs`) et ReDoc (`/redoc`).
- **Gestion des Erreurs** : Réponses HTTP claires (ex. : 404 pour ressources manquantes, 422 pour entrées invalides).

### 3. Développement du SDK
- **SDK Python (`cinelytics_sdk`)** : Package convivial pour interagir avec l’API.
- **Fonctionnalités Clés** :
  - Appels simplifiés pour récupérer films, évaluations, tags et analyses.
  - Formats de sortie flexibles : objets Pydantic, dictionnaires ou **pandas DataFrames** pour les analystes de données.
  - Configurable via des variables d’environnement (ex. : URL de base de l’API).
- **Publié sur PyPI** : Accessible mondialement via `pip install cinelytics_sdk`.
- **Documentation** : README détaillé avec exemples d’utilisation.

### 4. Déploiement
- **Déploiement Cloud** : Hébergement gratuit de l’API sur **Render**, accessible via `https://cinema-insights.onrender.com`.
- **Conteneurisation Docker** : Création d’un `Dockerfile` pour un déploiement local, garantissant portabilité et cohérence.
- **Prêt pour CI/CD** : Intégration avec GitHub pour le contrôle de version et les pipelines de déploiement automatisés.

---

## Comment Démarrer

### Prérequis
- Python 3.11+
- SQLite
- Docker (optionnel pour un déploiement conteneurisé)
- Compte GitHub (pour l’hébergement du code)
- Compte Render (pour le déploiement cloud, sans carte bancaire)

### Installation
1. **Cloner le Répertoire** :
   ```bash
   cd cinema-insights
   ```

2. **Configurer un Environnement Virtuel** :
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Installer les Dépendances** :
   ```bash
   pip install -r api/requirements.txt
   ```

4. **Lancer l’API Localement** :
   ```bash
   uvicorn api.main:app --host 0.0.0.0 --port 8000
   ```
   Accédez à l’API via `http://localhost:8000/docs`.

### Utilisation du SDK
1. **Installer le SDK** :
   ```bash
   pip install cinelytics_sdk
   ```

2. **Exemple d’Utilisation** :
   ```python
   from cinelytics_sdk import MovieClient, MovieConfig
   import pandas as pd

   # Initialiser le client
   config = MovieConfig(movie_base_url="https://cinema-insights.onrender.com")
   client = MovieClient(config=config)

   # Vérifier la santé de l’API
   print(client.health_check())

   # Récupérer un film spécifique
   movie = client.get_movie(1)
   print(f"Film : {movie.title}")

   # Lister les films au format pandas DataFrame
   movies_df = client.list_movies(limit=5, output_format="pandas")
   print(movies_df)

   # Obtenir les statistiques
   analytics = client.get_analytics()
   print(f"Nombre total de films : {analytics.movie_count}")
   ```

### Déploiement
- **Cloud (Render)** :
  1. Poussez votre code sur un répertoire GitHub.
  2. Créez un nouveau service Web sur Render, connectez votre répertoire GitHub et configurez :
     - Langage : `Python 3`
     - Commande de Build : `pip install -r requirements.txt`
     - Commande de Démarrage : `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - Type d’Instance : `Free`
  3. Déployez et accédez à l’API via `https://cinema-insights.onrender.com`.

- **Docker** :
  ```bash
  docker build -t cinema-insights-api .
  docker run -d -p 80:80 --name cinema-insights-container cinema-insights-api
  ```
  Accédez via `http://localhost/docs`.

---

## Réalisations Clés
- **Développement de Bout en Bout** : Conception, construction et déploiement d’un système backend prêt pour la production.
- **Outils Modernes** : Utilisation de FastAPI, SQLAlchemy, Pydantic et Docker pour une architecture évolutive.
- **Approche Centrée sur les Données** : Centralisation et structuration des données pour des requêtes efficaces.
- **SDK Convivial** : Simplification de l’utilisation de l’API avec un package Python publié.
- **Déploiement Professionnel** : Démonstration de workflows de déploiement cloud et conteneurisé.

---

## Pourquoi Ce Projet Se Démarque
Ce projet témoigne de ma capacité à livrer une **solution backend complète et prête pour la production**. Il met en avant :
- **Expertise Technique** : Maîtrise de Python, conception d’API, gestion de bases de données et pratiques modernes de déploiement.
- **Résolution de Problèmes** : Transformation de données désorganisées en un système structuré et interrogeable.
- **Orientation Utilisateur** : Création d’outils (SDK) adaptés aux analystes de données et développeurs.
- **Impact sur le Portfolio** : Un projet soigné et déployable, prêt à être présenté à des recruteurs et clients.

---

## Améliorations Futures
- **Phase 2** : Créer un tableau de bord interactif avec **Streamlit** pour la visualisation et l’analyse exploratoire.
- **Authentification** : Ajouter une authentification basée sur JWT pour sécuriser l’accès à l’API.
- **Analyse Avancée** : Intégrer des modèles de machine learning pour des recommandations de films.
- **Évolutivité** : Optimiser pour un trafic élevé avec mise en cache (ex. : Redis) et indexation de la base.

---

## Liens Utiles
- 🌍 **API (Render)** : [https://cinema-insights.onrender.com](https://cinema-insights.onrender.com)
- 📦 **PyPI** : [https://pypi.org/project/cinelytics_sdk](https://pypi.org/project/cinelytics_sdk)

---

## Contact
Pour toute question ou collaboration, n’hésitez pas à me contacter :
- **LinkedIn** : [Koukou Kader Kouadio](https://www.linkedin.com/in/koukou-kader-kouadio-2a32371a4/)
- **Email** : [kkaderkouadio@gmail.com](mailto:kkaderkouadio@gmail.com)


---

Merci d’explorer **Cinema_Insights** ! Ce projet reflète ma passion pour la création de solutions axées sur les données et mon engagement à produire un logiciel de qualité professionnelle.