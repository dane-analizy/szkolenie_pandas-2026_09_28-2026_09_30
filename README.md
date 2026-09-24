---
tags:
- project/szkolenia
- tech/python
- tech/pandas
- type/guide
---

# 📓 Notatniki Warsztatowe (Jupyter Notebooks)

W tym katalogu znajdują się interaktywne notatniki Jupyter oraz podręczniki w formacie Markdown przygotowane na warsztaty z biblioteki Pandas.

---

## 🛠️ Wymagania techniczne i instalacja środowiska

Do uruchomienia materiałów pokazowych i ćwiczeń potrzebujesz Pythona (wersja >= 3.10) oraz zestawu pakietów analitycznych.

### 1. Wymagane biblioteki
* **`pandas`** (>= 2.2.0) — manipulacja i czyszczenie danych tabelarycznych (`Series`, `DataFrame`).
* **`numpy`** (>= 1.26.0) — wektoryzacja SIMD, funkcje `np.where`, `np.select` oraz stała `np.nan`.
* **`duckdb`** (>= 0.10.0) — analityczna baza OLAP w procesie, odpytywanie plików Parquet i CSV za pomocą SQL.
* **`plotly`** (>= 5.20.0) — interaktywne wykresy w notatniku i przeglądarce (`plotly.express`).
* **`openpyxl`** (>= 3.1.0) — odczyt i wieloarkuszowy zapis plików Excel (`.xlsx`).
* **`pyarrow`** (>= 15.0.0) — obsługa formatu Parquet i silnika Apache Arrow w Pandas.
* **`matplotlib` & `seaborn`** — statyczne wykresy do raportów i publikacji.
* **`faker`** — generator danych testowych z polskimi realiami (PESEL, adresy, nazwiska).
* **`sqlalchemy`** — połączenia z relacyjnymi bazami SQL.
* **`jupyterlab` / `notebook`** — środowisko uruchomieniowe notatników.

---

### 2. Instalacja środowiska krok po kroku

Zalecamy pracę w wirtualnym środowisku (**venv**):

#### Krok 1: Utworzenie wirtualnego środowiska
W terminalu (w katalogu repozytorium):

* **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  ```
* **Windows (PowerShell / CMD):**
  ```powershell
  python -m venv .venv
  ```

#### Krok 2: Aktywacja środowiska

* **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```
* **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
  *(Jeśli PowerShell blokuje skrypty: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*
* **Windows (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

#### Krok 3: Instalacja pakietów

Możesz zainstalować pakiety z pliku [requirements.txt](requirements.txt):
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Lub bezpośrednio jednym poleceniem:
```bash
pip install pandas numpy duckdb plotly openpyxl pyarrow faker sqlalchemy matplotlib seaborn jupyterlab
```

#### Krok 4: Przygotowanie danych olimpijskich (`olimpics.zip`)

W repozytorium znajduje się spakowane archiwum z danymi do modułu 080: `olimpics.zip` (plik `olympics_dataset.csv`, ok. 27 MB).

> [!TIP]
> **Wypakowanie danych i wczytywanie ZIP w locie:**  
> Rozpakowanie archiwum (`unzip olimpics.zip`), zmiana nazwy pliku czy wrzucenie do katalogu roboczego to elementarz pracy analityka (zaraz obok sprawdzania kodowania i separatorów). Co ważne: Pandas potrafi też wczytać plik CSV wprost ze skompresowanego archiwum ZIP bez wcześniejszego rozpakowywania: `pd.read_csv('olimpics.zip')`.

* **Rozpakowanie w terminalu (Linux / macOS):**
  ```bash
  unzip olimpics.zip
  ```
* **Rozpakowanie w Windows (PowerShell):**
  ```powershell
  Expand-Archive -Path olimpics.zip -DestinationPath .
  ```
* **Bez rozpakowywania:** Kod w notatnikach automatycznie sprawdza obecność archiwum `olimpics.zip` oraz plików `olympics_dataset.csv` i `olympics.csv`.

#### Krok 5: Uruchomienie Jupyter Lab
```bash
jupyter lab
# lub:
jupyter notebook
```

---

Notatniki zostały podzielone na dwa podfoldery:

---

## 👨‍🏫 1. `notebooks/pokazowe/` (Materiały demonstracyjne i podręczniki)
Katalog zawiera notatniki demonstracyjne Jupyter (`.ipynb`) oraz podręczniki w formacie Markdown (`.md`). Pliki `.md` zawierają podsumowanie teorii, tabele parametrów, dobre praktyki i gotowe snippety kodu do szybkiego wglądu:

1. **[010_Wstep_i_ekosystem_Pandas.ipynb](pokazowe/010_Wstep_i_ekosystem_Pandas.ipynb)** | 📖 **[Podręcznik 010 (MD)](pokazowe/010_Wstep_i_ekosystem_Pandas.md)** — wektoryzacja `np.where`, `np.select`, Copy-on-Write, diagnostyka pamięci.
2. **[020_Wczytywanie_i_eksport_danych.ipynb](pokazowe/020_Wczytywanie_i_eksport_danych.ipynb)** | 📖 **[Podręcznik 020 (MD)](pokazowe/020_Wczytywanie_i_eksport_danych.md)** — CSV z polskimi liczbami, zagnieżdżony JSON (`json_normalize`, `explode`), Parquet.
3. **[030_Praca_ze_struktura_Series.ipynb](pokazowe/030_Praca_ze_struktura_Series.ipynb)** | 📖 **[Podręcznik 030 (MD)](pokazowe/030_Praca_ze_struktura_Series.md)** — slicing (`loc`, `iloc`), statystyki (`sum`, `mean`, `nlargest`), `.describe()`, `.unique()`, `.isnull().sum()`, `.fillna()`, `value_counts`.
4. **[040_Praca_z_DataFrame_selekcja_czyszczenie.ipynb](pokazowe/040_Praca_z_DataFrame_selekcja_czyszczenie.ipynb)** | 📖 **[Podręcznik 040 (MD)](pokazowe/040_Praca_z_DataFrame_selekcja_czyszczenie.md)** — `.info()`, `.describe(include='all')`, czyszczenie z `dropna(subset=[...])`, `.fillna({...})`, deduplikacja `drop_duplicates(subset=[...])`, sortowanie wielokolumnowe `sort_values`, rozkłady `value_counts`, iteracja z `itertuples()`.
5. **[050_Daty_i_szeregi_czasowe.ipynb](pokazowe/050_Daty_i_szeregi_czasowe.ipynb)** | 📖 **[Podręcznik 050 (MD)](pokazowe/050_Daty_i_szeregi_czasowe.md)** — `pd.to_datetime` z `errors='coerce'`, akcesor `.dt`, resampling dzienny, okna kroczące `rolling`.
6. **[060_Transformacje_grupowanie_laczenie.ipynb](pokazowe/060_Transformacje_grupowanie_laczenie.ipynb)** | 📖 **[Podręcznik 060 (MD)](pokazowe/060_Transformacje_grupowanie_laczenie.md)** — parametr `axis` (0 vs 1), `pivot_table` vs `melt`, SQL-style groupby z `as_index=False` i `NamedAgg`, `transform()`, relacyjny `merge` z `validate='1:m'` i `indicator=True`.
7. **[070_Wizualizacja_danych_Plotly.ipynb](pokazowe/070_Wizualizacja_danych_Plotly.ipynb)** | 📖 **[Podręcznik 070 (MD)](pokazowe/070_Wizualizacja_danych_Plotly.md)** — szybki `df.plot()`, interaktywne wykresy Plotly Express (`scatter`, `bar`, `box`).
8. **[080_Case_Study_Igrzyska_Olimpijskie.ipynb](pokazowe/080_Case_Study_Igrzyska_Olimpijskie.ipynb)** | 📖 **[Podręcznik 080 (MD)](pokazowe/080_Case_Study_Igrzyska_Olimpijskie.md)** — warsztat: 130 lat Igrzysk Olimpijskich (dane w archiwum `olimpics.zip`), tabela medalowa wszech czasów, sukcesy Polski.
9. **[090_Wydajnosc_i_Big_Data_DuckDB.ipynb](pokazowe/090_Wydajnosc_i_Big_Data_DuckDB.ipynb)** | 📖 **[Podręcznik 090 (MD)](pokazowe/090_Wydajnosc_i_Big_Data_DuckDB.md)** — typ `category` (-80% RAM), strumieniowanie `chunksize`, analityczny SQL na plikach w DuckDB.

---

## ✍️ 2. `notebooks/cwiczenia/` (Zadania praktyczne dla kursantów)
Notatniki z ćwiczeniami dla uczestników. Każde zadanie zawiera:
1. **Opis zadania w Markdown** (kontekst biznesowy i dane wejściowe),
2. **Pustą komórkę na kod kursanta** (`# TUTAJ WPISZ SWÓJ KOD:`),
3. **Komórkę ze wzorcowym rozwiązaniem** (`# ROZWIĄZANIE WZORCOWE:`).

1. **[010_Zadania_Wstep_i_NumPy.ipynb](cwiczenia/010_Zadania_Wstep_i_NumPy.ipynb)**
2. **[020_Zadania_Wczytywanie_i_eksport.ipynb](cwiczenia/020_Zadania_Wczytywanie_i_eksport.ipynb)**
3. **[030_Zadania_Series.ipynb](cwiczenia/030_Zadania_Series.ipynb)**
4. **[040_Zadania_DataFrame.ipynb](cwiczenia/040_Zadania_DataFrame.ipynb)**
5. **[050_Zadania_Daty_i_szeregi_czasowe.ipynb](cwiczenia/050_Zadania_Daty_i_szeregi_czasowe.ipynb)**
6. **[060_Zadania_Grupowanie_i_laczenie.ipynb](cwiczenia/060_Zadania_Grupowanie_i_laczenie.ipynb)**
7. **[070_Zadania_Wizualizacja.ipynb](cwiczenia/070_Zadania_Wizualizacja.ipynb)**
8. **[080_Zadania_Case_Studies_Domowe.ipynb](cwiczenia/080_Zadania_Case_Studies_Domowe.ipynb)** — zaawansowane zadania domowe: analiza koszykowa (self-merge) oraz detekcja awarii w telemetrii.
9. **[090_Zadania_Wydajnosc_i_optymalizacja.ipynb](cwiczenia/090_Zadania_Wydajnosc_i_optymalizacja.ipynb)**

---

## 📦 3. Przydatne zbiory danych online (do własnych ćwiczeń po szkoleniu)

Zwięzłe, publicznie dostępne zbiory danych pod stałymi adresami URL. Możesz je wczytać do dowolnego notatnika w jednej linijce kodu (`pd.read_csv('URL')`) — bez pobierania i rozpakowywania plików na dysku. Przydadzą się do ćwiczeń i prototypowania po szkoleniu:

### Szybkie snippety do wklejenia w komórkę:

```python
import pandas as pd

# 1. Spożycie alkoholu i napojów na świecie (groupby, agregacje, sortowanie)
drinks = pd.read_csv('http://bit.ly/drinksbycountry')

# 2. Baza ocen filmów IMDb (filtrowanie, warunki logiczne, sort_values, nlargest)
movies = pd.read_csv('http://bit.ly/imdbratings')

# 3. Zamówienia w sieci Chipotle (format TSV - tabulator, czyszczenie cen z .str, pivot_table)
orders = pd.read_csv('http://bit.ly/chiporders', sep='\t')

# 4. Notowania giełdowe małych spółek (resampling, okna kroczące rolling, DatetimeIndex)
stocks = pd.read_csv('http://bit.ly/smallstocks', parse_dates=['Date'])

# 5. Dane pasażerów Titanica (czyszczenie braków dropna/fillna, cechy kategoryczne, value_counts)
titanic = pd.read_csv('http://bit.ly/kaggletrain')

# 6. Rejestr obserwacji UFO w USA (akcesor czasowy .dt, strefy, rozkłady w czasie)
ufo = pd.read_csv('http://bit.ly/uforeports', parse_dates=['Time'])
```

### Zestawienie zbiorów i rekomendowane tematy do ćwiczeń:

| Zbiór | URL / Źródło | Parametry odczytu | Do jakich tematów w Pandas pasuje najlepiej? |
| :--- | :--- | :--- | :--- |
| **`drinks`** | `http://bit.ly/drinksbycountry` | Domyślne | • Agregacje grupowe: `groupby('continent').agg(...)`<br>• Średnie i sumy per kontynent<br>• Sortowanie: `sort_values(by='beer_servings', ascending=False)`<br>• Szybkie wykresy słupkowe: `df.plot(kind='bar')` |
| **`movies`** | `http://bit.ly/imdbratings` | Domyślne | • Filtrowanie logiczne `df.query()`<br>• Sortowanie po ocenie (`star_rating`) i czasie trwania (`duration`)<br>• Wartości skrajne: `.nlargest(10, 'star_rating')`<br>• Częstości: `value_counts()` na gatunkach filmowych (`genre`) |
| **`orders`** | `http://bit.ly/chiporders` | **`sep='\t'` (Tabulator)** | • Obsługa nietypowych separatorów w `read_csv`<br>• Oczyszczanie tekstu: usunięcie znaku `$` z cen i konwersja na float (`str.replace` / `to_numeric`)<br>• Wartość koszyka i tabele przestawne |
| **`stocks`** | `http://bit.ly/smallstocks` | **`parse_dates=['Date']`** | • Indeks czasowy i analiza finansowa<br>• Format szeroki: `pivot_table(index='Date', columns='Symbol', values='Close')`<br>• Okna kroczące `rolling()` i wyliczanie stóp zwrotu |
| **`titanic`** | `http://bit.ly/kaggletrain` | Domyślne | • Diagnoza i czyszczenie braków: `.isnull().sum()`, `dropna(subset=['Age', 'Embarked'])`<br>• Imputacja wieku medianą: `fillna(df['Age'].median())`<br>• Przeżywalność per klasa z `value_counts(normalize=True)` |
| **`ufo`** | `http://bit.ly/uforeports` | **`parse_dates=['Time']`** | • Akcesor `.dt`: wyciąganie roku (`dt.year`), dnia tygodnia (`dt.day_name()`)<br>• Agregacja w czasie metodą `.resample('YE')` lub `.resample('ME')`<br>• Wykrywanie anomalii w zgłoszeniach |
