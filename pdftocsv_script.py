import pdfplumber
import pandas as pd
import csv
import json
import pandas as pd

pdf_path = "estratto_conto.pdf"
csv_entrate_path = "estratto_conto_entrate.csv"
csv_uscite_path = "estratto_conto_uscite.csv"
keywords_path = "keywords_it.json"

def load_keywords(config_file):
    with open(config_file, 'r', encoding='utf-8') as file:
        return json.load(file)


def replace_descriptions(df, keywords_path):
    """
    Modifica il DataFrame sostituendo le descrizioni in base alle parole chiave fornite.
    Restituisce due DataFrame: uno per le entrate e uno per le uscite.
    
    :param df: DataFrame con colonne ['Data', 'Descrizione', 'Uscite', 'Entrate']
    :param keywords: Dizionario {parola_chiave: sostituzione}
    :return: df_uscite, df_entrate
    """

    keywords = load_keywords(keywords_path)
    def replace_description(desc):
        for key, replacement in keywords.items():
            if key.lower() in desc.lower():
                return replacement
        return desc

    df = df.copy()
    df["Descrizione"] = df["Descrizione"].apply(replace_description)

    df_uscite = df[df["Uscite"] > 0].copy()
    df_entrate = df[df["Entrate"] > 0].copy()

    return df_uscite, df_entrate


def convert_to_csv(pdf_path, csv_entrate_path, csv_uscite_path, keywords_path):
    transactions = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[2:-1]:
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
    
    df_uscite, df_entrate = replace_descriptions(df, keywords_path)
    df_entrate.to_csv(csv_entrate_path, sep=";", index=False, quoting=csv.QUOTE_ALL)
    df_uscite.to_csv(csv_uscite_path, sep=";", index=False, quoting=csv.QUOTE_ALL)

convert_to_csv(pdf_path, csv_entrate_path, csv_uscite_path, keywords_path)
