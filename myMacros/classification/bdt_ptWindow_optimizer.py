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

# Higgs Mass Window
h_mass_low_list = [70, 80, 90, 100, 110, 120]
#h_mass_low_list = [100, 110, 120]
h_mass_high_list = [100, 110, 120, 130, 140, 150, 160, 170]

#h_mass_low_list = []
#h_mass_high_list = []



print '\n======================== Starting BDT Paramter Optimiziation ========================'
print '=====================================================================================\n'

window_list = []

# list of regression metrics
metric_list  = []

for lowCut in h_mass_low_list:
    for highCut in h_mass_high_list:

        if lowCut >= highCut: continue

        window_list.append(str(lowCut)+'_'+str(highCut))

        # Set datacard output directory to current var name
        new_dir = "dir = 'bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"'\n"
        
        for line in fileinput.input('../myMacros/classification/dataCard_loop.py', inplace=True):

            if 'dir =' in line:

                print line.replace(line, new_dir),

            else: print line,
        # end file modification
        
        # new jet pt cut string
        new_lowCut = 'Vpt_low_window: V_pt > 50. & V_pt < '+str(lowCut)+' & H_pt < 999. & H_pt > 0. & H_mass < 9999. & H_mass > 0.\n'
        print new_lowCut

        for line in fileinput.input("13TeVconfig/cuts", inplace=True):

            if 'Vpt_low_window:' in line:

                print line.replace(line, new_lowCut),

            else: print line,
        # end file modification

        new_medCut = 'Vpt_med_window: V_pt > '+str(lowCut)+' & V_pt < '+str(highCut)+' & H_pt < 999. & H_pt > 0. & H_mass < 9999. & H_mass > 0.\n'
        print new_medCut

        for line in fileinput.input("13TeVconfig/cuts", inplace=True):

            if 'Vpt_med_window:' in line:

                print line.replace(line, new_medCut),

            else: print line,
        # end file modification

        new_highCut = 'Vpt_high_window: V_pt > '+str(highCut)+'. & H_pt < 999. & H_pt > 0. & H_mass < 9999. & H_mass > 0. & V_pt < 2000.\n'
        print new_highCut

        for line in fileinput.input("13TeVconfig/cuts", inplace=True):

            if 'Vpt_high_window:' in line:

                print line.replace(line, new_highCut),

            else: print line,
        # end file modification
            
        os.system('python ../myMacros/classification/dataCard_loop.py')
        
        if os.path.isfile('cls_expected.txt'):
            os.system('rm cls_expected.txt')

        # Copy over the control regions
        cp = "cp ../limits/bdt_param_optimize/6_22_BDT_depth1/vhbb_TH_Zlf.root ../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)
        os.system(cp)
        cp = "cp ../limits/bdt_param_optimize/6_22_BDT_depth1/vhbb_DC_TH_Zlf.txt ../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)
        os.system(cp)

        cp = "cp ../limits/bdt_param_optimize/6_22_BDT_depth1/vhbb_TH_Zhf.root ../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)
        os.system(cp)
        cp = "cp ../limits/bdt_param_optimize/6_22_BDT_depth1/vhbb_DC_TH_Zhf.txt ../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)
        os.system(cp)
        
        cp = "cp ../limits/bdt_param_optimize/6_22_BDT_depth1/vhbb_TH_ttbar.root ../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)
        os.system(cp)
        cp = "cp ../limits/bdt_param_optimize/6_22_BDT_depth1/vhbb_DC_TH_ttbar.txt ../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)
        os.system(cp)

        zlf = "../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_Zlf.txt"
        zhf = "../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_Zhf.txt"
        ttbar = "../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_ttbar.txt"

        # Combine electron and muon
        e_low= "../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_BDT_Zee_LowPt.txt"
        m_low = "../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_BDT_Zuu_LowPt.txt"
        low_combine_card = "../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_BDT_Combine_LowPt.txt"

        e_med= "../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_BDT_Zee_MedPt.txt"
        m_med = "../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_BDT_Zuu_MedPt.txt"
        med_combine_card = "../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_BDT_Combine_MedPt.txt"

        e_high= "../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_BDT_Zee_HighPt.txt"
        m_high = "../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_BDT_Zuu_HighPt.txt"
        high_combine_card = "../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_BDT_Combine_HighPt.txt"


        print '----> Combine All pT Bins...'
        t_total = "combineCards.py "+e_low+" "+m_low+" "+e_med+" "+m_med+" "+e_high+" "+m_high+" "+zlf+" "+zhf+" "+ttbar+" > ../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_BDT_Combine_AllPt.txt"
        os.system(t_total)
        
        '''
        print '----> Combine Low pT...'
        t_low = "combineCards.py ../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_Zlf.txt ../limits/bdt_param_optimize/6_22_BDT_depth1/vhbb_DC_TH_ttbar.txt ../limits/bdt_param_optimize/6_22_BDT_depth1/vhbb_DC_TH_Zhf.txt "+e_low+" "+m_low+" > "+low_combine_card
        os.system(t_low)

        print '----> Combine Med pT...'
        t_med = "combineCards.py ../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_Zlf.txt ../limits/bdt_param_optimize/6_22_BDT_depth1/vhbb_DC_TH_ttbar.txt ../limits/bdt_param_optimize/6_22_BDT_depth1/vhbb_DC_TH_Zhf.txt "+e_med+" "+m_med+" > "+med_combine_card
        os.system(t_med)

        print '----> Combine High pT...'
        t_high = "combineCards.py ../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_Zlf.txt ../limits/bdt_param_optimize/6_22_BDT_depth1/vhbb_DC_TH_ttbar.txt ../limits/bdt_param_optimize/6_22_BDT_depth1/vhbb_DC_TH_Zhf.txt "+e_high+" "+m_high+" > "+high_combine_card
        os.system(t_high)

        print '----> Combine All pT Bins...'
        t_total = "combineCards.py "+low_combine_card+" "+med_combine_card+" "+high_combine_card+" > ../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_BDT_Combine_AllPt.txt"
        os.system(t_total)
        '''
        
        print '----> Calculate CLs Limit...'
        #t6 = "combine -M Asymptotic -t -1 ../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_BDT_Combine_AllPt.txt >> cls_expected.txt"
        t6 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 ../limits/bdt_param_optimize/8_30_vPt"+str(lowCut)+"_"+str(highCut)+"/vhbb_DC_TH_BDT_Combine_AllPt.txt >> cls_expected.txt"
        os.system(t6)
        
        # get the 50% limit
        for line in fileinput.input("cls_expected.txt", inplace=True):

            if '(Significance =' in line:

                metric = line.replace('(Significance =', '')
                metric = metric.replace(')', '')
        
        print 'metric: ', metric

        metric_list.append(float(metric))

        # Store latest iteration in text file
        with open('../myMacros/classification/nEvt_metric.txt', 'a') as file:
            file.write('\n')
            file.write('metric:'+str(metric_list))


# end paramater loop

#metric_list = [0.639328, 0.633137, 0.641397, 0.640213, 0.640764, 0.646926, 0.639491, 0.619561, 0.639679, 0.634398, 0.643273, 0.642153, 0.643633, 0.653245, 0.644384, 0.624047, 0.640276, 0.635259, 0.645153, 0.646061, 0.644597, 0.653108, 0.648758, 0.629152, 0.664299, 0.675524, 0.775235, 0.843787, 0.683979, 0.679311, 0.664636, 0.701423, 0.775793, 0.840956, 0.709789, 0.700867, 0.690505, 0.69644, 0.768167, 0.659152, 0.648744, 0.631683]

print 'Window Metric List: ', metric_list

print window_list
         
# fill accuracy plots
cStd = TCanvas('cStd')
cStd.SetGrid()

h1b = TH1F('h1b', 'Vpt Region Optimization', len(metric_list), 0, len(metric_list)+1)
h1b.SetFillColor(4);
h1b.SetBarWidth(0.2);
h1b.SetBarOffset(0.0);
h1b.SetStats(0);
h1b.GetYaxis().SetTitle('Significance(exp)')
h1b.GetXaxis().SetTitle('Vpt regions')
h1b.SetMinimum(0);

for i in range(0, len(metric_list)):
    h1b.Fill(i+1, metric_list[i])
    h1b.GetXaxis().SetBinLabel(i+1, str(window_list[i]))
    h1b.GetXaxis().SetLabelSize(.01)
    h1b.Draw('b')
    
cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/Vpt_region_Opt.pdf")
#cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/nEvtsMin_opt_"+region.capitalize()+"Pt.png")




