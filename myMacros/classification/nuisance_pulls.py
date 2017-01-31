#!/usr/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)
from ROOT import TFile
import os
import sys
import re
import fileinput
import subprocess
import numpy as np
import multiprocessing
import logging
from matplotlib import interactive

#inpath = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/limits/temp/'
inpath = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/limits/v24_ICHEP_VH_11_22_noRP/'

outpath = '/afs/cern.ch/user/d/dcurry/www/v24_ICHEP_preSF_11_22/Nuisance_Pulls/'

# Make the dir and copy the website ini files
try:
    os.system('mkdir '+outpath)
except:
     print outpath+' already exists...'
temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outpath
os.system(temp_string2)
os.system(temp_string3)


# Move to in path
os.chdir(inpath)

# Make 3 sets of plots: btag, JEC/JER, All others
sys_list = ['Btag', 'JER', 'Other', 'BinStat']

for sys in sys_list:

    print '\n\t Making Nuisance Pull Plots for ', sys

    temp_sys = sys

    # Turn off all bools
    for sys in sys_list:
        new_bool = "is"+sys+" = False\n"
        for line in fileinput.input('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/python/diffNuisances.py', inplace=True):
            if "is"+sys+" =" in line:
                print line.replace(line, new_bool),
            else: print line,
    # end file modification

    sys = temp_sys

    # Turn on the appropriate bool(isBtag)
    new_bool = "is"+sys+" = True\n"
    for line in fileinput.input('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/python/diffNuisances.py', inplace=True):
        if "is"+sys+" =" in line:
            print line.replace(line, new_bool),
        else: print line,
    # end file modification
        
    os.system('rm outputfile.root')
    #outputFile = sys+"_outputfile.root"
        
    # Make the nuisance pull plot
    t1 = "python /afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/python/diffNuisances.py mlfit.root -g outputfile.root -ptol 0.00001"
    os.system(t1)

    # Then take the outputfile.root and plot the canvas
    file = TFile.Open('outputfile.root', 'read')

    pulls = file.Get('nuisancs')
    uncert = file.Get('post_fit_errs')

    pulls.Print(outpath+"nuisancs_"+sys+".pdf")
    pulls.Print(outpath+"nuisancs_"+sys+".png")
        
    uncert.Print(outpath+'post_fit_errs'+sys+'.png')
    uncert.Print(outpath+'post_fit_errs'+sys+'.pdf')
