import requests
import os
import gzip
import shutil

def clear_and_ensure_directory(directory_path):
    """
    Clears the directory at directory_path of all files and subdirectories,
    then ensures that the directory exists by creating it if it does not.
    """
    if os.path.exists(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        os.makedirs(directory_path, exist_ok=True)

def download_and_unzip_pdb(pdb_id):
    gz_file_path = os.path.join(pdb_directory, f'{pdb_id}.pdb.gz')
    pdb_file_path = os.path.join(pdb_directory, f'{pdb_id}.pdb')

    url = f'https://files.rcsb.org/download/{pdb_id}.pdb.gz'

    try:
        response = requests.get(url)
        # Check for a non-existent PDB ID
        if response.status_code == 404:
            print(f"PDB ID {pdb_id} does not exist. Please check the ID and try again.")
            return
        response.raise_for_status()

        with open(gz_file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {pdb_id}.pdb.gz successfully to {gz_file_path}.")

        # Unzipping the .gz file
        with gzip.open(gz_file_path, 'rb') as gz_file:
            with open(pdb_file_path, 'wb') as pdb_file:
                shutil.copyfileobj(gz_file, pdb_file)
        print(f"Unzipped {pdb_id}.pdb.gz successfully to {pdb_file_path}.")

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
        
def fetch_pubchem_data(name_or_id, data_type):
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    compound_identifier = "cid" if name_or_id.isdigit() else "name"
    if data_type == 'TXT':
        url = f"{base_url}/compound/{compound_identifier}/{name_or_id}/property/InChI/TXT"
    elif data_type == 'PNG':
        url = f"{base_url}/compound/{compound_identifier}/{name_or_id}/PNG"
    elif data_type == 'SDF':
        url = f"{base_url}/compound/{compound_identifier}/{name_or_id}/SDF"
    else:
        print("Invalid data type specified.")
        return None

    response = requests.get(url)
    if response.status_code == 200:
        return response.content if data_type == 'PNG' else response.text
    else:
        print(f"Error fetching data: HTTP {response.status_code}")
        return None
    
# Setup
root = os.path.dirname(os.path.abspath(__file__))
pdb_directory = os.path.join(root, 'PDB')
ligand_directory = os.path.join(root, 'Ligand')
clear_and_ensure_directory(pdb_directory)
clear_and_ensure_directory(ligand_directory)

# Download RCSB Data
user_pdb_id = input("Enter the PDB ID you want to download: ").strip()
pdb = user_pdb_id
download_and_unzip_pdb(pdb)

# Download Ligand Data
name_or_id = input("Enter a PubChem name or ID: ")
data_types = ['TXT', 'PNG', 'SDF']

for data_type in data_types:
    data = fetch_pubchem_data(name_or_id, data_type)
    if data:
        # Construct the file path within the Ligand directory
        file_path = os.path.join(ligand_directory, f"{name_or_id}.{data_type.lower()}")
        if data_type == 'PNG':
            with open(file_path, 'wb') as file:
                file.write(data)
            print(f"Image saved as {file_path}")
        else:
            # For text and SDF data, handle as text
            with open(file_path, 'w') as file:
                file.write(data)
            print(f"Data saved as {file_path}")