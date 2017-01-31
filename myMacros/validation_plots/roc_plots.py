# Plot Maker for quick ROC curve plots
#
# by David Curry
#
# 7.22.2016
###########################################

import sys
import os
import re
from ROOT import *
from matplotlib import interactive
from ROOT import gROOT



overtrain = False
overtrain = True


# Where to save
outdir = 'Zll_validation_plots/ROC/'


# List of ROC Curves(TMVA output root files)
tmva_dir = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/data/optimization/'

tmva_list = [
    tmva_dir+'MVA_gg_plus_ZH125_highZpt_.root',  tmva_dir+'MVA_gg_plus_ZH125_highZpt_HCSV_reg_mass.root',
    tmva_dir+'MVA_gg_plus_ZH125_highZpt_HCSV_reg_pt.root',  tmva_dir+'MVA_gg_plus_ZH125_highZpt_HVdPhi.root',
    tmva_dir+'MVA_gg_plus_ZH125_highZpt_V_mass.root',  tmva_dir+'MVA_gg_plus_ZH125_highZpt_V_pt.root',
    tmva_dir+'MVA_gg_plus_ZH125_highZpt_hJet_pt0.root',  tmva_dir+'MVA_gg_plus_ZH125_highZpt_deltaR_jj.root',
    tmva_dir+'MVA_gg_plus_ZH125_highZpt_hJet_btagCSV1.root', tmva_dir+'MVA_gg_plus_ZH125_highZpt_hJet_pt1.root',
    tmva_dir+'MVA_gg_plus_ZH125_highZpt_SumJet_pt20absJet_eta24Jet_puId0.root', tmva_dir+'MVA_gg_plus_ZH125_highZpt_hJet_btagCSV0.root',
    tmva_dir+'MVA_gg_plus_ZH125_highZpt_HCSV_dR.root', tmva_dir+'MVA_gg_plus_ZH125_highZpt_HCSV_dEta.root',
    tmva_dir+'MVA_gg_plus_ZH125_highZpt_HCSV_reg_ptV_pt.root', tmva_dir+'MVA_gg_plus_ZH125_highZpt_met_pt.root'
    ] 

var_list = ['', 
            'HCSV_reg_mass',
            'HCSV_reg_pt',
            'HVdPhi',
            'V_mass',
            'V_pt',
            'deltaR_jj',
            'hJet_pt0',
            'deltaR_jj',
            'hJet_btagCSV1',
            'hJet_pt1',
            'SumJet_pt20absJet_eta24Jet_puId0',
            'hJet_btagCSV0',
            'HCSV_dR',
            'HCSV_dEta',
            'HCSV_reg_ptV_pt',
            'met_pt'
            ]

var_list = []

color_list = [25,3,1,40,5,6,7,10,11,2,15,18, 38, 22, 35, 19, 25]


# Root file of Histograms
#file_all   = TFile.Open(tmva_list[0])
#file_all.cd('Method_BDT/gg_plus_ZH125_highZpt')
#roc_all = gDirectory.Get('MVA_gg_plus_ZH125_highZpt_rejBvsS')

stack  = THStack('stack', '')
canvas = TCanvas('canvas')
leg = TLegend(0.2,0.1,0.4,0.4)


for i, var in enumerate(var_list):

    break

    file = TFile.Open(tmva_dir+'MVA_gg_plus_ZH125_highZpt_'+var+'.root')
    
    file.cd('Method_BDT/gg_plus_ZH125_highZpt')

    roc = gDirectory.Get('MVA_gg_plus_ZH125_highZpt_rejBvsS')
    #roc = gDirectory.Get('MVA_gg_plus_ZH125_highZpt_effBvsS')

    stack.Add(roc)

    roc.SetLineColor(color_list[i])
    
    roc.SetLineWidth(2)

    if var == '': leg.AddEntry(roc, 'All Variables', 'l')
    else: leg.AddEntry(roc, var, 'l')

    if var == 'hJet_btagCSV0':
        print 'ROC Integral:', roc.GetIntegral()

# ====== Make the BDT overlay plot ======


'''
canvas.cd()
#canvas.SetLogx()
stack.Draw('nostackHIST')
stack.GetXaxis().SetTitle('Signal Eff.')
stack.GetYaxis().SetTitle('BKG Rejection Eff.')
#stack.GetXaxis().SetRangeUser(0.9, 1)
#stack.GetYaxis().SetRangeUser(0.6, 1)

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.Draw('same')


canvas.SaveAs('Zll_validation_plots/BDT/BDT_output_noReg_wReg.pdf')
'''

if overtrain:

    # ========= Overtraining Checks ===========
    param_dir = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/data/MVA_gg_plus_ZH125_highZpt.root'

    # Input file
    file = TFile.Open(param_dir)

    s1  = THStack('s1', '')
    c1 = TCanvas('c1')
    l1 = TLegend(0.2,0.1,0.4,0.4)

    file.cd('Method_BDT/gg_plus_ZH125_highZpt')

    test  = gDirectory.Get('MVA_gg_plus_ZH125_highZpt_rejBvsS')
    train = gDirectory.Get('MVA_gg_plus_ZH125_highZpt_trainingRejBvsS')

    s1.Add(test)
    s1.Add(train)

    test.SetLineColor(kBlue)
    train.SetLineColor(kRed)

    test.SetLineWidth(2)
    train.SetLineWidth(2)

    c1.cd()
    s1.Draw('nostackHIST')
    s1.GetXaxis().SetTitle('Signal Eff.')
    s1.GetYaxis().SetTitle('BKG Rejection Eff.')
    
    l1.SetFillStyle(0)
    l1.SetBorderSize(0)
    l1.AddEntry(test, 'Test', 'l')
    l1.AddEntry(train, 'Train', 'l')
    l1.Draw('same')
    
    canvas.SaveAs('Zll_validation_plots/BDT/ROC_overtraining.pdf')


# ==========================================


raw_input('Press return to continue...')
