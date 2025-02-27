import pdfplumber
import pandas as pd
import csv
import json
import pandas as pd

csv_path = "estratto_conto.csv"
csv_output_path = "estratto_conto_output.csv"
keywords_path = "keywords_ch.json"

def load_keywords(config_file):
    with open(config_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def convert_to_csv(csv_path, csv_output_path, keywords_path):
    df = pd.read_csv(csv_path, sep=";")
    keywords = load_keywords(keywords_path)

    def replace_description(desc):
        for key, replacement in keywords.items():
            if key.lower() in desc.lower():
                return replacement
        return desc

    df["Booking text"] = df["Booking text"].apply(replace_description)
    df["Date"] = pd.to_datetime(df["Date"], format="%d.%m.%Y").dt.strftime("%m-%d-%Y")
    df = df.sort_values(by="Date", ascending=True)
    df.to_csv(csv_output_path, index=False, sep=";")

convert_to_csv(csv_path, csv_output_path, keywords_path)
