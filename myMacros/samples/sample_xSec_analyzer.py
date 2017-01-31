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


# List of samples to be analyzed

sample_list = {'ZH125':0.04837, 'ggZH125': 0.01340, 'ZZ':0.03, 'WZ':0.16, 'ttbar':815.16, 
               'DY_inclusive':6024.0, 'DY_100to200':171.46, 'DY_200to400':52.585, 'DY_400to600':6.76131, 'DY_600toInf':2.718,
               #'DY_5to50_inclusive', 'DY_5to50_100to200', 'DY_5to50_200to400', 'DY_5to50_400to600', 'DY_5to50_600toInf',
               'ST_t':220.45, 'ST_s':10.32, 'ST_tW_antitop':35.6, 'ST_tW_top':35.6
               }


#With DY Bjet samples
sample_list_bjets = {
    #'ZH125':0.04837, 'ggZH125': 0.01340, 'ZZ':0.03, 'WZ':0.16, 'ttbar':815.16,
    'DY_inclusive':6024.0, 'DY_100to200':171.46, 'DY_200to400':52.585, 'DY_400to600':6.76131, 'DY_600toInf':2.718, 'DY_Bjets':1, 'DY_BgenFilter':1, 
    'DY_5to50_inclusive':1, 'DY_5to50_100to200':1, 'DY_5to50_200to400':1, 'DY_5to50_400to600':1, 'DY_5to50_600toInf':1
    
    #'ST_t':220.45, 'ST_s':10.32, 'ST_tW_antitop':35.6, 'ST_tW_top':35.6
    }

#data_list = ['Zuu', 'Zee']
#data_list = []

#dy_list = ['DY_inclusive']

# lumi in pb (10 fb = 10,000 pb)
lumi = 2219.0

# DY sums
dy_zee_low = 0
dy_zee_high = 0
dy_zuu_low = 0
dy_zuu_high = 0
dy_hf = 0


st_zee_low = 0
st_zee_high = 0
st_zuu_low = 0
st_zuu_high = 0


# Input path
in_path = '/exports/uftrig01a/dcurry/heppy/files/prep_out/v21_5_1_'

# No Bjets
#in_path = '/exports/uftrig01a/dcurry/heppy/files/prep_out/DY_noBjets/v21_5_1_'

os.system('rm sample_xSec.txt')


print '\n======================== Starting Sample Stat Analyzer ================================'
print '===================================================================================\n'


for sample in sample_list:
#for sample in sample_list_bjets:

    print '----->  Sample: ', sample
    print '\t path: ', in_path+sample+'.root'

    file = TFile(in_path+sample+'.root')

    posWeight = file.Get('CountPosWeight')
    negWeight = file.Get('CountNegWeight')
    
    #xsec = sample_list_bjets[sample]
    xsec = 1 

    theScale = lumi*xsec / (posWeight.GetBinContent(1) - negWeight.GetBinContent(1))

    negWeight_fraction = negWeight.GetBinContent(1) / (posWeight.GetBinContent(1) + negWeight.GetBinContent(1))

    # Now look at stats for BDT training
    tree = file.Get('tree')

    minBtag = 'min(Jet_btagCSV[hJCidx[0]],Jet_btagCSV[hJCidx[1]])'
    maxBtag = 'max(Jet_btagCSV[hJCidx[0]],Jet_btagCSV[hJCidx[1]])'
    
    CSVT = '0.935'
    CSVM = '0.80'
    CSVL = '0.460'
    CSVC = '0.244'
    
    # the BDT cuts
    '''
    zuu_high_cut = '(HLT_BIT_HLT_IsoMu20_v || HLT_BIT_HLT_IsoTkMu20_v) & Vtype == 0 & Jet_btagCSV[hJCidx[0]] > '+CSVL+' & Jet_btagCSV[hJCidx[1]] > '+CSVC+' & V_mass > 75. & V_mass < 105. & V_pt > 100 & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4 & HCSV_mass > 10. & HCSV_mass < 250. & Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20'
    
    zuu_low_cut = '(HLT_BIT_HLT_IsoMu20_v || HLT_BIT_HLT_IsoTkMu20_v) & Vtype == 0 & Jet_btagCSV[hJCidx[0]] > '+CSVL+' & Jet_btagCSV[hJCidx[1]] > '+CSVC+' & V_mass > 75. & V_mass < 105. & V_pt > 50 & V_pt < 100 & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4 & HCSV_mass > 10. & HCSV_mass < 250. & Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20'

    zee_high_cut = 'HLT_BIT_HLT_Ele23_WPLoose_Gsf_v & Vtype == 1 & Jet_btagCSV[hJCidx[0]] > '+CSVL+' & Jet_btagCSV[hJCidx[1]] > '+CSVL+' & V_mass > 75. & V_mass < 105. & V_pt > 100 & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4 & HCSV_reg_mass < 250. & Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20'
    
    zee_low_cut = 'HLT_BIT_HLT_Ele23_WPLoose_Gsf_v & Vtype == 1 & Jet_btagCSV[hJCidx[0]] > '+CSVL+' & Jet_btagCSV[hJCidx[1]] > '+CSVC+'& V_mass > 75. & V_mass < 105. & V_pt > 50 & V_pt < 100 & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4 & HCSV_mass > 40. & HCSV_mass < 250. & Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20'
    '''

    zuu_high_cut = '(HLT_BIT_HLT_IsoMu20_v || HLT_BIT_HLT_IsoTkMu20_v) & Vtype == 0 & Jet_btagCSV[hJCidx[0]] > '+CSVL+' & Jet_btagCSV[hJCidx[1]] > '+CSVC+' & V_mass > 75. & V_mass < 105. & V_pt > 100 & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4 & HCSV_mass > 90. & HCSV_mass < 150. & Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20'
    
    zuu_low_cut = '(HLT_BIT_HLT_IsoMu20_v || HLT_BIT_HLT_IsoTkMu20_v) & Vtype == 0 & Jet_btagCSV[hJCidx[0]] > '+CSVL+' & Jet_btagCSV[hJCidx[1]] > '+CSVC+' & V_mass > 75. & V_mass < 105. & V_pt > 50 & V_pt < 100 & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4 & HCSV_mass > 90. & HCSV_mass < 150. & Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20'

    zee_high_cut = 'HLT_BIT_HLT_Ele23_WPLoose_Gsf_v & Vtype == 1 & Jet_btagCSV[hJCidx[0]] > '+CSVL+' & Jet_btagCSV[hJCidx[1]] > '+CSVL+' & V_mass > 75. & V_mass < 105. & V_pt > 100 & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4 & HCSV_mass > 90. & HCSV_reg_mass < 150. & Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20'
    
    zee_low_cut = 'HLT_BIT_HLT_Ele23_WPLoose_Gsf_v & Vtype == 1 & Jet_btagCSV[hJCidx[0]] > '+CSVL+' & Jet_btagCSV[hJCidx[1]] > '+CSVC+'& V_mass > 75. & V_mass < 105. & V_pt > 50 & V_pt < 100 & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4 & HCSV_mass > 90. & HCSV_mass < 150. & Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20'


    all_cut = '(Vtype == 1 | Vtype == 0) & Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20 & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4'

    # DY HF cuts
    hf_cut = '(((V_mass > 85. & V_mass < 97. & met_pt < 60 & Jet_pt_reg[hJCidx[0]] > 20 & Jet_pt_reg[hJCidx[1]] > 20 & (HCSV_reg_mass < 90 || HCSV_reg_mass > 145) & Jet_btagCSV[hJCidx[0]] > 0.935 & Jet_btagCSV[hJCidx[1]] > 0.46 & (vLeptons_pt[0] > 20. & vLeptons_pt[1] >  20.) & (vLeptons_relIso04[0] < 0.25 & vLeptons_relIso04[1] < 0.25)) & (((HLT_BIT_HLT_IsoMu20_v == 1) || (HLT_BIT_HLT_IsoTkMu20_v == 1) || (HLT_BIT_HLT_Ele23_WPLoose_Gsf_v))))&&(((Vtype == 0) || (Vtype == 1)) & (vLeptons_pt[0] > 15. & vLeptons_pt[1] > 15.)))'
    
    
    h1 = TH1F('h1', '' , 50, 0, 500)
    h2 = TH1F('h2', '' , 50, 0, 500)
    h3 = TH1F('h3', '' , 50, 0, 500)
    h4 = TH1F('h4', '' , 50, 0, 500)
    h5 = TH1F('h5', '' , 50, 0, 500)
    h6 = TH1F('h6', '' , 50, 0, 500)
    
    tree.Project('h1', 'HCSV_mass', 'sign(genWeight)*'+(zuu_high_cut))
    tree.Project('h2', 'HCSV_mass', 'sign(genWeight)*'+(zuu_low_cut))
    tree.Project('h3', 'HCSV_mass', 'sign(genWeight)*'+(zee_high_cut))
    tree.Project('h4', 'HCSV_mass', 'sign(genWeight)*'+(zee_low_cut))
    tree.Project('h5', 'HCSV_mass', 'sign(genWeight)*'+(all_cut))
    tree.Project('h6', 'HCSV_mass', 'sign(genWeight)*'+(hf_cut))
    
    num_h1 = h1.GetEntries()
    num_h2 = h2.GetEntries()
    num_h3 = h3.GetEntries()
    num_h4 = h4.GetEntries()
    num_h5 = h5.GetEntries()
    num_h6 = h6.GetEntries()

    if 'DY' in sample:
        dy_zee_low = dy_zee_low + num_h4
        dy_zee_high = dy_zee_high + num_h3
        dy_zuu_low = dy_zuu_low + num_h2
        dy_zuu_high = dy_zuu_high + num_h1
        dy_hf = dy_hf + num_h6


    if 'ST' in sample:
        st_zee_low = st_zee_low + num_h4
        st_zee_high = st_zee_high + num_h3
        st_zuu_low = st_zuu_low + num_h2
        st_zuu_high = st_zuu_high + num_h1


    with open('sample_xSec.txt', 'a') as file:
        
        file.write('\n======= Sample: '+sample+'========\n')
        #file.write('Luminosity          : '+str(lumi)+'\n')
        #file.write('Cross Section       : '+str(xsec)+'\n')
        #file.write('Events(after preSelection): '+str(num_h5)+'\n')
        #file.write('Scale Factor        : '+str(theScale)+'\n')
        #file.write('Neg Weight Fraction : '+str(negWeight_fraction)+'\n')
        file.write('========= BDT Statistics ==========\n')
        file.write('Zuu_lowPt Events : '+str(num_h2)+'\n')
        file.write('Zee_lowPt Events : '+str(num_h4)+'\n')
        file.write('Zuu_highPt Events : '+str(num_h1)+'\n')
        file.write('Zee_highPt Events : '+str(num_h3)+'\n')
        

            
with open('sample_xSec.txt', 'a') as file:
    
     file.write('\n\n==== DY Total BDT Statistics ====\n')
     file.write('Zuu_lowPt Events : '+str(dy_zuu_low)+'\n')
     file.write('Zee_lowPt Events : '+str(dy_zee_low)+'\n')
     file.write('Zuu_highPt Events : '+str(dy_zuu_high)+'\n')
     file.write('Zee_highPt Events : '+str(dy_zee_high)+'\n')
     
     file.write('\n')
     file.write('DY Total HF Events : '+str(dy_hf)+'\n')
     #file.write('Zee_lowPt Events : '+str(dy_zee_low)+'\n')
     #file.write('Zuu_highPt Events : '+str(dy_zuu_high)+'\n')
     #file.write('Zee_highPt Events : '+str(dy_zee_high)+'\n')


     #file.write('\n\n========= ST Total BDT Statistics ==========\n')
     #file.write('Zuu_lowPt Events : '+str(st_zuu_low)+'\n')
     #file.write('Zee_lowPt Events : '+str(st_zee_low)+'\n')
     #file.write('Zuu_highPt Events : '+str(st_zuu_high)+'\n')
     #file.write('Zee_highPt Events : '+str(st_zee_high)+'\n')


'''
#  ======= STart Data Analyzer =====
for data in data_list:
    
    print '----->  Sample: ', data
    print '\t path: ', in_path+data+'.root'
    
    file = TFile(in_path+data+'.root')
    
    tree = file.Get('tree')

    # ===== Cuts =====
    json_cut = 'json == 1'

    hlt_singleMu_cut = json_cut + ' & HLT_BIT_HLT_IsoMu24_eta2p1_v == 1'

    hlt_doubleMu_cut = json_cut + ' & HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v == 1'    

    hlt_doubleEG_cut = json_cut + ' & HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v == 1'
    # ================
    

    hAll  = TH1F('hAll', '' , 10, 0, 500)
    hJson = TH1F('hJson', '' , 10, 0, 500)
    hHlt  = TH1F('hHlt', '' , 10, 0, 500)

    tree.Project('hAll', 'HCSV_mass')
    tree.Project('hJson', 'HCSV_mass', json_cut)
    
    if data == 'Zuu':
        tree.Project('hHlt', 'HCSV_mass', hlt_singleMu_cut)
    if data == 'Zee':
        tree.Project('hHlt', 'HCSV_mass', hlt_doubleEG_cut)
    if data == 'Zuu_double':
        tree.Project('hHlt', 'HCSV_mass', hlt_doubleMu_cut)

        
    num_all  = hAll.GetEntries()
    num_json = hJson.GetEntries()    
    num_hlt  = hHlt.GetEntries()
     
    with open('sample_xSec.txt', 'a') as file:
         
        file.write('\n\n===================== DATA: '+data+'============================\n')
        file.write('Total Events  : '+str(num_all)+'\n')
        file.write('Json Events   : '+str(num_json)+'\n')
        file.write('HLT Events   : '+str(num_hlt)+'\n')
        file.write('HLT fraction   : '+str(num_hlt/(num_json))+'\n')




# Check DY subcuts

for sample in dy_list:

    print '----->  Sample: ', sample
    print '\t path: ', in_path+sample+'.root'

    file = TFile(in_path+sample+'.root')

    tree = file.Get('tree')

    # ===== Cuts =====
    Vbb = "Sum$(GenJet_pt>20 && abs(GenJet_eta)<2.4 && GenJet_numBHadrons>0)>=2"
    Vb = "Sum$(GenJet_pt>20 && abs(GenJet_eta)<2.4 && GenJet_numBHadrons>0)==1"
    Vcc = "Sum$(GenJet_pt>20 && abs(GenJet_eta)<2.4 && GenJet_numCHadrons>0)>=1 && Sum$(GenJet_pt>20 & abs(GenJet_eta)<2.4 & GenJet_numBHadrons>0)==0"
#!Vb && !Vbb"

    Vudsg = "Sum$(GenJet_pt>20 & abs(GenJet_eta)<2.4 & GenJet_numBHadrons>0)==0 & Sum$(GenJet_pt>20 & abs(GenJet_eta)<2.4 && GenJet_numCHadrons>0)==0"

    
    hAll = TH1F('hAll', '' , 10, 0, 500)
    hlf  = TH1F('hlf', '' , 10, 0, 500)  
    hbb  = TH1F('hbb', '' , 10, 0, 500)
    hb   = TH1F('hb', '' , 10, 0, 500)
    hcc  = TH1F('hcc', '' , 10, 0, 500)
    
    tree.Project('hAll', 'HCSV_mass')
    tree.Project('hlf', 'HCSV_mass', Vudsg)
    tree.Project('hb', 'HCSV_mass', Vb)
    tree.Project('hbb', 'HCSV_mass', Vbb)
    tree.Project('hcc', 'HCSV_mass', Vcc)
    
    num_all = hAll.GetEntries()
    num_lf  = hlf.GetEntries()
    num_bb  = hbb.GetEntries()
    num_b   = hb.GetEntries()
    num_cc  = hcc.GetEntries()

    print '============= DY Gen Categories ============='
    print 'All : ', num_all
    print 'LF  : ', num_lf
    print 'Vbb : ', num_bb
    print 'Vb  : ', num_b
    print 'Vcc : ', num_cc
    print 'Sum : ', num_lf + num_bb + num_b + num_cc 
    
'''
