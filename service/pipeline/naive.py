class NaiveModel:
    def __init__(self, train):
        self._train = train

    def predict(self, start: int, periods: int):
        copy = [t for t in self._train]

        for period in range(len(self._train), max(len(self._train), start + periods)):
            copy.append(
                sum(copy[period - 4: period]) / 4
            )

        return copy[start:start + periods]
