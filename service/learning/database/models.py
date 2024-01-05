from sqlalchemy import String, Column, Integer, LargeBinary

from service.learning.database.base import LearningBase


class Artist(LearningBase):
    __tablename__ = "artists"

    id = Column(String, primary_key=True, index=True)
    train_begin = Column(Integer)
    train_end = Column(Integer)
    naive_model = Column(LargeBinary)
    complex_model = Column(LargeBinary)
