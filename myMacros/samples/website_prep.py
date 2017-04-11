
import sys
import os
import re
import fileinput
import subprocess
import numpy as np
from matplotlib import interactive
#from ROOT import *
import multiprocessing


# Which main directory:
# https://dcurry.web.cern.ch/dcurry/xxxx
#main_dir  = 'TEST4'
main_dir = 'v25_CR_LO_WithBjets2_4_9'



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

# control regions
control_list = ['Zlf_high_Zuu', 'Zhf_high_Zuu', 'ttbar_high_Zuu',
                'Zlf_low_Zuu', 'Zhf_low_Zuu','ttbar_low_Zuu',
                'Zlf_high_Zee', 'Zhf_high_Zee', 'ttbar_high_Zee',
                'Zlf_low_Zee', 'Zhf_low_Zee','ttbar_low_Zee',
                'Zlf_high', 'Zhf_high', 'ttbar_high',
                'Zlf_low', 'Zhf_low', 'ttbar_low',
                'Zlf_Zee'
                ]

regr_list = ['jet_regression_Zhf']

bdt_list = ['bdt_Zuu_low_Zpt','bdt_Zuu_high_Zpt',
            'bdt_Zee_low_Zpt','bdt_Zee_high_Zpt',
            'VV_bdt_Zee_low', 'VV_bdt_Zee_high',
            'VV_bdt_Zuu_low', 'VV_bdt_Zuu_high'
            ]

temp_list = []


#region_list = bdt_list
region_list = control_list
#region_list = regr_list
#region_list = temp_list




# ======= copy over datacards ========

datacard_dir_list = [
     '/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/4_22_2fb',
     '/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/4_22_5fb',
     '/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/4_22_10fb',
     '/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/4_22_20fb'
     ]

datacard_list = ['vhbb_DC_TH_BDT_M125_Zee_LowPt.txt', 'vhbb_DC_TH_BDT_M125_Zee_HighPt.txt']

datacard_list =[]

for datacard_dir in datacard_dir_list:

     for card in datacard_list:

          print '-----> Copying Datacards: ',card
     
          t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/datacards/'+card

          temp_string = 'cp -r '+datacard_dir+'/'+card+' /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/datacards/'

          # Now the workspace
          if 'Zee_LowPt' in card:
               t2 = 'cp -r '+datacard_dir+'/*TH_BDT_M125_Zee_LowPt.root /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/datacards/'
          if 'Zee_HighPt' in card:     
               t2 = 'cp -r /'+datacard_dir+'/*TH_BDT_M125_Zee_HighPt.root /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/datacards/'
          
          os.system(t1)

          os.system(t2)

          os.system(temp_string)



# copy over directories to my cern website area
for dir in region_list:

    print '-----> Copying PLots for: ',dir


    if 'Zlf_low_Zuu' in dir:
         t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_low_Zuu/'
         temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_low_Zuu/'
         temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_low_Zuu/'+dir
         temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_low_Zuu/'+dir
         temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
         temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        
        
    if 'Zlf_low_Zee' in dir:
        t1 = 'rm -rf /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_low_Zee/'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_low_Zee'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_low_Zee/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_low_Zee/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    if 'Zhf_low_Zuu' in dir:
        t1 = 'rm -rf /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_low_Zuu/'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_low_Zuu'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_low_Zuu/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_low_Zuu/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir


    if 'Zhf_low_Zee' in dir:
        t1 = 'rm -rf /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_low_Zee/'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_low_Zee'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_low_Zee/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_low_Zee/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    if 'ttbar_low_Zuu' in dir:
        t1 = 'rm -rf /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_low_Zuu/'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_low_Zuu'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_low_Zuu/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_low_Zuu/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    if 'ttbar_low_Zee' in dir:
        t1 = 'rm -rf /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_low_Zee'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_low_Zee'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_low_Zee/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_low_Zee/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    # High vpt region

    if 'Zlf_high_Zuu' in dir:
         t1 = 'rm -rf /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_high_Zuu/'
         temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_high_Zuu/'
         temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_high_Zuu/'+dir
         temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_high_Zuu/'+dir
         temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
         temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        
        
    if 'Zlf_high_Zee' in dir:
        t1 = 'rm -rf /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_high_Zee/'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_high_Zee'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_high_Zee/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_high_Zee/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    if 'Zhf_high_Zuu' in dir:
        t1 = 'rm -rf /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_high_Zuu/'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_high_Zuu'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_high_Zuu/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_high_Zuu/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir


    if 'Zhf_high_Zee' in dir:
        t1 = 'rm -rf /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_high_Zee/'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_high_Zee'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_high_Zee/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_high_Zee/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    if 'ttbar_high_Zuu' in dir:
        t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_high_Zuu/'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_high_Zuu'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_high_Zuu/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_high_Zuu/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    if 'ttbar_high_Zee' in dir:
        t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_high_Zee'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_high_Zee'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_high_Zee/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_high_Zee/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir




    if 'ttbar_high' == dir:
        t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_high'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_high'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_high/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_high/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir


    if 'Zlf_high' == dir:
        t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_high'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_high'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_high/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_high/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    if 'Zhf_high' == dir:
         t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_high'
         temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_high'
         temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_high/'+dir
         temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_high/'+dir
         temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
         temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    if 'ttbar_low' == dir:
        t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_low'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_low'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_low/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_low/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir


    if 'Zlf_low' == dir:
        t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_low'
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_low'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_low/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_low/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    if 'Zhf_low' == dir:
         t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_low'
         temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_low'
         temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_low/'+dir
         temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_low/'+dir
         temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
         temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    if 'Zlf_Zee' == dir:
         t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_Zee'
         temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_Zee'
         temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_Zee/'+dir
         temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_Zee/'+dir
         temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
         temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir


    if 'signal_all_Zpt' == dir:
         t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/signal_all_Zpt'
         temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/signal_all_Zpt'
         temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/signal_all_Zpt/'+dir
         temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/signal_all_Zpt/'+dir
         temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
         temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir



    if 'jet_regression' in dir:    
        t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    if 'bdt' in dir:
        t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir+'/'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    if 'bdt_tightHmass' in dir:
        t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir+'/'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir

    



    if 'regression' in dir:
        t1 = 'rm -r /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir+'/'
        temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string4 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
        temp_string5 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir



    #os.system(t1)
    
    #temp_string = 'cp -r /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+dir+' /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'

    #print temp_string
    os.system(temp_string)

    # copy over the index.php and .htaccess to each directory
    #temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/.htaccess /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir 
    #print temp_string2
    os.system(temp_string2)

    
    #temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/index.php /afs/cern.ch/user/d/dcurry/www/'+main_dir+'/'+dir
    #print temp_string3
    os.system(temp_string3)

    os.system(temp_string4)
    os.system(temp_string5)

    
'''
# make a png of cutstring for each directory
clf = TCanvas('clf')
chf = TCanvas('chf')
ctt = TCanvas('ctt')
crg = TCanvas('crg')

lf = TPaveText(.05,.1,.95,.8)
hf = TPaveText(.05,.1,.95,.8)
tt = TPaveText(.05,.1,.95,.8)
rg = TPaveText(.05,.1,.95,.8)

clf.cd()
lf.AddText('Z+Light Flavor Cuts')
lf.AddText('Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20')
lf.AddText('V_pt > 100 & HCSV_pt > 100')
lf.AddText('Jet_btagCSV[hJCidx[0]] < 0.97(tight) & Jet_btagCSV[hJCidx[1]] > 0')
lf.AddText('Sum$(Jet_pt > 20 & abs(Jet_eta) < 2.4 & Jet_puId == 1) == 2')
lf.AddText('abs(HVdPhi) > 2.9)')
lf.Draw()

chf.cd()
hf.AddText('Z+Heavy Flavor Cuts')
hf.AddText('Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20')
hf.AddText('V_mass > 75. & V_mass < 105')
hf.AddText('HCSV_mass < 90 || HCSV_mass > 145')
hf.AddText('Jet_btagCSV[hJCidx[0]] > 0.97(tight) & Jet_btagCSV[hJCidx[1]] > 0.6(loose)')
hf.AddText('Sum$(Jet_pt > 20 & abs(Jet_eta) < 2.4 & Jet_puId == 1) == 2')
hf.AddText('abs(HVdPhi) > 2.9)')
hf.Draw()

ctt.cd()
tt.AddText('ttbar Cuts')
tt.AddText('Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20')
tt.AddText('HCSV_pt > 100')
tt.AddText('V_mass < 75 || V_mass > 120')
tt.AddText('Jet_btagCSV[hJCidx[0]] > 0.97(tight) & Jet_btagCSV[hJCidx[1]] > 0.6(loose)')
tt.Draw()

crg.cd()
rg.AddText('ZH125 Jet Regression Cuts')
rg.AddText('Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20')
rg.AddText('abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4')
rg.AddText('HCSV_pt > 0')
rg.Draw()


clf.SaveAs('/afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zlf_cuts.png')

chf.SaveAs('/afs/cern.ch/user/d/dcurry/www/'+main_dir+'/Zhf_cuts.png')

ctt.SaveAs('/afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ttbar_cuts.png')
        
crg.SaveAs('/afs/cern.ch/user/d/dcurry/www/'+main_dir+'/ZH_jet_regr_cuts.png')

'''
