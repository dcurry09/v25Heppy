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

bkg_list = ['DY_inclusive', 'ttbar', 'ZZ_2L2Q_ext1', 'ZZ_2L2Q_ext2', 'ZZ_2L2Q_ext3', 'WZ', 'DY_Bjets']

data_list = ['Zuu', 'Zee']

signal_list =['ZH125', 'ggZH125']

DY_list = [ 
    'DY_100to200', 'DY_200to400', 'DY_400to600',
    'DY_1200to2500', 'DY_2500toInf',
    'DY_800to1200_ext1', 'DY_800to1200_ext2',
    'DY_600to800_ext1', 'DY_600to800_ext2', 'DY_600to800_ext3','DY_600to800_ext4', 'DY_600to800_ext5', 'DY_600to800_ext6',
    'DY_Bjets_Vpt100to200', 'DY_Bjets_Vpt200toInf',
    'DY_Bjets_Vpt100to200_ext2', 'DY_Bjets_Vpt200toInf_ext2',
    #'DY1J_10to50', 'DY2J_10to50', 'DY3J_10to50'
    ]

ST_list = ['ST_t', 'ST_t_antitop', 'ST_s', 'ST_tW_top', 'ST_tW_antitop']


temp_list = ['WZ']

#sample_list = bkg_list + data_list + ST_list+ signal_list + DY_list
#sample_list = data_list
sample_list = temp_list

sample_list1 = ST_list + ['WZ', 'DY_Bjets', 'DY_inclusive'] 

sample_list2 = ['ttbar', 'ZZ_2L2Q_ext1', 'ZZ_2L2Q_ext2', 'ZZ_2L2Q_ext3'] + signal_list + DY_list + data_list

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


    # p = multiprocessing.Pool()
    # results = p.imap(osSystem, sample_list1)
    # p.close()
    # p.join()

    # p = multiprocessing.Pool()
    # results = p.imap(osSystem, sample_list2)
    # p.close()
    # p.join()

print '\n\n-----> All Jobs Finished...\n'
