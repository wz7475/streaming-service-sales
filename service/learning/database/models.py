from sqlalchemy import String, Column, Date, LargeBinary

from service.learning.database.base import LearningBase


class Artist(LearningBase):
    __tablename__ = "artists"

    id = Column(String, primary_key=True, index=True)
    train_begin = Column(Date)
    train_end = Column(Date)
    naive_model = Column(LargeBinary)
    complex_model = Column(LargeBinary)
