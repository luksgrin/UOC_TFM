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