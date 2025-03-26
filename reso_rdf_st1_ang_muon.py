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
parser.add_argument('--ecal', type=str, help="Description of default ecal sample (name of directory!)", default='newPar_ECAL')
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
        result.push_back(abs(truth_val1 - track_pz_st3[i]));
    }
    double diff_val = Min(result);
    if (diff_val >= 0) {
    return diff_val;
    }
    else {
    return 1000;
    }

}

RVec<double> ang_xz(RVec<double> track_pz_st3, RVec<double> truthtrack_pz_st3, RVec<double> track_px_st3){
    double truth_val = truthtrack_pz_st3[truthtrack_pz_st3.size() - 1];
    RVec<double> result;
    for (int i=0; i<track_pz_st3.size(); i++) {
        if (double(track_px_st3[i]) / double(track_pz_st3[i]) != 0)  {
            result.push_back(double(track_px_st3[i]) / double(track_pz_st3[i]));
            }
    }
return result;
}

int validPz(RVec<double> track_pz_st3){
    for (int i=0; i<track_pz_st3.size(); i++) {
    if (double(track_pz_st3[i]) < 120){
        return 1;
    }
    else {
        return 0;
    }
    }
}
'''
)


def cal_reso(file_names,bins = [-300,42]):
    rdf = ROOT.RDataFrame("Events", file_names).Define("truthang_xz","ang_xz(truthtrack_pz_st1, truthtrack_pz_st1, truthtrack_px_st1)").Define("ang_xz","ang_xz(track_pz_st1, truthtrack_pz_st1, track_px_st1)")
    total_count=rdf.Count().GetValue()
    total_reco=0
    Resos = []
    for i in range(len(bins)-1):
        l_bin = bins[i]
        h_bin = bins[i+1]
        rdf_cut = rdf.Filter(f"truthang_xz[truthang_xz.size() - 1] > {l_bin} && truthang_xz[truthang_xz.size() - 1] < {h_bin}").Filter("truthtrack_z_vtx[truthtrack_z_vtx.size()-1] < 0")
        #rdf_cut2 = rdf.Filter(f"truthtrack_z_vtx[truthtrack_z_vtx.size() - 2] > {l_bin} && truthtrack_z_vtx[truthtrack_z_vtx.size() - 2] < {h_bin}")
        

        N_recoed = rdf_cut.Filter("n_tracks  > 0 && validPz(track_pz_st1)")
            #N_recoed.Define("pz_mask","abs(truthtrack_pz_st3[truthtrack_z_vtx.size() - 1] - track_pz_st3)")
        N_signal0 = N_recoed.Define("pz_diff1","pz_diff1(ang_xz, truthang_xz)")
        #n1=N_signal.Count().GetValue()
        N_signal = N_signal0.Filter("pz_diff1 < 999")
        total_reco+=N_signal.Count().GetValue()
        try:
            selection=N_signal.AsNumpy(columns=["pz_diff1"])
        #print(selection)
            q16, q84 = np.quantile(selection['pz_diff1'], 0.16), np.quantile(selection['pz_diff1'], 0.84)
            reso1 = (q84 - q16) / 2.0 
        except:
            reso1=0
        Resos.append(reso1)

    total_eff=total_reco / total_count
    return Resos,total_eff

bins = np.arange(-0.1,0.1,0.02)
#print(cal_eff("m100_emul/reco_standard_mu*.root", bins))
#print(cal_eff("m100_emul/reco_standard_mu*.root", bins))

    #colors = ['b', 'g', 'r', 'c']  # Colors for different directories
    #labels = ['0cm', '-50cm', '-100cm', '-200cm']  # Labels for the directories
    #for i, (bin_resols, xaxis) in enumerate(zip(all_bin_resols, all_xaxis)):
files=[f"/seaquest/users/xinlongl/semi-persistent/geom_change/m0_std_original_{args.nominal}/reco_standard_mu*.root",
       #f"/seaquest/users/xinlongl/semi-persistent/geom_change/m100_std_{args.type}_{args.nominal}/reco_standard_mu*.root",
       #f"/seaquest/users/xinlongl/semi-persistent/geom_change/m200_std_{args.type}_{args.nominal}/reco_standard_mu*.root",
       #"m0_aligned_emulreco_standard_mu*.root",
       "m100_aligned_emul/reco_standard_mu*.root",
       "m200_aligned_emul/reco_standard_mu*.root"
       #f"/seaquest/users/xinlongl/semi-persistent/geom_change/m0_std_{args.type}_{args.ecal}/reco_standard_mu*.root",
       #f"/seaquest/users/xinlongl/semi-persistent/geom_change/m100_std_{args.type}_{args.ecal}/reco_standard_mu*.root",
       #f"/seaquest/users/xinlongl/semi-persistent/geom_change/m200_std_{args.type}_{args.ecal}/reco_standard_mu*.root",

       ]
axis=np.arange(-0.09,0.09,0.02)
labels=['nominal', '100cm shift with EMCal', '200cm shift with EMCal']
colors=['b','g','r','y','m']
markers=['x','o','o','o']
for i in range(len(files)):
    x,eff=cal_reso(files[i],bins)
    print(type(x))
    plt.plot(axis,x, label=labels[i]+f": eff x acc = {eff:.2f}", marker=markers[i],mfc='none',color=colors[i])


# Set plot labels and title
plt.xlabel('st1 truth angle')
plt.ylabel(r'$\sigma (\frac{p_x}{p_z})$ ')
plt.ylim(0,0.0002)
#plt.yscale('log')
plt.legend()
plt.title('Muon gun angular resolution px/pz')



# Save and show the plot
plt.savefig(f'final_batch/fast_reso_st1_ang_pxpz_muon_{args.type}_{args.ecal}.pdf', format='pdf', bbox_inches="tight")
plt.show()

