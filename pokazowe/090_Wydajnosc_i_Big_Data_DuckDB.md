# Moduł 090: Wydajność, Duże Zbiory Danych i DuckDB

[⬅️ Poprzedni moduł: 080 (Case Studies)](080_Case_Study_Igrzyska_Olimpijskie.md) | [🏠 Spis treści](../README.md) | [➡️ Bonus 1: Ściąga (Cheat Sheet)](100_Bonus_1_Pandas_Cheat_Sheet.md)

> **Materiały powiązane:**
>
> - Notatnik demonstracyjny: [090_Wydajnosc_i_Big_Data_DuckDB.ipynb](090_Wydajnosc_i_Big_Data_DuckDB.ipynb)
> - Notatnik z ćwiczeniami: [090_Zadania_Wydajnosc_i_optymalizacja.ipynb](../cwiczenia/090_Zadania_Wydajnosc_i_optymalizacja.ipynb)

---

## 1. Narzędzia pomiaru czasu w Jupyterze

Zanim zaczniesz cokolwiek optymalizować, zmierz faktyczny czas wykonania kodu:

| Komenda | Zakres | Liczba powtórzeń | Kiedy stosować? |
| :--- | :--- | :--- | :--- |
| **`%time`** | Jedna linia | 1 raz | Długie operacje wejścia/wyjścia (wczytywanie dużego pliku CSV, zapytanie do bazy). |
| **`%%time`** | Cała komórka | 1 raz | Całe bloki czyszczenia i transformacji danych. |
| **`%timeit`** | Jedna linia | Wiele powtórzeń w pętli | Porównywanie alternatywnych jednolinijkowców (np. `np.where` vs `.apply`). Uśrednia wynik. |
| **`%%timeit`** | Cała komórka | Wiele powtórzeń w pętli | Dokładne porównanie dwóch algorytmów. |

Przydatne parametry `%timeit`:

- `-n 10` — wykonaj 10 powtórzeń w każdej serii.
- `-r 3` — powtórz serię 3 razy i podaj najlepszy wynik.

---

## 2. 6 zasad wydajności w Pandas

---

### 1. Wektoryzacja zamiast pętli `for` i `iterrows()`

- **Na czym polega:** Zastąpienie pętli Pythona operacją na całych kolumnach: `df['c'] = df['a'] * df['b']`.
- **Dlaczego przyspiesza:** W standardowej pętli Pythona interpreter sprawdza typy i odpytuje obiekty przy każdym wierszu. Wektoryzacja deleguje pętlę do skompilowanego kodu C. Dane leżą w ciągłym bloku pamięci, a procesor przetwarza po kilka liczb w jednym cyklu zegara (**SIMD — Single Instruction, Multiple Data**).
- **Zysk:** **100x – 1000x szybciej**.
- **Praktyka:** Jeśli iteracja jest niezbędna (np. wysyłka maila per wiersz), używaj `df.itertuples()` zamiast `iterrows()`.

---

### 2. `np.where()` i `np.select()` zamiast `df.apply(axis=1)`

- **Na czym polega:** Wektorowy odpowiednik konstrukcji `if-else` oraz `if-elif-else`.
- **Dlaczego `apply(axis=1)` spowalnia kod:** Dla miliona wierszy Pandas tworzy i niszczy w pamięci milion obiektów `Series`. Funkcja `np.where(warunek, tak, nie)` operuje bezpośrednio na tablicach w C bez alokowania obiektów wierszy.
- **Zysk:** **50x – 150x szybciej**.

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({'Wartosc': np.random.randint(1, 100, 1_000_000)})

# Wolno:
# df['Klasa'] = df.apply(lambda r: 'Duża' if r['Wartosc'] > 50 else 'Mała', axis=1)

# Szybko (wektorowo):
df['Klasa'] = np.where(df['Wartosc'] > 50, 'Duża', 'Mała')
```

---

### 3. `pd.eval()` i `df.query()` (silnik numexpr i pamięć cache)

- **Na czym polega:** Zapisywanie złożonych formuł arytmetycznych w tekście: `df.eval('a * 2.5 + b ** 2')`.
- **Dlaczego przyspiesza:** Standardowe wyrażenie Pythona alokuje w RAM tablice pośrednie dla każdego kroku obliczeń. Silnik **`numexpr`** dzieli dane na kawałki mieszczące się w pamięci podręcznej procesora (Cache L1/L2) i liczy je bez ciągłego odwoływania się do pamięci RAM.
- **Zysk:** **2x – 5x szybciej** i mniejsze zużycie RAM przy tabelach powyżej 100 000 wierszy.

---

### 4. Obliczenia na surowym NumPy (`.to_numpy()`)

- **Na czym polega:** Pominięcie etykiet Pandas i wykonanie obliczeń bezpośrednio na macierzy `ndarray`: `df['kwota'].to_numpy()`.
- **Dlaczego przyspiesza:** Eliminuje narzut weryfikacji indeksów i kolumn przy czysto numerycznych algorytmach (np. symulacje Monte Carlo).
- **Zysk:** **20% – 50% przyspieszenia** względem natywnego Pandas.

---

### 5. Typowanie przy odczycie (`dtype`) zamiast downcastingu

- **Na czym polega:** Podanie mniejszych typów danych (np. `int32`, `float32`, `category`) już w parametrze `dtype={...}` metody `pd.read_csv()`.
- **Dlaczego to kluczowe:** Zmniejszanie typów po wczytaniu pliku (downcasting) wymaga, by cały zbiór najpierw załadował się do RAM w domyślnych, 8-bajtowych typach `int64`/`float64`. Prowadzi to do **piku pamięciowego (*Memory Peak*)**, który potrafi wywołać `MemoryError` jeszcze w trakcie parsowania pliku.
- **Zysk:** **Do 75% mniej zużytego RAM-u** i szybszy import.

---

### 6. Typ kategoryczny (`category`) dla powtarzających się tekstów

- **Na czym polega:** Zamiana kolumny tekstowej o małej liczbie unikalnych wartości (np. województwa, statusy, kraje) na typ `category`.
- **Dlaczego przyspiesza:** Zamiast powielać w pamięci długie napisy, Pandas tworzy słownik unikalnych wartości, a w kolumnie zapisuje 1-bajtowe liczby całkowite (`uint8`).
- **Zysk:** **80–90% oszczędności RAM** na kolumnach tekstowych.

```python
s_tekst = pd.Series(['Aktywny', 'Oczekujący', 'Anulowany'] * 200_000)
s_kategoria = s_tekst.astype('category')

pamiec_tekst = s_tekst.memory_usage(deep=True) / 1024 / 1024
pamiec_kat = s_kategoria.memory_usage(deep=True) / 1024 / 1024

print(f"Pamięć przed: {pamiec_tekst:.2f} MB")
print(f"Pamięć po (category): {pamiec_kat:.2f} MB (oszczędność: {(1 - pamiec_kat/pamiec_tekst)*100:.1f}%)")
```

---

## 3. Przetwarzanie wsadowe (Chunking)

Gdy plik CSV jest większy niż dostępna pamięć RAM, wczytujemy go partiami:

```python
suma_ogolna = 0.0
licznik_wierszy = 0

# Wczytywanie pliku w porcjach po 100 000 wierszy
for chunk in pd.read_csv('wielki_plik.csv', chunksize=100_000, usecols=['wartosc']):
    suma_ogolna += chunk['wartosc'].sum()
    licznik_wierszy += len(chunk)

print(f"Średnia bez przekroczenia pamięci RAM: {suma_ogolna / licznik_wierszy:.2f}")
```

---

## 4. DuckDB — analityczny silnik SQL w jednym procesie

DuckDB działa w tym samym procesie co Python. Pozwala odpytywać pliki Parquet oraz CSV bezpośrednio na dysku, bez wcześniejszego ładowania ich do pamięci RAM przez Pandas:

```python
import duckdb

# Wykonanie zapytania SQL bezpośrednio na plikach Parquet z dysku
zapytanie = """
    SELECT 
        kategoria, 
        COUNT(*) AS liczba_zamowien, 
        ROUND(AVG(kwota_pln), 2) AS srednia_wartosc
    FROM 'dane/*.parquet'
    WHERE status = 'OPLACONE'
    GROUP BY kategoria
    ORDER BY srednia_wartosc DESC
"""

df_wynik = duckdb.query(zapytanie).to_df()
print("Wynik analityczny z DuckDB:")
print(df_wynik)
```

---

## 🎯 Ćwiczenia (w notatniku zadań)

W notatniku [090_Zadania_Wydajnosc_i_optymalizacja.ipynb](../cwiczenia/090_Zadania_Wydajnosc_i_optymalizacja.ipynb) przećwiczysz:

1. Optymalizację pamięci RAM poprzez konwersję kolumn tekstowych na typ kategoryczny (`.astype('category')`) oraz weryfikację oszczędności metodą `.memory_usage(deep=True)`.
