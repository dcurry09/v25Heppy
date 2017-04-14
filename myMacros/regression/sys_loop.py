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

bkg_list = ['WZ', 'ttbar', 'ZZ_2L2Q_ext1', 'ZZ_2L2Q_ext2', 'ZZ_2L2Q_ext3', 'DY_inclusive']

DY_list = ['DY_100to200', 'DY_200to400', 'DY_400to600', 
           'DY_Bjets',
           'DY_1200to2500', 'DY_2500toInf','DY_800to1200_ext1',
           'DY_600to800_ext1', 'DY_600to800_ext2',
           'DY_Bjets_Vpt100to200','DY_Bjets_Vpt200toInf','DY_Bjets_Vpt100to200_ext2', 'DY_Bjets_Vpt200toInf_ext2',
           'DY1J_10to50', 'DY2J_10to50', 'DY3J_10to50'
           ]

#DY_nlo_list = ['DY_Pt50to100', 'DY_Pt100to250', 'DY_Pt250to400', 'DY_Pt400to650', 'DY_Pt650toInf']

ST_list = ['ST_t', 'ST_t_antitop', 'ST_s', 'ST_tW_top', 'ST_tW_antitop']

temp_list = ['ST_s']

#sample_list = temp_list
#sample_list = DY_list + signal_list
#sample_list = data_list
sample_list = signal_list + ST_list + data_list + bkg_list + DY_list

#sample_list1 = signal_list + data_list + ST_list

#sample_list2 = bkg_list + DY_list


def osSystem(sample):

         os.system('./runAll.sh '+sample+' 13TeV sys')

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

    
    
