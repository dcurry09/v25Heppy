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


bin_list = [10,15,20,25,30,35,40,45,50]

pt_region_list = ['low','high']

#an_type = 'VV'
an_type = 'VH'

#for region in pt_region_list:

# clear the temp files from last datacard iteration
#os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')

metric_list  = []

for bin in bin_list:
        
    print '\n\n\t Looping Over Bin: ', bin

    # Go into datacard.config
    new_dir = "BDTrange: "+str(bin)+",-1,1\n"
    for line in fileinput.input('13TeVconfig/datacard', inplace=True):
        if 'BDTrange:' in line:
            print line.replace(line, new_dir),
        else: print line,
    # end file modification

    print '\n\n\t Setting DC Directory...'
             
    # Set datacard output directory to current var name
    new_dir = "dir = 'bdt_param_optimize/BDT_bins"+str(bin)+"'\n"
    for line in fileinput.input('../myMacros/classification/dataCard_loop.py', inplace=True):
        if 'dir =' in line:
            print line.replace(line, new_dir),
        else: print line,
    # end file modification

         
    os.system('python ../myMacros/classification/dataCard_loop.py')
         
    if os.path.isfile('cls_expected.txt'):
        os.system('rm cls_expected.txt')
             
    print '\n\n\t Combining Datacards...'

    # Combine electron and muon
    e_low_card = "../limits/bdt_param_optimize/BDT_bins"+str(bin)+"/vhbb_DC_TH_BDT_Zee_LowPt.txt"
    m_low_card = "../limits/bdt_param_optimize/BDT_bins"+str(bin)+"/vhbb_DC_TH_BDT_Zuu_LowPt.txt"

    e_high_card = "../limits/bdt_param_optimize/BDT_bins"+str(bin)+"/vhbb_DC_TH_BDT_Zee_HighPt.txt"
    m_high_card = "../limits/bdt_param_optimize/BDT_bins"+str(bin)+"/vhbb_DC_TH_BDT_Zuu_HighPt.txt"

    combine_card = "../limits/bdt_param_optimize/BDT_bins"+str(bin)+"/vhbb_DC_TH_BDT_Combine_AllPt.txt"

    t8 = "combineCards.py ../limits/temp/vhbb_DC_TH_Zlf_high_Zee.txt ../limits/temp/vhbb_DC_TH_ttbar_high_Zee.txt ../limits//temp/vhbb_DC_TH_Zhf_high_Zee.txt ../limits/temp/vhbb_DC_TH_Zlf_low_Zee.txt ../limits/temp/vhbb_DC_TH_ttbar_low_Zee.txt ../limits//temp/vhbb_DC_TH_Zhf_low_Zee.txt ../limits/temp/vhbb_DC_TH_Zlf_high_Zuu.txt ../limits/temp/vhbb_DC_TH_ttbar_high_Zuu.txt ../limits//temp/vhbb_DC_TH_Zhf_high_Zuu.txt ../limits/temp/vhbb_DC_TH_Zlf_low_Zuu.txt ../limits/temp/vhbb_DC_TH_ttbar_low_Zuu.txt ../limits//temp/vhbb_DC_TH_Zhf_low_Zuu.txt "+e_low_card+" "+m_low_card+" "+e_high_card+" "+m_high_card+" > "+combine_card

    print t8
         
    os.system(t8)
        
    # CLs Median expected limit
    t6 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 "+combine_card+" >> cls_expected.txt"
    os.system(t6)

    # get the 50% limit
    for line in fileinput.input("cls_expected.txt", inplace=True):

        if '(Significance =' in line:
            metric1 = line.replace('(Significance = ', '')
            metric = metric1.replace(')', '')
            metric_list.append(float(metric))
         
    print 'metric: ', metric
    print metric_list

# end loop         

print 'Bin Metric List: ', metric_list
    
# fill accuracy plots
cStd = TCanvas('cStd')
cStd.SetGrid()

h1b = TH1F('h1b', 'BDT Bin Optimization', len(bin_list), 0, len(bin_list)+1)
h1b.SetFillColor(4)
h1b.SetBarWidth(0.2)
h1b.SetBarOffset(0.0)
h1b.SetStats(0)
h1b.GetYaxis().SetTitle('Expected Significance')
h1b.GetXaxis().SetTitle('Bins')

h1b.SetMinimum(0)
    
for i in range(0, len(bin_list)):
    h1b.Fill(i+1, metric_list[i])
    h1b.GetXaxis().SetBinLabel(i+1, str(bin_list[i]))
    h1b.Draw('b')
    
cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_binOptimize_"+an_type+".pdf")
cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_binOptimize_"+an_type+"png")
    
print '\n.... Finished!'
