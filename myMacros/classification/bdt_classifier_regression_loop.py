# ===================================================
# Python script to perform BDT regression loop
#
#  !!!! Needs to be ran from python directory
#
# 2/15/2015 David Curry
# ===================================================

import sys
import os
import re
import fileinput
import subprocess
import numpy as np
from matplotlib import interactive
from ROOT import *


# Define regression types
regr_list = ['noReg', 'wReg']


# Define full training line
wReg_list = 'Nominal: HCSV_reg_mass HCSV_reg_pt HVdPhi HCSV_dEta HCSV_dR met_pt hJet_btagCSV[0] hJet_btagCSV[1] max(Jet_pt[0],hJet_pt[1]) min(hJet_pt[0],hJet_pt[1]) V_mass Sum$(Jet_pt>20.&abs(Jet_eta)<2.4&Jet_puId>0.) deltaR_jj V_pt (HCSV_reg_pt/V_pt) \n'

noReg_list = 'Nominal: HCSV_mass HCSV_pt HVdPhi HCSV_dEta HCSV_dR met_pt Jet_btagCSV[hJCidx[0]] Jet_btagCSV[hJCidx[1]] max(Jet_pt[hJCidx[0]],Jet_pt[hJCidx[1]]) min(Jet_pt[hJCidx[0]],Jet_pt[hJCidx[1]]) V_mass Sum$(Jet_pt>20.&abs(Jet_eta)<2.4&Jet_puId>0.) deltaR_jj V_pt (HCSV_pt/V_pt) \n'


for type in regr_list:

    # new BDT option string.  Remove current feature from training list
    if type == 'noReg':
        new_line = noReg_list

    if type == 'wReg':
        new_line = wReg_list

    print '----> New Training List: ', new_line

    for line in fileinput.input("13TeVconfig/training", inplace=True):

        if 'Nominal:' in line:

            print line.replace(line, new_line),

        else: print line,
    # end file modification

    # Now train the BDT on new option list/ modified file
    os.system('python ../myMacros/classification/bdt_classifier_training_loop.py')

    # Copy the MVA outfile for each iteration for plots later
    tfile = 'cp ../data/MVA_gg_plus_ZH125_highZpt.root ../data/regr_optimization/MVA_gg_plus_ZH125_highZpt_'+type+'.root'

    # Apply the BDT weights to samples
    os.system('python ../myMacros/classification/bdt_classifier_eval_loop.py')

    # Make the datacards for new training
    # Set datacard output directory to current var name
    new_dir = "dir = '3_3_regr_v1"+type+"'\n"
    for line in fileinput.input('../myMacros/classification/dataCard_loop.py', inplace=True):

        if 'dir =' in line:

            print line.replace(line, new_dir),

        else: print line,
    # end file modification

    os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')

    os.system('python ../myMacros/classification/dataCard_loop.py')


