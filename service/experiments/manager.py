from random import uniform
from typing import Any, Optional

from service.config import EXPERIMENTS_SPLIT_PERCENT
from service.experiments.database import crud
from service.experiments.database.database import ExperimentsLocalSession
from service.experiments.database.models import Result, ResultResponse
from service.learning.manager import LearningManager
from service.learning.emodel import EModel


class ExperimentsManager:

    def __init__(self, experiments_db: ExperimentsLocalSession,
                 learning_manager: LearningManager):
        self._db = experiments_db
        self._learning_manager = learning_manager

    def get(self, limit: int, artist: Optional[str], model: Optional[EModel]):
        return crud.get(self._db, limit, artist, model)

    def get_all(self) -> list[ResultResponse]:
        return crud.get_all(self._db)

    def perform_experiment(self, artist_id: str, start: int, periods: int) -> \
            list[Any]:
        model = EModel.Naive

        if uniform(0, 1) > EXPERIMENTS_SPLIT_PERCENT:
            model = EModel.Complex

        result = self._learning_manager.get_prediction(
            artist_id, model, start, periods, is_experiment=True
        )

        return result
