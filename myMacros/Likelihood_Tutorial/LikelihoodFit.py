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
import ctypes
from array import array;
import matplotlib.pyplot as plt
ROOT.gROOT.SetBatch(True)


# Set the output plot path
outpath = '/afs/cern.ch/user/d/dcurry/www/LikelihoodFitIntro5_10/'
try   : os.system('mkdir '+outpath)
except: 
    print outpath+' already exists...'
    #os.system("rm "+ outpath+"*") 
temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outpath
os.system(temp_string2)
os.system(temp_string3)
#########################



# Set fractions of sig and bkg
sig_percent = 0.80
bkg_percent = 1.0 - sig_percent

# Number of sim data points, gaussian width and Mean
nSim  = 1000
width = 1
mean  = 5

# Add lnn nuisances
lnn_Nusiance_Dict = {'Luminosity':0.05,
                     'Trigger':0.03
                     }

# Init the random generators used for SIM
gaussian    = TRandom()
composition = TRandom() 
bkg         = TRandom()
randomSigma = TRandom()

# Visualize the Simulation
def PlotSim():

    nbins = 50
    xmin = 0
    xmax = 10
    hSimData = TH1F("hSimData", "", nbins, xmin, xmax)
    
    for i in range(1,100000):
        if composition.Rndm(i) <= sig_percent: 
            hSimData.Fill(gaussian.Gaus(mean, width))
            #hSimData.Fill(gaussian.Gaus(mean, randomSigma.Uniform(1,2)))
        else:
            hSimData.Fill(bkg.Uniform(0,10))

    c = ROOT.TCanvas('','', 600, 600)
    c.SetFillStyle(4000)
    c.SetFrameFillStyle(1000)
    c.SetFrameFillColor(0)
    hSimData.Draw()
    c.SaveAs(outpath+'/preFit_SplusB.png')
    c.SaveAs(outpath+'/preFit_SplusB.pdf')

PlotSim()


def generateSim(i):

    if i%20 == 0: print '\t Generating Simulation Sample #', i

    sim = []
    for i in range(1,nSim):
        if composition.Rndm(i) <= sig_percent:
            #sim.append(gaussian.Gaus(mean, randomSigma.Uniform(1,2)))
            sim.append(gaussian.Gaus(mean, width))
        else:
            sim.append(bkg.Uniform(0,10))
    return sim


# Create Fit pulls for 1000 different minimizations
nTrials = 1000
sim_pulls = []
for i in range(nTrials):
    sim_pulls.append(generateSim(i))


def pulls():
   
    print '\n\t Creating Pull Plots...'
    
    # store the fitted results
    mu_fits    = []
    sigma_fits = []
    sig_fits   = []
    bkg_fits   = []

    

    for i in range(nTrials):

        def fcn(npar, gin, f, par, iflag):
            
            lnL = 0


            for j in range(0,nSim-1):            

                # Signal and BKG PDFs
                sig_exp = (sim_pulls[i][j] - par[0])/par[1]
                sig_pdf = np.exp(-0.5*sig_exp*sig_exp) / (par[1]*np.sqrt(2*np.pi))
                bkg_pdf = (1/10)

                # Lnn Nuisance PDFs
                lnn_nuisance_pdfs = {}
                for x,iNuis in enumerate(lnn_Nusiance_Dict):
                    lnn_exp = (lnn_Nusiance_Dict[iNuis] - par[x+2])/par[(x+1)+2]
                    lnn_nuisance_pdfs[iNuis] = np.exp(-0.5*lnn_exp*lnn_exp) / (par[(x+1)+2]*np.sqrt(2*np.pi))

                if sig_pdf > 0:
                    lnL += np.log(0.8*sig_pdf + 0.2*bkg_pdf) 
                    
                for iNuis in lnn_Nusiance_Dict: 
                    if lnn_nuisance_pdfs[iNuis] > 0:
                        lnL += np.log(lnn_nuisance_pdfs[iNuis])
                        
            f[0] = -2*lnL
            
        LikelihoodMinuit = TMinuit(3)
        LikelihoodMinuit.SetFCN(fcn)

        # parNo, name, initVal, StepSize, lowerLimit, upperLimit
        LikelihoodMinuit.DefineParameter(0,"mu",      2.0, 0.1, 0, 0)
        LikelihoodMinuit.DefineParameter(1,"sigma",   1.0, 0.5, 0, 0)
        #LikelihoodMinuit.DefineParameter(2,"SigFrac", 0.8, 0.01, 0.01, 1)
        #LikelihoodMinuit.DefineParameter(3,"BkgFrac", 0.2, 0.01, 0.01, 1)
        LikelihoodMinuit.Migrad()
        LikelihoodMinuit.mnprin(1, 0)

        # Store each fitted value for each iteration
        mu, muError       = map(ctypes.c_double, (999, 999))
        sigma, sigmaError = map(ctypes.c_double, (999, 999))
        #sigFrac, sigFracError = map(ctypes.c_double, (999, 999))
        #bkgFrac, bkgFracError = map(ctypes.c_double, (999, 999))
        
        LikelihoodMinuit.GetParameter(0, mu, muError)
        LikelihoodMinuit.GetParameter(1, sigma, sigmaError)
        #LikelihoodMinuit.GetParameter(2, sigFrac, sigFracError)
        #LikelihoodMinuit.GetParameter(3, bkgFrac, bkgFracError)
        
        mu_pull    = (np.float32(mu) - mean)/width
        sigma_pull = (np.float32(sigma) - 1.5)/width
        #sig_pull   = (np.float32(mu) - sig_percent)/width
        #bkg_pull   = (np.float32(mu) - bkg_percent)/width
        
        mu_fits.append(mu_pull)
        sigma_fits.append(sigma_pull)
        #sig_fits.append(sig_pull)
        #bkg_fits.append(bkg_pull)
    
    #print '\nMu Fits:', mu_fits
    #print '\nSigma Fits:', sigma_fits
    
    pullPlot('mu', mu_fits)
    pullPlot('sigma', sigma_fits)
    #pullPlot('sigFrac', sig_fits)
    #pullPlot('bkgFrac', bkg_fits)
    

def pullPlot(title, array):
    cStd = TCanvas('cStd')
    cStd.SetGrid()
    h1b = TH1F('h1b', title+' Fit Pulls', 50,-0.5,0.5)
    h1b.SetFillColor(4)
    #h1b.SetBarWidth(0.2)
    #h1b.SetBarOffset(0.0)
    h1b.SetStats(0)
    h1b.GetXaxis().SetTitle('Pull')
    for i in range(0, len(array)):
        h1b.Fill(array[i])
    h1b.Draw()
    cStd.SaveAs(outpath+title+'Pulls.png')
    cStd.SaveAs(outpath+title+'Pulls.pdf')
    cStd.IsA().Destructor(cStd)
    h1b.IsA().Destructor(h1b)

# Define the likelihood function to minimize
def fcn(npar, gin, f, par, iflag):

    # paramters to fit
    #mu = par[0]
    #sigma    = par[1]
    # sig_frac = par[2]
    # bkg_frac = par[3]

    sig_frac = 1
    bkg_frac = 0.9
    
    # The likelihood to minimize:  L = sig_frac*PDF(Sig) + bkg_frac*PDF(Bkg)

    lnL = 0

    for i in range(0,nSim-1):
            sig_exp = (sim_data[i] - par[0])/par[1]
            sig_pdf = np.exp(-0.5*sig_exp*sig_exp) / (par[1]*np.sqrt(2*np.pi))
            if sig_pdf > 0:
                lnL +=  np.log(sig_pdf)

    f[0] = -2*lnL


# Define TMinuit Object
def minimize():
    
    LikelihoodMinuit = TMinuit(2)
    LikelihoodMinuit.SetFCN(fcn)

    #parNo, name, initVal, StepSize, lowerLimit, upperLimit 
    LikelihoodMinuit.DefineParameter(0,"mu", 2, 0.1, 0, 0)
    LikelihoodMinuit.DefineParameter(1,"sigma", 1, 0.5, 0, 0)
    #LikelihoodMinuit.DefineParameter(2,"SigFrac",0.1,1,0,0)
    #LikelihoodMinuit.DefineParameter(3,"BkgFrac",0.1,1,0,0)
    #LikelihoodMinuit.SetErrorDef(0.5)
 
    LikelihoodMinuit.Migrad()
    LikelihoodMinuit.mnprin(1, 0)

    #print 'Mu Fit Value:', LikelihoodMinuit.GetParameter(0,1,1)
    #mu = ctypes.c_double
    

        


##______________________________________________________________________________
if __name__ == '__main__':
    #minimize()
    pulls()
