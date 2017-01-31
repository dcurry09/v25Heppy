
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



# ======= Choose what to optimize =========
trees = False
#trees = True

lr = False
#lr = True

node_cut = False
node_cut = True

boost = False
#boost = True

node_seperation = False
#node_seperation = True  

data = False
#data = True
# =========================================


# What channel to optimize
channel = 'Zll'
#channel = 'Zvv'
#channel = 'Wlv'


# Define the BDT paramter to vary
tree_list = [100, 300, 500, 800, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000]#, 7000, 8000]

# learning rate(shrinkage)
lr_list = [0.01, 0.05, 0.1, 0.3, 0.5, 1]

# node search space size. TMVA default is 20 
nodeCut_list = [2, 3, 4, 5, 10, 15, 20, 100, 500, 1000, 2000, 3000, 5000, 100000]

# Boost Type
boost_list = ['AdaBoost', 'Bagging', 'Grad']

# node seperation algorithm
nodeSeperation_list = ['CrossEntropy', 'GiniIndex', 'GiniIndexWithLaplace', 'MisClassificationError', 'SDivSqrtSPlusB', 'RegressionVariance']

# Define different partitioned dataset
file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/v11_04_17_2015_Zll.root')
tree = file.Get('tree')
nEntries = tree.GetEntries()
data_list = [nEntries*x for x in [.2, .4, .6, .8, .9, 1, 1.2, 1.4, 1.6, 1.8]]



print '\n======================== Starting BDT Paramter Optimiziation ========================'
print '=====================================================================================\n'


if trees:

    # list of regression metrics
    metric_list  = []

    # loop over parmater list
    for param in tree_list:
        
        print '\n\n======================== Starting New Tree Loop  ========================'
        print '=============================================================================='
        print '----> Looping over parameter: ', param 
                
        # new BDT option string
        new_options = 'options: !H:!V:NTrees='+str(param)+'::BoostType=Grad:Shrinkage=0.01:SeparationType=RegressionVariance:UseBaggedGrad:MaxDepth=3\n'
        
        for line in fileinput.input("13TeVconfig/regression", inplace=True):
            
            if 'options' in line:
                
                print line.replace(line, new_options),
                
            else: print line,
        # end file modification


        # Now run the BDT on new option list/ modified file
        os.system('./runAll.sh '+channel+' 13TeV trainReg && ./runAll.sh '+channel+' 13TeV sys')
        
        # Get the metric of success for each parameter iteration
        # put each iterations metric in a plot
        output = subprocess.check_output(['python', '../myMacros/simple_regression_HistMaker.py']) 
        
        metric_list.append(float(output))

    # end paramater loop

    
    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()
    
    #h1b = TH1F('h1b', 'Tree Optimization, #sigma/#mu: DiJet Mass', int(len(tree_list)), 0, int(tree_list[-1]))
    h1b = TH1F('h1b', 'Tree Optimization, #sigma/#mu: DiJet Mass', len(tree_list), 0, len(tree_list)+1)
    h1b.SetFillColor(4);
    h1b.SetBarWidth(0.4);
    h1b.SetBarOffset(0.0);
    h1b.SetStats(0);
    h1b.GetYaxis().SetTitle('#sigma/#mu')
    h1b.GetXaxis().SetTitle('Trees')
    #h1b.SetMinimum(10);
    #h1b.SetMaximum(20);

    for i in range(0, len(tree_list)):
        print 'metric:', metric_list[i]
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(tree_list[i]))
        h1b.Draw('b')

    cStd.SaveAs('../myMacros/plots/std_feature_loop_trees.pdf')

# ===================================================================================================
# end tree loop


if lr:

    # list of regression metrics
    metric_list  = []

    # loop over parmater list
    for param in lr_list:
        
        print '\n\n======================== Starting New Learning Rate Loop  ========================'
        print '=============================================================================='
        print '----> Looping over parameter: ', param
        
        
        # new BDT option string
        new_options = 'options: !H:!V:NTrees=2000::BoostType=Grad:Shrinkage='+str(param)+':SeparationType=RegressionVariance:UseBaggedGrad:MaxDepth=3\n'
        
        for line in fileinput.input("13TeVconfig/regression", inplace=True):
            
            if 'options' in line:

                print line.replace(line, new_options),
                
            else: print line,
        # end file modification

        # Now run the BDT on new option list/ modified file
        os.system('./runAll.sh '+channel+' 13TeV trainReg && ./runAll.sh '+channel+' 13TeV sys')
        
        # Get the metric of success for each parameter iteration
        # put each iterations metric in a plot
        output = subprocess.check_output(['python', '../myMacros/simple_regression_HistMaker.py'])

        metric_list.append(float(output))
        
    # end paramater loop

    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()
    
    h1b = TH1F('h1b', 'Learning Rate Optimization,  #sigma/#mu: DiJet Mass', len(lr_list), 0, len(lr_list)+1);
    h1b.SetFillColor(4);
    h1b.SetBarWidth(0.4);
    h1b.SetBarOffset(0.0);
    h1b.SetStats(0);
    h1b.GetYaxis().SetTitle('#sigma/#mu')
    h1b.GetXaxis().SetTitle('Learning Rate')
    #h1b.SetMinimum(10);
    #h1b.SetMaximum(20);
    
    for i in range(0, len(metric_list)):
        
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(lr_list[i]))
        h1b.Draw('b')
        
    cStd.SaveAs('../myMacros/plots/std_feature_loop_lr.pdf')
        
        
# ===================================================================================================
# end lr loop
        


if data:

    # list of regression metrics
    metric_list  = []

    # loop over parmater list
    for param in data_list:

        print '\n\n======================== Starting New Data Loop  ========================'
        print '=============================================================================='
        print '----> Looping over parameter: ', param
        

        # new training event cut
        new_train_cut = 'trainCut : evt%2==0 & evt<'+str(param)+'\n' 
        
        for line in fileinput.input("13TeVconfig/regression", inplace=True):

            if 'trainCut' in line:

                print line.replace(line, new_train_cut),

            else: print line,
        #end file modification

        # Now run the BDT on new option list/ modified file
        os.system('./runAll.sh '+channel+' 13TeV trainReg && ./runAll.sh '+channel+' 13TeV sys')

        # Get the metric of success for each parameter iteration
        # put each iterations metric in a plot
        output = subprocess.check_output(['python', '../myMacros/simple_regression_HistMaker.py'])

        metric_list.append(float(output))
        
        
    # end paramater loop
    
    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()
    
    h1b = TH1F('h1b', 'Training Data,  #sigma/#mu: DiJet Mass', len(data_list), 0, len(data_list)+1)
    h1b.SetFillColor(4)
    h1b.SetFillColor(4)
    h1b.SetBarWidth(0.4)
    h1b.GetYaxis().SetTitle('#sigma/#mu')
    h1b.GetXaxis().SetTitle('Training Data')
    h1b.SetBarOffset(0.0)
    h1b.SetStats(0)
    #h1b.SetMinimum(10);
    #h1b.SetMaximum(20);
    percent_list = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
    
    for i in range(0, len(metric_list)):
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, percent_list[i])
        h1b.Draw('b')
        
    cStd.SaveAs('../myMacros/plots/std_feature_loop_data.pdf')
    
    
# # ===================================================================================================
# end data loop


if node_cut:

    # list of regression metrics
    metric_list  = []

    # loop over parmater list
    for param in nodeCut_list:

        print '\n\n======================== Starting New Node Cut Loop  ========================'
        print '=============================================================================='
        print '----> Looping over parameter: ', param
        
        
        # new BDT option string
        new_options = 'options: !H:!V:NTrees=2000::BoostType=Grad:Shrinkage=0.01:SeparationType=RegressionVariance:UseBaggedGrad:MaxDepth=3:nCuts='+str(param)+'\n'

        new_filename = 'name: v11_train_Zll_noMET_nCuts'+str(param)+'\n'
        
        for line in fileinput.input("13TeVconfig/regression", inplace=True):
            
            if 'options' in line:
                
                print line.replace(line, new_options),
                
            else: print line,
        # end file modification

        for line in fileinput.input("13TeVconfig/regression", inplace=True):

            if 'name:' in line:
                
                print line.replace(line, new_filename),

            else: print line,
        # end file modification

        # Now run the BDT on new option list/ modified file
        os.system('./runAll.sh '+channel+' 13TeV trainReg && ./runAll.sh '+channel+' 13TeV sys')
'''       
        # Get the metric of success for each parameter iteration
        # put each iterations metric in a plot
        output = subprocess.check_output(['python', '../myMacros/simple_regression_HistMaker.py'])
        
        metric_list.append(float(output))
        
    # end paramater loop

    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    #h1b = TH1F('h1b', 'Tree Optimization, #sigma/#mu: DiJet Mass', int(len(tree_list)), 0, int(tree_list[-1]))
    h1b = TH1F('h1b', 'Node Search Size Optimization, #sigma/#mu: DiJet Mass', len(metric_list), 0, len(metric_list)+1)
    h1b.SetFillColor(4);
    h1b.SetBarWidth(0.4);
    h1b.SetBarOffset(0.0);
    h1b.SetStats(0);
    h1b.GetYaxis().SetTitle('#sigma/#mu')
    h1b.GetXaxis().SetTitle('Node Search Size')
    #h1b.SetMinimum(10);
    #h1b.SetMaximum(20);
    
    for i in range(0, len(metric_list)):
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(nodeCut_list[i]))
        h1b.Draw('b')
        
    cStd.SaveAs('../myMacros/plots/std_feature_loop_nodeCut.pdf')
'''    
# ===================================================================================================
# end node cut loop
        

if boost:
    
    # list of regression metrics
    metric_list  = []

    # loop over parmater list
    for param in boost_list:

        print '\n\n======================== Starting New Boost Loop  ========================'
        print '=============================================================================='
        print '----> Looping over parameter: ', param
        
        
        # new BDT option string
        new_options = 'options: !H:!V:NTrees=4000:Shrinkage=0.05:SeparationType=RegressionVariance:MaxDepth=3:BoostType='+param+'\n'
        
        for line in fileinput.input("13TeVconfig/regression", inplace=True):
            
            if 'options' in line:
                
                print line.replace(line, new_options),
                
            else: print line,
        # end file modification
            
        # Now run the BDT on new option list/ modified file
        os.system('./runAll.sh Hbb_'+channel+'_v7 13TeV trainReg && ./runAll.sh Hbb_'+channel+'_v7 13TeV sys')
        
        # Get the metric of success for each parameter iteration
        # put each iterations metric in a plot
        output = subprocess.check_output(['python', '../myMacros/simple_regression_HistMaker.py'])
        
        metric_list.append(float(output))
        
    # end paramater loop

    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    #h1b = TH1F('h1b', 'Tree Optimization, #sigma/#mu: DiJet Mass', int(len(tree_list)), 0, int(tree_list[-1]))
    h1b = TH1F('h1b', 'Boost Type Optimization, #sigma/#mu: DiJet Mass', len(metric_list), 0, len(metric_list)+1)
    h1b.SetFillColor(4);
    h1b.SetBarWidth(0.4);
    h1b.SetBarOffset(0.0);
    h1b.SetStats(0);
    h1b.GetYaxis().SetTitle('#sigma/#mu')
    h1b.GetXaxis().SetTitle('Boost Type')
    #h1b.SetMinimum(10);
    #h1b.SetMaximum(20);
    
    for i in range(0, len(metric_list)):
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, boost_list[i])
        h1b.Draw('b')
        
    cStd.SaveAs('../myMacros/plots/std_feature_loop_boost.pdf')
    
# ===================================================================================================
# end boost loop
        

if node_seperation:

    # list of regression metrics
    metric_list  = []

    # loop over parmater list
    for param in nodeSeperation_list:

        print '\n\n======================== Starting New Boost Loop  ========================'
        print '=============================================================================='
        print '----> Looping over parameter: ', param
        
        
        # new BDT option string
        new_options = 'options: !H:!V:NTrees=4000::BoostType=Grad:Shrinkage=0.05:SeparationType='+param+':UseBaggedGrad:MaxDepth=3\n'
        
        for line in fileinput.input("13TeVconfig/regression", inplace=True):
            
            if 'options' in line:
                
                print line.replace(line, new_options),
                
            else: print line,
        # end file modification
            
        # Now run the BDT on new option list/ modified file
        os.system('./runAll.sh Hbb_'+channel+'_v7 13TeV trainReg && ./runAll.sh Hbb_'+channel+'_v7 13TeV sys')
        
        # Get the metric of success for each parameter iteration
        # put each iterations metric in a plot
        output = subprocess.check_output(['python', '../myMacros/simple_regression_HistMaker.py'])
        
        metric_list.append(float(output))
        
    # end paramater loop

    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    #h1b = TH1F('h1b', 'Tree Optimization, #sigma/#mu: DiJet Mass', int(len(tree_list)), 0, int(tree_list[-1]))
    h1b = TH1F('h1b', 'Node Separation Optimization, #sigma/#mu: DiJet Mass', len(metric_list), 0, len(metric_list)+1)
    h1b.SetFillColor(4);
    h1b.SetBarWidth(0.4);
    h1b.SetBarOffset(0.0);
    h1b.SetStats(0);
    h1b.GetYaxis().SetTitle('#sigma/#mu')
    h1b.GetXaxis().SetTitle('Node Separation Algorithm')
    #h1b.SetMinimum(10);
    #h1b.SetMaximum(20);
    
    for i in range(0, len(metric_list)):
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, nodeSeperation_list[i])
        h1b.Draw('b')
        
    cStd.SaveAs('../myMacros/plots/std_feature_loop_nodeSeparation.pdf')
        
# ===================================================================================================
# end node separation loop
        


            




raw_input('press return to continue')
