# ===================================================
# Python script to perform BDT Classifier training loop
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
import logging
import multiprocessing


# ===== Define the regions to be submitted to ./runAll.sh train.py =====

training_list = ['gg_plus_ZH125_lowZpt', 'gg_plus_ZH125_highZpt', 'VV_bdt_lowZpt', 'VV_bdt_highZpt']

#training_list = ['gg_plus_ZH125_semiLepton', 'gg_plus_ZH125_1semiLepton', 'gg_plus_ZH125_NOsemiLepton', 'gg_plus_ZH125_medZpt', 'gg_plus_ZH125_highZpt', 'gg_plus_ZH125_lowZpt', 'gg_plus_ZH125_tightHmass']

#training_list = ['gg_plus_ZH125_lowZpt', 'gg_plus_ZH125_highZpt']

# for tree Opt
training_list_trees = ['gg_plus_trees100','gg_plus_trees150','gg_plus_trees200','gg_plus_trees250','gg_plus_trees300','gg_plus_trees350','gg_plus_trees400','gg_plus_trees450','gg_plus_trees500','gg_plus_trees550','gg_plus_trees600','gg_plus_trees700','gg_plus_trees800', 'gg_plus_trees1000']


# for nEvt Opt
training_list_nEvt = ['gg_plus_nEvt0.1', 'gg_plus_nEvt0.5', 'gg_plus_nEvt1', 'gg_plus_nEvt2', 'gg_plus_nEvt3', 'gg_plus_nEvt4', 'gg_plus_nEvt5', 'gg_plus_nEvt10', 'gg_plus_nEvt15', 'gg_plus_nEvt20']

train_list_depth = ['gg_plus_depth1','gg_plus_depth2','gg_plus_depth3','gg_plus_depth4','gg_plus_depth5']

train_list_cuts = ['gg_plus_nCuts5','gg_plus_nCuts10','gg_plus_nCuts25','gg_plus_nCuts50','gg_plus_nCuts100','gg_plus_nCuts250','gg_plus_nCuts500','gg_plus_nCuts1000']

#training_list = training_list_trees + training_list_nEvt + train_list_depth + train_list_cuts

#training_list = ['gg_plus_ZH125_highZpt']


# for non batch.  Must be done if making cuts fir first time. Errors occur when opening same file at same time
isbatch = False
#isbatch = True    

# for quiet running
isVerbose = False
isVerbose = True




print '\n======================== Starting BDT Training Loop ================================'
print '=====================================================================================\n'




# define the os.system function
if isbatch:

    print '\n------> Running in Batch Mode...'

    def osSystem(train):

        if isVerbose:
            os.system('./runAll.sh '+train+' 13TeV trainBDT')
        else:
            os.system('./runAll.sh '+train+' 13TeV trainBDT > print_dump.txt')
        
    # define the multiprocessing object
    p = multiprocessing.Pool()
    results = p.imap(osSystem, training_list)
    p.close()
    p.join()


# if not batch mode:
if not isbatch:

    for bdt in training_list:

        os.system('./runAll.sh '+ bdt +' 13TeV trainBDT')

        
        
print '\n\n-----> All Jobs Finished...\n'
