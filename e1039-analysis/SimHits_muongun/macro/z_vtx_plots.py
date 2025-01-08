import ROOT
import glob
import subprocess
import sys
ROOT.gROOT.SetBatch(True)
basedir='outputs/'
files=subprocess.check_output(f'ls {basedir} | grep  output_muon | grep -v DST',shell=True,text=True).strip().split('\n')
#print(subdirs)
# Total dataset is 11GB so split up into multiple dataframes. Add the histograms at the end
graph=ROOT.TGraph()
for file in files:
    z_vtx=file[12:-5]
    file=basedir+file
    fz_vtx=float(z_vtx)
    print(file)
    rdf=ROOT.RDataFrame("Events",file) 
    reconstructed=rdf.Filter("n_tracks").Count()
    vreconstructed=reconstructed.GetValue()
    efficiency=float(vreconstructed)/10000
    print(fz_vtx)
    print(efficiency)
    graph.AddPoint(fz_vtx,efficiency)
    htrack_z_vtx = rdf.Histo1D(("track z vtx","track_z_vtx",160,-490,800),"track_z_vtx")
    c=ROOT.TCanvas("c","c")
    htrack_z_vtx.Draw()
    c.Print("results/track_z_vtx"+z_vtx+".png")

c=ROOT.TCanvas("c","c")
graph.Sort()
graph.SetTitle("Reconstruction effieciency relative to vertex z position;z_vtx/cm;efficiency")
graph.Draw("AL*")
c.Print("results/z_vtx_efficiency.png")
fullpath=["outputs/"+file for file in files]
rdf=ROOT.RDataFrame("Events",fullpath)

hdimuon_z_vtx = rdf.Histo1D(("dimuon z vtx","dimuon_z_vtx",160,-600,800),"dimuon_z_vtx")
c1=ROOT.TCanvas("c1","c1")
hdimuon_z_vtx.Draw()
c1.Print("results/dimuon_z_vtx.png")

htruthdimuon_z_vtx = rdf.Histo1D(("truthdimuon z vtx","truthdimuon_z_vtx",160,-600,800),"truthdimuon_z_vtx")
c1_5=ROOT.TCanvas("c1.5","c1.5")
htruthdimuon_z_vtx.Draw()
c1_5.Print("results/truthdimuon_z_vtx.png")

htrack_z_vtx = rdf.Histo1D(("track z vtx","track_z_vtx",160,-490,800),"track_z_vtx")
c2=ROOT.TCanvas("c2","c2")
htrack_z_vtx.Draw()
c2.Print("results/track_z_vtx.png")

htruthtrack_z_vtx = rdf.Histo1D(("truthtrack z vtx","truthtrack_z_vtx",160,-490,800),"truthtrack_z_vtx")
c3=ROOT.TCanvas("c3","c3")
htruthtrack_z_vtx.Draw()
c3.Print("results/truthtrack_z_vtx.png")
'''
rdf540=ROOT.RDataFrame("Events","outputs/output_muon_540.root")
htrack_z_vtx540 = rdf540.Histo1D(("track z vtx 540","track_z_vtx540",160,-490,800),"track_z_vtx")
c4=ROOT.TCanvas("c4","c4")
htrack_z_vtx540.Draw()
c4.Print("results/track_z_vtx540.png")

rdf20=ROOT.RDataFrame("Events","outputs/output_muon_20.root")
htrack_z_vtx20 = rdf20.Histo1D(("track z vtx 20","track_z_vtx20",160,-490,800),"track_z_vtx")
c5=ROOT.TCanvas("c5","c5")
htrack_z_vtx20.Draw()
c5.Print("results/track_z_vtx20.png")
'''
