import sys
import os
import re
import fileinput
import subprocess
import numpy as np
from matplotlib import interactive
from ROOT import *


input_mc = TFile.Open('mcpu.root')

input_data = TFile.Open('outputData.root')

# Get the Histo
hist_mc   = input_mc.Get('pileup')
hist_data = input_data.Get('pileup')

# normalize the histo
norm_mc = hist_mc.Integral()
hist_mc.Scale(1/norm_mc)

norm_data = hist_data.Integral()
hist_data.Scale(1/norm_data)

print '\n\t======== MC ========'

# Print out the bin contents
for ibin in range(1,hist_mc.GetNbinsX()+1):
    
    #print 'Bin', ibin , ':', hist_mc.GetBinContent(ibin)
    
    #ratio = hist_data.GetBinContent(ibin)/hist_mc.GetBinContent(ibin)

    if hist_mc.GetBinContent(ibin) == 0: ratio = 1

    else: ratio = hist_data.GetBinContent(ibin)/hist_mc.GetBinContent(ibin)

    print ratio


'''
print '\n\t======== Data ========'

# Print out the bin contents
for ibin in range(1,hist_data.GetNbinsX()+1):

    print 'Bin', ibin , ':', hist_data.GetBinContent(ibin)

'''


