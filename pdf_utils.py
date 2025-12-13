import pdfplumber
import re

def extract_page_text(pdf_path):
    """
    Returns list of dict:
    [
      { "page": 1, "text": "full page text" },
      ...
    ]
    """
    pages_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text()
            if not page_text:
                continue

            # Clean CID issues
            page_text = re.sub(r'\(cid:\d{1,3}\)', '', page_text)
            page_text = re.sub(r'\s+', ' ', page_text).strip()

            pages_data.append({
                "page": page_no,
                "text": page_text
            })

    return pages_data