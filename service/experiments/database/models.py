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
