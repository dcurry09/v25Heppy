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


# Intended use is for 3 datacard types to be produced and final limits for each type.
#  Types are with SYS and MC stas, no SYS, and no SYS and no MC.  Set the cards in datacard.ini
# dc:BDT_Zee_high_Zpt_noSYS_noBin, BDT_Zee_high_Zpt, BDT_Zee_high_Zpt_noBin




# If new weights need to be made
# Now train the BDT on new option list/ modified file

# clear the temp files from last datacard iteration
#os.system('rm -rf /exports/uftrig01a/dcurry/heppy//files/tmp/*')

#os.system('python ../myMacros/classification/bdt_classifier_training_loop.py')

# Apply the BDT weights to samples
#os.system('python ../myMacros/classification/bdt_classifier_eval_loop.py')


#datacard_list = ['BDT_Zee_high_Zpt', 'BDT_Zee_low_Zpt',
#                 'BDT_Zee_high_Zpt_10fb', 'BDT_Zee_low_Zpt_10fb',
#                 'BDT_Zee_high_Zpt_20fb', 'BDT_Zee_low_Zpt_20fb',
#                 ]

#datacard_list = ['BDT_Zee_high_Zpt', 'BDT_Zee_high_Zpt_noBin', 'BDT_Zee_high_Zpt_noSYS_noBin',
#                 'BDT_Zee_low_Zpt', 'BDT_Zee_low_Zpt_noBin', 'BDT_Zee_low_Zpt_noSYS_noBin'
#                 ]

#datacard_list = ['BDT_Zee_low_Zpt_noSYS_noBin']

# list of metrics
metric_list  = []
pvalue_list  = []

# noSYS Falg
noSYS = False

for datacard in datacard_list:

    noSYS = False

    print datacard

    if 'noSYS' in datacard:
        noSYS = True
        datacard = datacard.replace('_noSYS_noBin', '')
        #print datacard

    #continue

    # Make the datacards for new training
    # Set datacard output directory to current var name
    new_dir = "dir = '3_28_BDT_"+datacard+"'\n"

    for line in fileinput.input('../myMacros/classification/dataCard_loop.py', inplace=True):
        
        if 'dir =' in line:

            print line.replace(line, new_dir),

        else: print line,
    # end file modification
        

    new_card = "bdt_list=['"+datacard+"']\n"
    print new_card
    for line in fileinput.input('../myMacros/classification/dataCard_loop.py', inplace=True):

        if 'bdt_list=[' in line:

                print line.replace(line, new_card),

        else: print line,
    # end file modification

    
    os.system('python ../myMacros/classification/dataCard_loop.py')
    
    
    # Get the metric of success for each parameter iteration
    # put each iterations metric in a plot

    if os.path.isfile('cls_expected.txt'):
        os.system('rm cls_expected.txt')

    if not noSYS:
        # CLs Median expected limit
        if 'high' in datacard:    
            t6 = "combine -M Asymptotic -t -1 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
        if 'low' in datacard:
            t6 = "combine -M Asymptotic -t -1 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_LowPt.txt >> cls_expected.txt"
        os.system(t6)

    if noSYS:
        if 'high' in datacard:
            t6 = "combine -M Asymptotic -t -1 -S 0 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
        if 'low' in datacard:
            t6 = "combine -M Asymptotic -t -1 -S 0 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_LowPt.txt >> cls_expected.txt"
        os.system(t6)

    
    # get the 50% limit
    for line in fileinput.input("cls_expected.txt", inplace=True):
        
        if 'Expected 50.0%:' in line:

            metric = line.replace('Expected 50.0%: r < ', '')

    print 'metric: ', metric

    metric_list.append(float(metric))
    
    # Now the p-value
    if os.path.isfile('pvalue_expected.txt'):
        os.system('rm pvalue_expected.txt')

    if not noSYS:
        if 'high' in datacard:
            t7 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> pvalue_expected.txt"
        if 'low' in datacard:
            t7 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_LowPt.txt >> pvalue_expected.txt"
        os.system(t7)


    if noSYS:
        if 'high' in datacard:
            t7 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --expectSignal=1 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> pvalue_expected.txt"
        if 'low' in datacard:
            t7 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --expectSignal=1 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_LowPt.txt >> pvalue_expected.txt"
        os.system(t7)

    # get the p-value
    for line in fileinput.input("pvalue_expected.txt", inplace=True):

        if '(Significance' in line:
            
            pvalue = line.replace('Significance = ', '')
            pvalue = pvalue.replace('(', '')
            pvalue = pvalue.replace(')', '')
             
    print 'Significance: ', pvalue

    pvalue_list.append(float(pvalue))


# ======= DO IT AGAIN for 20 Inv Fb =========

# list of metrics
metric_list_20fb  = []
pvalue_list_20fb  = []

# noSYS Falg
noSYS = False

for datacard in datacard_list:

    noSYS = False

    print datacard

    if 'noSYS' in datacard:
        noSYS = True
        datacard = datacard.replace('_noSYS_noBin', '')
        #print datacard

    #continue

    # change samples.cfg to new luminosity
    # Set datacard output directory to current var name
    new_lumi = "lumi=20190.00\n"

    for line in fileinput.input('13TeVconfig/samples_nosplit.cfg', inplace=True):

        if 'lumi=' in line:

            print line.replace(line, new_lumi),

        else: print line,
    # end file modification
    

    # Make the datacards for new training
    # Set datacard output directory to current var name
    new_dir = "dir = '3_28_BDT_"+datacard+"'\n"

    for line in fileinput.input('../myMacros/classification/dataCard_loop.py', inplace=True):
        
        if 'dir =' in line:

            print line.replace(line, new_dir),

        else: print line,
    # end file modification
        

    new_card = "bdt_list=['"+datacard+"']\n"
    print new_card
    for line in fileinput.input('../myMacros/classification/dataCard_loop.py', inplace=True):

        if 'bdt_list=[' in line:

                print line.replace(line, new_card),

        else: print line,
    # end file modification

    
    os.system('python ../myMacros/classification/dataCard_loop.py')
    
    
    # Get the metric of success for each parameter iteration
    # put each iterations metric in a plot

    if os.path.isfile('cls_expected.txt'):
        os.system('rm cls_expected.txt')

    if not noSYS:
        # CLs Median expected limit
        if 'high' in datacard:    
            t6 = "combine -M Asymptotic -t -1 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
        if 'low' in datacard:
            t6 = "combine -M Asymptotic -t -1 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_LowPt.txt >> cls_expected.txt"
        os.system(t6)

    if noSYS:
        if 'high' in datacard:
            t6 = "combine -M Asymptotic -t -1 -S 0 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> cls_expected.txt"
        if 'low' in datacard:
            t6 = "combine -M Asymptotic -t -1 -S 0 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_LowPt.txt >> cls_expected.txt"
        os.system(t6)

    
    # get the 50% limit
    for line in fileinput.input("cls_expected.txt", inplace=True):
        
        if 'Expected 50.0%:' in line:

            metric = line.replace('Expected 50.0%: r < ', '')

    print 'metric: ', metric

    metric_list_20fb.append(float(metric))
    
    # Now the p-value
    if os.path.isfile('pvalue_expected.txt'):
        os.system('rm pvalue_expected.txt')

    if not noSYS:
        if 'high' in datacard:
            t7 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> pvalue_expected.txt"
        if 'low' in datacard:
            t7 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 --expectSignal=1 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_LowPt.txt >> pvalue_expected.txt"
        os.system(t7)


    if noSYS:
        if 'high' in datacard:
            t7 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --expectSignal=1 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_HighPt.txt >> pvalue_expected.txt"
        if 'low' in datacard:
            t7 = "combine -M ProfileLikelihood -m 125 --signif --pvalue -t -1 -S 0 --expectSignal=1 ../limits/3_28_BDT_"+datacard+"/vhbb_DC_TH_BDT_M125_Zee_LowPt.txt >> pvalue_expected.txt"
        os.system(t7)

    # get the p-value
    for line in fileinput.input("pvalue_expected.txt", inplace=True):

        if '(Significance' in line:
            
            pvalue = line.replace('Significance = ', '')
            pvalue = pvalue.replace('(', '')
            pvalue = pvalue.replace(')', '')
             
    print 'Significance: ', pvalue

    pvalue_list_20fb.append(float(pvalue))

    # change samples.cfg to new luminosity
    # Set datacard output directory to current var name
    new_lumi = "lumi=2219.00\n"

    for line in fileinput.input('13TeVconfig/samples_nosplit.cfg', inplace=True):

        if 'lumi=' in line:

            print line.replace(line, new_lumi),

        else: print line,
    # end file modification


# end paramater loop



print '\n======= High Pt Region ========'
print 'CLs Median'
print 'All SYS       :', metric_list[0], '  20fb:', metric_list_20fb[0] 
print 'No MC         :', metric_list[1], '  20fb:', metric_list_20fb[1]
print 'No MC, No SYS :', metric_list[2], '  20fb:', metric_list_20fb[2]

print '\nP-value'
print 'All SYS       :', pvalue_list[0], '  20fb:', pvalue_list_20fb[0]
print 'No MC         :', pvalue_list[1], '  20fb:', pvalue_list_20fb[1]
print 'No MC, No SYS :', pvalue_list[2], '  20fb:', pvalue_list_20fb[2]



print '\n======= Low Pt Region ========'
print 'CLs Median'
print 'All SYS       :', metric_list[3], '  20fb:', metric_list_20fb[3]
print 'No MC         :', metric_list[4], '  20fb:', metric_list_20fb[4]
print 'No MC, No SYS :', metric_list[5], '  20fb:', metric_list_20fb[5]

print '\nP-value'
print 'All SYS       :', pvalue_list[3], '  20fb:', pvalue_list_20fb[3]
print 'No MC         :', pvalue_list[4], '  20fb:', pvalue_list_20fb[4]
print 'No MC, No SYS :', pvalue_list[5], '  20fb:', pvalue_list_20fb[5]

