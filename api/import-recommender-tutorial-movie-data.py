import pandas as pd
from typing import Any
from sqlmodel import Session, select
from src.db import engine, init_db
from src.namespaces import Namespace
from src.items import Item
from src.feedbacks import Feedback


namespace_name = "movie-test"

test_name = "import-recommender-tutorial-movie-data"


def convert_movie_to_item(movie: Any) -> Item:
    movieId = str(movie.movieId)
    title = str(movie.title)
    genres = str(movie.genres).split("|")

    print("genres", genres)
    item = Item()
    item.namespace_name = namespace_name
    item.name = f"movie-{movieId}"
    item.labels = {
        "test": test_name,
        "genres": ", ".join(genres),
    }
    item.annotations = {
        "movieId": movieId,
        "title": title,
        "genres": ", ".join(genres),
    }
    # for genre in genres:
    #     item.labels.update(genre, "true")
    return item


def convert_rating_to_feedback(rating: Any) -> Feedback:
    userId = str(rating.userId)
    movieId = str(rating.movieId)
    rating = str(rating.rating)
    # timestamp = str(rating.timestamp)

    feedback = Feedback()
    feedback.namespace_name = namespace_name
    feedback.name = f"movie-{movieId}-user-{userId}"
    feedback.actor_name = f"user-{userId}"
    feedback.item_name = f"movie-{movieId}"
    feedback.labels = {
        "test": test_name,
        "movieId": movieId,
        "userId": userId,
    }
    feedback.annotations = {
        "movieId": movieId,
        "userId": userId,
        "rating": rating,
        # "timestamp": timestamp,
    }
    feedback.type = "rating"
    feedback.value = rating
    return feedback


with Session(engine) as session:
    init_db()

    namespace = session.exec(
        select(Namespace).where(Namespace.name == namespace_name)
    ).one_or_none()
    if namespace is None:
        namespace = Namespace(
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
    for _, movie in movies.iterrows():
        item = convert_movie_to_item(movie)
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
