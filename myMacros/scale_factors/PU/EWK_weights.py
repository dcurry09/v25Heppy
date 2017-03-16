import sys
import os
import re
import fileinput
import subprocess
import numpy as np
from matplotlib import interactive
from ROOT import *


input_mc = TFile.Open('Zll_nloEWK_weight_unnormalized.root')
hist = input_mc.Get('SignalWeight_nloEWK')
hist.Rebin(4)

for ibin in range(1,hist.GetNbinsX()+1):
    
    #print 'Bin', ibin , ':', hist.GetBinContent(ibin)/4
    print hist.GetBinContent(ibin)/4



'''
print '\n\t======== Data ========'

# Print out the bin contents
for ibin in range(1,hist_data.GetNbinsX()+1):

    print 'Bin', ibin , ':', hist_data.GetBinContent(ibin)

'''


