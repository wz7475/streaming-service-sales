from sqlalchemy import Column, Integer, Sequence, String, Date, Float

from service.experiments.database.base import ExperimentsBase


class Result(ExperimentsBase):
    __tablename__ = "results"

    id = Column(Integer, Sequence("result_id_seq"), primary_key=True,
                index=True)
    artist_id = Column(String)
    model = Column(Integer)
    start = Column(Date)
    periods = Column(Integer)
    prediction = Column(String)
    duration = Column(Float)

