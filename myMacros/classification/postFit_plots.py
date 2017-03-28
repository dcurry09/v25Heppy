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
#from ROOT import *

isVV = False
#isVV = True

isFromDC = False
isFromDC = True

# Wlv: WH
#in_dir = 'WlnHbb_Datacards_Nov8_noRateParamsApplied_withSplitNuisances'

# Wlv: VV
#in_dir = 'WlnZbb_Datacards_Nov24_withNuisancesSplit'

# Zvv: ZH
#in_dir = 'ZnnHbb_LimitDatacards_withoutScaleFactors'

#Zvv: VV
#in_dir = 'Diboson_Datacards_FinalLimit_withoutScaleFactors_new'

# VV
in_dir = 'v25_VH_CMVA_LO_noVHewk_3_25/'

# VH
#in_dir = 'v25_VH_CMVA_LO_3_16'

# Gael
#in_dir = 'DC_v23_VH_v2_25_11_2016'

out_dir = '~/www/v25_VH_CMVA_LO_3_27_preFit/'


cr_list = {
    #'Zhf_low': 'Zhf_low', 
    #'Zlf_low': 'Zlf_low', 
    #'ttbar_low': 'ttbar_low',
    #'Zhf_high': 'Zhf_high', 
    #'Zlf_high': 'Zlf_high', 
    #'ttbar_high': 'ttbar_high'
    
    'Zlf_low_Zuu': 'Zlf_low_Zuu',
    'Zlf_low_Zee': 'Zlf_low_Zee',
    'Zlf_high_Zuu': 'Zlf_high_Zuu',
    'Zlf_high_Zee': 'Zlf_high_Zee',
        
    'Zhf_low_Zee': 'Zhf_low_Zee',
    'Zhf_high_Zee': 'Zhf_high_Zee',
    'Zhf_low_Zuu': 'Zhf_low_Zuu',
    'Zhf_high_Zuu': 'Zhf_high_Zuu',
    
    'ttbar_low_Zee': 'ttbar_low_Zee',
    'ttbar_high_Zee': 'ttbar_high_Zee',
    'ttbar_low_Zuu': 'ttbar_low_Zuu',
    'ttbar_high_Zuu': 'ttbar_high_Zuu',
    
    'BDT_Zee_LowPt': 'ZeeLowPt_13TeV',
    'BDT_Zee_HighPt':'ZeeHighPt_13TeV',
    'BDT_Zuu_LowPt': 'ZuuLowPt_13TeV',
    'BDT_Zuu_HighPt':'ZuuHighPt_13TeV'

    
    ####  wlv; ####
    #'vhbb_ttWen_13TeV': 'ttWen',
    #'vhbb_ttWmn_13TeV': 'ttWmn',
    #'vhbb_whfWen_13TeV': 'whfWen',
    #'vhbb_whfWmn_13TeV': 'whfWmn',
    #'vhbb_wlfWen_13TeV': 'wlfWen',
    #'vhbb_wlfWmn_13TeV': 'wlfWmn'
    
    #### Zvv ####
    #'vhbb_DC_TH_Znn_13TeV_HighPt_QCD':'Znn_13TeV',
    #'vhbb_DC_TH_Znn_13TeV_HighPt_TT':'Znn_13TeV',
    #'vhbb_DC_TH_Znn_13TeV_HighPt_Zbb':'Znn_13TeV',
    #'vhbb_DC_TH_Znn_13TeV_HighPt_Zlight':'Znn_13TeV'
    }

sr_list = { 
    
    'BDT_Zee_LowPt' :'ZeeLowPt_13TeV',
    'BDT_Zee_HighPt':'ZeeHighPt_13TeV',
    'BDT_Zuu_LowPt' :'ZuuLowPt_13TeV',
    'BDT_Zuu_HighPt':'ZuuHighPt_13TeV'
    
    #'ZeeBDT_lowpt': 'ZeeBDT_lowpt',
    #'ZeeBDT_highpt':'ZeeBDT_highpt',
    #'ZuuBDT_lowpt': 'ZuuBDT_lowpt',
    #'ZuuBDT_highpt':'ZuuBDT_highpt'

    #'vhbb_WenHighPt_13TeV': 'WenHighPt'
    #'vhbb_WmnHighPt_13TeV': 'WmnHighPt'
    
    #'Znn_13TeV_HighPt_Signal':'Znn_13TeV'
    }


vv_list = {
    'BDT_Zee_low_ZeePt':'ZeeLowPt_13TeV',
    'BDT_Zee_HighPt':'ZeeHighPt_13TeV',
    'BDT_Zuu_low_ZeePt':'ZuuLowPt_13TeV',
    'BDT_Zuu_HighPt':'ZuuHighPt_13TeV',
    }


final_list = cr_list
#final_list = sr_list
#final_list = vv_list

# =========================================================================

# Make the dir and copy the website ini files
try:
    os.system('mkdir '+out_dir)
except:
     print out_dir+' already exists...'

temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+out_dir
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+out_dir

os.system(temp_string2)
os.system(temp_string3)



for region in final_list:
    print region
    
    os.system('cp ../limits/'+in_dir+'/mlfit.root .')

    '''
    if not isVV:
        if os.path.isfile('mlfit_combined_channels.root'):
            if os.path.isfile('../limits/'+in_dir+'/mlfit.root'):
                os.system('rm mlfit.root')
            os.system('cp mlfit_combined_channels.root ../limits/'+in_dir+'/mlfit.root')

    elif isVV:
        if os.path.isfile('mlfit_VV_combined_channels.root'):
            if os.path.isfile('../limits/'+in_dir+'/mlfit.root'):
                os.system('rm mlfit.root')
            os.system('cp mlfit_VV_combined_channels.root ../limits/'+in_dir+'/mlfit.root')
    '''

    if 'Zlf' in region or 'Zhf' in region or 'ttbar' in region:
        s1 = 'python stack_from_dc_NEW.py -D ../limits/'+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V minCMVA -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'
    
    else:
        s1 = 'python stack_from_dc_NEW.py -D ../limits/'+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V BDT -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'

    if 'Wen' in region and 'HighPt' in region or 'Wmn' in region and 'HighPt' in region:
        s1 = 'python stack_from_dc_NEW.py -D ../limits/'+in_dir+'/'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V BDT -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'

    elif 'Wen' in region or 'Wmn' in region and not 'HighPt' in region:

        print '\n\t Making Wlv Control region Plots...\n\n'

        s1 = 'python stack_from_dc_NEW.py -D ../limits/'+in_dir+'/'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V minCMVA -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'



    if 'Znn' in region and 'Signal' in region:
        s1 = 'python stack_from_dc_NEW.py -D ../limits/'+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V BDT -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'

    elif 'Znn' in region:
         s1 = 'python stack_from_dc_NEW.py -D ../limits/'+in_dir+'/'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V minCMVA -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'
        


    if isFromDC:
        s1 = 'python stack_from_dc.py -D ../limits/'+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -F b -V BDT -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'
        
        if 'Zlf' in region or 'Zhf' in region or 'ttbar' in region:
            s1 = 'python stack_from_dc.py -D ../limits/'+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -F b -V minCMVA -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'
        
        
    print 'Plot Command:', s1
    
    os.system(s1)
    
    #if 'VV' in region:
    #    s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*gg_plus_ZH125_high_Zpt* '+out_dir
        
        
    # Move plot to website dir
    if 'Low' in region and 'Zee' in region or 'low' in region and 'Zee' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*gg_plus* '+out_dir

    if 'Med' in region and 'Zee' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/gg_plus_ZH125_med_Zpt_ZeeMedPt_13TeV_PostFit_b.* '+out_dir
        
    if 'High' in region and 'Zee' in region or 'high' in region and 'Zee' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*gg_plus* '+out_dir

    # muons
    if 'Low' in region and 'Zuu' in region or 'low' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*gg_plus* '+out_dir


    if 'High' in region and 'Zuu' in region or 'Zmm' in region or 'high' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*gg_plus* '+out_dir


        
    if 'Wen' in region or 'Wmn' in region:
        if 'HighPt' in region:
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*gg_plus_ZH125_high_Zpt_W* '+out_dir
        else:
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/minCMVA* '+out_dir
            

    if 'Znn' in region:
        if 'Signal' in region:
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*gg_plus_ZH125_high_Zpt_Znn_13TeV_PostFit_b* '+out_dir
        if 'QCD' in region:
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/Zvv_QCD/Zvv_QCD_minCMVA** '+out_dir
        if 'TT' in region:
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/Zvv_TT/minCMVA* '+out_dir    
        if 'Zlight' in region :
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/Zvv_Zlight/minCMVA* '+out_dir
        if 'Zbb' in region:
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/Zvv_Zbb/minCMVA* '+out_dir

    '''
    # Control Regions
    if 'Zlf_low' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/minCMVA_Zlf_low_PostFit_b* '+out_dir
    if 'Zlf_high' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/minCMVA_Zlf_high_PostFit_b* '+out_dir
    if 'Zhf_low' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/minCMVA_Zhf_low_PostFit_b* '+out_dir
    if 'Zhf_high' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/minCMVA_Zhf_high_PostFit_b* '+out_dir
    if 'ttbar_low' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/minCMVA_ttbar_low_PostFit_b* '+out_dir
    if 'ttbar_high' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/minCMVA_ttbar_high_PostFit_b* '+out_dir
    '''    


    if 'Zlf' in region or 'Zhf' in region or 'ttbar' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*min* '+out_dir
        


    os.system(s2)

#  LocalWords:  Zee
