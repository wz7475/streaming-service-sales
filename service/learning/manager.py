from service.learning.database.database import LearningLocalSession


class LearningManager:

    def __init__(self):
        self._db = LearningLocalSession()
