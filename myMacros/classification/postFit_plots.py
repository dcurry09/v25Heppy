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
#isFromDC = True

isMjj = False
#isMjj = True

isCRBDT = False
isCRBDT = True

path = '/afs/cern.ch/user/d/dcurry/public/shared/datacards/VH_combo_7_12/'
VV_path = '/afs/cern.ch/user/d/dcurry/public/shared/datacards/VZcombo_7_3/'

mjj_path = '/afs/cern.ch/user/d/dcurry/public/shared/datacards/mjj_7_31/'

##############

# Wlv: WH
#Wlv_in_dir = path+'WlvHbb'
#Wlv_in_dir = '../limits/WlnHbb_Datacards_July6_BDTFullRange/'

# Wlv: VV
#Wlv_in_dir = VV_path+'WlnZbb_Datacards_April6_v2_BTFullDecorr_WHFSplit_BDTGT0p2'

# WLv CR BDT
Wlv_in_dir = '/afs/cern.ch/user/d/dcurry/public/shared/datacards/CRBDT/Wln_CRBDTs'

# Mjj
#Wlv_in_dir = '../limits/WlnHbb_Datacards_July6_MjjAnalysis_BDTPlots/'
#Wlv_in_dir = mjj_path

##############

# Zvv: ZH
#Znn_in_dir = path+'ZnnHbb_Datacards_Jun18_Minus0p8_to_Plus1_NoLowStatShapes'

# Zvv: VV
#Znn_in_dir = VV_path+'ZnnZbb_Datacards_Jun19_Minus0p8_to_Plus1_NoLowStatShapes'

# Zvv CR BDT
Znn_in_dir = '/afs/cern.ch/user/d/dcurry/public/shared/datacards/CRBDT/VH_CR_BDT_v2'

# Mjj
#Znn_in_dir = '../limits/ZnnHbb_Jul28_BDTDatacards_MjjCategories'
#Znn_in_dir = '/afs/cern.ch/user/d/dcurry/public/shared/datacards/Mjj_HighBDT/'
#Znn_in_dir = '/afs/cern.ch/user/d/dcurry/public/shared/datacards/Znn_mjj_postFit_8_1/nJet'


###############

# Zll VV
#Zll_in_dir = VV_path+'ZllZbb_Datacards_Minus08to1_JECfix_7_3'

# Zll VH
Zll_in_dir = path+'ZllHbb_Datacards_Minus08to1_JECfix_7_3'
#Zll_in_dir = '../limits/ZllHbb_Datacards_02to1_6_2'

# Zll CR BDT
#Zll_in_dir = '../limits/ZllHbb_Datacards_CR_BDT_7_3'

# Mjj
#Zll_in_dir = '/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/ZllHbb_Datacards_BDT_MjjVar_8_1'
#Zll_in_dir = '../limits/'


#################

#out_dir = '~/www/VZ_AllChannels_7_25_Unblinded_postFit_v1/'
#out_dir = '~/www/VH_AllChannels_7_24_Unblinded_postFit_v3/'
out_dir = '~/www/Test_CRBDT_v4/'
 

cr_list = {
    
    ##### Zll #####
    #'Zlf_low_Zuu': 'Zlf_low_Zuu',
    # 'Zlf_low_Zee': 'Zlf_low_Zee',
    # 'Zlf_high_Zuu': 'Zlf_high_Zuu',
    # 'Zlf_high_Zee': 'Zlf_high_Zee',
        
    # 'Zhf_low_Zee': 'Zhf_low_Zee',
    # 'Zhf_high_Zee': 'Zhf_high_Zee',
    # 'Zhf_low_Zuu': 'Zhf_low_Zuu',
    # 'Zhf_high_Zuu': 'Zhf_high_Zuu',
    
    # 'ttbar_low_Zee': 'ttbar_low_Zee',
    # 'ttbar_high_Zee': 'ttbar_high_Zee',
    # 'ttbar_low_Zuu': 'ttbar_low_Zuu',
    # 'ttbar_high_Zuu': 'ttbar_high_Zuu',
    
    #'BDT_Zee_LowPt': 'ZeeLowPt_13TeV',
    #'BDT_Zuu_LowPt': 'ZuuLowPt_13TeV',
    #'BDT_Zee_HighPt':'ZeeHighPt_13TeV',
    #'BDT_Zuu_HighPt':'ZuuHighPt_13TeV',
    
    #'Mjj_Zuu_LowPt' :'ZuuLowPt_13TeV',
    #'Mjj_Zee_LowPt' :'ZeeLowPt_13TeV',    
    #'Mjj_Zuu_MedPt' :'ZuuMedPt_13TeV',
    #'Mjj_Zee_MedPt' :'ZeeMedPt_13TeV',
    #'Mjj_Zuu_HighPt':'ZuuHighPt_13TeV',
    #'Mjj_Zee_HighPt':'ZeeHighPt_13TeV',
    

    # #### Wlv and Znn ####
    # 'vhbb_ttWen_13TeV': 'ttWen',
    # 'vhbb_ttWmn_13TeV': 'ttWmn',
    # 'vhbb_whfWenHigh_13TeV': 'whfWenHigh',
    # 'vhbb_whfWmnHigh_13TeV': 'whfWmnHigh',
    # 'vhbb_whfWenLow_13TeV' : 'whfWenLow',
    # 'vhbb_whfWmnLow_13TeV' : 'whfWmnLow',
    # 'vhbb_wlfWen_13TeV': 'wlfWen',
    # 'vhbb_wlfWmn_13TeV': 'wlfWmn',
    #'vhbb_WenHighPt_13TeV':'WenHighPt',
    #'vhbb_WmnHighPt_13TeV':'WmnHighPt',
    
    # WLv Mjj
    #'vhbb_WenHighPt1_13TeV': 'WenHighPt1',
    #'vhbb_WenHighPt2_13TeV': 'WenHighPt2',
    #'vhbb_WenHighPt3_13TeV': 'WenHighPt3',
    #'vhbb_WenHighPt4_13TeV': 'WenHighPt4',
    #'vhbb_WenHighPt5_13TeV': 'WenHighPt5',
    #'vhbb_WenHighPt6_13TeV': 'WenHighPt6',
    #'vhbb_WmnHighPt1_13TeV': 'WmnHighPt1',
    #'vhbb_WmnHighPt2_13TeV': 'WmnHighPt2',
    #'vhbb_WmnHighPt3_13TeV': 'WmnHighPt3',
    #'vhbb_WmnHighPt4_13TeV': 'WmnHighPt4',
    #'vhbb_WmnHighPt5_13TeV': 'WmnHighPt5',
    #'vhbb_WmnHighPt6_13TeV': 'WmnHighPt6',
    
    'Znn_13TeV_TT':'Znn_13TeV_TT',
    'Znn_13TeV_Zlight':'Znn_13TeV_Zlight',
    'Znn_13TeV_Zbb':'Znn_13TeV_Zbb',
    #'Znn_13TeV_Signal':'Znn_13TeV_Signal'
    
    # Znn Mjj
    #'Znn_13TeV_Signal_Mjj_nAddJet0':'Znn_13TeV_Signal_Mjj_nAddJet0',
    #'Znn_13TeV_Signal_Mjj_nAddJet1':'Znn_13TeV_Signal_Mjj_nAddJet1',
    
    

    }


final_list = cr_list

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

    
    if 'Znn' in region: in_dir = Znn_in_dir
    elif 'Wen' in region or 'Wmn' in region: in_dir = Wlv_in_dir
    elif 'Zee' in region or 'Zuu' in region: in_dir = Zll_in_dir

    
    print region, in_dir


    os.system('rm mlfit.root')
    os.system('cp '+in_dir+'/mlfit.root .')


    if 'Zlf' in region or 'Zhf' in region or 'ttbar' in region and not isCRBDT:
        s1 = 'python stack_from_dc_NEW.py -D '+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V minCMVA -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'
    
    elif not isCRBDT:
        s1 = 'python stack_from_dc_NEW.py -D '+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V BDT -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'

    if 'Wen' in region and 'HighPt' in region or 'Wmn' in region and 'HighPt' in region and not isCRBDT:
        s1 = 'python stack_from_dc_NEW.py -D '+in_dir+'/'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V BDT -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'

    elif 'Wen' in region or 'Wmn' in region and not 'HighPt' in region and not isCRBDT:

        print '\n\t Making Wlv Control region Plots...\n\n'

        s1 = 'python stack_from_dc_NEW.py -D '+in_dir+'/'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V minCMVA -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'



    if 'Znn' in region and 'Signal' in region:
        s1 = 'python stack_from_dc_NEW.py -D '+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V BDT -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'

    elif 'Znn' in region and not isCRBDT:
         s1 = 'python stack_from_dc_NEW.py -D '+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V minCMVA -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'
        

    if isCRBDT:
        
        print '\n\t Making CR BDT postFit plots...'
        
        s1 = 'python stack_from_dc_CRBDT.py -D '+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V CRBDT -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'

        if 'Wen' in region or 'Wmn' in region:
            s1 = 'python stack_from_dc_CRBDT.py -D '+in_dir+'/'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V CRBDT -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'

        if isMjj:
            s1 = 'python stack_from_dc_Mjj.py -D '+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -M mlfit.root -F b -V Mjj -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'

            if 'Wen' in region or 'Wmn' in region:
                os.system('rm wln.root')
                os.system('cp '+in_dir+'/wln.root .')
                s1 = 'python stack_from_dc_Mjj.py -D '+in_dir+'/'+region+'.txt -B '+final_list[region]+' -M wln.root -F b -V Mjj -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'



    if isFromDC:
        s1 = 'python stack_from_dc.py -D '+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -F b -V BDT -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'
        
        if 'Zlf' in region or 'Zhf' in region or 'ttbar' in region:
            s1 = 'python stack_from_dc.py -D '+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -F b -V minCMVA -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'
        
            
        if isMjj:
            s1 = 'python stack_from_dc.py -D '+in_dir+'/vhbb_DC_TH_'+region+'.txt -B '+final_list[region]+' -F b -V Mjj -C 13TeVconfig/general -C 13TeVconfig/configPlot_vars -C 13TeVconfig/plots -C 13TeVconfig/paths -C 13TeVconfig/datacard'
            
        
    print 'Plot Command:', s1
    
    os.system(s1)
      


    ######### Move plot to website dir #########
    
    if isCRBDT:

        print 'Region:', region
        print 'final_list[region]:', final_list[region]
        
        #s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*Mjj* '+out_dir
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*gg_plus* '+out_dir
        
        if 'Wen' in region or 'Wmn' in region:
            #region = final_list[region][:-1]
            region = final_list[region]
            #s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+region+'/*Mjj* '+out_dir
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+region+'/*gg_plus* '+out_dir

        if 'Znn' in region:
            #s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/Znn_13TeV_Signal/*Mjj* '+out_dir
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/Znn_13TeV_Signal/*gg_plus* '+out_dir
            
    elif 'Low' in region and 'Zee' in region or 'low' in region and 'Zee' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*gg_plus* '+out_dir

    elif 'Med' in region and 'Zee' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/gg_plus_ZH125_med_Zpt_ZeeMedPt_13TeV_PostFit_b.* '+out_dir
        
    elif 'High' in region and 'Zee' in region or 'high' in region and 'Zee' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*gg_plus* '+out_dir

    # muons
    elif 'Low' in region and 'Zuu' in region or 'low' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*gg_plus* '+out_dir
    

    elif 'High' in region and 'Zuu' in region or 'Zmm' in region or 'high' in region:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*gg_plus* '+out_dir


        
    elif 'Wen' in region or 'Wmn' in region:
        if 'HighPt' in region:
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*gg_plus_ZH125_high_Zpt_W* '+out_dir
        else:
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*minCMVA* '+out_dir
            

    elif 'Znn' in region:
        if 'Signal' in region:
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/Znn_13TeV_Signal/*gg_plus_ZH125* '+out_dir
        if 'QCD' in region:
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/Znn_13TeV_QCD/Znn_QCD_minCMVA* '+out_dir
        if 'TT' in region:
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/Znn_13TeV_TT/*minCMVA* '+out_dir    
        if 'Zlight' in region :
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/Znn_13TeV_Zlight/*minCMVA* '+out_dir
        if 'Zbb' in region:
            s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/Znn_13TeV_Zbb/*minCMVA* '+out_dir


    if ('Zlf' in region or 'Zhf' in region or 'ttbar' in region) and not isCRBDT:
        s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*min* '+out_dir
        
    #if isMjj:
    #    s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*Mjj* '+out_dir
        #s2 = 'cp /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/plots/basic_out/'+final_list[region]+'/*. '+out_dir
        

    os.system(s2)

#  LocalWords:  Zee
