# Projekt: Sprzedaż nieruchomości
# Autorzy: Szymon Śliwa i Adam Zalewski
## Użyte technologie:
- Python 3.11.7
- Mysql 8.0
- Docker

## .env template:
```
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
```
## Jak to działa?
1. Pobierz projekt
2. Stwórz wirtualne środowisko
3. Zainstaluj wymagane paczki ```pip install -r requirements.txt```
4. Upewnij się, że posiadasz demona Docker
5. Jeżeli posiadasz zainstalowanego Make wtedy: ```make build``` i ```make run```
6. Jeżeli nie posiadasz to: ```docker-compose up --build -d```
7. Uruchom program main.py lub stwórz swój na jego wzór
8. Jeżeli chcesz zedytować predefiniowaną strukturę bazy danych możesz to zrobić w pliku ```mysql-init.scripts/init.sql```
