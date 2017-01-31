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
from decimal import *
from matplotlib import interactive
from ROOT import *


# ==== Choose signal or control regions ====

signal = False
signal = True

control = False
#control = True

# which Z channel
#channel_list = ['Zee', 'Zuu']
channel_list = ['Zuu']
#channel_list = ['Zee'] 

# For control, which background
zlf = False
#zlf = True

zhf = False
zhf = True

ttbar = False
#ttbar = True

bkg_list = []
if zlf:   bkg_list.append('Zlf')
if zhf:   bkg_list.append('Zhf')
if ttbar: bkg_list.append('ttbar')

# Decimal precision
getcontext().prec = 3
# ===========================================



# ======= Signal Region: Variables ========

jet_pt_list = [20, 25, 30, 35, 40, 45, 50]
jet_pt = False 
#jet_pt = True

z_mass_low_list  = [75, 80]
z_mass_high_list = [100, 105, 110, 115, 120]
z_mass = False
#z_mass = True

cmva_list = [0.5, 0.6, 0.72, 0.74, 0.76, 0.78, 0.80, 0.82, 0.84, 0.86, 0.88, 0.9, 0.92]
cmva_jet2_list = [0.5, 0.6, 0.72, 0.74, 0.76, 0.78, 0.80, 0.82, 0.84, 0.86, 0.88, 0.90, 0.92]

cmva_circle_list = []
cmva = False
#cmva = True

met_list = [40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100, 110]
met = False
#met = True

aJets_list = [3, 4, 5, 6, 7, 8]
aJets = False
aJets = True

aJets_pt_list= [20, 30, 35, 40, 45, 50, 60]
aJets_pt = False
#aJets_pt = True

deltaR_list = [1.4, 1.5, 1.6, 1.7, 1.8]
deltaR = False
#deltaR = True

# ==========================================

# =========== Control Region: Variables ============

h_pt_list = [75, 80, 85, 90, 95, 100, 105, 110, 120] 
h_pt = False
#h_pt = True

h_mass_low_list = [80, 85, 90, 95]
h_mass_high_list = [130, 140, 150, 160, 170]
h_mass = False
#h_mass = True

v_pt_list = [75, 80, 85, 90, 95, 100, 105, 110, 120]
v_pt = False
#v_pt = True

cmva_max_list = [0.7, 0.72, 0.74, 0.78, 0.8, 0.85, 0.898, 0.92, 0.94]
cmva_min_list = [0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56, 0.6, 0.65, 0.7, 0.75, 0.8]
cmva_control = False
cmva_control = True

vh_dphi_list = [2.3, 2.5, 2.7, 2.9, 3.1, 3.3, 3.5]
vh_dphi = False
vh_dphi = True

aJets_list_control = [0, 1, 2, 3, 4, 5]
#aJets = False
#aJets = True

v_mass_low_list = [60, 70, 75, 80]
v_mass_high_list = [90, 100, 105, 110, 115, 120, 130]
v_mass = False
v_mass = True

# ==========================================




print '\n======================== Starting Sig/Bkg Optimiziation ========================'
print '==================================================================================\n'


for channel in channel_list:

    print '============= Looping over channel: ', channel, ' ==============\n'

    if signal:
        
        if jet_pt:
    
            # copy back the original cut file
            os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
    
            # list of regression metrics
            metric_list, stat_list  = [], []
    
            # loop over parmater list
            for param in jet_pt_list:
                
                print '\n\n======================== Starting New jet Pt Loop  ========================'
                print '=============================================================================='
                print '----> Looping over parameter: ', param
                                
                # new jet pt cut string
                new_options = 'jet_pt_'+channel+': Jet_pt[<ZHbb|jet_index>[0]] >'+str(param)+' & Jet_pt[<ZHbb|jet_index>[1]] >'+str(param)+'\n'
                print new_options  
                
                for line in fileinput.input("13TeVconfig/cuts", inplace=True):
        
                    if 'jet_pt_'+channel+':' in line:
        
                        print line.replace(line, new_options),
                        
                    else: print line,
                # end file modification
            
                # Now run the plotter on new option list/modified file
                os.system('./runAll.sh signal_'+channel+'_high_Zpt 13TeV plot')
                
                # get the metric from sb_metric text file
                lines = [line.strip() for line in open('sb_metric.txt')]
                    
                # first entry is s/b metric
                metric_list.append(lines[0])
                
                # second line is # of signal events
                stat_list.append(lines[1])
                                        
            # end paramater loop
    
            # fill accuracy plots
            cStd = TCanvas('cStd')
            cStd.SetGrid()
            
            h1b = TH1F('h1b', 'S/B Optimization: Jet p_{T},    '+channel, len(metric_list), 0, len(metric_list)+1)
            h1b = TH1F('h1b', '', len(metric_list), 0, len(metric_list)+1)
            h1b.SetFillColor(4)
            h1b.SetBarWidth(0.4)
            h1b.SetStats(0)
            h1b.GetYaxis().SetTitle('S/sqrt(B)')
            h1b.GetYaxis().SetTitleOffset(1.4)
            h1b.SetMinimum(0)
            h1b.GetXaxis().SetTitle('Jet p_{T} Lower Limit')
    
            
            for i in range(0, len(metric_list)):
                h1b.Fill(i+1, float(metric_list[i]))
                h1b.GetXaxis().SetBinLabel(i+1, str(jet_pt_list[i])+'('+str(Decimal(str(stat_list[i]))*1)+')')
            
            h1b.Draw('b')
                    
            cStd.SaveAs('../myMacros/plots/sb_optimization/jet_pt_'+channel+'.pdf')
            
            
        # end jet_pt
        # ===================================================================
        
        
        if met:
    
            # copy back the original cut file
            os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
            
            # list of regression metrics
            metric_list, stat_list = [], []
            
            # loop over parmater list
            for param in met_list:
    
                print '\n\n======================== Starting New MET Loop  ========================'
                print '=============================================================================='
                print '----> Looping over parameter: ', param
                
                # new met cut string
                new_options = 'met_signal_'+channel+': met_pt < '+str(param)+'\n'
                print new_options
                
                for line in fileinput.input("13TeVconfig/cuts", inplace=True):
                    
                    if 'met_signal_'+channel+':' in line:
                        
                        print line.replace(line, new_options),
                        
                    else: print line,
                # end file modification
                    
                # Now run the plotter on new option list/modified file
                os.system('./runAll.sh signal_'+channel+'_high_Zpt 13TeV plot')
                    
                # get the metric from sb_metric text file
                lines = [line.strip() for line in open('sb_metric.txt')]
                 
                # first entry is s/b metric
                metric_list.append(lines[0])
                
                # second line is # of signal events
                stat_list.append(lines[1])
    
            # fill accuracy plots
            cStd = TCanvas('cStd')
            cStd.SetGrid()
    
            h1b = TH1F('h1b', 'S/B Optimization: MET,    '+channel, len(metric_list), 0, len(metric_list)+1)
            h1b.SetFillColor(4);
            h1b.SetBarWidth(0.4);
            h1b.SetBarOffset(0.0);
            h1b.SetStats(0);
            h1b.GetYaxis().SetTitle('S/sqrt(B)')
            h1b.GetYaxis().SetTitleOffset(1.4)
            h1b.SetMinimum(0)
            h1b.GetXaxis().SetTitle('MET Upper Limit')
    
            for i in range(0, len(metric_list)):
                h1b.Fill(i+1, float(metric_list[i]))
                h1b.GetXaxis().SetBinLabel(i+1, str(met_list[i])+'('+str(Decimal(str(stat_list[i]))*1)+')')
                h1b.Draw('b')
                
            cStd.SaveAs('../myMacros/plots/sb_optimization/met_'+channel+'.pdf')
    
                                                                                                                
        # end met loop                    
        # =====================================================================
        
        
        if z_mass:
    
            # copy back the original cut file
            os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
    
            # list of regression metrics
            metric_list, stat_list = [], []
    
            window_list =[]
            
            # loop over parmater list
            for low in z_mass_low_list:
    
                for high in z_mass_high_list:
                    
                    window_list.append(str(low)+'_'+str(high))
                
                    print '\n\n======================== Starting New Z mass Loop  ========================'
                    print '=============================================================================='
                    print '----> Looping over parameter: ', low, high
                
                    # new met cut string
                    new_options = 'Zwindow_mass  : V_mass > '+str(low)+' & V_mass < '+str(high)+'\n'
                
                    for line in fileinput.input("13TeVconfig/cuts", inplace=True):
                        
                        if 'Zwindow_mass  :' in line:
                        
                            print line.replace(line, new_options),
                        
                        else: print line,
                    # end file modification
                    
                    # Now run the plotter on new option list/modified file
                    os.system('./runAll.sh signal_'+channel+'_high_Zpt 13TeV plot')
                    
                    # get the metric from sb_metric text file
                    lines = [line.strip() for line in open('sb_metric.txt')]
    
                    # first entry is s/b metric
                    metric_list.append(lines[0])
                    
                    # second line is # of signal events
                    stat_list.append(lines[1])
    
            # end param loop
    
            # fill accuracy plots
            cStd = TCanvas('cStd')
            cStd.SetGrid()
            
            h1b = TH1F('h1b', 'S/B Optimization: Z Mass Window,    '+channel, len(metric_list), 0, len(metric_list)+1)
            h1b.SetFillColor(4);
            h1b.SetBarWidth(0.4);
            h1b.SetBarOffset(0.0);
            h1b.SetStats(0);
            h1b.GetYaxis().SetTitle('S/sqrt(B)')
            h1b.GetYaxis().SetTitleOffset(1.4)
            h1b.SetMinimum(0)
            h1b.GetXaxis().SetTitle('Z mass window')
            
            for i in range(0, len(metric_list)):
                h1b.Fill(i+1, float(metric_list[i]))
                h1b.GetXaxis().SetBinLabel(i+1, window_list[i]+'('+str(Decimal(str(stat_list[i]))*1)+')')
                h1b.Draw('b')
                
            cStd.SaveAs('../myMacros/plots/sb_optimization/z_mass_'+channel+'.pdf')
    
        # end z_mass
        # ===================================================================
                
    
        if cmva:
    
            for jet in range(0,2):
    
                # copy back the original cut file
                os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
                
                # list of regression metrics
                metric_list, stat_list  = [], []
            
                # loop over parmater list
                for param in cmva_list:
                
                    print '\n\n======================== Starting New CMVA Loop  ========================'
                    print '=============================================================================='
                    print '----> Looping over parameter: ', param
                    
                    # new jet pt cut string
                    if jet == 0:
                        new_options = 'cmvaBtag_'+channel+': Jet_btagCMVA[<ZHbb|jet_index>[0]] > '+str(param)+' & Jet_btagCMVA[<ZHbb|jet_index>[1]] > 0.7\n'
                    else:
                        new_options = 'cmvaBtag_'+channel+': Jet_btagCMVA[<ZHbb|jet_index>[0]] > 0.76 & Jet_btagCMVA[<ZHbb|jet_index>[1]] > '+str(param)+'\n'
    
                    print new_options
                
                    for line in fileinput.input("13TeVconfig/cuts", inplace=True):
                        
                        if 'cmvaBtag_'+channel+':' in line:
                            
                            print line.replace(line, new_options),
                            
                        else: print line,
                    # end file modification
                    
                    # Now run the plotter on new option list/modified file
                    os.system('./runAll.sh signal_'+channel+'_high_Zpt 13TeV plot')
                    
                    # get the metric from sb_metric text file
                    lines = [line.strip() for line in open('sb_metric.txt')]
                    
                    # first entry is s/b metric
                    metric_list.append(lines[0])
                    
                    # second line is # of signal events
                    stat_list.append(lines[1])
                    
                # end param loop
                    
                # fill accuracy plots
                cStd = TCanvas('cStd')
                cStd.SetGrid()
                
                h1b = TH1F('h1b', 'S/B Optimization: CMVA Jet '+str(jet+1)+',    '+channel, len(metric_list), 0, len(metric_list)+1)
                h1b.SetFillColor(4);
                h1b.SetBarWidth(0.4);
                h1b.SetBarOffset(0.0);
                h1b.SetStats(0);
                h1b.GetYaxis().SetTitle('S/sqrt(B)')
                h1b.GetYaxis().SetTitleOffset(1.4)
                h1b.SetMinimum(0)
                h1b.GetXaxis().SetTitle('CMVA Lower Limit')
                
                for i in range(0, len(metric_list)):
                    h1b.Fill(i+1, float(metric_list[i]))
                    h1b.GetXaxis().SetBinLabel(i+1, str(cmva_list[i]))
                    h1b.Draw('b')
                    
                cStd.SaveAs('../myMacros/plots/sb_optimization/cmva_jet'+str(jet)+'_'+channel+'.pdf')
    
            # end jet loop
    
        # end cmva
        # ===================================================================
                    
        
    
        if aJets:
    
            # copy back the original cut file
            os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
    
            # list of regression metrics
            metric_list, stat_list  = [], []
            
            # loop over parmater list
            for param in aJets_list:
                
                print '\n\n======================== Starting New aJets Loop  ========================'
                print '=============================================================================='
                print '----> Looping over parameter: ', param
                
                # new jet pt cut string
                #new_options = 'noAddJet: nJet == '+str(param)+'\n'
                new_options = 'noAddJet: Sum$(Jet_pt > 20 & abs(Jet_eta) < 2.4) < '+str(param)+'\n'
                print new_options  
                
                for line in fileinput.input("13TeVconfig/cuts", inplace=True):
                    
                    if 'noAddJet:' in line:
                        
                        print line.replace(line, new_options),
                        
                    else: print line,
                # end file modification
                    
                # Now run the plotter on new option list/modified file
                os.system('./runAll.sh signal_'+channel+'_high_Zpt 13TeV plot')
                
                # get the metric from sb_metric text file
                lines = [line.strip() for line in open('sb_metric.txt')]
                
                # first entry is s/b metric
                metric_list.append(lines[0])
                
                # second line is # of signal events
                stat_list.append(lines[1])
                
            # end paramater loop
                
            # fill accuracy plots
            cStd = TCanvas('cStd')
            cStd.SetGrid()
            
            h1b = TH1F('h1b', 'S/B Optimization: aJets,    '+channel, len(metric_list), 0, len(metric_list)+1)
            h1b.SetFillColor(4)
            h1b.SetBarWidth(0.4)
            h1b.SetBarOffset(0.0)
            h1b.SetStats(0)
            h1b.GetYaxis().SetTitle('S/sqrt(B)')
            h1b.GetYaxis().SetTitleOffset(1.4)
            h1b.SetMinimum(0)
            h1b.GetXaxis().SetTitle('# aJets')
            
            for i in range(0, len(metric_list)):
                h1b.Fill(i+1, float(metric_list[i]))
                h1b.GetXaxis().SetBinLabel(i+1, str(aJets_list[i])+'('+str(Decimal(str(stat_list[i]))*1)+')')
                h1b.Draw('b')
                
            cStd.SaveAs('../myMacros/plots/sb_optimization/aJets_'+channel+'.pdf')
    
                
        # end ajets
        # ===================================================================
            

        if aJets_pt:
    
            # copy back the original cut file
            os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
    
            # list of regression metrics
            metric_list, stat_list  = [], []
            
            # loop over parmater list
            for param in aJets_list:
                
                print '\n\n======================== Starting New aJets Pt Loop  ========================'
                print '=============================================================================='
                print '----> Looping over parameter: ', param
                
                # new jet pt cut string
                new_options = 'noAddJet: Sum$(Jet_pt > '+str(param)+' & abs(Jet_eta) < 2.4) < 3\n'
                print new_options  
                
                for line in fileinput.input("13TeVconfig/cuts", inplace=True):
                    
                    if 'noAddJet:' in line:
                        
                        print line.replace(line, new_options),
                        
                    else: print line,
                # end file modification
                    
                # Now run the plotter on new option list/modified file
                os.system('./runAll.sh signal_'+channel+'_high_Zpt 13TeV plot')
                
                # get the metric from sb_metric text file
                lines = [line.strip() for line in open('sb_metric.txt')]
                
                # first entry is s/b metric
                metric_list.append(lines[0])
                
                # second line is # of signal events
                stat_list.append(lines[1])
                
            # end paramater loop
                
            # fill accuracy plots
            cStd = TCanvas('cStd')
            cStd.SetGrid()
            
            h1b = TH1F('h1b', 'S/B Optimization: aJets Pt,    '+channel, len(metric_list), 0, len(metric_list)+1)
            h1b.SetFillColor(4)
            h1b.SetBarWidth(0.4)
            h1b.SetBarOffset(0.0)
            h1b.SetStats(0)
            h1b.GetYaxis().SetTitle('S/sqrt(B)')
            h1b.GetYaxis().SetTitleOffset(1.4)
            h1b.SetMinimum(0)
            h1b.GetXaxis().SetTitle('aJets Pt')
            
            for i in range(0, len(metric_list)):
                h1b.Fill(i+1, float(metric_list[i]))
                h1b.GetXaxis().SetBinLabel(i+1, str(aJets_list[i])+'('+str(Decimal(str(stat_list[i]))*1)+')')
                h1b.Draw('b')
                
            cStd.SaveAs('../myMacros/plots/sb_optimization/aJets_pt_'+channel+'.pdf')
    
                
        # end ajets pt
        # ===================================================================

        
    
        if deltaR:
            
            # copy back the original cut file
            os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
    
            # list of regression metrics
            metric_list, stat_list  = [], []
            
            # loop over parmater list
            for param in deltaR_list:
                
                print '\n\n======================== Starting New deltaR Loop  ========================'
                print '=============================================================================='
                print '----> Looping over parameter: ', param
                
                # new jet pt cut string
                new_options = 'deltaRjj_'+channel+': deltaR_jj < '+str(param)+'\n'
                print new_options 
                
                for line in fileinput.input("13TeVconfig/cuts", inplace=True):
                    
                    if 'deltaRjj_'+channel+':' in line:
                        
                        print line.replace(line, new_options),
                        
                    else: print line,
                # end file modification
                    
                # Now run the plotter on new option list/modified file
                os.system('./runAll.sh signal_'+channel+'_high_Zpt 13TeV plot')
                
                # get the metric from sb_metric text file
                lines = [line.strip() for line in open('sb_metric.txt')]
                
                # first entry is s/b metric
                metric_list.append(lines[0])
                
                # second line is # of signal events
                stat_list.append(lines[1])
                
            # end paramater loop
                
            # fill accuracy plots
            cStd = TCanvas('cStd')
            cStd.SetGrid()
            
            h1b = TH1F('h1b', 'S/B Optimization: Delta R(jj),    '+channel, len(metric_list), 0, len(metric_list)+1)
            h1b.SetFillColor(4)
            h1b.SetBarWidth(0.4)
            h1b.SetBarOffset(0.0)
            h1b.SetStats(0)
            h1b.GetYaxis().SetTitle('S/sqrt(B)')
            h1b.GetYaxis().SetTitleOffset(1.4)
            h1b.SetMinimum(0)
            h1b.GetXaxis().SetTitle('deltaR(jj) Lower Limit')
            
            for i in range(0, len(metric_list)):
                h1b.Fill(i+1, float(metric_list[i]))
                h1b.GetXaxis().SetBinLabel(i+1, str(deltaR_list[i])+'('+str(Decimal(str(stat_list[i]))*1)+')')
                h1b.Draw('b')
                
            cStd.SaveAs('../myMacros/plots/sb_optimization/deltaR_'+channel+'.pdf')
    
                
        # end deltaR
        # ===================================================================
            
    
    
    
    
    
    # ==================================================================================================
    # end signal loop
    
    
    if control:
        
        if h_pt:
            
            # loop over backgrounds
            for bkg in bkg_list:
    
                print '\n============================ Background: ', bkg,'=================================='
            
                # copy back the original cut file
                os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
    
                # list of regression metrics
                metric_list, stat_list  = [], []
            
                # loop over parmater list
                for param in h_pt_list:
                
                    print '\n\n======================== Starting New h_pt Loop  ========================'
                    print '=========================================================================='
                    print '----> Looping over parameter: ', param
                
                    # new jet pt cut string
                    if bkg != 'Zhf': new_options = 'Hpt_100: H_pt > '+str(param)+'\n'
                    else: new_options = 'Hpt_Zhf: H_pt > '+str(param)+'\n'
                    print new_options   
                
                    for line in fileinput.input("13TeVconfig/cuts", inplace=True):
                    
                        if bkg != 'Zhf':
                            if 'Hpt_100:' in line:
                                print line.replace(line, new_options),
                            else: print line,
    
                        else:
                            if 'Hpt_Zhf:' in line:
                                print line.replace(line, new_options),
                            else: print line,
    
                    # end file modification
                    
                    # Now run the plotter on new option list/modified file
                    os.system('./runAll.sh '+bkg+'_'+channel+' 13TeV plot')
                    
                    # get the metric from sb_metric text file
                    lines = [line.strip() for line in open(bkg+'_metric.txt')]
                    
                    # first entry is s/b metric
                    metric_list.append(lines[0])
                    
                # end paramater loop
                
                # fill accuracy plots
                cStd = TCanvas('cStd')
                cStd.SetGrid()
            
                h1b = TH1F('h1b', 'Control Region Optimization: H p_{T} Lower Limit,    '+bkg+'_'+channel, len(metric_list), 0, len(metric_list)+1)
                h1b.SetFillColor(4)
                h1b.SetBarWidth(0.4)
                h1b.SetBarOffset(0.0)
                h1b.SetStats(0)
                h1b.GetYaxis().SetTitle(bkg+'/bkgs')
                h1b.GetYaxis().SetTitleOffset(1.4)
                h1b.SetMinimum(0)
                h1b.GetXaxis().SetTitle('H p_{T}')
                
                for i in range(0, len(metric_list)):
                    h1b.Fill(i+1, float(metric_list[i]))
                    h1b.GetXaxis().SetBinLabel(i+1, str(h_pt_list[i]))
                    h1b.Draw('b')
                
                cStd.SaveAs('../myMacros/plots/sb_optimization/'+bkg+'_'+channel+'_hPt.pdf')
    
            # end background loop
            
        # end H pt
        # ===================================================================
    
        if v_pt:
            
            # loop over backgrounds
            for bkg in bkg_list:
    
                # only LF matters here
    
                if bkg != 'Zlf': continue
                
                print '\n============================ Background: ', bkg,'=================================='
            
                # copy back the original cut file
                os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
    
                # list of regression metrics
                metric_list, stat_list  = [], []
            
                # loop over parmater list
                for param in h_pt_list:
                
                    print '\n\n======================== Starting New V_pt Loop  ========================'
                    print '=========================================================================='
                    print '----> Looping over parameter: ', param
                    
                    # new jet pt cut string
                    if bkg == 'Zlf': new_options = 'Vpt_100: V_pt > '+str(param)+'\n'
                    if bkg == 'Zhf': new_options = 'Vpt_Zhf: V_pt > '+str(param)+'\n'
                    if bkg == 'ttbar': new_options = 'Vpt_ttbar: V_pt > '+str(param)+'\n'
                    print new_options  
                
                    for line in fileinput.input("13TeVconfig/cuts", inplace=True):
    
                        if bkg =='Zlf':
                            if 'Vpt_100:' in line:
                                print line.replace(line, new_options),
                            else: print line,
                            
                        if bkg =='Zhf':
                            if 'Vpt_Zhf:' in line:
                                print line.replace(line, new_options),
                            else: print line,
    
                        if bkg =='ttbar':
                            if 'Vpt_ttbar:' in line:
                                print line.replace(line, new_options),
                            else: print line,
    
                    # end file modification
                    
                    # Now run the plotter on new option list/modified file
                    os.system('./runAll.sh '+bkg+'_'+channel+' 13TeV plot')
                
                    # get the metric from sb_metric text file
                    lines = [line.strip() for line in open(bkg+'_metric.txt')]
                    
                    # first entry is s/b metric
                    metric_list.append(lines[0])
                    
                # end paramater loop
                
                # fill accuracy plots
                cStd = TCanvas('cStd')
                cStd.SetGrid()
            
                h1b = TH1F('h1b', 'Control Region Optimization: V p_{T} Lower Limit,    '+bkg+'_'+channel, len(metric_list), 0, len(metric_list)+1)
                h1b.SetFillColor(4)
                h1b.SetBarWidth(0.4)
                h1b.SetBarOffset(0.0)
                h1b.SetStats(0)
                h1b.GetYaxis().SetTitle(bkg+'/bkgs')
                h1b.GetYaxis().SetTitleOffset(1.4)
                h1b.SetMinimum(0)
                h1b.GetXaxis().SetTitle('V p_{T}')
                
                for i in range(0, len(metric_list)):
                    h1b.Fill(i+1, float(metric_list[i]))
                    h1b.GetXaxis().SetBinLabel(i+1, str(v_pt_list[i]))
                    h1b.Draw('b')
                
                cStd.SaveAs('../myMacros/plots/sb_optimization/'+bkg+'_'+channel+'_vPt.pdf')
    
            # end background loop
            
        # end V pt
        # ===================================================================
    
        if vh_dphi:
            
            # loop over backgrounds
            for bkg in bkg_list:
    
                # only LF and HF matters here
    
                if bkg == 'ttbar': continue
                
                print '\n============================ Background: ', bkg,'=================================='
            
                # copy back the original cut file
                os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
    
                # list of regression metrics
                metric_list, stat_list  = [], []
            
                # loop over parmater list
                for param in vh_dphi_list:
                
                    print '\n\n======================== Starting New VH dphi Loop  ========================'
                    print '=========================================================================='
                    print '----> Looping over parameter: ', param
                    
                    # new jet pt cut string
                    new_options = 'dPhiVH: abs( HVdPhi ) > '+str(param)+'\n'
                    print new_options  
                
                    for line in fileinput.input("13TeVconfig/cuts", inplace=True):
                    
                        if 'dPhiVH:' in line:
                        
                            print line.replace(line, new_options),
                            
                        else: print line,
                    # end file modification
                    
                    # Now run the plotter on new option list/modified file
                    os.system('./runAll.sh '+bkg+'_'+channel+' 13TeV plot')
                
                    # get the metric from sb_metric text file
                    lines = [line.strip() for line in open(bkg+'_metric.txt')]
                    
                    # first entry is s/b metric
                    metric_list.append(lines[0])
                    
                # end paramater loop
                
                # fill accuracy plots
                cStd = TCanvas('cStd')
                cStd.SetGrid()
            
                h1b = TH1F('h1b', 'Control Region Optimization: dPhi(VH) Lower Limit,    '+bkg+'_'+channel, len(metric_list), 0, len(metric_list)+1)
                h1b.SetFillColor(4)
                h1b.SetBarWidth(0.4)
                h1b.SetBarOffset(0.0)
                h1b.SetStats(0)
                h1b.GetYaxis().SetTitle(bkg+'/bkgs')
                h1b.GetYaxis().SetTitleOffset(1.4)
                h1b.SetMinimum(0)
                h1b.GetXaxis().SetTitle('dPhi(VH)')
                
                for i in range(0, len(metric_list)):
                    h1b.Fill(i+1, float(metric_list[i]))
                    h1b.GetXaxis().SetBinLabel(i+1, str(vh_dphi_list[i]))
                    h1b.Draw('b')
                
                cStd.SaveAs('../myMacros/plots/sb_optimization/'+bkg+'_'+channel+'_VHdphi.pdf')
    
            # end background loop
            
        # end VH dphi
        # ===================================================================
        
        if h_mass:
            
            # loop over backgrounds
            for bkg in bkg_list:
    
                # only LF and HF matters here
                
                if bkg != 'Zhf': continue
                
                print '\n============================ Background: ', bkg,'=================================='
            
                # copy back the original cut file
                os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
    
                # list of regression metrics
                metric_list, stat_list  = [], []
    
                window_list =[]        
    
                # loop over parmater list
                for h_low in h_mass_low_list:
                            
                    for h_high in h_mass_high_list:
                                
                        window_list.append(str(h_low)+'_'+str(h_high))
                
                        print '\n\n======================== Starting New H mass Loop  ========================'
                        print '=========================================================================='
                        print '----> Looping over parameter: ', param
                    
                        # new jet pt cut string
                        new_options = 'vetoHmass: (H_mass < '+str(h_low)+' | H_mass > '+str(h_high)+')\n'
                        print new_options  
                
                        for line in fileinput.input("13TeVconfig/cuts", inplace=True):
                    
                            if 'vetoHmass:' in line:
                        
                                print line.replace(line, new_options),
                            
                            else: print line,
                        # end file modification
                    
                        # Now run the plotter on new option list/modified file
                        os.system('./runAll.sh '+bkg+'_'+channel+' 13TeV plot')
                
                        # get the metric from sb_metric text file
                        lines = [line.strip() for line in open(bkg+'_metric.txt')]
                    
                        # first entry is s/b metric
                        metric_list.append(lines[0])
                    
                # end paramater loop
                
                # fill accuracy plots
                cStd = TCanvas('cStd')
                cStd.SetGrid()
            
                h1b = TH1F('h1b', 'Control Region Optimization: H Mass Window,    '+bkg+'_'+channel, len(metric_list), 0, len(metric_list)+1)
                h1b.SetFillColor(4)
                h1b.SetBarWidth(0.4)
                h1b.SetBarOffset(0.0)
                h1b.SetStats(0)
                h1b.GetYaxis().SetTitle(bkg+'/bkgs')
                h1b.GetYaxis().SetTitleOffset(1.4)
                h1b.SetMinimum(0)
                h1b.GetXaxis().SetTitle('M_{jj}')
                
                for i in range(0, len(metric_list)):
                    h1b.Fill(i+1, float(metric_list[i]))
                    h1b.GetXaxis().SetBinLabel(i+1, window_list[i])
                    h1b.Draw('b')
                
                cStd.SaveAs('../myMacros/plots/sb_optimization/'+bkg+'_'+channel+'_Hmass.pdf')
    
            # end background loop
            
        # end H mass
        # ===================================================================
        
        if cmva_control:
    
            # loop over backgrounds
            for bkg in bkg_list:
    
                print '\n============================ Background: ', bkg,'=================================='
                
                # copy back the original cut file
                os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
    
                # list of regression metrics
                metric_list, stat_list  = [], []
    
                # loop over parmater list
                for param in cmva_max_list:
                            
                    print '\n\n======================== Starting New CMVA Max Loop  ========================'
                    print '=========================================================================='
                    print '----> Looping over parameter: ', param
                    
                    # new jet pt cut string
                    new_options = 'maxBtag_test: max(hJets_btagCMVA[0],hJets_btagCMVA[1]) > '+str(param)+'\n'
                    print new_options  
                
                    for line in fileinput.input("13TeVconfig/cuts", inplace=True):
                    
                        if 'maxBtag_test:' in line:
                        
                            print line.replace(line, new_options),
                            
                        else: print line,
                    # end file modification
                    
                    # Now run the plotter on new option list/modified file
                    os.system('./runAll.sh '+bkg+'_'+channel+' 13TeV plot')
                
                    # get the metric from sb_metric text file
                    lines = [line.strip() for line in open(bkg+'_metric.txt')]
                    
                    # first entry is s/b metric
                    metric_list.append(lines[0])
                    
                # end paramater loop
                
                # fill accuracy plots
                cStd = TCanvas('cStd')
                cStd.SetGrid()
            
                h1b = TH1F('h1b', 'Control Region Optimization: CMVA Max,    '+bkg+'_'+channel, len(metric_list), 0, len(metric_list)+1)
                h1b.SetFillColor(4)
                h1b.SetBarWidth(0.4)
                h1b.SetBarOffset(0.0)
                h1b.SetStats(0)
                h1b.GetYaxis().SetTitle(bkg+'/bkgs')
                h1b.GetYaxis().SetTitleOffset(1.4)
                h1b.SetMinimum(0)
                h1b.GetXaxis().SetTitle('CMVA')
                
                for i in range(0, len(metric_list)):
                    h1b.Fill(i+1, float(metric_list[i]))
                    h1b.GetXaxis().SetBinLabel(i+1, str(cmva_max_list[i]))
                    h1b.Draw('b')
                
                cStd.SaveAs('../myMacros/plots/sb_optimization/'+bkg+'_'+channel+'_maxCMVA.pdf')
    
    
                # now loop over CMVA min
                
                # copy back the original cut file
                os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
    
                # list of regression metrics
                metric_list, stat_list  = [], []
    
                # loop over parmater list
                for param in cmva_min_list:
                            
                    print '\n\n======================== Starting New CMVA Min Loop  ========================'
                    print '=========================================================================='
                    print '----> Looping over parameter: ', param
                    
                    # new jet pt cut string
                    new_options = 'minBtag_test: min(hJets_btagCMVA[0],hJets_btagCMVA[1]) > '+str(param)+'\n'
                    print new_options  
                
                    for line in fileinput.input("13TeVconfig/cuts", inplace=True):
                    
                        if 'minBtag_test:' in line:
                        
                            print line.replace(line, new_options),
                            
                        else: print line,
                    # end file modification
                    
                    # Now run the plotter on new option list/modified file
                    os.system('./runAll.sh '+bkg+'_'+channel+' 13TeV plot')
                
                    # get the metric from sb_metric text file
                    lines = [line.strip() for line in open(bkg+'_metric.txt')]
                    
                    # first entry is s/b metric
                    metric_list.append(lines[0])
                    
                # end paramater loop
                
                # fill accuracy plots
                cStd = TCanvas('cStd')
                cStd.SetGrid()
            
                h1b = TH1F('h1b', 'Control Region Optimization: CMVA Min,    '+bkg+'_'+channel, len(metric_list), 0, len(metric_list)+1)
                h1b.SetFillColor(4)
                h1b.SetBarWidth(0.4)
                h1b.SetBarOffset(0.0)
                h1b.SetStats(0)
                h1b.GetYaxis().SetTitle(bkg+'/bkgs')
                h1b.GetYaxis().SetTitleOffset(1.4)
                h1b.SetMinimum(0)
                h1b.GetXaxis().SetTitle('CMVA')
                
                for i in range(0, len(metric_list)):
                    h1b.Fill(i+1, float(metric_list[i]))
                    h1b.GetXaxis().SetBinLabel(i+1, str(cmva_min_list[i]))
                    h1b.Draw('b')
                
                cStd.SaveAs('../myMacros/plots/sb_optimization/'+bkg+'_'+channel+'_minCMVA.pdf')
    
            # end background loop
            
        # end H mass
        # ===================================================================
        
        if aJets:
            
            # loop over backgrounds
            for bkg in bkg_list:
    
                print '\n============================ Background: ', bkg,'=================================='
            
                # copy back the original cut file
                os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
    
                # list of regression metrics
                metric_list, stat_list  = [], []
            
                # loop over parmater list
                for param in aJets_list:
                
                    print '\n\n======================== Starting New aJets Loop  ========================'
                    print '=========================================================================='
                    print '----> Looping over parameter: ', param
                    
                    # new jet pt cut string
                    if bkg == 'Zlf'  : new_options = 'aJets_Zlf: naJets == '+str(param)+'\n'
                    if bkg == 'Zhf'  : new_options = 'aJets_Zhf: naJets == '+str(param)+'\n'
                    if bkg == 'ttbar': new_options = 'aJets_ttbar: naJets == '+str(param)+'\n'
                    print new_options  
                
                    for line in fileinput.input("13TeVconfig/cuts", inplace=True):
    
                        if bkg == 'Zlf':
                            if 'aJets_Zlf::' in line:
                                print line.replace(line, new_options),
                            else: print line,
    
                        if bkg == 'Zhf':
                            if 'aJets_Zhf:' in line:
                                print line.replace(line, new_options),
                            else: print line,
                            
                        if bkg == 'ttbar':
                            if 'aJets_ttbar:' in line:
                                print line.replace(line, new_options),
                            else: print line,
    
                    # end file modification
                    
                    # Now run the plotter on new option list/modified file
                    os.system('./runAll.sh '+bkg+'_'+channel+' 13TeV plot')
                
                    # get the metric from sb_metric text file
                    lines = [line.strip() for line in open(bkg+'_metric.txt')]
                    
                    # first entry is s/b metric
                    metric_list.append(lines[0])
                    
                # end paramater loop
                
                # fill accuracy plots
                cStd = TCanvas('cStd')
                cStd.SetGrid()
            
                h1b = TH1F('h1b', 'Control Region Optimization: Additional Jets,    '+bkg+'_'+channel, len(metric_list), 0, len(metric_list)+1)
                h1b.SetFillColor(4)
                h1b.SetBarWidth(0.4)
                h1b.SetBarOffset(0.0)
                h1b.SetStats(0)
                h1b.GetYaxis().SetTitle(bkg+'/bkgs')
                h1b.GetYaxis().SetTitleOffset(1.4)
                h1b.SetMinimum(0)
                h1b.GetXaxis().SetTitle('# aJets')
                
                for i in range(0, len(metric_list)):
                    h1b.Fill(i+1, float(metric_list[i]))
                    h1b.GetXaxis().SetBinLabel(i+1, str(aJets_list[i]))
                    h1b.Draw('b')
                
                cStd.SaveAs('../myMacros/plots/sb_optimization/'+bkg+'_'+channel+'_aJets.pdf')
    
            # end background loop
            
        # end aJets
        # ===================================================================
    
        if v_mass:
            
            # loop over backgrounds
            for bkg in bkg_list:
    
                print '\n============================ Background: ', bkg,'=================================='
            
                # copy back the original cut file
                os.system('cp 13TeVconfig/old_cuts 13TeVconfig/cuts')
    
                # list of regression metrics
                metric_list, stat_list  = [], []
    
                window_list =[]        
    
                # loop over parmater list
                for v_low in v_mass_low_list:
                            
                    for v_high in v_mass_high_list:
                                
                        window_list.append(str(v_low)+'_'+str(v_high))
                
                        print '\n\n======================== Starting New V mass Loop  ========================'
                        print '=========================================================================='
                        print '----> Looping over parameter: ', v_low, v_high
                    
                        # new jet pt cut string
                        if bkg == 'ttbar': new_options = 'vetoVmass: (V_mass < '+str(v_low)+' | V_mass > '+str(v_high)+')\n'
                        else:              new_options = 'Zwindow_mass  : V_mass > '+str(v_low)+' & V_mass < '+str(v_high)+'\n'
    
                        print new_options   
                
                        for line in fileinput.input("13TeVconfig/cuts", inplace=True):
                    
                            if bkg == 'ttbar':
                                if 'vetoHmass:' in line:
                                                            
                                    print line.replace(line, new_options),
                            
                                else: print line,
    
                            else:
                                if 'Zwindow_mass  :' in line:
    
                                    print line.replace(line, new_options),
    
                                else: print line,
                        # end file modification
                    
                        # Now run the plotter on new option list/modified file
                        os.system('./runAll.sh '+bkg+'_'+channel+' 13TeV plot')
                
                        # get the metric from sb_metric text file
                        lines = [line.strip() for line in open(bkg+'_metric.txt')]
                    
                        # first entry is s/b metric
                        metric_list.append(lines[0])
                    
                # end paramater loop
                
                # fill accuracy plots
                cStd = TCanvas('cStd')
                cStd.SetGrid()
            
                h1b = TH1F('h1b', 'Control Region Optimization: V Mass Window,    '+bkg+'_'+channel, len(metric_list), 0, len(metric_list)+1)
                h1b.SetFillColor(4)
                h1b.SetBarWidth(0.4)
                h1b.SetBarOffset(0.0)
                h1b.SetStats(0)
                h1b.GetYaxis().SetTitle(bkg+'/bkgs')
                h1b.GetYaxis().SetTitleOffset(1.4)
                h1b.SetMinimum(0)
                h1b.GetXaxis().SetTitle('M_{ll}')
                
                for i in range(0, len(metric_list)):
                    h1b.Fill(i+1, float(metric_list[i]))
                    h1b.GetXaxis().SetBinLabel(i+1, window_list[i])
                    h1b.Draw('b')
                
                cStd.SaveAs('../myMacros/plots/sb_optimization/'+bkg+'_'+channel+'_Vmass.pdf')
    
            # end background loop
            
        # end V mass
        # ===================================================================
    
    # ==================================================================================================
    # end control loop

# end channel loop        

raw_input('press return to continue')
