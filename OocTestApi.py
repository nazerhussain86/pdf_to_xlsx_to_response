import os
from urllib.parse import quote

import requests
import pandas as pd
import urllib3

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Function to upload an Excel file to an API and save the response
# Function to send the file path to the API and save the response
def send_file_path_to_api(api_url, file_path):
    try:

        # Add the file path as a query parameter
        params = {'files': file_path}

        # Send a GET request with the query parameter
        response = requests.get(api_url, params=params, verify=False)
        response.raise_for_status()  # Raise an error for bad status codes
        print(f"Sent file path: {file_path} to {api_url}")

        # Save the API response to a text file with the same name
        response_file_name = os.path.splitext(file_path)[0] + "_response.txt"
        with open(response_file_name, 'w') as response_file:
            response_file.write(f"Response for {file_path}:\n")
            response_file.write(response.text)
        print(f"API response saved to: {response_file_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send file path {file_path}: {e}")



download_dir = ""# Directory containing downloaded files

# API endpoint to upload files
api_url = "APIURL"

# Iterate over all files in the download directory
for file_name in os.listdir(download_dir):
    file_path = os.path.join(download_dir, file_name)

    # Check if the file is an Excel file
    if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        print(f"Processing Excel file: {file_name}")

        # Upload the Excel file to the API
        send_file_path_to_api(api_url, file_path)
    else:
        print(f"Skipping non-Excel file: {file_name}")

print("Excel file upload and response saving completed.")
