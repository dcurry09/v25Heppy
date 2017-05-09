import sys
import os
import re
import fileinput
import subprocess
import numpy as np
from matplotlib import interactive
from ROOT import *
gROOT.SetBatch(True)

input_mc = TFile.Open('Zll_nloEWK_weight_unnormalized.root')
hist      = input_mc.Get('SignalWeight_nloEWK')
hist_up   = input_mc.Get('SignalWeight_nloEWK_up')
hist_down = input_mc.Get('SignalWeight_nloEWK_down')

hist.Rebin(4)
hist_up.Rebin(4)
hist_down.Rebin(4)

#for ibin in range(1,hist.GetNbinsX()+1):
    #print 'Bin', ibin , ':', hist.GetBinContent(ibin)/4
    #print hist.GetBinContent(ibin)/4

canv = TCanvas("canv","canv")

hist.SetLineColor(kBlack)
hist_up.SetLineColor(kRed)
hist_down.SetLineColor(kBlue)

hist.SetStats(0)

hist.Draw()
hist_up.Draw('same')
hist_down.Draw('same')

leg = TLegend(0.1,0.1,0.3,0.3)
leg.AddEntry(hist, 'Nominal')
leg.AddEntry(hist_up, 'Up')
leg.AddEntry(hist_down, 'Down')
leg.Draw('same')

outpath = '/afs/cern.ch/user/d/dcurry/www/4_15_TEST11/'

canv.Print(outpath+'EWK_VH.pdf')
canv.Print(outpath+'EWK_VH.png')

