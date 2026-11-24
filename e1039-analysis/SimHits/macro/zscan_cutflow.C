// Per-slice cutflow for the z-scan ntuples: where are events lost?
//   root -b -q 'zscan_cutflow.C("zscan_out", "dy")'
// "events" = entries in the ntuple, i.e. already AFTER the SQGeomAcc pair
// acceptance filter in RecoE1039SimZ.C; compare with the number of events
// generated (nevt given to run_dy_zscan.sh) for the acceptance itself.
#include <TFile.h>
#include <TSystem.h>
#include <TTree.h>
#include <glob.h>
#include <algorithm>
#include <cstdio>
#include <string>
#include <vector>

void zscan_cutflow(const char *dir = "zscan_out", const char *tag = "dy",
                   const char *cut = "dimuon_chisq_vx > 0 && dimuon_chisq_vx < 20")
{
    std::vector<std::pair<double, std::string>> F;
    glob_t g;
    const std::string pat = std::string(dir) + "/" + tag + "_z*.root";
    if (glob(pat.c_str(), 0, nullptr, &g) == 0)
        for (size_t i = 0; i < g.gl_pathc; ++i) {
            const std::string base = gSystem->BaseName(g.gl_pathv[i]);
            if (base.find("_DST") != std::string::npos) continue;
            F.push_back({atof(base.substr(base.rfind("_z") + 2).c_str()), g.gl_pathv[i]});
        }
    globfree(&g);
    std::sort(F.begin(), F.end());

    const char *sel[] = {
        "1",                                                        // events in ntuple
        "fpga_trigger[0]",                                          // FPGA1 fired
        "n_tracks >= 1",
        "n_tracks >= 2",
        "Sum$(track_charge > 0) >= 1 && Sum$(track_charge < 0) >= 1", // opposite-sign pair
        "n_dimuons >= 1",
        nullptr,                                                    // >=1 dimuon passing cut
        nullptr};                                                   // ... and within 100 cm of truth
    const std::string c6 = std::string("Sum$(") + cut + ") >= 1";
    const std::string c7 = std::string("Sum$((") + cut + ") && abs(dimuon_z_vtx - truthdimuon_z_vtx[0]) < 100) >= 1";
    sel[6] = c6.c_str();
    sel[7] = c7.c_str();

    printf("%8s %8s %8s %8s %8s %8s %8s %8s %8s\n", "z", "events", "fpga1", "trk>=1", "trk>=2",
           "mu+mu-", "dimuon", "chi2vx", "+dz<100");
    for (const auto &f : F) {
        TFile *fp = TFile::Open(f.second.c_str());
        TTree *t = fp && !fp->IsZombie() ? dynamic_cast<TTree *>(fp->Get("Events")) : nullptr;
        if (!t) { printf("%8.0f  no Events tree\n", f.first); continue; }
        printf("%8.0f", f.first);
        for (const char *s : sel) printf(" %8lld", t->GetEntries(s));
        printf("\n");
        fp->Close();
    }
}
