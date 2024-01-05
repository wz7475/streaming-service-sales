import pickle

from model.complex_and_naive_pred_all_artists import generate_models
from service.learning.database.database import LearningLocalSession
from service.learning.database.models import Artist


def build():
    db = LearningLocalSession()

    for artist_id, naive, complex in generate_models():
        artist = Artist(
            id=artist_id,
            train_begin=1,
            train_end=10,
            naive_model=pickle.dumps(naive),
            complex_model=pickle.dumps(complex)
        )
        db.add(artist)
        db.commit()


if __name__ == "__main__":
    build()
