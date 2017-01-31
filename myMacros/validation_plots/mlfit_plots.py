#!/usr/bin/env python

import ROOT
import os
from ROOT import *

ROOT.gROOT.SetBatch(True)

infile = ROOT.TFile.Open('/exports/uftrig01a/dcurry/heppy/files/prep_out/v23_7_18_ZH125.root')
tree = infile.Get("tree")



outpath = '/afs/cern.ch/user/d/dcurry/www/80x_validation/mlfit_plots/'

# Make the dir and copy the website ini files
try:
    os.system('mkdir '+outpath)
except:
     print outpath+' already exists...'

temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outpath

os.system(temp_string2)
os.system(temp_string3)
