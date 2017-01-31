
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

lr = False
#lr = True

nEvt = False
nEvt = True

node_cut = False
node_cut = True

boost = False
#boost = True

node_seperation = False
#node_seperation = True  

hMass = False
#hMass = True

vPt = False
#vPt = True

# =========================================


# Define the BDT paramter to vary
tree_list = [100, 150, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 1000]

depth_list = [1,2,3,4,5]

# learning rate(shrinkage)
lr_list = [0.01, 0.1, 0.12, 0.15, 0.2, 0.3, 0.5, 1]

# node search space size. TMVA default is 20 
nodeCut_list = [5, 10, 25, 50, 100, 250, 500, 1000]
#nodeCut_list = [750, 1000]

# number of events for node minimum
nEvt_list = [0.1, 0.5, 1, 2, 3, 4, 5, 10, 15]

 
# Higgs Mass Window
h_mass_low_list = [70, 80, 90, 100]
h_mass_high_list = [110, 120, 130, 140, 150, 160, 170]

# Higgs Mass Window
#v_pt_list = [80]
v_pt_list = [60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
#v_pt_high_list = [70, 80, 90, 100, 110, 120, 130, 150]


# Boost Type
boost_list = ['AdaBoost', 'Bagging', 'Grad']

# node seperation algorithm
nodeSeperation_list = ['CrossEntropy', 'GiniIndex', 'GiniIndexWithLaplace', 'MisClassificationError', 'SDivSqrtSPlusB', 'RegressionVariance']

# Random Trees
randomised_trees_list = ['False', 'True']



print '\n======================== Starting BDT Paramter Optimiziation ========================'
print '=====================================================================================\n'



# Now train the BDT on new option list/ modified file
#os.system('python ../myMacros/classification/bdt_classifier_training_loop.py')
    

# ====== For 3 pt Regions we need to train BDTS for each region and each opt point  =========

#pt_region_list = ['low','high']
pt_region_list = ['high']

for region in pt_region_list:

    print '\n\n\t========== Optimizing Pt Region: ',region, '============='

    # clear the temp files from last datacard iteration
    os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')
    
    # Go into training.config and change the tree cut
    new_dir = "opt_tree_cut:  bdt_"+region+"_Zpt\n"
    for line in fileinput.input('13TeVconfig/training', inplace=True):
        if 'opt_tree_cut:' in line:
            print line.replace(line, new_dir),
        else: print line,
    # end file modification
    
    # Now train the BDT on new option list/ modified file
    #os.system('python ../myMacros/classification/bdt_classifier_training_loop.py')
    
    # Apply the BDT weights to samples
    #os.system('python ../myMacros/classification/bdt_classifier_eval_loop.py')
    
    # ==== Now loop over datacards for each optimization point ====

    # list of regression metrics
    metric_list  = []
    metric_list_train = []

    os.system('rm ../myMacros/classification/metric.txt')


    
    for param in tree_list:
        
        # Set datacard output directory to current var name
        new_dir = "dir = 'bdt_param_optimize/6_22_BDT_trees"+str(param)+"'\n"
        
        for line in fileinput.input('../myMacros/classification/dataCard_loop.py', inplace=True):
            
            if 'dir =' in line:
                
                print line.replace(line, new_dir),

            else: print line,
        # end file modification

        # Set the Datacard variable to current tree BDT weights
        new_bdt = "bdt: gg_plus_trees"+str(param)+".nominal\n"

        for line in fileinput.input('13TeVconfig/datacard', inplace=True):

            if 'bdt:' in line:

                print line.replace(line, new_bdt),

            else: print line,
        # end file modification
            
        os.system('python ../myMacros/classification/dataCard_loop.py')

        # Get the metric of success for each parameter iteration
        # put each iterations metric in a plot
    
        if os.path.isfile('cls_expected.txt'):
            os.system('rm cls_expected.txt')

        # Combine electron and muon
        e_card = "../limits/bdt_param_optimize/6_22_BDT_trees"+str(param)+"/vhbb_DC_TH_BDT_Zee_"+region.capitalize()+"Pt.txt"
        m_card = "../limits/bdt_param_optimize/6_22_BDT_trees"+str(param)+"/vhbb_DC_TH_BDT_Zuu_"+region.capitalize()+"Pt.txt"
        combine_card = "../limits/bdt_param_optimize/6_22_BDT_trees"+str(param)+"/vhbb_DC_TH_BDT_Combine_"+region.capitalize()+"Pt.txt"

        t8 = "combineCards.py ../limits/bdt_param_optimize/6_22_BDT_trees"+str(param)+"/vhbb_DC_TH_Zlf.txt ../limits/bdt_param_optimize/6_22_BDT_trees"+str(param)+"/vhbb_DC_TH_ttbar.txt ../limits/bdt_param_optimize/6_22_BDT_trees"+str(param)+"/vhbb_DC_TH_Zhf.txt "+e_card+" "+m_card+" > "+combine_card
        
        print t8
        
        os.system(t8)

        # CLs Median expected limit
        #t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/3_25_BDT_v21_trees"+str(param)+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
        t6 = "combine -M Asymptotic -t -1 "+combine_card+" >> cls_expected.txt"
        os.system(t6)

        # get the 50% limit
        for line in fileinput.input("cls_expected.txt", inplace=True):

            if 'Expected 50.0%:' in line:

                metric = line.replace('Expected 50.0%: r < ', '')

        print 'metric: ', metric

        metric_list.append(float(metric))
        
        # Store latest iteration in text file
        with open('../myMacros/classification/metric.txt', 'a') as file:
            file.write('\n')
            file.write('metric:'+str(metric_list))
                #file.write('\n')
                #file.write('train:'+str(metric_list_train))
        
    # end paramater loop

    # Testing
    #metric_list = [4.7344, 3.8281, 3.2344, 3.1406, 2.8672, 3.2656, 3.1719, 3.0078, 2.9766, 2.8516, 2.8984, 3.1719, 3.1172, 3.125]
    #metric_list_train = [4.1406, 2.5391, 2.5703, 2.3359, 2.1641, 2.0859, 2.0703, 2.1016, 2.0234, 1.6953, 1.6797, 1.7422, 1.5547, 1.3867]
    
    print 'Tree Metric List: ', metric_list
    #print 'Train Metric List: ', metric_list_train

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
    
    h1b.SetMinimum(0)
    #h1b.SetMaximum(20);

    for i in range(0, len(tree_list)):
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(tree_list[i]))
        h1b.Draw('b')

    
    #cR.SaveAs('../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_trees_highPt_ratio.pdf')
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_trees_"+region.capitalize()+"Pt.pdf")
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_trees_"+region.capitalize()+"Pt.png")

    # ===================================================================================================
    # end tree loop



 
    # list of regression metrics
    metric_list  = []
    metric_list_train = []

    os.system('rm ../myMacros/classification/metric.txt')


    
    for param in nEvt_list:
        
        # Set datacard output directory to current var name
        new_dir = "dir = 'bdt_param_optimize/6_22_BDT_nEvt"+str(param)+"'\n"
        
        for line in fileinput.input('../myMacros/classification/dataCard_loop.py', inplace=True):
            
            if 'dir =' in line:
                
                print line.replace(line, new_dir),

            else: print line,
        # end file modification

        # Set the Datacard variable to current tree BDT weights
        new_bdt = "bdt: gg_plus_nEvt"+str(param)+".nominal\n"

        for line in fileinput.input('13TeVconfig/datacard', inplace=True):

            if 'bdt:' in line:

                print line.replace(line, new_bdt),

            else: print line,
        # end file modification
            
        os.system('python ../myMacros/classification/dataCard_loop.py')

        # Get the metric of success for each parameter iteration
        # put each iterations metric in a plot
    
        if os.path.isfile('cls_expected.txt'):
            os.system('rm cls_expected.txt')

        # Combine electron and muon
        e_card = "../limits/bdt_param_optimize/6_22_BDT_nEvt"+str(param)+"/vhbb_DC_TH_BDT_Zee_"+region.capitalize()+"Pt.txt"
        m_card = "../limits/bdt_param_optimize/6_22_BDT_nEvt"+str(param)+"/vhbb_DC_TH_BDT_Zuu_"+region.capitalize()+"Pt.txt"
        combine_card = "../limits/bdt_param_optimize/6_22_BDT_nEvt"+str(param)+"/vhbb_DC_TH_BDT_Combine_"+region.capitalize()+"Pt.txt"

        t8 = "combineCards.py ../limits/bdt_param_optimize/6_22_BDT_nEvt"+str(param)+"/vhbb_DC_TH_Zlf.txt ../limits/bdt_param_optimize/6_22_BDT_nEvt"+str(param)+"/vhbb_DC_TH_ttbar.txt ../limits/bdt_param_optimize/6_22_BDT_nEvt"+str(param)+"/vhbb_DC_TH_Zhf.txt "+e_card+" "+m_card+" > "+combine_card

        os.system(t8)

        # CLs Median expected limit
        #t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/3_25_BDT_v21_trees"+str(param)+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
        t6 = "combine -M Asymptotic -t -1 "+combine_card+" >> cls_expected.txt"
        os.system(t6)

        # get the 50% limit
        for line in fileinput.input("cls_expected.txt", inplace=True):

            if 'Expected 50.0%:' in line:

                metric = line.replace('Expected 50.0%: r < ', '')

        print 'metric: ', metric

        metric_list.append(float(metric))



        # Store latest iteration in text file
        with open('../myMacros/classification/nEvt_metric.txt', 'a') as file:
            file.write('\n')
            file.write('metric:'+str(metric_list))
            #file.write('\n')
            #file.write('train:'+str(metric_list_train))



    # end paramater loop

    print 'nEvt Metric List: ', metric_list
    #print 'Train Metric List: ', metric_list_train
    #metric_list = [12.6875, 13.5, 13.0625, 12.8125, 12.8125, 13.0625, 13.0625, 13.75, 14.6875]

    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    h1b = TH1F('h1b', 'nEvents Min Optimization', len(nEvt_list), 0, len(nEvt_list)+1)
    h1b.SetFillColor(4);
    h1b.SetBarWidth(0.2);
    h1b.SetBarOffset(0.0);
    h1b.SetStats(0);
    h1b.GetYaxis().SetTitle('Cls Expected 50%')
    h1b.GetXaxis().SetTitle('nEvtMin(%)')
    h1b.SetMinimum(0);
    #h1b.SetMaximum(20);

    for i in range(0, len(nEvt_list)):
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(nEvt_list[i]))
        h1b.Draw('b')
    
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/nEvtsMin_opt_"+region.capitalize()+"Pt.pdf")
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/nEvtsMin_opt_"+region.capitalize()+"Pt.png")



    # ==== Depth =====
     
    # list of regression metrics
    metric_list  = []
    metric_list_train = []

    os.system('rm ../myMacros/classification/metric.txt')

    for param in depth_list:

        # Set datacard output directory to current var name
        new_dir = "dir = 'bdt_param_optimize/6_22_BDT_depth"+str(param)+"'\n"
        
        for line in fileinput.input('../myMacros/classification/dataCard_loop.py', inplace=True):
            
            if 'dir =' in line:
                
                print line.replace(line, new_dir),

            else: print line,
        # end file modification

        # Set the Datacard variable to current tree BDT weights
        new_bdt = "bdt: gg_plus_depth"+str(param)+".nominal\n"

        for line in fileinput.input('13TeVconfig/datacard', inplace=True):

            if 'bdt:' in line:

                print line.replace(line, new_bdt),

            else: print line,
        # end file modification
            
        os.system('python ../myMacros/classification/dataCard_loop.py')

        # Get the metric of success for each parameter iteration
        # put each iterations metric in a plot
    
        if os.path.isfile('cls_expected.txt'):
            os.system('rm cls_expected.txt')

        # Combine electron and muon
        e_card = "../limits/bdt_param_optimize/6_22_BDT_depth"+str(param)+"/vhbb_DC_TH_BDT_Zee_"+region.capitalize()+"Pt.txt"
        m_card = "../limits/bdt_param_optimize/6_22_BDT_depth"+str(param)+"/vhbb_DC_TH_BDT_Zuu_"+region.capitalize()+"Pt.txt"
        combine_card = "../limits/bdt_param_optimize/6_22_BDT_depth"+str(param)+"/vhbb_DC_TH_BDT_Combine_"+region.capitalize()+"Pt.txt"

        t8 = "combineCards.py ../limits/bdt_param_optimize/6_22_BDT_depth"+str(param)+"/vhbb_DC_TH_Zlf.txt ../limits/bdt_param_optimize/6_22_BDT_depth"+str(param)+"/vhbb_DC_TH_ttbar.txt ../limits/bdt_param_optimize/6_22_BDT_depth"+str(param)+"/vhbb_DC_TH_Zhf.txt "+e_card+" "+m_card+" > "+combine_card

        os.system(t8)

        # CLs Median expected limit
        #t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/3_25_BDT_v21_trees"+str(param)+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
        t6 = "combine -M Asymptotic -t -1 "+combine_card+" >> cls_expected.txt"
        os.system(t6)

        # get the 50% limit
        for line in fileinput.input("cls_expected.txt", inplace=True):

            if 'Expected 50.0%:' in line:

                metric = line.replace('Expected 50.0%: r < ', '')

        print 'metric: ', metric

        metric_list.append(float(metric))


        '''
        # ===== Now get the training metric ======
        # First set TrainFlag to False in cnfig/General
        new_dir = 'TrainFlag: False\n'
        for line in fileinput.input('13TeVconfig/general', inplace=True):

            if 'TrainFlag:' in line:
                print line.replace(line, new_dir),
            else: print line,
        # end file modification

        os.system('python ../myMacros/classification/dataCard_loop.py')

        if os.path.isfile('cls_expected.txt'):
            os.system('rm cls_expected.txt')

        # CLs Median expected limit
        t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/3_2_BDT_v1_depth"+str(param)+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
        os.system(t6)

        # get the 50% limit
        for line in fileinput.input("cls_expected.txt", inplace=True):

            if 'Expected 50.0%:' in line:

                metric = line.replace('Expected 50.0%: r < ', '')

        print 'Train metric: ', metric

        metric_list_train.append(float(metric))

        # Set TrainFlag back to True
        new_dir = 'TrainFlag: True\n'
        for line in fileinput.input('13TeVconfig/general', inplace=True):

            if 'TrainFlag:' in line:
                print line.replace(line, new_dir),
            else: print line,
        # end file modification
        '''


        # Store latest iteration in text file
        with open('../myMacros/classification/depth_metric.txt', 'a') as file:
            file.write('\n')
            file.write('metric:'+str(metric_list))
            #file.write('\n')
            #file.write('train:'+str(metric_list_train))



    # end paramater loop

    print 'depth Metric List: ', metric_list
    #print 'Train Metric List: ', metric_list_train

    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    h1b = TH1F('h1b', 'Depth Optimization', len(depth_list), 0, len(depth_list)+1)
    h1b.SetFillColor(4);
    h1b.SetBarWidth(0.2);
    h1b.SetBarOffset(0.0);
    h1b.SetStats(0);
    h1b.GetYaxis().SetTitle('Cls Expected 50%')
    h1b.GetXaxis().SetTitle('depth')
    h1b.SetMinimum(0);
    #h1b.SetMaximum(20);

    for i in range(0, len(depth_list)):
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(depth_list[i]))
        h1b.Draw('b')
    
    '''
    # NEW also plot the train metric in red bars
    h2b = TH1F('h2b', '', len(metric_list), 0, len(metric_list)+1)
    h2b.SetFillColor(kRed);
    h2b.SetBarWidth(0.2);
    h2b.SetBarOffset(0.2);

    for i in range(0, len(metric_list)):
        h2b.Fill(i+1, metric_list_train[i])
        h2b.Draw('bsame')
    '''

    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/depthsMin_opt_"+region.capitalize()+"Pt.pdf")
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/depthsMin_opt_"+region.capitalize()+"Pt.png")


    

    for param in nodeCut_list:
        
        # Set datacard output directory to current var name
        new_dir = "dir = 'bdt_param_optimize/6_22_BDT_nCuts"+str(param)+"'\n"
        
        for line in fileinput.input('../myMacros/classification/dataCard_loop.py', inplace=True):
            
            if 'dir =' in line:
                
                print line.replace(line, new_dir),

            else: print line,
        # end file modification

        # Set the Datacard variable to current tree BDT weights
        new_bdt = "bdt: gg_plus_nCuts"+str(param)+".nominal\n"

        for line in fileinput.input('13TeVconfig/datacard', inplace=True):

            if 'bdt:' in line:

                print line.replace(line, new_bdt),

            else: print line,
        # end file modification
            
        os.system('python ../myMacros/classification/dataCard_loop.py')

        # Get the metric of success for each parameter iteration
        # put each iterations metric in a plot
    
        if os.path.isfile('cls_expected.txt'):
            os.system('rm cls_expected.txt')
        
        # Combine electron and muon
        e_card = "../limits/bdt_param_optimize/6_22_BDT_nCuts"+str(param)+"/vhbb_DC_TH_BDT_Zee_"+region.capitalize()+"Pt.txt"
        m_card = "../limits/bdt_param_optimize/6_22_BDT_nCuts"+str(param)+"/vhbb_DC_TH_BDT_Zuu_"+region.capitalize()+"Pt.txt"
        combine_card = "../limits/bdt_param_optimize/6_22_BDT_nCuts"+str(param)+"/vhbb_DC_TH_BDT_Combine_"+region.capitalize()+"Pt.txt"

        t8 = "combineCards.py ../limits/bdt_param_optimize/6_22_BDT_nCuts"+str(param)+"/vhbb_DC_TH_Zlf.txt ../limits/bdt_param_optimize/6_22_BDT_nCuts"+str(param)+"/vhbb_DC_TH_ttbar.txt ../limits/bdt_param_optimize/6_22_BDT_nCuts"+str(param)+"/vhbb_DC_TH_Zhf.txt "+e_card+" "+m_card+" > "+combine_card
        
        print t8
        
        os.system(t8)

        # CLs Median expected limit
        #t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/3_25_BDT_v21_nCuts"+str(param)+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
        t6 = "combine -M Asymptotic -t -1 "+combine_card+" >> cls_expected.txt"
        os.system(t6)

        # get the 50% limit
        for line in fileinput.input("cls_expected.txt", inplace=True):

            if 'Expected 50.0%:' in line:

                metric = line.replace('Expected 50.0%: r < ', '')

        print 'metric: ', metric

        metric_list.append(float(metric))
        
        # Store latest iteration in text file
        with open('../myMacros/classification/metric.txt', 'a') as file:
            file.write('\n')
            file.write('metric:'+str(metric_list))
                #file.write('\n')
                #file.write('train:'+str(metric_list_train))
        
    # end paramater loop

    # Testing
    #metric_list = [4.7344, 3.8281, 3.2344, 3.1406, 2.8672, 3.2656, 3.1719, 3.0078, 2.9766, 2.8516, 2.8984, 3.1719, 3.1172, 3.125]
    #metric_list_train = [4.1406, 2.5391, 2.5703, 2.3359, 2.1641, 2.0859, 2.0703, 2.1016, 2.0234, 1.6953, 1.6797, 1.7422, 1.5547, 1.3867]
    
    print 'nCut Metric List: ', metric_list
    #print 'Train Metric List: ', metric_list_train

    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()
    
    h1b = TH1F('h1b', 'nCuts Optimization', len(nodeCut_list), 0, len(nodeCut_list)+1)
    h1b.SetFillColor(4)
    h1b.SetBarWidth(0.2)
    h1b.SetBarOffset(0.0)
    h1b.SetStats(0)
    h1b.GetYaxis().SetTitle('Cls Expected 50%')
    h1b.GetXaxis().SetTitle('NCuts')
    
    h1b.SetMinimum(0)
    #h1b.SetMaximum(20);

    for i in range(0, len(nodeCut_list)):
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(nodeCut_list[i]))
        h1b.Draw('b')

    
    #cR.SaveAs('../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_nCuts_highPt_ratio.pdf')
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_nCuts_"+region.capitalize()+"Pt.pdf")
    cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_nCuts_"+region.capitalize()+"Pt.png")

    # ===================================================================================================
    # end tree loop
 



# ===================================================================================================
# end depth loop



raw_input('press return to continue')
