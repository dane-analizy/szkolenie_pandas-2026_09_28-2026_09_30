# Moduł 030: Praca ze Strukturą Series

[⬅️ Poprzedni moduł: 020 (Wczytywanie i eksport)](020_Wczytywanie_i_eksport_danych.md) | [🏠 Spis treści](../README.md) | [➡️ Następny moduł: 040 (DataFrame i czyszczenie)](040_Praca_z_DataFrame_selekcja_czyszczenie.md)

> **Materiały powiązane:**
>
> - Notatnik demonstracyjny: [030_Praca_ze_struktura_Series.ipynb](030_Praca_ze_struktura_Series.ipynb)
> - Notatnik z ćwiczeniami: [030_Zadania_Series.ipynb](../cwiczenia/030_Zadania_Series.ipynb)

---

## 1. Tworzenie Series i statystyki opisowe

`pd.Series` to jednowymiarowa tablica z etykietowanym indeksem. Każda kolumna w tabeli `DataFrame` to pod spodem właśnie obiekt `Series`.

```python
import pandas as pd
import numpy as np

# Tworzenie serii z własnym indeksem i nazwą
ceny = pd.Series(
    [12.50, 45.00, 8.99, 120.00, 24.50, 65.00, 45.00], 
    index=['Kawa', 'Herbata', 'Woda', 'Wino', 'Sok', 'Miód', 'Ciastko'],
    name='Cena_PLN'
)

# Podstawowe atrybuty diagnostyczne
print("Liczba elementów (.size):", ceny.size)
print("Typ danych (.dtype):", ceny.dtype)
print("Indeks etykiet (.index):", ceny.index)
print("Czyste wartości NumPy (.values):", ceny.values)

# Wartości unikalne: .unique() vs .nunique()
print("\nTablica unikalnych cen (.unique()):", ceny.unique())
print("Liczba unikalnych cen (.nunique()):", ceny.nunique())

# Statystyki opisowe (.describe()) dla liczb
print("\nRaport statystyczny (.describe()):")
print(ceny.describe())

# .describe() dla tekstu lub kategorii
miasta = pd.Series(['Warszawa', 'Kraków', 'Warszawa', 'Gdańsk', 'Warszawa'])
print("\nRaport describe() dla tekstu (count, unique, top, freq):")
print(miasta.describe())
```

---

## 2. Wybieranie danych: `loc`, `iloc` i wycinki

W `Series` masz dwa sposoby adresowania:

1. **Po etykietach (`loc`):** Przedział jest **domknięty obustronnie** — wycinek `'Kawa':'Woda'` zawiera również element `'Woda'`.
2. **Po pozycjach liczbowych (`iloc`):** Standard Pythona — lewostronnie domknięty, prawostronnie otwarty `[start:stop]`, czyli bez elementu `stop`.

```python
# 1. Pojedynczy element (skalar)
p1_nazwa = ceny['Kawa']         # Po etykiecie (12.50)
p1_loc = ceny.loc['Kawa']       # Jawne .loc po etykiecie (12.50)
p1_iloc = ceny.iloc[0]          # Po pozycji 0 (12.50)
p1_fast = ceny.iat[0]           # Najszybszy dostęp w C (do pojedynczych wartości)

# 2. Lista elementów (wymaga podwójnych nawiasów)
p2_etykiety = ceny[['Kawa', 'Wino']]
p2_pozycje = ceny.iloc[[0, 3]]

# 3. Wycinki zakresów (slicing)
wycinek_loc = ceny.loc['Kawa':'Woda']      # Zawiera: Kawa, Herbata, Woda (obustronnie domknięty)
wycinek_iloc = ceny.iloc[0:2]              # Tylko pozycje 0 i 1 (bez pozycji 2)

# 4. Krok i odwracanie kolejności
ostatni = ceny.iloc[-1]                    # Ostatni element
co_drugi = ceny.iloc[::2]                  # Co drugi element
odwrocona = ceny.iloc[::-1]                # Odwrócenie kolejności

# 5. Filtrowanie warunkiem logicznym (maska boolowska)
tanie = ceny[ceny < 20.0]
srednia_polka = ceny[(ceny >= 20.0) & (ceny <= 80.0)]  # Przy & oraz | nawiasy () są obowiązkowe
```

---

## 3. Resetowanie indeksu (`reset_index`)

- **`reset_index()`:** Przekształca dotychczasowy indeks w zwykłą kolumnę nowego obiektu `DataFrame`.
- **`reset_index(drop=True)`:** Wyrzuca stary indeks do kosza i przywraca czysty licznik `0, 1, 2, ...` bez zmiany obiektu na `DataFrame`.

```python
drogie = ceny[ceny > 30.0]
print("Przed resetem (stary indeks):\n", drogie)

# Porzucenie starego indeksu z drop=True:
drogie_czyste = drogie.reset_index(drop=True)
print("\nPo reset_index(drop=True):\n", drogie_czyste)
```

---

## 4. Arytmetyka i dopasowanie indeksów (Index Alignment)

Gdy dodajesz lub mnożysz dwie serie, Pandas łączy elementy **po nazwach indeksów**, a nie po ich kolejności w pamięci:

```python
stan_a = pd.Series([10, 20, 30], index=['Jabłka', 'Banany', 'Pomarańcze'])
stan_b = pd.Series([5, 15, 25], index=['Banany', 'Gruszki', 'Jabłka'])

# Zwykłe dodawanie: elementy obecne tylko w jednym sklepie dadzą NaN!
suma = stan_a + stan_b
print("Suma zapasów (NaN dla Gruszek i Pomarańczy):")
print(suma)

# Bezpieczne dodawanie: .add() z parametrem fill_value=0
suma_bezpieczna = stan_a.add(stan_b, fill_value=0)
print("\nSuma bezpieczna (brakujące pozycje potraktowane jako 0):")
print(suma_bezpieczna)
```

---

## 5. Agregacje i wartości skrajne (`sum`, `mean`, `nlargest`)

```python
wyniki = pd.Series([120, 450, 890, 230, 1100, 450, 75], name='Punkty')

# 1. Podstawowe statystyki
print("Suma (.sum()):", wyniki.sum())
print("Średnia (.mean()):", wyniki.mean())
print("Mediana (.median()):", wyniki.median())
print("Minimum (.min()):", wyniki.min())
print("Maksimum (.max()):", wyniki.max())
print("Odchylenie standardowe (.std()):", wyniki.std())
print("Wariancja (.var()):", wyniki.var())

# Różnica między .count() a .size:
# .count() zlicza tylko wartości niepuste (bez NaN), a .size zlicza wszystkie komórki
print("Liczba wartości bez NaN (.count()):", wyniki.count())

# 2. Szybkie wyciąganie skrajnych wartości: .nlargest() i .nsmallest()
top3 = wyniki.nlargest(3)
print("\nTop 3 najwyższe wyniki (.nlargest(3)):")
print(top3)

bottom2 = wyniki.nsmallest(2)
print("\n2 najniższe wyniki (.nsmallest(2)):")
print(bottom2)
```

> [!TIP]
> **Dlaczego `.nlargest(n)` zamiast `.sort_values().tail(n)`?**  
> Metoda `.nlargest()` korzysta z algorytmu kopca (*heap queue* o złożoności $O(N \log k)$). Nie musi sortować całego wektora w pamięci, więc działa znacznie szybciej przy dużych zbiorach danych.

---

## 6. Braki danych: `isnull().sum()`, `dropna()` i `fillna()`

```python
s_braki = pd.Series([10.0, np.nan, 25.0, None, 40.0, np.nan], index=['a', 'b', 'c', 'd', 'e', 'f'])

# 1. Wykrywanie braków: .isna() oraz .isnull() (tożsame metody)
print("Liczba braków (.isnull().sum()):", s_braki.isnull().sum())
print("Maska poprawnych komórek (.notna()):\n", s_braki.notna())

# 2. Usuwanie braków (.dropna())
czyste = s_braki.dropna()
print("\nPo usunięciu braków (.dropna()):\n", czyste)

# 3. Wypełnianie braków (.fillna())
wypelnione_zero = s_braki.fillna(0.0)

# Wypełnienie średnią z pozostałych elementów:
wypelnione_srednia = s_braki.fillna(s_braki.mean())
print("\nWypełnione średnią:", wypelnione_srednia)

# 4. Propagacja wartości w czasie (ffill i bfill — szeregi czasowe, finanse)
wypelnione_ffill = s_braki.ffill()  # Przenosi ostatnią znaną wartość w przód
wypelnione_bfill = s_braki.bfill()  # Pobiera najbliższą znaną wartość z przyszłości
```

---

## 7. Sortowanie i częstości: `sort_values`, `sort_index` i `value_counts`

```python
dane_sprzedaz = pd.Series([120.0, 45.0, 890.0, np.nan, 45.0], index=['Kawa', 'Herbata', 'Ekspres', 'Serwis', 'Filiżanka'])

# 1. Sortowanie po wartościach (sort_values)
print("Ceny rosnąco:\n", dane_sprzedaz.sort_values(ascending=True))
print("\nCeny malejąco z brakami na początku (na_position='first'):\n", 
      dane_sprzedaz.sort_values(ascending=False, na_position='first'))

# 2. Sortowanie po indeksie (sort_index)
print("\nAlfabetycznie po nazwach:\n", dane_sprzedaz.sort_index())

# 3. Zliczanie wystąpień wartości (value_counts)
statusy = pd.Series(['Aktywny', 'VIP', 'Aktywny', 'Nowy', None, 'VIP', 'Aktywny'])
print("\nLiczba wystąpień statusów:")
print(statusy.value_counts())

print("\nUdziały procentowe z uwzględnieniem braków (normalize=True, dropna=False):")
print(statusy.value_counts(normalize=True, dropna=False).round(2) * 100)

# 4. Sprawdzanie unikalności
print("\nCzy wartości są unikalne? (.is_unique):", statusy.is_unique)
print("Unikalne wpisy (.unique()):", statusy.dropna().unique())
print("Liczba unikalnych kategorii (.nunique()):", statusy.nunique())
```

---

## 8. Transformacja danych: `map()` vs `apply()`

| Metoda | Kiedy stosować? | Przykład | Szybkość |
| :--- | :--- | :--- | :--- |
| **`Series.map()`** | Zamiana wartości słownikiem lub prostą funkcją 1-do-1 | `s.map({'PL': 'Polska', 'DE': 'Niemcy'})` | Bardzo szybka (wewnętrzny C) |
| **`Series.apply()`** | Dowolna funkcja Pythona z dodatkowymi parametrami | `s.apply(moja_funkcja, prog=50)` | Wolniejsza (zwykła pętla Pythona) |

---

## 🎯 Ćwiczenia (w notatniku zadań)

W notatniku [030_Zadania_Series.ipynb](../cwiczenia/030_Zadania_Series.ipynb) przećwiczysz:

1. Statystyki opisowe, badanie braków (`.isnull().sum()`), imputację średnią (`.fillna()`) oraz wyciąganie wartości skrajnych (`.nlargest(2)`).
2. Slicing warunkowy oraz resetowanie indeksu z usunięciem starych etykiet (`drop=True`).
