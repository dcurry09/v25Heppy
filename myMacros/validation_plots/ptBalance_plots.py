###########################################
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
outdir = 'Zll_validation_plots/v21_ptBalance/'

# Root file of Histograms
file_reg   = TFile('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/plots/basic_out/jet_regression_Zhf/ptBalance.root')
file_noReg = TFile('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/plots/basic_out/jet_regression_Zhf/ptBalance_noReg.root') 


Z2b       = file_reg.Get('Z2b')
Z2b_noReg = file_noReg.Get('Z2b')
Z2b_title = 'Z2b'

Z1b       = file_reg.Get('Z1b')
Z1b_noReg = file_noReg.Get('Z1b')
Z1b_title = 'Z1b' 

Zlight       = file_reg.Get('Zudsg')
Zlight_noReg = file_noReg.Get('Zudsg')
Zlight_title = 'Zudscg'

ttbar       = file_reg.Get('ttbar')
ttbar_noReg = file_noReg.Get('ttbar')
ttbar_title = 'ttbar'

ZH125       = file_reg.Get('ZH125')
ZH125_noReg = file_noReg.Get('ZH125')
ZH125_title = 'ZH125'


def do_balance_plot(hReg, hNom, title):

     print '\n----> Making plot for', hReg

     stack  = THStack('stack', '')
     canvas = TCanvas('canvas')

     hReg.SetStats(0)
     hReg.SetLineColor(kRed)
     hNom.SetLineColor(kBlue)
     hReg.SetFillColor(0)
     hNom.SetFillColor(0)
     hReg.SetLineWidth(3)
     hNom.SetLineWidth(3)
     
     canvas.cd()
     stack.Add(hReg)
     stack.Add(hNom)
     stack.Draw('nostackHIST')
     stack.GetXaxis().SetTitle('Pt Balance: p_{T}(jj) / p_{T}(ll)')
     stack.GetYaxis().SetTitle('Entries/0.13')

     # New STats from TPaveStats
     hReg_metric = hReg.GetRMS()/hReg.GetMean()
     hNom_metric = hNom.GetRMS()/hNom.GetMean()
     percent_improvement = (1-(hReg_metric/hNom_metric))*100
     hReg_std = str(round(hReg.GetRMS(),3))
     hReg_mu  = str(round(hReg.GetMean(),3))
     hNom_std = str(round(hNom.GetRMS(),3))
     hNom_mu  = str(round(hNom.GetMean(),3))


     l = TLatex()
     l.SetNDC()
     l.SetTextSize(0.03)
     l.DrawLatex(0.1, 0.93, '#sqrt{s}=13TeV, '+title )
     l.Draw('same')
     
     leg = TLegend(0.62,0.6,0.9,0.9)
     leg.SetFillStyle(0)
     leg.SetBorderSize(0)
     leg.AddEntry(hReg, 'Regressed', 'l')
     leg.AddEntry(0, 'RMS='+hReg_std, '')
     leg.AddEntry(0, 'Mean='+hReg_mu, '')
     #leg.AddEntry(0, '#sigma/#mu='+hReg_metric_str, '')
     leg.AddEntry(hNom, 'Nominal', 'l')
     leg.AddEntry(0, 'RMS='+hNom_std, '')
     leg.AddEntry(0, 'Mean='+hNom_mu, '')
     #leg.AddEntry(0, '#sigma/#mu='+mass_metric1_str, '')
     leg.AddEntry(0, '', '')
     #x = leg.AddEntry(0, 'Improvement='+str(round(percent_improvement,1))+'%', '')
     #x.SetTextColor(kRed)
     #x.SetTextSize(0.03)
     leg.Draw('same')
     
     canvas.SaveAs(outdir+'pt_balance_'+title+'.pdf')
     
# end def do plot

#do_balance_plot(Z2b, Z2b_noReg, Z2b_title)

#do_balance_plot(Z1b, Z1b_noReg, Z1b_title)

#do_balance_plot(Zlight, Zlight_noReg, Zlight_title)

#do_balance_plot(ttbar, ttbar_noReg, ttbar_title)

#do_balance_plot(ZH125, ZH125_noReg, ZH125_title)


# Last thing make a summed plot

Z2b.Add(Z1b)
Z2b.Add(Zlight)
Z2b.Add(ttbar)
Z2b.Add(ZH125)

Z2b_noReg.Add(Z1b_noReg)
Z2b_noReg.Add(Zlight_noReg)
Z2b_noReg.Add(ttbar_noReg)
Z2b_noReg.Add(ZH125_noReg)

do_balance_plot(Z2b, Z2b_noReg, 'All_BKG+SIG')


raw_input('Press return to continue...')

