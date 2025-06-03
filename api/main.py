from fastapi import FastAPI, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal
import query_helpers as helpers
import traceback
import schemas



api_description = """ 
🎬 **Bienvenue sur l'API CINEMA_INSIGHTS**

Cette API vous permet d'explorer une base de données inspirée du célèbre jeu de données [MovieLens](https://grouplens.org/datasets/movielens/).  
Elle constitue un excellent point de départ pour découvrir comment interagir avec une API REST autour de données cinématographiques :
 films, utilisateurs, appréciations, tags et liens vers des ressources externes (IMDB, TMDB).

### 🚀 Fonctionnalités principales :

- 🔍 Rechercher un film par son identifiant ou parcourir l’ensemble des films disponibles  
- ⭐ Consulter les appréciations (ratings) données par les utilisateurs, par film ou par utilisateur  
- 🏷️ Accéder aux tags attribués aux films par les utilisateurs  
- 🔗 Récupérer les liens vers les fiches IMDB et TMDB pour chaque film  
- 📊 Visualiser des statistiques globales sur les données

### ⚙️ Détails techniques :
- Tous les endpoints prennent en charge la pagination (`skip`, `limit`) et des filtres optionnels selon le cas d’usage.
- L’API respecte les standards REST, avec des réponses claires et des codes HTTP appropriés en cas d’erreur (ex. : identifiant introuvable).

### 🧪 Astuce :
Testez facilement les fonctionnalités via l’interface interactive Swagger disponible à l’URL `/docs`.

---

Explorez, testez, intégrez et profitez des données cinéma comme jamais auparavant !
"""


# --- Initialisation de l'application FastAPI ---
app = FastAPI(
    title="CINEMA_INSIGHTS API",
    description = api_description,
    version = "0.1"
)

# --- Dépendance pour la session de base de données ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint pour tester la santé de l'API
@app.get(
    "/",
    summary="Bienvenue sur CINEMA_INSIGHTS API 🎬",
    description="Ce point de terminaison permet de vérifier que l'API CINEMA_INSIGHTS est opérationnelle.",
    response_description="Statut de l'API",
    operation_id="health_check_movies_api",
    tags=["monitoring"]
)

async def root():
    return {"message": "Bienvenue sur l'API CINEMA_INSIGHTS. Statut : OK"}


# Endpoint pour obtenir un film par son ID
@app.get(
    "/movies/{movie_id}", # /movies/1
    summary="Obtenir un film par son ID",
    description="Retourne les informations d’un film en utilisant son `movieId`.",
    response_description="Détails du film",
    response_model=schemas.MovieDetailed,
    tags=["films"],
)
def read_movie(movie_id: int = Path(..., description="L'identifiant unique du film"), db: Session = Depends(get_db)):
    movie = helpers.get_movie(db, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Film avec l'ID {movie_id} non trouvé")
    return movie


# Endpoint pour obtenir une liste des films (avec pagination et filtres facultatifs title, genre, skip, limit)
@app.get(
    "/movies",
    summary="Lister les films",
    description="Retourne une liste de films avec pagination et filtres optionnels par titre ou genre.",
    response_description="Liste de films",
    response_model=List[schemas.MovieSimple],
    tags=["films"],
)
def list_movies(
    skip: int = Query(0, ge=0, description="Nombre de résultats à ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de résultats à retourner"),
    title: str = Query(None, description="Filtre par titre"),
    genre: str = Query(None, description="Filtre par genre"),
    db: Session = Depends(get_db)
):
    movies = helpers.get_movies(db, skip=skip, limit=limit, title=title, genre=genre)
    return movies


# Endpoint pour obtenir une appreciation par utilisateur et film
@app.get(
    "/ratings/{user_id}/{movie_id}",
    summary="Obtenir une appreciation par utilisateur et film",
    description="Retourne l'appreciation d'un utilisateur pour un film donné.",
    response_description="Détails de l'appreciation",
    response_model=schemas.RatingSimple,
    tags=["appreciations"],
)
def read_rating(
    user_id: int = Path(..., description="ID de l'utilisateur"),
    movie_id: int = Path(..., description="ID du film"),
    db: Session = Depends(get_db)
):
    rating = helpers.get_rating(db, user_id=user_id, movie_id=movie_id)
    if rating is None:
        raise HTTPException(
            status_code=404,
            detail=f"Aucune appreciation trouvée pour l'utilisateur {user_id} et le film {movie_id}"
        )
    return rating


# Endpoint pour obtenir une liste d’appreciations avec filtres
@app.get(
    "/ratings",
    summary="Lister les appreciations",
    description="Retourne une liste d’appreciations avec pagination et filtres optionnels (film, utilisateur, note min).",
    response_description="Liste des appreciations",
    response_model=List[schemas.RatingSimple],
    tags=["appreciations"],
)
def list_ratings(
    skip: int = Query(0, ge=0, description="Nombre de résultats à ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de résultats à retourner"),
    movie_id: Optional[int] = Query(None, description="Filtrer par ID de film"),
    user_id: Optional[int] = Query(None, description="Filtrer par ID d'utilisateur"),
    min_rating: Optional[float] = Query(None, ge=0.0, le=5.0, description="Filtrer les notes supérieures ou égales à cette valeur"),
    db: Session = Depends(get_db)
):
    ratings = helpers.get_ratings(db, skip=skip, limit=limit, movie_id=movie_id, user_id=user_id, min_rating=min_rating)
    return ratings

#  Endpoint pour retourner un tag pour un utilisateur et un film donnés, avec le texte du tag
@app.get(
    "/tags/{user_id}/{movie_id}/{tag_text}",
    summary="Obtenir un tag spécifique",
    description="Retourne un tag pour un utilisateur et un film donnés, avec le texte du tag.",
    response_model=schemas.TagSimple,
    tags=["tags"],
)
def read_tag(
    user_id: int = Path(..., description="ID de l'utilisateur"),
    movie_id: int = Path(..., description="ID du film"),
    tag_text: str = Path(..., description="Contenu exact du tag"),
    db: Session = Depends(get_db)
):
    result = helpers.get_tag(db, user_id=user_id, movie_id=movie_id, tag_text=tag_text)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Tag non trouvé pour l'utilisateur {user_id}, le film {movie_id} et le tag '{tag_text}'"
        )
    return result



# Endpoint pour retourner une liste de tags avec pagination et filtres facultatifs par utilisateur ou film
@app.get(
    "/tags",
    summary="Lister les tags",
    description="Retourne une liste de tags avec pagination et filtres facultatifs par utilisateur ou film.",
    response_model=List[schemas.TagSimple],
    tags=["tags"],
)
def list_tags(
    skip: int = Query(0, ge=0, description="Nombre de résultats à ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de résultats à retourner"),
    movie_id: Optional[int] = Query(None, description="Filtrer par ID de film"),
    user_id: Optional[int] = Query(None, description="Filtrer par ID d'utilisateur"),
    db: Session = Depends(get_db)
):
    return helpers.get_tags(db, skip=skip, limit=limit, movie_id=movie_id, user_id=user_id)



# Endpoint pour retourner les identifiants IMDB et TMDB pour un film donné
@app.get(
    "/tags",
    summary="Lister les tags",
    description="Retourne une liste de tags avec pagination et filtres facultatifs par utilisateur ou film.",
    response_model=List[schemas.TagSimple],
    tags=["tags"],
)
def list_tags(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    movie_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        return helpers.get_tags(db, skip=skip, limit=limit, movie_id=movie_id, user_id=user_id)
    except Exception as e:
        print("ERREUR /tags :", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint pour retourner une liste paginée des identifiants IMDB et TMDB de tous les films
@app.get(
    "/links",
    summary="Lister les liens des films",
    description="Retourne une liste paginée des identifiants IMDB et TMDB de tous les films.",
    response_model=List[schemas.LinkSimple],
    tags=["links"],
)
def list_links(
    skip: int = Query(0, ge=0, description="Nombre de résultats à ignorer"),
    limit: int = Query(100, le=1000, description="Nombre maximal de résultats à retourner"),
    db: Session = Depends(get_db)
):
    return helpers.get_links(db, skip=skip, limit=limit)


# Endpoint pour obtenir des statistiques sur la base de données
@app.get(
    "/analytics",
    summary="Obtenir des statistiques",
    description="""
    Retourne un résumé analytique de la base de données :

    - Nombre total de films
    - Nombre total d’appreciations
    - Nombre total de tags
    - Nombre de liens vers IMDB/TMDB
    """,
    response_model=schemas.AnalyticsResponse,
    tags=["analytics"]
)
def get_analytics(db: Session = Depends(get_db)):
    movie_count = helpers.get_movie_count(db)
    rating_count = helpers.get_rating_count(db)
    tag_count = helpers.get_tag_count(db)
    link_count = helpers.get_link_count(db)

    return schemas.AnalyticsResponse(
        movie_count=movie_count,
        rating_count=rating_count,
        tag_count=tag_count,
        link_count=link_count
    )