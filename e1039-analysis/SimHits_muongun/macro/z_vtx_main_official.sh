#source ../setup.sh
export DIR_TOP=$(dirname $(readlink -f $BASH_SOURCE))
source $DIR_TOP/../../../../SpinQuest_official_branch/core-inst/this-e1039.sh 
cd $DIR_TOP/..
rm work/* -rf
rm install/* -rf
cd work
cmake ../src/ -DCMAKE_INSTALL_PREFIX=../install
make clean
make
make install
export LD_LIBRARY_PATH=$DIR_TOP/../install/lib/:$LD_LIBRARY_PATH
cd $DIR_TOP

z_vtxs=($(seq -500 10 600))
read -p "Do you want to clear ./outputs ? (yes/no): " answer
if [ $answer != yes ] ; then
	exit
fi
#rm ./outputs/* -rf
#z_vtxs=($(seq -500 200 600))
for z_vtx in ${z_vtxs[@]}
do
	if [ -e outputs_official\/output_muon_$z_vtx.root ] ; then
		continue
	fi
		
	echo $z_vtx
	root -b -q RecoE1039Sim.C\(10000,3,1,$z_vtx,true,true,false,\"\",\"\",\"outputs_offcial\/output_muon_$z_vtx.root\",\"./\",\"/pnfs/e1039/persistent/users/apun/bkg_study/e1039pythiaGen_26Oct21/10_bkge1039_pythia_wshielding_100M.root\",0\)
	#mv output_$z_vtx*.root outputs
done

