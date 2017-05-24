
# ===================================================
# Python script to perform datacard loop over bins/regions
#
# !!!! Needs to be ran from python directory
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


# ======== Control Regions ========


#control_list = ['Zlf_high', 'Zhf_high', 'ttbar_high',
#                'Zlf_low', 'Zhf_low','ttbar_low',
#                'BDT_high_Zpt', 'BDT_low_Zpt']

#control_combine_list_low  = ['vhbb_DC_TH_Zlf_low.txt', 'vhbb_DC_TH_Zhf_low.txt', 'vhbb_DC_TH_ttbar_low.txt']
#control_combine_list_high = ['vhbb_DC_TH_Zlf_high.txt', 'vhbb_DC_TH_Zhf_high.txt', 'vhbb_DC_TH_ttbar_high.txt']

#control_combine_list_low  = ['vhbb_DC_TH_Zlf_low.txt', 'vhbb_DC_TH_Zhf_low.txt', 'vhbb_DC_TH_ttbar_low.txt', 'vhbb_DC_TH_BDT_LowPt.txt']
#control_combine_list_high = ['vhbb_DC_TH_Zlf_high.txt', 'vhbb_DC_TH_Zhf_high.txt', 'vhbb_DC_TH_ttbar_high.txt', 'vhbb_DC_TH_BDT_HighPt.txt']

control_combine_list_low  = ['vhbb_DC_TH_Zlf_low_Zee.txt', 'vhbb_DC_TH_Zhf_low_Zee.txt', 'vhbb_DC_TH_ttbar_low_Zee.txt',
                             'vhbb_DC_TH_Zlf_low_Zuu.txt', 'vhbb_DC_TH_Zhf_low_Zuu.txt', 'vhbb_DC_TH_ttbar_low_Zuu.txt']

control_combine_list_high  = ['vhbb_DC_TH_Zlf_high_Zee.txt', 'vhbb_DC_TH_Zhf_high_Zee.txt', 'vhbb_DC_TH_ttbar_high_Zee.txt',
                             'vhbb_DC_TH_Zlf_high_Zuu.txt', 'vhbb_DC_TH_Zhf_high_Zuu.txt', 'vhbb_DC_TH_ttbar_high_Zuu.txt']

control_SR_combine_list_low  = ['vhbb_DC_TH_Zlf_low_Zee.txt', 'vhbb_DC_TH_Zhf_low_Zee.txt', 'vhbb_DC_TH_ttbar_low_Zee.txt', 'vhbb_DC_TH_BDT_Zee_LowPt.txt', 
                                'vhbb_DC_TH_BDT_Zuu_LowPt.txt', 
                                'vhbb_DC_TH_Zlf_low_Zuu.txt', 'vhbb_DC_TH_Zhf_low_Zuu.txt', 'vhbb_DC_TH_ttbar_low_Zuu.txt', ]

control_SR_combine_list_high  = ['vhbb_DC_TH_Zlf_high_Zee.txt', 'vhbb_DC_TH_Zhf_high_Zee.txt', 'vhbb_DC_TH_ttbar_high_Zee.txt', 'vhbb_DC_TH_BDT_Zee_HighPt.txt', 
                                 'vhbb_DC_TH_BDT_Zuu_HighPt.txt',  
                                 'vhbb_DC_TH_Zlf_high_Zuu.txt', 'vhbb_DC_TH_Zhf_high_Zuu.txt', 'vhbb_DC_TH_ttbar_high_Zuu.txt']

SR_combine_list_low = ['vhbb_DC_TH_BDT_Zee_LowPt.txt', 'vhbb_DC_TH_BDT_Zuu_LowPt.txt']

SR_combine_list_high = ['vhbb_DC_TH_BDT_Zee_HighPt.txt', 'vhbb_DC_TH_BDT_Zuu_HighPt.txt']

# ==================================

# ======== Signal Split Regions ========
bdt_list = ['BDT_Zee_high_Zpt', 'BDT_Zuu_high_Zpt', 'BDT_Zee_low_Zpt', 'BDT_Zuu_low_Zpt']

control_list = ['Zlf_high_Zuu', 'Zhf_high_Zuu', 'ttbar_high_Zuu', 'Zlf_low_Zuu', 'Zhf_low_Zuu','ttbar_low_Zuu',
                'Zlf_high_Zee', 'Zhf_high_Zee', 'ttbar_high_Zee', 'Zlf_low_Zee', 'Zhf_low_Zee','ttbar_low_Zee']

zhf_list = ['Zhf_low_Zee', 'Zhf_high_Zuu', 'Zhf_low_Zuu', 'Zhf_high_Zee']

zlf_list = ['Zlf_low_Zee', 'Zlf_high_Zuu', 'Zlf_low_Zuu', 'Zlf_high_Zee']

ttbar_list = ['ttbar_low_Zee', 'ttbar_high_Zuu', 'ttbar_low_Zuu', 'ttbar_high_Zee']


# ======== Diboson Analysis =========
vv_bdt_list = ['VV_BDT_Zee_lowZpt', 'VV_BDT_Zee_highZpt', 'VV_BDT_Zuu_lowZpt', 'VV_BDT_Zuu_highZpt']

vv_bdt_list1 = ['VV_BDT_Zee_lowZpt', 'VV_BDT_Zuu_lowZpt']

vv_bdt_list2 = ['VV_BDT_Zee_highZpt', 'VV_BDT_Zuu_highZpt']

vv_control_list = ['Zlf_high_Zuu_VV', 'Zhf_high_Zuu_VV', 'ttbar_high_Zuu_VV', 'Zlf_low_Zuu_VV', 'Zhf_low_Zuu_VV','ttbar_low_Zuu_VV',
                   'Zlf_high_Zee_VV', 'Zhf_high_Zee_VV', 'ttbar_high_Zee_VV', 'Zlf_low_Zee_VV', 'Zhf_low_Zee_VV','ttbar_low_Zee_VV']

vv_zhf_list = ['Zhf_high_Zuu_VV', 'Zhf_high_Zee_VV', 'Zhf_low_Zuu_VV', 'Zhf_low_Zee_VV']

vv_zlf_list = ['Zlf_low_Zee_VV', 'Zlf_high_Zuu_VV', 'Zlf_low_Zuu_VV', 'Zlf_high_Zee_VV']

vv_ttbar_list = ['ttbar_low_Zee_VV', 'ttbar_high_Zuu_VV', 'ttbar_low_Zuu_VV', 'ttbar_high_Zee_VV']

# ====================================

temp_list = ['BDT_Zee_high_Zpt']
#temp_list = zlf_list + bdt_list

# ==============================================

#### Chose VH or VV ####
#datacard_list = bdt_list
#datacard_list = control_list + bdt_list
#datacard_list = control_list

#datacard_list = vv_bdt_list
#datacard_list = vv_control_list + vv_bdt_list
#datacard_list = vv_control_list

datacard_list = temp_list

##### Directory to save datacards ####
#title = 'Datacards_NoRebin_TEST'
title = 'Datacards_minCMVAMed_5_23'

sig_dir = 'ZllHbb_SR_'+title

cr_dir = 'ZllHbb_CR_'+title

# final combined directory
dir = 'ZllHbb_'+title

# Final VV combined Dir
#dir = 'ZllZbb_'+title

print '\n\t ###### Making DC in', dir, cr_dir, sig_dir

#Choose batch mode or sequential
batch = False
#batch = True

# choose bdt, CR split
isSplit = False
isSplit = True

isVV = False
#isVV = True
 
# For Control Region Scale Factors
isCombine = False
#isCombine = True

# BDT final fit(split Pt Categories)
splitRegionFOM = False
splitRegionFOM = True

# Old Test
isFinalFit = False
#isFinalFit = True

# For BDT final fit(One Category)
isFOM = False
#isFOM = True

# For Diboson Analysis
isDiboson = False
#isDiboson = True

# For semiLepton regions
semiLepton = False
#semiLepton = True

#print 'Moving DCs...'

# Move old datacards to a repository
#try:
#    os.makedirs('../limits/repository/')
#except:
#    print 'Repo already exists...'

#print 'Here...'

#os.system('mv ../limits/*.txt ../limits/*.root ../limits/repository/')

#print 'Here2...'




print '\n======================== Starting DataCard Loop ================================'
print '=====================================================================================\n'

if batch:
 
    print '\n------> Running in Batch Mode...' 

    os.system('rm ../limits/*.txt ../limits/*.root')

    # define the os.system function
    def osSystem(datacard):

        print '\n------> Making DataCard for ', datacard,'...'

        os.system('./runAll.sh '+datacard+' 13TeV dc')           
            
    # define the multiprocessing object
    #p = multiprocessing.Pool()
    #results = p.imap(osSystem, datacard_list)
    #p.close()
    #p.join()
    
    # Move all datacards to unique directory
    #if os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+sig_dir):
    #    os.system('rm -rf /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+sig_dir)

    #if os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+cr_dir):
    #    os.system('rm -rf /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+cr_dir)
    
    if not isVV:

        # define the multiprocessing object
        p = multiprocessing.Pool() 
        results = p.imap(osSystem, datacard_list)
        p.close()
        p.join()
    

        if os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir):
            os.system('rm -rf /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir)

        if not os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+sig_dir):
            os.makedirs('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+sig_dir)

        if not os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+cr_dir):
            os.makedirs('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+cr_dir)
        
        if not os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir):
            os.makedirs('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir)
        
        print '\n-----> All jobs finished.  Moving all datacards to /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir

        # signal DCs
        os.system('cp ../limits/*BDT* ../limits/'+sig_dir+'/')
    

        # background
        os.system('cp ../limits/*Zhf* ../limits/'+cr_dir+'/')
        os.system('cp ../limits/*Zlf* ../limits/'+cr_dir+'/')
        os.system('cp ../limits/*ttbar* ../limits/'+cr_dir+'/')
    
        # move both to one dir
        #os.system('mv ../limits/*.root ../limits/*.txt ../limits/'+dir+'/')
        os.system('cp ../limits/'+cr_dir+'/* ../limits/'+dir+'/')
        os.system('cp ../limits/'+sig_dir+'/* ../limits/'+dir+'/')
    
    if isVV:
        
        print '\n###### Making Diboson Cards ######'
        
        os.system('rm ../limits/*.txt ../limits/*.root')
        
        dir     = 'ZllZbb_'+title
        sig_dir = 'ZllZbb_SR_'+title
        cr_dir  = 'ZllZbb_CR_'+title
        
        # define the multiprocessing object
        p = multiprocessing.Pool()
        results = p.imap(osSystem, datacard_list)
        p.close()
        p.join()

        # p = multiprocessing.Pool()
        # results = p.imap(osSystem, vv_bdt_list)
        # p.close()
        # p.join()

        if not os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+sig_dir):
            os.makedirs('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+sig_dir)
        os.system('cp ../limits/*BDT* ../limits/'+sig_dir+'/')

        # p1 = multiprocessing.Pool()
        # results = p1.imap(osSystem, vv_ttbar_list)
        # p1.close()
        # p1.join()
        
        # p1 = multiprocessing.Pool()
        # results = p1.imap(osSystem, vv_zhf_list)
        # p1.close()
        # p1.join()
        
        # p1 = multiprocessing.Pool()
        # results = p1.imap(osSystem, vv_zlf_list)
        # p1.close()
        # p1.join()

        if os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir):
            os.system('rm -rf /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir)
        os.makedirs('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir)

        if not os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+cr_dir):
            os.makedirs('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+cr_dir)
             
        print '\n-----> All jobs finished.  Moving all datacards to /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir


        # background
        os.system('cp ../limits/*Zhf* ../limits/'+cr_dir+'/')
        os.system('cp ../limits/*Zlf* ../limits/'+cr_dir+'/')
        os.system('cp ../limits/*ttbar* ../limits/'+cr_dir+'/')

        # move both to one dir
        os.system('cp ../limits/'+cr_dir+'/* ../limits/'+dir+'/')
        os.system('cp ../limits/'+sig_dir+'/* ../limits/'+dir+'/')

        

if isSplit:
    
    print '\n------> Running in Split Mode...' 

    os.system('rm ../limits/*.txt ../limits/*.root')
    
    def osSystem(datacard):

        print '\n------> Making DataCard for ', datacard,'...'

        os.system('./runAll.sh '+datacard+' 13TeV dc')           


    if not isVV:
        
        p = multiprocessing.Pool() 
        results = p.imap(osSystem, bdt_list)
        p.close()
        p.join()
        
        if not os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+sig_dir):
            os.makedirs('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+sig_dir)
        os.system('cp ../limits/*BDT* ../limits/'+sig_dir+'/')
        
        p1 = multiprocessing.Pool()
        results = p1.imap(osSystem, ttbar_list)
        p1.close()
        p1.join()

        p1 = multiprocessing.Pool()
        results = p1.imap(osSystem, zhf_list)
        p1.close()
        p1.join()

        p1 = multiprocessing.Pool()
        results = p1.imap(osSystem, zlf_list)
        p1.close()
        p1.join()
    

        if os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir):
            os.system('rm -rf /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir)
        os.makedirs('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir)

        if not os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+cr_dir):
            os.makedirs('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+cr_dir)
        
        
        print '\n-----> All jobs finished.  Moving all datacards to /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir


        # background
        os.system('cp ../limits/*Zhf* ../limits/'+cr_dir+'/')
        os.system('cp ../limits/*Zlf* ../limits/'+cr_dir+'/')
        os.system('cp ../limits/*ttbar* ../limits/'+cr_dir+'/')
        
        # move both to one dir
        os.system('cp ../limits/'+cr_dir+'/* ../limits/'+dir+'/')
        os.system('cp ../limits/'+sig_dir+'/* ../limits/'+dir+'/')
    
    
    if isVV:

        print '\n\t###### Making Diboson Cards ######'

        os.system('rm ../limits/*.txt ../limits/*.root')
        
        dir     = 'ZllZbb_'+title
        sig_dir = 'ZllZbb_SR_'+title
        cr_dir  = 'ZllZbb_CR_'+title
        
        # p = multiprocessing.Pool()
        # results = p.imap(osSystem, vv_bdt_list)
        # p.close()
        # p.join()
        
        p = multiprocessing.Pool()
        results = p.imap(osSystem, vv_bdt_list1)
        p.close()
        p.join()

        p = multiprocessing.Pool()
        results = p.imap(osSystem, vv_bdt_list2)
        p.close()
        p.join()

        if not os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+sig_dir):
            os.makedirs('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+sig_dir)
        os.system('cp ../limits/*BDT* ../limits/'+sig_dir+'/')

        p1 = multiprocessing.Pool()
        results = p1.imap(osSystem, vv_ttbar_list)
        p1.close()
        p1.join()
        
        p1 = multiprocessing.Pool()
        results = p1.imap(osSystem, vv_zhf_list)
        p1.close()
        p1.join()
        
        p1 = multiprocessing.Pool()
        results = p1.imap(osSystem, vv_zlf_list)
        p1.close()
        p1.join()

        if os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir):
            os.system('rm -rf /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir)
        os.makedirs('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir)

        if not os.path.exists('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+cr_dir):
            os.makedirs('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+cr_dir)
             
        print '\n-----> All jobs finished.  Moving all datacards to /afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/'+dir


         # background
        os.system('cp ../limits/*Zhf* ../limits/'+cr_dir+'/')
        os.system('cp ../limits/*Zlf* ../limits/'+cr_dir+'/')
        os.system('cp ../limits/*ttbar* ../limits/'+cr_dir+'/')

         # move both to one dir
        os.system('cp ../limits/'+cr_dir+'/* ../limits/'+dir+'/')
        os.system('cp ../limits/'+sig_dir+'/* ../limits/'+dir+'/')
        



# Run combination and Fit tools 
if isCombine:
    
    os.chdir('../limits/'+dir)
    
    temp_string_low  = 'combineCards.py'
    temp_string_high = 'combineCards.py'
    temp_string_combine = 'combineCards.py'
    
    temp_string_combine_BKGonly = 'combineCards.py'
    temp_string_combine_SIGonly = 'combineCards.py'

    # Combine the CR datacards
    for dc_low,dc_high in zip(control_SR_combine_list_low, control_SR_combine_list_high):
            temp_string_combine = temp_string_combine + ' '+dc_low 
            temp_string_combine = temp_string_combine + ' '+dc_high

    temp_string_combine = temp_string_combine + ' ' + ' > vhbb_DC_TH_CR_SIGplusBKG_Combined_combine.txt'
    print 'SIG+BKG combine string:', temp_string_combine
    
    # SIG only
    for dc_low,dc_high in zip(SR_combine_list_low,SR_combine_list_high):
        #print 'DC Low:', dc_low, 'dc High:', dc_high
        temp_string_combine_SIGonly = temp_string_combine_SIGonly + ' '+dc_low
        temp_string_combine_SIGonly = temp_string_combine_SIGonly + ' '+dc_high

    temp_string_combine_SIGonly = temp_string_combine_SIGonly + ' ' + ' > vhbb_DC_TH_CR_SIG_Combined.txt'
    print 'SIG combine string:', temp_string_combine_SIGonly
    
    # BKG only    
    for dc_low,dc_high in zip(control_combine_list_low,control_combine_list_high):
        #print 'DC Low:', dc_low, 'dc High:', dc_high
        temp_string_combine_BKGonly = temp_string_combine_BKGonly + ' '+dc_low
        temp_string_combine_BKGonly = temp_string_combine_BKGonly + ' '+dc_high
    
    temp_string_combine_BKGonly = temp_string_combine_BKGonly + ' ' + ' > vhbb_DC_TH_CR_BKG_Combined.txt'
    print 'BKG combine string:', temp_string_combine_BKGonly

    #print '\n\n============ Low Pt Scale Factors ========='
    #os.system(temp_string_low)
    #t3 = "combine -M MaxLikelihoodFit vhbb_DC_TH_CR_Combined_low.txt --saveShapes --saveWithUncertainties -v 3 --expectSignal=0"# | grep '' | awk '{print $5 }'" 
    #os.system(t3)
        
    #print '\n\n============ High Pt Scale Factors========='
    #os.system(temp_string_high)
    #t4 = 'combine -M MaxLikelihoodFit vhbb_DC_TH_CR_Combined_high.txt --saveShapes --saveWithUncertainties -v 3 --expectSignal=0'
    #os.system(t4)


    # TExt files to store output
    os.system('rm sig_only_RP.txt')
    os.system('rm bkg_only_RP.txt')
    os.system('rm sigPlusBkg_RP.txt')
    
    
    print '\n\n ============= SIG Only Scale Facors =============='
    os.system(temp_string_combine_SIGonly)
    #t5 = 'combine -M MaxLikelihoodFit -m 125 --expectSignal=1 --robustFit=1 --stepSize=0.05 --rMin=-5 --rMax=5 --saveNorm -v 3 vhbb_DC_TH_CR_SIG_Combined.txt >> sig_only_RP.txt'
    t5 = 'combine -M MaxLikelihoodFit -m 125 --expectSignal=1 --minimizerAlgo=Minuit -v 3 vhbb_DC_TH_CR_SIG_Combined.txt'
    #os.system(t5)
    
    print '\n\n ============= BKG Scale Facors =============='
    os.system(temp_string_combine_BKGonly)
    #t5 = 'combine -M MaxLikelihoodFit -m 125 --expectSignal=1 --robustFit=1 --stepSize=0.05 --rMin=-5 --rMax=5 --saveNorm -v 3 vhbb_DC_TH_CR_BKG_Combined.txt >> bkg_only_RP.txt'
    #t5 = 'combine -M MaxLikelihoodFit -m 125 --expectSignal=1 -v 3 --minimizerAlgo=Minuit vhbb_DC_TH_CR_BKG_Combined.txt'
    #os.system(t5)
    
    print '\n\n ============= SIG + BKG Scale Facors =============='
    os.system(temp_string_combine)
    #t5 = 'combine -M MaxLikelihoodFit -m 125 --expectSignal=1 --robustFit=1 --stepSize=0.05 --rMin=-5 --rMax=5 --saveNorm -v 3 vhbb_DC_TH_CR_SIGplusBKG_Combined_combine.txt'
    t5 = 'combine -M MaxLikelihoodFit -m 125 --expectSignal=1 -v 3 --minimizerAlgo=Minuit vhbb_DC_TH_CR_SIGplusBKG_Combined_combine.txt'
    os.system(t5)
    
    #--minimizerAlgo=Minuit --minimizerTolerance=100.0
    
    

###################################################################################
#### End Control Regions


############  ONe pT SR Region ############

if isFOM:
    
    os.chdir('../limits/'+dir)

    print '\t\n\n ================ Combined One pT Region Datacard =================='
    print '==================================================================================='

    t_ele = 'combineCards.py Zmm_TT=vhbb_DC_TH_ttbar_Zuu.txt Zmm_Zhf=vhbb_DC_TH_Zhf_Zuu.txt Zmm_Zlf=vhbb_DC_TH_Zlf_Zuu.txt Zmm_SIG=vhbb_DC_TH_BDT_Zuu.txt Zee_TT=vhbb_DC_TH_ttbar_Zee.txt Zee_Zhf=vhbb_DC_TH_Zhf_Zee.txt Zee_Zlf=vhbb_DC_TH_Zlf_Zee.txt Zee_SIG=vhbb_DC_TH_BDT_Zee.txt > vhbb_Zll.txt'

    os.system(t_ele)

    print '\t\n\n========= CLS Limit ========='
    t1 = "combine -M Asymptotic -t -1 vhbb_Zll.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    os.system(t1)
    
    print '\n==== NO SYS ===='
    t1 = "combine -M Asymptotic -t -1 -S 0 vhbb_Zll.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    os.system(t1)
    
    print '\t\n\n========= Significance ========='
    # P-value
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 vhbb_Zll.txt | grep Significance | awk '{print $3}'"
    os.system(t2)

    print '\n==== NO SYS ===='
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --expectSignal=1 vhbb_Zll.txt | grep Significance | awk '{print $3}'"

    os.system(t2)

    print '\t\n\n========= Signal Strength Uncertainty ========='

    #t3 = "combine -M MaxLikelihoodFit -m 125 -t -1 --expectSignal=1 --robustFit=1 --stepSize=0.05 --rMin=-5 --rMax=5 --saveNorm --saveShapes --plots vhbb_Zll.txt | grep 'Best fit r' | awk '{print $5}'"

    t3 = "combine -M MaxLikelihoodFit -m 125 --expectSignal=1 --saveNormalizations --saveShapes --saveWithUncertainties -v 3 vhbb_Zll.txt"
    
    #os.system(t3)
    




#############################################################################################################
## Split Vpt Regions
##
#############################################################################################################




if splitRegionFOM:

    os.chdir('../limits/'+dir)
    #os.chdir(dir)


    #print '\t\n\n ================ Combined Electron and Control Region Datacard =================='
    #print '==================================================================================='
    #print '\n=============== Low V pT Region ==============='
    
    t_ele = 'combineCards.py Zee_TT_low=vhbb_DC_TH_ttbar_low_Zee.txt Zee_Zhf_low=vhbb_DC_TH_Zhf_low_Zee.txt Zee_Zlf_low=vhbb_DC_TH_Zlf_low_Zee.txt Zee_SIG_low=vhbb_DC_TH_BDT_Zee_LowPt.txt > vhbb_DC_TH_Electron_ControlRegion_Combined_LowPt.txt'

    os.system(t_ele)
    '''
    print '\t\n\n========= CLS Limit ========='
    t1 = "combine -M Asymptotic -t -1 vhbb_DC_TH_Electron_ControlRegion_Combined_LowPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    os.system(t1)
    
    print '\n==== NO SYS ===='
    t1 = "combine -M Asymptotic -t -1 -S 0 vhbb_DC_TH_Electron_ControlRegion_Combined_LowPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    os.system(t1)
    
    print '\t\n\n========= Significance ========='
    # P-value
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 vhbb_DC_TH_Electron_ControlRegion_Combined_LowPt.txt | grep Significance | awk '{print $3}'"
    os.system(t2)

    print '\n==== NO SYS ===='
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --expectSignal=1 vhbb_DC_TH_Electron_ControlRegion_Combined_LowPt.txt | grep Significance | awk '{print $3}'"

    os.system(t2)

    '''

    #print '\t\n\n========= Signal Strength Uncertainty ========='

    t3 = "combine -M MaxLikelihoodFit -m 125 -t -1 --expectSignal=1 --robustFit=1 --stepSize=0.05 --rMin=-5 --rMax=5 --saveNorm --saveShapes --plots vhbb_DC_TH_Electron_ControlRegion_Combined_LowPt.txt | grep 'Best fit r' | awk '{print $5}'"

    #t3 = "combine -M MaxLikelihoodFit -m 125 --expectSignal=1 --saveWorkspace --saveNormalizations --saveShapes --saveWithUncertainties vhbb_DC_TH_Electron_ControlRegion_Combined_LowPt.txt"
    
    #os.system(t3)
    
    
    
    #print '\n=============== High V pT Region ==============='
    
    t_ele_h = 'combineCards.py Zee_TT_high=vhbb_DC_TH_ttbar_high_Zee.txt Zee_Zhf_high=vhbb_DC_TH_Zhf_high_Zee.txt Zee_Zlf_high=vhbb_DC_TH_Zlf_high_Zee.txt Zee_SIG_high=vhbb_DC_TH_BDT_Zee_HighPt.txt > vhbb_DC_TH_Electron_ControlRegion_Combined_HighPt.txt'

    os.system(t_ele_h)

    '''
    print '\t\n\n========= CLS Limit ========='
    t1 = "combine -M Asymptotic -t -1 vhbb_DC_TH_Electron_ControlRegion_Combined_HighPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    os.system(t1)
    
    print '\n==== NO SYS ===='
    t1 = "combine -M Asymptotic -t -1 -S 0 vhbb_DC_TH_Electron_ControlRegion_Combined_HighPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    os.system(t1)
    
    print '\t\n\n========= Significance ========='
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 vhbb_DC_TH_Electron_ControlRegion_Combined_HighPt.txt | grep Significance | awk '{print $3}'"
    os.system(t2)

    print '\n==== NO SYS ===='
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --expectSignal=1 vhbb_DC_TH_Electron_ControlRegion_Combined_HighPt.txt | grep Significance | awk '{print $3}'"
    os.system(t2)


    '''
    #print '\t\n\n========= Signal Strength Uncertainty ========='
    
    #t3 = "combine -M MaxLikelihoodFit -m 125 -t -1 --expectSignal=1 --robustFit=1 --stepSize=0.05 --rMin=-5 --rMax=5 --saveNorm --saveShapes --plots vhbb_DC_TH_Electron_ControlRegion_Combined_HighPt.txt | grep 'Best fit r' | awk '{print $5}'"
    t3 = "combine -M MaxLikelihoodFit -m 125 --expectSignal=1 --saveWorkspace --saveNormalizations --saveShapes --saveWithUncertainties vhbb_DC_TH_Electron_ControlRegion_Combined_HighPt.txt"
    #os.system(t3)
    
    
    
    #print '\t\n\n ================ Combined Muon and Control Region Datacard =================='
    #print '==================================================================================='

    #print '\n=============== Low V pT Region ==============='
    
    t_mu = 'combineCards.py Zmm_TT_low=vhbb_DC_TH_ttbar_low_Zuu.txt Zmm_Zhf_low=vhbb_DC_TH_Zhf_low_Zuu.txt Zmm_Zlf_low=vhbb_DC_TH_Zlf_low_Zuu.txt Zmm_SIG_low=vhbb_DC_TH_BDT_Zuu_LowPt.txt > vhbb_DC_TH_Muon_ControlRegion_Combined_LowPt.txt'

    #t_mu = 'combineCards.py Zmm_TT_low=vhbb_DC_TH_ttbar_low_Zuu.txt Zmm_Zhf_low=vhbb_DC_TH_Zhf_low_Zuu.txt Zmm_SIG_low=vhbb_DC_TH_BDT_Zuu_LowPt.txt > vhbb_DC_TH_Muon_ControlRegion_Combined_LowPt.txt'
    

    os.system(t_mu)
    
    '''
    print '\t\n\n========= CLS Limit ========='
    t1 = "combine -M Asymptotic -t -1 vhbb_DC_TH_Muon_ControlRegion_Combined_LowPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    os.system(t1)
    
    print '\n==== NO SYS ===='
    t1 = "combine -M Asymptotic -t -1 -S 0 vhbb_DC_TH_Muon_ControlRegion_Combined_LowPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    os.system(t1)
    
    print '\t\n\n========= Significance ========='
    # P-value
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 vhbb_DC_TH_Muon_ControlRegion_Combined_LowPt.txt | grep Significance | awk '{print $3}'"
    os.system(t2)
    
    print '\n==== NO SYS ===='
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --expectSignal=1 vhbb_DC_TH_Muon_ControlRegion_Combined_LowPt.txt | grep Significance | awk '{print $3}'"
    os.system(t2)

    '''
    
    #print '\t\n\n========= Signal Strength Uncertainty ========='
    #Uncertainty on Mu
    #t3 = "combine -M MaxLikelihoodFit -m 125 -t -1 --expectSignal=1 --robustFit=1 --stepSize=0.05 --rMin=-5 --rMax=5 --saveNorm --saveShapes --plots vhbb_DC_TH_Muon_ControlRegion_Combined_LowPt.txt | grep 'Best fit r' | awk '{print $5}'"

    t3 = "combine -M MaxLikelihoodFit -m 125 --expectSignal=1 --saveWorkspace --saveNormalizations --saveShapes --saveWithUncertainties vhbb_DC_TH_Muon_ControlRegion_Combined_LowPt.txt"
    #os.system(t3)



    #print '\n=============== High V pT Region ==============='
    
    t_mu_h = 'combineCards.py Zmm_TT_high=vhbb_DC_TH_ttbar_high_Zuu.txt Zmm_Zhf_high=vhbb_DC_TH_Zhf_high_Zuu.txt Zmm_Zlf_high=vhbb_DC_TH_Zlf_high_Zuu.txt Zmm_SIG_high=vhbb_DC_TH_BDT_Zuu_HighPt.txt > vhbb_DC_TH_Muon_ControlRegion_Combined_HighPt.txt'

    os.system(t_mu_h)
    
    '''
    print '\t\n\n========= CLS Limit ========='
    t1 = "combine -M Asymptotic -t -1 vhbb_DC_TH_Muon_ControlRegion_Combined_HighPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    os.system(t1)
    
    print '\n==== NO SYS ===='
    t1 = "combine -M Asymptotic -t -1 -S 0 vhbb_DC_TH_Muon_ControlRegion_Combined_HighPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    os.system(t1)
    
    print '\t\n\n========= Significance ========='
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 vhbb_DC_TH_Muon_ControlRegion_Combined_HighPt.txt | grep Significance | awk '{print $3}'"
    os.system(t2)

    print '\n==== NO SYS ===='
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --expectSignal=1 vhbb_DC_TH_Muon_ControlRegion_Combined_HighPt.txt | grep Significance | awk '{print $3}'"
    os.system(t2)
    '''
    
    #print '\t\n\n========= Signal Strength Uncertainty ========='
    
    #t3 = "combine -M MaxLikelihoodFit -m 125 -t -1 --expectSignal=1 --robustFit=1 --stepSize=0.05 --rMin=-5 --rMax=5 --saveNorm --saveShapes --plots vhbb_DC_TH_Muon_ControlRegion_Combined_HighPt.txt | grep 'Best fit r' | awk '{print $5}'"

    t3 = "combine -M MaxLikelihoodFit -m 125 --expectSignal=1 --saveWorkspace --saveNormalizations --saveShapes --saveWithUncertainties vhbb_DC_TH_Muon_ControlRegion_Combined_HighPt.txt"
    #os.system(t3)


    # ==================================================================================================
    # ==================================================================================================

    #print '\t\n\n ================ Combined E+M and Control Region Datacard =================='
    #print '==================================================================================='
    
    #  print '\n=============== Low V pT Region ==============='
    
    t_low = 'combineCards.py vhbb_DC_TH_Muon_ControlRegion_Combined_LowPt.txt vhbb_DC_TH_Electron_ControlRegion_Combined_LowPt.txt > vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_LowPt.txt'

    os.system(t_low)
    
    #print '\t\n\n========= CLS Limit ========='
    t1 = "combine -M Asymptotic -m 125 -t -1 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_LowPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    #os.system(t1)
    
    #print '\n==== NO SYS ===='
    t1 = "combine -M Asymptotic -m 125 -t -1 -S 0 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_LowPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    #os.system(t1)

    #print '\n==== Post Fit ===='
    t1 = "combine -M Asymptotic -m 125 -t -1 --toysFreq vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_LowPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    #os.system(t1)

    #print '\n==== Post Fit NO SYS ===='
    t1 = "combine -M Asymptotic -m 125 -t -1 -S 0 --toysFreq vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_LowPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    #os.system(t1)

    #print '\t\n\n========= Significance ========='
    # P-value
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_LowPt.txt | grep Significance | awk '{print $3}'"
    #os.system(t2)
    
    #print '\n==== NO SYS ===='
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --expectSignal=1 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_LowPt.txt | grep Significance | awk '{print $3}'"
    #os.system(t2)
    
    #print '\n==== Post Fit ===='
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --toysFreq --expectSignal=1 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_LowPt.txt | grep Significance | awk '{print $3}'"
    #os.system(t2)

    #print '\n==== Post Fit NO SYS===='
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --toysFreq --expectSignal=1 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_LowPt.txt | grep Significance | awk '{print $3}'"
    #os.system(t2)

    #print '\t\n\n========= Signal Strength Uncertainty ========='

    #Uncertainty on Mu

    #t3 = "combine -M MaxLikelihoodFit -m 125 -t -1 --expectSignal=1 --robustFit=1 --stepSize=0.05 --rMin=-5 --rMax=5 --saveNorm --saveShapes --plots vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_LowPt.txt | grep 'Best fit r' | awk '{print $5}'"
    #t3 = "combine -M MaxLikelihoodFit --expectSignal=1 -t -1 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_LowPt.txt"

    t3 = "combine -M MaxLikelihoodFit -m 125 --expectSignal=1 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_LowPt.txt"
    #os.system(t3)


    #print '\n=============== High V pT Region ==============='
    
    t_high = 'combineCards.py vhbb_DC_TH_Muon_ControlRegion_Combined_HighPt.txt vhbb_DC_TH_Electron_ControlRegion_Combined_HighPt.txt > vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_HighPt.txt'
    os.system(t_high)
    

    #print '\t\n\n========= CLS Limit ========='
    t1 = "combine -M Asymptotic -m 125 -t -1 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_HighPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
   # os.system(t1)
    
    #print '\n==== NO SYS ===='
    t1 = "combine -M Asymptotic -m 125 -t -1 -S 0 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_HighPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    #os.system(t1)
    
    #print '\n==== Post Fit ===='
    t1 = "combine -M Asymptotic -m 125 -t -1 --toysFreq vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_HighPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    #os.system(t1)

    #print '\n==== Post Fit NO SYS ===='
    t1 = "combine -M Asymptotic -m 125 -t -1 -S 0 --toysFreq vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_HighPt.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    #os.system(t1)

    #print '\t\n\n========= Significance ========='
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_HighPt.txt | grep Significance | awk '{print $3}'"
    #os.system(t2)

    #print '\n==== NO SYS ===='
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --expectSignal=1 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_HighPt.txt | grep Significance | awk '{print $3}'"
    #os.system(t2)

    #print '\n==== Post Fit ===='
    
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --toysFreq --expectSignal=1 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_HighPt.txt | grep Significance | awk '{print $3}'"
    #os.system(t2)

    #print '\t\n\n========= Signal Strength Uncertainty ========='
    
    #t3 = "combine -M MaxLikelihoodFit -m 125 -t -1 --expectSignal=1 --robustFit=1 --stepSize=0.05 --rMin=-5 --rMax=5 --saveNorm --saveShapes --plots vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_HighPt.txt | grep 'Best fit r' | awk '{print $5}'"

    #t3 = "combine -M MaxLikelihoodFit --expectSignal=1 -t -1 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_HighPt.txt"

    t3 = "combine -M MaxLikelihoodFit -m 125 --expectSignal=1 vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_HighPt.txt"
    #os.system(t3)
    

    #print '\t\n\n========= All Pt regions Combined  ========='
    
    # Now combine the signal and control regions together for a better fit
    temp_string = 'combineCards.py'

    temp_string = temp_string + ' vhbb_DC_TH_Muon_ControlRegion_Combined_LowPt.txt vhbb_DC_TH_Electron_ControlRegion_Combined_LowPt.txt vhbb_DC_TH_Muon_ControlRegion_Combined_HighPt.txt vhbb_DC_TH_Electron_ControlRegion_Combined_HighPt.txt'

    #temp_string = temp_string + ' ' + ' > vhbb_DC_TH_Electron_Muon_ControlRegion_Combined_pTregions.txt'
    temp_string = temp_string + ' ' + ' > vhbb_Zll.txt'
    
    # TEST datacard where CRs are added once and at the end
    #temp_string = 'combineCards.py Zee_TT_low=vhbb_DC_TH_ttbar_low_Zee.txt Zee_Zhf_low=vhbb_DC_TH_Zhf_low_Zee.txt Zee_Zlf_low=vhbb_DC_TH_Zlf_low_Zee.txt Zee_SIG_low=vhbb_DC_TH_BDT_Zee_LowPt.txt Zmm_TT_low=vhbb_DC_TH_ttbar_low_Zuu.txt Zmm_Zhf_low=vhbb_DC_TH_Zhf_low_Zuu.txt Zmm_Zlf_low=vhbb_DC_TH_Zlf_low_Zuu.txt Zmm_SIG_low=vhbb_DC_TH_BDT_Zuu_LowPt.txt Zee_TT_high=vhbb_DC_TH_ttbar_high_Zee.txt Zee_Zhf_high=vhbb_DC_TH_Zhf_high_Zee.txt Zee_Zlf_high=vhbb_DC_TH_Zlf_high_Zee.txt Zee_SIG_high=vhbb_DC_TH_BDT_Zee_HighPt.txt Zmm_TT_high=vhbb_DC_TH_ttbar_high_Zuu.txt Zmm_Zhf_high=vhbb_DC_TH_Zhf_high_Zuu.txt Zmm_Zlf_high=vhbb_DC_TH_Zlf_high_Zuu.txt Zmm_SIG_high=vhbb_DC_TH_BDT_Zuu_HighPt.txt > vhbb_Zll.txt'
    
    #temp_string = 'combineCards.py Zee_SIG_low=vhbb_DC_TH_BDT_Zee_LowPt.txt Zmm_SIG_low=vhbb_DC_TH_BDT_Zuu_LowPt.txt Zmm_SIG_high=vhbb_DC_TH_BDT_Zuu_HighPt.txt Zee_SIG_high=vhbb_DC_TH_BDT_Zee_HighPt.txt > vhbb_Zll.txt'
    
    os.system(temp_string)
    


    #print '\t\n\n========= CLS Limit ========='
    # CLs Limit
    t1 = "combine -M Asymptotic -m 125 -t -1 vhbb_Zll.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    #os.system(t1)
    
    #print '\n==== NO SYS ===='
    t1 = "combine -M Asymptotic -m 125 -t -1 -S 0 vhbb_Zll.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    #os.system(t1)

    #print '\n==== Post Fit ===='
    t1 = "combine -M Asymptotic -m 125 -t -1 --toysFreq vhbb_Zll.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    #os.system(t1)
    
    #print '\n==== Post Fit NO SYS ===='
    t1 = "combine -M Asymptotic -m 125 -t -1 -S 0 --toysFreq vhbb_Zll.txt | grep 'Expected 50.0%' | awk '{print $5 }'"
    #os.system(t1)


    print '\t\n\n========= Significance ========='
    
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 vhbb_Zll.txt | grep Significance | awk '{print $3}'"
    os.system(t2)
    
    print '\n==== NO SYS ===='
    t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --expectSignal=1 vhbb_Zll.txt | grep Significance | awk '{print $3}'"
    os.system(t2)

    #print '\n==== Post Fit ===='
    #t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --toysFreq --expectSignal=1 vhbb_Zll.txt | grep Significance | awk '{print $3}'"
    #os.system(t2)
    
    # print '\n==== Post Fit NO SYS ===='
    # t2 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --toysFreq --expectSignal=1 vhbb_Zll.txt | grep Significance | awk '{print $3}'"
    # os.system(t2)

    print '\t\n\n========= Signal Strength Uncertainty ========='

    #Uncertainty on Mu
    
    #t3 = "combine -M MaxLikelihoodFit -m 125 -t -1 --expectSignal=1 --robustFit=1 --stepSize=0.05 --rMin=-5 --rMax=5 --minimizerAlgo=Minuit --minimizerTolerance=100.0 --saveNorm --saveShapes vhbb_Zll.txt | grep 'Best fit r' | awk '{print $5}'"
    
    #t3 = "combine -M MaxLikelihoodFit -m 125 --expectSignal=1 --robustFit=1 --stepSize=0.05 --rMin=-5 --rMax=5 --minimizerAlgo=Minuit --minimizerTolerance=100.0 --saveNorm --saveShapes vhbb_Zll.txt | grep 'Best fit r' | awk '{print $5}'"
    
    t3 = 'combine -M MaxLikelihoodFit -m 125 --expectSignal=1 --robustFit=1 --stepSize=0.05 --rMin=-5 --rMax=5 --saveNorm -v 3 --saveShapes vhbb_Zll.txt'

    #t3 = "combine -M MaxLikelihoodFit -m 125 --expectSignal=1 -t -1 --saveNorm --saveShapes --saveWithUncertainties --plots vhbb_Zll.txt"
    
    #t3 = "combine -M MaxLikelihoodFit -m 125 -t -1 --expectSignal=0 vhbb_Zll.txt"

    #t3 = "combine -M MaxLikelihoodFit -m 125 -t -1 --expectSignal=1 vhbb_Zll.txt"
    
    #t3 = 'combine -M MaxLikelihoodFit -m 125 vhbb_Zll.txt --saveShapes --saveWithUncertainties -v 3 --expectSignal=0'
    
    #os.system(t3)
    


#############################################################################################################

