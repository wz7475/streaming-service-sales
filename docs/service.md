# Dokumentacja - Mikroserwis

## Opis
Mikroserwis do serwowania predykcji czasu odsłuchu poszczególnych artystów 
został zrealizowany przy użyciu biblioteki FastAPI, wykorzystując sqlalchemy 
oraz bazę danych sqlite. Serwis umożliwia serwowanie predykcji generowanych 
przez określony model dla konkretnego artysty, a także przeprowadzanie 
eksperymentów A/B. Dodatkowo, mikroserwis pozwala na zapytania dotyczące 
wyników historycznych predykcji. 

## Jak uruchomić
1. Wymaga poetry (https://python-poetry.org/docs/#installation).
2. Zainstaluj zależności: `poetry install`.
3. Uruchom w root `mkdir service/db`.
4. Do następnych kroków `cd service`.
5. Aby wygenerować bazę danych, uruchom `python build.py`.
6. Aby uruchomić serwis, uruchom `python main.py`.

## Endpointy

### `/predict/{artist_id}/{start}/{periods}/{model}`
- **Opis**: Serwuje predykcje dla danego artysty z okresu od start do periods, 
wykorzystując zadany model.
- **Parametry URL**:
  - artist_id: Identyfikator artysty.
  - start: Początek okresu predykcji.
  - periods: Liczba okresów do przewidzenia.
  - model: Nazwa wybranego modelu - `naive | complex | all`

### `/predict/{artist_id}/{start}/{periods}/`
- **Opis**: Realizuje eksperymenty A/B, serwuje predykcje z losowego modelu 
(losowanie jest realizowane poprzez próg określony w pliku konfiguracyjnym).
- **Parametry URL**:
  - artist_id: Identyfikator artysty.
  - start: Początek okresu predykcji.
  - periods: Liczba okresów do przewidzenia.

### `/predict/info/{artist_id}`
- **Opis**: Udostępnia informacje o artyście, takie jak train_start i train_end.
- **Parametry URL**:
  - artist_id: Identyfikator artysty.

### `/experiments/get/all`
- **Opis**: Zwraca wyniki wszystkich przeprowadzonych eksperymentów w przeszłości.

### `/experiments/get/?limit=n&artist=X&model=Y`
- **Opis**: Zwraca informacje o N ostatnich eksperymentach dla danego artysty 
- (jeżeli nie podany, to dla wszystkich) z wykorzystaniem zadanego modelu 
- (jeżeli nie podany, to dla naiwnego i złożonego modelu).
- **Parametry URL**:
  - limit: Limit ilości eksperymentów do zwrócenia.
  - artist: Identyfikator artysty (opcjonalny).
  - model: Nazwa wybranego modelu (opcjonalny) - `naive | complex | all`.

## Struktura Wewnętrzna Serwisu

### `main.py`
- **Opis**: Plik główny zawierający implementację endpointów.

### `dependencies.py`
- **Opis**: Plik zawierający definicje zależności.

### `/experiments`
- **Opis**: Katalog zawierający definicję bazy danych przechowującą wyniki 
predykcji oraz menedżera zajmującego się przeprowadzaniem eksperymentów.

### `/learning`
- **Opis**: Katalog zawierający definicję bazy danych z modelami oraz menedżera 
do serwowania predykcji.

## Model danych

### Tabela "Artists"

Opis tabeli "Artists":
- **id (String)**: Identyfikator artysty (klucz główny).
- **train_begin (Integer)**: Początek okresu treningowego.
- **train_end (Integer)**: Koniec okresu treningowego.
- **naive_model (LargeBinary)**: Binarny plik modelu dla podejścia naiwnego.
- **complex_model (LargeBinary)**: Binarny plik modelu dla podejścia zaawansowanego.

### Tabela "Results"

Opis tabeli "Results":
- **id (Integer)**: Identyfikator wyniku (klucz główny).
- **artist_id (String)**: Identyfikator artysty związany z wynikiem.
- **model (Integer)**: Identyfikator modelu.
- **start (Integer)**: Początek okresu predykcji.
- **periods (Integer)**: Liczba okresów predykcji.
- **prediction (LargeBinary)**: Binarny plik z wynikami predykcji.
- **duration (Float)**: Czas trwania predykcji.
- **timestamp (DateTime)**: Data i czas utworzenia wyniku.
- **is_experiment (Boolean)**: Informacja, czy wynik pochodzi z eksperymentu A/B (True/False).
