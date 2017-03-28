
# ===================================================
# Python script to perform BDT parameter optimization
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
trees = True

depth = False
depth = True

nEvt = False
nEvt = True

node_cut = False
node_cut = True
# =======================================

# Define the BDT paramter to vary
tree_list = [100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 1000]


depth_list = [1,2,3,4,5]

# learning rate(shrinkage)
lr_list = [0.01, 0.1, 0.12, 0.15, 0.2, 0.3, 0.5, 1]

# node search space size. TMVA default is 20
nodeCut_list = [5, 10, 25, 50, 100, 250, 500, 1000]
#nodeCut_list = [750, 1000]

# number of events for node minimum
nEvt_list = [0.1, 0.5, 1, 2, 3, 4, 5, 10, 15, 20]

# Higgs Mass Window
h_mass_low_list = [70, 80, 90, 100]
h_mass_high_list = [110, 120, 130, 140, 150, 160, 170]

# Higgs Mass Window
#v_pt_list = [80]
v_pt_list = [60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
#v_pt_high_list = [70, 80, 90, 100, 110, 120, 130, 150]

print '\n======================== Starting BDT Paramter Optimiziation ========================'
print '=====================================================================================\n'


# ====== For 3 pt Regions we need to train BDTS for each region and each opt point  =========

#pt_region_list = ['low','med','high']
pt_region_list = ['low', 'high']

for region in pt_region_list:

    print '\n\n\t========== Optimizing Pt Region: ',region, '============='

    # clear the temp files from last datacard iteration
    #os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')
    
    # Go into training.config and change the tree cut
    new_dir = "opt_tree_cut:  bdt_"+region+"_Zpt\n"
    for line in fileinput.input('13TeVconfig/training', inplace=True):
        if 'opt_tree_cut:' in line:
            print line.replace(line, new_dir),
        else: print line,
    # end file modification

    '''
    # Init ROC file
    
    if os.path.isfile('roc_lowPt.txt'):
        os.system('rm roc_lowPt.txt')
    if os.path.isfile('roc_medPt.txt'):
        os.system('rm roc_medPt.txt')
    if os.path.isfile('roc_highPt.txt'):
        os.system('rm roc_highPt.txt')

    roc_file = 'roc_'+region+'Pt.txt'
    open(roc_file, 'a').close()

    # Now train the BDT on new option list/ modified file
    os.system("python ../myMacros/classification/bdt_classifier_training_loop.py")
    
    # Save the roc file for this iteration
    if os.path.isfile('roc_lowPt.txt'):
        os.system('cp roc_lowPt.txt final_roc_lowPt.txt')
    if os.path.isfile('roc_medPt.txt'):
        os.system('cp roc_medPt.txt final_roc_medPt.txt')
    if os.path.isfile('roc_highPt.txt'):
        os.system('cp roc_highPt.txt final_roc_highPt.txt')
    '''    
       
    roc_file = 'final_roc_'+region+'Pt.txt'
    
 
    if trees:
              
       tree_metric_list  = []

       os.system('rm ../myMacros/classification/metric.txt')

       with open(roc_file) as temp_file:

           for i, line in enumerate(temp_file):

               print '\nTree entry:', i, 'ROC:',line

               if i >= len(tree_list): break
               
               tree_metric_list.append(float(line.strip('\n')))
    
    # end tree loop
    
    print 'Tree Metric List: ', tree_metric_list
    
    if nEvt:

       nEvt_metric_list  = []

       os.system('rm ../myMacros/classification/metric.txt')

       with open(roc_file) as temp_file:

           for i, line in enumerate(temp_file):
               
               if i < len(tree_list) or i >= (len(tree_list) + len(nEvt_list)): continue

               nEvt_metric_list.append(float(line.strip('\n')))

    # end tree loop

    print 'nEvt Metric List: ', nEvt_metric_list

    if depth:

       depth_metric_list  = []

       os.system('rm ../myMacros/classification/metric.txt')

       with open(roc_file) as temp_file:

           for i, line in enumerate(temp_file):
               
               if i < (len(tree_list) + len(nEvt_list)) or i >= (len(tree_list) + len(nEvt_list) + len(depth_list)): continue

               depth_metric_list.append(float(line.strip('\n')))

    # end depth loop

    print 'depth Metric List: ', depth_metric_list
    
    if node_cut:

       nCuts_metric_list  = []
       
       os.system('rm ../myMacros/classification/metric.txt')

       with open(roc_file) as temp_file:

           for i, line in enumerate(temp_file):
               
               if i < (len(tree_list) + len(nEvt_list) + len(depth_list)): continue

               nCuts_metric_list.append(float(line.strip('\n')))

    # end tree loop

    print 'nCuts Metric List: ', nCuts_metric_list
    
    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    h1b = TH1F('h1b', 'nTrees Optimization', len(tree_list), 0, len(tree_list)+1)
    h1b.SetFillColor(4)
    h1b.SetBarWidth(0.2)
    h1b.SetBarOffset(0.0)
    h1b.SetStats(0)
    h1b.GetYaxis().SetTitle('Cls Expected 50%')
    h1b.GetXaxis().SetTitle('Trees')
    
    #h1b.SetMinimum(0)
    #h1b.SetMaximum(20);

    for i in range(0, len(tree_list)):
        h1b.Fill(i+1, tree_metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(tree_list[i]))
        h1b.Draw('b')

    #cR.SaveAs('../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_trees_highPt_ratio.pdf')
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_trees_"+region.capitalize()+"Pt.pdf")
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_trees_"+region.capitalize()+"Pt.png")
    

    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    h1b = TH1F('h1b', 'nEvents Optimization', len(nEvt_list), 0, len(nEvt_list)+1)
    h1b.SetFillColor(4)
    h1b.SetBarWidth(0.2)
    h1b.SetBarOffset(0.0)
    h1b.SetStats(0)
    h1b.GetYaxis().SetTitle('Cls Expected 50%')
    h1b.GetXaxis().SetTitle('Trees')
    
    #h1b.SetMinimum(0)
    #h1b.SetMaximum(20);

    for i in range(0, len(nEvt_list)):
        h1b.Fill(i+1, nEvt_metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(nEvt_list[i]))
        h1b.Draw('b')

    #cR.SaveAs('../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_nEvts_highPt_ratio.pdf')
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_nEvts_"+region.capitalize()+"Pt.pdf")
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_nEvts_"+region.capitalize()+"Pt.png")

    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()
    
    h1b = TH1F('h1b', 'Depth Optimization', len(depth_list), 0, len(depth_list)+1)
    h1b.SetFillColor(4)
    h1b.SetBarWidth(0.2)
    h1b.SetBarOffset(0.0)
    h1b.SetStats(0)
    h1b.GetYaxis().SetTitle('Cls Expected 50%')
    h1b.GetXaxis().SetTitle('Depth')
    
    #h1b.SetMinimum(0)
    #h1b.SetMaximum(20);

    for i in range(0, len(depth_list)):
        h1b.Fill(i+1, depth_metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(depth_list[i]))
        h1b.Draw('b')

    #cR.SaveAs('../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_depths_highPt_ratio.pdf')
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_depths_"+region.capitalize()+"Pt.pdf")
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_depths_"+region.capitalize()+"Pt.png")

    
    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    h1b = TH1F('h1b', 'nCuts Optimization', len(nodeCut_list), 0, len(nodeCut_list)+1)
    h1b.SetFillColor(4)
    h1b.SetBarWidth(0.2)
    h1b.SetBarOffset(0.0)
    h1b.SetStats(0)
    h1b.GetYaxis().SetTitle('Cls Expected 50%')
    h1b.GetXaxis().SetTitle('nCuts')
    
    #h1b.SetMinimum(0)
    #h1b.SetMaximum(20);

    for i in range(0, len(nodeCut_list)):
        h1b.Fill(i+1, nCuts_metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(nodeCut_list[i]))
        h1b.Draw('b')

    #cR.SaveAs('../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_nCutss_highPt_ratio.pdf')
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_nCuts_"+region.capitalize()+"Pt.pdf")
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_nCuts_"+region.capitalize()+"Pt.png")

