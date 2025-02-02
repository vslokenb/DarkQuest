#!/bin/bash
ls / 
#ls -a /home
#ls /scratch
#ls -a /usr
#ls /cvmfs
n_events=$1
z_vtx=$2
EMCal_pos=$3
St3_pos_dif=$4
particle_type=$5
if [ -z ${CONDOR_DIR_INPUT+x} ]; then
	CONDOR_DIR_INPUT=./input;
	echo "CONDOR_DIR_INPUT is initiallized as $CONDOR_DIR_INPUT"
else
	echo "CONDOR_DIR_INPUT is set to '$CONDOR_DIR_INPUT'";
fi

if [ -z ${CONDOR_DIR_OUTPUT+x} ]; then
	CONDOR_DIR_OUTPUT=./out;
	mkdir -p $CONDOR_DIR_OUTPUT
	echo "CONDOR_DIR_OUTPUT is initiallized as $CONDOR_DIR_OUTPUT"
else
	echo "CONDOR_DIR_OUTPUT is set to '$CONDOR_DIR_OUTPUT'";
fi
ls
echo "hello, grid." | tee out.txt $CONDOR_DIR_OUTPUT/out.txt
echo "HOST = $HOSTNAME" | tee -a out.txt $CONDOR_DIR_OUTPUT/out.txt
pwd | tee -a out.txt $CONDOR_DIR_OUTPUT/out.txt
tar -xzvf $CONDOR_DIR_INPUT/input_MC.tar.gz
tar -xzvf e1039_MC.tar.gz
ls -lh | tee -a out.txt $CONDOR_DIR_OUTPUT/out.txt
source core-inst/this-e1039.sh
export DIR_TOP='./'
export LD_LIBRARY_PATH="./work":$LD_LIBRARY_PATH
if [ -e RecoE1039Sim_std.C ]; then
	mv RecoE1039Sim_std.C RecoE1039Sim.C
	sed -i 's/RecoE1039Sim_std/RecoE1039Sim/g' RecoE1039Sim.C
fi

if [ $particle_type == "mu-" ]; then

	time root -b -q RecoE1039Sim.C\($n_events,3,1,$z_vtx,true,true,false,\"\",\"\",\"reco_mu-_"$EMCal_pos"_"$St3_pos_dif".root\",\"./\",\"/pnfs/e1039/persistent/users/apun/bkg_study/e1039pythiaGen_26Oct21/10_bkge1039_pythia_wshielding_100M.root\",0,$EMCal_pos,$St3_pos_dif\)
	echo RecoE1039Sim.C\($n_events,3,1,$z_vtx,true,true,false,\"\",\"\",\"reco_mu-_$z_vtx.root\",\"./\",\"/pnfs/e1039/persistent/users/apun/bkg_study/e1039pythiaGen_26Oct21/10_bkge1039_pythia_wshielding_100M.root\",0,$EMCal_pos,$St3_pos_dif\)

elif [ $particle_type == "mu+" ]; then

	time root -b -q RecoE1039Sim.C\($n_events,3,10,$z_vtx,true,true,false,\"\",\"\",\"reco_mu+_"$EMCal_pos"_"$St3_pos_dif".root\",\"./\",\"/pnfs/e1039/persistent/users/apun/bkg_study/e1039pythiaGen_26Oct21/10_bkge1039_pythia_wshielding_100M.root\",0,$EMCal_pos,$St3_pos_dif\)
	echo RecoE1039Sim.C\($n_events,3,10,$z_vtx,true,true,false,\"\",\"\",\"reco_mu+_$z_vtx.root\",\"./\",\"/pnfs/e1039/persistent/users/apun/bkg_study/e1039pythiaGen_26Oct21/10_bkge1039_pythia_wshielding_100M.root\",0,$EMCal_pos,$St3_pos_dif\)

elif [ $particle_type == "JPsi" ]; then

	time root -b -q RecoE1039Sim.C\($n_events,5,1,$z_vtx,true,true,false,\"\",\"\",\"reco_JPsi_"$EMCal_pos"_"$St3_pos_dif".root\",\"./\",\"/pnfs/e1039/persistent/users/apun/bkg_study/e1039pythiaGen_26Oct21/10_bkge1039_pythia_wshielding_100M.root\",0,$EMCal_pos,$St3_pos_dif\)
	echo RecoE1039Sim.C\($n_events,5,1,$z_vtx,true,true,false,\"\",\"\",\"reco_JPsi_$z_vtx.root\",\"./\",\"/pnfs/e1039/persistent/users/apun/bkg_study/e1039pythiaGen_26Oct21/10_bkge1039_pythia_wshielding_100M.root\",0,$EMCal_pos,$St3_pos_dif\)

fi

ls
RET=$?
if [ $RET -ne 0 ] ; then
	echo "Error in RecoSim.C: $RET"
	exit $RET
fi
mv reco*.root $CONDOR_DIR_OUTPUT/
echo "gridrun.sh finished!"
