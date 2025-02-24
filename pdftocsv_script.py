import pdfplumber
import pandas as pd
import re

pdf_path = "estratto_conto.pdf"
csv_path = "estratto_conto.csv"
transactions = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            for row in table[1:]:
                if len(row) >= 5:
                    date = row[0]
                    description = row[2]
                    uscita = row[3] if row[3] else "0"
                    entrata = row[4] if row[4] else "0"

                    uscita = float(uscita.replace(".", "").replace(",", ".")) if uscita.strip() else 0.0
                    entrata = float(entrata.replace(".", "").replace(",", ".")) if entrata.strip() else 0.0

                    transactions.append([date, description, uscita, entrata])

df = pd.DataFrame(transactions, columns=["Data", "Descrizione", "Uscite", "Entrate"])

df["Data"] = pd.to_datetime(df["Data"], format="%d.%m.%y").dt.strftime("%m-%d-%Y")

df.to_csv(csv_path, index=False, sep=";")

len(df), csv_path