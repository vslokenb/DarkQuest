import ROOT
import matplotlib.pyplot as plt
import argparse
import numpy as np
import argparse
import mplhep as hep
plt.style.use(hep.style.CMS)

parser = argparse.ArgumentParser(description="A Python script that accepts command-line options")
parser.add_argument('--type', type=str, help="Description of input sample type (name of directory!)", required=True)
parser.add_argument('--nominal', type=str, help="Description of default sample (name of directory!)", default='newPar')
args = parser.parse_args()

# FUNCTION TO DO ROUGH PZ MATCH CONDITION
ROOT.gInterpreter.Declare(
'''
#include "ROOT/RVec.hxx"

using namespace ROOT::VecOps;

double pz_diff1(RVec<double> track_pz_st3, RVec<double> truthtrack_pz_st3) {
    double truth_val1 = truthtrack_pz_st3[truthtrack_pz_st3.size() - 1];
    //double truth_val2 = truthtrack_pz_st3[truthtrack_pz_st3.size() - 2];
    RVec<double> result;
    for (int i=0; i<track_pz_st3.size(); i++) {
        if (abs(truth_val1 - track_pz_st3[i]) > 0){
            result.push_back(abs(truth_val1 - track_pz_st3[i]));
            }
    }
    double diff_val = Min(result);
    if (diff_val >= 0) {
    return diff_val;
    }
    else {
    return 1000;
    }

}
double pz_diff2(RVec<double> track_pz_st3, RVec<double> truthtrack_pz_st3) {
    //double truth_val1 = truthtrack_pz_st3[truthtrack_pz_st3.size() - 1];
    double truth_val2 = truthtrack_pz_st3[truthtrack_pz_st3.size() - 2];
    RVec<double> result;
    for (int i=0; i<track_pz_st3.size(); i++) {
        if (abs(truth_val2 - track_pz_st3[i]) > 0){
            result.push_back(abs(truth_val2 - track_pz_st3[i]));
            }
    }
    double diff_val = Min(result);
    if (diff_val >= 0) {
    return diff_val;
    }
    else {
    return 1000;
    }

}

int ang_xz(RVec<double> track_pz_st3, RVec<double> truthtrack_pz_st3, RVec<double> track_px_st3){
    double truth_val = truthtrack_pz_st3[truthtrack_pz_st3.size() - 1];
    RVec<double> result;
    for (int i=0; i<track_pz_st3.size(); i++) {
        if (double(track_px_st3[i]) / double(track_pz_st3[i]) != 0 && double(track_px_st3[i]) / double(track_pz_st3[i]) > -0.07 && double(track_px_st3[i]) / double(track_pz_st3[i]) < 0.07)  {
            return 1;
            }
        else {
            return 0;
            }
    }
}
int validPz(RVec<double> track_pz_st3){
    for (int i=0; i<track_pz_st3.size(); i++) {
    if (double(track_pz_st3[i]) < 65 && double(track_pz_st3[i]) > 10){
        return 1;
    }
    else {
        return 0;
    }
    }
}
'''
)


def cal_eff(file_names,bins = [-300,42]):
    rdf = ROOT.RDataFrame("Events", file_names)
    Effs = []
    for i in range(len(bins)-1):
        l_bin = bins[i]
        h_bin = bins[i+1]
        rdf_cut = rdf.Filter(f"truthtrack_z_vtx[truthtrack_z_vtx.size() - 1] > {l_bin} && truthtrack_z_vtx[truthtrack_z_vtx.size() - 1] < {h_bin}")
        N_tot = rdf_cut.Sum("n_truthtracks").GetValue()
        if N_tot == 0:
            print('oh no')
            eff = 0
        else:
            N_recoed = rdf_cut.Filter("n_tracks > 0 && n_tracks < 3")
            #N_recoed.Define("pz_mask","abs(truthtrack_pz_st3[truthtrack_z_vtx.size() - 1] - track_pz_st3)")
            N_signal0 = N_recoed.Filter("ang_xz(track_pz_st3, truthtrack_pz_st3,track_px_st3)").Define("pz_diff1","pz_diff1(track_pz_st3, truthtrack_pz_st3)")
            N_signal = N_signal0.Filter("pz_diff1 < 999 && validPz(track_pz_st3)")
            n1=N_signal.Count().GetValue()
            #reso1=N_signal.StdDev("pz_diff1").GetValue()
        #REPEAT BUT WITH OTHER TRUTH VALUE
            N_recoed2 = rdf_cut.Filter("n_tracks > 0 && n_tracks < 3")
            #N_recoed.Define("pz_mask","abs(truthtrack_pz_st3[truthtrack_z_vtx.size() - 1] - track_pz_st3)")
            N_signal02 = N_recoed2.Filter("ang_xz(track_pz_st3, truthtrack_pz_st3,track_px_st3)").Define("pz_diff2","pz_diff2(track_pz_st3, truthtrack_pz_st3)")
            N_signal2 = N_signal02.Filter("pz_diff2 < 999 && validPz(track_pz_st3)")
            n2=N_signal2.Count().GetValue()
        try:
            eff=(n1+n2)/N_tot
        except:
            eff=0
        Effs.append(eff)
    return Effs

bins = [-300, -250, -200, -150, -100, -50, 0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
#print(cal_eff("m0_emul/reco_standard_mu*.root", bins))
#print(cal_eff("m100_emul/reco_standard_mu*.root", bins))
#print(cal_eff("m100_emul/reco_standard_mu*.root", bins))

    #colors = ['b', 'g', 'r', 'c']  # Colors for different directories
    #labels = ['0cm', '-50cm', '-100cm', '-200cm']  # Labels for the directories
    #for i, (bin_resols, xaxis) in enumerate(zip(all_bin_resols, all_xaxis)):
files=[f"/seaquest/users/xinlongl/semi-persistent/geom_change/m0_std_{args.type}_{args.nominal}/reco_standard_JPsi*.root",
       f"/seaquest/users/xinlongl/semi-persistent/geom_change/m100_std_{args.type}_{args.nominal}/reco_standard_JPsi*.root",
       f"/seaquest/users/xinlongl/semi-persistent/geom_change/m200_std_{args.type}_{args.nominal}/reco_standard_JPsi*.root",
       f"/seaquest/users/xinlongl/semi-persistent/geom_change/m0_std_original_{args.nominal}/reco_standard_JPsi*.root"]#[f"0cm_shift_standard_{args.type}/reco_standard_JPsi*.root",f"100cm_shift_standard_{args.type}/reco_standard_JPsi*.root",f"200cm_shift_standard_{args.type}/reco_standard_JPsi*.root",f"/seaquest/users/xinlongl/semi-persistent/geom_change/m0_std_original_{args.nominal}/reco_standard_JPsi*.root"]
axis=[-275,-225,-175,-125,-75,-25,25,75,125,175,225,275,325,375,425,475,525,575]
labels=['0cm shift','100cm shift','200cm shift', 'nominal']
colors=['b','g','r','c']
for i in range(len(files)):
    x=cal_eff(files[i],bins)
    plt.plot(axis,x, label=labels[i], marker='.',color=colors[i])


# Set plot labels and title
plt.xlabel('truth z vtx')
plt.ylabel('single track efficiency with angular match')
plt.ylim(0,1)
plt.legend()
plt.title('J/Psi efficiency x acceptance (std tracking)')



# Save and show the plot
plt.savefig(f'fast_eff_angmask_JPsi_{args.type}_{args.nominal}.pdf', format='pdf')
plt.show()

