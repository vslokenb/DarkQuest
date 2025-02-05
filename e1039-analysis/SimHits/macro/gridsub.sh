#!/bin/bash
work_dir=$1
particle_type=$2
reco_type=$3
n_events=$4
EMCal_pos=$5
St3_pos_dif=$6
n_jobs=$7
work_dir=/pnfs/e1039/scratch/users/$USER/MUONGUN/$work_dir
echo $work_dir
mkdir -p $work_dir
#exit
chmod -R 01755 $work_dir
dir_macros=$(dirname $(readlink -f $BASH_SOURCE))

cd $dir_macros
if [ $reco_type == "displaced" ]; then
	source ../../../../DarkQuest_original_branch/core-inst/this-e1039.sh
	mkdir -p work
	rm work/* -rf
	cd work
	cmake ../src
	make
	cd ..
	tar -czvf e1039_MC.tar.gz ../../../../DarkQuest_original_branch/core-inst --transform='s,^DarkQuest_original_branch/,,'
	tar -czvf input_MC.tar.gz G4_EMCal.C RecoE1039Sim.C e1039_MC.tar.gz work data

elif [ $reco_type == "standard" ]; then
	echo "running standard tracking"
	source ../../../../SpinQuest_official_branch/core-inst/this-e1039.sh
	mkdir -p work
	rm work/* -rf
	cd work
	cmake ../src_std
	make
	cd ..
	tar -czvf e1039_MC.tar.gz ../../../../SpinQuest_official_branch/core-inst --transform='s,^SpinQuest_official_branch/,,'
	tar -czvf input_MC.tar.gz G4_EMCal.C RecoE1039Sim_std.C e1039_MC.tar.gz work data
fi

#z_vtxs=($(seq -100 100 100))
z_vtxs=($(seq 1 1 $n_jobs))

for dir_ind in ${z_vtxs[@]}
do
	job_dir=$work_dir/$dir_ind
	#exit
	mkdir -p $job_dir
	cp input_MC.tar.gz $job_dir
	mkdir -p $job_dir/out
	cp -a $dir_macros/gridrun.sh $job_dir
	CMD="/exp/seaquest/app/software/script/jobsub_submit_spinquest.sh"
	CMD+=" --expected-lifetime='short'"
	CMD+=" --memory=2000"
	CMD+=" -L $job_dir/log_gridrun.txt"
	CMD+=" -f $job_dir/input_MC.tar.gz"
	CMD+=" -d OUTPUT $job_dir/out"
	CMD+=" file://$job_dir/gridrun.sh $particle_type $reco_type $n_events -300 600 $EMCal_pos $St3_pos_dif"
	echo $CMD
	unbuffer $CMD |& tee $job_dir/log_jobsub_submit.txt
	RET_SUB=${PIPESTATUS[0]}
	test $RET_SUB -ne 0 && exit $RET_SUB
done
