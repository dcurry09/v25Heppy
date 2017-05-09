###### LikelihoodFit.py ###############################
# by D. Curry May 5, 2017
# Beginner guide to performing Likelihood Fit
# on simulated signal and background distributions
#
######################################################

import ROOT
from ROOT import *
import os
import sys
import multiprocessing
import numpy as np
ROOT.gROOT.SetBatch(True)


# Set the output plot path
outpath = '/afs/cern.ch/user/d/dcurry/www/LikelihoodFitIntro/'
try   : os.system('mkdir '+outpath)
except: 
    print outpath+' already exists...'
    #os.system("rm "+ outpath+"*") 
temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outpath
os.system(temp_string2)
os.system(temp_string3)
#########################


print '\n\t ----> Generating the Signal and BKG Distributions...'

# Generate the signal gaussian
hSig = TH1F("Sig", "", 100, -10, 10)
hSig.FillRandom("gaus", 10000)
hSig.SetLineColor(kRed)
hSig.SetStats(0)

# Generate a flat background
hBkg = TH1F("Bkg", "", 100, -10, 10)
for bin in range(100+1):
    hBkg.SetBinContent(bin, 300)


# Draw(Save) Signal and Bkg plots
c = ROOT.TCanvas('','', 600, 600)
c.SetFillStyle(4000)
c.SetFrameFillStyle(1000)
c.SetFrameFillColor(0)
hSig.Draw()
hBkg.Draw("SAME")
c.SaveAs(outpath+'/preFit_SplusB.png')
c.SaveAs(outpath+'/preFit_SplusB.pdf')

# Define the likelihood function to minimize
def fcn(npar, gin, f, par, iflag):

    mu = par[0]
    lnL = 0.0;
    for i in range (0,10000):
        lnL += r[i]*log(mu) - mu - log(rfac[i])

    f = -lnL

    return f


# Initialize Minuitdouble arglist[10];
ierflg = 0
start = 1.0
step = 0.1
l_bnd = 0.1
u_bnd = 10.
TMinuit minuit(1)
minuit.SetFCN(fcn)
minuit.mnparm(0,"Gaussian Mu", start, step, l_bnd, u_bnd, ierflg)
