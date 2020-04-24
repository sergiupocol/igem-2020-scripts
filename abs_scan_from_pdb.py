# access PDB API from https://github.com/williamgilpin/pypdb.git
import sys
sys.path.insert(0, '../pypdb')
from pypdb import *
import json
import subprocess

# fill with the ids of proteins to be analyzed
# the pdb entries must correspond to the protein *complexed with its ligand(s)*
# TODO: add support to pdb files without the ligand by using CHIMERA to determine the 
# atomic position of the ligand
pdb_ids = ['4BBP', '6GV6'] # ZnuA - Zn, Metallothionein - Cd (Protein - Ligand) 


for id in pdb_ids:
	# API call to get PDB file
	pdb_file = get_pdb_file(id, filetype='pdb', compression=False)

	# generate a dict of the ligand
	ligand_dict = json.loads(get_ligands(id))
	ligand_name = ligand_dict['ligandInfo']['ligand']['chemicalName']
	
	het_line_index = pdb_file.find('HET    ' + ligand_name):]
	ligand_res_num = pdb_file[het_line_index+14:het_line_index+17] # based on PDB file format
	
	# write a pdb file
	file_name = id+'.pdb'
	file = open(file_name, "w")
	file.write(pdb_file)
	file.close()

	# Ensure ABS Scan exists in the current dir
	bash_command = "alanine_scanning.py -f {} -n {} -d 4.5 -o {}".format(file_name, ligand_res_num, id+'_scan')
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()






	
