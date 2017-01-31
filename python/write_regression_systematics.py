#! /usr/bin/env python
import sys
import os,subprocess
import ROOT 
import math
import shutil
import numpy as np
from array import array
from collections import Counter
import warnings
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='creating converter.*' )
ROOT.gROOT.SetBatch(True)
from optparse import OptionParser
from myutils import BetterConfigParser, ParseInfo
from myutils.btag_reweight import BTagWeightCalculator, Jet
from myutils.leptonSF import *


#Usage: ./write_regression_systematic.py path

#os.mkdir(path+'/sys')
argv = sys.argv
parser = OptionParser()
#parser.add_option("-P", "--path", dest="path", default="", 
#                      help="path to samples")
parser.add_option("-S", "--samples", dest="names", default="", 
                      help="samples you want to run on")
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration defining the plots to make")
(opts, args) = parser.parse_args(argv)
if opts.config =="":
        opts.config = "config"

print opts.config
config = BetterConfigParser()
config.read(opts.config)
anaTag = config.get("Analysis","tag")
TrainFlag = eval(config.get('Analysis','TrainFlag'))
btagLibrary = config.get('BTagReshaping','library')
samplesinfo=config.get('Directories','samplesinfo')

VHbbNameSpace=config.get('VHbbNameSpace','library')
ROOT.gSystem.Load(VHbbNameSpace)
AngLikeBkgs=eval(config.get('AngularLike','backgrounds'))
ang_yield=eval(config.get('AngularLike','yields'))

#path=opts.path
pathIN = config.get('Directories','SYSin')
pathOUT = config.get('Directories','SYSout')
#tmpDir = os.environ["TMPDIR"]

name = config.get('TrainRegression', 'name')

#print 'INput samples:\t%s'%pathIN
#print 'OUTput samples:\t%s'%pathOUT+name

namelist=opts.names.split(',')

#load info
info = ParseInfo(samplesinfo,pathIN)

# counter object
count = Counter()

def deltaPhi(phi1, phi2): 
    result = phi1 - phi2
    while (result > math.pi): result -= 2*math.pi
    while (result <= -math.pi): result += 2*math.pi
    return result


def deltaR(phi1, eta1, phi2, eta2):
    deta = eta1-eta2
    dphi = deltaPhi(phi1, phi2)
    result = math.sqrt(deta*deta + dphi*dphi)
    return result


def resolutionBias(eta):
    if(eta< 0.5): return 0.052
    if(eta< 1.1): return 0.057
    if(eta< 1.7): return 0.096
    if(eta< 2.3): return 0.134
    if(eta< 5): return 0.28
    return 0

def corrPt(pt,eta,mcPt):
    return (pt+resolutionBias(math.fabs(eta))*(pt-mcPt))/pt

def corrCSV(btag,  csv, flav):
    if(csv < 0.): return csv
    if(csv > 1.): return csv;
    if(flav == 0): return csv;
    if(math.fabs(flav) == 5): return  btag.ib.Eval(csv)
    if(math.fabs(flav) == 4): return  btag.ic.Eval(csv)
    if(math.fabs(flav) != 4  and math.fabs(flav) != 5): return  btag.il.Eval(csv)
    return -10000


def csvReshape(sh, pt, eta, csv, flav):
	return sh.reshape(float(eta), float(pt), float(csv), int(flav))


def addAdditionalJets(H, tree):

    for i in range(tree.nhjidxaddJetsdR08):
	    
        idx = tree.hjidxaddJetsdR08[i]
	
	if (idx == tree.hJCidx[0]) or (idx == tree.hJCidx[1]): continue
        
	if tree.Jet_puId[idx] < 4: continue
	
	if tree.Jet_pt_reg[idx] < 15: continue

	if tree.Jet_id[idx] < 3: continue

	addjet = ROOT.TLorentzVector()
	
	addjet.SetPtEtaPhiM(tree.Jet_pt_reg[idx], tree.Jet_eta[idx], tree.Jet_phi[idx], tree.Jet_mass[idx])
	
	H = H + addjet

	#print 'H mass + FSR:', H.M()
	#print 'H PT + FSR  :', H.Pt()

    return H

def projectionMETOntoJet(met, metphi, jet, jetphi, onlyPositive=True, threshold = math.pi/4.0):
  deltaphi = deltaPhi(metphi, jetphi)
  projection = met * math.cos(deltaphi)  
  if onlyPositive and abs(deltaphi) >= threshold:
      return 0.0
  else:
      return projection

def projMetOntoH(ev, tryAlsoWNoLept, recoverAlsoFSR):

  if len(ev.hJCidx)<2:
    return ev.HCSV_mass
  lep0pt = ev.Jet_leptonPt[ev.hJCidx[0]]
  lep1pt = ev.Jet_leptonPt[ev.hJCidx[1]]

  nu = ROOT.TLorentzVector()
  j0 = ROOT.TLorentzVector()
  j1 = ROOT.TLorentzVector()
  j0.SetPtEtaPhiM( ev.Jet_pt_reg[ev.hJCidx[0]],  ev.Jet_eta[ev.hJCidx[0]],  ev.Jet_phi[ev.hJCidx[0]],  ev.Jet_mass[ev.hJCidx[0]])
  j1.SetPtEtaPhiM( ev.Jet_pt_reg[ev.hJCidx[1]],  ev.Jet_eta[ev.hJCidx[1]],  ev.Jet_phi[ev.hJCidx[1]],  ev.Jet_mass[ev.hJCidx[1]])

  proj0 = projectionMETOntoJet(ev.met_pt, ev.met_phi, j0.Pt() , j0.Phi(), False, 999)
  dPhi0= deltaPhi(ev.met_phi,  j0.Phi())    
  proj1 = projectionMETOntoJet(ev.met_pt, ev.met_phi, j1.Pt() ,j1.Phi(), False, 999)
  dPhi1= deltaPhi(ev.met_phi,  j1.Phi())    

  if recoverAlsoFSR:
      FSRjet = ROOT.TLorentzVector()
      idxtoAdd = []
      idxtoAdd =  [x for x in range(ev.nJet)  if ( x not in ev.hJCidx and ev.Jet_pt[x]>15. and abs(ev.Jet_eta[x])<3.0 and  ev.Jet_id[x]>=3 and ev.Jet_puId[x]>=4 and  min( deltaR(ev.Jet_eta[x],ev.Jet_phi[x], j0.Eta(), j0.Phi()), deltaR(ev.Jet_eta[x],ev.Jet_phi[x], j1.Eta(), j1.Phi() ) ) <0.8 )  ] 
      for ad in idxtoAdd:        
            FSRjet.SetPtEtaPhiM( ev.Jet_pt_reg[ad],  ev.Jet_eta[ad],  ev.Jet_phi[ad],  ev.Jet_mass[ad])
            dR0 = deltaR(ev.Jet_eta[ad],ev.Jet_phi[ad], j0.Eta(), j0.Phi() )
            dR1 = deltaR(ev.Jet_eta[ad],ev.Jet_phi[ad], j1.Eta(), j1.Phi() )
            if dR0<dR1:
                   j0 +=FSRjet
            else:
                   j1 +=FSRjet


  if not tryAlsoWNoLept:
      if (lep0pt>0 or lep1pt>0):  
              if ( (abs(dPhi0)<abs(dPhi1)) and lep0pt>0) :
                  nu.SetPtEtaPhiM( proj0,  j0.Eta(),  j0.Phi(), 0)
                  #j0+=nu
              elif ( (abs(dPhi0)>abs(dPhi1))  and lep1pt>0 ):
                  nu.SetPtEtaPhiM( proj1,  j1.Eta(),  j1.Phi(), 0)
                  #j1+=nu

      return (j0+j1).M()
 
  else : 
          if (abs(dPhi0)<abs(dPhi1)) :
                 nu.SetPtEtaPhiM( proj0,  j0.Eta(),  j0.Phi(), 0)
                 #j0+=nu
          else:
                 nu.SetPtEtaPhiM( proj1,  j1.Eta(),  j1.Phi(), 0)
                 #j1+=nu
  
  return (j0+j1).M()


def higgs_semiL_bias(pt, eta, IsSemiLepton):

	'''
	Returns a Higgs mass resolution correction vs pt/et for semi and non semiLeptonic jets
	'''
	
	bias = 1
	
	if IsSemiLepton:
		
            if pt > 50 and pt < 100: 
	        if eta < 0.9:	    
		    bias = abs((0.18-0.14)/0.18)
		if eta > 0.9 and eta < 1.6:
		    bias = abs((0.18-0.14)/0.18)	
		if eta > 1.6 and eta < 2.4:
			bias = abs((0.185-0.142)/0.185)

	    if pt > 100 and pt < 150:
                if eta < 0.9:
                    bias = abs((0.192-0.144)/0.192)
		if eta > 0.9 and eta < 1.6:
                    bias = abs((0.195-0.144)/0.195)
		if eta > 1.6 and eta < 2.4:
                    bias = abs((0.195-0.148)/0.195)
		    
	    if pt > 150:
		    if eta < 0.9:
			    bias = abs((0.157-0.136)/0.57)
		    if eta > 0.9 and eta < 1.6:
			    bias = abs((0.173-0.143)/0.173)
		    if eta > 1.6 and eta < 2.4:
			    bias = abs((0.169-0.146)/0.169)

	else:
		
            if pt > 50 and pt < 100: 
	        if eta < 0.9:	    
		    bias = abs((0.177-0.137)/0.177)
		if eta > 0.9 and eta < 1.6:
		    bias = abs((0.16-0.132)/0.16)	
		if eta > 1.6 and eta < 2.4:
                    bias = abs((0.18-0.136)/0.18)

	    if pt > 100 and pt < 150:
                if eta < 0.9:
                    bias = abs((0.159-0.13)/0.159)
		if eta > 0.9 and eta < 1.6:
                    bias = abs((0.156-0.128)/0.156)
		if eta > 1.6 and eta < 2.4:
                    bias = abs((0.159-0.132)/0.159)
		    
	    if pt > 150:
		    if eta < 0.9:
			    bias = abs((0.136-0.116)/0.136)
		    if eta > 0.9 and eta < 1.6:
			    bias = abs((0.142-0.118)/0.142)
		    if eta > 1.6 and eta < 2.4:
			    bias = abs((0.123-0.123)/0.123)

	return bias


# End Functions
# =============================================================================



for job in info:

    if not job.name in namelist: continue

    ROOT.gROOT.ProcessLine(
        "struct H {\
        int         HiggsFlag;\
        float         mass;\
        float         pt;\
        float         eta;\
        float         phi;\
        float         dR;\
        float         dPhi;\
        float         dEta;\
        } ;"
    )

    
    lhe_weight_map = False if not config.has_option('LHEWeights', 'weights_per_bin') else eval(config.get('LHEWeights', 'weights_per_bin'))
    
    #Set up offline b-weight calculation
    #csvpath = "/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/data/csv"
    #csvpath = "./"
    #bweightcalc = BTagWeightCalculator(
	#    csvpath + "/csv_rwt_fit_hf_2015_12_14.root",
	#    csvpath + "/csv_rwt_fit_lf_2015_12_14.root"
	 #   )
    #bweightcalc.btag = "btagCSV"

    
    # make the input/output files    
    input  = ROOT.TFile.Open(pathIN+'/'+job.prefix+job.identifier+'.root','read')
    output = ROOT.TFile.Open(pathOUT+'/'+job.prefix+name+job.identifier+'.root','recreate')
    
    input.cd()

    if lhe_weight_map and 'DY' in job.name:
        inclusiveJob = info.get_sample('DY')
        print inclusiveJob.name
        inclusive = ROOT.TFile.Open(pathIN+inclusiveJob.get_path,'read')
        inclusive.cd()
        obj = ROOT.TObject
        for key in ROOT.gDirectory.GetListOfKeys():
            input.cd()
            obj = key.ReadObj()
            if obj.GetName() == job.tree:
                continue
            output.cd()
            obj.Write(key.GetName())
	inclusive.Close()
    else:
        obj = ROOT.TObject
        for key in ROOT.gDirectory.GetListOfKeys():
            input.cd()
            obj = key.ReadObj()
            if obj.GetName() == job.tree:
                continue
            output.cd()
            obj.Write(key.GetName())
        
    input.cd()
    tree = input.Get(job.tree)
    #tree = input.Get('tree')
    nEntries = tree.GetEntries()

    print 'Input: ' , input
    print 'Output: ', output
    print 'job.tree:', job.tree
    print 'tree" ', tree
    print 'nEntries:', nEntries  


    output.cd()

    # For new regresssion zerop the branches out before cloning new tree
    #tree.SetBranchStatus('HCSV_reg_mass',0)
    #tree.SetBranchStatus('HCSV_reg_pt',0)
    #tree.SetBranchStatus('HCSV_reg_mass',0)
    #tree.SetBranchStatus('HCSV_reg_pt',0)
        
    newtree = tree.CloneTree(0)
        
    hJ0 = ROOT.TLorentzVector()
    hJ1 = ROOT.TLorentzVector()
    hJ2 = ROOT.TLorentzVector()
    vect = ROOT.TLorentzVector()

    hJ0_reg = ROOT.TLorentzVector()
    hJ1_reg = ROOT.TLorentzVector()

    # for adding 3rd jet
    hJ0_noReg = ROOT.TLorentzVector()
    hJ1_noReg = ROOT.TLorentzVector()
    
    regWeight = config.get("TrainRegression","regWeight")
    regDict = eval(config.get("TrainRegression","regDict"))
    regVars = eval(config.get("TrainRegression","regVars"))

    #regWeightFilterJets = config.get("Regression","regWeightFilterJets")
    #regDictFilterJets = eval(config.get("Regression","regDictFilterJets"))
    #regVarsFilterJets = eval(config.get("Regression","regVarsFilterJets"))

    # Standard Branches
    HCSV_dR_reg   = array('f',[0]*1)
    HCSV_dEta_reg = array('f',[0]*1)
    HCSV_dPhi_reg = array('f',[0]*1)

    newtree.Branch('HCSV_dR_reg', HCSV_dR_reg, 'HCSV_dR_reg[1]/F')
    newtree.Branch('HCSV_dEta_reg', HCSV_dEta_reg, 'HCSV_dEta_reg[1]/F')
    newtree.Branch('HCSV_dPhi_reg', HCSV_dEta_reg, 'HCSV_dPhi_reg[1]/F')
    
    HVdPhi_reg = array('f',[0]*1)
    newtree.Branch('HVdPhi_reg', HVdPhi_reg, 'HVdPhi_reg[1]/F')

    HCSV_reg_pt_FSR = array('f',[0]*1)
    newtree.Branch('HCSV_reg_pt_FSR', HCSV_reg_pt_FSR, 'HCSV_reg_pt_FSR[1]/F')

    # Higgs masses
    
    HCSV_reg_mass_FSR = array('f',[0]*1)
    newtree.Branch('HCSV_reg_mass_FSR', HCSV_reg_mass_FSR, 'HCSV_reg_mass_FSR[1]/F')

    HCSV_reg_mass_FSR2 = array('f',[0]*1)
    newtree.Branch('HCSV_reg_mass_FSR2', HCSV_reg_mass_FSR2, 'HCSV_reg_mass_FSR2[1]/F')

    HCSV_reg_mass_met_FSR = array('f',[0]*1)
    newtree.Branch('HCSV_reg_mass_met_FSR', HCSV_reg_mass_met_FSR, 'HCSV_reg_mass_met_FSR[1]/F')

    HCSV_reg_mass_met = array('f',[0]*1)
    newtree.Branch('HCSV_reg_mass_met', HCSV_reg_mass_met, 'HCSV_reg_mass_met[1]/F')

    # Optional semiLepton decay only
    HCSV_reg_mass_met_FSR_wSemiL = array('f',[0]*1)
    newtree.Branch('HCSV_reg_mass_met_FSR_wSemiL', HCSV_reg_mass_met_FSR_wSemiL, 'HCSV_reg_mass_met_FSR_wSemiL[1]/F')

    HCSV_reg_pt_FSR_wSemiL = array('f',[0]*1)
    newtree.Branch('HCSV_reg_pt_FSR_wSemiL', HCSV_reg_pt_FSR_wSemiL, 'HCSV_reg_pt_FSR_wSemiL[1]/F')

    HCSV_reg_pt_FSR = array('f',[0]*1)
    newtree.Branch('HCSV_reg_pt_FSR', HCSV_reg_pt_FSR, 'HCSV_reg_pt_FSR[1]/F')
    
    Jet_mt = array('f',[0]*2)
    newtree.Branch('Jet_mt', Jet_mt, 'Jet_mt[2]/F')

    # For higgs regression resolution
    HReg_resolution = array('f',[0]*1)
    newtree.Branch('HReg_resolution', HReg_resolution, 'HReg_resolution[1]/F')

    # For Higgs semiLepton bias in pt/eta bins
    Hreg_semiL_bias = array('f',[0]*1)
    newtree.Branch('Hreg_semiL_bias', Hreg_semiL_bias, 'Hreg_semiL_bias[1]/F')

    
    
    # ========== Lepton SF branches ============

    # per event we have a weight that we fill based on vtype.  It is good for every event
    #lepton_EvtWeight = array('f',[0]*1)
    
    #newtree.Branch('lepton_EvtWeight',lepton_EvtWeight,'lepton_EvtWeight/F')

    vLeptons_SFweight_HLT = array('f',[0]*1)
    vLeptons_SFweight_HLT[0] = 1
    newtree.Branch('vLeptons_SFweight_HLT', vLeptons_SFweight_HLT, 'vLeptons_SFweight_HLT/F')

    eTrigSFWeight = array('f',[0]*1)
    newtree.Branch('eTrigSFWeight', eTrigSFWeight, 'eTrigSFWeight/F')

    eTrigSFWeight_ele23 = array('f',[0]*1)
    eTrigSFWeight_ele23[0] = 1
    newtree.Branch('eTrigSFWeight_ele23', eTrigSFWeight_ele23, 'eTrigSFWeight_ele23/F')

    eTrigSFWeight_ele27 = array('f',[0]*1)
    eTrigSFWeight_ele27[0] = 1
    newtree.Branch('eTrigSFWeight_ele27', eTrigSFWeight_ele27, 'eTrigSFWeight_ele27/F')

    eTrigSFWeight_ele27_BCDEF = array('f',[0]*1)
    newtree.Branch('eTrigSFWeight_ele27_BCDEF', eTrigSFWeight_ele27_BCDEF, 'eTrigSFWeight_ele27_BCDEF/F')

    # New for double ele
    eTrigSFWeight_doubleEle76x = array('f',[0]*1)
    eTrigSFWeight_doubleEle76xUp = array('f',[0]*1)
    eTrigSFWeight_doubleEle76xDown = array('f',[0]*1)
    newtree.Branch('eTrigSFWeight_doubleEle76x', eTrigSFWeight_doubleEle76x, 'eTrigSFWeight_doubleEle76x/F')
    newtree.Branch('eTrigSFWeight_doubleEle76xUp', eTrigSFWeight_doubleEle76xUp, 'eTrigSFWeight_doubleEle76xUp/F')
    newtree.Branch('eTrigSFWeight_doubleEle76xDown', eTrigSFWeight_doubleEle76xDown, 'eTrigSFWeight_doubleEle76xDown/F')

    eTrackerSFWeight = array('f',[0]*1)
    newtree.Branch('eTrackerSFWeight', eTrackerSFWeight, 'eTrackerSFWeight/F')

    eTrackerSFWeightUp = array('f',[0]*1)
    newtree.Branch('eTrackerSFWeightUp', eTrackerSFWeightUp, 'eTrackerSFWeightUp/F')

    eTrackerSFWeightDown = array('f',[0]*1)
    newtree.Branch('eTrackerSFWeightDown', eTrackerSFWeightDown, 'eTrackerSFWeightDown/F')

    eId80SFWeight = array('f',[0]*1)
    newtree.Branch('eId80SFWeight', eId80SFWeight, 'eId80SFWeight/F')

    eId90SFWeight = array('f',[0]*1)
    newtree.Branch('eId90SFWeight', eId90SFWeight, 'eId90SFWeight/F')

    eId90SFWeight_BCDEF = array('f',[0]*1)
    newtree.Branch('eId90SFWeight_BCDEF', eId90SFWeight_BCDEF, 'eId90SFWeight_BCDEF/F')

    mTrigSFWeight = array('f',[0]*1)
    newtree.Branch('mTrigSFWeight', mTrigSFWeight, 'mTrigSFWeight/F')

    mTrigSFWeight_ICHEP = array('f',[0]*1)
    mTrigSFWeight_ICHEP[0] = 1
    newtree.Branch('mTrigSFWeight_ICHEP', mTrigSFWeight_ICHEP, 'mTrigSFWeight_ICHEP/F')

    mTrackerSFWeight = array('f',[0]*1)
    newtree.Branch('mTrackerSFWeight', mTrackerSFWeight, 'mTrackerSFWeight/F')

    mTrackerSFWeightUp = array('f',[0]*1)
    newtree.Branch('mTrackerSFWeightUp', mTrackerSFWeightUp, 'mTrackerSFWeightUp/F')

    mTrackerSFWeightDown = array('f',[0]*1)
    newtree.Branch('mTrackerSFWeightDown', mTrackerSFWeightDown, 'mTrackerSFWeightDown/F')

    mIdSFWeight = array('f',[0]*1)
    newtree.Branch('mIdSFWeight', mIdSFWeight, 'mIdSFWeight/F')

    mIsoSFWeight = array('f',[0]*1)
    newtree.Branch('mIsoSFWeight', mIsoSFWeight, 'mIsoSFWeight/F')

    # New for double ele
    mTrigSFWeight_doubleMu76x = array('f',[0]*1)
    mTrigSFWeight_doubleMu76xUp = array('f',[0]*1)
    mTrigSFWeight_doubleMu76xDown = array('f',[0]*1)
    newtree.Branch('mTrigSFWeight_doubleMu76x', mTrigSFWeight_doubleMu76x, 'mTrigSFWeight_doubleMu76x/F')
    newtree.Branch('mTrigSFWeight_doubleMu76xUp', mTrigSFWeight_doubleMu76xUp, 'mTrigSFWeight_doubleMu76xUp/F')
    newtree.Branch('mTrigSFWeight_doubleMu76xDown', mTrigSFWeight_doubleMu76xDown, 'mTrigSFWeight_doubleMu76xDown/F')
    
    # For DY special Weights
    DY_specialWeight = array('f',[0]*1)
    newtree.Branch('DY_specialWeight',DY_specialWeight,'DY_specialWeight/F')

    # For LO/NLO Weighting
    NLO_Weight = array('f',[0]*1)
    newtree.Branch('NLO_Weight',NLO_Weight,'NLO_Weight/F')
    

    if 'DY' in job.name:
            nloweight = ROOT.TTreeFormula('nloweight', "VHbb::LOtoNLOWeightBjetSplitEtabb(abs(Jet_eta[hJCidx[0]]-Jet_eta[hJCidx[1]]),Sum$(GenJet_pt>20 && abs(GenJet_eta)<2.4&&GenJet_numBHadrons))", tree)

            specialWeight = ROOT.TTreeFormula('specialWeight',job.specialweight, tree)




    # For 2016E+F HIP mitigation
    #bTagWeightEF = array('f',[0]*1)
    #newtree.Branch('bTagWeightEF',bTagWeightEF,'bTagWeightEF/F')
    
    mTrigSFWeightUp   = array('f',[0]*1)
    mTrigSFWeightDown = array('f',[0]*1)
    
    mIdSFWeightUp      = array('f',[0]*1)
    mIdSFWeightDown    = array('f',[0]*1)
    
    mIsoSFWeightUp     = array('f',[0]*1)
    mIsoSFWeightDown   = array('f',[0]*1)
    
    eId90SFWeightUp  = array('f',[0]*1)
    eId90SFWeightDown= array('f',[0]*1)
    
    eTrigSFWeightUp   = array('f',[0]*1)
    eTrigSFWeightDown = array('f',[0]*1)
    
    newtree.Branch('mTrigSFWeightUp',mTrigSFWeightUp,'mTrigSFWeightUp/F')
    newtree.Branch('mTrigSFWeightDown',mTrigSFWeightDown,'mTrigSFWeightDown/F')
    newtree.Branch('mIdSFWeightUp',mIdSFWeightUp,'mIdSFWeightUp/F')
    newtree.Branch('mIdSFWeightDown',mIdSFWeightDown,'mIdSFWeightDown/F')
    newtree.Branch('mIsoSFWeightUp',mIsoSFWeightUp,'mIsoSFWeightUp/F')
    newtree.Branch('mIsoSFWeightDown',mIsoSFWeightDown,'mIsoSFWeightDown/F')
    newtree.Branch('eId90SFWeightUp', eId90SFWeightUp, 'eId90SFWeightUp/F')
    newtree.Branch('eId90SFWeightDown', eId90SFWeightDown, 'eId90SFWeightDown/F')
    newtree.Branch('eTrigSFWeight', eTrigSFWeight, 'eTrigSFWeight/F')
    newtree.Branch('eTrigSFWeightDown', eTrigSFWeightDown, 'eTrigSFWeightDown/F')

    
    # ======== Regression branches ==========
    applyRegression = False

    '''

    applyRegression = True


    #H_pt = ROOT.H()
    #HNoReg_pt = ROOT.H()
    

    #Jet_pt = array('f',[0]*2)
    #Jet_mass = array('f',[0]*2)
    

    hJet_pt_reg = array('f',[0]*2)
    newtree.Branch('hJet_pt_reg', hJet_pt_reg, 'hJet_pt_reg[2]/F')
    
    #hJet_mass_reg = array('f',[0]*2)
    #newtree.Branch('hJet_mass_reg', hJet_mass_reg, 'hJet_mass_reg[2]/F')
    
    # New branch for trying to correct mass with 3rd jet nearby the dijets
    H_mass_addJet = array('f',[0]*1)
    H_mass_addJet_noReg = array('f',[0]*1)
    newtree.Branch('H_mass_addJet', H_mass_addJet, 'H_mass_addJet[1]/F')
    newtree.Branch('H_mass_addJet_noReg', H_mass_addJet_noReg, 'H_mass_addJet_noReg[1]/F')
    
    HCSV_reg_mass = array('f',[0]*1)    
    newtree.Branch('HCSV_reg_mass', HCSV_reg_mass, 'HCSV_reg_mass[1]/F') 

    HCSV_reg_pt = array('f',[0]*1)
    newtree.Branch('HCSV_reg_pt', HCSV_reg_pt, 'HCSV_reg_pt[1]/F')
    '''



    
    # define all the readers
    #readerJet0 = ROOT.TMVA.Reader("!Color:!Silent" )
    #readerJet1 = ROOT.TMVA.Reader("!Color:!Silent" )

    '''
    readerJet0_JER_up = ROOT.TMVA.Reader("!Color:!Silent" )
    readerJet1_JER_up = ROOT.TMVA.Reader("!Color:!Silent" )
    readerJet0_JER_down = ROOT.TMVA.Reader("!Color:!Silent" )
    readerJet1_JER_down = ROOT.TMVA.Reader("!Color:!Silent" )
    readerJet0_JEC_up = ROOT.TMVA.Reader("!Color:!Silent" )
    readerJet1_JEC_up = ROOT.TMVA.Reader("!Color:!Silent" )
    readerJet0_JEC_down = ROOT.TMVA.Reader("!Color:!Silent" )
    readerJet1_JEC_down = ROOT.TMVA.Reader("!Color:!Silent" )


    theForms = {}
    theVars0 = {}
    theVars1 = {}

    def addVarsToReader(reader,theVars,theForms,i):
        for key in regVars:
            print key
            var = regDict[key]
            theVars[key] = array( 'f', [ 0 ] )
            reader.AddVariable(key,theVars[key])
            formula = regDict[key].replace("[0]","[%.0f]" %i)

            if key == 'Jet_chHEF+Jet_neHEF':
                print 'Adding var: %s with %s to readerJet%.0f' %(key,formula,i)
                print 'Form:', 'form_reg_Jet_chHEF_%.0f+Jet_neHEF_%.0f'%(i,i)
                theForms['form_reg_Jet_chHEF_%.0f+Jet_neHEF_%.0f'%(i,i)] = formula #ROOT.TTreeFormula("form_reg_%s_%.0f"%(key,i),'%s' %(formula),tree)
                #theForms['form_reg_%s_%.0f'%(key,i)].GetNdata()

            else:
                print 'Adding var: %s with %s to readerJet%.0f' %(key,formula,i)
                print 'Form:', 'form_reg_%s_%.0f'%(key,i)
		theForms['form_reg_%s_%.0f'%(key,i)] = formula
                #theForms['form_reg_%s_%.0f'%(key,i)].GetNdata()


	return

    addVarsToReader(readerJet0,theVars0,theForms,0)
    addVarsToReader(readerJet1,theVars1,theForms,1)
    readerJet0.BookMVA( "jet0Regression", regWeight )
    readerJet1.BookMVA( "jet1Regression", regWeight )
    '''

    '''
    theVars0_JER_up = {}
    theVars1_JER_up = {}
    theVars0_JER_down = {}
    theVars1_JER_down = {}
    theVars0_JEC_up = {}
    theVars1_JEC_up = {}
    theVars0_JEC_down = {}
    theVars1_JEC_down = {}
    '''


    '''
    def addVarsToReader(reader,regDict,regVars,theVars,theForms,i,hJet_MET_dPhiArray,METet,rho,hJet_MtArray,hJet_EtArray,hJet_ptRawArray,syst=""):

        print '\n======== Adding Variables to Reader for Jet', i, ' ========'	    

        for key in regVars:
		
            var = regDict[key]
            theVars[key+syst] = array( 'f', [ 0 ] )

	    reader.AddVariable(key,theVars[key+syst])
            formulaX = var
	    brakets = ""
	    if formulaX.find("[hJCidx[0]]"): brakets = "[hJCidx[0]]"
	    elif formulaX.find("[hJCidx[1]]"): brakets = "[hJCidx[1]]"
	    elif formulaX.find("[0]"): brakets = "[0]"
	    elif formulaX.find("[1]"): brakets = "[1]"
	    else: pass
	    
	    formulaX = formulaX.replace(brakets,"[X]")
	    	    
	    print 'Adding var: %s to with reference %s readerJet%s' %(key, formulaX, i)
	    
	    if syst == "":
		    pass
	    # formulaX = formulaX.replace("Jet_pt[X]","Jet_rawPt[X]*Jet_corr[X]*Jet_corr_JER[X]")
	    elif syst == "JER_up":
		    formulaX = formulaX.replace("Jet_pt[X]","Jet_rawPt[X]*Jet_corr[X]*Jet_corr_JERUp[X]")
	    elif syst == "JER_down":
		    formulaX = formulaX.replace("Jet_pt[X]","Jet_rawPt[X]*Jet_corr[X]*Jet_corr_JERDown[X]")
	    elif syst == "JEC_up":
		    formulaX = formulaX.replace("Jet_pt[X]","Jet_rawPt[X]*Jet_corr_JECUp[X]*Jet_corr_JER[X]")
	    elif syst == "JEC_down":
		    formulaX = formulaX.replace("Jet_pt[X]","Jet_rawPt[X]*Jet_corr_JECDown[X]*Jet_corr_JER[X]")
	    else:
		    raise Exception(syst," is unknown!")
	    
	    formula = formulaX.replace("[X]",brakets)
	    formula = formula.replace("[0]","[%.0f]" %i)
	    theForms['form_reg_%s_%.0f'%(key+syst,i)] = ROOT.TTreeFormula("form_reg_%s_%.0f"%(key+syst,i),'%s' %(formula),tree)
	    
	    #theForms['form_reg_%s_%.0f'%(key,i)] = ROOT.TTreeFormula("form_reg_%s_%.0f"%(key,i),'%s' %(formula),tree)
	    theForms['form_reg_%s_%.0f'%(key,i)].GetNdata()
	    
        print '=====================================================\n'

        return 


    addVarsToReader(readerJet0,regDict,regVars,theVars0,theForms,0,hJet_MET_dPhiArray,METet,rho,hJet_MtArray,hJet_EtArray,hJet_ptRawArray)    
    addVarsToReader(readerJet1,regDict,regVars,theVars1,theForms,1,hJet_MET_dPhiArray,METet,rho,hJet_MtArray,hJet_EtArray,hJet_ptRawArray)    
    
    if job.type != 'DATA':
	    addVarsToReader(readerJet0_JER_up,regDict,regVars,theVars0,theForms,0,hJet_MET_dPhiArray,METet,rho,hJet_MtArray,hJet_EtArray,hJet_ptRawArray,"JER_up")
	    addVarsToReader(readerJet1_JER_up,regDict,regVars,theVars1,theForms,1,hJet_MET_dPhiArray,METet,rho,hJet_MtArray,hJet_EtArray,hJet_ptRawArray,"JER_up")
	    addVarsToReader(readerJet0_JER_down,regDict,regVars,theVars0,theForms,0,hJet_MET_dPhiArray,METet,rho,hJet_MtArray,hJet_EtArray,hJet_ptRawArray,"JER_down")
	    addVarsToReader(readerJet1_JER_down,regDict,regVars,theVars1,theForms,1,hJet_MET_dPhiArray,METet,rho,hJet_MtArray,hJet_EtArray,hJet_ptRawArray,"JER_down")
	    addVarsToReader(readerJet0_JEC_up,regDict,regVars,theVars0,theForms,0,hJet_MET_dPhiArray,METet,rho,hJet_MtArray,hJet_EtArray,hJet_ptRawArray,"JEC_up")
	    addVarsToReader(readerJet1_JEC_up,regDict,regVars,theVars1,theForms,1,hJet_MET_dPhiArray,METet,rho,hJet_MtArray,hJet_EtArray,hJet_ptRawArray,"JEC_up")
	    addVarsToReader(readerJet0_JEC_down,regDict,regVars,theVars0,theForms,0,hJet_MET_dPhiArray,METet,rho,hJet_MtArray,hJet_EtArray,hJet_ptRawArray,"JEC_down")
	    addVarsToReader(readerJet1_JEC_down,regDict,regVars,theVars1,theForms,1,hJet_MET_dPhiArray,METet,rho,hJet_MtArray,hJet_EtArray,hJet_ptRawArray,"JEC_down")
	    
    readerJet0.BookMVA( "jet0Regression", regWeight )
    readerJet1.BookMVA( "jet1Regression", regWeight )

    if job.type != 'DATA':
	    readerJet0_JER_up.BookMVA( "jet0Regression", regWeight )
	    readerJet1_JER_up.BookMVA( "jet1Regression", regWeight )
	    readerJet0_JER_down.BookMVA( "jet0Regression", regWeight )
	    readerJet1_JER_down.BookMVA( "jet1Regression", regWeight )
	    readerJet0_JEC_up.BookMVA( "jet0Regression", regWeight )
	    readerJet1_JEC_up.BookMVA( "jet1Regression", regWeight )
	    readerJet0_JEC_down.BookMVA( "jet0Regression", regWeight )
	    readerJet1_JEC_down.BookMVA( "jet1Regression", regWeight )
    '''
	    
    	    
    #Add training Flag
    #EventForTraining = array('i',[0])
    #newtree.Branch('EventForTraining',EventForTraining,'EventForTraining/I')
    #EventForTraining[0]=0
    
    #TFlag=ROOT.TTreeFormula("EventForTraining","evt%2",tree)


    '''
    if True:

	    # Add new JER/JEC SYS branches for high/low and central/forward regions

	    # Jet flag for low/high central/forward region
            hJet_low     = array('f',[0]*2)
            hJet_high    = array('f',[0]*2)
            hJet_central = array('f',[0]*2)
            hJet_forward = array('f',[0]*2)

            newtree.Branch('hJet_low', hJet_low, 'hJet_low[2]/F')
            newtree.Branch('hJet_high',hJet_high, 'hJet_high[2]/F')
            newtree.Branch('hJet_central', hJet_central, 'hJet_central[2]/F')
            newtree.Branch('hJet_forward', hJet_forward, 'hJet_forward[2]/F')

            #Do loop here to define all the variables
            VarList = ['HCSV_reg_corrSYSUD_mass_CAT','HCSV_reg_corrSYSUD_pt_CAT', 'HCSV_reg_corrSYSUD_phi_CAT', 'HCSV_reg_corrSYSUD_eta_CAT','Jet_pt_reg_corrSYSUD_CAT']
            SysList = ['JER','JEC']
            UDList = ['Up','Down']
            CatList = ['low','high','central','forward']
            SysDicList = []

            ConditionDic = {'low':'len(tree.hJCidx)==2 and tree.Jet_corr_SYSUD[tree.hJCidx[0]]>0. and tree.Jet_corr_SYSUD[tree.hJCidx[1]]>0. and (tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[0]]<100. or tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[1]]<100.)',\
                            'high':'len(tree.hJCidx)==2 and tree.Jet_corr_SYSUD[tree.hJCidx[0]]>0. and tree.Jet_corr_SYSUD[tree.hJCidx[1]]>0. and (tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[0]]>100. or tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[1]]>100.)',\
                            'central':'len(tree.hJCidx)==2 and tree.Jet_corr_SYSUD[tree.hJCidx[0]]>0. and tree.Jet_corr_SYSUD[tree.hJCidx[1]]>0. and (abs(tree.Jet_eta[tree.hJCidx[0]])<1.4 or abs(tree.Jet_eta[tree.hJCidx[1]])<1.4)',\
                            'forward':'len(tree.hJCidx)==2 and tree.Jet_corr_SYSUD[tree.hJCidx[0]]>0. and tree.Jet_corr_SYSUD[tree.hJCidx[1]]>0. and (abs(tree.Jet_eta[tree.hJCidx[0]])>1.4 or abs(tree.Jet_eta[tree.hJCidx[1]])>1.4)'
                    }
            JetConditionDic = {'low':'tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[INDEX]]<100.',\
                               'high':'tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[INDEX]]>100.',\
                               'central':'abs(tree.Jet_eta[tree.hJCidx[INDEX]])<1.4',\
                               'forward':'abs(tree.Jet_eta[tree.hJCidx[INDEX]])>1.4'
                    }
            #DefaultVar = {'HCSV_reg_corrSYSUD_mass_CAT':'tree.HCSV_reg_mass','HCSV_reg_corrSYSUD_pt_CAT':'tree.HCSV_reg_pt','HCSV_reg_corrSYSUD_phi_CAT':'tree.HCSV_reg_phi','HCSV_reg_corrSYSUD_eta_CAT':'tree.HCSV_reg_eta'}
            DefaultVar = {'HCSV_reg_corrSYSUD_mass_CAT':'tree.HCSV_reg_mass','HCSV_reg_corrSYSUD_pt_CAT':'tree.HCSV_reg_pt','HCSV_reg_corrSYSUD_phi_CAT':'tree.HCSV_reg_phi','HCSV_reg_corrSYSUD_eta_CAT':'tree.HCSV_reg_eta','Jet_pt_reg_corrSYSUD_CAT':'tree.Jet_pt_reg[tree.hJCidx[INDEX]]'}
            SYSVar = {'HCSV_reg_corrSYSUD_mass_CAT':'tree.HCSV_reg_mass*(HJet_sys.M()/HJet.M())','HCSV_reg_corrSYSUD_pt_CAT':'tree.HCSV_reg_pt*(HJet_sys.Pt()/HJet.Pt())','HCSV_reg_corrSYSUD_phi_CAT':'tree.HCSV_reg_phi*(HJet_sys.Phi()/HJet.Phi())','HCSV_reg_corrSYSUD_eta_CAT':'tree.HCSV_reg_eta*(HJet_sys.Eta()/HJet.Eta())','Jet_pt_reg_corrSYSUD_CAT':'tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[INDEX]]'}

            #Make a dic corresponding to each sys and create the variables
            for var in VarList:
                for syst in SysList:
                    for cat in CatList:
                        for ud in UDList:
                            #fill Dic
                            SysDic = {}
                            SysDic['var'] = var
                            SysDic['sys'] = syst
                            SysDic['UD'] = ud
                            SysDic['cat'] = cat
                            SysDic['varname'] = var.replace('SYS',syst).replace('UD',ud).replace('CAT',cat)
                            #Define var
                            if var == 'Jet_pt_reg_corrSYSUD_CAT':
                                #print 'yeah man'
                                SysDic['varptr'] = array('f',2*[0])
                                newtree.Branch(SysDic['varname'],SysDic['varptr'],SysDic['varname']+'[2]/F')
                                SysDicList.append(SysDic)
                            else:
                                SysDic['varptr'] = array('f',[0])
                                newtree.Branch(SysDic['varname'],SysDic['varptr'],SysDic['varname']+'/F')
                                SysDicList.append(SysDic)



	    #JER branches
	    HCSV_reg_mass_JER_up = array('f',[0]*1)
	    HCSV_reg_mass_JER_down = array('f',[0]*1)
	    newtree.Branch('HCSV_reg_mass_JER_down', HCSV_reg_mass_JER_down, 'HCSV_reg_mass_JER_down[1]/F')
	    newtree.Branch('HCSV_reg_mass_JER_up', HCSV_reg_mass_JER_up, 'HCSV_reg_mass_JER_up[1]/F')

	    HCSV_reg_pt_JER_up = array('f',[0]*1)
	    newtree.Branch('HCSV_reg_pt_JER_up', HCSV_reg_pt_JER_up, 'HCSV_reg_pt_JER_up[1]/F')
	    HCSV_reg_pt_JER_down = array('f',[0]*1)
	    newtree.Branch('HCSV_reg_pt_JER_down', HCSV_reg_pt_JER_down, 'HCSV_reg_pt_JER_down[1]/F')
	    
	    hJet_pt_JER_up = array('f',[0]*2)
	    newtree.Branch('hJet_pt_JER_up',hJet_pt_JER_up,'hJet_pt_JER_up[2]/F')
	    hJet_pt_JER_down = array('f',[0]*2)
	    newtree.Branch('hJet_pt_JER_down',hJet_pt_JER_down,'hJet_pt_JER_down[2]/F')
	    hJet_e_JER_up = array('f',[0]*2)
	    newtree.Branch('hJet_e_JER_up',hJet_e_JER_up,'hJet_e_JER_up[2]/F')
	    hJet_e_JER_down = array('f',[0]*2)
	    newtree.Branch('hJet_e_JER_down',hJet_e_JER_down,'hJet_e_JER_down[2]/F')
	    H_JER = array('f',[0]*4)
	    newtree.Branch('H_JER',H_JER,'mass_up:mass_down:pt_up:pt_down/F')
	    HVMass_JER_up = array('f',[0])
	    HVMass_JER_down = array('f',[0])
	    newtree.Branch('HVMass_JER_up',HVMass_JER_up,'HVMass_JER_up/F')
	    newtree.Branch('HVMass_JER_down',HVMass_JER_down,'HVMass_JER_down/F')
	    angleHB_JER_up = array('f',[0])
	    angleHB_JER_down = array('f',[0])
	    angleZZS_JER_up = array('f',[0])
	    angleZZS_JER_down = array('f',[0])
	    newtree.Branch('angleHB_JER_up',angleHB_JER_up,'angleHB_JER_up/F')
	    newtree.Branch('angleHB_JER_down',angleHB_JER_down,'angleHB_JER_down/F')
	    newtree.Branch('angleZZS_JER_up',angleZZS_JER_up,'angleZZS_JER_up/F')
	    newtree.Branch('angleZZS_JER_down',angleZZS_JER_down,'angleZZS_JER_down/F')
	    
	    #JES branches
	    HCSV_reg_mass_JES_up = array('f',[0]*1)
	    newtree.Branch('HCSV_reg_mass_JES_up', HCSV_reg_mass_JES_up, 'HCSV_reg_mass_JES_up[1]/F')
	    HCSV_reg_mass_JES_down = array('f',[0]*1)
	    newtree.Branch('HCSV_reg_mass_JES_down', HCSV_reg_mass_JES_down, 'HCSV_reg_mass_JES_down[1]/F')
	    
	    HCSV_reg_pt_JES_up = array('f',[0]*1)
	    newtree.Branch('HCSV_reg_pt_JES_up', HCSV_reg_pt_JES_up, 'HCSV_reg_pt_JES_up[1]/F')
	    HCSV_reg_pt_JES_down = array('f',[0]*1)
	    newtree.Branch('HCSV_reg_pt_JES_down', HCSV_reg_pt_JES_down, 'HCSV_reg_pt_JES_down[1]/F')
	    
	    hJet_pt_JES_up = array('f',[0]*2)
	    newtree.Branch('hJet_pt_JES_up',hJet_pt_JES_up,'hJet_pt_JES_up[2]/F')
	    hJet_pt_JES_down = array('f',[0]*2)
	    newtree.Branch('hJet_pt_JES_down',hJet_pt_JES_down,'hJet_pt_JES_down[2]/F')
	    hJet_e_JES_up = array('f',[0]*2)
	    newtree.Branch('hJet_e_JES_up',hJet_e_JES_up,'hJet_e_JES_up[2]/F')
	    hJet_e_JES_down = array('f',[0]*2)
	    newtree.Branch('hJet_e_JES_down',hJet_e_JES_down,'hJet_e_JES_down[2]/F')
	    H_JES = array('f',[0]*4)
	    newtree.Branch('H_JES',H_JES,'mass_up:mass_down:pt_up:pt_down/F')
	    HVMass_JES_up = array('f',[0])
	    HVMass_JES_down = array('f',[0])
	    newtree.Branch('HVMass_JES_up',HVMass_JES_up,'HVMass_JES_up/F')
	    newtree.Branch('HVMass_JES_down',HVMass_JES_down,'HVMass_JES_down/F')
	    angleHB_JES_up = array('f',[0])
	    angleHB_JES_down = array('f',[0])
	    angleZZS_JES_up = array('f',[0])
	    angleZZS_JES_down = array('f',[0])
	    newtree.Branch('angleHB_JES_up',angleHB_JES_up,'angleHB_JES_up/F')
	    newtree.Branch('angleHB_JES_down',angleHB_JES_down,'angleHB_JES_down/F')
	    newtree.Branch('angleZZS_JES_up',angleZZS_JES_up,'angleZZS_JES_up/F')
	    newtree.Branch('angleZZS_JES_down',angleZZS_JES_down,'angleZZS_JES_down/F')
	    '''



    '''
    ### Adding new variable from configuration ###
    newVariableNames = []
    try:
	    writeNewVariables = eval(config.get("Regression","writeNewVariables"))
	    newVariableNames = writeNewVariables.keys()
	    newVariables = {}
	    newVariableFormulas = {}
	    for variableName in newVariableNames:
		    newVariables[variableName] = array('f',[0])
		    newtree.Branch(variableName,newVariables[variableName],variableName+'/F')
		    newVariableFormulas[variableName] =ROOT.TTreeFormula(variableName,writeNewVariables[variableName],tree)
		    print "adding variable ",variableName,", using formula",writeNewVariables[variableName]," ."
    except:
	    pass
	    
     '''
	    

    
    print '\n\n======== Filling New Branches/ Applying Regression ========'
        
    for entry in range(0,nEntries):

	    # for testing
	    if entry > 10000: break
	    	    
            tree.GetEntry(entry)

	    if entry % 10000 is 0: print 'Event #', entry
	    
            if tree.nJet < 2: continue
	    #if tree.nhJCidx == 0 : continue
	    
	    # Set the special Weight
	    # Init the weight string
	    if 'DY' not in job.name: 
		    DY_specialWeight[0] = 1
		    NLO_Weight[0] = 1		    
	    else:
		    specialWeight_ = specialWeight.EvalInstance()
		    DY_specialWeight[0] = specialWeight_
		    
		    nlo_weight_ = nlo_weight.EvalInstance()
		    NLO_Weight[0] = nlo_weight_ 

	    '''
	    ### Fill new variable from configuration ###
	    for variableName in newVariableNames:
		    newVariableFormulas[variableName].GetNdata()
		    newVariables[variableName][0] = newVariableFormulas[variableName].EvalInstance()
	    '''
	    

	    #if tree.hJCidx[0] > 10 or tree.hJCidx[1] > 10: continue
	    
	    '''
	    Jet_pt_0 = tree.Jet_pt[tree.hJCidx[0]]
	    Jet_pt_1 = tree.Jet_pt[tree.hJCidx[1]]
            Jet_eta_0 = tree.Jet_eta[tree.hJCidx[0]]
            Jet_eta_1 = tree.Jet_eta[tree.hJCidx[1]]
            Jet_ptRaw0 = tree.Jet_rawPt[tree.hJCidx[0]]
            Jet_ptRaw1 = tree.Jet_rawPt[tree.hJCidx[1]]
	    Jet_m_0 = tree.Jet_mass[tree.hJCidx[0]]
	    Jet_m_1 = tree.Jet_mass[tree.hJCidx[1]]
	    Jet_phi_0 = tree.Jet_phi[tree.hJCidx[0]]
            Jet_phi_1 = tree.Jet_phi[tree.hJCidx[1]]
	    if job.type != 'DATA': hJet_mcPt0 = tree.Jet_mcPt[tree.hJCidx[0]]
	    if job.type != 'DATA': hJet_mcPt1 = tree.Jet_mcPt[tree.hJCidx[1]]
	    Jet_mass_0 = tree.Jet_mass[tree.hJCidx[0]]
	    Jet_mass_1 = tree.Jet_mass[tree.hJCidx[1]]


	    Jet_btagCSV_0 = tree.Jet_btagCSV[tree.hJCidx[0]]
            Jet_btagCSV_1 = tree.Jet_btagCSV[tree.hJCidx[1]]
	    

	    Jet_e_0 = hJ0.E()
            Jet_e_1 = hJ1.E()
            Jet_mt_0 = hJ0.Mt()
            Jet_mt_1 = hJ1.Mt()
            Jet_met_dPhi_0 =   deltaPhi(tree.met_phi,Jet_phi_0)
            Jet_met_dPhi_1 =   deltaPhi(tree.met_phi,Jet_phi_1)
	    
	    met_pt_0 = tree.met_pt
	    met_pt_1 = tree.met_pt

            #Jet_met_proj_0 = projectionMETOntoJet(met_pt_0, tree.met_phi,Jet_pt_0, Jet_phi_0)
            #Jet_met_proj_1 = projectionMETOntoJet(met_pt_0, tree.met_phi,Jet_pt_1, Jet_phi_1)

            #met_projection_Hpt.Fill(Jet_pt_0, Jet_met_proj_0)

            Jet_vtxPt_0 = max(0.,tree.Jet_vtxPt[tree.hJCidx[0]])
            Jet_vtxPt_1 = max(0.,tree.Jet_vtxPt[tree.hJCidx[1]])
            Jet_vtx3dL_0= max(0.,tree.Jet_vtx3DVal[tree.hJCidx[0]])
            Jet_vtx3dL_1= max(0.,tree.Jet_vtx3DVal[tree.hJCidx[1]])
            Jet_vtx3deL_0= max(0.,tree.Jet_vtx3DSig[tree.hJCidx[0]])
            Jet_vtx3deL_1= max(0.,tree.Jet_vtx3DSig[tree.hJCidx[1]])
            Jet_vtxMass_0= max(0.,tree.Jet_vtxMass[tree.hJCidx[0]])
            Jet_vtxMass_1= max(0.,tree.Jet_vtxMass[tree.hJCidx[1]])
            Jet_vtxNtrk_0= max(0.,tree.Jet_vtxNtracks[tree.hJCidx[0]])
            Jet_vtxNtrk_1= max(0.,tree.Jet_vtxNtracks[tree.hJCidx[1]])
            Jet_chEmEF_0=tree.Jet_chEmEF[tree.hJCidx[0]]
            Jet_chEmEF_1=tree.Jet_chEmEF[tree.hJCidx[1]]
            Jet_chHEF_0=tree.Jet_chHEF[tree.hJCidx[0]]
            Jet_chHEF_1=tree.Jet_chHEF[tree.hJCidx[1]]
            Jet_neHEF_0=tree.Jet_neHEF[tree.hJCidx[0]]
            Jet_neHEF_1=tree.Jet_neHEF[tree.hJCidx[1]]
            Jet_neEmEF_0=tree.Jet_neEmEF[tree.hJCidx[0]]
            Jet_neEmEF_1=tree.Jet_neEmEF[tree.hJCidx[1]]


	    Jet_rawPt_0 = tree.Jet_rawPt[tree.hJCidx[0]]
            Jet_rawPt_1 = tree.Jet_rawPt[tree.hJCidx[1]]
            #Jet_JECUnc_0 = tree.Jet_JECUnc[tree.hJCidx[0]]
            #Jet_JECUnc_1 = tree.Jet_JECUnc[tree.hJCidx[1]]
            Jet_chMult_0 = tree.Jet_chMult[tree.hJCidx[0]]
            Jet_chMult_1 = tree.Jet_chMult[tree.hJCidx[1]]
            Jet_leadTrackPt_0 = max(0.,tree.Jet_leadTrackPt[tree.hJCidx[0]])
            Jet_leadTrackPt_1 = max(0.,tree.Jet_leadTrackPt[tree.hJCidx[1]])
            Jet_leptonPtRel_0 = max(0.,tree.Jet_leptonPtRel[tree.hJCidx[0]])
            Jet_leptonPtRel_1= max(0.,tree.Jet_leptonPtRel[tree.hJCidx[1]])
            Jet_leptonDeltaR_0 = max(0.,tree.Jet_leptonDeltaR[tree.hJCidx[0]])
            Jet_leptonDeltaR_1 = max(0.,tree.Jet_leptonDeltaR[tree.hJCidx[0]])
            Jet_leptonPt_0 = max(0.,tree.Jet_leptonPt[tree.hJCidx[0]])
            Jet_leptonPt_1= max(0.,tree.Jet_leptonPt[tree.hJCidx[1]])
            rho_0=tree.rho
            rho_1=tree.rho

            nPVs_0=tree.nPVs
            nPVs_1=tree.nPVs
	    
	    hJ0.SetPtEtaPhiM(Jet_pt_0,Jet_eta_0,Jet_phi_0,Jet_m_0)
            hJ1.SetPtEtaPhiM(Jet_pt_1,Jet_eta_1,Jet_phi_1,Jet_m_1)

            Jet_e_0 = hJ0.E()
            Jet_e_1 = hJ1.E()
            Jet_mt_0 = hJ0.Mt()
            Jet_mt_1 = hJ1.Mt()



	    Jet_btagCSV_0 = tree.Jet_btagCSV[tree.hJCidx[0]]
            Jet_btagCSV_1 = tree.Jet_btagCSV[tree.hJCidx[1]]
	    

	    Jet_e_0 = hJ0.E()
            Jet_e_1 = hJ1.E()
            Jet_mt_0 = hJ0.Mt()
            Jet_mt_1 = hJ1.Mt()
            Jet_met_dPhi_0 =   deltaPhi(tree.met_phi,Jet_phi_0)
            Jet_met_dPhi_1 =   deltaPhi(tree.met_phi,Jet_phi_1)
	    
	    met_pt_0 = tree.met_pt
	    met_pt_1 = tree.met_pt

            #Jet_met_proj_0 = projectionMETOntoJet(met_pt_0, tree.met_phi,Jet_pt_0, Jet_phi_0)
            #Jet_met_proj_1 = projectionMETOntoJet(met_pt_0, tree.met_phi,Jet_pt_1, Jet_phi_1)

            #met_projection_Hpt.Fill(Jet_pt_0, Jet_met_proj_0)

            Jet_vtxPt_0 = max(0.,tree.Jet_vtxPt[tree.hJCidx[0]])
            Jet_vtxPt_1 = max(0.,tree.Jet_vtxPt[tree.hJCidx[1]])
            Jet_vtx3dL_0= max(0.,tree.Jet_vtx3DVal[tree.hJCidx[0]])
            Jet_vtx3dL_1= max(0.,tree.Jet_vtx3DVal[tree.hJCidx[1]])
            Jet_vtx3deL_0= max(0.,tree.Jet_vtx3DSig[tree.hJCidx[0]])
            Jet_vtx3deL_1= max(0.,tree.Jet_vtx3DSig[tree.hJCidx[1]])
            Jet_vtxMass_0= max(0.,tree.Jet_vtxMass[tree.hJCidx[0]])
            Jet_vtxMass_1= max(0.,tree.Jet_vtxMass[tree.hJCidx[1]])
            Jet_vtxNtrk_0= max(0.,tree.Jet_vtxNtracks[tree.hJCidx[0]])
            Jet_vtxNtrk_1= max(0.,tree.Jet_vtxNtracks[tree.hJCidx[1]])
            Jet_chEmEF_0=tree.Jet_chEmEF[tree.hJCidx[0]]
            Jet_chEmEF_1=tree.Jet_chEmEF[tree.hJCidx[1]]
            Jet_chHEF_0=tree.Jet_chHEF[tree.hJCidx[0]]
            Jet_chHEF_1=tree.Jet_chHEF[tree.hJCidx[1]]
            Jet_neHEF_0=tree.Jet_neHEF[tree.hJCidx[0]]
            Jet_neHEF_1=tree.Jet_neHEF[tree.hJCidx[1]]
            Jet_neEmEF_0=tree.Jet_neEmEF[tree.hJCidx[0]]
            Jet_neEmEF_1=tree.Jet_neEmEF[tree.hJCidx[1]]


	    Jet_rawPt_0 = tree.Jet_rawPt[tree.hJCidx[0]]
            Jet_rawPt_1 = tree.Jet_rawPt[tree.hJCidx[1]]
            #Jet_JECUnc_0 = tree.Jet_JECUnc[tree.hJCidx[0]]
            #Jet_JECUnc_1 = tree.Jet_JECUnc[tree.hJCidx[1]]
            Jet_chMult_0 = tree.Jet_chMult[tree.hJCidx[0]]
            Jet_chMult_1 = tree.Jet_chMult[tree.hJCidx[1]]
            Jet_leadTrackPt_0 = max(0.,tree.Jet_leadTrackPt[tree.hJCidx[0]])
            Jet_leadTrackPt_1 = max(0.,tree.Jet_leadTrackPt[tree.hJCidx[1]])
            Jet_leptonPtRel_0 = max(0.,tree.Jet_leptonPtRel[tree.hJCidx[0]])
            Jet_leptonPtRel_1= max(0.,tree.Jet_leptonPtRel[tree.hJCidx[1]])
            Jet_leptonDeltaR_0 = max(0.,tree.Jet_leptonDeltaR[tree.hJCidx[0]])
            Jet_leptonDeltaR_1 = max(0.,tree.Jet_leptonDeltaR[tree.hJCidx[0]])
            Jet_leptonPt_0 = max(0.,tree.Jet_leptonPt[tree.hJCidx[0]])
            Jet_leptonPt_1= max(0.,tree.Jet_leptonPt[tree.hJCidx[1]])
            rho_0=tree.rho
            rho_1=tree.rho

            nPVs_0=tree.nPVs
            nPVs_1=tree.nPVs
	    
	    hJ0.SetPtEtaPhiM(Jet_pt_0,Jet_eta_0,Jet_phi_0,Jet_m_0)
            hJ1.SetPtEtaPhiM(Jet_pt_1,Jet_eta_1,Jet_phi_1,Jet_m_1)

            Jet_e_0 = hJ0.E()
            Jet_e_1 = hJ1.E()
            Jet_mt_0 = hJ0.Mt()
            Jet_mt_1 = hJ1.Mt()
	    '''

	    

	    '''
            for key, value in regDict.items():
		    for syst in ["","JER_up","JER_down","JEC_up","JEC_down"]:
			    if job.type == 'DATA' and not syst is "": continue
			    #theForms["form_reg_%s_0" %(key+syst)].GetNdata();
			    #theForms["form_reg_%s_1" %(key+syst)].GetNdata();
			    theVars0[key+syst][0] = theForms["form_reg_%s_0" %(key+syst)].EvalInstance()
			    theVars1[key+syst][0] = theForms["form_reg_%s_1" %(key+syst)].EvalInstance()
	    '''
	    
	    #for key in regVars:
            #        theVars0[key][0] = eval("%s_0" %(key))
            #        theVars1[key][0] = eval("%s_1" %(key))
	    

	    # for adding 3rd jet
	    #hJ0.SetPtEtaPhiM(Jet_pt_0, Jet_eta_0, Jet_phi_0, Jet_m_0)
	    #hJ1.SetPtEtaPhiM(Jet_pt_1, Jet_eta_1, Jet_phi_1, Jet_m_1)
	    
	    #HCSV_dR_reg[0]   = hJ0.DeltaR(hJ1)
	    #HCSV_dR_reg[0]   = deltaR(tree.HCSV_reg_phi, tree.HCSV_reg_eta, tree.V_phi, tree.V_eta)
	    #HCSV_dEta_reg[0] = abs(hJ0.Eta()-hJ1.Eta())
	    #HCSV_dPhi_reg[0] = abs(deltaPhi(hJ0.Phi(), hJ1.Phi()))
	    #HVdPhi_reg[0]    = abs(deltaPhi(tree.HCSV_reg_phi, tree.V_phi))
	    
	    
	    #Jet_mt[0] = hJ0.Mt()
	    #Jet_mt[1] = hJ1.Mt()

	    '''
	    hJet_ptOld[0] = tree.Jet_pt[tree.hJCidx[0]]
	    hJet_ptOld[1] = tree.Jet_pt[tree.hJCidx[1]]
	    if job.type != 'DATA': hJet_ptMc[0] = tree.Jet_mcPt[tree.hJCidx[0]]
	    if job.type != 'DATA': hJet_ptMc[1] = tree.Jet_mcPt[tree.hJCidx[1]]
	    hJet_phi[0] = tree.Jet_phi[tree.hJCidx[0]]
	    hJet_phi[1] = tree.Jet_phi[tree.hJCidx[1]]
	    hJet_eta[0] = tree.Jet_eta[tree.hJCidx[0]]
	    hJet_eta[1] = tree.Jet_eta[tree.hJCidx[1]]
	    hJet_mass[0] = tree.Jet_mass[tree.hJCidx[0]]
	    hJet_mass[1] = tree.Jet_mass[tree.hJCidx[1]]
	    '''

            # Add FSR into the Higgs MAss
	    #HRegwithFSR = ROOT.TLorentzVector()
	    #HRegwithFSR.SetPtEtaPhiM(tree.HCSV_reg_pt, tree.HCSV_reg_eta, tree.HCSV_reg_phi, tree.HCSV_reg_mass)
	    #HRegwithFSR = addAdditionalJets(HRegwithFSR, tree)
	    #HCSV_reg_mass_FSR[0] = HRegwithFSR.M()
	    #HCSV_reg_pt_FSR[0]   = HRegwithFSR.Pt()
	    
	    # New Funtion
	    #HCSV_reg_mass_met[0] = projMetOntoH(tree, True, False)
	    #HCSV_reg_mass_met_FSR[0] = projMetOntoH(tree, True, True)
	    #HCSV_reg_mass_met_FSR_wSemiL[0] = projMetOntoH(tree, False, True)

	    # Add the higgs regression resolution
	    #HReg_resolution[0] = (tree.HCSV_mass - tree.HCSV_reg_mass)/tree.HCSV_mass 

	    # Add the higgs correction bias
	    #IsSemiLepton = False
	    #if (tree.Jet_leptonPt[tree.hJCidx[0]] > 0) or (tree.Jet_leptonPt[tree.hJCidx[1]] > 0): IsSemiLepton = True
	    #Hreg_semiL_bias[0] = higgs_semiL_bias(tree.HCSV_reg_pt, tree.HCSV_reg_eta, IsSemiLepton)
	     
	    '''
            if applyRegression:

		#if tree.nJet < 2: continue    
		#if tree.hJidx < 2: continue
		    
                #HNoReg_HiggsFlag = 1
                HCSVNoReg_mass = (hJ0+hJ1).M()
                HCSVNoReg_pt = (hJ0+hJ1).Pt()
                HCSVNoReg_eta = (hJ0+hJ1).Eta()
                HCSVNoReg_phi = (hJ0+hJ1).Phi()
                HCSVNoReg_dR = hJ0.DeltaR(hJ1)
                HCSVNoReg_dPhi = hJ0.DeltaPhi(hJ1)
                HCSVNoReg_dEta = abs(hJ0.Eta()-hJ1.Eta())
                hJet_MtArray[0][0] = hJ0.Mt()
                hJet_MtArray[1][0] = hJ1.Mt()
                hJet_EtArray[0][0] = hJ0.Et()
                hJet_EtArray[1][0] = hJ1.Et()

				
                rPt0 = max(0.0001,readerJet0.EvaluateRegression( "jet0Regression" )[0])
                rPt1 = max(0.0001,readerJet1.EvaluateRegression( "jet1Regression" )[0])
		
		hJet_pt_reg[0] = rPt0
		hJet_pt_reg[1] = rPt1
		
                hJet_regWeight[0] = rPt0/Jet_pt_0
                hJet_regWeight[1] = rPt1/Jet_pt_1
		
		rM0 = Jet_m_0*hJet_regWeight[0]
		rM1 = Jet_m_1*hJet_regWeight[1]
		
                #rE0 = hJet_e0*hJet_regWeight[0]
                #rE1 = hJet_e1*hJet_regWeight[1]
		
                hJ0_reg.SetPtEtaPhiM(rPt0, Jet_eta_0, Jet_phi_0, Jet_m_0)
                hJ1_reg.SetPtEtaPhiM(rPt1, Jet_eta_1, Jet_phi_1, Jet_m_1)
		
		#hJ0.SetPtEtaPhiM(rPt0,hJet_eta0,hJet_phi0, 0.)
		#hJ1.SetPtEtaPhiM(rPt1,hJet_eta1,hJet_phi1, 0.)
		
		#Jet_mass_reg[0] = rM0
		#Jet_mass_reg[1] = rM1
		
		#print 'Hmass    :', HCSVNoReg_mass
		#print 'Hmass Reg:', (hJ0+hJ1).M()

		#HCSV_reg_mass[0] = (hJ0_reg + hJ1_reg).M()
                #HCSV_reg_pt[0]  = (hJ0_reg + hJ1_reg).Pt()
		HCSV_reg_mass[0] = (hJ0_reg + hJ1_reg).M()
                HCSV_reg_pt[0]  = (hJ0_reg + hJ1_reg).Pt()

                #HCSV_reg_eta = (hJ0+hJ1).Eta()
                #HCSV_reg_phi = (hJ0+hJ1).Phi()
                #HCSV_reg_mass = (hJ0+hJ1).M()
		#HCSV_reg_pt = (hJ0+hJ1).Pt()
		#HCSV_reg_dR = hJ0.DeltaR(hJ1)
                #HCSV_reg_dPhi = hJ0.DeltaPhi(hJ1)
                #HCSV_reg_dEta = abs(hJ0.Eta()-hJ1.Eta())
                #HVMass_Reg[0] = (hJ0+hJ1+vect).M()
		
		#HVdphi_reg[0] = abs(H_phi - tree.V_phi)
		
	    # end if regression	


	    for i in range(2):
		    flavour = int(tree.Jet_hadronFlavour[tree.hJCidx[i]])
		    pt = float(tree.Jet_pt[tree.hJCidx[i]])
		    eta = float(tree.Jet_eta[tree.hJCidx[i]])
		    csv = float(tree.Jet_btagCSV[tree.hJCidx[i]])
		    hJet_btagCSVOld[i] = csv
		    ##FIXME## we have to add the CSV reshaping
		    hJet_btagCSV[i] = csv
		    if anaTag == '7TeV':
			    tree.Jet_btagCSV[tree.hJCidx[i]] = corrCSV(btagNom,csv,flavour)
			    hJet_btagCSVDown[i] = corrCSV(btagDown,csv,flavour)
			    hJet_btagCSVUp[i] = corrCSV(btagUp,csv,flavour)
			    hJet_btagCSVFDown[i] = corrCSV(btagFDown,csv,flavour)
			    hJet_btagCSVFUp[i] = corrCSV(btagFUp,csv,flavour)
		    else:
			    # tree.Jet_btagCSV[i] = btagNom.reshape(eta,pt,csv,flavour)
			    # hJet_btagCSVDown[i] = btagDown.reshape(eta,pt,csv,flavour)
			    # hJet_btagCSVUp[i] = btagUp.reshape(eta,pt,csv,flavour)
			    # hJet_btagCSVFDown[i] = btagFDown.reshape(eta,pt,csv,flavour)
			    # hJet_btagCSVFUp[i] = btagFUp.reshape(eta,pt,csv,flavour)
			    # tree.Jet_btagCSV[i] = tree.Jet_btagCSV[i]
			    hJet_btagCSVDown[i] = tree.Jet_btagCSV[tree.hJCidx[i]]
			    hJet_btagCSVUp[i] = tree.Jet_btagCSV[tree.hJCidx[i]]
			    hJet_btagCSVFDown[i] = tree.Jet_btagCSV[tree.hJCidx[i]]
			    hJet_btagCSVFUp[i] = tree.Jet_btagCSV[tree.hJCidx[i]]
	    '''	

			    
	    if job.type != 'DATA':

		    '''
		    hJet_high[0], hJet_high[1] = 0,0
		    hJet_low[0],hJet_low[0]  = 0,0
		    hJet_central[0],hJet_central[0]  = 0,0
		    hJet_forward[0],hJet_forward[0]  = 0,0
		    
		    # hJet flags
		    if tree.Jet_pt_reg[tree.hJCidx[0]] > 100.: hJet_high[0] == 1
		    if tree.Jet_pt_reg[tree.hJCidx[1]] > 100.: hJet_high[1] == 1

		    if tree.Jet_pt_reg[tree.hJCidx[0]] < 100.: hJet_low[0] == 1
                    if tree.Jet_pt_reg[tree.hJCidx[1]] < 100.: hJet_low[1] == 1

		    if tree.Jet_eta[tree.hJCidx[0]] > 1.4: hJet_forward[0] == 1
                    if tree.Jet_eta[tree.hJCidx[1]] > 1.4: hJet_forward[1] == 1
		    
		    if tree.Jet_eta[tree.hJCidx[0]] < 1.4: hJet_central[0] == 1
                    if tree.Jet_eta[tree.hJCidx[1]] < 1.4: hJet_central[1] == 1
		    
		    ####################
                    #Dijet mass
                    ####################

                    #Initialize two higgs jet

		    def fillvar():
                        for SysDic in SysDicList:
                            if not eval(ConditionDic[SysDic['cat']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('CAT',SysDic['cat'])):
                                if SysDic['var'] == 'Jet_pt_reg_corrSYSUD_CAT':
                                    #print 'yeah man2'
                                    SysDic['varptr'][0] =  eval(DefaultVar[SysDic['var']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('INDEX','0'))
                                    SysDic['varptr'][1] =  eval(DefaultVar[SysDic['var']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('INDEX','1'))
                                else:
                                    SysDic['varptr'][0] =  eval(DefaultVar[SysDic['var']])
                            else:
                                if SysDic['var'] == 'Jet_pt_reg_corrSYSUD_CAT':
                                    booljet1 = eval(JetConditionDic[SysDic['cat']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('INDEX','0'))
                                    booljet2 = eval(JetConditionDic[SysDic['cat']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('INDEX','1'))
                                    if booljet1 and not booljet2:
                                        SysDic['varptr'][0] =  eval(SYSVar[SysDic['var']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('INDEX','0'))
                                        SysDic['varptr'][1] =  eval(DefaultVar[SysDic['var']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('INDEX','1'))
                                    elif not booljet1 and booljet2:
                                        SysDic['varptr'][0] =  eval(DefaultVar[SysDic['var']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('INDEX','0'))
                                        SysDic['varptr'][1] =  eval(SYSVar[SysDic['var']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('INDEX','1'))
                                    elif booljet1 and booljet1:
                                        SysDic['varptr'][0] =  eval(SYSVar[SysDic['var']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('INDEX','0'))
                                        SysDic['varptr'][1] =  eval(SYSVar[SysDic['var']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('INDEX','1'))
                                    else:
                                        print '@ERROR: jet category could not be indentified. Aborting'
                                else:
                                    Jet1 = ROOT.TLorentzVector()
                                    Jet2 = ROOT.TLorentzVector()
                                    Jet1_sys = ROOT.TLorentzVector()
                                    Jet2_sys = ROOT.TLorentzVector()
                                    Jet1.SetPtEtaPhiM(tree.Jet_pt_reg[tree.hJCidx[0]],tree.Jet_eta[tree.hJCidx[0]],tree.Jet_phi[tree.hJCidx[0]],tree.Jet_mass[tree.hJCidx[0]])
                                    Jet2.SetPtEtaPhiM(tree.Jet_pt_reg[tree.hJCidx[1]],tree.Jet_eta[tree.hJCidx[1]],tree.Jet_phi[tree.hJCidx[1]],tree.Jet_mass[tree.hJCidx[1]])

				    booljet1 = eval(JetConditionDic[SysDic['cat']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('INDEX','0'))
				    booljet2 = eval(JetConditionDic[SysDic['cat']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('INDEX','1'))
				     
                                    if booljet1 and not booljet2:
                                        eval('Jet1_sys.SetPtEtaPhiM(tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[0]],tree.Jet_eta[tree.hJCidx[0]],tree.Jet_phi[tree.hJCidx[0]],tree.Jet_mass[tree.hJCidx[0]])'.replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']))
                                        Jet2_sys = Jet2
                                    elif not booljet1 and booljet2:
                                        eval('Jet2_sys.SetPtEtaPhiM(tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[1]],tree.Jet_eta[tree.hJCidx[1]],tree.Jet_phi[tree.hJCidx[1]],tree.Jet_mass[tree.hJCidx[1]])'.replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']))
                                        Jet1_sys = Jet1
                                    elif booljet1 and booljet1:
                                        eval('Jet1_sys.SetPtEtaPhiM(tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[0]],tree.Jet_eta[tree.hJCidx[0]],tree.Jet_phi[tree.hJCidx[0]],tree.Jet_mass[tree.hJCidx[0]])'.replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']))
                                        eval('Jet2_sys.SetPtEtaPhiM(tree.Jet_pt_reg_corrSYSUD[tree.hJCidx[1]],tree.Jet_eta[tree.hJCidx[1]],tree.Jet_phi[tree.hJCidx[1]],tree.Jet_mass[tree.hJCidx[1]])'.replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']))
                                    else:
                                        print '@ERROR: jet category could not be indentified. Aborting'
                                        print 'cat is', SysDic['cat']
                                        print 'condition is', ConditionDic[SysDic['cat']].replace('SYS',SysDic['sys']).replace('UD',SysDic['UD']).replace('CAT',SysDic['cat'])
                                        print 'jet cond is', JetConditionDic[SysDic['cat']].replace('INDEX','1')
                                        sys.exit()

                                    HJet = Jet1+Jet2
                                    HJet_sys = Jet1_sys+Jet2_sys
                                    SysDic['varptr'][0] = eval(SYSVar[SysDic['var']])

                    fillvar()
                    '''    


		    # ================ Lepton Scale Factors =================
		    # For custom made form own JSON files

		    eTrigSFWeight[0]    = 1
		    eId80SFWeight[0]    = 1

		    eId90SFWeight[0]    = 1
		    eId90SFWeightUp[0]    = 1
		    eId90SFWeightDown[0]    = 1

		    eId90SFWeight_BCDEF[0] = 1

		    eTrackerSFWeight[0] = 1
		    eTrackerSFWeightUp[0] = 1
		    eTrackerSFWeightDown[0] = 1

		    eTrigSFWeight_ele27[0] = 1
		    #eTrigSFWeight_ele27Up[0] = 1
		    #eTrigSFWeight_ele27Down[0] = 1
		    
		    eTrigSFWeight_ele27_BCDEF[0] = 1
		    
		    eTrigSFWeight_doubleEle76x[0] = 1
		    eTrigSFWeight_doubleEle76xUp[0] = 1
		    eTrigSFWeight_doubleEle76xDown[0] = 1

		    mIdSFWeight[0]      = 1
		    mIdSFWeightUp[0]      = 1
		    mIdSFWeightDown[0]      = 1

		    mTrackerSFWeight[0] = 1
		    mTrackerSFWeightUp[0] = 1
		    mTrackerSFWeightDown[0] = 1
		    
		    mTrigSFWeight[0]    = 1
		    mTrigSFWeightUp[0]    = 1
		    mTrigSFWeightDown[0]    = 1
		    
		    mIsoSFWeight[0] = 1
		    mIsoSFWeightUp[0] = 1
		    mIsoSFWeightDown[0] = 1
		    
		    mTrigSFWeight_ICHEP[0] = 1

		    mTrigSFWeight_doubleMu76x[0] = 1
		    mTrigSFWeight_doubleMu76xUp[0] = 1
		    mTrigSFWeight_doubleMu76xDown[0] = 1

		    muTrigEffBfr1 = 1
		    muTrigEffBfr2 = 1
		    
		    muTrigEffAftr1 = 1
		    muTrigEffAftr2 = 1
		    
		    jsons = {
			    'myutils/jsons/SingleMuonTrigger_LooseMuons_afterL2fix_Z_RunBCD_prompt80X_7p65.json' : ['MuonTrigger_data_all_IsoMu22_OR_IsoTkMu22_pteta_Run2016B_afterL2Fix', 'abseta_pt_MC'],
			    'myutils/jsons/SingleMuonTrigger_LooseMuons_beforeL2fix_Z_RunBCD_prompt80X_7p65.json' : ['MuonTrigger_data_all_IsoMu22_OR_IsoTkMu22_pteta_Run2016B_beforeL2Fix', 'abseta_pt_MC'],
			    'myutils/jsons/EfficienciesAndSF_ISO.json' : ['MC_NUM_LooseRelIso_DEN_LooseID_PAR_pt_spliteta_bin1', 'abseta_pt_ratio'],
			    #'myutils/jsons/WP90PlusIso_BCD.json' : ['WP90PlusIso_BCD', 'eta_pt_ratio'],
			    #'myutils/jsons/WP90PlusIso_BCDEF.json' : ['WP90PlusIso_BCDEF', 'eta_pt_ratio'],
			    #'myutils/jsons/WP90_BCD_withRelIso.json': ['electronTriggerEfficiencyHLT_Ele27_WPLoose_eta2p1_WP90_BCD', 'eta_pt_ratio'],
			    #'myutils/jsons/WP90_BCDEF_withRelIso.json' : ['electronTriggerEfficiencyHLT_Ele27_WPLoose_eta2p1_WP90_BCDEF', 'eta_pt_ratio'],
			    #'myutils/jsons/HLT_Ele23_WPLoose.json' : ['HLT_Ele23_WPLoose', 'eta_pt_ratio'],
			    
			    # 80x in v25
			    '../myMacros/scale_factors/80x/ScaleFactor_etracker_80x.json' : ['ScaleFactor_etracker_80x', 'eta_pt_ratio'],
			    '../myMacros/scale_factors/80x/ScaleFactor_eMVAID_80x.json' : ['ScaleFactor_eMVAID_80x', 'eta_pt_ratio'],
			    '../myMacros/scale_factors/ScaleFactor_doubleElectron76x.json' : ['ScaleFactor_doubleElectron76x', 'eta_pt_ratio'],
			    '../myMacros/scale_factors/ScaleFactor_doubleMuon76x.json' : ['ScaleFactor_doubleMuon76x', 'eta_pt_ratio']
			    }

		    for j, name in jsons.iteritems():
			    
			    #print '\n New Json Iteration...'
			    #print j
			    #print name[0], name[1]
			    			    
			    weight = []
			    lepCorr = LeptonSF(j , name[0], name[1])
			    
			    if '_double' in j:
				    weight.append(lepCorr.get_2D( abs(tree.vLeptons_eta[1]), abs(tree.vLeptons_eta[0])))
			    else:	    
				    weight.append(lepCorr.get_2D( tree.vLeptons_pt[0], tree.vLeptons_eta[0]))
				    weight.append(lepCorr.get_2D( tree.vLeptons_pt[1], tree.vLeptons_eta[1]))

			    if tree.Vtype == 0:

				    if j.find('SingleMuonTrigger_LooseMuons_beforeL2fix_Z_RunBCD_prompt80X_7p65') != -1:
					    muTrigEffBfr1 = weight[0][0]
					    muTrigEffBfr2 = weight[1][0]
					    muEffUpBfr1   = (weight[0][0]+weight[0][1])
                                            muEffUpBfr2   = (weight[1][0]+weight[1][1])
                                            muEffDownBfr1 = (weight[0][0]-weight[0][1])
                                            muEffDownBfr2 = (weight[1][0]-weight[1][1])
				
				    elif j.find('ScaleFactor_doubleMuon76x') != -1:
					    mTrigSFWeight_doubleMu76x[0] = weight[0][0]
                                            mTrigSFWeight_doubleMu76xUp[0] = weight[0][0] + weight[0][1] 
                                            mTrigSFWeight_doubleMu76xDown[0] = weight[0][0] - weight[0][1]
					    
				    elif j.find('SingleMuonTrigger_LooseMuons_afterL2fix_Z_RunBCD_prompt80X_7p65') != -1:
					    muTrigEffAftr1 = weight[0][0]
					    muTrigEffAftr2 = weight[1][0]
					    
					    muEffUpAftr1   = (weight[0][0]+weight[0][1])
                                            muEffUpAftr2   = (weight[1][0]+weight[1][1])
                                            muEffDownAftr1 = (weight[0][0]-weight[0][1])
                                            muEffDownAftr2 = (weight[1][0]-weight[1][1])
					    

				    elif j.find('MuonID') != -1:
					    mIdSFWeight[0]     = weight[0][0]*weight[1][0]
					    mIdSFWeightUp[0]   = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
                                            mIdSFWeightDown[0] = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
    
				    elif j.find('EfficienciesAndSF_ISO') != -1:
					    mIsoSFWeight[0]     = weight[0][0]*weight[1][0]
					    mIsoSFWeightUp[0]   = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
                                            mIsoSFWeightDown[0] = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    

			    elif tree.Vtype == 1:
				    				    
				    	    
				    if j.find('ScaleFactor_eMVAID_80x') != -1:
					    eId90SFWeight[0] = weight[0][0]*weight[1][0]
					    eId90SFWeightUp[0] = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
					    eId90SFWeightDown[0] = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    
				    elif j.find('ScaleFactor_doubleElectron76x') != -1:
                                            eTrigSFWeight_doubleEle76x[0] = weight[0][0]
                                            eTrigSFWeight_doubleEle76xUp[0] = weight[0][0] + weight[0][1]
                                            eTrigSFWeight_doubleEle76xDown[0] = weight[0][0] - weight[0][1]

				    elif j.find('ScaleFactor_etracker_80x') != -1:
					    eTrackerSFWeight[0] = weight[0][0]*weight[1][0]
					    eTrackerSFWeightUp[0]   = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
                                            eTrackerSFWeightDown[0] = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])

                    # End JSON loop ====================================

		    if tree.Vtype == 0:
			    
			    #for ICHEP dataset
			    eff1 = 0.04854*muTrigEffBfr1 + 0.95145*muTrigEffAftr1
			    eff2 = 0.04854*muTrigEffBfr2 + 0.95145*muTrigEffAftr2
			    mTrigSFWeight_ICHEP[0] = eff1*(1-eff2)*eff1 + eff2*(1-eff1)*eff2 + eff1*eff1*eff2*eff2
			    
			    eff1Up = 0.04854*muEffUpBfr1 +  0.95145*muEffUpAftr1
			    eff2Up = 0.04854*muEffUpBfr2 +  0.95145*muEffUpAftr2
			    mTrigSFWeightUp[0] = eff1Up*(1-eff2Up)*eff1Up + eff2Up*(1-eff1Up)*eff2Up + eff1Up*eff1Up*eff2Up*eff2Up
			    
			    eff1Down = 0.04854*muEffDownBfr1 +  0.95145*muEffDownAftr1
			    eff2Down = 0.04854*muEffDownBfr2 +  0.95145*muEffDownAftr2
                            mTrigSFWeightDown[0] = eff1Down*(1-eff2Down)*eff1Down + eff2Down*(1-eff1Down)*eff2Down + eff1Down*eff1Down*eff2Down*eff2Down
			    
			    # for 22/fb
			    eff1 = 0.02772*muTrigEffBfr1 + 0.97227*muTrigEffAftr1
			    eff2 = 0.02772*muTrigEffBfr2 + 0.97227*muTrigEffAftr2
			    mTrigSFWeight[0] = eff1*(1-eff2)*eff1 + eff2*(1-eff1)*eff2 + eff1*eff1*eff2*eff2
					    

		    			    
		    '''
		    # Now assign the lepton event weight based on vType
		    pTcut = 22;

                    DR = [999, 999]
                    debug = False
		    
                    # dR matching
                    for k in range(0,2):
                        for l in range(0,len(tree.trgObjects_hltIsoMu18_eta)):
                            dr_ = deltaR(tree.vLeptons_eta[k], tree.vLeptons_phi[k], tree.trgObjects_hltIsoMu18_eta[l], tree.trgObjects_hltIsoMu18_phi[l])
                            if dr_ < DR[k] and tree.vLeptons_pt[k] > 22:
                                DR[k] = dr_

                    Mu1pass = DR[0] < 0.5
                    Mu2pass = DR[1] < 0.5
		    
                    SF1 = tree.vLeptons_SF_HLT_RunD4p2[0]*0.1801911165 + tree.vLeptons_SF_HLT_RunD4p3[0]*0.8198088835
                    SF2 = tree.vLeptons_SF_HLT_RunD4p2[1]*0.1801911165 + tree.vLeptons_SF_HLT_RunD4p3[1]*0.8198088835
                    eff1 = tree.vLeptons_Eff_HLT_RunD4p2[0]*0.1801911165 + tree.vLeptons_Eff_HLT_RunD4p3[0]*0.8198088835
                    eff2 = tree.vLeptons_Eff_HLT_RunD4p2[1]*0.1801911165 + tree.vLeptons_Eff_HLT_RunD4p3[1]*0.8198088835

                    #print 'vLeptSFw is', vLeptons_SFweight_HLT[0]
                    #print 'Vtype is', tree.Vtype
		    
                    if tree.Vtype == 1:
			    vLeptons_SFweight_HLT[0] = eTrigSFWeight*eIDTightSFWeight
                    elif tree.Vtype == 0:
			vLeptons_SFweight_HLT[0] = 1    
                        if not Mu1pass and not Mu2pass:
                            vLeptons_SFweight_HLT[0] = 0
                        elif Mu1pass and not Mu2pass:
                            vLeptons_SFweight_HLT[0] = SF1
                        elif not Mu1pass and Mu2pass:
                            vLeptons_SFweight_HLT[0] = SF2
                        elif Mu1pass and Mu2pass:
                            effdata = 1 - (1-SF1*eff1)*(1-SF2*eff2);
                            effmc = 1 - (1-eff1)*(1-eff2);
                            vLeptons_SFweight_HLT[0] = effdata/effmc
		    '''	    
                		
	    # end if not Data
	    newtree.Fill()
	    # end event loop	



		

    print count	    
    print 'Exit loop'
    newtree.AutoSave()
    print 'Save'
    output.Close()
    print 'Close'
    
    #t3 specific
    # targetStorage = pathOUT.replace('gsidcap://t3se01.psi.ch:22128/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')+'/'+job.prefix+job.identifier+'.root'
    #command = 'lcg-del -b -D srmv2 -l %s' %(targetStorage)
    #print(command)
    #subprocess.call([command], shell=True)
    # command = 'lcg-cp -b -D srmv2 file:///%s %s' %(tmpDir+'/'+job.prefix+job.identifier+'.root',targetStorage)
    #print(command)
    #subprocess.call([command], shell=True)
