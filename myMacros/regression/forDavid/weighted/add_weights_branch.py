# there are four kinds of weights that need to be added:
# - pT/eta flatness
#   o take from 2D-histogram files applying inverse weight
# - category normalization
#   o take from text file generated via bias script
# - category-based from bias
#   o take from text file generated via bias script
# - 2:1:3 B:C:light bias to account for dedicated C v. B and C vs. DUSG training
#   o assign by hand

import sys
sys.argv.append( '-b-' )
import os
import shutil
from ROOT import *
from array import array
import time
import multiprocessing


def getEtaPtBin(etaGroomed, ptGroomed, etaPtBins):
  
  binNumber = -1
  for i in range(len(etaPtBins)):
    # print etaPtBins[i]
    if eval(etaPtBins[i]):
      binNumber = i
      break
  return binNumber


def getCategoryBias(category, flavour, etaPtBin, biasDict):
  
  key = "%s_%s" %(category, flavour)
  return biasDict[key][etaPtBin]

def getNormalization(category, flavour, etaPtBin, NormDict):
  
  key = "%s_%s" %(category, flavour)
  return NormDict[key][etaPtBin] 


def getEtaPtWeight(etaGroomed, ptGroomed, h2EtaPt):
  
  # print h2EtaPt.FindBin(etaGroomed, ptGroomed)
  binContent = h2EtaPt.GetBinContent(h2EtaPt.FindBin(etaGroomed, ptGroomed))

  #if (binContent != 0):
  #  return 1./binContent
  #else:
  #  print "ERROR: Bin content %i for pT = %f GeV and eta = %f" %(binContent, etaGroomed, ptGroomed)
  #  return -1


def getPtWeight(ptGroomed, h2EtaPt):


  #if ptGroomed < 50: return 0.9
  #else: return 0.1
  
  
  # Get total of entries in the hist
  total = h2EtaPt.Integral()

  binContent = h2EtaPt.GetBinContent(h2EtaPt.FindBin(ptGroomed))

  # Median value to flatten out to
  #med = total / h2EtaPt.GetNbinsX()

  # the weight to multiply jet pt to flatten out
  if (binContent != 0):
    weight = 1./binContent
    return weight
  else:
    print "ERROR: Bin content %i for pT = %f GeV" %(binContent, ptGroomed)
    return -1
      


# def processNtuple(inFileName, inDirName, histoDirName, outDirName, etaPtBins, biasDict, flavourBias, NormDict):
def processNtuple(inFileName, inDirName, histoDirName, outDirName):
    
  print "Starting to process %s" %inFileName
  
  # histogram input
  weightHistName = "jets"
  #sample = inFileName.replace("_forTraining", "").split("_",1)[0]
  sample = inFileName.replace(".root","")
  print "This sample is %s " %(sample)
  #if inFileName.startswith("skimmed_20k_eachptetabin_"):
  histoFileName = "%s/%s_EtaPtWeightHisto.root" %(histoDirName, sample)  #Category-inclusive pt/eta weights
 #Category-specific pt/eta - for Category-specific training
  print "Getting histogram %s from %s" %(weightHistName, histoFileName)
  histoFile  = TFile.Open( histoFileName )
  h2EtaPt  = histoFile.Get(weightHistName)
  # make copy of input ntuple to be safe and work with that
  print "copying %s/%s to %s/%s" %(inDirName, inFileName, outDirName, inFileName)
  shutil.copy2("%s/%s" %(inDirName, inFileName), "%s/%s"%(outDirName, inFileName))
  
  # retrieve the ntuple of interest
  inFile = TFile.Open( "%s/%s" %(outDirName, inFileName), "update" ) # this now uses the copied file in outDirName
  inTreeName = "tree"
  myTree = inFile.Get( inTreeName )
  
  # create new branches
  weight_etaPt = array( 'f', [0]*15)
  mc_weight_etaPt = array( 'f', [0]*15)

  b_weight_etaPt    = myTree.Branch( 'weight_etaPt', weight_etaPt, 'weight_etaPt[15]/F' )
  mc_b_weight_etaPt = myTree.Branch( 'mc_weight_etaPt', mc_weight_etaPt, 'mc_weight_etaPt[15]/F' )
  
  # b_weight_etaPtInc = myTree.Branch( "weight_etaPtInc", weight_etaPtInc, 'weight_etaPtInc/F' )
  # b_weight_category = myTree.Branch( "weight_category", weight_category, 'weight_category/F' )
  # b_weight_norm = myTree.Branch( "weight_norm", weight_norm, 'weight_norm/F' )
  # b_weight_flavour = myTree.Branch( "weight_flavour", weight_flavour, 'weight_flavour/F' )
  # b_weight = myTree.Branch( "weight", weight, 'weight/F' )
  # connect branches needed for weight calculation
  #Jet_pt = array( "f", [0.] )
  #Jet_eta = array( "f", [0.] )
  #myTree.SetBranchAddress( 'Jet_pt', Jet_pt )
  #myTree.SetBranchAddress( 'Jet_eta', Jet_eta )

  ### actual loop ###
  entries = myTree.GetEntriesFast()
  print "%s: Starting event loop" %(multiprocessing.current_process().name)
  print '# of Entries:', entries
  startTime = time.time()
  for ientry in xrange(entries):

    # get the next tree in the chain and verify
    myTree.GetEntry(ientry)

    #if ientry % 1000 == 0: print '----> Entry # ', ientry
    
    # timing
    reportEveryNevents = 10000
    if (ientry%reportEveryNevents==0):
      if (ientry != 0):
        print "%s: Progress: %3.1f%%" %(multiprocessing.current_process().name, float(ientry)/(entries)*100)
        endTime = time.time()
        deltaTime = endTime - startTime
        rate = float(reportEveryNevents)/deltaTime
        print "%s: current rate: %5.2f Hz" %(multiprocessing.current_process().name, rate)
        startTime = time.time()
    

    #print 'nJet: ', myTree.nJet

    # Get the hIggs jet weights        
    for iJet in range(0,15):    
      
      #print 'iJet:', iJet

      if iJet < myTree.nJet:
        #print 'Fill is good weight'
        #weight_etaPt[iJet] = getEtaPtWeight(myTree.Jet_eta[iJet], myTree.Jet_pt[iJet], h2EtaPt)
        weight_etaPt[iJet] = getPtWeight(myTree.Jet_pt[iJet], h2EtaPt)
      else:
        #print 'Fill with dummy weight'
        weight_etaPt[iJet] = -999

      if iJet < myTree.nGenJet:
        mc_weight_etaPt[iJet] = getPtWeight(myTree.GenJet_wNuPt[iJet], h2EtaPt)
      else:
         mc_weight_etaPt[iJet] = -999
        
    #print 'Filling branches...'
    b_weight_etaPt.Fill()
    mc_b_weight_etaPt.Fill()
    

  inFile.Write()
  histoFile.Close()
  inFile.Close()

  print "%s: Total time: %5.2f s" %(multiprocessing.current_process().name, time.clock())
  
  

def main():

  ROOT.gROOT.SetBatch(True)
  parallelProcesses = multiprocessing.cpu_count()
  # create Pool
  p = multiprocessing.Pool(parallelProcesses)
  print "Using %i parallel processes" %parallelProcesses
    
  #outDirName = '/shome/thaarres/HiggsTagger/weighted_rootfiles'
  #histoDirName = '/shome/thaarres/HiggsTagger/EtaPtWeights'
  #inDirName = "/shome/thaarres/HiggsTagger/rootfiles/signal"
  
  outDirName = '/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/jetPt_weighted/'
  histoDirName = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/myMacros/regression/forDavid/weighted/jetWeights'
  inDirName = '/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/'

  weightHistName = "jets"

  # category dependent bias for each flavour combination
  # etaPtBins = []
#   etaPtBins.append
#   etaPtBins.append("15 < ptGroomed <= 40 and abs(etaGroomed) <= 1.2")
#   etaPtBins.append("15 < ptGroomed <= 40 and 1.2 < abs(etaGroomed) <= 2.1")
#   etaPtBins.append("15 < ptGroomed <= 40 and abs(etaGroomed) > 2.1")
#   etaPtBins.append("40 < ptGroomed <= 60 and abs(etaGroomed) <= 1.2")
#   etaPtBins.append("40 < ptGroomed <= 60 and 1.2 < abs(etaGroomed) <= 2.1")
#   etaPtBins.append("40 < ptGroomed <= 60 and abs(etaGroomed) > 2.1")
#   etaPtBins.append("60 < ptGroomed <= 90 and abs(etaGroomed) <= 1.2")
#   etaPtBins.append("60 < ptGroomed <= 90 and 1.2 < abs(etaGroomed) <= 2.1")
#   etaPtBins.append("60 < ptGroomed <= 90 and abs(etaGroomed) > 2.1")
#   etaPtBins.append("90 < ptGroomed <= 150 and abs(etaGroomed) <= 1.2")
#   etaPtBins.append("90 < ptGroomed <= 150 and 1.2 < abs(etaGroomed) <= 2.1")
#   etaPtBins.append("90 < ptGroomed <= 150 and abs(etaGroomed) > 2.1")
#   etaPtBins.append("150 < ptGroomed <= 400 and abs(etaGroomed) <= 1.2")
#   etaPtBins.append("150 < ptGroomed <= 400 and 1.2 < abs(etaGroomed) <= 2.1")
#   etaPtBins.append("150 < ptGroomed <= 400 and abs(etaGroomed) > 2.1")
#   etaPtBins.append("400 < ptGroomed <= 600 and abs(etaGroomed)<= 1.2")
#   etaPtBins.append("400 < ptGroomed <= 600 and abs(etaGroomed) > 1.2")
#   etaPtBins.append("ptGroomed > 600 and abs(etaGroomed) <= 1.2")
#   etaPtBins.append("ptGroomed > 600 and abs(etaGroomed) > 1.2")
#
 #  # read in bias file
 #  print "Reading in bias file"
 #  biasDict = {}
 #  biasFile = open(biasFileName, "r")
 #  for line in biasFile:
 #    if (line.find("***") >= 0): #***************   NoVertex_C   ***************
 #      key = line.replace("*","").strip()
 #      print "-%s-" %key
 #      biasDict[key] = []
 #    elif (line.find("<bias>") >= 0): # <bias>3.19179</bias>
 #      biasValue = float(line.replace("<bias>","").replace("</bias>",""))
 #      biasDict[key].append(biasValue)
 #  print biasDict
 #
 # # read in normalization file
 #  print "Reading in normalization file"
 #  NormDict = {}
 #  normFile = open(normFileName, "r")
 #  for line2 in normFile:
 #    if (line2.find("***") >= 0): #***************   NoVertex_C   ***************
 #      key2 = line2.replace("*","").strip()
 #      print "-%s-" %key2
 #      NormDict[key2] = []
 #    elif (line2.find("<bias>") >= 0): # <bias>3.19179</bias>
 #      NormValue = float(line2.replace("<bias>","").replace("</bias>",""))
 #      NormDict[key2].append(NormValue)
 #  print NormDict
  
  for inFileName in os.listdir(inDirName):
    if inFileName.endswith("v14_11_2015_ZH125.root"): # and inFileName.startswith("skimmed_20k_eachptetabin"):
      # processNtuple(inFileName, inDirName, histoDirName, outDirName, etaPtBins, signalFlavours, biasDict, flavourBias)
      # processNtuple(inFileName, inDirName, histoDirName, outDirName, etaPtBins)
      # break
      # p.apply_async(processNtuple, args = (inFileName, inDirName, histoDirName, outDirName, etaPtBins, biasDict, flavourBias, NormDict))
      p.apply_async(processNtuple, args = (inFileName, inDirName, histoDirName, outDirName))
      

  p.close()
  p.join()
  
  print "done"  


if __name__ == "__main__":
  main()
