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

bkg_list = ['WZ', 'ttbar', 'ZZ_2L2Q']
#bkg_list = ['ZZ', 'WZ', 'ZZ_2L2Q']


DY_list = [ 'DY_inclusive', 'DY_100to200', 'DY_200to400', 'DY_400to600', 'DY_600toInf', 'DY_Bjets', 'DY_BgenFilter',
            #'DY_inclusive_nlo', 'DY_Pt100to250', 'DY_Pt250to400', 'DY_Pt400to650', 'DY_Pt650toInf'
            ]
            

ST_list = ['ST_t', 'ST_s', 'ST_tW_top', 'ST_tW_antitop']

temp_list = ['ttbar']

#gJets_list = ['gJets_100to200']
#, 'gJets_200to400', 'gJets_400to600', 'gJets_600toInf']

#qcd_list = ['qcd_100to250']
#, 'qcd_250to500', 'qcd_500to1000', 'qcd_1000toInf']

#DY_list = ['DY_inclusive_lhe', 'DY_100to200_lhe', 'DY_200to400_lhe', 'DY_400to600_lhe', 'DY_600toInf_lhe']

#DY_list = ['DY_inclusive']

# final list
#sample_list = data_list
#sample_list = signal_list + DY_list
#sample_list = bkg_list
#sample_list = DY_list
sample_list = temp_list
#sample_list = data_list
#sample_list = signal_list + bkg_list + DY_list + ST_list



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



