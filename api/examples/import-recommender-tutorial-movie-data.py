from datetime import datetime, timedelta
import pandas as pd
from typing import Any
from sqlmodel import Session, select
from src.db import init_db, get_engine
from src.namespaces.entity import NamespaceEntity
from src.items.entity import ItemEntity
from src.feedbacks.entity import FeedbackEntity


namespace_name = "movie-test"

test_name = "import-recommender-tutorial-movie-data"


def convert_movie_to_item(movie: Any, index: Any) -> ItemEntity:
    movieId = str(movie.movieId)
    title = str(movie.title)
    genres = str(movie.genres).split("|")

    print("genres", genres)
    item = ItemEntity()
    item.namespace = namespace_name
    item.name = f"movie-{movieId}"
    item.title = title
    item.labels = {
        "test": test_name,
    }
    for genre in genres:
        item.labels[genre.lower()] = "true"
    item.annotations = {
        "movieId": movieId,
        "genres": ", ".join(genres),
    }
    item.tags = []
    for genre in genres:
        item.tags.append(genre)
    item.importedTimestamp = datetime.now()
    item.creationTimestamp = datetime.now() - timedelta(days=index)
    item.features = {}
    for genre in genres:
        item.features[genre.lower()] = "true"
    return item


def convert_rating_to_feedback(rating: Any) -> FeedbackEntity:
    userId = str(rating.userId)
    movieId = str(rating.movieId)
    rating = str(rating.rating)
    # timestamp = str(rating.timestamp)

    feedback = FeedbackEntity()
    feedback.namespace = namespace_name
    feedback.name = f"movie-{movieId}-user-{userId}"
    feedback.actor = f"user-{userId}"
    feedback.item = f"movie-{movieId}"
    feedback.labels = {
        "test": test_name,
        "movieId": movieId,
        "userId": userId,
    }
    feedback.annotations = {
        "movieId": movieId,
        "userId": userId,
        # "timestamp": timestamp,
    }
    feedback.type = "rating"
    feedback.value = rating
    return feedback


init_db()

with Session(get_engine()) as session:
    namespace = session.exec(
        select(NamespaceEntity).where(NamespaceEntity.name == namespace_name)
    ).one_or_none()
    if namespace is None:
        namespace = NamespaceEntity(
            name=namespace_name,
            labels={
                "test": test_name,
            },
        )
        session.add(namespace)
        session.commit()
        session.refresh(namespace)

    # Convert movies to items
    movies = pd.read_csv(
        "https://s3-us-west-2.amazonaws.com/recommender-tutorial/movies.csv"
    )
    # print(movies.head())
    for index, movie in movies.iterrows():
        item = convert_movie_to_item(movie, index)
        session.add(item)
    session.commit()

    # Convert ratings to feedback
    ratings = pd.read_csv(
        "https://s3-us-west-2.amazonaws.com/recommender-tutorial/ratings.csv"
    )
    print(ratings.head())
    for _, rating in ratings.iterrows():
        feedback = convert_rating_to_feedback(rating)
        session.add(feedback)
    session.commit()
