# Run this: bash run.sh ../../../../data/RMM1.pdb ../../../../data/pdbData/orig.pdb

# Parse inputs
proteinPDBpath=$1
ligandPDBpath=$2

IFS='/' read -r -a tmp <<< "$proteinPDBpath"
IFS='.' read -r -a proteinPDBfilename <<< "${tmp[${#tmp[@]}-1]}"

IFS='/' read -r -a tmp <<< "$ligandPDBpath"
IFS='.' read -r -a ligandPDBfilename <<< "${tmp[${#tmp[@]}-1]}"

echo ">>>Inputs used are: $proteinPDBfilename and $ligandPDBfilename"

# Protonation

## Case 1: protein.

echo ">>>CASE 1: protein."
echo ">>>Remove the previous hydrogens and them rebuild them according to reduce"

reduce -Trim $proteinPDBpath > "${proteinPDBfilename}_noh.pdb"
reduce -BUILD "${proteinPDBfilename}_noh.pdb" > "${proteinPDBfilename}_h.pdb"

echo ">>>Renumber the atoms of the protein receptor partner using PDB-Tools"

pdb_reatom "${proteinPDBfilename}_h.pdb" > protein.pdb

## Case 2: RNA motif.

echo ">>>CASE 2: RNA ligand."
echo ">>>Remove the previous hydrogens and them rebuild them according to reduce"

reduce -Trim $ligandPDBpath > "${ligandPDBfilename}_noh.pdb"
reduce -BUILD "${ligandPDBfilename}_noh.pdb" > "${ligandPDBfilename}_h.pdb"

echo ">>>Rename and/or remove incompatible atom types of RNA"

python3.9 /Users/orion/Lucas_Goiriz_Beltran/UOC_TFM/code/reduce_to_amber.py "${ligandPDBfilename}_h.pdb" rna_pre.pdb

python3 ../manipulador.py rna_pre.pdb > rna.pdb

# Setup

echo ">>>Make lighdock setup"

lightdock3_setup.py protein.pdb rna.pdb -anm #-rst restraints.list

# Simulation

echo ">>>Make lightdock simulation"

lightdock3.py setup.json 100 -s ddna -c 8

# Clustering and Filtering
echo ">>>Do clustering and filtering"

## Calculate the number of swarms
s=`ls -d ./swarm_* | wc -l`
swarms=$((s-1))

## Create files for Ant-Thony
for i in $(seq 0 $swarms)
  do
    echo "cd swarm_${i}; lgd_generate_conformations.py ../protein.pdb ../rna.pdb  gso_100.out 200 > /dev/null 2> /dev/null;" >> generate_lightdock.list;
  done

for i in $(seq 0 $swarms)
  do
    echo "cd swarm_${i}; lgd_cluster_bsas.py gso_100.out > /dev/null 2> /dev/null;" >> cluster_lightdock.list;
  done

### Generate LightDock models
ant_thony.py -c 8 generate_lightdock.list;

### Clustering BSAS (rmsd) within swarm
ant_thony.py -c 8 cluster_lightdock.list;

### Generate ranking files for filtering
lgd_rank.py $s 100;

### Filtering models by >40% of satisfied restraints
lgd_filter_restraints.py --cutoff 5.0 --fnat 0.4 --lnuc rank_by_scoring.list restraints.list A B

# Results
echo ">>>Top 10 simulations are:"
head filtered/rank_filtered.list