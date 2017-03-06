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
from ROOT import gROOT
gROOT.SetBatch(True)

outpath = '/afs/cern.ch/user/d/dcurry/www/v25_BDT_BinOptimize2/'

try: os.system('mkdir '+outpath)
except: print outpath+' already exists...'
temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outpath
os.system(temp_string2)
os.system(temp_string3)


bin_list = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,30]
#bin_list = [10,20]

#an_type = 'VV'
an_type = 'VH'

metric_list  = []

for bin in bin_list:
    break
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
    new_dir = "dir= 'bdt_param_optimize/BDT_bins"+str(bin)+"'\n"
    for line in fileinput.input('../myMacros/classification/dataCard_loop.py', inplace=True):
        if 'dir=' in line:
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
#                10        11        12      13       14       15       16       17       18      19         20       21      22      23       24      25        30  
metric_list = [1.74255, 1.75735, 1.76061, 1.75754, 1.75645, 1.76068, 1.75923, 1.76551, 1.75976, 1.76537, 1.76385, 1.76413, 1.76367, 1.76844, 1.77271, 1.77178, 1.77037]
print 'Bin Metric List: ', metric_list
    
# fill accuracy plots
cStd = TCanvas('cStd')
cStd.SetGrid()

h1b = TH1F('h1b', 'BDT Bin Optimization', len(bin_list), 0, len(bin_list)+1)
h1b.SetFillColor(1)
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
    
cStd.SaveAs(outpath+"bdt_binOptimize_"+an_type+".pdf")
cStd.SaveAs(outpath+"bdt_binOptimize_"+an_type+".png")
    
print '\n.... Finished!'
