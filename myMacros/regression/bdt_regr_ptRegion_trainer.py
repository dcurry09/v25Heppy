# ===================================================
# Python script to perform BDT regression loop
# Tests performance as a function of several parmeters
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


# Define pt regions to train individually
pt_list = ['20_40', '40_60', '60_80', '80_100', '100_Inf']


print '\n======================== Starting BDT Jet Regression Split in Pt Regions ======================='
print '==================================================================================================\n'


# Init the files
os.system('cp myutils/RegressionTrainer_twoJets.py myutils/RegressionTrainer.py')

# the regression config file
os.system('cp 13TeVconfig/regression_twoJets 13TeVconfig/regression')

# systematics
os.system('cp write_regression_systematics_twoJets_ptRegion.py write_regression_systematics.py')



# loop over parmater list
for param in pt_list:

    break
    
    print '\n\n======================== Starting New Pt Region   ========================'
    print '=============================================================================='
    print '----> Looping over parameter: ', param

    # new BDT option string
    new_name = 'name: v12_train_Zll_trees800_twoJet_ptRegions_'+param+'\n'

    print '----> Weight Name: ', new_name

    basic_cut = 'abs(Jet_eta[hJidx[0]]) < 2.4 & abs(Jet_eta[hJidx[1]]) < 2.4 & Jet_mcPt[hJidx[0]] > 0. & Jet_mcPt[hJidx[1]] > 0.'

    if param is '20_40':
        new_cut = 'cut: '+basic_cut+' & Jet_pt[hJidx[0]] > 20 & Jet_pt[hJidx[1]] > 20 & Jet_pt[hJidx[0]] < 40 & Jet_pt[hJidx[1]] < 40\n'

    if param is '40_60':
        new_cut = 'cut: '+basic_cut+' & Jet_pt[hJidx[0]] > 40 & Jet_pt[hJidx[1]] >40 & Jet_pt[hJidx[0]] < 60 & Jet_pt[hJidx[1]] < 60\n'
            
    if param is '60_80':
        new_cut = 'cut: '+basic_cut+' & Jet_pt[hJidx[0]] > 60 & Jet_pt[hJidx[1]] >60 & Jet_pt[hJidx[0]] < 80 & Jet_pt[hJidx[1]] < 80\n'
        
    if param is '80_100':
        new_cut = 'cut: '+basic_cut+' & Jet_pt[hJidx[0]] > 80 & Jet_pt[hJidx[1]] > 80 & Jet_pt[hJidx[0]] < 100 & Jet_pt[hJidx[1]] < 100\n'

    if param is '100_Inf':
        new_cut = 'cut: '+basic_cut+' & Jet_pt[hJidx[0]] > 100 & Jet_pt[hJidx[1]] > 100\n' 


    
    for line in fileinput.input("13TeVconfig/regression", inplace=True):
        
        if 'name:' in line:
            
            print line.replace(line, new_name),
            
        else: print line,
    # end file modification

    
    for line in fileinput.input("13TeVconfig/regression", inplace=True):
        
        if 'cut:' in line:

            print line.replace(line, new_cut),
             
        else: print line,
    # end file modification

          
    # Train jet regression
    os.system('./runAll.sh ZH125 13TeV trainReg')

# end region loop


# the regression config file
os.system('cp 13TeVconfig/regression_twoJets 13TeVconfig/regression')
     
# apply weights to new sample
os.system('./runAll.sh ZH125 13TeV sys')

#plot the results
os.system('python ../myMacros/simple_regression_HistMaker.py')


