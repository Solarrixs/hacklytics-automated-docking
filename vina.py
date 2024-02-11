from pathlib import Path
import subprocess
import os
import shutil

pdb_dir = Path('./PDB')
ligand_dir = Path('./Ligand')
pdb_filepath = None
ligand_filepath = None

pdb_files = list(pdb_dir.glob('*.pdb'))
ligand_files = list(ligand_dir.glob('*.sdf'))

if pdb_files:
    pdb_file = pdb_files[0]
    receptorpath = str(pdb_file)

if ligand_files:
    ligand_file = ligand_files[0]
    ligandpath = str(ligand_file)

def run_vina(receptor_filepath, ligand_filepath, output_filepath, center, size, config_filepath=None):
    vina_executable = './vina'
    
    # Basic Vina command components
    command = [
        vina_executable,
        '--receptor', receptor_filepath,
        '--ligand', ligand_filepath,
        '--out', output_filepath,
        '--center_x', str(center[0]),
        '--center_y', str(center[1]),
        '--center_z', str(center[2]),
        '--size_x', str(size[0]),
        '--size_y', str(size[1]),
        '--size_z', str(size[2])
    ]
    
    # If a config file is provided, add it to the command
    if config_filepath is not None:
        command += ['--config', config_filepath]
    
    # Run Vina with the specified parameters
    subprocess.run(command, check=True)

receptor = receptorpath
ligand = ligandpath
output_folder = "./Docking"

if os.path.exists(output_folder):
    shutil.rmtree(output_folder)
os.makedirs(output_folder)

pdbqtreceptor = os.system("obabel " + receptor + " -xr -O " + os.path.join(output_folder, "Receptor.pdbqt"))
pdbqtligand = os.system("mk_prepare_ligand.py -i " + ligand + " -o " + os.path.join(output_folder, "Ligand.pdbqt"))

center = [0, 0, 0]
size = [100, 100, 100]

run_vina('./Docking/receptor.pdbqt', './Docking/Ligand.pdbqt', './Docking/Result.pdbqt', center, size)
