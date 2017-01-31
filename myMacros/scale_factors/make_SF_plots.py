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


# ==== Get the MC/Data TH2F =====
input_mc   = TFile.Open('efficiency-mc-passingLoose-test.root')
input_data = TFile.Open('efficiency-data-passingLoose-test.root')

#input_mc   = TFile.Open('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_6_3_patch2/src/PhysicsTools/TagAndProbe/test/efficiency-mc-passingLoose-test.root')
#input_data = TFile.Open('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_6_3_patch2/src/PhysicsTools/TagAndProbe/test/efficiency-data-passingLoose-test.root')

hist_mc   = input_mc.Get('GsfElectronToRECO/MCtruth_passingLoose/fit_eff_plots/probe_Ele_pt_probe_Ele_eta_PLOT_mcTrue_true')
hist_data = input_data.Get('GsfElectronToRECO/passingLoose/fit_eff_plots/probe_Ele_pt_probe_Ele_eta_PLOT')

mc   = hist_mc.GetPrimitive('probe_Ele_pt_probe_Ele_eta_PLOT_mcTrue_true')
data = hist_data.GetPrimitive('probe_Ele_pt_probe_Ele_eta_PLOT')



# ==== Hisotgrams =====
#eta_bins = [-2.5, -1.556, -0.8, 0.0, 0.8, 1.556, 2.5]

#pt_bins = [20, 25., 35., 45., 55., 200.]

#heta_mc   = TH1F('heta_mc', '', len(eta_bins)-1, eta_bins)
#heta_data = TH1F('heta_data', '', len(eta_bins)-1, eta_bins)

# ==== Make a 1D pt plot =====

#cpt = TCanvas('cpt')
#cpt.cd()
#pt_prof = mc.Profile()
#pt_prof.Draw()




# Make a 2d ratio plot
c = TCanvas('c1')

data.Divide(mc)
eSF = data
c.cd()
eSF.Draw()

    
    
raw_input('...press enter to continue...')    

