---
tags:
- project/szkolenia
- tech/python
- tech/pandas
- tech/plotly
- type/cheatsheet
---

# 📑 Ściąga – Pandas & PyData Cheat Sheet

[⬅️ Poprzedni moduł: 090 (Wydajność i DuckDB)](090_Wydajnosc_i_Big_Data_DuckDB.md) | [🏠 Spis treści](../README.md) | [➡️ Bonus 2: Datasety treningowe](110_Bonus_2_Przydatne_Datasety_Treningowe.md)

Szybki podręczny przewodnik po najważniejszych metodach, składni i idiomatycznych wzorcach w codziennej pracy analityka.

---

## 🛠️ Konfiguracja, Diagnostyka i Magia Jupytera

```python
import pandas as pd
import numpy as np

# Konfiguracja środowiska
pd.set_option('display.max_columns', 20)      # Maksymalna liczba kolumn
pd.set_option('display.max_rows', 10)         # Maksymalna liczba wierszy
pd.set_option('display.float_format', '{:,.2f} zł'.format) # Format walutowy
pd.set_option('mode.copy_on_write', True)     # Włączenie bezpiecznego standardu CoW

# Diagnostyka
df.info(memory_usage='deep')                  # Pełna diagnostyka typów i faktycznego RAM
df.describe(include='all')                    # Statystyki opisowe
df.shape                                      # (liczba_wierszy, liczba_kolumn)

# Magiczne komendy Jupytera do mierzenia czasu:
# %time operacja_jednorazowa()                # Czas wykonania 1 linijki
# %%time                                      # Czas wykonania całej komórki
# %timeit df['a'] * 2                         # Wielokrotne powtórzenia ze średnią (+/- std)
```

---

## 📥 Wczytywanie i Zapis (I/O)

```python
# CSV z polskimi ustawieniami regionalnymi i jawnym typowaniem (eliminuje Memory Peak!)
df = pd.read_csv('plik.csv', sep=';', decimal=',', encoding='cp1250', parse_dates=['data'], dtype={'id': 'int32', 'status': 'category'})
df.to_csv('wynik.csv', index=False, sep=';', decimal=',')

# Excel: Pojedynczy arkusz vs Wieloarkuszowy ExcelWriter
df.to_excel('pojedynczy.xlsx', sheet_name='Dane', index=False)

with pd.ExcelWriter('wieloarkuszowy.xlsx', engine='openpyxl') as writer:
    df1.to_excel(writer, sheet_name='Styczeń', index=False)
    df2.to_excel(writer, sheet_name='Luty', index=False)

# JSON: Spłaszczanie słowników i rozwijanie list
df = pd.json_normalize(dane_api)              # Spłaszcza {"klient": {"miasto": "Gdańsk"}} -> klient.miasto
df = df.explode('lista_pozycji')              # Rozbija zagnieżdżoną listę na osobne wiersze!

# Parquet (Szybki odczyt kolumnowy z filtrem na dysku)
df = pd.read_parquet('dane.parquet', columns=['id', 'kwota'], filters=[('kwota', '>', 100)])
df.to_parquet('wynik.parquet', compression='snappy')
```

---

## 🎯 Selekcja, Slicing i Zarządzanie Indeksem

```python
# Zarządzanie indeksem i MultiIndex
df = df.reset_index(drop=True)                # PORZUCENIE starego indeksu (czysta numeracja 0..N)
df = df.set_index('klient_id')                # Ustawienie kolumny jako indeksu
df.columns = df.columns.droplevel(0)          # Usunięcie poziomu nadrzędnego po groupby
etykiety = df.columns.get_level_values(1)     # Pobranie listy etykiet z danego poziomu
df.columns = ['_'.join(c) for c in df.columns]# Alternatywa: spłaszczenie dwupoziomowych kolumn

# Widok vs Kopia (defensywne kodowanie)
sub = df[df['wiek'] > 30].copy()              # Jawna, bezpieczna kopia w RAM (deep=True)

# Dostęp skalarowy (najszybszy)
df.iat[0, 1]                                  # Po pozycji numerycznej [wiersz, kolumna]
df.at['klient_101', 'kwota']                  # Po etykietach

# Slicing w Series i DataFrame
df.iloc[0:5, 1:4]                             # Pozycje numeryczne (0..4 wiersze, 1..3 kolumny)
df.loc['2024-01-01':'2024-01-31', ['A', 'B']] # Etykiety (domknięte OBUSTAWNIE!)
s.iloc[-1]                                    # Ostatni element
s.iloc[::2]                                   # Co drugi element

# Filtrowanie i zapytania
df[(df['wiek'] >= 18) & (df['kraj'] == 'PL')] # Pamiętaj o nawiasach () wokół warunków!
df.query("wiek >= 18 and kraj == 'PL' and zarobki > @prog")
```

---

## 🔄 Parametr `axis` – Ściąga Pamięciowa

```python
# axis=0 (lub 'index')  --> Kierunek PIONOWY (w dół)
df.mean(axis=0)                               # Średnia z każdej kolumny
pd.concat([df1, df2], axis=0)                 # Doklej wiersze pod spodem (wydłuża tabelę)
df.drop('index_wiersza', axis=0)              # Usuń wiersz

# axis=1 (lub 'columns') --> Kierunek POZIOMY (w poprzek)
df.mean(axis=1)                               # Średnia z każdego wiersza
pd.concat([df1, df2], axis=1)                 # Doklej kolumny obok siebie (poszerza tabelę)
df.drop('nazwa_kolumny', axis=1)              # Usuń kolumnę
df.apply(lambda row: row['a'] * 2, axis=1)    # Przekazuje cały wiersz do funkcji
```

---

## 🧹 Czyszczenie Danych, Wektoryzacja i NumPy

```python
# Warunki wektorowe (zamiast powolnego apply)
df['klasa'] = np.where(df['kwota'] > 1000, 'Duża', 'Mała')
df['poziom'] = np.select([df['wiek'] < 25, df['wiek'] <= 50], ['Junior', 'Mid'], default='Senior')

# Obsługa braków (Missing Data - pamiętaj o subset!)
df.isna().sum()                               # Liczba braków per kolumna (tożsame z df.isnull().sum())
df.dropna(subset=['kwota', 'klient_id'])      # Usuwa wiersze z brakami TYLKO w podanych kolumnach!
df.dropna(subset=['tel', 'mail'], how='all')  # Usuwa tylko gdy OBA pola są puste
df['kolumna'].fillna(df['kolumna'].mean())    # Wypełnienie średnią
df.fillna({'kwota': 0, 'telefon': 'Brak'})    # Wypełnienie słownikiem per kolumna
df['kolumna'].ffill()                         # Przeniesienie poprzedniej wartości

# Usuwanie i audyt duplikatów (pamiętaj o subset i keep!)
df.drop_duplicates(subset=['klient_id'], keep='first') # Zachowaj pierwszy wpis
df.drop_duplicates(subset=['klient_id'], keep='last')  # Zachowaj najświeższy wpis
df[df.duplicated(subset=['klient_id'], keep=False)]    # Pokaż wszystkie powtórzone wiersze

# Sortowanie DataFrame i indeksu
df.sort_values(by='kwota', ascending=False)   # Sortowanie po 1 kolumnie malejąco
df.sort_values(by=['miasto', 'kwota'], ascending=[True, False], ignore_index=True) # Wielokolumnowe
df.sort_values(by='kwota', na_position='first') # Braki NaN na samym początku
df.sort_index(ascending=True)                 # Sortowanie po etykietach indeksu
s.nlargest(5)                                 # Top 5 wartości (szybsze od pełnego sortowania!)

# Zliczanie częstości, unikalność i rozkłady (value_counts, nunique, unique)
df['kategoria'].value_counts()                # Liczba wystąpień
df['kategoria'].value_counts(normalize=True, dropna=False) * 100 # Procenty z brakami!
df.value_counts(subset=['kategoria', 'miasto']) # Częstość kombinacji par kolumn
df['kwota'].value_counts(bins=4)              # Automatyczny mini-histogram
df.nunique()                                  # Liczba unikalnych per kolumna w DataFrame
df['miasto'].unique()                         # Tablica unikalnych wartości (Series)

# Iteracja po wierszach (itertuples >> iterrows)
for row in df.itertuples(index=True):         # 50x szybsze niż iterrows, zachowuje typy!
    print(row.Index, row.klient, row.kwota)
# ANTYWZORZEC: for idx, row in df.iterrows()  # Powolne i rzutuje int na float/object!

# Tekst i Regex (akcesor .str)
df['telefon'] = df['telefon'].str.replace(r'\D', '', regex=True) # Tylko cyfry
df['email'] = df['email'].str.strip().str.lower()
df['domena'] = df['email'].str.extract(r'@([\w\.]+)')

# Kategoryzacja i kwartyle
df['przedzial'] = pd.cut(df['wiek'], bins=[0, 18, 65, 120], labels=['Młody', 'Dorosły', 'Senior'])
df['kwartyl'] = pd.qcut(df['wydatki'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
```

---

## ⏱️ Daty i Szeregi Czasowe (Time Series)

```python
# Bezpieczne parsowanie (errors='coerce' zamienia śmieci w NaT!)
df['data'] = pd.to_datetime(df['data_raw'], format='%d.%m.%Y', errors='coerce', dayfirst=True)

# Akcesor .dt
df['rok'] = df['data'].dt.year
df['dzien_tygodnia'] = df['data'].dt.day_name(locale='pl_PL')
df['czy_weekend'] = df['data'].dt.dayofweek >= 5

# Resampling i okna kroczące (wymaga DatetimeIndex)
df_dzienne = df.resample('D').agg({'obroty': 'sum', 'temp': 'mean'})
df['SMA_20'] = df['cena'].rolling(window=20, min_periods=5).mean()
```

---

## 📊 Grupowanie i Relacyjne Łączenie Danych

```python
# Nowoczesny GroupBy w stylu SQL z as_index=False (agg == aggregate)
df_raport = df.groupby('dzial', as_index=False).agg(
    liczba_osob=('id', 'count'),
    srednia_pensja=('pensja', 'mean'),
    max_pensja=('pensja', 'max')
)

# Słownik z listą funkcji per kolumna (generuje MultiIndex w kolumnach)
df_podsum = df.groupby('dzial', as_index=False).aggregate({
    'pensja': ['mean', 'max'],                 # Kilka funkcji dla jednej kolumny
    'staz': 'median'
})
df_podsum.columns = ['_'.join(c).strip('_') for c in df_podsum.columns] # Spłaszczenie nagłówków

# Wewnątrzgrupowy udział (transform nie zwija wierszy!)
df['udzial_w_dziale'] = df['pensja'] / df.groupby('dzial')['pensja'].transform('sum')

# Złączenia relacyjne z walidacją 1:m i indykatorem
df_polaczone = pd.merge(klienci, zamowienia, on='id', how='left', validate='1:m', indicator=True)
niesparowani = df_polaczone.query("_merge == 'left_only'")
```

---

## 📈 Wizualizacja: Matplotlib oraz Interaktywne Plotly Express

```python
# 1. Publikacyjny Matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

fig, ax = plt.subplots(figsize=(8, 4))
df_raport.plot(kind='bar', x='dzial', y='srednia_pensja', ax=ax, color='teal')
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x*1e-3:.0f}k zł'))
plt.tight_layout()
fig.savefig('wykres.png', dpi=300)

# 2. Interaktywne Plotly Express (HTML dla biznesu)
import plotly.express as px

fig = px.scatter(df, x='wiek', y='zarobki', color='dzial', hover_name='nazwisko', title="Raport Płac")
fig.write_html('raport_interaktywny.html')

# 3. Plotly jako natywny backend Pandas
# pd.options.plotting.backend = 'plotly'
# df.plot(kind='scatter', x='a', y='b')
```
