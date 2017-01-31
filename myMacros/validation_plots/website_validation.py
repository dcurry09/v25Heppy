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
from ROOT import *
import multiprocessing


# Which main directory:
# https://dcurry.web.cern.ch/dcurry/xxxx
main_dir = '80x_validation'

# From where to get the plots
dir = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/myMacros/validation_plots/Zll_validation_plots/80x/'


# Move old datacards to a repository
try:
     os.makedirs('/afs/cern.ch/user/d/dcurry/www/'+main_dir)
     temp_string1 = 'cp /afs/cern.ch/user/d/dcurry/www/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir
     temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir

     # Now make the individual dirs
     #t3 = 'mkdir '

     os.system(temp_string1)
     os.system(temp_string2)

except:
     print main_dir+' already exists...'





print '-----> Copying PLots for: ',dir

temp_string = 'cp -r '+dir+'/* /afs/cern.ch/user/d/dcurry/www/'+main_dir
os.system(temp_string)
