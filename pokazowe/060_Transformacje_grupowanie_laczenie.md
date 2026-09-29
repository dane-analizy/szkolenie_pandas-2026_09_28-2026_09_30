# Moduł 060: Transformacje, Grupowanie i Łączenie Danych

[⬅️ Poprzedni moduł: 050 (Daty i szeregi czasowe)](050_Daty_i_szeregi_czasowe.md) | [🏠 Spis treści](../README.md) | [➡️ Następny moduł: 070 (Wizualizacja)](070_Wizualizacja_danych_Plotly.md)

> **Materiały powiązane:**
>
> - Notatnik demonstracyjny: [060_Transformacje_grupowanie_laczenie.ipynb](060_Transformacje_grupowanie_laczenie.ipynb)
> - Notatnik z ćwiczeniami: [060_Zadania_Grupowanie_i_laczenie.ipynb](../cwiczenia/060_Zadania_Grupowanie_i_laczenie.ipynb)

---

## 1. O co chodzi z parametrem `axis`?

Parametr `axis` często bywa mylący. Najprostsza reguła:

```
        axis=1  ('columns')  -->  Kierunek POZIOMY (w poprzek kolumn)
       ┌───────────┬───────────┬───────────┐
       │ Kolumna A │ Kolumna B │ Kolumna C │
       ├───────────┼───────────┼───────────┤
axis=0 │    10     │    20     │    30     │ ──> sum(axis=1) sumuje w poprzek wiersza: 60
('index')   40     │    50     │    60     │ ──> sum(axis=1) sumuje w poprzek wiersza: 150
  │    └───────────┴───────────┴───────────┘
  ▼          │           │           │
       sum(axis=0) sum(axis=0) sum(axis=0)
          liczy       liczy       liczy
          w pionie:   w pionie:   w pionie:
            50          70          90
```

### Zestawienie działania `axis=0` vs `axis=1`

| Metoda | `axis=0` (lub `'index'`) – domyślny | `axis=1` (lub `'columns'`) |
| :--- | :--- | :--- |
| **`df.sum()` / `mean()`** | Zwija wiersze **w pionie** (daje wynik dla każdej kolumny). | Sumuje **w poziomie** (daje wynik dla każdego wiersza). |
| **`pd.concat([df1, df2])`** | Dokleja wiersze **pod spodem** (wydłuża tabelę). | Dokleja kolumny **obok siebie** (poszerza tabelę). |
| **`df.drop('nazwa')`** | Usuwa **wiersz** o podanym indeksie. | Usuwa **kolumnę** (`df.drop('wiek', axis=1)`). |
| **`df.apply(funkcja)`** | Przekazuje do funkcji całą **kolumnę** jako `Series`. | Przekazuje do funkcji cały **wiersz** jako `Series`. |

```python
import pandas as pd
import numpy as np

df_oceny = pd.DataFrame({
    'Matematyka': [4, 5, 3],
    'Fizyka': [3, 4, 4],
    'Informatyka': [5, 5, 4]
}, index=['Uczeń_1', 'Uczeń_2', 'Uczeń_3'])

# axis=0: Średnia z każdego przedmiotu (w pionie)
print("Średnia per przedmiot (axis=0):\n", df_oceny.mean(axis=0))

# axis=1: Średnia każdego ucznia ze wszystkich przedmiotów (w poziomie)
print("\nŚrednia per uczeń (axis=1):\n", df_oceny.mean(axis=1))
```

---

## 2. Kiedy stosować `apply(axis=1)`, a kiedy wektoryzację?

`apply(..., axis=1)` jest czytelne, ale powolne, bo tworzy obiekt Pythona dla każdego wiersza. W kodzie produkcyjnym zastępuj je wektorowym `np.where`:

```python
df_zam = pd.DataFrame({
    'Klient': ['Firma A', 'Osoba B', 'Firma C'],
    'Kwota': [1500, 250, 4200],
    'Czy_Firma': [True, False, True]
})

# 1. Podejście wolne (apply axis=1):
def rabat_apply(row):
    return row['Kwota'] * 0.10 if (row['Czy_Firma'] and row['Kwota'] > 1000) else 0.0

df_zam['Rabat_apply'] = df_zam.apply(rabat_apply, axis=1)

# 2. Podejście wektorowe (np.where) — rzędy wielkości szybsze
warunek = (df_zam['Czy_Firma'] == True) & (df_zam['Kwota'] > 1000)
df_zam['Rabat_wektor'] = np.where(warunek, df_zam['Kwota'] * 0.10, 0.0)
```

---

## 3. Zmiana kształtu tabel: `pivot_table` vs `melt`

```python
df_sprzedaz = pd.DataFrame({
    'Data': ['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'],
    'Region': ['Północ', 'Południe', 'Północ', 'Południe'],
    'Produkt': ['Laptop', 'Laptop', 'Mysz', 'Laptop'],
    'Sprzedaz': [4000, 4200, 150, 4100]
})

# 1. pivot_table (układ szeroki — macierz)
tabela_przestawna = df_sprzedaz.pivot_table(
    values='Sprzedaz',
    index='Region',
    columns='Produkt',
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='SUMA'
)
print("Tabela przestawna:\n", tabela_przestawna)

# 2. melt (układ wąski / Tidy Data — spłaszczenie kolumn do wierszy)
df_szeroka = pd.DataFrame({
    'Kraj': ['Polska', 'Niemcy'],
    'Sprzedaz_Q1': [100, 400],
    'Sprzedaz_Q2': [120, 420]
})

df_waska = pd.melt(
    df_szeroka,
    id_vars=['Kraj'],
    value_vars=['Sprzedaz_Q1', 'Sprzedaz_Q2'],
    var_name='Kwartal',
    value_name='Przychod'
)
print("\nPo wykonaniu melt():\n", df_waska)
```

---

## 4. Agregacje `groupby`: `NamedAgg`, słowniki funkcji i `as_index`

### 4.1. `agg()` vs `aggregate()`

To dokładnie ta sama metoda — `agg` to oficjalny, powszechnie używany skrót.

### 4.2. Styl SQL: `as_index=False`

Domyślnie kolumna grupująca staje się indeksem. Dodanie `as_index=False` zostawia ją jako zwykłą kolumnę tabeli, tak jak w wyniku zapytania SQL `GROUP BY`:

```python
df_kadry = pd.DataFrame({
    'Dzial': ['IT', 'IT', 'IT', 'Marketing', 'Marketing', 'Finanse', 'Finanse'],
    'Pracownik': ['Jan', 'Anna', 'Tomasz', 'Ewa', 'Piotr', 'Krzysztof', 'Zofia'],
    'Pensja': [16000, 12000, 8000, 11000, 7500, 18000, 9000],
    'Staz': [5, 3, 1, 4, 2, 8, 3]
})

# Agregacja NamedAgg z as_index=False (płaskie kolumny, czysty raport):
raport = df_kadry.groupby('Dzial', as_index=False).agg(
    Liczba_Osob=('Pensja', 'count'),
    Srednia_Pensja=('Pensja', 'mean'),
    Max_Pensja=('Pensja', 'max'),
    Sredni_Staz=('Staz', 'mean')
)
print("Raport kadrowy (NamedAgg + as_index=False):")
print(raport)

# Agregacja ze słownikiem funkcji (tworzy MultiIndex w kolumnach):
agg_slownik = df_kadry.groupby('Dzial').agg({
    'Pensja': ['mean', 'max'],
    'Staz': ['min', 'max']
})
# Spłaszczenie dwupoziomowych nazw kolumn:
agg_slownik.columns = ['_'.join(c).strip('_') for c in agg_slownik.columns.values]
```

### 4.3. `transform()` — kalkulacja grupowa bez zwijania wierszy

`transform()` nie zwija wierszy do jednego na grupę, tylko zwraca wektor o identycznej długości jak wejściowa tabela. Przydaje się do wyliczania udziałów procentowych w grupie:

```python
budzet_dzialu = df_kadry.groupby('Dzial')['Pensja'].transform('sum')
df_kadry['Udzial_w_Budzecie'] = (df_kadry['Pensja'] / budzet_dzialu).round(3)
print("\nTabela z udziałem w budżecie działu:\n", df_kadry[['Dzial', 'Pracownik', 'Pensja', 'Udzial_w_Budzecie']])
```

---

## 5. Łączenie tabel: `pd.merge()` i walidacja

`pd.merge()` działa jak klauzula `JOIN` w relacyjnych bazach danych SQL:

```python
klienci = pd.DataFrame({
    'klient_id': [1, 2, 3, 4],
    'nazwisko': ['Kowalski', 'Nowak', 'Wiśniewski', 'Zielińska']
})

zamowienia = pd.DataFrame({
    'zamowienie_id': [101, 102, 103],
    'klient_id': [1, 2, 2],
    'kwota': [250.0, 490.0, 110.0]
})

# Bezpieczny merge z kontrolą relacji (validate='1:m') i weryfikacją dopasowania (_merge)
df_polaczone = pd.merge(
    klienci,
    zamowienia,
    on='klient_id',
    how='left',
    validate='1:m',     # Kontrola relacji: 1 klient -> wiele zamówień
    indicator=True      # Flagi dopasowania: 'both', 'left_only', 'right_only'
)

# Klienci, którzy jeszcze nie złożyli żadnego zamówienia:
nieaktywni = df_polaczone[df_polaczone['_merge'] == 'left_only']
print("Klienci bez zamówień:\n", nieaktywni[['klient_id', 'nazwisko']])
```

---

## 🎯 Ćwiczenia (w notatniku zadań)

W notatniku [060_Zadania_Grupowanie_i_laczenie.ipynb](../cwiczenia/060_Zadania_Grupowanie_i_laczenie.ipynb) przećwiczysz:

1. Agregacje grupowe `groupby` w stylu SQL ze składnią `NamedAgg` oraz `as_index=False` (płaskie kolumny bez MultiIndex).
2. Relacyjne złączenie `pd.merge` z jawną kontrolą integralności relacji (`validate='1:m'`).
