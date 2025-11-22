# 🧠 Smart Habit Coach  
Aplikacja do monitorowania nawyków oraz przewidywania ich wykonania za pomocą Machine Learning.

<img width="2010" height="1402" alt="Zrzut ekranu 2025-11-22 o 19 50 43" src="https://github.com/user-attachments/assets/13862d73-9a01-499f-86b2-b515a3fe1684" />

---

## 📌 Opis projektu

**Smart Habit Coach** to aplikacja, która łączy:

- **FastAPI** — szybki backend z REST API  
- **SQLModel + SQLite** — prosta, lekka baza danych  
- **Streamlit** — elegancki frontend  
- **Machine Learning (scikit-learn)** — przewidywanie wykonania nawyku  
- **Pytest** — testy jednostkowe  
- **Seed danych demo** — łatwe przygotowanie środowiska  
- **Reset DB** — czyszczenie bazy jednym poleceniem

Celem projektu jest stworzenie inteligentnego systemu, który:

1. Pozwala użytkownikowi tworzyć i logować nawyki  
2. Prezentuje statystyki historyczne i wskaźniki (wykresy, streaki, skuteczność)  
3. Trenuje model ML dla każdego nawyku osobno  
4. Przewiduje prawdopodobieństwo wykonania nawyku w wybranym dniu  

---

# 🚀 Funkcje aplikacji

### ✔ Zarządzanie nawykami
- Dodawanie nowych nawyków  
- Wyświetlanie listy nawyków  
- Usuwanie nawyków (wraz z powiązanymi logami)
- Edycja istniejących nawyków

### ✔ Logowanie wykonań
- Data wykonania  
- Czy wykonano  
- Nastrój i poziom energii  
- Notatka

### ✔ Dashboard
- Liczba nawyków  
- Średnia skuteczność  
- Najdłuższy streak  
- Wybór nawyku do pogłębionej analizy  

### ✔ Statystyki nawyku
- Wykres wykonania w czasie  
- Wskaźniki streaków  
- Skuteczność (done/not done)

### ✔ Machine Learning
- Trenowanie modelu ML per nawyk  
- Zapisywanie modelu `joblib`  
- Predykcja prawdopodobieństwa wykonania nawyku  
- Obsługa błędów (np. zbyt mało danych)

### ✔ Testy
- Testy CRUD  
- Testy logów  
- Testy ML (różne scenariusze)  

---

# 🛠️ Technologie

| Warstwa | Technologia |
|---------|-------------|
| Backend | FastAPI, SQLModel, Uvicorn |
| ML | scikit-learn (RandomForestClassifier) |
| Frontend | Streamlit |
| Baza danych | SQLite |
| Testy | pytest |
| Inne | joblib, pandas |

---

# 📂 Struktura projektu

```text
smart_habit_coach/
│
├── backend/
│   ├── app/
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── ml/
│   │   ├── seed_demo.py
│   │   └── tools/reset_db.py
│   └── tests/
│
├── frontend/
│   ├── app.py
│   ├── api_client.py
│   └── styles.css
│
├── ml_models/   # (ignored in git)
│
├── requirements.txt
├── README.md
└── .gitignore
```
---

## Uruchomienie projektu
### Klonowanie repo
```bash
git clone https://github.com/Karol-Polak/smart_habit_coach
cd smart-habit-coach
```
### Sworzenie wirtualnego środowiska
```bash
python3 -m venv venv
source venv/bin/activate
```

### Instalacja zależności
```bash
pip install -r requirements.txt
```

### Uruchomienie backendu
```bash
uvicorn backend.app.main:app --reload
```
API dostępne pod:
- http://localhost:8000
- http://localhost:8000/docs

### Uruchomienie frontendu
```bash
streamlit run frontend/app.py
```
