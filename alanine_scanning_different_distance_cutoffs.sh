#!/usr/bin/env bash

usage_error() {
  echo "Usage: $0 PROTEIN_COMPLEX.pdb LIGAND_RES_NUMBER" >&2
  exit 1
}

file_not_found_error() {
  echo $1 " not found" >&2
  exit 1
}

if [ ${#} -ne 2 ]; then # CHECK FOR USAGE ERROR
  usage_error
else
  PDB_FILE=$1
  if [ ! -f $PDB_FILE ]; then # MAKE SURE THE PDB FILE IS THERE
    file_not_found_error $PDB_FILE
  fi

  RES_NUM=$2
  # DEFINE THE DISTANCE CUTOFFS ARRAY
  # Based on results in https://www.jbc.org/content/282/37/27468.full
  # FutA1 complexes in a monoclinic lattice system of a = 98.3 Å, b = 65.7 Å, c = 50.3 Å
  distance_cutoffs=("5" "15" "25") # all the way up to FutA1's ***estimated*** radius

  mkdir result_csv_files

  for i in ${distance_cutoffs[@]}; do
    OUTDIR="ABS_Scan_Results_"+${distance_cutoffs[i]}
    # For each cutoff, run ABS Scan, then move the result file to the folder
    # This line lets the python script call the python interpreter
    # thus alanine_scanning.py MUST be in this directory
    ./alanine_scanning.py -f $PDB_FILE -n $RES_NUM -d ${distance_cutoffs[i]} -o $OUTDIR

    results_filename = "cutoff_"+${distance_cutoffs[i]}+".csv"
    cp $OUTDIR/Alanine_Scanning_Binding_Energies_Result.csv result_csv_files/$results_filename
  done
  echo "DONE!"
fi
