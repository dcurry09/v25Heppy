# ===================================================
# Python script to perform CMSSW Higgs combination Tools
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


# Datacard to be evaluated
datacard_list = ['../limits/vhbb_DC_WS_BDT_M125_Zuu_HighPt_13TeV.txt']

# Which combination tools to run
#tool_list = ['CLs_limits', 'exp_significance', 'obs_significance']
tool_list = ['exp_significance']
#tool_list = ['CLs_limits']

for datacard in datacard_list:

    for tool in tool_list:

        if tool is 'CLs_limits':
        
            print '\n-----> Running CLs Limit Calculation on datacard: ', datacard
            
            os.system('combine -M Asymptotic '+datacard)


        if tool is 'exp_significance':
            
            print '\n-----> Running Expected Likelihood Significance Calculation on datacard: ', datacard
            
            os.system('combine -d '+datacard+' -M ProfileLikelihood -v 1 --significance --expectSignal=1 -t -1 -m 125 -n Expected')
            

        if tool is 'obs_significance':

            print '\n-----> Running Observed Likelihood Significance Calculation on datacard: ', datacard

            os.system('combine -M ProfileLikelihood --signif '+ datacard)


