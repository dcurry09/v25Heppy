# ===================================================
# Python script to perform file prep loop
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
import multiprocessing

# ===== Define the samples to be submitted to ./runAll.sh =====

data_list = ['Zuu', 'Zee']

signal_list = ['ZH125', 'ggZH125']

bkg_list = ['WZ', 'ttbar', 'ZZ_2L2Q_ext1', 'ZZ_2L2Q_ext2', 'ZZ_2L2Q_ext3']


DY_list = [
    'DY_inclusive', 
    'DY_100to200', 'DY_200to400', 'DY_400to600',
    #'DY_Bjets',
    'DY_800to1200_ext1', 
    'DY_600to800_ext1', 'DY_600to800_ext2',
    'DY_Bjets_Vpt100to200_ext2', 'DY_Bjets_Vpt200toInf_ext2',
    #'DY_1200to2500', 'DY_2500toInf',
    'DY1J_10to50', 'DY2J_10to50', 'DY3J_10to50'
    ]

ST_list = ['ST_t', 'ST_t_antitop', 'ST_s', 'ST_tW_top', 'ST_tW_antitop']

temp_list = ['DY_600to800_ext1', 'DY_600to800_ext2', 'DY_600to800_ext3', 'DY_600to800_ext4', 'DY_600to800_ext5', 'DY_600to800_ext6']


# final list
#sample_list = DY_list
#sample_list = signal_list
#sample_list = bkg_list
sample_list = temp_list
#sample_list = data_list
#sample_list = signal_list + bkg_list + DY_list + ST_list + data_list



print '\n======================== Starting Prep Loop ================================'
print '===================================================================================\n'

# define the os.system function
def osSystem(sample):

    os.system('./runAll.sh '+sample+' 13TeV prep')


# define the multiprocessing object
p = multiprocessing.Pool()
results = p.imap(osSystem, sample_list)
p.close()
p.join()



