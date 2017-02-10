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


# Get the MVAout file
file = TFile('/exports/uftrig01a/dcurry/heppy/v25/ZH125_ext1.root')

tree = file.Get('tree')

# plot cuts

cut = 'Vtype==1 & Jet_btagCMVAV2[hJCMVAV2idx[0]] > -0.716 & Jet_btagCMVAV2[hJCMVAV2idx[1]] > -0.716 & V_mass>75. & V_mass < 105. & V_pt < 2000. & H_pt < 999. & H_pt > 0. & H_mass < 9999. & H_mass > 0. & V_pt > 150.& H_pt < 999. & H_pt > 0. & H_mass < 9999. & H_mass > 0. & V_pt < 2000. & Jet_puId[hJCMVAV2idx[0]] >= 4 & Jet_puId[hJCMVAV2idx[1]] >= 4 & (((Vtype==1) & vLeptons_relIso03[0] < 0.15 & vLeptons_relIso03[1] < 0.15 & vLeptons_pt[0] > 20. & vLeptons_pt[1] > 20.0) || ((Vtype==0) & vLeptons_relIso04[0] < 0.25 & vLeptons_relIso04[1] < 0.25 & vLeptons_pt[0] > 20. & vLeptons_pt[1] > 20.)) & run<=276811 & V_pt > -25.0 & HCMVAV2_reg_mass < 150. & HCMVAV2_reg_mass > 90. & Jet_pt_reg[hJCMVAV2idx[0]] > 20. & Jet_pt_reg[hJCMVAV2idx[1]] > 20.'

single_trigger_cut = 'HLT_BIT_HLT_Ele27_eta2p1_WPLoose_Gsf_v==1'

double_trigger_cut = 'HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v==1'

print '\n-----> BDT plot Cut: ', cut


# Make the plot
#c1    = TCanvas('c1')
#s1 = THStack('s1', '')

#hSingle = TH1F('hSingle', '' , 50, 0, 400)
#hDouble = TH1F('hhDouble', '' , 50, 0, 400)

#tree.Project('hSingle', 'HCSV_mass', cut+' & '+single_trigger_cut)
#tree.Project('hDouble', 'HCSV_mass', cut+' & '+double_trigger_cut)


print 'Single trigger Events:', tree.GetEntries(cut+' & '+single_trigger_cut)

print 'Double trigger Events:', tree.GetEntries(cut+' & '+double_trigger_cut)


raw_input('\n\n\t....press return to continue')
