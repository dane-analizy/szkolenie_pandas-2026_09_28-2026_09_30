# Moduł 080: Case Studies – Letnie Igrzyska Olimpijskie (1896–2024)

[⬅️ Poprzedni moduł: 070 (Wizualizacja)](070_Wizualizacja_danych_Plotly.md) | [🏠 Spis treści](../README.md) | [➡️ Następny moduł: 090 (Wydajność i DuckDB)](090_Wydajnosc_i_Big_Data_DuckDB.md)

> **Materiały powiązane:**
>
> - Notatnik demonstracyjny (Warsztat na żywo): [080_Case_Study_Igrzyska_Olimpijskie.ipynb](080_Case_Study_Igrzyska_Olimpijskie.ipynb)
> - Notatnik z ćwiczeniami (Zadania domowe): [080_Zadania_Case_Studies_Domowe.ipynb](../cwiczenia/080_Zadania_Case_Studies_Domowe.ipynb)

---

## 🏆 Warsztat na żywo: 130 lat Letnich Igrzysk Olimpijskich (1896–2024)

### 1. Źródło danych i przygotowanie pliku

- **Zbiór danych:** Baza Letnich Igrzysk Olimpijskich z Kaggle (1896–2024).
- **Plik w repozytorium:** `../olimpics.zip` (zawiera plik `olympics_dataset.csv`).

> [!TIP]
> **Wypakowanie danych i wczytywanie ZIP w locie:**  
> Rozpakowanie archiwum (`unzip olimpics.zip`), zmiana nazwy z `olympics_dataset.csv` na `olympics.csv` czy wrzucenie pliku do katalogu roboczego to w końcu elementarz analityka (zaraz obok sprawdzania kodowania i separatorów). Co ważne: Pandas potrafi też wczytać plik CSV bezpośrednio ze skompresowanego archiwum ZIP bez wcześniejszego rozpakowywania na dysk: `pd.read_csv('../olimpics.zip')`.

---

### 2. Krok 1: Wczytanie, diagnostyka i optymalizacja typów

```python
import os
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Wczytanie danych z archiwum ZIP lub pliku rozpakowanego
if os.path.exists('../olimpics.zip'):
    df_raw = pd.read_csv('../olimpics.zip')
elif os.path.exists('olympics_dataset.csv'):
    df_raw = pd.read_csv('olympics_dataset.csv')
else:
    df_raw = pd.read_csv('olympics.csv')

# Ujednolicenie nazw kolumn i odrzucenie rekordów bez medalu
df_olimp = df_raw.rename(columns={'Name': 'Athlete', 'Team': 'Country'}).copy()
if 'Medal' in df_olimp.columns and 'No medal' in df_olimp['Medal'].values:
    df_olimp = df_olimp[df_olimp['Medal'] != 'No medal']

# 2. Optymalizacja pamięciowa: konwersja kolumn tekstowych na typ category
kolumny_tekstowe = ['City', 'Sport', 'Event', 'Country', 'Medal']
for col in kolumny_tekstowe:
    if col in df_olimp.columns:
        df_olimp[col] = df_olimp[col].astype('category')

print("Wymiary tabeli:", df_olimp.shape)
print("Zakres lat igrzysk:", sorted(df_olimp['Year'].unique()))
print(f"Liczba unikalnych sportowców: {df_olimp['Athlete'].nunique():,}")
print(f"Liczba reprezentowanych krajów: {df_olimp['Country'].nunique()}")
```

---

### 3. Krok 2: Analiza równouprawnienia płci (Gender Diversity)

Sprawdźmy, jak na przestrzeni dekad zmieniał się udział kobiet wśród medalistów:

```python
# Zliczamy medalistów w rozbiciu na płeć w poszczególnych edycjach
medalisci_plec = df_olimp.groupby(['Year', 'Sex']).size().unstack(fill_value=0)

# Udział procentowy kobiet na podium
medalisci_plec['Procent_Kobiet'] = (
    medalisci_plec['F'] / (medalisci_plec['F'] + medalisci_plec['M']) * 100
).round(1)

print("Udział kobiet w wybranych edycjach:")
print(medalisci_plec.loc[[1900, 1924, 1976, 2000, 2024], ['F', 'M', 'Procent_Kobiet']])

# Wizualizacja trendu w Plotly
fig_gender = px.line(
    medalisci_plec.reset_index(),
    x='Year',
    y='Procent_Kobiet',
    markers=True,
    title="Udział procentowy kobiet wśród medalistów Letnich Igrzysk Olimpijskich (1896-2024)",
    labels={'Year': 'Rok Igrzysk', 'Procent_Kobiet': '% Kobiet na podium'},
    template='plotly_white'
)
# fig_gender.show()
```

---

### 4. Krok 3: Ważony ranking medalowy sportowców (Gold=6, Silver=2, Bronze=1)

Samo sumowanie krążków bywa mylące — 3 złote medale to zupełnie inny sukces sportowy niż 3 brązy. Zastosujmy klasyczną wagową punktację:
$$\text{Ranking} = 6 \times \text{Złoto} + 2 \times \text{Srebro} + 1 \times \text{Brąz}$$

```python
# Macierz: Sportowiec x Medal
sportowcy_medale = df_olimp.pivot_table(
    index=['Athlete', 'Country', 'Sport'],
    columns='Medal',
    values='Year',
    aggfunc='count',
    fill_value=0
)[['Gold', 'Silver', 'Bronze']]

# Wyliczenie punktacji
sportowcy_medale['Punkty'] = (
    6 * sportowcy_medale['Gold'] + 
    2 * sportowcy_medale['Silver'] + 
    1 * sportowcy_medale['Bronze']
)
sportowcy_medale['Suma_Medali'] = sportowcy_medale.sum(axis=1) - sportowcy_medale['Punkty']

# Top 10 najbardziej utytułowanych sportowców wszech czasów
top10_sportowcow = sportowcy_medale.sort_values(by=['Punkty', 'Gold'], ascending=False).head(10)
print("Top 10 sportowców wszech czasów (ranking 6-2-1):")
print(top10_sportowcow[['Gold', 'Silver', 'Bronze', 'Punkty']])
```

---

### 5. Krok 4: Montreal 1976 – 73 zawodników a 26 medali

> [!WARNING]
> **Pułapka w danych sportowych:**  
> W surowym zbiorze na igrzyskach w Montrealu (1976) na podium stanęło aż **73 polskich sportowców**. Tymczasem według oficjalnej klasyfikacji olimpijskiej i [Wikipedii](https://pl.wikipedia.org/wiki/Letnie_Igrzyska_Olimpijskie_1976) Polska zdobyła w Montrealu **26 medali** (7 złotych, 6 srebrnych, 13 brązowych).  
> **Skąd ta różnica?**  
> W sportach drużynowych (np. historyczny złoty medal siatkarzy Huberta Wagnera) fizyczny krążek odbiera każdy z 12 zawodników i każdy ma swój wiersz w bazie. Jednak w klasyfikacji państw to wciąż **dokładnie jeden złoty medal** dla kraju w danej konkurencji.

#### Prawidłowa oficjalna agregacja osiągnięć kraju

Przed podsumowaniem dorobku państwa trzeba **usunąć duplikaty konkurencji** za pomocą parametru `subset`:

```python
# 1. Deduplikacja do poziomu unikalnej konkurencji medalowej kraju
df_oficjalne = df_olimp.drop_duplicates(
    subset=['Year', 'Country', 'Sport', 'Event', 'Medal']
).copy()

# 2. Weryfikacja Montrealu 1976 dla Polski
polska_1976 = df_oficjalne.query("Country in ['POL', 'Poland'] and Year == 1976")
bilans_1976 = polska_1976['Medal'].value_counts()[['Gold', 'Silver', 'Bronze']]
print("Oficjalny bilans Polski w Montrealu 1976 po deduplikacji:")
print(bilans_1976)
print("Łączna suma medali:", bilans_1976.sum())  # Dokładnie 26 medali!
```

---

### 6. Krok 5: Geopolityka w danych (Moskwa 1980 vs Los Angeles 1984)

Zobaczmy, jak w tabelach odbiły się wydarzenia polityczne XX wieku: bojkot Igrzysk w Moskwie (1980) przez USA i kraje zachodnie oraz rewanżowy bojkot Los Angeles (1984) przez ZSRR, Polskę i blok wschodni:

```python
# Kraje z medalami w Moskwie (1980):
kraje_moskwa = set(df_oficjalne[df_oficjalne['Year'] == 1980]['Country'].unique())

# Kraje z medalami w Los Angeles (1984):
kraje_la = set(df_oficjalne[df_oficjalne['Year'] == 1984]['Country'].unique())

# Kraje na podium w Moskwie, których zabrakło w Los Angeles:
kraje_bojkotujace_1984 = sorted(list(kraje_moskwa - kraje_la))
print("Kraje na podium w Moskwie 1980 nieobecne w LA 1984 (bojkot bloku wschodniego):")
print(kraje_bojkotujace_1984[:15])  # M.in. POL, URS, GDR, BUL, CUB, HUN
```

---

### 7. Krok 6: Oficjalna tabela medalowa wszech czasów i dorobek Polski

```python
# Tabela medalowa wszech czasów
tabela_medalowa = df_oficjalne.pivot_table(
    index='Country',
    columns='Medal',
    values='Event',
    aggfunc='count',
    fill_value=0
)[['Gold', 'Silver', 'Bronze']]

tabela_medalowa['Total'] = tabela_medalowa.sum(axis=1)

# Sortowanie: najpierw Złoto, potem Srebro, potem Brąz
ranking_krajow = tabela_medalowa.sort_values(
    by=['Gold', 'Silver', 'Bronze'],
    ascending=[False, False, False]
)

print("\nTop 10 potęg olimpijskich wszech czasów (oficjalna klasyfikacja MKOl):")
print(ranking_krajow.head(10))

# Profil medalowy Polski w kolejnych edycjach
polska_lata = df_oficjalne.query("Country in ['POL', 'Poland']").pivot_table(
    index='Year',
    columns='Medal',
    values='Event',
    aggfunc='count',
    fill_value=0
)[['Gold', 'Silver', 'Bronze']]
polska_lata['Total'] = polska_lata.sum(axis=1)

# Wykres słupkowy w Plotly Express ze skumulowanymi kruszcami
fig_polska = px.bar(
    polska_lata.reset_index(),
    x='Year',
    y=['Gold', 'Silver', 'Bronze'],
    title="Oficjalny dorobek medalowy Polski na Letnich Igrzyskach Olimpijskich (1896-2024)",
    labels={'Year': 'Rok Igrzysk', 'value': 'Liczba medali', 'variable': 'Kruszec'},
    color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'},
    barmode='stack',
    template='plotly_white'
)
# fig_polska.show()
```

---

## 🏠 Zadania do samodzielnej pracy w domu

W notatniku [080_Zadania_Case_Studies_Domowe.ipynb](../cwiczenia/080_Zadania_Case_Studies_Domowe.ipynb) znajdziesz zadania olimpijskie oraz dwa zaawansowane projekty domowe:

1. **Zadania olimpijskie (1–5):**
   - **Zadanie 1:** Dynamika równouprawnienia płci na podium w kolejnych edycjach igrzysk.
   - **Zadanie 2:** Ważony ranking medalowy sportowców w pływaniu (Złoto=6, Srebro=2, Brąz=1).
   - **Zadanie 3:** Analiza geopolityczna i skutki bojkotów (Moskwa 1980 vs Los Angeles 1984).
   - **Zadanie 4:** Paradoks Montrealu 1976 – deduplikacja medali w konkurencjach drużynowych do poziomu medali kraju.
   - **Zadanie 5:** Olimpijska długowieczność – sportowcy z medalami na co najmniej 5 różnych edycjach igrzysk.
2. **Zaawansowane projekty domowe (6–7):**
   - **Projekt 6: Analiza koszykowa (E-Commerce)** – badanie par produktów najczęściej kupowanych razem w ramach tego samego zamówienia (self-merge).
   - **Projekt 7: Wykrywanie bloków awarii w telemetrii przemysłowej** – identyfikacja i numerowanie ciągłych incydentów awarii za pomocą wektora różnic (`.diff()`) i sumy skumulowanej (`.cumsum()`).
   *(W notatniku przygotowano przykładowy, działający kod wzorcowy – można od niego zacząć jako punktu wyjścia do dalszych analiz i rozwijania tych projektów).*
