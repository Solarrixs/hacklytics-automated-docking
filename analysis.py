from pathlib import Path
import deepchem as dc

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

print(dc.deepchem.dock.ConvexHullPocketFinder.find_pockets(pdb_filepath, ligand_filepath))