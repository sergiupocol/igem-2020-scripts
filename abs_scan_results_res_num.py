import sys
sys.path.insert(0, '../pypdb')
from pypdb import *
from Bio.PDB import *
import pandas as pd
# OSPREY identifies residues by their peptide chain and residue number
# Given residue number from Alanine_Scanning_Binding_Energies_Result.csv
# AND the peptide chain from the pdb file, generate the osprey code
# The ABS Scan requires the specification of a LIGAND number

pdb_id = '2pt1' # CHANGE HERE
protein_name = 'FutA1'
ligand_name = 'SO4'
ligand_name_id = 'H_'+ligand_name
pdb_file_name = pdb_id + '.pdb'
ligand_res_number = 362 # SO4 in FutA1

# Grab the peptide chain the ligand is bound to
pdb_file = get_pdb_file(pdb_id, filetype='pdb', compression=False)


parser = PDBParser()
structure = parser.get_structure(protein_name, pdb_file_name)

# Now goal is to get chain containing ligand residue
# OSPREY requires a residue id which is comprised of
#   a hetero-flag (non-standard residue), sequence identifier (order in chain)
#   and an insertion code (for insertion mutations but since we're parsing wild
#   type protein it will always be 'A')

# Unfold residues then call get parent
ligand_chain = ''
ligand_id = (ligand_name_id, ligand_res_number, ' ')

# Go through avery chain
# if chain has a resiude w ligand_res_number
# then grab the residue and set ligand_chain
# " Residue object have the tuple (hetfield, resseq, icode) as id"
for model in structure:
    for chain in model:
        if chain.has_id(ligand_id):
            ligand_chain = chain.get_id()
            break

ligand_osprey_code = ligand_chain+ligand_name

# RESULTS file
result_file = pd.read_csv('Alanine_Scanning_Binding_Energies_Result.csv')

osprey_codes = []

for index, row in result_file.itterows():
    receptor = row['Receptor']
    res_name = receptor[:3]
    res_number = receptor[4:receptor[4:receptor.length].find('_')]
    res_id = (res_name, res_number, ' ')
    for model in structure:
        for chain in model:
            if chain.has_id(res_id):
                res_chain = chain.get_id()
                osprey_codes.append(res_chain+res_name)
                break
