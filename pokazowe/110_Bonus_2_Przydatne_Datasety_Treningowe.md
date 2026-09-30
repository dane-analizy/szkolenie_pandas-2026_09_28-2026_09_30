---
tags:
- project/szkolenia
- tech/python
- tech/pandas
- type/reference
---

# 📦 Przydatne Datasety Treningowe (Szybkie Linki do Warsztatów)

[⬅️ Poprzedni moduł: Bonus 1 (Cheat Sheet)](100_Bonus_1_Pandas_Cheat_Sheet.md) | [🏠 Spis treści](../README.md)

Poniższe zbiory danych są publicznie dostępne pod stałymi, krótkimi linkami URL i doskonale nadają się do szybkich demonstracji na żywo (*Live Coding*) oraz jako baza do ćwiczeń dla uczestników szkolenia.

---

## 🌐 1. Podręczne zbiory online (gotowe do wklejenia)

```python
import pandas as pd

# 1. Spożycie alkoholu i napojów na świecie (Groupby, agregacje, sortowanie)
drinks = pd.read_csv('http://bit.ly/drinksbycountry')

# 2. Baza ocen filmów IMDb (Filtrowanie, warunki logiczne, sort_values, nlargest)
movies = pd.read_csv('http://bit.ly/imdbratings')

# 3. Zamówienia w sieci Chipotle (Format TSV - tabulator, czyszczenie cen z .str, pivot_table)
orders = pd.read_csv('http://bit.ly/chiporders', sep='\t')

# 4. Notowania giełdowe małych spółek (Resampling, okna kroczące rolling, DatetimeIndex)
stocks = pd.read_csv('http://bit.ly/smallstocks', parse_dates=['Date'])

# 5. Dane pasażerów Titanica (Czyszczenie braków dropna/fillna, cechy kategoryczne, value_counts)
titanic = pd.read_csv('http://bit.ly/kaggletrain')

# 6. Rejestr obserwacji UFO w USA (Akcesor czasowy .dt, strefy, rozkłady w czasie)
ufo = pd.read_csv('http://bit.ly/uforeports', parse_dates=['Time'])
```

---

## 📋 2. Szczegółowy opis i zastosowanie dydaktyczne zbiorów

| Zmienna | URL / Źródło | Separator / Parametry | Do jakich tematów w Pandas pasuje najlepiej? |
| :--- | :--- | :--- | :--- |
| **`drinks`** | `http://bit.ly/drinksbycountry` | Domyślny przecinek | • `groupby('continent').agg(...)`<br>• Wyliczanie średnich i sum per kontynent<br>• `sort_values(by='beer_servings', ascending=False)`<br>• Proste wykresy słupkowe `df.plot(kind='bar')` |
| **`movies`** | `http://bit.ly/imdbratings` | Domyślny przecinek | • Zaawansowane filtrowanie logiczne `df.query()`<br>• Sortowanie po ocenie (`star_rating`) i czasie trwania (`duration`)<br>• `.nlargest(10, 'star_rating')`<br>• `value_counts()` na gatunkach (`genre`) |
| **`orders`** | `http://bit.ly/chiporders` | **`sep='\t'` (Tabulator!)** | • Obsługa nietypowych separatorów w `read_csv`<br>• Czyszczenie napisów: usunięcie znaku `$` z ceny i konwersja na float (`str.replace` / `to_numeric`)<br>• Wyliczanie łącznej wartości koszyka |
| **`stocks`** | `http://bit.ly/smallstocks` | **`parse_dates=['Date']`** | • Indeks czasowy i szeregi czasowe<br>• `pivot_table(index='Date', columns='Symbol', values='Close')`<br>• Okna kroczące `rolling()` i wyliczanie stóp zwrotu |
| **`titanic`** | `http://bit.ly/kaggletrain` | Domyślny przecinek | • Obsługa braków: `.isnull().sum()`, `dropna(subset=['Age', 'Embarked'])`<br>• Imputacja wieku medianą: `fillna(df['Age'].median())`<br>• `value_counts(normalize=True)` dla przeżywalności per klasa (`Pclass`) |
| **`ufo`** | `http://bit.ly/uforeports` | **`parse_dates=['Time']`** | • Akcesor `.dt`: wyciąganie roku (`dt.year`), dnia tygodnia (`dt.day_name()`)<br>• Zliczanie raportów w czasie metodą `.resample('YE')` lub `.resample('ME')`<br>• Wykrywanie braków w opisach i lokalizacjach |

---

## 🏆 3. Główny zbiór do Case Study (Kaggle)

* **Nazwa zbioru:** **Summer Olympics Medals (1896–2024)**
* **Link:** [https://www.kaggle.com/datasets/stefanydeoliveira/summer-olympics-medals-1896-2024](https://www.kaggle.com/datasets/stefanydeoliveira/summer-olympics-medals-1896-2024)
* **Zastosowanie:** Główny projekt warsztatowy prowadzony na żywo z grupą ([Moduł 080](080_Case_Study_Igrzyska_Olimpijskie.md)).
* **Kluczowe operacje ćwiczone na tym zbiorze:**
  * Wczytanie z jawnym typowaniem i diagnostyka (`.info()`, `.describe()`, `.shape`, `.columns`, `.dtypes`)
  * Czyszczenie danych: filtrowanie medalistów vs uczestników bez medalu (`dropna` z `subset`), unikalne dyscypliny i sportowcy (`nunique`, `unique`)
  * Tabela medalowa wszech czasów z `pivot_table` (Kraj $\times$ Kolor Medalu: Gold, Silver, Bronze)
  * Analiza historyczna reprezentacji Polski na przestrzeni 130 lat igrzysk
  * Wykresy trendu i interaktywne mapy w Plotly Express
