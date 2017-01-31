
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
#node_cut = True

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
tree_list = [300, 350, 400, 450, 500, 600, 700, 900, 1000]
#tree_list = [250]#, 300, 500, 700, 900, 1000, 1500, 2000]

# learning rate(shrinkage)
lr_list = [0.01, 0.1, 0.12, 0.15, 0.2, 0.3, 0.5, 1]

# node search space size. TMVA default is 20 
nodeCut_list = [5, 10, 15, 20, 50, 100, 250, 500, 750, 1000]
#nodeCut_list = [750, 1000]

# number of events for node minimum
nEventsMin_list = [0.01, 0.05, 1, 2, 3, 4, 5, 10, 15, 20]


# Higgs Mass Window
h_mass_low_list = [80, 85, 90, 95, 100]
h_mass_high_list = [105, 130, 140, 150, 160]

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


if trees:

    # list of regression metrics
    metric_list  = []
    metric_list_train = []

    os.system('rm ../myMacros/classification/metric.txt')

    # loop over parmater list
    for param in tree_list:

        print '\n\n======================== Starting New Tree Loop  ========================'
        print '=============================================================================='
        print '----> Looping over parameter: ', param 
                

        # clear the temp files from last datacard iteration
        #os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')


        # new BDT option string
        new_options = 'SettingsTight: !H:!V:NTrees='+str(param)+':MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.12:SeparationType=MisClassificationError:nCuts=25\n'
        
        for line in fileinput.input("13TeVconfig/training", inplace=True):
            
            if 'SettingsTight:' in line:
                
                print line.replace(line, new_options),
                
            else: print line,
        # end file modification

        # Now train the BDT on new option list/ modified file
        os.system('python ../myMacros/classification/bdt_classifier_training_loop.py')


        # Copy the MVA outfile for each iteration for plots later
        tfile = 'cp ../data/MVA_gg_plus_ZH125_looseHMass.root ../data/param_optimization/MVA_gg_plus_ZH125_highZpt_trees'+str(param)+'.root'
        os.system(tfile)
        
     
        # Apply the BDT weights to samples
        os.system('python ../myMacros/classification/bdt_classifier_eval_loop.py')
        
        # Make the datacards for new training
        # Set datacard output directory to current var name
        new_dir = "dir = 'bdt_param_optimize/3_25_BDT_v21_trees"+str(param)+"'\n"
        
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

        # Combine electron and muon
        e_card = "../limits/bdt_param_optimize/3_25_BDT_v21_trees"+str(param)+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt"
        m_card = "../limits/bdt_param_optimize/3_25_BDT_v21_trees"+str(param)+"/vhbb_DC_TH_BDT_M125_Zuu_HighPt.txt"
        combine_card = "../limits/bdt_param_optimize/3_25_BDT_v21_trees"+str(param)+"/vhbb_DC_TH_BDT_M125_Combine_HighPt.txt"

        t8 = "combineCards.py "+e_card+" "+m_card+" > "+combine_card
        
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
        t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/3_25_BDT_v21_trees"+str(param)+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
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

    '''
    # NEW also plot the train metric in red bars
    h2b = TH1F('h2b', '', len(tree_list), 0, len(tree_list)+1)
    h2b.SetFillColor(kRed);
    h2b.SetBarWidth(0.2);
    h2b.SetBarOffset(0.2);
   

    for i in range(0, len(tree_list)):
        h2b.Fill(i+1, metric_list_train[i])
        h2b.Draw('bsame')

    # Ratio Plot
    cR = TCanvas('cR', '', 700,300)
    cR.cd()
    h3b = TH1F('h3b', '', len(tree_list), 0, len(tree_list)+1)
    h3b.SetStats(0)
    h3b.SetMarkerSize(4)
    h3b.SetMarkerStyle(1)
    h3b.SetMarkerColor(kRed)
    h3b.GetXaxis().SetLabelSize(0.1)
    h3b.GetYaxis().SetTitle('Test - Train')
    h3b.GetXaxis().SetTitle('Trees')

    for i in range(0, len(tree_list)):
        h3b.Fill(i+1, metric_list[i] - metric_list_train[i])
        h3b.GetXaxis().SetBinLabel(i+1, str(tree_list[i]))
        h3b.Draw()
    '''

    #cR.SaveAs('../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_trees_highPt_ratio.pdf')
    cStd.SaveAs('../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_trees_highPt.pdf')


# ===================================================================================================
# end tree loop


if lr:

    # list of regression metrics
    metric_list  = []
    metric_list_train = []

    os.system('rm ../myMacros/classification/lr_metric.txt')


    # loop over parmater list
    for param in lr_list:
        
        print '\n\n======================== Starting New LR Loop  ========================'
        print '=============================================================================='
        print '----> Looping over parameter: ', param 
                

        # clear the temp files from last datacard iteration
        os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')


        # new BDT option string
        new_options = 'SettingsTight: !H:!V:NTrees=150:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta='+str(param)+':SeparationType=MisClassificationError:nCuts=25\n'
        
        for line in fileinput.input("13TeVconfig/training", inplace=True):
            
            if 'SettingsTight:' in line:
                
                print line.replace(line, new_options),
                
            else: print line,
        # end file modification

        # Now train the BDT on new option list/ modified file
        os.system('python ../myMacros/classification/bdt_classifier_training_loop.py')

        
        # Copy the MVA outfile for each iteration for plots later
        tfile = 'cp ../data/MVA_gg_plus_ZH125_highZpt.root ../data/param_optimization/MVA_gg_plus_ZH125_highZpt_LR'+str(param)+'.root'
        os.system(tfile)
        
        
        # Apply the BDT weights to samples
        os.system('python ../myMacros/classification/bdt_classifier_eval_loop.py')

        # Make the datacards for new training
        # Set datacard output directory to current var name
        new_dir = "dir = 'bdt_param_optimize/3_2_BDT_v1_LR"+str(param)+"'\n"

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
        
        # CLs Median expected limit
        t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/3_2_BDT_v1_LR"+str(param)+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
        os.system(t6)

        # get the 50% limit
        for line in fileinput.input("cls_expected.txt", inplace=True):

            if 'Expected 50.0%:' in line:

                metric = line.replace('Expected 50.0%: r < ', '')

        print 'metric: ', metric

        metric_list.append(float(metric))


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
        t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/3_2_BDT_v1_LR"+str(param)+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
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


        # Store latest iteration in text file
        with open('../myMacros/classification/lr_metric.txt', 'a') as file:
            file.write('\n')
            file.write('metric:'+str(metric_list))
            file.write('\n')
            file.write('train:'+str(metric_list_train))

    # end paramater loop

    print 'LR Metric List: ', metric_list
    print 'LR Train Metric List: ', metric_list_train


    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    h1b = TH1F('h1b', 'Learning Rate Optimization', len(lr_list), 0, len(lr_list)+1)
    h1b.SetFillColor(4);
    h1b.SetBarWidth(0.2);
    h1b.SetBarOffset(0.0);
    h1b.SetStats(0);
    h1b.GetYaxis().SetTitle('Cls Expected 50%')
    h1b.GetXaxis().SetTitle('LR')
    h1b.SetMinimum(0);
    #h1b.SetMaximum(20);

    for i in range(0, len(lr_list)):
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(lr_list[i]))
        h1b.Draw('b')

    # NEW also plot the train metric in red bars
    h2b = TH1F('h2b', '', len(metric_list), 0, len(metric_list)+1)
    h2b.SetFillColor(kRed);
    h2b.SetBarWidth(0.2);
    h2b.SetBarOffset(0.2);

    for i in range(0, len(metric_list)):
        h2b.Fill(i+1, metric_list_train[i])
        h2b.Draw('bsame')


    cStd.SaveAs('../myMacros/classification/bdt_optimization_plots/lr_opt_lowPt.pdf')

# ===================================================================================================
# end lr loop

 
if nEvt:

    # list of regression metrics
    metric_list  = []
    metric_list_train = []

    os.system('rm ../myMacros/classification/nEvt_metric.txt')


    # loop over parmater list
    for param in nEventsMin_list:

        print '\n\n======================== Starting New nEvt Loop  ========================'
        print '=============================================================================='
        print '----> Looping over parameter: ', param


        # clear the temp files from last datacard iteration
        #os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')


        # new BDT option string
        new_options = 'SettingsTight: !H:!V:NTrees=400:MinNodeSize='+str(param)+'%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.12:SeparationType=MisClassificationError\n'

        for line in fileinput.input("13TeVconfig/training", inplace=True):

            if 'SettingsTight:' in line:

                print line.replace(line, new_options),

            else: print line,
        # end file modification

        # Now train the BDT on new option list/ modified file
        os.system('python ../myMacros/classification/bdt_classifier_training_loop.py')


        # Copy the MVA outfile for each iteration for plots later
        tfile = 'cp ../data/MVA_gg_plus_ZH125_highZpt.root ../data/param_optimization/MVA_gg_plus_ZH125_highZpt_nEvt'+str(param)+'.root'
        os.system(tfile)
        
        # Apply the BDT weights to samples
        os.system('python ../myMacros/classification/bdt_classifier_eval_loop.py')

        # Make the datacards for new training
        # Set datacard output directory to current var name
        new_dir = "dir = 'bdt_param_optimize/3_2_BDT_v1_nEvt"+str(param)+"'\n"
        
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

        # Combine electron and muon
        e_card = "../limits/bdt_param_optimize/3_25_BDT_v1_nEvt"+str(param)+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt"
        m_card = "../limits/bdt_param_optimize/3_25_BDT_v1_nEvt"+str(param)+"/vhbb_DC_TH_BDT_M125_Zuu_HighPt.txt"
        combine_card = "../limits/bdt_param_optimize/3_25_BDT_v1_nEvt"+str(param)+"/vhbb_DC_TH_BDT_M125_Combine_HighPt.txt"

        t8 = "combineCards.py "+e_card+" "+m_card+" > "+combine_card

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
        t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/3_2_BDT_v1_nEvt"+str(param)+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
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
        with open('../myMacros/classification/nEvt_metric.txt', 'a') as file:
            file.write('\n')
            file.write('metric:'+str(metric_list))
            #file.write('\n')
            #file.write('train:'+str(metric_list_train))



    # end paramater loop

    print 'nEvt Metric List: ', metric_list
    #print 'Train Metric List: ', metric_list_train

    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    h1b = TH1F('h1b', 'nEvents Min Optimization', len(nEventsMin_list), 0, len(nEventsMin_list)+1)
    h1b.SetFillColor(4);
    h1b.SetBarWidth(0.2);
    h1b.SetBarOffset(0.0);
    h1b.SetStats(0);
    h1b.GetYaxis().SetTitle('Cls Expected 50%')
    h1b.GetXaxis().SetTitle('nEvtMin(%)')
    h1b.SetMinimum(0);
    #h1b.SetMaximum(20);

    for i in range(0, len(nEventsMin_list)):
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(nEventsMin_list[i]))
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

    cStd.SaveAs('../myMacros/classification/bdt_optimization_plots/nEvtsMin_opt_lowPt.pdf')

# ===================================================================================================
# end nEvt loop


if node_cut:

    # list of regression metrics
    metric_list  = []
    metric_list_train = []

    os.system('rm ../myMacros/classification/node_metric.txt')

    # loop over parmater list
    for param in nodeCut_list:
        
        break
         
        print '\n\n======================== Starting New Node Cut Loop  ========================'
        print '=============================================================================='
        print '----> Looping over parameter: ', param


        # clear the temp files from last datacard iteration
        os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')


        # new BDT option string
        new_options = 'SettingsTight: !H:!V:NTrees=150:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.12:SeparationType=MisClassificationError:nCuts='+str(param)+'\n'

        for line in fileinput.input("13TeVconfig/training", inplace=True):

            if 'SettingsTight:' in line:

                print line.replace(line, new_options),

            else: print line,
        # end file modification

        # Now train the BDT on new option list/ modified file
        os.system('python ../myMacros/classification/bdt_classifier_training_loop.py')
            

        # Copy the MVA outfile for each iteration for plots later
        tfile = 'cp ../data/MVA_gg_plus_ZH125_highZpt.root ../data/param_optimization/MVA_gg_plus_ZH125_highZpt_nodeCuts'+str(param)+'.root'
        os.system(tfile)

        # Apply the BDT weights to samples
        os.system('python ../myMacros/classification/bdt_classifier_eval_loop.py')

        # Make the datacards for new training
        # Set datacard output directory to current var name
        new_dir = "dir = 'bdt_param_optimize/3_2_BDT_v1_nodeCut"+str(param)+"'\n"

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

        # CLs Median expected limit
        t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/3_2_BDT_v1_nodeCut"+str(param)+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
        os.system(t6)

        # get the 50% limit
        for line in fileinput.input("cls_expected.txt", inplace=True):

            if 'Expected 50.0%:' in line:

                metric = line.replace('Expected 50.0%: r < ', '')

        print 'metric: ', metric

        metric_list.append(float(metric))

        print metric_list

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
        t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/3_2_BDT_v1_nodeCut"+str(param)+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
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

        # Store latest iteration in text file
        with open('../myMacros/classification/node_metric.txt', 'a') as file:
            file.write('\n')
            file.write('metric:'+str(metric_list))
            file.write('\n')
            file.write('train:'+str(metric_list_train))

    # end paramater loop
            
    # Temp Hack
    metric_list = [3.6406, 4.0781, 3.1719, 3.2969, 3.2344, 3.7344, 3.7344, 3.5469,3.6719, 3.3281]
    metric_list_train = [2.8516, 2.4609, 2.3359, 2.1016, 2.3359, 2.2734, 2.3516, 2.1016,1.9609, 1.9766]

    print 'node Cut Metric List: ', metric_list
    print 'Train Metric List: ', metric_list_train

    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    h1b = TH1F('h1b', 'Node Cut Optimization', len(nodeCut_list), 0, len(nodeCut_list)+1)
    h1b.SetFillColor(4);
    h1b.SetBarWidth(0.2);
    h1b.SetBarOffset(0.0);
    h1b.SetStats(0);
    h1b.GetYaxis().SetTitle('Cls Expected 50%')
    h1b.GetXaxis().SetTitle('# Node Cuts')
    h1b.SetMinimum(0);
    #h1b.SetMaximum(20);

    for i in range(0, len(nodeCut_list)):
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(nodeCut_list[i]))
        h1b.Draw('b')

    
    # NEW also plot the train metric in red bars
    h2b = TH1F('h2b', '', len(metric_list), 0, len(metric_list)+1)
    h2b.SetFillColor(kRed);
    h2b.SetBarWidth(0.2);
    h2b.SetBarOffset(0.2);

    for i in range(0, len(metric_list)):
        h2b.Fill(i+1, metric_list_train[i])
        h2b.Draw('bsame')


    cStd.SaveAs('../myMacros/classification/bdt_optimization_plots/nodeCut_opt_lowPt.pdf')

# ===================================================================================================
# end node_cut loop



if hMass:

    # list of regression metrics
    metric_list  = []

    window_list =[]

    # loop over parmater list
    # loop over parmater list
    for h_low in h_mass_low_list:
        for h_high in h_mass_high_list:
        
             window_list.append(str(h_low)+'_'+str(h_high))
            
             print '\n\n======================== Starting New HMASS Loop  ========================'
             print '=============================================================================='

             # clear the temp files from last datacard iteration
             os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')

             # new jet pt cut string
             new_options = 'looseHMass: (HCSV_reg_mass < '+str(h_high)+' && HCSV_reg_mass > '+str(h_low)+')\n'
             print new_options
        
             for line in fileinput.input("13TeVconfig/cuts", inplace=True):
            
                 if 'looseHMass:' in line:
                
                     print line.replace(line, new_options),
                
                 else: print line,
             # end file modification

             # Now train the BDT on new option list/ modified file
             os.system('python ../myMacros/classification/bdt_classifier_training_loop.py')

             
             # Apply the BDT weights to samples
             os.system('python ../myMacros/classification/bdt_classifier_eval_loop.py')

             # Make the datacards for new training
             # Set datacard output directory to current var name
             window = str(h_low)+str(h_high)
             
             new_dir = "dir = 'bdt_param_optimize/3_2_BDT_v1_hmass"+window+"'\n"

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
        
             # CLs Median expected limit
             t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/3_2_BDT_v1_hmass"+window+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
             os.system(t6)

             # get the 50% limit
             for line in fileinput.input("cls_expected.txt", inplace=True):

                 if 'Expected 50.0%:' in line:

                     metric = line.replace('Expected 50.0%: r < ', '')

             print 'metric: ', metric
             metric_list.append(float(metric))
             
             print metric_list

    # end paramater loop
    print 'HMass Metric List: ', metric_list
    
    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    h1b = TH1F('h1b', 'H_mass Window Optimization', len(metric_list), 0, len(metric_list)+1)
    h1b.SetFillColor(4);
    h1b.SetBarWidth(0.4);
    h1b.SetBarOffset(0.0);
    h1b.SetStats(0);
    h1b.GetYaxis().SetTitle('Cls Expected 50%')
    h1b.GetXaxis().SetTitle('H mass')
    #h1b.SetMinimum(10);
    #h1b.SetMaximum(20);

    for i in range(0, len(metric_list)):
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(window_list[i]))
        h1b.Draw('b')

    cStd.SaveAs('../myMacros/classification/bdt_optimization_plots/hMass_opt.pdf')

# ===================================================================================================
# end Higgs MAss loop




if vPt:
    '''
    # list of regression metrics
    metric_list  = []

    # loop over parmater list
    # loop over parmater list
    #for v_low in v_mass_low_list:
    #    for v_high in v_mass_high_list:
    for vPt in v_pt_list:

     
             #window_list.append(str(h_low)+'_'+str(h_high))
        
             print '\n\n======================== Starting New V Pt Loop  ========================'
             print '=============================================================================='
             
             # clear the temp files from last datacard iteration
             os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')
             
             # new jet pt cut string
             new_options = 'Vpt_100: V_pt > '+str(vPt)+' & V_pt < 1000\n'
             print new_options
        
             for line in fileinput.input("13TeVconfig/cuts", inplace=True):
            
                 if 'Vpt_100:' in line:
                
                     print line.replace(line, new_options),
                
                 else: print line,
             # end file modification

             # Also modify the low V pT cut
             new_options = 'Vpt_low_window: V_pt > 50. & V_pt <'+str(vPt)+'\n'
             print new_options

             for line in fileinput.input("13TeVconfig/cuts", inplace=True):

                 if 'Vpt_low_window:' in line:

                     print line.replace(line, new_options),

                 else: print line,
             # end file modification


             # Now train the BDT on new option list/ modified file
             os.system('python ../myMacros/classification/bdt_classifier_training_loop.py')
                 
             # Apply the BDT weights to samples
             os.system('python ../myMacros/classification/bdt_classifier_eval_loop.py')
             
             # Make the datacards for new training
             # Set datacard output directory to current var name
             window = str(vPt)
             
             new_dir = "dir = 'bdt_param_optimize/4_25_BDT_Vpt"+window+"'\n"
             
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
        
             # Combine the low and high DC
             temp_string = "combineCards.py ../limits/bdt_param_optimize/4_25_BDT_Vpt"+window+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt ../limits/bdt_param_optimize/4_25_BDT_Vpt"+window+"/vhbb_DC_TH_BDT_M125_Zee_LowPt.txt > ../limits/bdt_param_optimize/4_25_BDT_Vpt"+window+"/vhbb_DC_TH_Electron_Muon_Combined.txt"
                 
             os.system(temp_string)
             
             
             # CLs Median expected limit
             t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/4_25_BDT_Vpt"+window+"/vhbb_DC_TH_Electron_Muon_Combined.txt >> cls_expected.txt"
             os.system(t6)

             # get the 50% limit
             for line in fileinput.input("cls_expected.txt", inplace=True):

                 if 'Expected 50.0%:' in line:

                     metric = line.replace('Expected 50.0%: r < ', '')

             print 'metric: ', metric
             metric_list.append(float(metric))
             
             print metric_list
    '''         
    # end paramater loop
    [60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
    metric_list = [6.2812, 6.3438, 6.1094, 6.2812, 6.2812, 6.2912, 6.3125, 6.3820, 6.3820, 6.400]
    
    print 'Vpt Metric List: ', metric_list
    


    # fill accuracy plots
    cStd = TCanvas('cStd')
    cStd.SetGrid()

    h1b = TH1F('h1b', 'V_pT Optimization', len(metric_list), 0, len(metric_list)+1)
    h1b.SetFillColor(4);
    h1b.SetBarWidth(0.4);
    h1b.SetBarOffset(0.0);
    h1b.SetStats(0);
    h1b.GetYaxis().SetTitle('Cls Expected 50%')
    h1b.GetXaxis().SetTitle('V_pT')
    h1b.SetMinimum(0);
    #h1b.SetMaximum(20);

    for i in range(0, len(metric_list)):
        h1b.Fill(i+1, metric_list[i])
        h1b.GetXaxis().SetBinLabel(i+1, str(v_pt_list[i]))
        h1b.Draw('b')

    cStd.SaveAs('../myMacros/classification/bdt_optimization_plots/Vpt_opt.pdf')

# ===================================================================================================
# end V Pt loop




raw_input('press return to continue')
