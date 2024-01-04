from sqlalchemy import Column, Integer, Sequence

from service.experiments.database.base import ExperimentsBase


class Result(ExperimentsBase):
    __tablename__ = "results"

    id = Column(Integer, Sequence("result_id_seq"), primary_key=True,
                index=True)
