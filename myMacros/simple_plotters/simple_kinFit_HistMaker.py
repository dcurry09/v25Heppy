###########################################
# Plot Maker for quick plots
#
# by David Curry
#
# 7.22.1014
###########################################

import sys
import os
from ROOT import *
from ROOT import gROOT
from matplotlib import interactive

# for Kin Fit
file_kf = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v11_04_17_2015_Zllv11_train_Zll_noMET_kinFit.root')
tree_kf = file_kf.Get('tree')

# Post Regression, Pre KinFit
file_regr = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v11_04_17_2015_Zllv11_train_Zll_noMET.root')
tree_regr = file_regr.Get('tree')

# Pre Regression
file_old = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/v11_04_17_2015_Zll.root')
tree_old = file_old.Get('tree')


header = '#sqrt{s}=13TeV,   Z(l^{-}l^{+})H(b#bar{b}),   CMS Simulation'

title = 'v11_kinFit'


# ===== Plot the DiJet Mass ======

cMass = TCanvas('cMass')
sMass = THStack('sMass', '')

mass     = TH1F('mass', '' , 50, 20, 220)
mass_regr = TH1F('mass_regr', '' , 50, 20, 220)
mass_regr_kf = TH1F('mass_regr_kf', '' , 50, 20, 220)


# Cuts
cut  = 'H_pt > 0 & Jet_pt[hJidx[0]] > 20. & Jet_pt[hJidx[1]] > 20. & abs(Jet_eta[hJidx[0]]) < 2.4 & abs(Jet_eta[hJidx[1]]) < 2.4'

# only test on odd events
cut = cut +' & evt%2 != 0'

# additional Jet
#cut = cut+ ' & naJidx > 1 '

# V cut(Zll)
#if Zll: cut = cut +' & V_mass < 105 & V_mass > 75'

# MET(Zll)
#if Zll: cut = cut +' & met_pt < 60'

# MET(Wlv)
#if Wlv: cut = cut +' & met_pt > 45'

# MET(Zvv)
#if Zvv: cut = cut +' & met_pt > 130'

# CMVA cut
#cut = cut +' & Jet_btagCSV[hJidx[0]] > 0.76 & Jet_btagCSV[hJidx[1]] > 0.7'

# btagged jets
cut = cut +' & abs(Jet_mcFlavour[hJidx[0]]) == 5 & abs(Jet_mcFlavour[hJidx[1]]) == 5'

# project the branch into a histogram, (hist, branch, cuts)
tree_kf.Project('mass_regr_kf', 'H_mass_kf', cut)
tree_regr.Project('mass_regr', 'HCSV_mass', cut)
tree_old.Project('mass', 'HCSV_mass', cut)


print '==== Mass Entries ===='
print 'Regressed : ', mass_regr.GetEntries()
print 'Baseline  : ', mass.GetEntries()


mass.Scale(1 / mass.GetEntries())
mass_regr.Scale(1 / mass_regr.GetEntries())
mass_regr_kf.Scale(1 / mass_regr_kf.GetEntries())

mass.SetStats(0)
mass_regr.SetLineColor(kRed)
mass_regr_kf.SetLineColor(kGreen)

sMass.Add(mass)
sMass.Add(mass_regr)
sMass.Add(mass_regr_kf)
sMass.Draw('nostack')

sMass.SetTitle('')
sMass.GetYaxis().SetTitle('Entries/4[GeV]')
sMass.GetXaxis().SetTitle('m(jj) [GeV]')


# Gaussian Fits
fit_min = 90
fit_max = 145

mass.Fit('gaus', 'Q','same', 90, 135)
fit=mass.GetFunction('gaus')
fit.SetLineColor(kBlue)
mass_std = fit.GetParameter(2)
mass_mu = fit.GetParameter(1)
mass_metric = mass_std/mass_mu
mass_std=str(round(mass_std,4))
mass_mu=str(round(mass_mu,4))
mass_metric = str(round(mass_metric,4))

mass_regr.Fit('gaus', 'Q', 'same', fit_min, fit_max)
fit2=mass_regr.GetFunction('gaus')
fit2.SetLineColor(kRed)
mass_reg_std=fit2.GetParameter(2)
mass_reg_mu=fit2.GetParameter(1)
mass_metric1 = mass_reg_std/mass_reg_mu
mass_reg_std=str(round(mass_reg_std,4))
mass_reg_mu=str(round(mass_reg_mu,4))
mass_metric1 = str(round(mass_metric1,4))

mass_regr_kf.Fit('gaus', 'Q', 'same', fit_min, fit_max)
fit3=mass_regr_kf.GetFunction('gaus')
fit3.SetLineColor(kGreen)
mass_kf_std=fit3.GetParameter(2)
mass_kf_mu=fit3.GetParameter(1)
mass_metric3 = mass_kf_std/mass_kf_mu
mass_kf_std=str(round(mass_kf_std,4))
mass_kf_mu=str(round(mass_kf_mu,4))
mass_metric3 = str(round(mass_metric3,4))

leg = TLegend(0.62,0.6,0.9,0.9)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.AddEntry(mass, 'Nominal', 'l')
leg.AddEntry(0, '#sigma='+mass_std, '')
leg.AddEntry(0, '#mu='+mass_mu, '')
leg.AddEntry(0, '#sigma/#mu='+mass_metric, '')

leg.AddEntry(mass_regr, 'Regressed', 'l')
leg.AddEntry(0, '#sigma='+mass_reg_std, '')
leg.AddEntry(0, '#mu='+mass_reg_mu, '')
leg.AddEntry(0, '#sigma/#mu='+mass_metric1, '')

leg.AddEntry(mass_regr_kf, 'Regressed(w/ KinFit)', 'l')
leg.AddEntry(0, '#sigma='+mass_kf_std, '')
leg.AddEntry(0, '#mu='+mass_kf_mu, '')
leg.AddEntry(0, '#sigma/#mu='+mass_metric3, '')

leg.Draw('same')

l_1 = TLatex()
l_1.SetNDC()
l_1.SetTextSize(0.03)
l_1.DrawLatex(0.1, 0.93, header)
l_1.Draw('same')

cMass.SaveAs('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/myMacros/plots/regression/kinFit_dijet_mass_'+title+'.pdf')




raw_input('press return to continue')
