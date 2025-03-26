import ROOT
import matplotlib.pyplot as plt
import argparse
import numpy as np
import argparse
#import mplhep as hep
#plt.style.use(hep.style.CMS)
parser = argparse.ArgumentParser(description="A Python script that accepts command-line options")
parser.add_argument('--type', type=str, help="Description of input sample type (name of directory!)", required=False)
parser.add_argument('--nominal', type=str, help="Description of default sample (name of directory!)", default='newPar')
parser.add_argument('--ecal', type=str, help="Description of default sample (name of directory!)", default='hit_truthx')
args = parser.parse_args()
ROOT.EnableImplicitMT()


# C++ function to perform the logic "Accepted event = at least n detIDs in certain range and at least m hit on specific detID"
# FUNCTION TO DO diff distrib
ROOT.gInterpreter.Declare(
'''
#include "ROOT/RVec.hxx"

using namespace ROOT::VecOps;

RVec<double> obs_st3(RVec<double> track_px_st3,RVec<double> hit_pos){
    RVec<double> result;
    for (int i=0; i<track_px_st3.size(); i++) {
        if (18 < double(track_px_st3[i]) && double(track_px_st3[i]) < 31)  {
            result.push_back(double(hit_pos[i]));
            }
    }
return result;
}

double pz_diff1(RVec<double> track_pz_st3, RVec<double> truthtrack_pz_st3) {
    double truth_val1 = truthtrack_pz_st3[truthtrack_pz_st3.size() - 1];
    //double truth_val2 = truthtrack_pz_st3[truthtrack_pz_st3.size() - 2];
    RVec<double> result;
    for (int i=0; i<track_pz_st3.size(); i++) {
        if (abs(truth_val1 - track_pz_st3[i]) > 0){
            result.push_back((truth_val1 - track_pz_st3[i]));
            }
    }
    double diff_val = Min(result);
    if (diff_val >= 0) {
    return diff_val;
    }
    else if (diff_val <= 0){
    double diff_val1 = -1*Min(abs(result));
    return diff_val1;
    }
    else {
    return 1000;
    }

}
RVec<double> p_rangeZ(RVec<double> track_pz_st3, RVec<double> truthtrack_pz_st3, RVec<double> track_px_st3,RVec<double> truthtrack_px_st3){
    double truth_val1 = truthtrack_pz_st3[truthtrack_pz_st3.size() - 1];
    double truth_val2 = truthtrack_px_st3[truthtrack_px_st3.size() - 1];
    RVec<double> result1;
    RVec<double> result2;
    RVec<double> result3;
    RVec<double> result4;
    for (int i=0; i<track_pz_st3.size(); i++) {
        if (double(track_px_st3[i]) / double(track_pz_st3[i]) > 0.04 || double(track_px_st3[i]) / double(track_pz_st3[i]) < -0.04){
            result1.push_back(double(track_pz_st3[i])+truth_val1);
            result2.push_back(truth_val1);
            result3.push_back(double(track_px_st3[i]));
            result4.push_back(truth_val2);
            }
    }
    return result1;
}

RVec<double> p_rangeX(RVec<double> track_pz_st3, RVec<double> truthtrack_pz_st3, RVec<double> track_px_st3,RVec<double> truthtrack_px_st3){
    double truth_val1 = truthtrack_pz_st3[truthtrack_pz_st3.size() - 1];
    double truth_val2 = truthtrack_px_st3[truthtrack_px_st3.size() - 1];
    RVec<double> result1;
    RVec<double> result2;
    RVec<double> result3;
    RVec<double> result4;
    for (int i=0; i<track_pz_st3.size(); i++) {
        if (double(track_px_st3[i]) / double(track_pz_st3[i]) > 0.04 || double(track_px_st3[i]) / double(track_pz_st3[i]) < -0.04){
            result1.push_back(double(track_pz_st3[i]));
            result2.push_back(truth_val1);
            result3.push_back(double(track_px_st3[i])+truth_val2);
            result4.push_back(truth_val2);
            }
    }
    return result3;
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

int PzCut(RVec<double> track_pz_st3) {
    // set up the counts
    // Loop over the tracks vector
    for (int i=0; i<track_pz_st3.size(); i++) {
        if (track_pz_st3[i] > 25){
            return 1;
        }
        else {
        return 0;
        }
    }
    
}
'''
)


ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTextFont(42)
c = ROOT.TCanvas("c", "", 800, 1000)
c.SetLeftMargin(0.18)
c.SetRightMargin(0.05)
c.cd()
hs = ROOT.THStack("hs","")
#h.Scale(1/h.Integral())

file_names=[f"/seaquest/users/xinlongl/semi-persistent/geom_change/m0_std_original_{args.nominal}/reco_standard_JPsi*.root",
       #f"/seaquest/users/xinlongl/semi-persistent/geom_change/m100_std_{args.type}_{args.nominal}/reco_standard_JPsi*.root",
       #"/seaquest/users/xinlongl/semi-persistent/geom_change/m200_std_{args.type}_{args.nominal}/reco_standard_JPsi*.root",
       ##"m0_aligned_emulreco_standard_JPsi*.root",
       "m100_aligned_emul/reco_standard_JPsi*.root",
       "m200_aligned_emul/reco_standard_JPsi*.root"
       #f"/seaquest/users/xinlongl/semi-persistent/geom_change/m0_std_{args.type}_{args.ecal}/reco_standard_JPsi*.root",
       #f"/seaquest/users/xinlongl/semi-persistent/geom_change/m100_std_{args.type}_{args.ecal}/reco_standard_JPsi*.root",
       #f"/seaquest/users/xinlongl/semi-persistent/geom_change/m200_std_{args.type}_{args.ecal}/reco_standard_JPsi*.root",
]
index=-1
histo_index=['h1','h2','h3','h4']
dictionary={}
dict_count={}
color=[4,3,2]
for i in range(len(file_names)):
    rdf = ROOT.RDataFrame("Events", file_names[i]).Filter("truthdimuon_z_vtx[truthdimuon_z_vtx.size()-1] < 0") #.Define("obs_st3", f"obs_st3(hit_detID, {args.obs})")
    N_recoed = rdf.Filter("dimuon_matched[0]  > 0")
    #N_recoed.Define("pz_mask","abs(truthtrack_pz_st3[truthtrack_z_vtx.size() - 1] - track_pz_st3)")
    N_signal0 = N_recoed.Define("pz_diff1","pz_diff1(dimuon_mass, truthdimuon_mass)") #USING MASS IN SAME FUNCTION
    N_signal = N_signal0.Filter("pz_diff1 < 999 && validPz(dimuon_pz)")
    n1=N_signal.Count().GetValue()
    #reso1=N_signal.StdDev("pz_diff1").GetValue()
    h0=rdf.Histo1D(("Dimuon mass",";Dimuon mass [GeV]; fraction of N_{gen}",50, 0, 5),"dimuon_mass")
    
    n0=rdf.Count().GetValue()
    h0.Scale(1/n0)
    h0.SetLineColor(color[i])
    h0.SetLineStyle(1)
    h0.SetLineWidth(2)
    dictionary[histo_index[i]]=h0.GetValue()
    dict_count[histo_index[i]]=n1/n0
    print(n0,n1,n1/n0)
    hs.Add(dictionary[histo_index[i]])
    h0.SetMaximum(0.003)
    h0.SetMinimum(0)
    if i == 0:  # Draw the first histogram
        h0.Draw("HIST")
    else:  # Overlay subsequent histograms
        h0.Draw("HIST SAME")
    
#hs.SetMaximum(0.0001)
#hs.SetMaximum(0)
legend=ROOT.TLegend(0.2,0.76,0.68,0.86)
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.AddEntry(dictionary[histo_index[0]],f"nominal: eff x acc = {dict_count[histo_index[0]]:.4f}","lep")
legend.AddEntry(dictionary[histo_index[1]],f"100cm shift with EMCal: eff x acc = {dict_count[histo_index[1]]:.4f}","lep")
legend.AddEntry(dictionary[histo_index[2]],f"200cm shift with EMCal: eff x acc = {dict_count[histo_index[2]]:.4f}","lep")
#legend.AddEntry(dictionary[histo_index[3]],"nominal","lep")
legend.SetTextSize(0.020)
legend.Draw()
label = ROOT.TLatex()
label.SetNDC(True)
label.SetTextSize(0.040)
label.DrawLatex(0.150, 0.920, r"J / \psi \rightarrow \mu \mu mass")
print("all done! saving")
#w.Print()
'''if index <2:
    index+=1
else:
    index="nom"'''
c.Update()
#pad = c.GetPad(0)
#pad.SetMinimum(0)
#ad.SetMaximum(0.003)
c.SaveAs(f"final_batch/jpsi_mass_lowz_{args.ecal}.png")
c.SaveAs(f"final_batch/jpsi_mass_lowz_{args.ecal}.pdf")
