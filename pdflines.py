import pdfplumber
import os
from datetime import datetime

PDF_PATH = r"C:\Users\DELL\Downloads\HSN codes mapping guidance _251025_094630.pdf"
OUTPUT_DIR = r"C:\python files\pdf_output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
txt_output_file = os.path.join(
    OUTPUT_DIR, f"pdf_lines_{timestamp}.txt"
)

with pdfplumber.open(PDF_PATH) as pdf, open(txt_output_file, "w", encoding="utf-8") as txt_file:
    for page_number, page in enumerate(pdf.pages, start=1):
        txt_file.write(f"\n===== PAGE {page_number} =====\n")

        text = page.extract_text()

        if not text:
            txt_file.write("[NO TEXT FOUND]\n")
            continue

        lines = text.split("\n")

        for line_no, line in enumerate(lines, start=1):
            clean_line = line.strip()
            if clean_line:
                txt_file.write(f"{clean_line}\n")

print("✅ Line-by-line extraction completed")
print("Saved at:", txt_output_file)
