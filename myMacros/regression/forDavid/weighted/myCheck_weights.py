from ROOT import *
from ROOT import gROOT
import math
import numpy as np
from matplotlib import interactive
import os


#file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/jetPt_weighted/v14_11_2015_ZH125.root')
file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/regression/dec_zll_genJet_boost/v14_11_2015_ggZH125.root')
tree = file.Get('tree')



hJet_pt_weight = TH1F('hJet_pt_weight', '' , 100, 0, 150)
hJet_pt = TH1F('hJet_pt', '' , 100, 0, 150)

hRes = TH1F('hRes', '' , 30, -1, 1)
hRes_noReg = TH1F('hRes_noReg', '' , 30, -1, 1)


def deltaPhi(phi1, phi2):
    result = phi1 - phi2
    while (result > math.pi): result -= 2*math.pi
    while (result <= -math.pi): result += 2*math.pi
    return result

def deltaR(phi1, phi2, eta1, eta2):
    deta = eta1 - eta2
    dphi = deltaPhi(phi1, phi2)
    #dphi = phi1 - phi2
    #if dphi > np.pi: dphi -= 2*np.pi
    #if dphi <= -np.pi: dphi += 2*np.pi
    return np.sqrt(dphi*dphi + deta*deta)


for ievt in range(tree.GetEntries()):

    tree.GetEntry(ievt)

    if ievt > 10000: break

    if ievt % 10000 == 0: print '-----> Event # ', ievt
    
    for ijet in range(tree.nJet):
        if ijet > 14: continue
        #hJet_pt_weight.Fill(tree.Jet_pt[ijet], tree.weight_etaPt[ijet])
        #hJet_pt.Fill(tree.Jet_pt[ijet])

    #if tree.HCSV_pt < 100: continue    

    # check Dr with genJets
    for iJet in range(2):

        for iGen in range(tree.nGenJet):

            #if tree.GenJet_numBHadrons[iGen] > 0: continue
            if tree.GenJet_wNuPt[iGen] > 20 and abs(tree.GenJet_wNuEta[iGen]) < 2.4 and tree.GenJet_numCHadrons[iGen] > 0: continue
            
            
            dr = deltaR(tree.GenJet_wNuPhi[iGen], tree.Jet_phi[tree.hJCidx[iJet]], tree.GenJet_wNuEta[iGen], tree.Jet_eta[tree.hJCidx[iJet]])
            
            if dr < 0.2:
                hRes.Fill( (tree.Jet_pt_REG[iJet] - tree.GenJet_wNuPt[iGen])/tree.GenJet_wNuPt[iGen] )
                hRes_noReg.Fill( (tree.Jet_pt[tree.hJCidx[iJet]] - tree.GenJet_wNuPt[iGen])/tree.GenJet_wNuPt[iGen] )
                break


# end event loop


'''
# Draw the Hist
canvas = TCanvas('canvas')
canvas.cd()

hJet_pt_weight.Scale(1./(hJet_pt_weight.Integral()))
hJet_pt_weight.SetStats(0)
hJet_pt_weight.SetFillColor(kYellow)
hJet_pt_weight.GetXaxis().SetTitle('p_{T} [GeV}')
hJet_pt_weight.Draw()

canvas.SaveAs('pt_weighted.pdf')

canvas2 = TCanvas('canvas2')
canvas2.cd()

hJet_pt.Scale(1./(hJet_pt.Integral()))
hJet_pt.SetStats(0)
hJet_pt.SetFillColor(kYellow)
hJet_pt.GetXaxis().SetTitle('p_{T} [GeV}')
hJet_pt.Draw()

canvas2.SaveAs('pt_noWeights.pdf')
'''

canvas3 = TCanvas('canvas3')
canvas3.cd()

s1 = THStack('s1', '')

hRes.SetLineColor(kRed)
s1.Add(hRes)
s1.Add(hRes_noReg)
s1.Draw('nostack')

res = RooRealVar("res","res",-1,1,"GeV")
bC_p0=RooRealVar("bC_p0", "bC_p0", -0.5, 0.5)
bC_p1=RooRealVar("bC_p1", "bC_p1", 0., 0.5)
bC_p2=RooRealVar("bC_p2", "bC_p2", -1, 1.)
bC_p3=RooRealVar("bC_p3", "bC_p3", -1., 1.)
bC_p4=RooRealVar("bC_p4", "bC_p4", -1., 1.)
bukin_ = RooBukinPdf("bukin_", "Bukin function", res, bC_p0,bC_p1,bC_p2,bC_p3,bC_p4)

signalHistogram= RooDataHist("signalHistogram", "Signal Histogram", RooArgList(res), hRes)
bukin_.fitTo(signalHistogram, RooFit.Range(-0.3, 0.3), RooFit.Save())

plot = res.frame();
signalHistogram.plotOn(plot, RooFit.MarkerColor(2));
bukin_.plotOn(plot, RooFit.LineColor(2), RooFit.LineWidth(0));
plot.Draw("sames")

hReg_std = bC_p1.getVal()
hReg_mu = bC_p0.getVal()
hReg_metric = hReg_std/hReg_mu
hReg_std=str(round(hReg_std,4))
hReg_mu=str(round(hReg_mu,4))
hReg_metric_str = str(round(hReg_metric,3))

signalHistogram2= RooDataHist("signalHistogram2", "Signal Histogram", RooArgList(res), hRes_noReg)
signalHistogram2.plotOn(plot, RooFit.MarkerColor(1));

bukin_.fitTo(signalHistogram2, RooFit.Range(-0.3, 0.3), RooFit.Save())
bukin_.plotOn(plot, RooFit.LineColor(1), RooFit.LineWidth(0));
plot.Draw("sames")

hNom_std=bC_p1.getVal()
hNom_mu=bC_p0.getVal()
mass_metric1 = hNom_std/hNom_mu
hNom_std=str(round(hNom_std,4))
hNom_mu=str(round(hNom_mu,4))
mass_metric1_str = str(round(mass_metric1,3))

#l = TLatex()
#l.SetNDC()
#l.SetTextSize(0.03)
#l.DrawLatex(0.1, 0.93, myHeader)
#l.Draw('same')

leg = TLegend(0.62,0.6,0.9,0.9)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.AddEntry(hRes, 'Regressed', 'l')
leg.AddEntry(0, 'RMS='+hReg_std, '')
leg.AddEntry(0, 'Mean='+hReg_mu, '')
#leg.AddEntry(0, '#sigma/#mu='+hReg_metric_str, '')
leg.AddEntry(hRes_noReg, 'Nominal', 'l')
leg.AddEntry(0, 'RMS='+hNom_std, '')
leg.AddEntry(0, 'Mean='+hNom_mu, '')
#leg.AddEntry(0, '#sigma/#mu='+mass_metric1_str, '')
leg.AddEntry(0, '', '')
#x = leg.AddEntry(0, 'Improvement='+str(round(percent_improvement,1))+'%', '')
#x.SetTextColor(kRed)
#x.SetTextSize(0.03)
leg.Draw('same')

  
raw_input('press return to continue')
