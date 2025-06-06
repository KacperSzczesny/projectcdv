# Flask Backend Project

## Opis
Prosty backend stworzony we Flasku z przykładowymi endpointami GET i POST.

## Wymagania
- Python 3.8+
- Flask

## Instalacja
1. Sklonuj repozytorium lub pobierz pliki.
2. Stwórz i aktywuj wirtualne środowisko (opcjonalnie):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. Zainstaluj wymagane pakiety:
   ```bash
   pip install -r requirements.txt
   ```

## Uruchomienie
```bash
python app.py
```

## API Endpoints
- `GET /api/hello` - zwraca komunikat powitalny
- `POST /api/echo` - zwraca przesłane dane JSON

## Postman
Dołączona jest kolekcja Postman z podstawowymi requestami.
