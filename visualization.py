import streamlit as st
from streamlit_molstar import st_molstar
from pathlib import Path
from streamlit_molstar.auto import st_molstar_auto

st.set_page_config(layout="wide")

pdb_dir = Path('./PDB')
ligand_dir = Path('./Ligand')
pdb_filepath = None
ligand_filepath = None

pdb_files = list(pdb_dir.glob('*.pdb'))
ligand_files = list(ligand_dir.glob('*.sdf'))

if pdb_files:
    pdb_file = pdb_files[0]
    pdb_filepath = str(pdb_file)

if ligand_files:
    ligand_file = ligand_files[0]
    ligand_filepath = str(ligand_file)

# Viewer
st.write("Visualization of Receptor")
st_molstar(pdb_filepath, key='1', height="512px")

st.write("Visualization of Ligand")
st_molstar(ligand_filepath, key='2', height="512px")

st.write("Molecular Dynamics")
files = ['./Docking/Receptor.pdbqt', './Docking/Result.pdbqt']
st_molstar_auto(files, key="3", height="512px")

with open('./Docking/Result.pdbqt', 'r') as file:
    lines = file.readlines()
    if len(lines) > 2:
        secondline = lines[1]
        parts = secondline.split()
        result = " ".join(parts[1:4])
        st.write(result)