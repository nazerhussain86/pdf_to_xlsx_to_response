import pdfplumber
import pandas as pd
import os
from datetime import datetime

PDF_PATH = r"C:\Users\DELL\Downloads\HSN codes mapping guidance _251025_094630.pdf"
OUTPUT_DIR = r"C:\python files\pdf_output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

text_output_file = os.path.join(
    OUTPUT_DIR, f"extracted_text_{timestamp}.txt"
)

excel_output_file = os.path.join(
    OUTPUT_DIR, f"extracted_tables_{timestamp}.xlsx"
)

all_tables = []
page_table_map = []

with pdfplumber.open(PDF_PATH) as pdf, open(text_output_file, "w", encoding="utf-8") as txt_file:
    for page_number, page in enumerate(pdf.pages, start=1):
        print(f"Processing Page {page_number}")

        text = page.extract_text()
        if text:
            txt_file.write(f"\n--- PAGE {page_number} ---\n")
            txt_file.write(text + "\n")
        else:
            txt_file.write(f"\n--- PAGE {page_number} ---\nNO TEXT FOUND\n")

        tables = page.extract_tables()

        for table_index, table in enumerate(tables):
            if not table or len(table) <= 1:
                continue

            headers = table[0]
            headers = [
                str(h).strip() if h not in (None, "") else f"Column_{i}"
                for i, h in enumerate(headers)
            ]

            df = pd.DataFrame(table[1:], columns=headers)

            df = df.loc[:, ~df.columns.duplicated()]
            df.reset_index(drop=True, inplace=True)

            df["Page"] = page_number
            df["TableNo"] = table_index + 1

            all_tables.append(df)

if all_tables:
    final_df = pd.concat(all_tables, ignore_index=True, sort=False)
    final_df.to_excel(excel_output_file, index=False)

print("Extraction completed")
print(text_output_file)
print(excel_output_file)
