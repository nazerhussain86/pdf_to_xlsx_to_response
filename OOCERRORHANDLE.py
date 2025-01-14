import os
import requests
import pdfplumber
import pandas as pd


# Function to extract tables from a PDF and save them to an Excel file
def extract_tables_from_pdf_to_excel(pdf_path, excel_dir):
    try:
        # Extract file name without extension
        pdf_file_name = os.path.splitext(os.path.basename(pdf_path))[0]
        excel_path = os.path.join(excel_dir, f"{pdf_file_name}.xlsx")

        # Open the PDF file using the full path
        with pdfplumber.open(pdf_path) as pdf:
            # Create a writer object for Excel
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                # Iterate over each page
                for page_num, page in enumerate(pdf.pages):
                    # Extract tables from the page
                    tables = page.extract_tables()

                    if not tables:
                        print(f"No tables found on page {page_num + 1}.")
                        continue

                    # Process each table
                    for table_num, table in enumerate(tables):
                        # Convert table to DataFrame
                        df = pd.DataFrame(table[1:], columns=table[0])

                        # Generate a unique sheet name for each table
                        sheet_name = f"Page{page_num + 1}"
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        print(f"Table extracted from page {page_num + 1}.")

        print(f"Tables extracted and saved to: {excel_path}")
        return excel_path
    except Exception as e:
        print(f"An error occurred while processing {pdf_path}: {e}")
        return None


def download_file(url, save_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error for bad status codes
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")


# List of file URLs to download
file_urls = [] # give urls to download

# Directory to save downloaded files
download_dir = ""# Directory to save downloaded files
pdf_dir = os.path.join(download_dir, "pdf")
excel_dir = os.path.join(download_dir, "excel")

# Create directories if they don't exist
os.makedirs(pdf_dir, exist_ok=True)
os.makedirs(excel_dir, exist_ok=True)

# Download each file
for url in file_urls:
    file_name = os.path.basename(url)  # e.g., "file1.pdf"
    pdf_save_path = os.path.join(pdf_dir, file_name)

    # Download the file
    download_file(url, pdf_save_path)

    # Extract tables from the PDF and save to Excel
    excel_file_path = extract_tables_from_pdf_to_excel(pdf_save_path, excel_dir)

    if excel_file_path:
        print(f"Excel file created: {excel_file_path}")
    else:
        print(f"Failed to process {file_name}.")

print("Bulk download, upload, and response saving completed.")
