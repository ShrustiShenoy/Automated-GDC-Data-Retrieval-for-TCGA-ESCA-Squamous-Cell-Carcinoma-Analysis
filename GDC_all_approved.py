import requests
import json
import os
import re

def sanitize_filename(filename):
    sanitized_name = re.sub(r'[\\/*?:"<>|]', "_", filename)
    return sanitized_name
    
# Define the file formats to EXCLUDE
excluded_formats = ["MAF", "PDF","HTML","SVS"]  # Add more formats as needed

filters = {
    "op": "and",
    "content": [
        {"op": "in", "content": {"field": "cases.project.project_id", "value": ["TCGA-ESCA"]}},
        {"op": "in", "content": {"field": "cases.disease_type", "value": ["Squamous Cell Neoplasms"]}},
        {"op": "in", "content": {"field": "files.access", "value": ["open"]}},
        {"op": "not in", "content": {"field": "files.data_format", "value": excluded_formats}},
        {"op": "in", "content": {"field": "files.data_category", "value": ["Copy Number Variation", "Simple Nucleotide Variation"]}}
        #{"op": "not in", "content": {"field": "files.data_format", "value": ["MAF", "SVS","XML","PDF"]}}
        #{"op": "in", "content": {"field": "files.analysis.experimental_strategy", "value": ["Whole genome sequencing", "Whole exome sequencing"]}},
        
    ],
}

url = "https://api.gdc.cancer.gov/files"
params = {
    "filters": json.dumps(filters),
    "format": "JSON",
    "size": "1000",
    "fields": "file_id,file_name,data_category,data_type,access",
}

response = requests.get(url, params=params)

print("API Response:", response.status_code)
print(json.dumps(response.json(), indent=4))

if response.status_code == 200:
    data = response.json()
    file_list = [(file["file_id"], file["file_name"], file["data_category"], file["data_type"], file["access"]) 
                  for file in data["data"]["hits"]]
    
    if not file_list:
        print("⚠️ No open-access files found for Squamous Cell Neoplasms in TCGA-ESCA.")
    else:
        print(f"✅ Found {len(file_list)} open-access files.")

        def download_file(file_id, file_name, download_folder="downloads"):
            # Create directory (and parents if needed) safely
            os.makedirs(download_folder, exist_ok=True)  # Key fix: atomic directory creation

            sanitized_name = sanitize_filename(file_name)
            file_path = os.path.join(download_folder, sanitized_name)

            # Guard against directory collisions
            if os.path.isdir(file_path):
                print(f"❌ Error: {file_path} is a directory.")
                return

            download_url = f"https://api.gdc.cancer.gov/data/{file_id}"
            
            try:
                with requests.get(download_url, stream=True) as file_response:
                    file_response.raise_for_status()  # Raise HTTP errors
                    with open(file_path, "wb") as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                print(f"✅ Downloaded: {file_name}")
            except Exception as e:
                print(f"❌ Failed to download {file_name}: {str(e)}")

        for file_id, file_name, data_category, data_type, access in file_list:
            print(f"File: {file_name} | Category: {data_category} | Type: {data_type} | Access: {access}")
            download_file(file_id, file_name)
            
else:
    print(f"❌ API request failed. Status code: {response.status_code}")