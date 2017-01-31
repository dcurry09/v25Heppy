# Plot Maker for quick plots
#
# by David Curry
#
# 7.22.1014
###########################################

import sys
import os
import re
from ROOT import *
from matplotlib import interactive
from ROOT import gROOT



# Where to save
outdir = 'Zll_validation_plots/BDT/'

# Root file of Histograms
#file_noReg = TFile('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/limits/2_22_BDT_noRegression_noBin_noSYS/vhbb_TH_BDT_M125_Zee_HighPt.root')
#file_reg   = TFile('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/limits/2_22_BDT_noBin_NoSYS/vhbb_TH_BDT_M125_Zee_HighPt.root')

#file_noReg = TFile.Open('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/limits/2_22_BDT_noRegression_noBin_noSYS/vhbb_TH_BDT_M125_Zee_HighPt.root', 'read')
file_noReg = TFile.Open('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/limits/2_22_BDT_withMET_noBin_noSYS/vhbb_TH_BDT_M125_Zee_HighPt.root', 'read')
file_reg   = TFile.Open('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/limits/2_22_BDT_noBin_NoSYS/vhbb_TH_BDT_M125_Zee_HighPt.root', 'read')

file_reg.cd('ZeeHighPt_13TeV')
Z2b = gDirectory.Get('Zj2b')
Z1b       = gDirectory.Get('Zj1b')
Zlight       = gDirectory.Get('Zj0b')
ttbar       = gDirectory.Get('TT')
ZH125       = gDirectory.Get('ZH')
ggZH125       = gDirectory.Get('ggZH')

file_noReg.cd('ZeeHighPt_13TeV')
Z2b_noReg = gDirectory.Get('Zj2b')
Z1b_noReg = gDirectory.Get('Zj1b')
Zlight_noReg = gDirectory.Get('Zj0b')
ttbar_noReg = gDirectory.Get('TT')
ZH125_noReg = gDirectory.Get('ZH')
ggZH125_noReg = gDirectory.Get('ggZH')





# ====== Make the BDT overlay plot ======

stack  = THStack('stack', '')
canvas = TCanvas('canvas')

# Add the backgrounds
Z2b.Add(Z1b)
Z2b.Add(Zlight)
Z2b.Add(ttbar)
Z2b.SetLineColor(kBlue)
Z2b.SetLineStyle(1)

Z2b_noReg.Add(Z1b_noReg)
Z2b_noReg.Add(Zlight_noReg)
Z2b_noReg.Add(ttbar_noReg)
Z2b_noReg.SetLineColor(kBlue)
Z2b_noReg.SetLineStyle(3)


# Add the signals
ZH125.Add(ggZH125)
ZH125.SetLineColor(kRed)
ZH125.SetLineStyle(1)

ZH125_noReg.Add(ggZH125)
ZH125_noReg.SetLineColor(kRed)
ZH125_noReg.SetLineStyle(3)

# normalize
Z2b.Scale(1 / Z2b.Integral())
Z2b_noReg.Scale(1 / Z2b_noReg.Integral())
ZH125.Scale(1 / ZH125.Integral())
ZH125_noReg.Scale(1 / ZH125_noReg.Integral())

#Legend
leg = TLegend(0.5,0.6,0.7,0.9)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.AddEntry(Z2b, 'BKG w/Regression', 'l')
leg.AddEntry(Z2b_noReg, 'BKG w/MET', 'l')
leg.AddEntry(ZH125, 'SIG w/Regression', 'l')
leg.AddEntry(ZH125_noReg, 'SIG w/MET', 'l')


canvas.cd()
stack.Add(Z2b)
stack.Add(ZH125)
stack.Add(Z2b_noReg)
stack.Add(ZH125_noReg)
stack.Draw('nostackHIST')
leg.Draw('same')

canvas.SaveAs('Zll_validation_plots/BDT/BDT_output_noReg_wReg.pdf')


# ======================================

raw_input('Press return to continue...')


