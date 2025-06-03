
# %%
from database import SessionLocal
import query_helpers as query_helpers

# %%
from database import SessionLocal
import models
# Créer une session
db = SessionLocal()

# %%
# Tester la récupération de films
movies = query_helpers.get_movies(db, limit=5, genre="Comedy")

for movie in movies:
    print(f"ID: {movie.movieId}, Titre: {movie.title}, Genres: {movie.genres}")


# %%
#  récupérer et afficher tous les tags ajoutés par l’utilisateur 2 pour le film 60756
tags = db.query(models.Tag).filter(models.Tag.movieId == 60756).filter(models.Tag.userId == 2).all()

for tag in tags:
    print(tag.userId, tag.movieId, tag.tag, tag.timestamp)
# %%
# Fermer la session
db.close()
# %%





