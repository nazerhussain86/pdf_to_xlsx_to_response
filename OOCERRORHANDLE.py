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
file_urls = ["https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/671106624122024INMAA1SB22301220241652.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/686810730122024INMAA4SB22301220241754.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/868407528032024INMAA1SB22290320241929.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/693608022012024INMAA1SB22230120241839.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/824813512032024INMAA1SB22130320241636.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/841773418032024INMAA1SB22200320241434.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/885840903042024INMAA1SB22170420241913.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/939721425042024INMAA1SB22010520241400.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/998845518052024INMAA1SB22200520241708.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/156276910062024INMAA1SB22120620241604.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/141409004062024INMAA1SB22130620241522.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/196017126062024INMAA1SB22040720241659.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/230949610072024INMAA1SB22110720241526.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/222337506072024INMAA1SB22120720241814.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/228749809072024INMAA1SB22120720241958.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/234969211072024INMAA4SB22120720242140.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/260167322072024INMAA1SB22250720241454.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/275077527072024INMAA1SB22010820241823.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/299985306082024INMAA1SB22070820241413.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/320156914082024INMAA4SB22160820241553.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/307949709082024INMAA1SB22170820241542.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/342769323082024INMAA4SB22230820241851.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/360299930082024INMAA4SB22030920240755.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/368163702092024INMAA1SB22040920241752.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/428323824092024INMAA4SB22240920242041.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/425867723092024INMAA1SB22250920241715.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/462719907102024INMAA1SB22081020242152.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/472727710102024INMAA1SB22141020241336.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/141041004062024INMAA1SB22141020241807.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/472794810102024INMAA1SB22141020241857.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/477074211102024INMAA1SB22161020241741.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/141041004062024INMAA1SB22171020241522.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/485860816102024INMAA1SB22181020241520.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/501084622102024INMAA1SB22231020241741.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/508653724102024INMAA1SB22251020241650.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/512962125102024INMAA4SB22261020241800.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/521124228102024INMAA1SB22291020241550.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/521227728102024INMAA1SB22291020241550.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/513769325102024INMAA4SB22021120242104.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/544248808112024INMAA4SB22081120241734.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/581458022112024INMAA4SB22271120241910.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/599606428112024INMAA4SB22291120242100.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/598050128112024INMAA4SB22291120242214.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/604692530112024INMAA1SB22021220242002.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/601128929112024INMAA1SB22041220241020.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/604692530112024INMAA1SB22091220241808.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/626222007122024INMAA1SB22101220240053.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/604692530112024INMAA1SB22101220240350.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/626165707122024INMAA1SB22101220240350.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/627836609122024INMAA1SB22111220241953.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/626385907122024INMAA1SB22181220241459.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/657931119122024INMAA4SB22201220241850.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/658901219122024INMAA4SB22201220241922.pdf",
"https://dms.impexcube.in/MailRead/Export/PRTR/CHN/pdf/656729118122024INMAA1SB22201220241956.pdf",]

# Directory to save downloaded files
download_dir = r"D:\READING_Files\PRTR\LECCOPYERRORHANDLE"
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