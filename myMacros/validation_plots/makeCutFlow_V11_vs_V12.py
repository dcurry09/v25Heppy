import ROOT
import sys
from math import sqrt
import os

# plot relative cut efficiencies w.r.t. previous cuts
doRelative = False
#doRelative = True 


# Where to save plots
outdir = '~/www/v25_cutflow/'

try:
    os.system('mkdir '+outdir)
except:
     print outdir+' already exists...'

temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outdir
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outdir

os.system(temp_string2)
os.system(temp_string3)



ROOT.gROOT.SetBatch(True)

tree_SIG = ROOT.TChain("tree")
tree_SIG.Add("/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_ZH125.root")
denominator_cut_SIG = "abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4 & vLeptons_new_pt[0] > 15. & vLeptons_new_pt[1] > 15."

tree_MC = ROOT.TChain("tree")
#tree_MC.Add("/exports/uftrig01a/dcurry/heppy/files/MVA_out/v24_9_15_DY_200to400.root")
tree_MC.Add("/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_DY_inclusive.root")
tree_MC.Add("/exports/uftrig01a/dcurry/heppy/files/MVA_out/v25_DY_100to200.root")
#tree_MC.Add("/exports/uftrig01a/dcurry/heppy/files/MVA_out/v24_9_15_DY_400to600.root")
#tree_MC.Add("/exports/uftrig01a/dcurry/heppy/files/MVA_out/v24_9_15_DY_600toInf.root")
denominator_cut_MC = denominator_cut_SIG


# order: (cutlabel, cutstring_MC, custring_13TeV)
cuts = {
    #1: ("PreSelection", "abs(Jet_eta[hJCidx[0]]) < 2.4"),
    1: ("pT(ll)>50", "V_new_pt > 50"),  
    2: ("pT(ll)>150", "V_new_pt > 150"),
    3: ("75<mass(ll)<105", "V_new_mass > 75 && V_new_mass < 105"),
    #5: ("Jet_pt>20", "Jet_pt_reg[hJCidx[0]]>20 && Jet_pt_reg[hJCidx[1]]>20"),
    4: ("90<mass(jj)<150", "HCMVAV2_reg_mass > 90 && HCMVAV2_reg_mass < 150"),
    5: ("JetCSV>loose", "Jet_btagCMVAV2[hJCMVAV2[0]]>-0.5884 && Jet_btagCMVAV2[hJCMVAV2idx[1]]>-0.5884"),
    6: ("#delta #phi(V,H)>2.5", "abs(HVdPhi) > 2.5")
    
    #-1:        ("ElID", "cutFlow>=5&&isWenu", "cutFlow>=5 && isWenu==1"),

    #5:      ("MuID", "cutFlow>=5 && isWmunu==1", "cutFlow>=5 && isWmunu==1"),
    #7:      ("AddLep", "cutFlow>=7", "cutFlow>=7"),

    #2:      ("HJetSel", "(hJet_ptCorr[0]>30. &&hJet_ptCorr[1]>30. && hJet_puJetIdL[0]>0.0 && hJet_puJetIdL[1]>0.0) && (max(hJet_csvReshapedNew[0],hJet_csvReshapedNew[1])>0.898 && max(hJet_csvReshapedNew[0],hJet_csvReshapedNew[1])<10.0 && min(hJet_csvReshapedNew[0],hJet_csvReshapedNew[1])>0.5 && min(hJet_csvReshapedNew[0],hJet_csvReshapedNew[1])<10.0)", "cutFlow>=2"),
    #1:      ("HJetSel", " cutFlow>=2&&Jet_btagCSV[hJetInd1]>0.935", "cutFlow>=2&&Jet_btagCSV[hJetInd1]>0.935"),
    #-1:        ("hbhe", "hbhe","WTH is this?"),
    #-1:      ("HVDPhi", "cutFlow>=9", "cutFlow>=9"),
    #1:      ("Trigger", "cutFlow>=1", "cutFlow>=1"),
    #9:      ("MetSig", "met_pt/sqrt(met_sumEt)>2", "met_pt/sqrt(met_sumEt)>2"),
    #10:     ("CSV","Jet_btagCSV[hJetInd1] > 0.97", "Jet_btagCSV[hJetInd1] > 0.97"),
}

for key in cuts.keys():
    if (key == -1): del cuts[key]

print "number of entries in the MC denominator region: %i " % tree_MC.GetEntries(denominator_cut_MC)
print "number of entries in the SIG denominator region: %i " % tree_SIG.GetEntries(denominator_cut_SIG)

cutflow_MC = ROOT.TH1F("cutflow", "cutflow", len(cuts.keys())+1, 0, len(cuts.keys())+1 )
cutflow_SIG = ROOT.TH1F("cutflow", "cutflow", len(cuts.keys())+1, 0, len(cuts.keys())+1 )


keys = cuts.keys()
keys.sort()

full_cutstring_MC  = denominator_cut_MC
full_cutstring_SIG = denominator_cut_SIG

h1 = ROOT.TH1F("h1","h1",100,0,100)
tree_MC.Draw("run>>h1","(%s)" % denominator_cut_MC)
cutflow_MC.Fill(0, h1.Integral() )
cutflow_MC.GetXaxis().SetBinLabel(1, "denom")

h2 = ROOT.TH1F("h2","h2",100,0,100)
tree_SIG.Draw("run>>h2","(%s)" % denominator_cut_SIG)
cutflow_SIG.Fill(0, h2.Integral() )
cutflow_SIG.GetXaxis().SetBinLabel(1, "denom")

#SIGScale = 2991609  # number of generated MC events
#SIGScale = 2991609 * (50001./2861195.)  # number of generated MC events, correct for the partial sample size
SIGScale = 0.261*10000


for index in keys:
    if (index == -1): continue
    print "index: %i" % index
    print "filling cut %s" % cuts[index][0]
    #print "cut_MC: %s" % cuts[index][1]
    #print "cut_SIG: %s" % cuts[index][2]
    full_cutstring_MC += " && (%s)" % cuts[index][1]
    full_cutstring_SIG   += " && (%s) " % cuts[index][1]
    print "full cutstring MC: %s" % full_cutstring_MC
    print "full cutstring SIG: %s " % full_cutstring_SIG
    #npass_mc = tree_MC.GetEntries(full_cutstring_MC)

    h1 = ROOT.TH1F("h1","h1",100,0,100)
    tree_MC.Draw("run>>h1","(%s)*DY_specialWeight" % full_cutstring_MC)
    npass_mc = h1.Integral()

    h2 = ROOT.TH1F("h2","h2",100,0,100)
    tree_SIG.Draw("run>>h2","(%s)" % full_cutstring_SIG)
    npass_SIG = h2.Integral()

    print '', npass_mc, npass_SIG
    #print (1.0*npass_SIG)/SIGScale 
    cutflow_MC.Fill(index, npass_mc)
    cutflow_MC.GetXaxis().SetBinLabel(index+1, cuts[index][0])
    cutflow_SIG.Fill(index, npass_SIG)
    cutflow_SIG.GetXaxis().SetBinLabel(index+1, cuts[index][0])

# normalize to first bin
cutflow_MC.Scale(1./cutflow_MC.GetBinContent(1))
cutflow_SIG.Scale(1./cutflow_SIG.GetBinContent(1))


effLumi = 7685000.
#effLumi = 237871.21
#effLumi = 449715.5
xsec = 0.133 # xsec*BR
#xsec = 247.74 # xsec*BR
#xsec = 23.64
#MCScale = (effLumi * xsec)
MCScale = 100801
#MCScale = 2113969

## since I can't figure out the number of ttbar MC raw events, let's hack it and assume
## that the MC and 13 TeV are parallel after the V/H pt cuts
#1000.0 * (DataLumi / effLumi) * PUweight * weightTrig2012A

if (doRelative):
    # plot relative cut efficiency w.r.t. to previous cuts
    for i in range(cutflow_MC.GetNbinsX(), 0, -1):
        print '\nindex:',i
        if (i==1): 
            cutflow_MC.SetBinContent(i,1.0)
            cutflow_SIG.SetBinContent(i,1.0)
            continue
        print "cutflow_MC.GetBinContent(i-1) = %f" % cutflow_MC.GetBinContent(i-1)
        print "cutflow_MC.GetBinContent(i) = %f" % cutflow_MC.GetBinContent(i)
        print "bin will be set to: %f" % (cutflow_MC.GetBinContent(i)/cutflow_MC.GetBinContent(i-1))
        print "cutflow_SIG.GetBinContent(i-1) = %f" % cutflow_SIG.GetBinContent(i-1)
        print "cutflow_SIG.GetBinContent(i) = %f" % cutflow_SIG.GetBinContent(i)
        print "bin will be set to: %f" % (cutflow_SIG.GetBinContent(i)/cutflow_SIG.GetBinContent(i-1))
        if (cutflow_MC.GetBinContent(i-1) != 0):
            cutflow_MC.SetBinContent(i,cutflow_MC.GetBinContent(i)/cutflow_MC.GetBinContent(i-1))
        if (cutflow_SIG.GetBinContent(i-1) != 0):
            cutflow_SIG.SetBinContent(i,cutflow_SIG.GetBinContent(i)/cutflow_SIG.GetBinContent(i-1))



cutflow_SIG.SetTitle("Z(ll)H(bb) Cutflow")
cutflow_MC.SetLineWidth(3)
cutflow_SIG.SetLineWidth(3)
cutflow_MC.SetLineColor(ROOT.kBlue)
cutflow_SIG.SetLineColor(ROOT.kRed)

leg = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)

#if (doRelative): 
#    leg = ROOT.TMcend(0.7,0.2,0.9,0.4)


leg.AddEntry(cutflow_SIG, "ZHbb Signal MC", "l")
leg.AddEntry(cutflow_MC, "DY BKG MC", "l")

ROOT.gStyle.SetOptStat(0)
maxval = max(cutflow_MC.GetMaximum(), cutflow_SIG.GetMaximum())*1.5
minval = min(cutflow_MC.GetMinimum(), cutflow_SIG.GetMinimum())/2.
cutflow_SIG.SetMaximum(maxval)
cutflow_SIG.SetMinimum(minval)

cutflow_SIG.SetTitle('')

canv = ROOT.TCanvas("canv", "canv", 800, 800)
canv.SetLogy()

doDivide = False

if (doDivide):
    canv.cd()
    pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,1)
    #pad1.SetTopMargin(0)
    pad1.Draw()
    pad1.cd()
    pad1.SetLogy()
    cutflow_SIG.Draw("hist text0 same")
    cutflow_MC.Draw("hist text0 same")
    leg.Draw("same")
    canv.cd()
    pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.3)
    #pad2.SetBottomMargin(0)
    pad2.Draw()
    pad2.cd()
    pad2.SetGrid(True)
    #cutflow_SIG.Sumw2()
    #cutflow_MC.Sumw2()
    cutflow_ratio = cutflow_SIG.Clone()
    cutflow_ratio.Divide(cutflow_MC)
    cutflow_ratio.SetMarkerColor(4)
    cutflow_ratio.SetMarkerSize(0.8)
    cutflow_ratio.SetMarkerStyle(20)
    cutflow_ratio.SetLineColor(4)
    cutflow_ratio.SetLineWidth(2)
    cutflow_ratio.SetMaximum(2.0)
    cutflow_ratio.SetMinimum(0.5)
    cutflow_ratio.GetYaxis().SetNdivisions(505)
    cutflow_ratio.SetTitle('')
    cutflow_ratio.GetYaxis().SetLabelSize(0.15)
    cutflow_ratio.GetYaxis().SetTitle('')
    cutflow_ratio.Sumw2()
    for ibin in range(cutflow_ratio.GetNbinsX() + 1):
        if (cutflow_ratio.GetBinContent(ibin) != 0):
            cutflow_ratio.SetBinError(ibin, cutflow_ratio.GetBinContent(ibin)*sqrt((1./cutflow_SIG.GetBinContent(ibin)) + (1./cutflow_MC.GetBinContent(ibin))))
            print "ibin = ",ibin, ": ", cutflow_ratio.GetBinContent(ibin), ": ", cutflow_ratio.GetBinError(ibin), ", sqrt stuff: ", sqrt((1./cutflow_SIG.GetBinContent(ibin)) + (1./cutflow_MC.GetBinContent(ibin)))
        else: cutflow_ratio.SetBinError(ibin, 0.)
    cutflow_ratio.Draw('PE same')
    canv.cd()

else:
    cutflow_SIG.Draw("hist text0 ")
    cutflow_MC.Draw("hist text0 same")
    leg.Draw("same")
#raw_input()
canv.SaveAs(outdir+"cutflow.png")
canv.SaveAs(outdir+"cutflow.pdf")
#canv.SaveAs("cutflow.C")
#ifile_MC.Close()
#ifile_SIG.Close()

    


