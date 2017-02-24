# ===================================================
# Python script to perform BDT Classifier loop
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


# ===== Define the regions to be submitted to ./runAll.sh evaluateMVA.py =====

#sample_list = ['ZH125', 'DY_inclusive_lhe', 'DY_100to200_lhe', 'DY_200to400_lhe', 'DY_400to600_lhe', 'DY_600toInf_lhe', \
#               'ttbar', 'gJets_100to200', 'qcd_100to250']

bkg_list = ['DY_inclusive', 'ttbar', 'ZZ_2L2Q', 'WZ']

data_list = ['Zuu', 'Zee']

signal_list =['ZH125', 'ggZH125']

#DY_list = [ 'DY_100to200', 'DY_200to400', 'DY_400to600', 'DY_Bjets', 'DY_BgenFilter',
#            'DY_600to800', 'DY_800to1200', 'DY_1200to2500', 'DY_2500toInf', 'DY_70to100'
##            'DY_Pt50to100', 'DY_Pt100to250', 'DY_Pt250to400','DY_Pt400to650','DY_Pt650toInf'
#            ]

ST_list = ['ST_t', 'ST_t_antitop', 'ST_s', 'ST_tW_top', 'ST_tW_antitop']

DY_list = ['DY0J', 'DY1J', 'DY2J_ext1', 'DY2J_ext2', 'DY2J_ext3', 'DY2J_ext4']

temp_list = ['DY2J_ext1', 'DY2J_ext2', 'DY2J_ext3', 'DY2J_ext4']


sample_list = bkg_list + data_list + signal_list + DY_list + ST_list
#sample_list = data_list
#sample_list = temp_list

# Batch Mode
isBatch = False
isBatch = True

isVerbose = False
isVerbose = True


print '\n======================== Starting BDT Evaluation Loop ================================'
print '=====================================================================================\n'

if not isBatch:

    print '\n------> Running in Sequential Mode...'
    
    for sample in sample_list:
        
        os.system('./runAll.sh '+sample+' 13TeV evalBDT')


if isBatch:

    print '\n------> Running in Batch Mode...'

    # define the os.system function
    def osSystem(sample):

        if isVerbose:
            os.system('./runAll.sh '+sample+' 13TeV evalBDT')
        else:
            os.system('./runAll.sh '+sample+' 13TeV evalBDT > print_dump.txt')

    # define the multiprocessing object
    p = multiprocessing.Pool()
    results = p.imap(osSystem, sample_list)
    p.close()
    p.join()


print '\n\n-----> All Jobs Finished...\n'
