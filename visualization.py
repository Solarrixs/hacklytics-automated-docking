import streamlit as st
from streamlit_molstar import st_molstar
from pathlib import Path
from streamlit_molstar.auto import st_molstar_auto
import time

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
st.write("Visualization of Receptor Binding Domain")
st_molstar(pdb_filepath, key='1', height="320px")

st.write("Visualization of Ligand")
st_molstar(ligand_filepath, key='2', height="320px")

st.write("Molecular Dynamics")
files = [pdb_filepath, ligand_filepath]
st_molstar_auto(files, key="3", height="320px")