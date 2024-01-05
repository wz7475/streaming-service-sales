from service.experiments.database.database import ExperimentsLocalSession
from service.experiments.manager import ExperimentsManager
from service.learning.manager import LearningManager

experiments_db = ExperimentsLocalSession()
learning_manager = LearningManager(experiments_db)
experiments_manager = ExperimentsManager(experiments_db, learning_manager)


def get_experiments_manager():
    return experiments_manager


def get_learning_manager():
    return learning_manager
