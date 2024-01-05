import pickle
from datetime import date, datetime
from typing import Optional, Type

from sqlalchemy.orm import Session

from service.experiments.database.models import Result, ResultResponse
from service.learning.manager import EModel


def _decompile_results(results: list[Type[Result]]) -> list[
    Type[ResultResponse]]:
    return [
        ResultResponse.from_result(result) for result in results
    ]


def get(db: Session, limit: int, artist_id: Optional[str],
        model: Optional[EModel]) -> list[Type[ResultResponse]]:
    query = db.query(Result)

    if artist_id is not None:
        query = query.filter(Result.artist_id == artist_id)

    if model is not None and model != EModel.All:
        query = query.filter(Result.model == model.value)

    return _decompile_results(query.limit(limit).all())


def get_all(db: Session) -> list[Type[ResultResponse]]:
    results = db.query(Result).all()

    return _decompile_results(results)


def put_result(db: Session, artist_id: str, model: EModel, start: int,
               periods: int, prediction: list[float],
               duration: float, timestamp: datetime,
               is_experiment: bool) -> Result:
    result = Result(
        artist_id=artist_id,
        model=model.value,
        start=start,
        periods=periods,
        prediction=pickle.dumps(prediction),
        duration=duration,
        timestamp=timestamp,
        is_experiment=is_experiment
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return result
