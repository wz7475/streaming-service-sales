import pickle
from datetime import datetime
from functools import lru_cache
from timeit import default_timer
from typing import Optional

from service.experiments.database.crud import put_result
from service.experiments.database.database import ExperimentsLocalSession
from service.learning.database import crud
from service.learning.database.database import LearningLocalSession
from service.learning.database.models import Artist
from service.learning.emodel import EModel
from service.learning.errors import ArtistNotFound, UnknownModel
from service.learning.predictor import IPredictor


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
                       periods: int, is_experiment: bool = False) -> list[
        float]:
        artist = self.get_artist(artist_id)
        predictor: Optional[IPredictor] = None

        if model == EModel.Naive:
            predictor = pickle.loads(artist.naive_model)
        elif model == EModel.Complex:
            predictor = pickle.loads(artist.complex_model)
        else:
            raise UnknownModel(model)

        start_time = default_timer()

        result = predictor.predict(start, periods)

        end_time = default_timer()
        elapsed_time = end_time - start_time

        put_result(
            self._experiments_db,
            artist_id,
            model,
            start,
            periods,
            result,
            elapsed_time,
            datetime.now(),
            is_experiment
        )

        # @todo: Models should return native python list[float]
        if isinstance(result, list):
            return [r.astype(float) for r in result]
        return result.astype(float).tolist()
