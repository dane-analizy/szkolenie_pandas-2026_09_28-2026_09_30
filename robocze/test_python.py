import pandas as pd

df = pd.DataFrame(
    {
        "Klient": [
            "Jan Kowalski",
            "Anna Nowak",
            "Piotr Wiśniewski",
            "Maria Dąbrowska",
            "Tomasz Lis",
        ],
        "Wiek": [28, 42, 35, 22, 51],
        "Miasto": ["Warszawa", "Kraków", "Warszawa", "Gdańsk", "Kraków"],
        "Kwota_Zakupow": [1250.50, 4300.00, 890.20, 310.00, 2150.00],
        "Status": ["Aktywny", "VIP", "Aktywny", "Nowy", "VIP"],
    }
)

print("start")

print(df)

print("----------------")

print(df.to_markdown(index=False))

print("stop")
