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
    
    #regWeight = config.get("TrainRegression","regWeight")
    #regDict = eval(config.get("TrainRegression","regDict"))
    #regVars = eval(config.get("TrainRegression","regVars"))

    
    # hJ0 = ROOT.TLorentzVector()
    # hJ1 = ROOT.TLorentzVector()
    # hJ2 = ROOT.TLorentzVector()
    # vect = ROOT.TLorentzVector()

    # hJ0_reg = ROOT.TLorentzVector()
    # hJ1_reg = ROOT.TLorentzVector()

    # # for adding 3rd jet
    # hJ0_noReg = ROOT.TLorentzVector()
    # hJ1_noReg = ROOT.TLorentzVector()
    
    
    # #regWeightFilterJets = config.get("Regression","regWeightFilterJets")
    # #regDictFilterJets = eval(config.get("Regression","regDictFilterJets"))
    # #regVarsFilterJets = eval(config.get("Regression","regVarsFilterJets"))

    # # Standard Branches
    # HCSV_dR_reg   = array('f',[0]*1)
    # HCSV_dEta_reg = array('f',[0]*1)
    # HCSV_dPhi_reg = array('f',[0]*1)

    # newtree.Branch('HCSV_dR_reg', HCSV_dR_reg, 'HCSV_dR_reg[1]/F')
    # newtree.Branch('HCSV_dEta_reg', HCSV_dEta_reg, 'HCSV_dEta_reg[1]/F')
    # newtree.Branch('HCSV_dPhi_reg', HCSV_dEta_reg, 'HCSV_dPhi_reg[1]/F')
    
    # HVdPhi_reg = array('f',[0]*1)
    # newtree.Branch('HVdPhi_reg', HVdPhi_reg, 'HVdPhi_reg[1]/F')

    # HCSV_reg_pt_FSR = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_pt_FSR', HCSV_reg_pt_FSR, 'HCSV_reg_pt_FSR[1]/F')

    # # Higgs masses
    
    # HCSV_reg_mass_FSR = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_mass_FSR', HCSV_reg_mass_FSR, 'HCSV_reg_mass_FSR[1]/F')

    # HCSV_reg_mass_FSR2 = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_mass_FSR2', HCSV_reg_mass_FSR2, 'HCSV_reg_mass_FSR2[1]/F')

    # HCSV_reg_mass_met_FSR = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_mass_met_FSR', HCSV_reg_mass_met_FSR, 'HCSV_reg_mass_met_FSR[1]/F')

    # HCSV_reg_mass_met = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_mass_met', HCSV_reg_mass_met, 'HCSV_reg_mass_met[1]/F')

    # # Optional semiLepton decay only
    # HCSV_reg_mass_met_FSR_wSemiL = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_mass_met_FSR_wSemiL', HCSV_reg_mass_met_FSR_wSemiL, 'HCSV_reg_mass_met_FSR_wSemiL[1]/F')

    # HCSV_reg_pt_FSR_wSemiL = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_pt_FSR_wSemiL', HCSV_reg_pt_FSR_wSemiL, 'HCSV_reg_pt_FSR_wSemiL[1]/F')

    # HCSV_reg_pt_FSR = array('f',[0]*1)
    # newtree.Branch('HCSV_reg_pt_FSR', HCSV_reg_pt_FSR, 'HCSV_reg_pt_FSR[1]/F')
    
    # Jet_mt = array('f',[0]*2)
    # newtree.Branch('Jet_mt', Jet_mt, 'Jet_mt[2]/F')

    # # For higgs regression resolution
    # HReg_resolution = array('f',[0]*1)
    # newtree.Branch('HReg_resolution', HReg_resolution, 'HReg_resolution[1]/F')

    # # For Higgs semiLepton bias in pt/eta bins
    # Hreg_semiL_bias = array('f',[0]*1)
    # newtree.Branch('Hreg_semiL_bias', Hreg_semiL_bias, 'Hreg_semiL_bias[1]/F')

    
    
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

    # # New for trigger string short cut
    # zee_trigger = zee_trigger = array('f',[0]*1)
    # newtree.Branch('zee_trigger',zee_trigger,'zee_trigger/F')
    
    # zuu_trigger = array('f',[0]*1)
    # newtree.Branch('zuu_trigger',zuu_trigger,'zuu_trigger/F')

    # # For DY special Weights
    DY_specialWeight = array('f',[0]*1)
    newtree.Branch('DY_specialWeight',DY_specialWeight,'DY_specialWeight/F')

    # # For LO/NLO Weighting
    NLO_Weight = array('f',[0]*1)
    newtree.Branch('NLO_Weight',NLO_Weight,'NLO_Weight/F')
    
    # for EWK reweighting
    DY_ewkWeight = array('f',[0]*1)
    newtree.Branch('DY_ewkWeight',DY_ewkWeight,'DY_ewkWeight/F')

    if 'DY' in job.name:
	    nloweight = ROOT.TTreeFormula('nloweight', "VHbb::LOtoNLOWeightBjetSplitEtabb(abs(Jet_eta[hJCidx[0]]-Jet_eta[hJCidx[1]]),Sum$(GenJet_pt>20 && abs(GenJet_eta)<2.4&&GenJet_numBHadrons))", tree)

	    specialWeight = ROOT.TTreeFormula('specialWeight',job.specialweight, tree)

	    DY_ewkWeight ROOT.TTreeFormula('ewkWeight', 'VHbb::ptWeightEWK_Zll(nGenVbosons[0], GenVbosons_pt[0], VtypeSim, nGenTop, nGenHiggsBoson)')
	    

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

    #########################################################################################

    
    print '\n\n======== Filling New Branches/ Applying Regression ========'
        
    for entry in range(0,nEntries):

	    # for testing
	    #if entry > 10000: break
	    	    
            tree.GetEntry(entry)

	    if entry % 10000 is 0: print 'Event #', entry
	    
            #if tree.nJet < 2: continue
	    #if tree.nhJCidx == 0 : continue
	    
	    # Set the special Weight
	    # Init the weight string
	    if 'DY' not in job.name: 
	    	    DY_specialWeight[0] = 1
	    	    NLO_Weight[0] = 1		    
		    DY_ewkWeight[0] = 1
	    else:
	    	    specialWeight_ = specialWeight.EvalInstance()
	    	    DY_specialWeight[0] = specialWeight_
		    
	    	    nlo_weight_ = nlo_weight.EvalInstance()
	    	    NLO_Weight[0] = nlo_weight_ 
		    
		    ewkWeight_ = ewkWeight.EvalInstance()
		    DY_ewkWeight[0] = ewkWeight_
		    
	    
	    # if tree.Vtype_new == 0 and (tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v==1 or tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v==1 or tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v==1 or tree.HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v==1):  
	    # 	    zuu_trigger[0] = 1
	    # else:
	    # 	    zuu_trigger[0] = 0


	    # if tree.Vtype_new == 1 and tree.HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v == 1:
	    # 	    zee_trigger[0] = 1
            # else:
            #         zee_trigger[0] = 0


			    
	    if job.type != 'DATA':

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


		    muISO_BCDEF = 1
		    muISO_GH = 1
		    
		    muID_BCDEF= 1
		    muID_GH = 1
		    

		    jsons = {
			    #### Muon trigger ISO, and ID ####
			    
			    # ID
			    'myutils/jsons/80x/muon_ID_BCDEF.json' : ['MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta', 'pt_abseta_ratio'],
			    'myutils/jsons/80x/muon_ID_GH.json'    : ['MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta', 'pt_abseta_ratio'],
			    
			    # ISO
			    'myutils/jsons/80x/muon_ISO_BCDEF.json' : ['LooseISO_LooseID_pt_eta', 'pt_abseta_ratio'],
			    'myutils/jsons/80x/muon_ISO_GH.json'    : ['LooseISO_LooseID_pt_eta', 'pt_abseta_ratio'],
			    
			    #### Electron trigger and ID ####
			    # 80x in v25
			    #'../myMacros/scale_factors/80x/ScaleFactor_etracker_80x.json' : ['ScaleFactor_tracker_80x', 'eta_pt_ratio'],
			    #'../myMacros/scale_factors/80x/ScaleFactor_eMVAID_80x.json' : ['ScaleFactor_MVAID_80x', 'eta_pt_ratio']
			    #'../myMacros/scale_factors/ScaleFactor_doubleElectron76x.json' : ['ScaleFactor_doubleElectron76x', 'eta_pt_ratio'],
			    #'../myMacros/scale_factors/ScaleFactor_doubleMuon76x.json' : ['ScaleFactor_doubleMuon76x', 'eta_pt_ratio']
			    }

		    for j, name in jsons.iteritems():
			    
			    # print '\n New Json Iteration...'
			    # print j
			    # print name[0], name[1]
			    			    
			    weight = []
			    lepCorr = LeptonSF(j, name[0], name[1])
			    
			    weight.append(lepCorr.get_2D( tree.vLeptons_new_pt[0], tree.vLeptons_new_eta[0]))
			    weight.append(lepCorr.get_2D( tree.vLeptons_new_pt[1], tree.vLeptons_new_eta[1]))
				    
			    if tree.Vtype_new == 0:
				    
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
					    
					    
				    elif j.find('muon_ID_BCDEF') != -1:
					    muID_BCDEF = weight[0][0]*weight[1][0]  
					    mIDSFWeightUp_BCDEF   = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
					    mIDSFWeightDown_BCDEF = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    #print muID_BCDEF

				    elif j.find('muon_ID_GH') != -1:
					    muID_GH = weight[0][0]*weight[1][0]
					    mIDSFWeightUp_GH  = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
					    mIDSFWeightDown_GH = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    #print muID_GH

				    elif j.find('muon_ISO_BCDEF') != -1:
					    muISO_BCDEF = weight[0][0]*weight[1][0]
					    mISOSFWeightUp_BCDEF   = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
					    mISOSFWeightDown_BCDEF = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    #print muISO_BCDEF

				    elif j.find('muon_ISO_GH') != -1:
					    muISO_GH = weight[0][0]*weight[1][0]
					    mISOSFWeightUp_GH   = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
					    mISOSFWeightDown_GH = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    #print muISO_GH

			    elif tree.Vtype_new == 1:
				    				    	    
				    if j.find('ScaleFactor_eMVAID_80x') != -1:
					    eId90SFWeight[0] = weight[0][0]*weight[1][0]
					    eId90SFWeightUp[0] = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
					    eId90SFWeightDown[0] = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])
					    
				    elif j.find('WP90_BCD_withRelIso.json') != -1:
					    eff1 = weight[0][0]
					    eff2 = weight[1][0]
					    eff1Up = (weight[0][0]+weight[0][1])
					    eff2Up = (weight[1][0]+weight[1][1])
					    eff1Down = (weight[0][0]-weight[0][1])
                                            eff2Down = (weight[1][0]-weight[1][1])
					    eTrigSFWeight_ele27[0]     = eff1*(1-eff2)*eff1 + eff2*(1-eff1)*eff2 + eff1*eff1*eff2*eff2
					    eTrigSFWeight_ele27Up[0]   = eff1Up*(1-eff2Up)*eff1Up + eff2Up*(1-eff1Up)*eff2Up + eff1Up*eff1Up*eff2Up*eff2Up 
					    eTrigSFWeight_ele27Down[0] = eff1Down*(1-eff2Down)*eff1Down + eff2Down*(1-eff1Down)*eff2Down + eff1Down*eff1Down*eff2Down*eff2Down
					    
					    
				    elif j.find('ScaleFactor_doubleElectron76x') != -1:
                                            eTrigSFWeight_doubleEle76x[0] = weight[0][0]
                                            eTrigSFWeight_doubleEle76xUp[0] = weight[0][0] + weight[0][1]
                                            eTrigSFWeight_doubleEle76xDown[0] = weight[0][0] - weight[0][1]

				    elif j.find('ScaleFactor_etracker_80x') != -1:
					    eTrackerSFWeight[0] = weight[0][0]*weight[1][0]
					    eTrackerSFWeightUp[0]   = (weight[0][0]+weight[0][1])*(weight[1][0]+weight[1][1])
                                            eTrackerSFWeightDown[0] = (weight[0][0]-weight[0][1])*(weight[1][0]-weight[1][1])

                    # End JSON loop ====================================

		    if tree.Vtype_new == 0:
			    
			    #for ICHEP dataset
			    #eff1 = 0.04854*muTrigEffBfr1 + 0.95145*muTrigEffAftr1
			    #eff2 = 0.04854*muTrigEffBfr2 + 0.95145*muTrigEffAftr2
			    #mTrigSFWeight_ICHEP[0] = eff1*(1-eff2)*eff1 + eff2*(1-eff1)*eff2 + eff1*eff1*eff2*eff2
			    
			    #eff1Up = 0.04854*muEffUpBfr1 +  0.95145*muEffUpAftr1
			    #eff2Up = 0.04854*muEffUpBfr2 +  0.95145*muEffUpAftr2
			    #mTrigSFWeightUp[0] = eff1Up*(1-eff2Up)*eff1Up + eff2Up*(1-eff1Up)*eff2Up + eff1Up*eff1Up*eff2Up*eff2Up
			    
			    #eff1Down = 0.04854*muEffDownBfr1 +  0.95145*muEffDownAftr1
			    #eff2Down = 0.04854*muEffDownBfr2 +  0.95145*muEffDownAftr2
                            #mTrigSFWeightDown[0] = eff1Down*(1-eff2Down)*eff1Down + eff2Down*(1-eff1Down)*eff2Down + eff1Down*eff1Down*eff2Down*eff2Down
			    
			    # for 35.9/fb
			    #eff1 = 0.02772*muTrigEffBfr1 + 0.97227*muTrigEffAftr1
			    #eff2 = 0.02772*muTrigEffBfr2 + 0.97227*muTrigEffAftr2
			    #TrigSFWeight[0] = eff1*(1-eff2)*eff1 + eff2*(1-eff1)*eff2 + eff1*eff1*eff2*eff2
			    
			    mIdSFWeight[0] = muID_BCDEF*(20.1/36.4) + muID_GH*(16.3/36.4)
			    mIdSFWeightUp[0] = mIDSFWeightUp_BCDEF*(20.1/36.4) + mIDSFWeightUp_GH*(16.3/36.4)
			    mIdSFWeightDown[0] = mIDSFWeightDown_BCDEF*(20.1/36.4) + mIDSFWeightDown_GH*(16.3/36.4)
			    
			    mIsoSFWeight[0] = muISO_BCDEF*(20.1/36.4) + muISO_GH*(16.3/36.4)
                            mIsoSFWeightUp[0] = mISOSFWeightUp_BCDEF*(20.1/36.4) + mISOSFWeightUp_GH*(16.3/36.4)
                            mIsoSFWeightDown[0] = mISOSFWeightDown_BCDEF*(20.1/36.4) + mISOSFWeightDown_GH*(16.3/36.4)
 
		    '''
		    # Now assign the lepton event weight based on vType
		    pTcut = 22;

                    DR = [999, 999]
                    debug = False
		    
                    # dR matching
                    for k in range(0,2):
                        for l in range(0,len(tree.trgObjects_hltIsoMu18_eta)):
                            dr_ = deltaR(tree.vLeptons_new_eta[k], tree.vLeptons_new_phi[k], tree.trgObjects_hltIsoMu18_eta[l], tree.trgObjects_hltIsoMu18_phi[l])
                            if dr_ < DR[k] and tree.vLeptons_new_pt[k] > 22:
                                DR[k] = dr_

                    Mu1pass = DR[0] < 0.5
                    Mu2pass = DR[1] < 0.5
		    
                    SF1 = tree.vLeptons_new_SF_HLT_RunD4p2[0]*0.1801911165 + tree.vLeptons_new_SF_HLT_RunD4p3[0]*0.8198088835
                    SF2 = tree.vLeptons_new_SF_HLT_RunD4p2[1]*0.1801911165 + tree.vLeptons_new_SF_HLT_RunD4p3[1]*0.8198088835
                    eff1 = tree.vLeptons_new_Eff_HLT_RunD4p2[0]*0.1801911165 + tree.vLeptons_new_Eff_HLT_RunD4p3[0]*0.8198088835
                    eff2 = tree.vLeptons_new_Eff_HLT_RunD4p2[1]*0.1801911165 + tree.vLeptons_new_Eff_HLT_RunD4p3[1]*0.8198088835

                    #print 'vLeptSFw is', vLeptons_new_SFweight_HLT[0]
                    #print 'Vtype_new is', tree.Vtype_new
		    
                    if tree.Vtype_new == 1:
			    vLeptons_new_SFweight_HLT[0] = eTrigSFWeight*eIDTightSFWeight
                    elif tree.Vtype_new == 0:
			vLeptons_new_SFweight_HLT[0] = 1    
                        if not Mu1pass and not Mu2pass:
                            vLeptons_new_SFweight_HLT[0] = 0
                        elif Mu1pass and not Mu2pass:
                            vLeptons_new_SFweight_HLT[0] = SF1
                        elif not Mu1pass and Mu2pass:
                            vLeptons_new_SFweight_HLT[0] = SF2
                        elif Mu1pass and Mu2pass:
                            effdata = 1 - (1-SF1*eff1)*(1-SF2*eff2);
                            effmc = 1 - (1-eff1)*(1-eff2);
                            vLeptons_new_SFweight_HLT[0] = effdata/effmc
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
