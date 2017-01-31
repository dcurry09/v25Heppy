###########################################
# Creates stats for sample cross sections, negative weights, etc..
#
# by David Curry
#
###########################################

import sys
import os
import re
import fileinput
import subprocess
import shutil
from ROOT import *
from matplotlib import interactive
import numpy as np
from collections import Counter
import itertools as it


#sample_list = ['Zee', 'Zee_sEG']

sample_list = ['ZH125']

# Input path
in_path = '/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/v14/'

# Trigger Lists

zuu_list = ['HLT_ZmmHbbAll', 'HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v', 'HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v', 'HLT_BIT_HLT_Mu17_TkMu8_DZ_v', 'HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v', 'HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v', 'HLT_BIT_HLT_DoubleIsoMu17_eta2p1_v', 'HLT_BIT_HLT_IsoMu24_eta2p1_v', 'HLT_BIT_HLT_IsoMu24_eta2p1_CentralPFJet30_BTagCSV07_v', 'HLT_BIT_HLT_Mu24_eta2p1_v', 'HLT_BIT_HLT_TkMu24_eta2p1_v', 'HLT_BIT_HLT_Mu24_v', 'HLT_BIT_HLT_IsoMu27_v', 'HLT_BIT_HLT_IsoTkMu27_v', 'HLT_BIT_HLT_TkMu27_v', 'HLT_BIT_HLT_Mu27_v', 'HLT_BIT_HLT_IsoMu20_eta2p1_v', 'HLT_BIT_HLT_IsoMu20_eta2p1_CentralPFJet30_BTagCSV07_v', 'HLT_BIT_HLT_Mu20_v', 'HLT_BIT_HLT_TkMu20_v', 'HLT_BIT_HLT_IsoMu20_v', 'HLT_BIT_HLT_IsoTkMu20_v', 'HLT_BIT_HLT_Mu20_v', 'HLT_BIT_HLT_TkMu20_v', 'HLT_BIT_HLT_Mu40_eta2p1_PFJet200_PFJet50_v']

zee_list = ['HLT_ZeeHbbAll', 'HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v', 'HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v', 'HLT_BIT_HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v', 'HLT_BIT_HLT_DoubleEle24_22_eta2p1_WP75_Gsf_v', 'HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v', 'HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_v', 'HLT_BIT_HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v', 'HLT_BIT_HLT_Ele32_eta2p1_WP75_Gsf_v', 'HLT_BIT_HLT_Ele32_eta2p1_WP75_Gsf_CentralPFJet30_BTagCSV07_v', 'HLT_BIT_HLT_Ele27_eta2p1_WP85_Gsf_HT200_v', 'HLT_BIT_HLT_Ele27_WP85_Gsf_v', 'HLT_BIT_HLT_Ele27_eta2p1_WP75_Gsf_v', 'HLT_BIT_HLT_Ele27_eta2p1_WP75_Gsf_CentralPFJet30_BTagCSV07_v', 'HLT_BIT_HLT_Ele105_CaloIdVT_GsfTrkIdT_v', 'HLT_BIT_HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v']

all_list =  [ zuu_list, zee_list]

zuu_results = []
zee_results = []

signal_cut = 'Jet_pt[hJCidx] >20 & Jet_pt[hJCidx] >20 & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4 & V_mass > 75. & V_mass < 105. & Jet_btagCSV[hJCidx[0]] > 0.97 & Jet_btagCSV[hJCidx[1]] > 0.89 & met_pt < 60 & Sum$(Jet_pt > 20 & abs(Jet_eta) < 2.4) < 3'  

print '\n======================== Starting Sample Stat Analyzer ================================'
print '==================================================================================='

for sample in sample_list: 

    for list in all_list:

        if list == zuu_list: cut  = 'Vtype == 0'
        #& HLT_ZmmHbbAll==1'
        
        if list == zee_list: cut  = 'Vtype == 1'
        #& HLT_ZeeHbbAll==1'
    
        for trigger in list:
    
            print '\n-----> Trigger: ', trigger
            #print '\t path: ', in_path+sample+'.root'
             
            file = TFile(in_path+sample+'.root')
            tree = file.Get('tree')

            # ====== Cuts ======
            all_cut = cut + ' & vLeptons_pt[0]>20 & vLeptons_pt[1]>20'
            
            trigger_cut      = cut + ' & '+ trigger + '==1 & vLeptons_pt[0]>20 & vLeptons_pt[1]>20'

            trig_signal_cut  = cut + ' & '+ trigger + '==1' + ' & '+signal_cut
            
            lowPt_cut = trigger_cut + ' & V_pt > 50 & V_pt < 100'

            medPt_cut = trigger_cut + ' & V_pt > 100 & V_pt < 150'

            highPt_cut = trigger_cut + ' & V_pt > 150' 

            tlowPt_cut = all_cut + ' & V_pt > 50 & V_pt < 100'
            
            tmedPt_cut = all_cut + ' & V_pt > 100 & V_pt < 150'
            
            thighPt_cut = all_cut + ' & V_pt > 150'

            # ==================
            
            hall_trig = TH1F('hall_trig', '' , 10, 0, 500)
            hall  = TH1F('hall', '' , 10, 0, 500)
            htrig = TH1F('htrig', '' , 10, 0, 500)
            hsig  = TH1F('hsig', '' , 10, 0, 500)
            hlow  = TH1F('hlow', '' , 10, 0, 500)
            hmed  = TH1F('hmed', '' , 10, 0, 500)
            hhigh  = TH1F('hhigh', '' , 10, 0, 500)
            hlowt  = TH1F('hlowt', '' , 10, 0, 500)
            hmedt  = TH1F('hmedt', '' , 10, 0, 500)
            hhight  = TH1F('hhight', '' , 10, 0, 500)
            

            tree.Project('hall_trig', 'HCSV_mass', 'sign(genWeight)*(%s)'%(all_cut))
            tree.Project('hall', 'HCSV_mass')
            tree.Project('htrig', 'HCSV_mass', 'sign(genWeight)*(%s)'%(trigger_cut))
            tree.Project('hsig', 'HCSV_mass', 'sign(genWeight)*(%s)'%(trig_signal_cut))
            tree.Project('hlow', 'HCSV_mass',  'sign(genWeight)*(%s)'%(lowPt_cut))
            tree.Project('hmed', 'HCSV_mass',  'sign(genWeight)*(%s)'%(medPt_cut))
            tree.Project('hhigh', 'HCSV_mass', 'sign(genWeight)*(%s)'%(highPt_cut))
            tree.Project('hlowt', 'HCSV_mass',  'sign(genWeight)*(%s)'%(tlowPt_cut))
            tree.Project('hmedt', 'HCSV_mass',  'sign(genWeight)*(%s)'%(tmedPt_cut))
            tree.Project('hhight', 'HCSV_mass', 'sign(genWeight)*(%s)'%(thighPt_cut))
            

            num_all_trig  = hall_trig.GetEntries()
            num_all  = hall.GetEntries()
            num_trig = htrig.GetEntries()
            num_sig  = hsig.GetEntries()
            num_low  = hlow.GetEntries()
            num_med  = hmed.GetEntries()
            num_high  = hhigh.GetEntries()
            tnum_low  = hlowt.GetEntries()
            tnum_med  = hmedt.GetEntries()
            tnum_high  = hhight.GetEntries()
             

            all_p = 100*(num_trig/num_all_trig)
            low_p = 100*(num_low/tnum_low)
            med_p = 100*(num_med/tnum_med)
            high_p = 100*(num_high/tnum_high)
            
            
            

            # store the results: trigger,all,passed,percentage,low%,med%,high%
            if list == zuu_list:
                zuu_results.append([trigger, num_all, num_trig, all_p, low_p, med_p, high_p])

            if list == zee_list:
                zee_results.append([trigger, num_all, num_trig, all_p, low_p, med_p, high_p])
                
            hall.IsA().Destructor(hall)
            htrig.IsA().Destructor(htrig)
            hsig.IsA().Destructor(hsig)
            hlow.IsA().Destructor(hlow)
            hmed.IsA().Destructor(hmed)
            hhigh.IsA().Destructor(hhigh)
            hlowt.IsA().Destructor(hlowt)
            hmedt.IsA().Destructor(hmedt)
            hhight.IsA().Destructor(hhight)

            

# Print the results
print '============= Trigger Counts for Zuu ============='
print ' Trigger:    50 < V pT < 100,      100 < V pT < 150,     V pT > 150'
for result in zuu_results:
    print '---------------------------------------------------------------------'
    print result[0]
    #,'    ',  result[5],'    ',result[6], '     ', result[7] 
    print '          ',result[4],'             ',result[5], '     ', result[6]
    
    

print '============= Trigger Counts for Zee ============='
print ' Trigger:    50 < V pT < 100,      100 < V pT < 150,     V pT > 150'
for result in zee_results:
     print '---------------------------------------------------------------------'
     print result[0]
     print '          ',result[4],'             ',result[5], '     ', result[6]
