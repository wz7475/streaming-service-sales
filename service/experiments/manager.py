from service.experiments.database.database import ExperimentsLocalSession


class ExperimentsManager:

    def __init__(self):
        self._db = ExperimentsLocalSession()
