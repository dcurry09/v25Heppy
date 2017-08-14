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

datacard_dir = 'ZllZbb_Datacards_Minus08to1_JECfix_7_3'

inpath = '/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+datacard_dir+'/'

outpath = '/afs/cern.ch/user/d/dcurry/www/NuisancePulls_'+datacard_dir+'_v1/'

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

# Make 2 Nuisance tests: BKG Only and SIG+BKG fpr asimov and unblinded data fits
#pull_list = ['SigPlusBKG_asimov']#, 'SigPlusBKG_data']
pull_list = ['SigPlusBKG_data']

print '\n\tMaking Pulls for DC: ', datacard_dir

for pull in pull_list:

    print '\n\t Making Nuisance Pulls for ', pull

    if pull == 'BKG_asimov':
        os.system('combine -M MaxLikelihoodFit -m 125 -t -1 --expectSignal=0 vhbb_Zll.txt')
                
    if pull == 'SigPlusBKG_asimov':
        os.system('combine -M MaxLikelihoodFit -m 125 -t -1 --expectSignal=1 vhbb_Zll.txt')

    if pull == 'BKG_data':
        os.system('combine -M MaxLikelihoodFit -m 125 --expectSignal=0 --minimizerAlgo=Minuit vhbb_Zll.txt')

    if pull == 'SigPlusBKG_data':
        os.system('combine -M MaxLikelihoodFit -m 125 -v 3 --expectSignal=1 --minimizerAlgo=Minuit vhbb_Zll.txt')
        
        #os.system('combine -M MaxLikelihoodFit -v 3 -m 125 --rMin=-5 --rMax=5 --stepSize=0.05 --expectSignal=1 --robustFit=1 --saveNorm --saveShapes --saveWithUncertainties --minimizerTolerance=10.0 --minimizerAlgoForMinos Minuit2,Migrad vhbb_Zll.txt')

        
    os.system('rm '+outpath+'/Zll_'+pull+'_pulls.txt')
    
    os.system('rm ../../python/mlfit.root')
    
    os.system('cp ../../python/diffNuisances.py .')
    
    os.system('python diffNuisances.py -a '+inpath+'/mlfit.root  >> '+outpath+'/Zll_'+pull+'_pulls.txt')
