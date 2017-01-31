# ===================================================
# Python script to perform BDT Classification Optimization
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


# Define list of training features

training_variables = [
    '',
    'HCSV_reg_mass ',
    'HCSV_reg_pt ',
    'HVdPhi ',
    'V_mass ',
    'V_pt ',
    #'max(hJet_pt[0],hJet_pt[1]) ',
    #'min(hJet_pt[0],hJet_pt[1]) ',
    'deltaR_jj ',
    'hJet_pt[0] ',
    'hJet_pt[1] ',
    'Sum$(Jet_pt>20.&abs(Jet_eta)<2.4&Jet_puId>0.) ',
    'HCSV_dEta ',
    'HCSV_dR ',
    'met_pt ',
    'hJet_btagCSV[0] ',
    'hJet_btagCSV[1] ',
    '(HCSV_reg_pt/V_pt)'
    ]



# Define full training line
full_list = 'Nominal: HCSV_reg_mass HCSV_reg_pt HVdPhi HCSV_dEta HCSV_dR met_pt hJet_btagCSV[0] hJet_btagCSV[1] hJet_pt[0] hJet_pt[1] V_mass Sum$(Jet_pt>20.&abs(Jet_eta)<2.4&Jet_puId>0.) deltaR_jj V_pt (HCSV_reg_pt/V_pt)'
 


# ===== Perform n-1 feature optimization =====

# list of regression metrics
metric_list  = []

# loop over training features
for variable in training_variables:

    # testing
    #break

    print '\n\n======================== Starting New Feature Loop  ========================'
    print '----> Removing Feature: ', variable

    # clear the temp files from last datacard iteration
    os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')

    # new BDT option string.  Remove current feature from training list
    if variable == 'V_pt': 
        new_line = 'Nominal: HCSV_reg_mass HCSV_reg_pt HVdPhi HCSV_dEta HCSV_dR met_pt hJet_btagCSV[0] hJet_btagCSV[1] V_mass Sum$(Jet_pt>20.&abs(Jet_eta)<2.4&Jet_puId>0.) deltaR_jj hJet_pt[0] hJet_pt[1] (HCSV_reg_pt/V_pt)'

    elif variable == 'HCSV_reg_pt':
        new_line = 'Nominal: HCSV_reg_mass HVdPhi HCSV_dEta HCSV_dR met_pt hJet_btagCSV[0] hJet_btagCSV[1] V_mass Sum$(Jet_pt>20.&abs(Jet_eta)<2.4&Jet_puId>0.) deltaR_jj V_pt hJet_pt[0] hJet_pt[1] (HCSV_reg_pt/V_pt)'
    
    else: new_line = full_list.replace(variable, '')
    
    print '----> New Training List: ', new_line

    for line in fileinput.input("13TeVconfig/training", inplace=True):
        
        if 'Nominal:' in line:
            
            print line.replace(line, new_line),
            
        else: print line,
    # end file modification
        
    # Now train the BDT on new option list/ modified file
    os.system('python ../myMacros/classification/bdt_classifier_training_loop.py')

    char_list = ['(', ')', '[', ']', '&', '>', '<', '/', '.', '$', ',', ' ']
    temp_var = variable
    for char in char_list: 
        temp_var = temp_var.replace(char, '')
    

    # Copy the MVA outfile for each iteration for plots later
    tfile = 'cp ../data/MVA_gg_plus_ZH125_highZpt.root ../data/optimization/MVA_gg_plus_ZH125_highZpt_'+temp_var+'.root'
    os.system(tfile)
    
    # Apply the BDT weights to samples
    os.system('python ../myMacros/classification/bdt_classifier_eval_loop.py')

    # Make the datacards for new training
    # Set datacard output directory to current var name
    new_dir = "dir = '3_2_BDT_v1"+temp_var+"'\n"

    for line in fileinput.input('../myMacros/classification/dataCard_loop.py', inplace=True):

        if 'dir =' in line:

            print line.replace(line, new_dir),

        else: print line,
    # end file modification

    os.system('python ../myMacros/classification/dataCard_loop.py')

    # Get the metric of success for each parameter iteration
    # put each iterations metric in a plot

    if os.path.isfile('cls_expected.txt'):
        os.system('rm cls_expected.txt')

    #output = subprocess.check_output(['python', '../myMacros/simple_regression_HistMaker.py'])
    
    # CLs Median expected limit
    t6 = "combine -M Asymptotic -t -1 ../limits/3_2_BDT_v1"+temp_var+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"  
    os.system(t6)
    
    # get the 50% limit
    for line in fileinput.input("cls_expected.txt", inplace=True):

        if 'Expected 50.0%:' in line:

            metric = line.replace('Expected 50.0%: r < ', '') 

    print 'metric: ', metric      

    metric_list.append(float(metric))

# end feature loop


# For plot making
#metric_list = [5.2344, 6.4062, 5.2969, 5.2344, 5.2969, 5.3281, 5.2656, 5.2031, 5.2031, 5.2344, 5.2344, 5.3906, 5.2969, 5.3906, 5.4219, 5.3281, 8.5312, 5.2344]

print metric_list

# Nornalize list to first entry
norm = metric_list[0]
norm_metric_list = [x / norm for x in metric_list]

#print 'norm:', norm_metric_list

# fill accuracy plots
cStd = TCanvas('cStd')
cStd.SetGrid()

h1b = TH1F('h1b', 'BDT Training Variable N-1 Optimization', len(training_variables), 0, len(training_variables)+1)
h1b.SetFillColor(4);
h1b.SetBarWidth(0.4);
h1b.SetBarOffset(0.0);
h1b.SetStats(0);
h1b.GetYaxis().SetTitle('Cls Expected 50%')
#h1b.GetXaxis().SetTitle('Training Variables')
#h1b.SetMinimum(10);
#h1b.SetMaximum(20);

for i in range(0, len(training_variables)):
    #print 'metric:', metric_list[i]
    h1b.Fill(i+1, metric_list[i])
    h1b.GetXaxis().SetBinLabel(i+1, training_variables[i])
    
    if i == 0:
         h1b.GetXaxis().SetBinLabel(i+1, 'All Variables')
    
    h1b.Draw('b')
    
cStd.SaveAs('../myMacros/classification/bdt_optimization_plots/training_vars.pdf')

# Now one for normalized entries
cN = TCanvas('cN')
#cN.SetGrid()
hN = TH1F('hN', 'BDT Training Variable N-1 Optimization', len(training_variables), 0, len(training_variables)+1)
hN.SetStats(0);
hN.GetYaxis().SetTitle('Cls Expected 50%(Normalized to All Variables)')
hN.GetXaxis().SetTitle('Training Variables')

for i in range(0, len(training_variables)):
    hN.Fill(i+1, norm_metric_list[i])
    hN.GetXaxis().SetBinLabel(i+1, training_variables[i])
    
    if i == 0:
         hN.GetXaxis().SetBinLabel(i+1, 'All Variables')

#hN.SetMarkerStyle(
hN.Draw('][')

cN.SaveAs('../myMacros/classification/bdt_optimization_plots/training_vars_NORM.pdf')
 
# ===================================================================================================


raw_input('press return to continue')
