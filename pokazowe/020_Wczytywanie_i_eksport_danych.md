# Moduł 020: Wczytywanie i Eksport Danych (I/O)

[⬅️ Poprzedni moduł: 010 (Wstęp i NumPy)](010_Wstep_i_ekosystem_Pandas.md) | [🏠 Spis treści](../README.md) | [➡️ Następny moduł: 030 (Struktura Series)](030_Praca_ze_struktura_Series.md)

> **Materiały powiązane:**
>
> - Notatnik demonstracyjny: [020_Wczytywanie_i_eksport_danych.ipynb](020_Wczytywanie_i_eksport_danych.ipynb)
> - Notatnik z ćwiczeniami: [020_Zadania_Wczytywanie_i_eksport.ipynb](../cwiczenia/020_Zadania_Wczytywanie_i_eksport.ipynb)

---

## 1. Parametry odczytu plików w Pandas

Większość problemów przy imporcie (błędy kodowania, liczby zamienione na tekst, brakujące komórki czy brak pamięci RAM) wynika ze złych parametrów odczytu.

### 1.1. Kluczowe parametry `pd.read_csv()`

| Parametr | Domyślnie | Zastosowanie |
| :--- | :--- | :--- |
| `sep` / `delimiter` | `','` | Separator kolumn. W polskich plikach z Excela zazwyczaj: `sep=';'`. |
| `decimal` | `'.'` | Znak dziesiętny. W polskich plikach: `decimal=','` (np. `123,45`). |
| `encoding` | `'utf-8'` | Kodowanie znaków. Starsze pliki z Windowsa: `'cp1250'` lub `'iso-8859-2'`. |
| `usecols` | `None` | Lista kolumn do wczytania (np. `usecols=['id', 'kwota']`). Oszczędza RAM i czas. |
| `skiprows` | `None` | Liczba wierszy do pominięcia od góry pliku (np. nagłówki raportu, metadane). |
| `nrows` | `None` | Wczytanie tylko pierwszych $N$ wierszy (do szybkiego podglądu struktury). |
| `parse_dates` | `False` | Lista kolumn do automatycznej konwersji na daty (`parse_dates=['data_zam']`). |
| `date_format` | `None` | Jawny format daty (np. `'%d.%m.%Y'`) — drastycznie przyspiesza parsowanie. |
| `dtype` | `None` | Słownik typów kolumn (np. `{'id': 'int32', 'status': 'category'}`). Zapobiega pikom pamięci. |
| `na_values` | `None` | Dodatkowe wartości traktowane jako brak danych (np. `na_values=['BRAK', 'N/D', -999]`). |
| `index_col` | `None` | Kolumna, która ma stać się indeksem wierszy (np. `index_col='id'`). |

### 1.2. Kluczowe parametry `pd.read_excel()`

| Parametr | Domyślnie | Zastosowanie |
| :--- | :--- | :--- |
| `sheet_name` | `0` | Nazwa arkusza (`'Sprzedaż'`), indeks (`0`), lista (`['Q1', 'Q2']`) lub `None` (wczytuje wszystkie arkusze jako słownik `{nazwa: DataFrame}`). |
| `skiprows` | `None` | Pominięcie początkowych wierszy z banerami lub metadanymi. |
| `usecols` | `None` | Zakres kolumn literowo (`usecols="A:D,G"`) lub lista nazw kolumn. |
| `engine` | `None` | Silnik odczytu. Dla plików `.xlsx` standard to `engine='openpyxl'`. |

---

## 2. Pliki CSV i eliminacja piku pamięciowego (*Memory Peak*)

### Skąd bierze się Memory Peak?

Gdy wczytujesz duży plik CSV bez podania typów, Pandas domyślnie przydziela 8-bajtowe liczby `int64`/`float64`, a teksty ładuje jako obiekty Pythona. W trakcie parsowania zużycie pamięci RAM potrafi wzrosnąć kilkukrotnie powyżej rozmiaru samego pliku na dysku. Zanim zdążysz zmniejszyć typy (*downcasting*), program rzuci błąd `MemoryError`.

### Rozwiązanie: Schemat `dtype` przy odczycie

Zdefiniuj słownik typów i przekaż go do `pd.read_csv()`. Dane od razu trafią do lekkich buforów C (np. `category`, `int32`, `float32`).

```python
import pandas as pd

# 1. Definicja schematu kolumn przed odczytem
schema_transakcji = {
    'ID_Transakcji': 'int32',
    'Klient_ID': 'int32',
    'Kwota_Brutto': 'float32',
    'Status': 'category',            # 1-2 bajty zamiast ciężkich obiektów string
    'Wojewodztwo': 'category'
}

# 2. Wczytanie pliku CSV ze zdefiniowanym schematem
df_transakcje = pd.read_csv(
    'raport_sprzedazy.csv',
    sep=';',
    decimal=',',
    encoding='cp1250',
    usecols=['ID_Transakcji', 'Data', 'Kwota_Brutto', 'Status', 'Klient_ID', 'Wojewodztwo'],
    dtype=schema_transakcji,
    parse_dates=['Data'],
    na_values=['BRAK', 'N/D', 'null', ''],
    nrows=10_000
)

# 3. Zapis do CSV z polskimi ustawieniami (np. dla polskiego Excela)
df_transakcje.to_csv('transakcje_clean.csv', sep=';', decimal=',', index=False)
```

---

## 3. Praca z Excelem: Arkusz pojedynczy a `pd.ExcelWriter()`

### 3.1. Zapis pojedynczego arkusza

```python
df_transakcje.to_excel('raport_prosty.xlsx', sheet_name='Zamówienia', index=False, engine='openpyxl')
```

### 3.2. Zapis wielu zakładek z `pd.ExcelWriter()`

Gdy raport ma zawierać kilka zakładek (podsumowanie, szczegóły, próbka):

```python
df_podsumowanie = df_transakcje.groupby('Status')['Kwota_Brutto'].sum().reset_index()
df_top10 = df_transakcje.nlargest(10, 'Kwota_Brutto')

# Zapis wielu zakładek w ramach jednego pliku
with pd.ExcelWriter('raport_zarzadczy.xlsx', engine='openpyxl') as writer:
    df_podsumowanie.to_excel(writer, sheet_name='KPI i Podsumowanie', index=False)
    df_top10.to_excel(writer, sheet_name='Top 10 Transakcji', index=False)
    df_transakcje.head(500).to_excel(writer, sheet_name='Surowe Dane (Próbka)', index=False)
```

---

## 4. Złożone struktury API i JSON: `json_normalize()` oraz `.explode()`

Odpowiedzi z REST API rzadko są płaskimi tabelami. Zazwyczaj zawierają dwa wyzwania:

1. **Zagnieżdżone słowniki** (`{"klient": {"miasto": "Gdańsk"}}`) — spłaszcza je funkcja `pd.json_normalize()`.
2. **Listy wewnątrz komórek** (`{"kategorie": ["Elektronika", "AGD"]}`) — metoda `.explode()` rozbija je na osobne wiersze, powielając resztę kolumn.

```python
import pandas as pd

dane_api = [
    {
        "id_zamowienia": 101,
        "klient": {"nazwisko": "Kowalski", "miasto": "Warszawa"},
        "kategorie": ["Elektronika", "AGD"],
        "kwota": 1500
    },
    {
        "id_zamowienia": 102,
        "klient": {"nazwisko": "Nowak", "miasto": "Kraków"},
        "kategorie": ["Książki"],
        "kwota": 120
    }
]

# KROK 1: Spłaszczenie zagnieżdżonych słowników
df_plaski = pd.json_normalize(dane_api)
print("1. Po json_normalize (lista w kolumnie kategorie):")
print(df_plaski[['id_zamowienia', 'klient.miasto', 'kategorie', 'kwota']])

# KROK 2: Rozbicie listy na osobne wiersze
df_rozbity = df_plaski.explode('kategorie').reset_index(drop=True)
print("\n2. Po .explode('kategorie'):")
print(df_rozbity[['id_zamowienia', 'klient.miasto', 'kategorie', 'kwota']])
```

---

## 5. Bazy SQL i format Parquet

### 5.1. Bazy danych SQL

```python
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///:memory:')

# Zapis tabeli do bazy
df_transakcje.to_sql('transakcje', con=engine, index=False, if_exists='replace')

# Bezpieczny odczyt z zapytaniem parametryzowanym
query = "SELECT * FROM transakcje WHERE Kwota_Brutto > :min_kwota"
df_sql = pd.read_sql_query(query, con=engine, params={'min_kwota': 1000.0})
```

### 5.2. Format Parquet

Parquet to binarny format kolumnowy z wbudowaną kompresją i dokładnymi metadanymi typów. Wczytuje się znacznie szybciej niż CSV i zajmuje ułamek miejsca na dysku.

```python
# Zapis z kompresją snappy
df_transakcje.to_parquet('transakcje.parquet', compression='snappy')

# Odczyt kolumnowy z filtrowaniem na poziomie dysku (Predicate Pushdown)
# Wczytujemy tylko 2 kolumny i wiersze spełniające warunek, bez ładowania całego pliku do RAM:
df_parquet = pd.read_parquet(
    'transakcje.parquet',
    columns=['ID_Transakcji', 'Kwota_Brutto'],
    filters=[('Kwota_Brutto', '>', 500)]
)
```

---

## 6. Generowanie danych testowych: Biblioteka `Faker`

Gdy potrzebujesz realistycznych danych do testów wydajnościowych lub weryfikacji procesów:

```python
from faker import Faker
import pandas as pd
import numpy as np

fake = Faker('pl_PL')
Faker.seed(42)

n = 10_000
dane_klientow = {
    'PESEL': [fake.pesel() for _ in range(n)],
    'Klient': [fake.name() for _ in range(n)],
    'Miasto': [fake.city() for _ in range(n)],
    'Firma': [fake.company() for _ in range(n)],
    'Email': [fake.email() for _ in range(n)],
    'Limit_Kredytowy': np.random.choice([5000, 10000, 25000, 50000], size=n)
}

df_klienci = pd.DataFrame(dane_klientow)
print(df_klienci.head(3))
```

---

## 🎯 Ćwiczenia (w notatniku zadań)

W notatniku [020_Zadania_Wczytywanie_i_eksport.ipynb](../cwiczenia/020_Zadania_Wczytywanie_i_eksport.ipynb) przećwiczysz:

1. Parsowanie danych CSV ze średnikiem jako separatorem kolumn i polskim przecinkiem jako separatorem dziesiętnym (`sep=';'`, `decimal=','`).
2. Rozwijanie zagnieżdżonych list zamówień do osobnych wierszy za pomocą metody `.explode()`.
