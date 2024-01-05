from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from service.config import EXPERIMENTS_DATABASE_URL
from service.experiments.database.base import ExperimentsBase

from service.experiments.database.models import Result

experiments_engine = create_engine(EXPERIMENTS_DATABASE_URL)
ExperimentsBase.metadata.create_all(experiments_engine)

ExperimentsLocalSession = sessionmaker(autocommit=False, autoflush=False,
                                       bind=experiments_engine)


def init():
    pass
