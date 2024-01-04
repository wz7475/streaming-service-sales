from service.experiments.manager import ExperimentsManager
from service.learning.manager import LearningManager

experiments_manager = ExperimentsManager()
learning_manager = LearningManager()


def get_experiments_manager():
    return experiments_manager


def get_learning_manager():
    return learning_manager
