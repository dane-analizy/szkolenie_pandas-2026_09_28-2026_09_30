# Moduł 070: Wizualizacja Danych: Pandas, Matplotlib i Plotly Express

[⬅️ Poprzedni moduł: 060 (Transformacje i łączenie)](060_Transformacje_grupowanie_laczenie.md) | [🏠 Spis treści](../README.md) | [➡️ Następny moduł: 080 (Case Studies)](080_Case_Study_Igrzyska_Olimpijskie.md)

> **Materiały powiązane:**
>
> - Notatnik demonstracyjny: [070_Wizualizacja_danych_Plotly.ipynb](070_Wizualizacja_danych_Plotly.ipynb)
> - Notatnik z ćwiczeniami: [070_Zadania_Wizualizacja.ipynb](../cwiczenia/070_Zadania_Wizualizacja.ipynb)

---

## 1. Szybka eksploracja z `DataFrame.plot()`

Pandas pozwala rysować wykresy bezpośrednio z poziomu tabeli za pomocą metody `df.plot()`:

- `'line'` – wykres liniowy (domyślny, idealny dla szeregów czasowych).
- `'bar'` / `'barh'` – słupkowy pionowy / poziomy (dla kategorii).
- `'hist'` – histogram rozkładu częstości.
- `'box'` – wykres pudełkowy (kwartyle, mediana, outliery).
- `'scatter'` – wykres punktowy zależności dwóch zmiennych (`x` i `y`).

```python
import pandas as pd
import matplotlib.pyplot as plt

df_sprzedaz = pd.DataFrame({
    'Kategoria': ['Laptopy', 'Smartfony', 'Akcesoria', 'Audio'],
    'Sprzedaz_2023': [320_000, 450_000, 120_000, 180_000],
    'Sprzedaz_2024': [390_000, 510_000, 180_000, 175_000]
}).set_index('Kategoria')

# Szybki wykres słupkowy
df_sprzedaz.plot(kind='bar', figsize=(8, 4), title="Sprzedaż R/R")
plt.tight_layout()
plt.show()
```

---

## 2. Dopracowany wykres w Matplotlib: Obiektowe API (`fig, ax`)

Gdy wykres ma trafić do oficjalnego raportu, skorzystaj z obiektowego API (`fig, ax`), aby kontrolować każdy detal:

```python
import matplotlib.ticker as ticker

fig, ax = plt.subplots(figsize=(10, 5))

# Przekazujemy ax do metody Pandas
df_sprzedaz.plot(kind='bar', ax=ax, width=0.75, colormap='viridis', edgecolor='black')

# 1. Tytuł i podpisy osi
ax.set_title("Dynamika sprzedaży w kategoriach produktowych", fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel("Kategoria", fontsize=11)
ax.set_ylabel("Przychód ze sprzedaży", fontsize=11)
ax.set_xticklabels(df_sprzedaz.index, rotation=0)

# 2. Formatowanie osi Y za pomocą modułu ticker (np. 400 tys. zł)
formater_pln = ticker.FuncFormatter(lambda x, p: f'{x*1e-3:,.0f} tys. zł')
ax.yaxis.set_major_formatter(formater_pln)

# 3. Etykiety wartości nad słupkami (bar_label)
for container in ax.containers:
    ax.bar_label(container, fmt=lambda x: f'{x*1e-3:.0f}k', padding=3, fontsize=9)

# 4. Legenda poza wykresem
ax.legend(title="Rok", loc='upper left', bbox_to_anchor=(1.01, 1.0))
plt.tight_layout()
plt.show()
```

---

## 3. Statystyczny Seaborn: Macierz korelacji

```python
import seaborn as sns
import numpy as np

sns.set_theme(style="whitegrid")

df_dane = pd.DataFrame(np.random.randn(100, 4), columns=['Cena', 'Rabat', 'Liczba_Sztuk', 'Zysk'])
macierz_kor = df_dane.corr()

plt.figure(figsize=(7, 5))
sns.heatmap(macierz_kor, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1, linewidths=0.5)
plt.title("Macierz korelacji zmiennych biznesowych", fontsize=12, fontweight='bold')
plt.show()
```

---

## 4. Plotly Express (`px`) — interaktywność dla biznesu

Plotly Express generuje interaktywne wykresy w przeglądarce i notatniku:

- **Hover:** najechanie kursorem wyświetla szczegółowe wartości.
- **Zoom / Pan:** powiększanie i przesuwanie bez dopisywania kodu.
- **Legenda:** kliknięcie w element legendy wyłącza go lub izoluje serię.
- **Eksport do HTML:** gotowy raport można zapisać w jednym pliku HTML i wysłać mailem.

```python
import plotly.express as px
import numpy as np

df_klienci = pd.DataFrame({
    'Klient': [f'Klient_{i}' for i in range(1, 21)],
    'Wydatki_PLN': np.random.uniform(500, 15000, 20),
    'Liczba_Zamowien': np.random.randint(1, 25, 20),
    'Segment': np.random.choice(['VIP', 'Lojalny', 'Standard', 'Nowy'], 20),
    'Zadowolenie_NPS': np.random.randint(1, 11, 20)
})

# Interaktywny wykres punktowy (Scatter Plot)
fig = px.scatter(
    df_klienci,
    x='Wydatki_PLN',
    y='Liczba_Zamowien',
    color='Segment',
    size='Wydatki_PLN',
    hover_name='Klient',
    hover_data=['Zadowolenie_NPS'],
    title="Segmentacja klientów: wydatki a częstotliwość zakupów",
    template='plotly_white'
)
fig.show()

# Zapis do samodzielnego pliku HTML:
fig.write_html('raport_segmentacji.html')
```

### Wskazówka: Plotly jako bezpośredni backend w Pandas

```python
# Przełączenie domyślnego silnika rysowania na Plotly:
pd.options.plotting.backend = 'plotly'

# Teraz standardowe df.plot() tworzy interaktywne wykresy Plotly:
fig_pandas = df_klienci.plot(
    kind='scatter',
    x='Wydatki_PLN',
    y='Liczba_Zamowien',
    title="Wykres przez Pandas Plotting Backend"
)

# Przywrócenie domyślnego backendu:
pd.options.plotting.backend = 'matplotlib'
```

---

## 5. Eksport wykresów do plików graficznych

```python
# Wysoka rozdzielczość 300 DPI do prezentacji
fig.savefig('wykres_raport.png', dpi=300, bbox_inches='tight')

# Skalowalny format wektorowy SVG
fig.savefig('wykres_wektor.svg', format='svg', bbox_inches='tight')
```

---

## 🎯 Ćwiczenia (w notatniku zadań)

W notatniku [070_Zadania_Wizualizacja.ipynb](../cwiczenia/070_Zadania_Wizualizacja.ipynb) przećwiczysz:

1. Budowę interaktywnego wykresu słupkowego w Plotly Express (`px.bar`) z automatycznymi etykietami wartości (`text_auto=True`).
