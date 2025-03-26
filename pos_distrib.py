import ROOT
import matplotlib.pyplot as plt
import argparse
import numpy as np
import argparse
#import mplhep as hep
#plt.style.use(hep.style.CMS)
parser = argparse.ArgumentParser(description="A Python script that accepts command-line options")
parser.add_argument('--type', type=str, help="Description of input sample type (name of directory!)", required=False)
parser.add_argument('--obs', type=str, help="Description of default sample (name of directory!)", default='hit_truthx')
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

int isValidPz(RVec<int> track_pz_st3, RVec<int> truthtrack_pz_st3) {
    // set up the counts
    // Loop over the tracks vector
    double truth_val1 = truthtrack_pz_st3[truthtrack_pz_st3.size() - 1]; 
    double truth_val2 = truthtrack_pz_st3[truthtrack_pz_st3.size() - 2];
    for (int i=0; i<track_pz_st3.size(); i++) {
        if (fabs(truth_val1 - track_pz_st3[i]) < 25 || fabs(truth_val2 - track_pz_st3[i]) < 25){
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
c.SetLeftMargin(0.15)
c.SetRightMargin(0.05)
c.cd()
hs = ROOT.THStack("hs","")
#h.Scale(1/h.Integral())

file_names=['/seaquest/users/xinlongl/semi-persistent/geom_change/m100_std_upgrade_newPar_emul_PRO/reco*_mu*.root', 'm100_aligned_emul/reco*_mu*.root']
index=-1
histo_index=['h1','h2','h3','h4']
dictionary={}
color=[600,416,632,432]
for i in range(len(file_names)):
    rdf = ROOT.RDataFrame("Events", file_names[i]).Define("obs_st3", f"obs_st3(hit_detID, {args.obs})")
    
    h0=rdf.Histo1D((f"{args.obs}",f";{args.obs}; N_events",50, -250, 250),"obs_st3")
    ''' hZ=rdf.Histo1D(("dimuon_pz",";pz; N_{events}",3000, 0,120),"dimuon_pz")
    hX=rdf.Histo1D(("track_px_st3",";px truth+reco; N_{events}",3000, -6,6),"track_px_st3")
    c1 = ROOT.TCanvas()
    hZ.Draw()
    c1.SaveAs("pz_range_test.png")
    c2=ROOT.TCanvas()
    hX.Draw()
    c2.SaveAs("px_range_test.png")'''
    '''xmean1 = -0.06#h0.GetMean()
    xmean2 = 0.06
    xrms = 0.02#h0.GetRMS()
    #print(xmean1,xrms," MEAN AND RMS PRE FIT")
    var=ROOT.RooRealVar("ang_xz","ang_xz",-0.15,0.15,"")
    var.setRange("r1",-0.15,0)
    var.setRange("r2",0,0.15)'''
    h0.Scale(1/h0.Integral())
    h0.SetLineColor(color[i])
    dictionary[histo_index[i]]=h0.GetValue()
    hs.Add(dictionary[histo_index[i]])
    #rdhMaker = ROOT.RooDataHistHelper("pz_diff", "pz_diff", ROOT.RooArgSet(var))
    #roo_data_hist_result = rdf.Book(ROOT.std.move(rdhMaker), "pz_diff")
    #roo_data_set_result = rdf.Book(ROOT.std.move(ROOT.RooDataSetHelper("dataset", "dataset", ROOT.RooArgSet(var))), "pz_diff")
    #data_set_roo = roo_data_set_result.GetValue()
    #h=ROOT.RooDataHist("datahist", "datahist", ROOT.RooArgList(var, "ang_xz"), h1)
  
    '''mean1=ROOT.RooRealVar("mean","mean",-0.06,-0.15,0.15,"GeV")
    mean2=ROOT.RooRealVar("mean","mean",0.06,-0.15,0.15,"GeV")
    sigma=ROOT.RooRealVar("sigma","sigma",xrms,0.0001,2*xrms,"GeV")
    a0=ROOT.RooRealVar()
    a1=ROOT.RooRealVar()
    a2=ROOT.RooRealVar()
    w = ROOT.TStopwatch()
    w.Start()'''



    '''pdf_sig = ROOT.RooGaussian("pdfsig","pdfsig",var, mean1, sigma)
    pdf_bkg = ROOT.RooGaussian("pdfbkg","pdfbkg",var, mean2,sigma)
    pdf_sig.forceNumInt(True)
    pdf_bkg.forceNumInt(True)
    frac1 = ROOT.RooRealVar("frac1", "frac1", 0.5, 0, 1.0)
    #frac2= ROOT.RooRealVar("frac2", "frac2", 0.5, 0, 1.0)
    pdf = ROOT.RooAddPdf("pdf", "pdf", ROOT.RooArgList(pdf_sig, pdf_bkg), ROOT.RooArgList(frac1))
    pdf.generateBinned(var)
    pdf.fitTo(h,ROOT.RooFit.Range("r1,r2"))
    print("time after fit")
    w.Print() 
    print(rdf.Sum("ang_xz").GetValue(), "count in ang")'''
#print(cal_eff("m0_emul/reco_standard_mu*.root", bins))
#print(cal_eff("m100_emul/reco_standard_mu*.root", bins))
#print(cal_eff("m100_emul/reco_standard_mu*.root", bins))

    #colors = ['b', 'g', 'r', 'c']  # Colors for different directories
    #labels = ['0cm', '-50cm', '-100cm', '-200cm']  # Labels for the directories
    #for i, (bin_resols, xaxis) in enumerate(zip(all_bin_resols, all_xaxis)):
#, '/seaquest/users/xinlongl/semi-persistent/geom_change/m0_std_original_emul_PRO', '/seaquest/users/xinlongl/semi-persistent/geom_change/m100_std_upgrade_emul_PRO','/seaquest/users/xinlongl/semi-persistent/geom_change/m100_std_upgrade_PRO']
    #"/seaquest/users/vsloken/scratch/m0_emul/reco*_mu*.root"]#,f"100cm_shift_standard_{args.type}/reco_standard_mu*.root",f"200cm_shift_standard_{args.type}/reco_standard_mu*.root",f"/seaquest/users/xinlongl/semi-persistent/geom_change/m0_std_original_{args.nominal}"]
#axis=np.arange(-275,575,50)
    #frame = var.frame()
    #frame.GetXaxis().SetTitle("px / pz at st3")
    #h.plotOn(frame)
    #frame.Draw("SAME")
    #pdf.plotOn(frame, ROOT.RooFit.Components("pdfsig"),ROOT.RooFit.LineStyle(2), ROOT.RooFit.LineColor(2))
    #pdf.plotOn(frame, ROOT.RooFit.Components("pdfbkg"), ROOT.RooFit.LineStyle(2), ROOT.RooFit.LineColor(3))
    #pdf.plotOn(frame, ROOT.RooFit.LineStyle(1), ROOT.RooFit.LineColor(4))

#frame.SetTitle("J/Psi Angular distribution")
hs.Draw("nostack")
legend=ROOT.TLegend(0.6,0.8,0.95,0.9)
legend.AddEntry(dictionary[histo_index[0]],"100cm shift","lep")
legend.AddEntry(dictionary[histo_index[1]],"100cm shift with corrected EMCal","lep")
#legend.AddEntry(dictionary[histo_index[2]],"100cm shift with EMCal + align","lep")
#legend.AddEntry(dictionary[histo_index[3]],"nominal","lep")
legend.SetTextSize(0.020)
legend.Draw()
label = ROOT.TLatex()
label.SetNDC(True)
label.SetTextSize(0.040)
label.DrawLatex(0.100, 0.920, f"{args.obs} position")
print("all done! saving")
#w.Print()
'''if index <2:
    index+=1
else:
    index="nom"'''
c.SaveAs(f"truthmuon_100_emul_distrib_{args.obs}.png")
