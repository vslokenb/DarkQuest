import ROOT
import matplotlib.pyplot as plt
import argparse

import argparse

import mplhep as hep
plt.style.use(hep.style.CMS)

parser = argparse.ArgumentParser(description="A Python script that accepts command-line options")
parser.add_argument('--type', type=str, help="Description of input sample type (name of directory!)", required=True)
parser.add_argument('--nominal', type=str, help="Description of default sample (name of directory!)", default='newPar')
args = parser.parse_args()

# C++ function to perform the logic "Accepted event = at least n detIDs in certain range and at least m hit on specific detID"
ROOT.gInterpreter.Declare(
'''
#include "ROOT/RVec.hxx"

using namespace ROOT::VecOps;

int isValidCount(RVec<int> hit_detID) {
    // set up the counts
    int detID_41_42 = 0;
    int detID_18_31 = 0;
    // Loop over the hit_detID vector
    for (int i=0; i<hit_detID.size(); i++) {
        if ((hit_detID[i] == 41) || (hit_detID[i] == 42)) {
            detID_41_42++;
        }
        if ((hit_detID[i] > 18) && (hit_detID[i] < 31)) {
            detID_18_31++;
        }
    }
    // Check if event valid 
    if ((detID_41_42 >= 1) && (detID_18_31 >= 4)) {
        return 1;
    }
    else {
        return 0;
    }
}
'''
)

def cal_eff(file_names,bins = [-300,42]):
    print(file_names)
    rdf = ROOT.RDataFrame("Events", file_names)
    Effs = []
    for i in range(len(bins)-1):
        l_bin = bins[i]
        h_bin = bins[i+1]
        rdf_cut = rdf.Filter(f"truthtrack_z_vtx[0] > {l_bin} && truthtrack_z_vtx[0] < {h_bin} && isValidCount(hit_detID)")
        N_tot = rdf_cut.Count().GetValue()
        if N_tot == 0:
            eff = 0
        else:
            N_recoed = rdf_cut.Filter("n_tracks > 0").Count().GetValue()
            eff = N_recoed/N_tot
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
plt.ylabel('single track efficiency')
plt.ylim(0,1)
plt.legend()
plt.title('J/Psi efficiency on accepted events (std tracking)')



# Save and show the plot
plt.savefig(f'fast_effxaccept_JPsi_{args.type}_{args.nominal}.pdf', format='pdf')
plt.show()

