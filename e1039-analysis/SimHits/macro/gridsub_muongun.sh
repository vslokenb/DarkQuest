#!/bin/bash
work_dir=$1
n_events=$2
work_dir=/pnfs/e1039/scratch/users/$USER/MUONGUN/$work_dir
echo $work_dir
mkdir -p $work_dir
#exit
chmod -R 01755 $work_dir
dir_macros=$(dirname $(readlink -f $BASH_SOURCE))

cd $dir_macros
tar -czvf e1039_MC.tar.gz /seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest_original_branch/core-inst --transform='s,^seaquest/users/xinlongl/projects/z_vtx_sensitivity/DarkQuest_original_branch/,,'
tar -czvf input_MC.tar.gz G4_EMCal.C RecoE1039Sim_muongun.C e1039_MC.tar.gz src work data

z_vtxs=($(seq -100 100 100))
dir_ind=1
for z_vtx in ${z_vtxs[@]}
do
	job_dir=$work_dir/$dir_ind
	#exit
	mkdir -p $job_dir
	cp input_MC.tar.gz $job_dir
	mkdir -p $job_dir/out
	cp -a $dir_macros/gridrun_muongun.sh $job_dir
	CMD="/exp/seaquest/app/software/script/jobsub_submit_spinquest.sh"
	CMD+=" --expected-lifetime='medium'"
	CMD+=" --memory=2000"
	CMD+=" -L $job_dir/log_gridrun.txt"
	CMD+=" -f $job_dir/input_MC.tar.gz"
	CMD+=" -d OUTPUT $job_dir/out"
	CMD+=" file://$job_dir/gridrun_muongun.sh $n_events $z_vtx"
	echo $CMD
	unbuffer $CMD |& tee $job_dir/log_jobsub_submit.txt
	RET_SUB=${PIPESTATUS[0]}
	test $RET_SUB -ne 0 && exit $RET_SUB
	(( dir_ind++ ))
done
