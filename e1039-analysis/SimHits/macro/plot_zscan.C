// plot_zscan.C — truth z vs reconstructed dimuon z for a z-scan made with
// run_dy_zscan.sh (files <dir>/<tag>_z<Z>.root, tree "Events" from SimAna).
//
//   root -b -q 'plot_zscan.C("zscan_out", "dy")'
//   root -b -q 'plot_zscan.C("zscan_out", "jpsi", "dimuon_chisq_vx > 0 && dimuon_chisq_vx < 20")'
//
// Arguments: directory, sample tag ("dy" or "jpsi"), selection on the reco
// dimuons (default: 0 < dimuon_chisq_vx < 20; pass "1" for no selection).
//
// Each sample is labelled individually by its truth z (median of
// truthdimuon_z_vtx[0], the generated pair; the <Z> in the file name is the
// fallback).
// Outputs, written to <dir>/:
//   zscan_<tag>_recoz.{png,pdf}   reco z distribution per sample (unit area),
//                                 with a dashed line at each sample's truth z
//   zscan_<tag>_truth_vs_reco.{png,pdf}  median reco z vs truth z, 16-84% band,
//                                 every point labelled
// and a table on the console.

#include <TCanvas.h>
#include <TFile.h>
#include <TGraphAsymmErrors.h>
#include <TH1D.h>
#include <TLatex.h>
#include <TLegend.h>
#include <TLine.h>
#include <TROOT.h>
#include <TStyle.h>
#include <TSystem.h>
#include <TTree.h>

#include <glob.h>

#include <algorithm>
#include <cstdio>
#include <iostream>
#include <string>
#include <vector>

struct ZSample {
    std::string file;
    double zname = 0;      // z from the file name
    double ztruth = 0;     // median truth z of the generated dimuon
    double ztruthRms = 0;  // its 16-84% half-width
    Long64_t nevt = 0;     // events in the ntuple
    Long64_t nreco = 0;    // reco dimuons passing the selection
    double q16 = 0, q50 = 0, q84 = 0;
    TH1D *h = nullptr;
};

void plot_zscan(const char *dir = "zscan_out", const char *tag = "dy",
                const char *cut = "dimuon_chisq_vx > 0 && dimuon_chisq_vx < 20")
{
    gROOT->SetBatch(kTRUE);
    gStyle->SetOptStat(0);
    const double ZLO = -500, ZHI = 700;   // reco z axis range [cm]
    const int NB = 120;                   // 10 cm bins for the display
    const int NFINE = 2400;               // 0.5 cm bins for the quantiles
    const Long64_t NMIN = 20;             // fewer reco dimuons: listed, not plotted

    // ---- find the samples ----------------------------------------------------
    std::vector<ZSample> S;
    glob_t g;
    const std::string pat = std::string(dir) + "/" + tag + "_z*.root";
    if (glob(pat.c_str(), 0, nullptr, &g) == 0)
        for (size_t i = 0; i < g.gl_pathc; ++i) {
            ZSample s;
            s.file = g.gl_pathv[i];
            const std::string base = gSystem->BaseName(s.file.c_str());
            if (base.find("_DST") != std::string::npos) continue;
            const size_t p = base.rfind("_z");
            s.zname = atof(base.substr(p + 2).c_str());
            S.push_back(s);
        }
    globfree(&g);
    if (S.empty()) {
        std::cerr << "ERROR: no files match " << pat << std::endl;
        return;
    }
    std::sort(S.begin(), S.end(), [](const ZSample &a, const ZSample &b) { return a.zname < b.zname; });

    // ---- fill ------------------------------------------------------------------
    const int colors[] = {kBlue + 1, kRed + 1, kGreen + 2, kMagenta + 1, kOrange + 7,
                          kCyan + 2, kViolet + 5, kPink + 9, kTeal - 6, kAzure + 7,
                          kSpring - 6, kGray + 2};
    const int NCOL = sizeof(colors) / sizeof(int);
    std::vector<ZSample> good;
    for (size_t i = 0; i < S.size(); ++i) {
        ZSample &s = S[i];
        TFile *f = TFile::Open(s.file.c_str());
        TTree *t = f && !f->IsZombie() ? dynamic_cast<TTree *>(f->Get("Events")) : nullptr;
        if (!t) {
            std::cerr << "WARNING: no Events tree in " << s.file << ", skipped" << std::endl;
            continue;
        }
        s.nevt = t->GetEntries();
        // truth z of the generated dimuon
        // Entry [0] only: with pileup mixed in, the truth-dimuon list also
        // holds pairings with pileup muons; the generated pair comes first.
        // Median and 16-84% half-width, so stray entries cannot pull it.
        gROOT->cd();
        TH1D *htp = new TH1D(Form("ht_%zu", i), "", 4000, -1000, 1000);
        t->Draw(Form("truthdimuon_z_vtx[0]>>ht_%zu", i), "n_truthdimuons > 0", "goff");
        if (htp->Integral() > 0) {
            double q[3], p[3] = {0.16, 0.50, 0.84};
            htp->GetQuantiles(3, q, p);
            s.ztruth = q[1];
            s.ztruthRms = 0.5 * (q[2] - q[0]);
        } else {
            s.ztruth = s.zname;
        }
        delete htp;
        // reco z, display and fine binning
        s.h = new TH1D(Form("hreco_%zu", i), "", NB, ZLO, ZHI);
        s.h->SetDirectory(gROOT);
        TH1D *hf = new TH1D(Form("hfine_%zu", i), "", NFINE, ZLO, ZHI);
        hf->SetDirectory(gROOT);
        t->Draw(Form("dimuon_z_vtx>>hreco_%zu", i), cut, "goff");
        t->Draw(Form("dimuon_z_vtx>>hfine_%zu", i), cut, "goff");
        s.nreco = static_cast<Long64_t>(hf->GetEntries());
        if (hf->Integral() > 0) {
            double q[3], p[3] = {0.16, 0.50, 0.84};
            hf->GetQuantiles(3, q, p);
            s.q16 = q[0]; s.q50 = q[1]; s.q84 = q[2];
        }
        s.h->SetDirectory(nullptr);
        delete hf;
        f->Close();
        delete f;
        const int col = colors[good.size() % NCOL];
        s.h->SetLineColor(col);
        s.h->SetLineWidth(2);
        good.push_back(s);
    }
    if (good.empty()) return;

    // ---- table -----------------------------------------------------------------
    std::cout << "\nselection on reco dimuons: " << cut << "\n";
    printf("%-22s %9s %8s %8s %9s %9s %9s %9s %9s\n", "sample", "truth z", "events", "reco",
           "median", "q16", "q84", "bias", "half-wid");
    for (const auto &s : good)
        printf("%-22s %9.1f %8lld %8lld %9.1f %9.1f %9.1f %9.1f %9.1f\n",
               gSystem->BaseName(s.file.c_str()), s.ztruth, s.nevt, s.nreco, s.q50, s.q16, s.q84,
               s.nreco ? s.q50 - s.ztruth : 0.0, s.nreco ? 0.5 * (s.q84 - s.q16) : 0.0);

    const char *proc = std::string(tag) == "jpsi" ? "J/#psi" : (std::string(tag) == "dy" ? "DY" : tag);

    // ---- plot 1: reco z per sample ----------------------------------------------
    TCanvas *c1 = new TCanvas("c_recoz", "recoz", 1000, 700);
    c1->SetLeftMargin(0.11);
    c1->SetRightMargin(0.30);
    double ymax = 0;
    for (auto &s : good)
        if (s.nreco >= NMIN && s.h->Integral() > 0) {
            s.h->Scale(1.0 / s.h->Integral());
            ymax = std::max(ymax, s.h->GetMaximum());
        }
    TH1D *fr = new TH1D("fr_recoz", "", NB, ZLO, ZHI);
    fr->SetDirectory(nullptr);
    fr->SetMinimum(0);
    fr->SetMaximum(1.15 * std::max(ymax, 1e-3));
    fr->GetXaxis()->SetTitle("reconstructed dimuon z_{vtx} [cm]");
    fr->GetYaxis()->SetTitle("fraction of reco dimuons / 10 cm");
    fr->GetYaxis()->SetTitleOffset(1.4);
    fr->Draw("AXIS");
    TLegend *leg = new TLegend(0.71, 0.12, 0.99, 0.90);
    leg->SetBorderSize(0);
    leg->SetFillStyle(0);
    leg->SetTextSize(0.027);
    leg->SetHeader(Form("%s MC, truth z (N reco)", proc));
    for (auto &s : good) {
        if (s.nreco >= NMIN) s.h->Draw("HIST SAME");
        TLine *l = new TLine(s.ztruth, 0, s.ztruth, fr->GetMaximum());
        l->SetLineColor(s.h->GetLineColor());
        l->SetLineStyle(2);
        if (s.ztruth > ZLO && s.ztruth < ZHI) l->Draw("SAME");
        leg->AddEntry(s.h, Form("z = %.0f cm  (%lld%s)", s.ztruth, s.nreco,
                                s.nreco >= NMIN ? "" : ", not drawn"), "l");
    }
    leg->Draw();
    TLatex tl;
    tl.SetNDC();
    tl.SetTextFont(62);
    tl.SetTextSize(0.045);
    tl.DrawLatex(0.11, 0.92, "SpinQuest Simulation");
    tl.SetTextFont(42);
    tl.SetTextSize(0.028);
    tl.SetTextSize(0.024);
    tl.DrawLatex(0.715, 0.075, "solid: reco z");
    tl.DrawLatex(0.715, 0.040, "dashed: truth z of the sample");
    c1->SaveAs(Form("%s/zscan_%s_recoz.png", dir, tag));
    c1->SaveAs(Form("%s/zscan_%s_recoz.pdf", dir, tag));

    // ---- plot 2: truth z vs reco z ------------------------------------------------
    TCanvas *c2 = new TCanvas("c_tvr", "truth_vs_reco", 800, 750);
    c2->SetLeftMargin(0.13);
    c2->SetGridx();
    c2->SetGridy();
    double lo = 1e9, hi = -1e9;
    for (const auto &s : good) {
        lo = std::min(lo, s.ztruth);
        hi = std::max(hi, s.ztruth);
        if (s.nreco >= NMIN) { lo = std::min(lo, s.q16); hi = std::max(hi, s.q84); }
    }
    const double pad = 0.08 * (hi - lo) + 20;
    TH1D *f2 = new TH1D("fr_tvr", "", 10, lo - pad, hi + pad);
    f2->SetDirectory(nullptr);
    f2->SetMinimum(lo - pad);
    f2->SetMaximum(hi + pad);
    f2->GetXaxis()->SetTitle("truth z_{vtx} [cm]");
    f2->GetYaxis()->SetTitle("reconstructed dimuon z_{vtx} [cm]");
    f2->GetYaxis()->SetTitleOffset(1.5);
    f2->Draw("AXIS");
    TLine *diag = new TLine(lo - pad, lo - pad, hi + pad, hi + pad);
    diag->SetLineStyle(2);
    diag->SetLineColor(kGray + 2);
    diag->Draw("SAME");
    TLatex lab;
    lab.SetTextFont(42);
    lab.SetTextSize(0.024);
    int ilab = 0;
    for (const auto &s : good) {
        if (s.nreco < NMIN) continue;
        TGraphAsymmErrors *gr = new TGraphAsymmErrors(1);
        gr->SetPoint(0, s.ztruth, s.q50);
        gr->SetPointError(0, s.ztruthRms, s.ztruthRms, s.q50 - s.q16, s.q84 - s.q50);
        gr->SetMarkerStyle(20);
        gr->SetMarkerSize(1.2);
        gr->SetMarkerColor(s.h->GetLineColor());
        gr->SetLineColor(s.h->GetLineColor());
        gr->SetLineWidth(2);
        gr->Draw("P SAME");
        lab.SetTextColor(s.h->GetLineColor());
        // stagger the labels (4 vertical slots) so neighbouring samples stay legible
        const double span = hi - lo + 2 * pad;
        const double dy = (0.035 + 0.035 * (ilab % 4)) * span * ((ilab % 2) ? 1.0 : -1.0);
        lab.DrawLatex(s.ztruth + 0.012 * span, s.q50 + dy,
                      Form("z=%.0f: %+.0f", s.ztruth, s.q50 - s.ztruth));
        ++ilab;
    }
    tl.SetTextFont(62);
    tl.SetTextSize(0.045);
    tl.SetTextColor(kBlack);
    tl.DrawLatex(0.13, 0.92, "SpinQuest Simulation");
    tl.SetTextFont(42);
    tl.SetTextSize(0.028);
    tl.DrawLatex(0.16, 0.85, Form("%s MC: median reco z, bars = 16-84%%", proc));
    tl.DrawLatex(0.16, 0.81, "labels: truth z and (median reco #minus truth) [cm]");
    c2->SaveAs(Form("%s/zscan_%s_truth_vs_reco.png", dir, tag));
    c2->SaveAs(Form("%s/zscan_%s_truth_vs_reco.pdf", dir, tag));
}
