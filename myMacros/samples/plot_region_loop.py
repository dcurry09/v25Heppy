# ===================================================
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
#import ROOT
import multiprocessing
#ROOT.gROOT.SetBatch(True)

# ===== Define the regions to be submitted to ./runAll.sh and plots made =====

isSplit = False
#isSplit = True

# control regions

#control_list = ['Zlf_Zee', 'Zhf_Zee','ttbar_Zee',
#                'Zlf_Zuu', 'Zhf_Zuu', 'ttbar_Zuu']


control_list = ['Zlf_low_Zee', 'Zhf_low_Zee','ttbar_low_Zee',
                'Zlf_high_Zuu', 'Zhf_high_Zuu', 'ttbar_high_Zuu',
                'Zlf_low_Zuu', 'Zhf_low_Zuu','ttbar_low_Zuu',
                'Zlf_high_Zee', 'Zhf_high_Zee', 'ttbar_high_Zee']


zhf_list = ['Zhf_low_Zee', 'Zhf_high_Zuu', 'Zhf_low_Zuu', 'Zhf_high_Zee']

zlf_list = ['Zlf_low_Zee', 'Zlf_high_Zuu', 'Zlf_low_Zuu', 'Zlf_high_Zee']

zlf_mu_list = ['Zlf_high_Zuu', 'Zlf_low_Zuu']

zlf_ele_list = ['Zlf_low_Zee', 'Zlf_high_Zee']

ttbar_list = ['ttbar_low_Zee', 'ttbar_high_Zuu', 'ttbar_low_Zuu', 'ttbar_high_Zee']


log_control_list = ['Zlf_Zuu_log', 'Zlf_Zee_log', 'Zhf_Zee_log', 'Zhf_Zuu_log', 'ttbar_Zuu_log', 'ttbar_Zee_log']

pt_log_control_list = ['Zlf_Zuu_log_lowPt', 'Zlf_Zuu_log_medPt', 'Zlf_Zuu_log_highPt',\
                       'Zlf_Zee_log_lowPt', 'Zlf_Zee_log_medPt', 'Zlf_Zee_log_highPt',\
                       'Zhf_Zee_log_lowPt', 'Zhf_Zee_log_medPt', 'Zhf_Zee_log_highPt',\
                       'Zhf_Zuu_log_lowPt', 'Zhf_Zuu_log_medPt', 'Zhf_Zuu_log_highPt', \
                       'ttbar_Zee_log_lowPt', 'ttbar_Zee_log_medPt', 'ttbar_Zee_log_highPt', \
                       'ttbar_Zuu_log_lowPt', 'ttbar_Zuu_log_medPt', 'ttbar_Zuu_log_highPt'
                       ]

# BDT Regions
# signal regions for Z_pt cuts  
signal_list = [
     #'bdt_Zuu_low_Zpt', 'bdt_Zee_low_Zpt',
     'bdt_Zuu_high_Zpt', 'bdt_Zee_high_Zpt'
     
     #'bdt_Zee_high_Zpt_TightBDTcut', 'bdt_Zuu_high_Zpt_TightBDTcut'
               
     #'VV_bdt_Zee_low', 'VV_bdt_Zee_high',
     #'VV_bdt_Zuu_low', 'VV_bdt_Zuu_high'
     ]

vv_signal_list = ['VV_bdt_Zee_low', 'VV_bdt_Zee_high',
                  'VV_bdt_Zuu_low', 'VV_bdt_Zuu_high']


mjj_list = ['mjj_Zee_low_Zpt', 'mjj_Zee_med_Zpt', 'mjj_Zee_high_Zpt',
            'mjj_Zuu_low_Zpt', 'mjj_Zuu_med_Zpt', 'mjj_Zuu_high_Zpt']

# Jet Regression Regions
#reg_list = ['jet_regression_Zhf']

#temp_list = ['bdt_Zee', 'bdt_Zuu']
#temp_list = mjj_list
temp_list = ['Zhf_high_Zuu']


##### choose which lists to loop over ####

region_list = temp_list
#region_list = vv_signal_list
#region_list = reg_list
#region_list = control_list
#region_list = signal_list
#region_list = control_list + signal_list


# ============================================================================



print '\n======================== Starting Plot Region Loop ================================'
print '=====================================================================================\n'

# clean all plots
os.system('rm -r ../plots/*')

os.system('rm sb_results.txt')
os.system('rm bkg_results.txt')

# init any complied macros
#ROOT.gSystem.CompileMacro("/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/plugins/PU.C")


def osSystem(region):
     os.system('./runAll.sh '+region+' 13TeV plot')
     
if not isSplit:
     p = multiprocessing.Pool()
     results = p.imap(osSystem, region_list)
     p.close()
     p.join()


if isSplit:
     
     p1 = multiprocessing.Pool()
     results = p1.imap(osSystem, ttbar_list)
     p1.close()
     p1.join()
     
     p2 = multiprocessing.Pool()
     results = p2.imap(osSystem, zhf_list)
     p2.close()
     p2.join()

     p3 = multiprocessing.Pool()     
     results = p3.imap(osSystem, zlf_list)
     p3.close()
     p3.join()
     
     #p3 = multiprocessing.Pool()
     #results = p3.imap(osSystem, zhf_list+zlf_list)
     #p3.close()
     #p3.join()
     
     # p3 = multiprocessing.Pool()
     # results = p3.imap(osSystem, zlf_ele_list)
     # p3.close()
     # p3.join()

     #p4 = multiprocessing.Pool()
     #results = p4.imap(osSystem, signal_list)
     #p4.close()
     #p4.join()


# If desired move newly created plots to their own directory
#os.system('cp -r /afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/plots/basic_out/ /afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/plots/v13_10_20')

# Also move the S/B metric file to a new labeled one
#os.system('cp -r /afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/python/sb_results.txt /afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/python/count_results/sb_results_v12_post_opt.txt')

#os.system('cp -r /afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/python/bkg_results.txt /afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/python/bkg_results_v12_pre_opt.txt')
          



