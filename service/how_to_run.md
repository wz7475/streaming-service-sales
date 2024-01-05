## Instrukcja uruchomienia serwisu
_przed uruchomieniem serwisu należy uruchomić pipeline do przygotowania danych - patrz `docs/pipeline.md`_
1. Wymaga poetry (https://python-poetry.org/docs/#installation).
2. Zainstaluj zależności: `poetry install`.
3. Uruchom w root `mkdir service/db`.
4. Do następnych kroków `cd service`.
5. Aby wygenerować bazę danych, uruchom `python build.py`.
6. Aby uruchomić serwis, uruchom `python main.py`.