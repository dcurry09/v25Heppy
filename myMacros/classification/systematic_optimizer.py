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


# Define the systematiuc list
sys_list_1 = ['AllSYS', 'JER','JEC','bTagWeight_HF','bTagWeight_LF','bTagWeight_LFStats1','bTagWeight_LFStats2','bTagWeight_HFStats1','bTagWeight_HFStats2','bTagWeight_cErr1','bTagWeight_cErr2']


full_sys_list_1 =  "sys_BDT: ['JER','JEC','bTagWeight_HF','bTagWeight_LF','bTagWeight_LFStats1','bTagWeight_LFStats2','bTagWeight_HFStats1','bTagWeight_HFStats2','bTagWeight_cErr1','bTagWeight_cErr2']\n"

sys_list_2 = ['lumi_13TeV', 'pdf_qqbar', 'pdf_gg', 'QCDscale_VH', 'QCDscale_ttbar','QCDscale_VV','QCDscale_QCD', 'QCDscale_VH_ggZHacceptance_lowPt', 'QCDscale_VH_ggZHacceptance_highPt', 'CMS_vhbb_boost_EWK_13TeV', 'CMS_vhbb_boost_QCD_13TeV','CMS_vhbb_ST','CMS_vhbb_VV', 'CMS_vhbb_eff_e_13TeV', 'CMS_vhbb_eff_m_13TeV']

full_sys_list_2 =  "InUse: ['lumi_13TeV', 'pdf_qqbar', 'pdf_gg', 'QCDscale_VH', 'QCDscale_ttbar','QCDscale_VV','QCDscale_QCD', 'QCDscale_VH_ggZHacceptance_lowPt', 'QCDscale_VH_ggZHacceptance_highPt', 'CMS_vhbb_boost_EWK_13TeV', 'CMS_vhbb_boost_QCD_13TeV','CMS_vhbb_ST','CMS_vhbb_VV', 'CMS_vhbb_eff_e_13TeV', 'CMS_vhbb_eff_m_13TeV']\n"

sys_list = sys_list_1 + sys_list_2
# + ['binStats']

sys_list_1 = [] 
sys_list_2 = []

# ====== Start the Optimization =======



# list of regression metrics
metric_list  = []

'''

for sys in sys_list_1:

     print '\n\n======================== Starting New SYS Loop  ========================'
     print '=============================================================================='
     print '----> Removing Systematic: ', sys
     
     new_options = full_sys_list_1.replace("'"+sys+"',", '')

     if sys == 'bTagWeight_cErr2':
          new_options = full_sys_list_1.replace(",'"+sys+"'", '')

     print new_options

     # clear the temp files from last datacard iteration
     #os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')


     for line in fileinput.input("13TeVconfig/datacard", inplace=True):

         if 'sys_BDT:' in line:

             print line.replace(line, new_options),

         else: print line,
     # end file modification


     # Set datacard output directory to current var name
     new_dir = "dir = 'sys_optimize/6_2_"+sys+"'\n"
             
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
     t6 = "combine -M Asymptotic -t -1 ../limits/sys_optimize/6_2_"+sys+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
     os.system(t6)

     # get the 50% limit
     for line in fileinput.input("cls_expected.txt", inplace=True):
         
         if 'Expected 50.0%:' in line:

             metric = line.replace('Expected 50.0%: r < ', '')

     print 'metric: ', metric
     
     metric_list.append(float(metric))

     print metric_list




# End first SYS loop         


for sys in sys_list_2:

     print '\n\n======================== Starting New SYS Loop  ========================'
     print '=============================================================================='
     print '----> Removing Systematic: ', sys

     new_options = full_sys_list_2.replace("'"+sys+"',", '')

     if sys == 'CMS_vhbb_eff_m_13TeV':
          new_options = full_sys_list_2.replace(", '"+sys+"'", '')

     print new_options

     # clear the temp files from last datacard iteration
     #os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')



     for line in fileinput.input("13TeVconfig/datacard", inplace=True):

         if 'InUse:' in line:

             print line.replace(line, new_options),

         else: print line,
     # end file modification


     # Set datacard output directory to current var name
     new_dir = "dir = 'sys_optimize/6_2_"+sys+"'\n"
             
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
     t6 = "combine -M Asymptotic -t -1 ../limits/sys_optimize/6_2_"+sys+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
     os.system(t6)

     # get the 50% limit
     for line in fileinput.input("cls_expected.txt", inplace=True):
         
         if 'Expected 50.0%:' in line:

             metric = line.replace('Expected 50.0%: r < ', '')

     print 'metric: ', metric
     
     metric_list.append(float(metric))

     print metric_list



# Lastly, remove the bin-by-bin SYS
'''

'''
print '\n\n======================== Removing bin-by-bin stat  ========================'
print '=============================================================================='

# Reset all SYS back in place

new_options1 = full_sys_list_1
new_options2 = full_sys_list_2

# clear the temp files from last datacard iteration
#os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')


for line in fileinput.input("13TeVconfig/datacard", inplace=True):

    if 'InUse:' in line:

        print line.replace(line, new_options2),

    else: print line,
# end file modification


for line in fileinput.input("13TeVconfig/datacard", inplace=True):

    if 'sys_BDT:' in line:

        print line.replace(line, new_options1),

    else: print line,
# end file modification



new_options = "doBin: False\n"

for line in fileinput.input("13TeVconfig/datacard", inplace=True):

         if 'doBin:' in line:

             print line.replace(line, new_options),

         else: print line,
# end file modification

# Set datacard output directory to current var name
new_dir = "dir = 'sys_optimize/6_2_bin'\n"
             
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
t6 = "combine -M Asymptotic -t -1 ../limits/sys_optimize/6_2_bin/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
os.system(t6)

# get the 50% limit
for line in fileinput.input("cls_expected.txt", inplace=True):
         
     if 'Expected 50.0%:' in line:

          metric = line.replace('Expected 50.0%: r < ', '')

          print 'metric: ', metric
     
metric_list.append(float(metric))

print metric_list

# Reset doBin back to True
new_options = "doBin: True\n"

for line in fileinput.input("13TeVconfig/datacard", inplace=True):

     if 'doBin:' in line:

          print line.replace(line, new_options),

     else: print line,
# end file modification
'''



# ===============================================================


metric_list = [6.3438, 6.3438, 6.25, 6.3438, 6.1094, 6.3438, 6.3438, 6.1094, 6.1719, 6.3438, 6.3438, 6.3438, 6.3438, 6.2812, 6.3438, 6.3438, 6.3438, 6.3438, 6.2031, 6.2031, 6.3438, 6.3438, 6.3438, 6.3438, 6.3438, 6.3438]

# fill accuracy plots
cStd = TCanvas('cStd')
cStd.SetGrid()

h1b = TH1F('h1b', 'Systematic N-1', len(metric_list), 0, len(metric_list)+1)
h1b.SetFillColor(4);
h1b.SetBarWidth(0.4);
h1b.SetBarOffset(0.0);
h1b.SetStats(0);
h1b.GetYaxis().SetTitle('Cls Expected 50%')
#h1b.GetXaxis().SetTitle('')
h1b.SetMinimum(5)
#h1b.SetMaximum(20);

for i in range(0, len(metric_list)):
    h1b.Fill(i+1, metric_list[i])
    h1b.GetXaxis().SetBinLabel(i+1, sys_list[i])


h1b.GetXaxis().SetLabelSize(0.02)
h1b.Draw('b')

cStd.SaveAs('../myMacros/classification/bdt_optimization_plots/systematic_opt.pdf')







