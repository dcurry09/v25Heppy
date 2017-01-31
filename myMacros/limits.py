# ===================================================
# Python script to perform datacard loop over bins/regions
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
import multiprocessing
import logging
from matplotlib import interactive
from ROOT import *

# First make the list of datacards to be used in limit calcualtion
mjj_list = ['vhbb_TH_MJJ_M125_ZuuLowPt_13TeV', 'vhbb_TH_MJJ_M125_ZuuMedPt_13TeV', 'vhbb_TH_MJJ_M125_ZuuMedPt_13TeV', \
            'vhbb_TH_MJJ_M125_ZeeLowPt_13TeV', 'vhbb_TH_MJJ_M125_ZeeMedPt_13TeV', 'vhbb_TH_MJJ_M125_ZeeMedPt_13TeV', \

bdt_list = ['vhbb_DC_TH_BDT_M125_ZuuLowPt_13TeV', 'vhbb_DC_TH_BDT_M125_ZuuMedPt_13TeV', 'vhbb_DC_TH_BDT_M125_ZuuHighPt_13TeV', \
            'vhbb_DC_TH_BDT_M125_ZeeLowPt_13TeV', 'vhbb_DC_TH_BDT_M125_ZeeMedPt_13TeV', 'vhbb_DC_TH_BDT_M125_ZeeHighPt_13TeV']

limit_list = mjj_list + bdt_list
#limit_list = bdt_list

outpath = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/limits/'

# Move old limits to a repository
os.system('mv ../limits/higgs* ../limits/roostats* ../limits/repository/')


print '\n======================== Starting DataCard Loop ================================'
print '=====================================================================================\n'


# define the os.system function
def osSystem(limit):

    os.system('combine -M Asymptotic -m 125 --out '+outpath+' '+outpath+'/vhbb_DC_WS_MJJ_M125_ZeeLowPt_13TeV.txt')


# define the multiprocessing object
p = multiprocessing.Pool()
results = p.imap(osSystem, limit_list)
p.close()
p.join()
