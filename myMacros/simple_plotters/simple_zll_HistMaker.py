

###########################################
# Plot Maker for quick plots in Zll channel
#
# by David Curry
#
# 2.25.2015
###########################################

import sys
import os
import re
import fileinput
import subprocess
import numpy as np
from decimal import *
from ROOT import *
from ROOT import gROOT
from matplotlib import interactive


#name = '100t-5d-500k'
#name = '100t-7d-500k'
#name = '100t-13d-500k'
#name = '50t-13d-500k'
#name = '50t-13d-1000k'
#name = '300t-5d-500k'
#name = '300t-13d-500k'
name = '1000k-depth20-trees300-v2'


#file = TFile('/exports/uftrig01a/dcurry/heppy/files/prep_out/regression_'+name+'.root')
file = TFile('/exports/uftrig01a/dcurry/heppy/files/prep_out/v23_7_18_ZH125.root')
tree = file.Get('tree')

file_ttbar = TFile('/exports/uftrig01a/dcurry/heppy/files/prep_out/v23_7_18_Zuu.root')
tree_ttbar = file_ttbar.Get('tree')

# Histogram filename
newfile = TFile("plots/jetCorr_plots.root","recreate")

cut  = 'Vtype > -1 & Vtype < 2 & Jet_pt[hJCidx[0]] > 20. & Jet_pt[hJCidx[1]] > 20. & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4'

#cut  = cut +' & Jet_btagCSV[hJCidx[0]] > 0.9 & & Jet_btagCSV[hJCidx[1]] > 0.46'

zlf_cut = cut + ' & HCSV_reg_pt > 100. & V_pt > 100. & abs(HVdPhi) > 2.9 & V_mass > 75. & V_mass < 105. & Jet_btagCSV[hJCidx[0]] < 0.935 & Jet_btagCSV[hJCidx[1]] < 0.460'

data_cut = zlf_cut + ' & (HLT_BIT_HLT_IsoMu20_v || HLT_BIT_HLT_IsoTkMu20_v)'




#============================================== 
# 2D Jet corr plots

'''
c1 = TCanvas('c1')
s1 = THStack('s1', '')

c1.cd()

#h1 = TH3F('h1', '', 50, 20, 220, 30, -2.4, 2.4, 50, 20, 220)
#h2 = TH2F('h2', '', 50, 20, 220, 30, 0.5, 1.5)

#tree.Project('h1', 'Jet_corr:Jet_pt', cut)
#tree_ttbar.Project('h2', "(Jet_pt/Jet_rawPt):Jet_pt", data_cut)

#tree.Project('h1', 'Jet_eta:Jet_pt:hJet_pt_REG')

tree.Draw('Jet_eta:Jet_pt:hJet_pt_REG >> h1', '', 'surf2z')

h1.Draw('surf2z')
c1.Update()
c1.SaveAs('plots/jet_corr.pdf')

# normalize
#h1.Scale(1 / h1.Integral())
#h2.Scale(1 / h2.Integral())

#h1.SetLineWidth(2)
#h1.SetStats(0)

#h2.SetLineWidth(2)
#h2.SetStats(0)


# get the profiles
prof_mc = h1.ProfileX()
prof_mc.SetLineColor(kRed)
prof_data = h2.ProfileX()
prof_data.SetLineColor(kBlack)

prof_mc.SetMinimum(0.95)
prof_mc.SetMaximum(1.15)

prof_mc.SetStats(0)
prof_mc.Draw()
prof_data.Draw('same')
prof_mc.GetXaxis().SetTitle('Jet pT')
prof_mc.GetYaxis().SetTitle('Jet Correction')


#h2.SetLineColor(kRed)
#h2.SetLineWidth(2)
#h2.SetFillStyle(3335)
#h2.SetFillColor(kRed)

#s1.Add(h2)
#s1.Add(h1)
#s1.Draw('lego2')
#s1.GetXaxis().SetTitle('Jet p_{T} [GeV]')

#h1.Draw('lego2')

leg = TLegend(0.62,0.7,0.9,0.9)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.AddEntry(prof_mc, 'ZLF', 'l')
leg.AddEntry(prof_data, 'Data', 'l')
leg.Draw('same')

c1.SaveAs('plots/jet_corr.pdf')
c1.SaveAs('plots/jet_corr.png')
#c1.SaveAs('plots/jet_corr.C')
#c1.SaveAs('plots/jet_corr.root')


# Save the plots
#h1.Write()
#h2.Write()
#del newfile


raw_input('press return to continue')
'''



#==================================================
c1 = TCanvas('c1')
s1 = THStack('s1', '')

c1.cd()

tree.Draw('HCSV_reg_mass_FSR >> h3(100,20,220)', cut)
tree.Draw('HCSV_reg_mass >> h4(100,20,220)', cut)

# normalize
#h3.Scale(1 / h3.Integral())
#h4.Scale(1 / h4.Integral())

h3.SetLineWidth(2)
h3.SetFillColor(kBlue)
h4.SetLineColor(kRed)
h4.SetLineWidth(3)
h3.SetStats(0)
h3.Draw()
h4.Draw('same')

#h4.SetLineColor(kRed)
#h4.SetLineWidth(2)
#h4.SetFillStyle(3335)


#s1.Add(h4)
#s1.Add(h3)
#s1.Draw('nostack')
#s1.GetXaxis().SetTitle('Jet pT Regressed [GeV]')


#leg = TLegend(0.62,0.6,0.9,0.9)
#leg.SetFillStyle(0)
#leg.SetBorderSize(0)
#leg.AddEntry(h3, 'ZH125', 'l')
#leg.AddEntry(h4, 'ttbar', 'l')
#leg.Draw('same')

c1.SaveAs('plots/jet_pt_'+name+'.pdf')
c1.SaveAs('plots/jet_pt_'+name+'.png')

raw_input('press return to continue')

     
     
