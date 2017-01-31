# ===================================================
# 
# Code to wrap all of analysis steps in one place
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


# ====== Which Analysis Steps to Run? =======

# moves files onto UFtrig
file_mover = False
#file_mover = True

# merge DY samples
addingSamples = False
#addingSamples = True

# send files to heppy prep code
prep_loop = False
#prep_loop = True

# plots many regions at once
plot_region_loop = False
#plot_region_loop = True

# for S/B regression optimization
optimize_region = False
#optimize_region = True

# for BDT jet regression
regression = False
regression = True

# for BDT Classifier S/B
classifier = False
classifier = True

# ============================================

if regression:

    print '\n============= Performing Jet Energy Regression =============\n'
         
         # systematics
         os.system('python ../myMacros/regression/bdt_regression_sys_loop.py')
         
         


if classifier:

     print '\n============= Performing S/B BDT Classification =============\n'
     
     # Train the BDTs
     #os.system('python ../myMacros/bdt_classifier_training_loop.py')
     
     # Apply BDT weights to all samples
     os.system('python ../myMacros/classification/bdt_classifier_eval_loop.py')

     # make the datacards
     #os.system('python ../myMacros/dataCard_loop.py')
     

    

if file_mover:

    print '\n============= Moving Files Onto UFTrig =============\n'

    os.system('python /afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/VHbb/myMacros/file_mover.py')


if addingSamples:
    
    print '\n============= Adding LHE Weights to DY Samples =============\n'
     
    os.system('python /afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/VHbb/python/addingSamples.py --config 13TeVconfig/lheWeights ')
    

if prep_loop:
    
    print '\n============= Preparing Samples for Heppy Code =============\n'
    
    os.system('python /afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/VHbb/myMacros/prep_loop.py')
    

    
