from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from service.config import LEARNING_DATABASE_URL
from service.learning.database.base import LearningBase

from service.learning.database.models import Artist

learning_engine = create_engine(LEARNING_DATABASE_URL)
LearningBase.metadata.create_all(learning_engine)

LearningLocalSession = sessionmaker(autocommit=False, autoflush=False,
                                    bind=learning_engine)
