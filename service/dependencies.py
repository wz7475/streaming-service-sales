from service.experiments.manager import ExperimentsManager
from service.learning.manager import LearningManager

learning_manager = LearningManager()
experiments_manager = ExperimentsManager(learning_manager)


def get_experiments_manager():
    return experiments_manager


def get_learning_manager():
    return learning_manager
