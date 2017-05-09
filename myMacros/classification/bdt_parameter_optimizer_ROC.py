
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
gROOT.SetBatch(True)

outpath = '/afs/cern.ch/user/d/dcurry/www/v25_BDT_optimization_4_20/'
try:
    os.system('mkdir '+outpath)
except:
     print outpath+' already exists...'
temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outpath
os.system(temp_string2)
os.system(temp_string3)

# ======= Choose what to optimize =========
trees = False
trees = True

depth = False
depth = True

nEvt = False
nEvt = True

node_cut = False
node_cut = True

lr = False
lr = True
# =======================================

# Define the BDT paramter to vary
tree_list = [100, 200, 300, 400, 450, 500, 550, 600, 700, 800, 900, 1000]
#tree_list = [100, 150]

depth_list = [1,2,3,4,5]

# learning rate(shrinkage or adaboost)
lr_list = [0.01, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.2, 0.3, 0.4, 0.5]

# node search space size. TMVA default is 20
nodeCut_list = [5, 10, 25, 50, 100, 150, 200, 250, 300, 400, 500]

# number of events for node minimum
nEvt_list = [0.1, 0.2, 0.3, 0.5, 1, 2, 3, 4, 5, 10, 15, 20]

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

pt_region_list = ['high']
#pt_region_list = ['low','high']

for region in pt_region_list:

    print '\n\n\t========== Optimizing Pt Region: ',region, '============='

    # Set the pt region cut
    new_options = 'opt_tree_cut:bdt_'+region+'_Zpt\n'
    for line in fileinput.input("13TeVconfig/training", inplace=True):
        if 'opt_tree_cut:' in line:
            print line.replace(line, new_options),
        else: print line,
    # end file modification
    
         
    if trees:
    
        if os.path.isfile('roc_temp.txt'):    
            os.system('rm roc_temp.txt')
            
        # Init ROC file
        if os.path.isfile('roc_trees_'+region+'Pt.txt'):
            os.system('rm roc_trees_'+region+'Pt.txt')

        roc_file = 'roc_trees_'+region+'Pt.txt'
        open(roc_file, 'a').close()
              
        tree_metric_list  = []

        # Change the training loop list
        new_options = 'optimizer_training_list= training_list_trees\n'

        for line in fileinput.input("../myMacros/classification/bdt_classifier_training_loop.py", inplace=True):
            
            if 'optimizer_training_list=' in line:

                print line.replace(line, new_options),

            else: print line,
        # end file modification


        # Now train the BDT on new option list/ modified file
        os.system("python ../myMacros/classification/bdt_classifier_training_loop.py")
        
        # copy temp roc into final storage        
        os.system('cp roc_temp.txt roc_trees_'+region+'Pt.txt')

        with open(roc_file) as temp_file:
            
            for i, line in enumerate(temp_file):

                print '\nTree entry:', i, 'ROC:',line

                if i >= len(tree_list): break
               
                tree_metric_list.append(float(line.strip('\n')))
    
        # end tree loop

        print 'Tree Metric List: ', tree_metric_list

        #fill accuracy plots
        cStd = TCanvas('cStd')
        cStd.SetGrid()

        h1b = TH1F('h1b', 'nTrees Optimization', len(tree_metric_list), 0, len(tree_metric_list)+1)
        h1b.SetFillColor(4)
        h1b.SetBarWidth(0.2)
        h1b.SetBarOffset(0.3)
        h1b.SetStats(0)
        h1b.GetYaxis().SetTitle('AUC ROC')
        h1b.GetXaxis().SetTitle('Trees')

        for i in range(0, len(tree_metric_list)):
            h1b.SetBinContent(i+1, tree_metric_list[i])
            h1b.GetXaxis().SetBinLabel(i+1, str(tree_list[i]))
        h1b.Draw('B')

        cStd.Update()
        
        cStd.SaveAs(outpath+"/bdt_paramOptimization_trees_"+region.capitalize()+"Pt.pdf")
        cStd.SaveAs(outpath+"/bdt_paramOptimization_trees_"+region.capitalize()+"Pt.png")
    


    #######################################################


    if depth:
    
        if os.path.isfile('roc_temp.txt'):    
            os.system('rm roc_temp.txt')
            
        # Init ROC file
        if os.path.isfile('roc_depth_'+region+'Pt.txt'):
            os.system('rm roc_depth_'+region+'Pt.txt')

        roc_file = 'roc_depth_'+region+'Pt.txt'
        open(roc_file, 'a').close()
              
        tree_metric_list  = []

        # Change the training loop list
        new_options = 'optimizer_training_list= training_list_depth\n'

        for line in fileinput.input("../myMacros/classification/bdt_classifier_training_loop.py", inplace=True):
            
            if 'optimizer_training_list=' in line:

                print line.replace(line, new_options),

            else: print line,
        # end file modification


        # Now train the BDT on new option list/ modified file
        os.system("python ../myMacros/classification/bdt_classifier_training_loop.py")
        
        # copy temp roc into final storage        
        os.system('cp roc_temp.txt roc_depth_'+region+'Pt.txt')

        with open(roc_file) as temp_file:
            
            for i, line in enumerate(temp_file):

                print '\nTree entry:', i, 'ROC:',line

                if i >= len(tree_list): break
               
                tree_metric_list.append(float(line.strip('\n')))
    
                    
        print 'Tree Metric List: ', tree_metric_list

        cStd = TCanvas('cStd')
        cStd.SetGrid()

        h1b = TH1F('h1b', 'Depth Optimization', len(tree_metric_list), 0, len(tree_metric_list)+1)
        h1b.SetFillColor(4)
        h1b.SetBarWidth(0.2)
        h1b.SetBarOffset(0.3)
        h1b.SetStats(0)
        h1b.GetYaxis().SetTitle('AUC ROC')
        h1b.GetXaxis().SetTitle('Depth')

        for i in range(0, len(tree_metric_list)):
            h1b.SetBinContent(i+1, tree_metric_list[i])
            h1b.GetXaxis().SetBinLabel(i+1, str(depth_list[i]))
        h1b.Draw('B')

        cStd.Update()
        cStd.SaveAs(outpath+"/bdt_paramOptimization_depth_"+region.capitalize()+"Pt.pdf")
        cStd.SaveAs(outpath+"/bdt_paramOptimization_depth_"+region.capitalize()+"Pt.png")
    


    #######################################################


    if nEvt:
    
        if os.path.isfile('roc_temp.txt'):    
            os.system('rm roc_temp.txt')
            
        # Init ROC file
        if os.path.isfile('roc_nEvt_'+region+'Pt.txt'):
            os.system('rm roc_nEvt_'+region+'Pt.txt')

        roc_file = 'roc_nEvt_'+region+'Pt.txt'
        open(roc_file, 'a').close()
              
        tree_metric_list  = []

        # Change the training loop list
        new_options = 'optimizer_training_list= training_list_nEvt\n'

        for line in fileinput.input("../myMacros/classification/bdt_classifier_training_loop.py", inplace=True):
            
            if 'optimizer_training_list=' in line:

                print line.replace(line, new_options),

            else: print line,
        # end file modification


        # Now train the BDT on new option list/ modified file
        os.system("python ../myMacros/classification/bdt_classifier_training_loop.py")
        
        # copy temp roc into final storage        
        os.system('cp roc_temp.txt roc_nEvt_'+region+'Pt.txt')

        with open(roc_file) as temp_file:
            
            for i, line in enumerate(temp_file):

                print '\nTree entry:', i, 'ROC:',line

                if i >= len(tree_list): break
               
                tree_metric_list.append(float(line.strip('\n')))
    
        print 'Tree Metric List: ', tree_metric_list

        cStd = TCanvas('cStd')
        cStd.SetGrid()

        h1b = TH1F('h1b', 'nNEvt Optimization', len(tree_metric_list), 0, len(tree_metric_list)+1)
        h1b.SetFillColor(4)
        h1b.SetBarWidth(0.2)
        h1b.SetBarOffset(0.3)
        h1b.SetStats(0)
        h1b.GetYaxis().SetTitle('AUC ROC')
        h1b.GetXaxis().SetTitle('NEvt')

        for i in range(0, len(tree_metric_list)):
            h1b.SetBinContent(i+1, tree_metric_list[i])
            h1b.GetXaxis().SetBinLabel(i+1, str(nEvt_list[i]))
        h1b.Draw('B')
    
        cStd.Update()
        cStd.SaveAs(outpath+"/bdt_paramOptimization_nEvt_"+region.capitalize()+"Pt.pdf")
        cStd.SaveAs(outpath+"/bdt_paramOptimization_nEvt_"+region.capitalize()+"Pt.png")
    
    #######################################################

    if node_cut:
    
        if os.path.isfile('roc_temp.txt'):    
            os.system('rm roc_temp.txt')
            
        # Init ROC file
        if os.path.isfile('roc_node_cut_'+region+'Pt.txt'):
            os.system('rm roc_node_cut_'+region+'Pt.txt')

        roc_file = 'roc_node_cut_'+region+'Pt.txt'
        open(roc_file, 'a').close()
              
        tree_metric_list  = []

        # Change the training loop list
        new_options = 'optimizer_training_list= training_list_cuts\n'

        for line in fileinput.input("../myMacros/classification/bdt_classifier_training_loop.py", inplace=True):
            
            if 'optimizer_training_list=' in line:

                print line.replace(line, new_options),

            else: print line,
        # end file modification


        # Now train the BDT on new option list/ modified file
        os.system("python ../myMacros/classification/bdt_classifier_training_loop.py")
        
        # copy temp roc into final storage        
        os.system('cp roc_temp.txt roc_node_cut_'+region+'Pt.txt')

        with open(roc_file) as temp_file:
            
            for i, line in enumerate(temp_file):

                print '\nTree entry:', i, 'ROC:',line

                if i >= len(tree_list): break
               
                tree_metric_list.append(float(line.strip('\n')))
    
                    
        print 'Tree Metric List: ', tree_metric_list

        cStd = TCanvas('cStd')
        cStd.SetGrid()

        h1b = TH1F('h1b', 'nNode_Cut Optimization', len(tree_metric_list), 0, len(tree_metric_list)+1)
        h1b.SetFillColor(4)
        h1b.SetBarWidth(0.2)
        h1b.SetBarOffset(0.3)
        h1b.SetStats(0)
        h1b.GetYaxis().SetTitle('AUC ROC')
        h1b.GetXaxis().SetTitle('Node_Cut')
        
        for i in range(0, len(tree_metric_list)):
            h1b.SetBinContent(i+1, tree_metric_list[i])
            h1b.GetXaxis().SetBinLabel(i+1, str(nodeCut_list[i]))
        h1b.Draw('B')

        cStd.Update()
        cStd.SaveAs(outpath+"/bdt_paramOptimization_node_cut_"+region.capitalize()+"Pt.pdf")
        cStd.SaveAs(outpath+"/bdt_paramOptimization_node_cut_"+region.capitalize()+"Pt.png")
    
    #######################################################


    if lr:
    
        if os.path.isfile('roc_temp.txt'):    
            os.system('rm roc_temp.txt')
            
        # Init ROC file
        if os.path.isfile('roc_lr_'+region+'Pt.txt'):
            os.system('rm roc_lr_'+region+'Pt.txt')

        roc_file = 'roc_lr_'+region+'Pt.txt'
        open(roc_file, 'a').close()
              
        tree_metric_list  = []

        # Change the training loop list
        new_options = 'optimizer_training_list= training_list_LR\n'

        for line in fileinput.input("../myMacros/classification/bdt_classifier_training_loop.py", inplace=True):
            
            if 'optimizer_training_list=' in line:

                print line.replace(line, new_options),

            else: print line,
        # end file modification


        # Now train the BDT on new option list/ modified file
        os.system("python ../myMacros/classification/bdt_classifier_training_loop.py")
        
        # copy temp roc into final storage        
        os.system('cp roc_temp.txt roc_lr_'+region+'Pt.txt')

        with open(roc_file) as temp_file:
            
            for i, line in enumerate(temp_file):

                print '\nTree entry:', i, 'ROC:',line

                if i >= len(tree_list): break
               
                tree_metric_list.append(float(line.strip('\n')))
    
    # end tree loop

    #tree_metric_list = [0.5, 0.8]
                    
    print 'Tree Metric List: ', tree_metric_list

    #fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    h1b = TH1F('h1b', 'nLr Optimization', len(tree_metric_list), 0, len(tree_metric_list)+1)
    h1b.SetFillColor(4)
    h1b.SetBarWidth(0.2)
    h1b.SetBarOffset(0.3)
    h1b.SetStats(0)
    h1b.GetYaxis().SetTitle('AUC ROC')
    h1b.GetXaxis().SetTitle('LR')

    #h1b.SetMinimum(0)
    #h1b.SetMaximum(20);

    for i in range(0, len(tree_metric_list)):
        #h1b.Fill(i+1, tree_metric_list[i])
        h1b.SetBinContent(i+1, tree_metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(lr_list[i]))
    h1b.Draw('B')

    cStd.Update()
    #cR.SaveAs('../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_lr_highPt_ratio.pdf')
    cStd.SaveAs(outpath+"/bdt_paramOptimization_lr_"+region.capitalize()+"Pt.pdf")
    cStd.SaveAs(outpath+"/bdt_paramOptimization_lr_"+region.capitalize()+"Pt.png")
    
    #######################################################
