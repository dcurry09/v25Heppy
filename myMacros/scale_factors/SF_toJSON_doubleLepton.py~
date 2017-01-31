# ===================================================
# Python script to transofrm root file of SFs to JSON
#
# 2/15/2016 David Curry
# ===================================================

import sys
import os
import re
import fileinput
import subprocess
import numpy as np
from matplotlib import interactive
from ROOT import *


input_root_file = TFile.Open('doubleLepton/triggerSummary_ee.root')
text_file = open("ScaleFactor_doubleElectron76x.txt", "w")

#input_root_file = TFile.Open('doubleLepton/triggerSummary_uu.root')
#text_file = open("ScaleFactor_doubleMuon76x.txt", "w")

# ======== If you first have to divide to TH2F =========

#input_mc   = TFile.Open('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_6_3_patch2/src/PhysicsTools/TagAndProbe/test/efficiency-mc-passingLoose-test.root')   
#input_data = TFile.Open('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_6_3_patch2/src/PhysicsTools/TagAndProbe/test/efficiency-data-passingLoose-test.root')

#input_mc   = TFile.Open('efficiency-mc-passingLoose-test.root')
#input_data = TFile.Open('efficiency-data-passingLoose-test.root')

#hist_mc   = input_mc.Get('GsfElectronToRECO/MCtruth_passingLoose/fit_eff_plots/probe_Ele_pt_probe_Ele_eta_PLOT_mcTrue_true')
#hist_data = input_data.Get('GsfElectronToRECO/passingLoose/fit_eff_plots/probe_Ele_pt_probe_Ele_eta_PLOT')

#mc   = hist_mc.GetPrimitive('probe_Ele_pt_probe_Ele_eta_PLOT_mcTrue_true')
#data = hist_data.GetPrimitive('probe_Ele_pt_probe_Ele_eta_PLOT')
 
#data.Divide(mc)
#eSF = data


# ===== If root file is a 2D histogram of scale factors do the following =======

eSF = input_root_file.Get('scalefactor_eta2d_with_syst')


# loop over eta(x-axis) bins
for iEta in range(1,eSF.GetNbinsX()+1):
    
    print '\nEta bin:', iEta 
    print 'Bin Low Edge :', eSF.GetXaxis().GetBinLowEdge(iEta)
    print 'Bin High Edge:', eSF.GetXaxis().GetBinUpEdge(iEta)
    
    etal = eSF.GetXaxis().GetBinLowEdge(iEta)
    etah = eSF.GetXaxis().GetBinUpEdge(iEta)
    
    # Loop over pT(y-axis) bins
    for ipt in range(1, eSF.GetNbinsY()+1):
        
        print '\nPt bin:', ipt
        print 'Bin Low Edge :', eSF.GetYaxis().GetBinLowEdge(ipt)
        print 'Bin High Edge:', eSF.GetYaxis().GetBinUpEdge(ipt)
        
        ptl = eSF.GetYaxis().GetBinLowEdge(ipt)
        pth = eSF.GetYaxis().GetBinUpEdge(ipt)

        # Get the SF for this 2D bin
    
        #sf = round(eSF.GetBinContent(ipt, iEta), 3)
        #err = round(eSF.GetBinError(ipt, iEta), 3)
         
        sf  = round(eSF.GetBinContent(iEta, ipt), 3)
        err = round(eSF.GetBinError(iEta, ipt), 3)

        print 'SF:', sf
        print 'SF Uncert:',  err

        # export to text file as columns: eta low, eta high, pt low, pt high, SF, SF uncert
        text_file.write('%s %s %s %s %s %s\n' % (etal, etah, ptl, pth, sf, err) )
        #text_file.write('%s %s %s %s %s %s\n' % (ptl, pth, etal, etah, sf, err) )



text_file.close()
