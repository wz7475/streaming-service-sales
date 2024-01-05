import pickle
from datetime import datetime

from sqlalchemy import Column, Integer, Sequence, String, LargeBinary, Date, \
    Float, DateTime, Boolean

from service.experiments.database.base import ExperimentsBase


class Result(ExperimentsBase):
    __tablename__ = "results"

    id = Column(Integer, Sequence("result_id_seq"), primary_key=True,
                index=True)
    artist_id = Column(String)
    model = Column(Integer)
    start = Column(Integer)
    periods = Column(Integer)
    prediction = Column(LargeBinary)
    duration = Column(Float)
    timestamp = Column(DateTime)
    is_experiment = Column(Boolean)


class ResultResponse:
    def __init__(self, artist_id: str, model: int, start: int, periods: int,
                 prediction: bytes, duration: float, timestamp: datetime,
                 is_experiment: bool):
        self.artist_id = artist_id
        self.model = model
        self.start = start
        self.periods = periods
        self.prediction: list[list[float]] = pickle.loads(prediction)
        self.duration = duration
        self.timestamp = timestamp
        self.is_experiment = is_experiment

    @classmethod
    def from_result(cls, result: Result):
        return cls(
            result.artist_id,
            result.model,
            result.start,
            result.periods,
            result.prediction,
            result.duration,
            result.timestamp,
            result.is_experiment
        )
