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

pdb_reatom "${proteinPDBfilename}_h.pdb" > protein_pre.pdb

echo ">>>Fix HIS residues so that they work with AMBER force field"

python3.9 ../../../fixHIS.py protein_pre.pdb > protein.pdb

## Case 2: RNA motif.

echo ">>>CASE 2: RNA ligand."
echo ">>>Remove the previous hydrogens and them rebuild them according to reduce"

reduce -Trim $ligandPDBpath > "${ligandPDBfilename}_noh.pdb"
reduce -BUILD "${ligandPDBfilename}_noh.pdb" > "${ligandPDBfilename}_h.pdb"

echo ">>>Remove possible top overhang OH"

python3.9 ../../../removeEnds.py "${ligandPDBfilename}_h.pdb" > "${ligandPDBfilename}_nvh.pdb"

echo ">>>Rename and/or remove incompatible atom types of RNA"

python3.9 ../../../reduce_to_amber.py "${ligandPDBfilename}_nvh.pdb" rna.pdb

python3.9 ../../../manipulateRNA.py rna.pdb

# Setup

echo ">>>Make lightdock setup"

# Without restraints
lightdock3_setup.py protein.pdb rna.pdb -anm


# Simulation
echo ">>>Recover RNA tags in lightdock_rna.pdb"

python3.9 ../../../manipulateRNAagain.py lightdock_rna.pdb

echo ">>>Make lightdock simulation"

lightdock3.py setup.json 100 -s dna -c 4

# Clustering
echo ">>>Do clustering and filtering"

python3.9 ../../../manipulateRNA.py lightdock_rna.pdb

## Calculate the number of swarms
s=`ls -d ./swarm_* | wc -l`
swarms=$((s-1))

## Create files for Ant-Thony
for i in $(seq 0 $swarms)
  do
    echo "cd swarm_${i}; lgd_generate_conformations.py ../protein.pdb ../rna.pdb gso_100.out 200 > /dev/null 2> /dev/null;" >> generate_lightdock.list;
  done

for i in $(seq 0 $swarms)
  do
    echo "cd swarm_${i}; lgd_cluster_bsas.py gso_100.out > /dev/null 2> /dev/null;" >> cluster_lightdock.list;
  done

### Generate LightDock models
ant_thony.py -c 4 generate_lightdock.list;

### Clustering BSAS (rmsd) within swarm
ant_thony.py -c 4 cluster_lightdock.list;

### Generate ranking files for filtering
lgd_rank.py $s 100;