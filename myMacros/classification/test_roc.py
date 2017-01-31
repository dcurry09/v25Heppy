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


tree_list = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 700, 800, 1000] # 14

nEvt_list = [0.1, 0.5, 1, 2, 3, 4, 5, 10, 15, 20] # 10



roc_file = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/python/roc_lowPt.txt'

tree_metric_list  = []

with open(roc_file) as temp_file:

    for i, line in enumerate(temp_file):

        print '\nTree entry:', i, 'ROC:',line

        if i >= len(tree_list): break

        tree_metric_list.append(float(line.strip('\n')))

    # end tree loop

    print 'Tree Metric List: ', tree_metric_list

nEvt_metric_list  = []

with open(roc_file) as temp_file:

    for i, line in enumerate(temp_file):

        if i < len(tree_list) or i >= (len(tree_list) + len(nEvt_list)): continue

        nEvt_metric_list.append(float(line.strip('\n')))

    # end tree loop

    print 'nEvt Metric List: ', nEvt_metric_list


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
    h1b.Fill(i+1, tree_metric_list[i])
    h1b.GetXaxis().SetBinLabel(i+1, str(tree_list[i]))
    h1b.Draw('b')

cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_trees_"+region.capitalize()+"Pt.pdf")
cStd.SaveAs("../myMacros/classification/bdt_optimization_plots/bdt_paramOptimization_trees_"+region.capitalize()+"Pt.png")
