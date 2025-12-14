import json
import pandas as pd
import re

# ================= FILE PATHS =================
json_input_path = r"C:\python files\pdf_output\hsn_from_txt.json"
excel_input_path = r"C:\Users\DELL\Downloads\HSN_Consolidated_CLEAN (1).xlsx"
json_updated_only_path = r"C:\python files\pdf_output\hsn_updated_only.json"

# ================= EXCEL HEADER DETECTION =================
def read_excel_with_dynamic_header(xlsx, sheet_name):
    raw_df = pd.read_excel(xlsx, sheet_name=sheet_name, header=None)

    header_row_index = None
    for i in range(min(5, len(raw_df))):
        row_text = " ".join(raw_df.iloc[i].astype(str).str.lower())
        if "hs" in row_text and "code" in row_text and "description" in row_text:
            header_row_index = i
            break

    if header_row_index is None:
        return None

    df = pd.read_excel(xlsx, sheet_name=sheet_name, header=header_row_index)

    df.columns = (
        df.columns
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .str.lower()
    )
    return df

# ================= LOAD EXCEL =================
xlsx = pd.ExcelFile(excel_input_path)
excel_desc_map = {}

for sheet_name in xlsx.sheet_names:  # SKIP FIRST SHEET
    df = read_excel_with_dynamic_header(xlsx, sheet_name)
    if df is None:
        continue

    hsn_col = None
    desc_col = None

    for col in df.columns:
        if re.search(r"\bhs\b.*\bcode\b", col):
            hsn_col = col
        if "description" in col:
            desc_col = col

    if not hsn_col or not desc_col:
        continue

    df[hsn_col] = df[hsn_col].astype(str).str.strip()
    df[desc_col] = df[desc_col].astype(str).str.strip()

    excel_desc_map.update(dict(zip(df[hsn_col], df[desc_col])))

print("HSN records loaded from Excel:", len(excel_desc_map))

# ================= LOAD JSON =================
with open(json_input_path, "r", encoding="utf-8") as jf:
    json_data = json.load(jf)

updated_records = []
not_found = []

# ================= REPLACE & FILTER =================
for item in json_data:
    hsn = str(item.get("hsncode", "")).strip()

    if hsn in excel_desc_map:
        new_desc = excel_desc_map[hsn]

        if new_desc and new_desc != item.get("description", "").strip():
            item["description"] = new_desc

        updated_records.append({
            "sno": item.get("sno"),
            "chapter": item.get("chapter"),
            "hsCode": item.get("hsncode"),
            "description": item.get("description"),
            "ministry" : item.get("ministry_department"),
        })
    else:
        not_found.append(hsn)

# ================= SORT BY S.NO =================
updated_records = sorted(
    updated_records,
    key=lambda x: (
        int(x.get("chapter", 0)) if str(x.get("chapter", "")).isdigit() else 0,
        int(x.get("sno", 0)) if str(x.get("sno", "")).isdigit() else 0
    )
)


print("Total records:", len(updated_records))
# ================= SAVE UPDATED ONLY =================
with open(json_updated_only_path, "w", encoding="utf-8") as jf:
    json.dump(updated_records, jf, indent=2, ensure_ascii=False)

print("✅ Updated-only JSON created")
print("Updated records:", len(updated_records))
print("HSN not found:", len(set(not_found)))
print("Saved at:", json_updated_only_path)
