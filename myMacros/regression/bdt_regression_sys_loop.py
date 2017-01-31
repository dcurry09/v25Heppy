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
#from ROOT import *
import multiprocessing


data_list = ['Zuu', 'Zee']

signal_list = ['ZH125', 'ggZH125']

bkg_list = ['WZ', 'ttbar', 'ZZ_2L2Q']

DY_list = ['DY_inclusive', 'DY_100to200', 'DY_200to400', 'DY_400to600', 'DY_600toInf', 'DY_Bjets', 'DY_BgenFilter',
           #'DY_inclusive_nlo', 'DY_Pt100to250', 'DY_Pt250to400', 'DY_Pt400to650', 'DY_Pt650toInf'
           ]

ST_list = ['ST_t', 'ST_s', 'ST_tW_top', 'ST_tW_antitop']

temp_list = ['ZH125']

sample_list = temp_list
#sample_list = DY_list + signal_list
#sample_list = data_list
#sample_list = signal_list + data_list + bkg_list + DY_list + ST_list


os.system('rm sys_done.txt')

def osSystem(sample):

         os.system('./runAll.sh '+sample+' 13TeV sys')

# define the multiprocessing object
p = multiprocessing.Pool()
results = p.imap(osSystem, sample_list)
p.close()
p.join()


os.system("ls >> sys_done.txt")
    
    