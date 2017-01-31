# Plot Maker for quick Profile plots in ttbar CR
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
import ConfigParser
from collections import Counter

indir = 'v24_ICJEP_CMVA'

# DC file
file_e_low = TFile.Open('/afs/cern.ch/work/d/dcurry/public/cmva_heppy/CMSSW_7_1_5/src/VHbb/limits/'+indir+'/vhbb_TH_BDT_Zee_LowPt.root', 'read')
tree_e_low = gDirectory.Get('ZeeLowPt_13TeV')

file_e_high = TFile.Open('/afs/cern.ch/work/d/dcurry/public/cmva_heppy/CMSSW_7_1_5/src/VHbb/limits/'+indir+'/vhbb_TH_BDT_Zee_HighPt.root', 'read')
tree_e_high = gDirectory.Get('ZeeHighPt_13TeV')

file_m_low = TFile.Open('/afs/cern.ch/work/d/dcurry/public/cmva_heppy/CMSSW_7_1_5/src/VHbb/limits/'+indir+'/vhbb_TH_BDT_Zuu_LowPt.root', 'read')
tree_m_low = gDirectory.Get('ZuuLowPt_13TeV')

file_m_high = TFile.Open('/afs/cern.ch/work/d/dcurry/public/cmva_heppy/CMSSW_7_1_5/src/VHbb/limits/'+indir+'/vhbb_TH_BDT_Zuu_HighPt.root', 'read')
tree_m_high = gDirectory.Get('ZuuHighPt_13TeV')


# list of signals/bkgs to get
list = ['ZH', 'ggZH', 'Zj2b', 'Zj1b', 'Zj0b', 'TT', 's_Top', 'VVLF', 'VVHF']

 
ele_count_low = Counter()
mu_count_low  = Counter()
ele_count_high = Counter()
mu_count_high  = Counter()

Zee_bkg_tot = 0
Zee_sig_tot = 0
Zuu_bkg_tot = 0
Zuu_sig_tot = 0

sig_tot = 0
bkg_tot = 0

for region in list:
    
    hist_e_low = tree_e_low.Get(region) 
    hist_e_high = tree_e_high.Get(region)
    
    #print region,': ', hist_e.Integral(), 'error:',  hist_e.Integral() * 1./sqrt(hist_e.GetEffectiveEntries())

    # Get the 4 most sensnitve bins
    #print region,': ', hist_e.Integral(12,15)
    #'error:',  hist_m.Integral(12,15) * 1./sqrt(hist_m.Integral(12,15))

    ele_count_low[region] += hist_e_low.Integral()  
    ele_count_high[region] += hist_e_high.Integral()

    if region == 'ZH' or region == 'ggZH':
        Zee_sig_tot += hist_e_low.Integral()
        Zee_sig_tot += hist_e_high.Integral()

    else: 
        Zee_bkg_tot += hist_e_low.Integral()
        Zee_bkg_tot += hist_e_high.Integral()

    hist_e_low.IsA().Destructor(hist_e_low)
    hist_e_high.IsA().Destructor(hist_e_high)


for region in list:

    hist_m_low  = tree_m_low.Get(region)
    hist_m_high = tree_m_high.Get(region)

    mu_count_low[region]  += hist_m_low.Integral()
    mu_count_high[region] += hist_m_high.Integral()

    #print region,': ', hist_m.Integral(), 'error:',  hist_m.Integral() * 1./sqrt(hist_m.GetEffectiveEntries())

    # Get the 4 most sensnitve bins
    #print region,': ', hist_m.Integral(12,15) 
    #'error:',  hist_m.Integral(12,15) * 1./sqrt(hist_m.Integral(12,15))

    if region =='ZH' or region == 'ggZH':
        Zuu_sig_tot += hist_m_low.Integral()
        Zuu_sig_tot += hist_m_high.Integral()

    else: 
        Zuu_bkg_tot += hist_m_low.Integral()
        Zuu_bkg_tot += hist_m_high.Integral()

    hist_m_low.IsA().Destructor(hist_m_low)
    hist_m_high.IsA().Destructor(hist_m_high)


print '===== Results ======'

print 'Total Signal    :', Zuu_sig_tot + Zee_sig_tot
print 'Total Background:', Zuu_bkg_tot + Zee_bkg_tot

print '\n####### Muon ######'
print 'Low pT:', mu_count_low
print '\nHigh pT:', mu_count_high
print '\nCombined:', mu_count_low + mu_count_high


print '\n\n####### Electron ######'
print 'Low pT:', ele_count_low
print '\nHigh pT:', ele_count_high
print '\nCombined:', ele_count_low + ele_count_high


print '\n\n####### Electron + Muon ######'
print 'Low pT:', ele_count_low + mu_count_low
print '\nHigh pT:', ele_count_high + mu_count_high
print '\nCombined:', ele_count_low + ele_count_high + mu_count_low + mu_count_high

