# Dokumentacja - Analiza i Modele

Poniżej znajduje się krótki opis oraz cel każdego z notatników używanych w projekcie:

## 1. `all_plays_in_service.ipynb`
- Analiza wszystkich odtworzeń w serwisie.
- Porównanie agregacji odtworzeń miesięcznych i tygodniowych.

## 2. `analyze_sarima_dummy.ipynb`
- Analiza skuteczności modelu SARIMA w porównaniu do modelu naiwnego.
- Porównanie rzędu wielkości błędów między oboma modelami.

## 3. `compare_artists.ipynb`
- Porównanie/analiza wszystkich odtworzeń w serwisie, pogrupowanych według artystów.
- Analiza możliwości wykorzystania klasterowania artystów.
- Z powodu uzyskania zadowalających wyników i dużej złożoności klustrowania ten koncept nie był dalje rozwijany.

## 4. `duration_of_play.ipynb`
- Analiza długości trwania jednego odsłuchania.

## 5. `generate_artist_sessions.ipynb`
- Grupowanie wszystkich odtworzeń per artysta.

## 6. `model_all_artists.ipynb`
- Analiza wykorzystania modelu SARIMA do predykcji łącznej ilości odtworzeń dla wszystkich artystów.
- Analiza skuteczności - zadowalające wyniki, analiza sekwencji z miesięcznymi okresami.

## 7. `one_artist_model.ipynb`
- Pierwsza próba wykorzystania modelu SARIMA do predykcji dla jednego artysty.
- Analiza skuteczności - słabe wyniki, problem z nauką sekwencji z tygodniowymi okresami.

## 8. `sample_predictions_on_1_artist.ipynb`
- Analiza możliwości wyznaczania hiperparametrów dla wszystkich artystów, lecz trenowanie modelu dla każdego artysty osobno.