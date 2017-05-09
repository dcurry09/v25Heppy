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

#training_list = ['gg_plus_ZH125_lowZpt', 'gg_plus_ZH125_highZpt', 'VV_bdt_lowZpt', 'VV_bdt_highZpt']

#training_list = ['gg_plus_ZH125_semiLepton', 'gg_plus_ZH125_1semiLepton', 'gg_plus_ZH125_NOsemiLepton', 'gg_plus_ZH125_medZpt', 'gg_plus_ZH125_highZpt', 'gg_plus_ZH125_lowZpt', 'gg_plus_ZH125_tightHmass']

training_list = ['gg_plus_ZH125_lowZpt', 'gg_plus_ZH125_highZpt']

#training_list = ['gg_plus_ZH125_highZpt']

#training_list = ['VV_bdt_highZpt']#, 'VV_bdt_highZpt']

#####################################################################



##### for nEvt Opt #####
training_list_trees = ['gg_plus_trees100', 'gg_plus_trees200', 'gg_plus_trees300','gg_plus_trees350','gg_plus_trees400','gg_plus_trees450','gg_plus_trees500','gg_plus_trees550','gg_plus_trees600','gg_plus_trees700','gg_plus_trees800', 'gg_plus_trees900', 'gg_plus_trees1000']

#training_list_trees = ['gg_plus_trees100','gg_plus_trees150']

training_list_nEvt = ['gg_plus_nEvt0.1', 'gg_plus_nEvt0.2', 'gg_plus_nEvt0.3', 'gg_plus_nEvt0.5', 'gg_plus_nEvt1', 'gg_plus_nEvt2', 'gg_plus_nEvt3', 'gg_plus_nEvt4', 'gg_plus_nEvt5', 'gg_plus_nEvt10', 'gg_plus_nEvt15', 'gg_plus_nEvt20']

training_list_depth = ['gg_plus_depth1','gg_plus_depth2','gg_plus_depth3','gg_plus_depth4','gg_plus_depth5']

training_list_cuts = ['gg_plus_nCuts5','gg_plus_nCuts10','gg_plus_nCuts25','gg_plus_nCuts50','gg_plus_nCuts100','gg_plus_nCuts250','gg_plus_nCuts500','gg_plus_nCuts1000']

training_list_LR = ['gg_plus_LR001','gg_plus_LR01','gg_plus_LR011','gg_plus_LR012','gg_plus_LR013','gg_plus_LR014','gg_plus_LR015','gg_plus_LR02','gg_plus_LR03','gg_plus_LR04',
                 'gg_plus_LR05']

optimizer_training_list= training_list_LR
##########################



# If we want to optimize
isOpt = False
#isOpt = True    



print '\n======================== Starting BDT Training Loop ================================'
print '=====================================================================================\n'




# define the os.system function
if isOpt:
    
    for bdt in optimizer_training_list:
        os.system('./runAll.sh '+ bdt +' 13TeV trainBDT')



# if not batch mode:
if not isOpt:

    for bdt in training_list:

        os.system('./runAll.sh '+ bdt +' 13TeV trainBDT')

        
        
print '\n\n-----> All Jobs Finished...\n'
