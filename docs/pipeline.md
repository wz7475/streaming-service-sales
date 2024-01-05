# Dokumentacja - Budowanie Bazy Danych Modeli

Proces tworzenia bazy danych modeli obejmuje uruchomienie kilku skryptów i 
notatników, przy jednoczesnym wyłączeniu mikroserwisu.

## 1. `clear_sessions.py`
Skrypt ten jest odpowiedzialny za przefiltrowanie sesji i przekształcenie ich 
do postaci `timestamp, track_id`.

## 2. `clear_tracks.py`
Ten skrypt przeprowadza proces przefiltrowania utworów, zamieniając je na 
postać `id, artist_id`.

## 3. `generate_timestamp_artist.py`
Skrypt ten łączy wygenerowane pliki z skryptów `clear_session.py` oraz 
`clear_tracks.py` w formę `timestamp, artist_id`.

## 4. `generate_artist_sessions.ipynb`
Notatnik ten zajmuje się filtrowaniem i podziałem danych wygenerowanych przez 
skrypt `generate_timestamp_artist.py` na pojedynczy plik dla każdego artysty.

## 5. `service/build.py`
Główny skrypt, wykorzystujący funkcje z pliku `service_model_on_1_artist.py`. 
Ten skrypt generuje modele za pomocą wspomnianego skryptu i zapisuje je do 
bazy danych. Cały proces powinien być przeprowadzony przy 
wyłączonym mikroserwisie, aby uniknąć konfliktów i zapewnić poprawność danych.