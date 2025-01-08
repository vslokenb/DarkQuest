#raw_list=../../samples/mini_scale/AprimeSignal-Sim/DAVTAV_raw_list.txt
#raw_list=$1
raw_list=file_list.txt
grid_dir=$1
P=$2
storage_dir=f
if [ $P = mu ]; then
	#./generaterunfile.sh ~/test/test_hepmc/DarkQuest/lhe/output/displaced_Aprime_Muons/
	./generaterunfile.sh '/seaquest/users/xinlongl/test/test_hepmc/DarkQuest/lhe/output/displaced_Aprime_Muons/Pion*'
	storage_dir=~/semi-persistent/Signal/First_Pro_WithoutDE_Ori/muon
elif [ $P = e ]; then
	./generaterunfile.sh '/seaquest/users/xinlongl/test/test_hepmc/DarkQuest/lhe/output/displaced_Aprime_Electrons/Pion*'
	storage_dir=~/semi-persistent/Signal/First_Pro_WithoutDE_Ori/electron
fi
#storage_dir=$3
id=0
#--strip-components=2
tar -czvf e1039_MC.tar.gz /seaquest/users/xinlongl/projects/Pro_DarkQuest_Sim/core-software-original/core-inst --transform='s,^seaquest/users/xinlongl/projects/Pro_DarkQuest_Sim/core-software-original/,,'
tar -czvf public_MC.tar.gz G4_EMCal.C RecoSim.C support e1039_MC.tar.gz embedding
#exit
while IFS= read -r line
do
	#echo CP2
	job_dir=$grid_dir/$id
	file_base=$(basename "$line")
	echo $storage_dir/reco_$file_base.root
	#exit
	#continue
	
	if [ ! -e $storage_dir/reco_$file_base.root ] ; then
		ran1=$(( RANDOM % 99 + 2 ))
		ran2=$(( RANDOM % 99 + 2 ))
		ran_dir1=$(printf "%04d" $ran1)
		ran_dir2=$(printf "%04d" $ran2)
		echo /pnfs/e1039/persistent/users/kenichi/data_emb_e906/$ran_dir1/embedding_data.root
		echo /pnfs/e1039/persistent/users/kenichi/data_emb_e906/$ran_dir2/embedding_data.root
		echo CP1
		#cp /pnfs/e1039/persistent/users/kenichi/data_emb_e906/$ran_dir1/embedding_data.root embedding/file1.root
		#cp /pnfs/e1039/persistent/users/kenichi/data_emb_e906/$ran_dir2/embedding_data.root embedding/file2.root
		if [ $P = mu ]; then
			./gridsub_MC.sh AprimeSignalMu-Sim 0 $line reco_$file_base.root support/RecoSim_config.ini /pnfs/e1039/scratch/users/$USER/DAVTAV/$job_dir
			echo ./gridsub_MC.sh AprimeSignal-Sim 2000 $line $file_base.root RecoSim_config.ini /pnfs/e1039/scratch/users/$USER/DAVTAV/$job_dir	
		elif [ $P = e ]; then
			./gridsub_MC.sh AprimeSignalE-Sim 0 $line reco_$file_base.root support/RecoSim_config.ini /pnfs/e1039/scratch/users/$USER/DAVTAV/$job_dir
			echo ./gridsub_MC.sh AprimeSignal-Sim 2000 $line $file_base.root RecoSim_config.ini /pnfs/e1039/scratch/users/$USER/DAVTAV/$job_dir	
		fi
	else
		echo "reco_$file_base.root already exist!"
	fi
	#echo /seaquest/users/xinlongl/projects/DAV-TAV/main/../main/cpp_modules/gridsub_MC.sh AprimeSignal-Sim 0 $line $file_base.root RecoSim_config.ini /pnfs/e1039/scratch/users/DAVTAV/$job_dir	
	(( id++ ))
	echo $job_dir $file_base $id
done< "$raw_list"
