import re
import json

txt_file_path = r"C:\python files\pdf_output\pdf_lines_2025-12-13_21-30.txt"
json_output_path = r"C:\python files\pdf_output\hsn_from_txt.json"

records = []

current_ministry = None
in_table = False
current_record = None
desc_buffer = []

with open(txt_file_path, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

for line in lines:

    # -------- STOP CONDITION --------
    if line.startswith("1 The HS Codes pertaining to"):
        in_table = False
        continue

    # -------- MINISTRY DETECTION --------
    if line.startswith("D/o ") or line.startswith("M/o "):
        current_ministry = line
        continue

    # -------- TABLE START --------
    if line.upper().startswith("S.NO.") and "HS CODE" in line.upper():
        in_table = True
        current_record = None
        desc_buffer = []
        continue

    if not in_table:
        continue

    # -------- NUMBER ROW (CORE PATTERN) --------
    # Matches:
    # 1 6 6011000
    # 2 6 6012010 BULBS HORTICULTURAL
    match = re.match(r"^(\d+)\s+(\d+)\s+(\d{4,8})(.*)", line)

    if match:
        # Save previous record
        if current_record:
            current_record["description"] = " ".join(desc_buffer).strip()
            records.append(current_record)
            desc_buffer = []

        sno, chapter, hsn, trailing_desc = match.groups()

        current_record = {
            "sno": int(sno),
            "chapter": chapter.zfill(2),
            "hsncode": hsn,
            "description": "",
            "ministry_department": current_ministry
        }

        if trailing_desc.strip():
            desc_buffer.append(trailing_desc.strip())

        continue

    # -------- DESCRIPTION CONTINUATION --------
    if current_record:
        desc_buffer.append(line)

# -------- SAVE LAST RECORD --------
if current_record:
    current_record["description"] = " ".join(desc_buffer).strip()
    records.append(current_record)

# -------- SAVE JSON --------
with open(json_output_path, "w", encoding="utf-8") as jf:
    json.dump(records, jf, indent=2, ensure_ascii=False)

print("✅ Extraction completed")
print("Total records:", len(records))
print("Saved JSON at:", json_output_path)
