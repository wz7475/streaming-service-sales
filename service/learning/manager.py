import pickle
from enum import Enum
from functools import lru_cache
from typing import Optional

from service.experiments.database.database import ExperimentsLocalSession
from service.learning.database import crud
from service.learning.database.database import LearningLocalSession
from service.learning.database.models import Artist
from service.learning.errors import ArtistNotFound, UnknownModel
from service.learning.predictor import IPredictor


class EModel(Enum):
    All = "all"
    Naive = "naive"
    Complex = "complex"


class ML:

    def __init__(self, y):
        self.y = y

    def predict(self, start, end):
        p = self.y

        for x in range(min(len(self.y) - 1, start), end):
            p.append(
                sum(p[x - 4: x]) / 4
            )

        return p[start:end + 1]


class MLComplex:
    def __init__(self, y):
        self.y = y

    def predict(self, start, end):
        p = self.y

        for x in range(min(len(self.y) - 1, start), end):
            avg = sum(p[x - 4:x]) / 4
            dynamic = [p[x - i] - p[x - i - 1] for i in range(1, 4)]
            dynamic_avg = sum(dynamic) / len(dynamic)

            p.append(
                avg + dynamic_avg
            )

        return p[start:end + 1]


class LearningManager:

    def __init__(self, experiments_db: ExperimentsLocalSession):
        self._db = LearningLocalSession()
        self._experiments_db = experiments_db
        self._artists = []

    @lru_cache()
    def get_artist(self, artist_id: str) -> Artist:
        artist = crud.get_artist(self._db, artist_id)

        if artist is None:
            raise ArtistNotFound(artist_id)

        return artist

    def get_prediction(self, artist_id: str, model: EModel, start: int,
                       periods: int) -> list[float]:
        artist = self.get_artist(artist_id)
        predictor: Optional[IPredictor] = None

        if model == EModel.Naive:
            predictor = pickle.loads(artist.naive_model)
        elif model == EModel.Complex:
            predictor = pickle.loads(artist.complex_model)
        else:
            raise UnknownModel(model)

        result = predictor.predict(start, periods)

        # @todo: Models should return native python list[float]
        if isinstance(result, list):
            return [r.astype(float) for r in result]
        return result.astype(float).tolist()
