import pickle
from datetime import date

from sqlalchemy.orm import Session

from service.experiments.database.models import Result
from service.learning.manager import EModel


def get_all(db: Session) -> list[Result]:
    results = db.query(Result).all()
    
    for result in results:
        result.prediction = pickle.loads(result.prediction)

    return results


def put_result(db: Session, artist_id: str, model: EModel, start: date,
               periods: int, prediction: list[float],
               duration: float) -> Result:
    result = Result(
        artist_id=artist_id,
        model=model.value,
        start=start,
        periods=periods,
        prediction=pickle.dumps(prediction),
        duration=duration
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return result
