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
from bTagSF import *

# sample prefix
prefix = 'v24_9_15_'

inpath = '/exports/uftrig01a/dcurry/heppy/files/sys_out/'
outpath = '/exports/uftrig01a/dcurry/heppy/files/temp_sys/'

# List of files to add btag weights to
bkg_list = ['DY_inclusive', 'ttbar', 'ZZ_2L2Q', 'WZ']

data_list = ['Zuu', 'Zee']

signal_list =['ZH125', 'ggZH125']

DY_list = ['DY_100to200', 'DY_200to400', 'DY_400to600', 'DY_600toInf', 'DY_Bjets', 'DY_BgenFilter']
           #'DY_5to50_inclusive', 'DY_5to50_100to200', 'DY_5to50_200to400', 'DY_5to50_400to600', 'DY_5to50_600toInf']

ST_list = ['ST_t', 'ST_s', 'ST_tW_top', 'ST_tW_antitop']


file_list = bkg_list + data_list + signal_list + DY_list + ST_list

for file in file_list:

    infile  = inpath+prefix+file
    outfile = outpath+prefix+file


    print '\n Adding btag weights to sample:', infile
    print '\n Output File                  :', outfile

    s = 'python bTagSF.py'+infile+' '+outfile 

    print s

    os.system(s)


