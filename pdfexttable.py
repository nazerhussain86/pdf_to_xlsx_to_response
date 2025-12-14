import pdfplumber
import pandas as pd
import os
import re
from datetime import datetime

PDF_PATH = r"C:\Users\DELL\Downloads\HSN codes mapping guidance _251025_094630.pdf"
OUTPUT_DIR = r"C:\python files\pdf_output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

excel_output_file = os.path.join(
    OUTPUT_DIR, f"hsn_mapping_{timestamp}.xlsx"
)

json_output_file = os.path.join(
    OUTPUT_DIR, f"hsn_mapping_{timestamp}.json"
)

required_columns = {
    "sno": ["s. no", "s.no", "sl no", "sr no", "serial", "s no"],
    "chapter": ["chapter"],
    "hs_code": ["hs code", "hscode", "hsn", "itc", "itc-hs"],
    "description": ["description", "goods"],
    "department": ["ministry", "department"]
}

def clean_text(val):
    return str(val).strip() if val not in (None, "") else ""

def is_valid_hs(code):
    return bool(re.fullmatch(r"\d{2,8}", str(code).strip()))

final_rows = []

with pdfplumber.open(PDF_PATH) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
        print(f"Processing Page {page_number}")
        tables = page.extract_tables()

        for table in tables:
            if not table or len(table) <= 1:
                continue

            headers = [
                clean_text(h).lower() if h else f"col_{i}"
                for i, h in enumerate(table[0])
            ]

            df = pd.DataFrame(table[1:], columns=headers)
            df = df.loc[:, ~df.columns.duplicated()]
            df = df.applymap(clean_text)
            df.reset_index(drop=True, inplace=True)

            column_map = {}
            for std, keys in required_columns.items():
                for col in df.columns:
                    if any(k in col for k in keys):
                        column_map[std] = col
                        break

            if not {"chapter", "hs_code", "description", "department"}.issubset(column_map):
                continue

            df = df[
                df[column_map["hs_code"]].apply(is_valid_hs)
            ].reset_index(drop=True)

            merged_rows = []
            last_row = None

            for _, row in df.iterrows():
                if last_row is None:
                    last_row = row
                    continue

                if row[column_map["hs_code"]]:
                    merged_rows.append(last_row)
                    last_row = row
                else:
                    last_row[column_map["description"]] += " " + row[column_map["description"]]

            if last_row is not None:
                merged_rows.append(last_row)

            clean_df = pd.DataFrame(merged_rows)

            extracted = pd.DataFrame({
                "s_no": clean_df[column_map["sno"]] if "sno" in column_map else range(1, len(clean_df) + 1),
                "chapter": clean_df[column_map["chapter"]],
                "hs_code": clean_df[column_map["hs_code"]],
                "description": clean_df[column_map["description"]],
                "ministry_department": clean_df[column_map["department"]],
                "page": page_number
            })

            final_rows.append(extracted)

if final_rows:
    final_df = pd.concat(final_rows, ignore_index=True)
else:
    final_df = pd.DataFrame(
        columns=[
            "s_no",
            "chapter",
            "hs_code",
            "description",
            "ministry_department",
            "page"
        ]
    )

final_df.to_excel(excel_output_file, index=False)
final_df.to_json(json_output_file, orient="records", indent=2)

print("✅ Extraction completed")
print("Excel:", excel_output_file)
print("JSON :", json_output_file)
