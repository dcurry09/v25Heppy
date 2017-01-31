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
file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/MVA_out/v12_07_2015_Zll.root')
#file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/MVA_out/v12_07_2015_DY_inclusive.root')

tree = file.Get('tree')


# plot cuts
maxBtag = 'max(Jet_btagCSV[hJCidx[0]],Jet_btagCSV[hJCidx>[1]]) > 0.605'
minBtag = 'min(Jet_btagCSV[hJCidx[0]],Jet_btagCSV[hJCidx[1]]) > 0.3'

zuu_lowPt = maxBtag+ ' & '+minBtag+ ' & V_mass > 75. & V_mass < 105. & V_pt > 50. & V_pt < 100. & H_mass > 40. & H_mass < 250.'

cut = 'Vtype == 0 < 2 & H_pt > 0 & Jet_pt[hJCidx[0]] > 20. & Jet_pt[hJCidx[1]] > 20. & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4'

bdt_cut = zuu_lowPt + ' & '+cut

print '\n-----> BDT plot Cut: ',bdt_cut


# Make the plot
c1    = TCanvas('c1')

s1 = THStack('s1', '')

hbdt = TH1F('hbdt', '' , 15, -1, 1)

tree.Project('hbdt', 'gg_plus_ZH125_Zuu_lowZpt', bdt_cut)

s1.Add(hbdt)

s1.Draw('nostack')




raw_input('\n\n\t....press return to continue')
