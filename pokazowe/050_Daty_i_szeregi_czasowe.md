# Moduł 050: Daty i Szeregi Czasowe (Time Series)

[⬅️ Poprzedni moduł: 040 (DataFrame i czyszczenie)](040_Praca_z_DataFrame_selekcja_czyszczenie.md) | [🏠 Spis treści](../README.md) | [➡️ Następny moduł: 060 (Transformacje i łączenie)](060_Transformacje_grupowanie_laczenie.md)

> **Materiały powiązane:**
>
> - Notatnik demonstracyjny: [050_Daty_i_szeregi_czasowe.ipynb](050_Daty_i_szeregi_czasowe.ipynb)
> - Notatnik z ćwiczeniami: [050_Zadania_Daty_i_szeregi_czasowe.ipynb](../cwiczenia/050_Zadania_Daty_i_szeregi_czasowe.ipynb)

---

## 1. Konwersja typów: `pd.to_datetime()` i `pd.to_numeric()`

W danych transakcyjnych daty i liczby rzadko przychodzą w czystej postaci.

### 1.1. Kluczowe parametry `pd.to_datetime()`

| Parametr | Dopuszczalne wartości | Domyślnie | Zastosowanie |
| :--- | :--- | :--- | :--- |
| `format` | Wzorce daty (`'%d.%m.%Y'`, `'%Y-%m-%d %H:%M:%S'`) | `None` | Podanie formatu przyspiesza parsowanie nawet 10–20x i eliminuje pomyłki między dniem a miesiącem. |
| `errors` | `'raise'`, `'coerce'`, `'ignore'` | `'raise'` | Opcja `'coerce'` wstawia `NaT` (*Not a Time*) zamiast rzucać wyjątek przy uszkodzonych wpisach (np. `'2024-02-30'` czy `'BRAK'`). |
| `dayfirst` | `True` / `False` | `False` | Przydatne w Europie. Przy dacie `'01/02/2024'` i `dayfirst=True` Pandas zinterpretuje ją jako 1 lutego, a nie 2 stycznia. |
| `utc` | `True` / `False` | `None` | Sprowadza znaczniki czasu do wspólnej strefy UTC. |

### 1.2. Czyszczenie liczb za pomocą `pd.to_numeric()`

```python
import pandas as pd

# errors='coerce' zamienia nieprawidłowe wartości tekstowe na np.nan
df = pd.DataFrame({'Cena_raw': ['12.50', '99.90', 'BRAK', '45.00']})
df['Cena_czysta'] = pd.to_numeric(df['Cena_raw'], errors='coerce')

# Wykrycie uszkodzonych rekordów:
uszkodzone = df[df['Cena_czysta'].isna()]
print("Uszkodzone wpisy:\n", uszkodzone)
```

---

## 2. Akcesor `.dt` i cechy kalendarzowe

Akcesor `.dt` udostępnia wektorowe metody i atrybuty dla kolumn z datami:

```python
import pandas as pd

daty_raw = ['01/05/2024 14:30', '15/06/2024 09:15', '31/12/2023', 'BŁĄD', '2024-07-01']

# Bezpieczne parsowanie z errors='coerce' i dayfirst=True
daty_czyste = pd.to_datetime(daty_raw, errors='coerce', dayfirst=True)
df_daty = pd.DataFrame({'Data': daty_czyste}).dropna()

# Wyciąganie składowych kalendarzowych
df_daty['Rok'] = df_daty['Data'].dt.year
df_daty['Miesiac'] = df_daty['Data'].dt.month
df_daty['DzienTygodnia'] = df_daty['Data'].dt.day_name()
df_daty['Kwartal'] = df_daty['Data'].dt.quarter
df_daty['CzyWeekend'] = df_daty['Data'].dt.dayofweek >= 5  # 5 = Sobota, 6 = Niedziela

# Arytmetyka na datach (np. termin płatności 14 dni)
df_daty['Termin_14dni'] = df_daty['Data'] + pd.Timedelta(days=14)
print(df_daty)
```

---

## 3. Strefy czasowe (Time Zones)

Gdy pracujesz z danymi z wielu stref czasowych:

```python
# 1. Nadanie strefy czasowej (tz_localize) - przejście od strefy naiwnej do świadomej:
ts_warszawa = pd.Timestamp('2024-05-15 10:00:00').tz_localize('Europe/Warsaw')

# 2. Przeliczenie do innej strefy (tz_convert) - przeliczenie godziny:
ts_nowy_jork = ts_warszawa.tz_convert('America/New_York')
ts_utc = ts_warszawa.tz_convert('UTC')

print(f"Warszawa:  {ts_warszawa}")
print(f"Nowy Jork: {ts_nowy_jork}")
print(f"UTC:       {ts_utc}")
```

---

## 4. Dni robocze i kalendarze biznesowe

```python
from pandas.tseries.offsets import CustomBusinessDay
import datetime

# Generowanie 10 kolejnych dni roboczych (od poniedziałku do piątku)
dni_robocze = pd.bdate_range(start='2024-05-01', periods=10)

# Definicja kalendarza z polskimi świętami
polskie_swieta = [
    datetime.date(2024, 1, 1),
    datetime.date(2024, 5, 1),
    datetime.date(2024, 5, 3),
    datetime.date(2024, 11, 11),
    datetime.date(2024, 12, 25)
]
pl_roboczy = CustomBusinessDay(holidays=polskie_swieta)

start = pd.Timestamp('2024-04-30')  # Wtorek przed majówką
kolejny_roboczy = start + pl_roboczy
# 1 maja to święto, więc kolejny dzień roboczy to czwartek 2 maja
print(f"Kolejny dzień roboczy po 30 kwietnia: {kolejny_roboczy.strftime('%Y-%m-%d')}")
```

---

## 5. Agregacje czasowe: `resample()`

`resample()` to odpowiednik `groupby()` dla szeregów z indeksem czasowym (`DatetimeIndex`):

```python
import numpy as np

np.random.seed(42)
os_godzinowa = pd.date_range('2024-01-01', periods=720, freq='h')  # 30 dni co godzinę
df_telemetria = pd.DataFrame({
    'Zuzycie_Pradu': np.random.uniform(5.0, 25.0, size=len(os_godzinowa)),
    'Temperatura': 18 + 5 * np.sin(np.linspace(0, 10, len(os_godzinowa)))
}, index=os_godzinowa)

# Downsampling: przejście z danych godzinowych do podsumowań dziennych ('D')
df_dzienne = df_telemetria.resample('D').agg({
    'Zuzycie_Pradu': 'sum',
    'Temperatura': ['mean', 'min', 'max']
})
print("Podsumowanie dzienne (Downsampling):")
print(df_dzienne.head(3))
```

---

## 6. Okna kroczące: `rolling` i `expanding`

Okna kroczące wygładzają wahania i pomagają analizować trendy w czasie:

```python
ceny = pd.Series(
    100 + np.cumsum(np.random.normal(0.2, 2.0, 180)),
    index=pd.date_range('2024-01-01', periods=180, freq='D'),
    name='Kurs'
)

# Średnia krocząca z 14 dni (SMA 14)
sma_14 = ceny.rolling(window=14, min_periods=5).mean()

# Odchylenie standardowe w oknie kroczącym
std_14 = ceny.rolling(window=14).std()

# Dynamiczne pasma zmienności
gorne_pasmo = sma_14 + 2 * std_14
dolne_pasmo = sma_14 - 2 * std_14
```

---

## 🎯 Ćwiczenia (w notatniku zadań)

W notatniku [050_Zadania_Daty_i_szeregi_czasowe.ipynb](../cwiczenia/050_Zadania_Daty_i_szeregi_czasowe.ipynb) przećwiczysz:

1. Parsowanie nieregularnych dat z `errors='coerce'` oraz filtrację błędnych wpisów (`NaT`).
2. Resampling szeregów czasowych do podsumowań dziennych sumy transakcji (`.resample('D').sum()`).
