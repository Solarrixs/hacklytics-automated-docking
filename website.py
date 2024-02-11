from taipy import Gui
import requests
import os
import gzip
import shutil
import streamlit as st
from streamlit_molstar import st_molstar
from pathlib import Path
from streamlit_molstar.auto import st_molstar_auto

def visualize_molecules():
    # Set Streamlit page configuration
    st.set_page_config(layout="wide")

    # Paths to directories
    pdb_dir = Path('./PDB')
    ligand_dir = Path('./Ligand')
    # Initialize filepaths
    pdb_filepath = None
    ligand_filepath = None

    # List PDB and ligand files
    pdb_files = list(pdb_dir.glob('*.pdb'))
    ligand_files = list(ligand_dir.glob('*.sdf'))

    # Select the first file found for visualization
    if pdb_files:
        pdb_filepath = str(pdb_files[0])

    if ligand_files:
        ligand_filepath = str(ligand_files[0])

    # Visualization
    if pdb_filepath:
        st.write("Visualization of Receptor Binding Domain")
        st_molstar(pdb_filepath, key='1', height="512px")

    if ligand_filepath:
        st.write("Visualization of Ligand")
        st_molstar(ligand_filepath, key='2', height="512px")

    if pdb_filepath and ligand_filepath:
        st.write("Molecular Dynamics")
        files = [pdb_filepath, ligand_filepath]
        st_molstar_auto(files, key="3", height="512px")
        
    # Open File
    os.system('streamlit run "/Users/maxxyung/Documents/Master Documents/004 Coding Projects/hacklytics-automated-docking/visualization.py"')

def clear_and_ensure_directory(directory_path):
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
        
def fetch_pubchem_data(name_or_id, data_type, state):
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
        state.error("Invalid PBD ID")
        print(f"Error fetching data: HTTP {response.status_code}")
        return None

# ------------ Front end portion -----------
    
pubchem_name = ""
error = ""
pdb_id = ""
content = ""
structure = "Molecular Structure: " 

def is_field_valid(pubchem_name, pdb_id):
    if len(pdb_id) == 0 and len(pubchem_name) == 0:
        return "Fill in the field"
    elif len(pdb_id) == 0:
        return "PDB ID field is empty."
    elif len(pubchem_name) == 0:
        return "PubChem Name field is empty."
    else:
        return ""

root = os.path.dirname(os.path.abspath(__file__))
pdb_directory = os.path.join(root, 'PDB')
ligand_directory = os.path.join(root, 'Ligand')
clear_and_ensure_directory(pdb_directory)
clear_and_ensure_directory(ligand_directory)

def handle_on_action(state):
    state.error = is_field_valid(state.pubchem_name, state.pdb_id)
    if len(state.error) != 0:
        return

    state.structure = "Molecular Structure: "
    state.content = ""
    # Download RCSB Data
    pdb = state.pdb_id
    download_and_unzip_pdb(pdb)

    # Download Ligand Data
    name_or_id = state.pubchem_name
    data_types = ['TXT', 'PNG', 'SDF']

    for data_type in data_types:
        data = fetch_pubchem_data(name_or_id, data_type, state)
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

    # file_path = "/Ligand/" + state.pubchem_name + ".txt"
    file_path = os.path.join(ligand_directory, f"{state.pubchem_name}.txt")
    with open(file_path, 'r') as file:
        file_content = file.read()
    state.structure += file_content

    state.content = "/Ligand/" + state.pubchem_name + ".png"
    
    state.pdb_id = ""
    state.pubchem_name = ""

page = """
<|2 6 2 |layout|

<|toggle|theme|>

<| 
## Affini Dock ## {: .text-center .h1}
<|layout|columns=1 1|
<|{content}|image|height=400px|width=400px|>

<|{structure}|text|>
|>
<|layout|columns=1 1|

<|
<|{pdb_id}|input|label=PBD ID|class_name=fullwidth|>{: .m1}
<|Compute|button|on_action=handle_on_action|label=Compute|>
<|Generate|button|on_action=visualize_molecules|label=Generate|>
|>

<|
<|{pubchem_name}|input|label=PubChem Name or ID|class_name=fullwidth|>{: .m1}
<|{error}|text|>{: .color-primary}
|>

|>
|>
|>
"""

my_theme = {
  "palette": {
    "image": {"borderColor": "#FFFFFF"},
  }
}

Gui(page).run(use_reloader=True, port=3002, theme=my_theme)