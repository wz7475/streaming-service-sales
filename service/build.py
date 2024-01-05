import pickle

from service.learning.database.database import LearningLocalSession
from service.learning.database.models import Artist
from service.pipeline.naive import NaiveModel


def build():
    db = LearningLocalSession()

    artist = Artist(
        id="34",
        train_begin=1,
        train_end=10,
        naive_model=pickle.dumps(
            NaiveModel([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ),
        complex_model=pickle.dumps(
            NaiveModel([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        )
    )
    db.add(artist)
    db.commit()


if __name__ == "__main__":
    build()
