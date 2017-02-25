#!/usr/bin/env python
#from samplesclass import sample
#from printcolor import printc
import pickle
import sys
import os
import ROOT 
import math
import shutil
from collections import Counter
from ROOT import TFile, TMath
from ROOT import TXNetFile
from array import array
import warnings
from optparse import OptionParser
from ROOT import *
import numpy as np

#from BetterConfigParser import BetterConfigParser
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='creating converter.*' )
argv = sys.argv

count = Counter()


def deltaPhi(phi1, phi2): 
    result = phi1 - phi2
    while (result > math.pi): result -= 2*math.pi
    while (result <= -math.pi): result += 2*math.pi
    return result


def projectionMETOntoJet(met, metphi, jet, jetphi, onlyPositive=True, threshold = math.pi/4.0):

  deltaphi = deltaPhi(metphi, jetphi)
  met_dot_jet = met * jet * math.cos(deltaphi)
  jetsq = jet * jet
  projection = met_dot_jet / jetsq * jet

  if onlyPositive and abs(deltaphi) >= threshold:
      return 0.0
  else:
      return projection



def resolutionBias(eta):    
    if(eta< 0.5): return 0.052
    if(eta< 1.1): return 0.057
    if(eta< 1.7): return 0.096
    if(eta< 2.3): return 0.134
    if(eta< 5): return 0.28
    return 0

def corrPt(pt,eta,mcPt):
    return (pt+resolutionBias(math.fabs(eta))*(pt-mcPt))/pt

def addAdditionalJets(H, tree):
    for i in range(tree.nhjidxaddJetsdR08):
        idx = tree.hjidxaddJetsdR08[i]
        if (idx == tree.hJCidx[0]) or (idx == tree.hJCidx[1]): continue
        addjet = ROOT.TLorentzVector()
        addjet.SetPtEtaPhiM(tree.Jet_pt[idx],tree.Jet_eta[idx],tree.Jet_phi[idx],tree.Jet_mass[idx])
        H = H + addjet
    return H

ROOT.gROOT.ProcessLine(
        "struct H {\
        int         HiggsFlag;\
        float         mass;\
	float 	      masswithFSR;\
        float         pt;\
        float         ptwithFSR;\
        float         eta;\
        float         phi;\
        float         dR;\
        float         dPhi;\
        float         dEta;\
        } ;"
    )


inpath = '/exports/uftrig01a/dcurry/heppy/files/prep_out/'
outpath = '/exports/uftrig01a/dcurry/heppy/files/jec_out/'

# List of files to add btag weights to
bkg_list = ['DY_inclusive', 'ttbar', 'ZZ_2L2Q', 'WZ']

data_list = ['Zuu', 'Zee']

signal_list = ['ZH125', 'ggZH125']

DY_list = ['DY_70to100','DY_100to200', 'DY_200to400', 'DY_400to600', 'DY_600to800', 'DY_800to1200', 'DY_1200to2500', 'DY_2500toInf', 'DY_Bjets', 'DY_BgenFilter',
              'DY_Pt50to100', 'DY_Pt100to250', 'DY_Pt250to400','DY_Pt400to650','DY_Pt650toInf'
              ]

DY_parton_list = ['DY0J', 'DY1J']

ST_list = ['ST_s', 'ST_tW_top', 'ST_tW_antitop', 'ST_t_antitop']

prep_list = ['prep_DY_2J', 'prep_DY_2J_NewExt1', 'prep_DY_2J_NewExt2', 'prep_DY_2J_NewExt3',
             'prep_DY_2J_NewExt4', 'prep_DY_2J_NewExt5', 'prep_DY_2J_NewExt6', 'prep_DY_2J_NewExt7', 'prep_DY_2J_NewExt8']

temp_list = ['DY_inclusive']

#file_list = bkg_list + data_list + signal_list + ST_list + DY_parton_list
file_list = temp_list



for file in file_list:

    input  = TFile.Open(inpath+'/v25_'+file+'.root', 'read')
    
    output = TFile.Open(outpath+'/v25_'+file+'.root', 'recreate')

    regWeight = 'ttbar-G25-500k-13d-300t.weights.xml'

    regVars = ["Jet_pt",
               "nPVs",
               "Jet_eta",
               "Jet_mt",
               "Jet_leadTrackPt",
               "Jet_leptonPtRel",
               "Jet_leptonPt",
               "Jet_leptonDeltaR",
               "Jet_neHEF",
               "Jet_neEmEF",
               "Jet_vtxPt",
               "Jet_vtxMass",
               "Jet_vtx3dL",
               "Jet_vtxNtrk",
               "Jet_vtx3deL",
               ]      	

    regDict = {"Jet_pt":"Jet_pt[hJCMVAV2idx[0]]",
               #"Jet_corr":"Jet_corr[hJCMVAV2idx[0]]"
               "nPVs":"nPVs",
               "Jet_eta":"Jet_eta[hJCMVAV2idx[0]]",
               "Jet_mt":"Jet_mt[hJCMVAV2idx[0]]",
               "Jet_leadTrackPt": "Jet_leadTrackPt[hJCMVAV2idx[0]]",
               "Jet_leptonPtRel":"Jet_leptonPtRel[hJCMVAV2idx[0]]",
               "Jet_leptonPt":"Jet_leptonPt[hJCMVAV2idx[0]]",
               "Jet_leptonDeltaR":"Jet_leptonDeltaR[hJCMVAV2idx[0]]",
               "Jet_neHEF":"Jet_neHEF[hJCMVAV2idx[0]]",
               "Jet_neEmEF":"Jet_neEmEF[hJCMVAV2idx[0]]",
               "Jet_vtxPt":"Jet_vtxPt[hJCMVAV2idx[0]]",
               "Jet_vtxMass":"Jet_vtxMass[hJCMVAV2idx[0]]",
               "Jet_vtx3dL":"Jet_vtx3dl[hJCMVAV2idx[0]]",
               "Jet_vtxNtrk":"Jet_vtxNtrk[hJCMVAV2idx[0]]",
               "Jet_vtx3deL":"Jet_vtx3deL[hJCMVAV2idx[0]]",
               #"met_pt":"met_pt[hJCMVAV2idx[0]]",
               #"Jet_met_proj":"Jet_met_proj[hJCMVAV2idx[0]]"
               } 

    
    JECsys = [ 
        "JER",
        "PileUpDataMC",
        "PileUpPtRef",
        #"PileUpPtBB",
        #"PileUpPtEC1",
        #"PileUpPtEC2",
        #"PileUpPtHF",
        
        # "RelativeJEREC1",
        # "RelativeJEREC2",
        # "RelativeJERHF",
        # "RelativeFSR",
        # "RelativeStatFSR",
        # "RelativeStatEC",
        # "RelativeStatHF",
        # "RelativePtBB",
        # "RelativePtEC1",
        # "RelativePtEC2",
        # "RelativePtHF",
        
        # "AbsoluteScale",
        # "AbsoluteMPFBias",
        # "AbsoluteStat",
        # "SinglePionECAL",
        # "SinglePionHCAL",
        # "Fragmentation",
        # "TimePtEta",
        # "FlavorQCD"
        ]
    
    print '----> Input : ', input
    print '----> Output: ', output
    
    input.cd()
    obj = ROOT.TObject
    for key in ROOT.gDirectory.GetListOfKeys():
        input.cd()
        obj = key.ReadObj()
        if obj.GetName() == 'tree':
            continue
        output.cd()
        obj.Write(key.GetName())

    input.cd()
    tree = input.Get('tree')
    nEntries = tree.GetEntries()



    # For new regresssion zerop the branches out before cloning new tree
    tree.SetBranchStatus('HCMVAV2_reg_mass',0)
    tree.SetBranchStatus('HCMVAV2_reg_pt',0)
    tree.SetBranchStatus('HCMVAV2_reg_eta',0)
    tree.SetBranchStatus('HCMVAV2_reg_phi',0)
    
    output.cd()
    
    newtree = tree.CloneTree(0)        

    JEC_systematics = {}

    hJ0 = ROOT.TLorentzVector()
    hJ1 = ROOT.TLorentzVector()

    # for the dijet mass/pt
    JEC_systematics['HCMVAV2_reg_mass'] = np.zeros(1, dtype=float)
    newtree.Branch('HCMVAV2_reg_mass', JEC_systematics['HCMVAV2_reg_mass'], 'HCMVAV2_reg_mass/F')
    
    JEC_systematics['HCMVAV2_reg_pt'] = np.zeros(1, dtype=float)
    newtree.Branch('HCMVAV2_reg_pt', JEC_systematics['HCMVAV2_reg_mass'], 'HCMVAV2_reg_pt/F')
    
    JEC_systematics['HCMVAV2_reg_eta'] = np.zeros(1, dtype=float)
    newtree.Branch('HCMVAV2_reg_eta', JEC_systematics['HCMVAV2_reg_eta'], 'HCMVAV2_reg_eta/F')

    JEC_systematics['HCMVAV2_reg_phi'] = np.zeros(1, dtype=float)
    newtree.Branch('HCMVAV2_reg_phi', JEC_systematics['HCMVAV2_reg_phi'], 'HCMVAV2_reg_phi/F')

    # For the dijet Jets
    JEC_systematics['hJetCMVAV2_pt_reg'] = np.zeros(2, dtype=float)
    newtree.Branch('hJetCMVAV2_pt_reg', JEC_systematics['hJetCMVAV2_pt_reg'], 'hJetCMVAV2_pt_reg[2]/F')
    
    for syst in JECsys:
        for sdir in ["Up", "Down"]:
            JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir] = np.zeros(1, dtype=float)
            newtree.Branch("HCMVAV2_reg_mass_corr"+syst+sdir, JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir], "HCMVAV2_reg_mass_corr"+syst+sdir+"/F")
            
            JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir] = np.zeros(1, dtype=float)
            newtree.Branch("HCMVAV2_reg_pt_corr"+syst+sdir, JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir], "HCMVAV2_reg_pt_corr"+syst+sdir+"/F")
                
            JEC_systematics["HCMVAV2_reg_eta_corr"+syst+sdir] = np.zeros(1, dtype=float)
            newtree.Branch("HCMVAV2_reg_eta_corr"+syst+sdir, JEC_systematics["HCMVAV2_reg_eta_corr"+syst+sdir], "HCMVAV2_reg_eta_corr"+syst+sdir+"/F")
            
            JEC_systematics["HCMVAV2_reg_phi_corr"+syst+sdir] = np.zeros(1, dtype=float)
            newtree.Branch("HCMVAV2_reg_phi_corr"+syst+sdir, JEC_systematics["HCMVAV2_reg_phi_corr"+syst+sdir], "HCMVAV2_reg_phi_corr"+syst+sdir+"/F")

            JEC_systematics["hJetCMVAV2_pt_reg"+syst+sdir] = np.zeros(2, dtype=float)
            newtree.Branch("hJetCMVAV2_pt_reg"+syst+sdir, JEC_systematics["hJetCMVAV2_pt_reg"+syst+sdir], "hJetCMVAV2_pt_reg"+syst+sdir+"[2]/F")


    # jet reg weights
    JetCMVAV2_regWeight = array('f',[0]*2)
    newtree.Branch('JetCMVAV2_regWeight',JetCMVAV2_regWeight,'JetCMVAV2_regWeight[2]/F')
    
    # define all the readers
    TMVA_reader = {}
    theVars1 = {}
    theVars0 = {}
    
    TMVA_reader['readerJet0'] = ROOT.TMVA.Reader("!Color:!Silent" )
    TMVA_reader['readerJet1'] = ROOT.TMVA.Reader("!Color:!Silent" )
    
    for syst in JECsys:
        for sdir in ["Up", "Down"]:
            TMVA_reader['readerJet0_'+syst+sdir] = ROOT.TMVA.Reader("!Color:!Silent" )
            TMVA_reader['readerJet1_'+syst+sdir] = ROOT.TMVA.Reader("!Color:!Silent" )

    def addVarsToReader(reader,theVars):
            for key in regVars:
                #print key
                var = regDict[key]
                theVars[key] = array( 'f', [ 0 ] )
                reader.AddVariable(key,theVars[key])
            return

    # Init the TMVA readers
    addVarsToReader(TMVA_reader['readerJet0'],theVars0)
    addVarsToReader(TMVA_reader['readerJet1'],theVars1)
    TMVA_reader['readerJet0'].BookMVA("readerJet0", regWeight)
    TMVA_reader['readerJet1'].BookMVA("readerJet1", regWeight)

    # for syst in JECsys:
    #     for sdir in ["Up", "Down"]:
    #         addVarsToReader(TMVA_reader['readerJet0_'+syst+sdir], theVarsJEC0[syst+sdir])
    #         addVarsToReader(TMVA_reader['readerJet1_'+syst+sdir], theVarsJEC1[syst+sdir])
    #         TMVA_reader['readerJet0_'+syst+sdir].BookMVA("readerJet0_"+syst+sdir, regWeight)
    #         TMVA_reader['readerJet1_'+syst+sdir].BookMVA("readerJet1_"+syst+sdir, regWeight)




    print '\n\t ----> Evaluating Regression on sample....'

    for entry in range(0,nEntries):
        
        tree.GetEntry(entry)
        
        if entry % 1000 is 0: print '-----> Event # ', entry

        if entry > 100: break

        Jet_pt_0 = tree.Jet_pt[tree.hJCMVAV2idx[0]]
        Jet_pt_1 = tree.Jet_pt[tree.hJCMVAV2idx[1]]
        Jet_eta_0 = tree.Jet_eta[tree.hJCMVAV2idx[0]]
        Jet_eta_1 = tree.Jet_eta[tree.hJCMVAV2idx[1]]
        Jet_ptRaw_0 = tree.Jet_rawPt[tree.hJCMVAV2idx[0]]
        Jet_ptRaw_1 = tree.Jet_rawPt[tree.hJCMVAV2idx[1]]
        Jet_m_0 = tree.Jet_mass[tree.hJCMVAV2idx[0]]
        Jet_m_1 = tree.Jet_mass[tree.hJCMVAV2idx[1]]
        Jet_phi_0 = tree.Jet_phi[tree.hJCMVAV2idx[0]]
        Jet_phi_1 = tree.Jet_phi[tree.hJCMVAV2idx[1]]
        
        Jet_e_0 = hJ0.E()
        Jet_e_1 = hJ1.E()
        Jet_mt_0 = hJ0.Mt()
        Jet_mt_1 = hJ1.Mt()
        
        Jet_vtxPt_0 = max(0.,tree.Jet_vtxPt[tree.hJCMVAV2idx[0]])
        Jet_vtxPt_1 = max(0.,tree.Jet_vtxPt[tree.hJCMVAV2idx[1]])
        Jet_vtx3dL_0= max(0.,tree.Jet_vtx3DVal[tree.hJCMVAV2idx[0]])
        Jet_vtx3dL_1= max(0.,tree.Jet_vtx3DVal[tree.hJCMVAV2idx[1]])
        Jet_vtx3deL_0= max(0.,tree.Jet_vtx3DSig[tree.hJCMVAV2idx[0]])
        Jet_vtx3deL_1= max(0.,tree.Jet_vtx3DSig[tree.hJCMVAV2idx[1]])
        Jet_vtxMass_0= max(0.,tree.Jet_vtxMass[tree.hJCMVAV2idx[0]])
        Jet_vtxMass_1= max(0.,tree.Jet_vtxMass[tree.hJCMVAV2idx[1]])
        Jet_vtxNtrk_0= max(0.,tree.Jet_vtxNtracks[tree.hJCMVAV2idx[0]])
        Jet_vtxNtrk_1= max(0.,tree.Jet_vtxNtracks[tree.hJCMVAV2idx[1]])
        
        Jet_chEmEF_0=tree.Jet_chEmEF[tree.hJCMVAV2idx[0]]
        Jet_chEmEF_1=tree.Jet_chEmEF[tree.hJCMVAV2idx[1]]
        Jet_chHEF_0=tree.Jet_chHEF[tree.hJCMVAV2idx[0]]
        Jet_chHEF_1=tree.Jet_chHEF[tree.hJCMVAV2idx[1]]
        Jet_neHEF_0=tree.Jet_neHEF[tree.hJCMVAV2idx[0]]
        Jet_neHEF_1=tree.Jet_neHEF[tree.hJCMVAV2idx[1]]
        Jet_neEmEF_0=tree.Jet_neEmEF[tree.hJCMVAV2idx[0]]
        Jet_neEmEF_1=tree.Jet_neEmEF[tree.hJCMVAV2idx[1]]
        Jet_rawPt_0 = tree.Jet_rawPt[tree.hJCMVAV2idx[0]]
        Jet_rawPt_1 = tree.Jet_rawPt[tree.hJCMVAV2idx[1]]
        Jet_chMult_0 = tree.Jet_chMult[tree.hJCMVAV2idx[0]]
        Jet_chMult_1 = tree.Jet_chMult[tree.hJCMVAV2idx[1]]
        Jet_leadTrackPt_0 = max(0.,tree.Jet_leadTrackPt[tree.hJCMVAV2idx[0]])
        Jet_leadTrackPt_1 = max(0.,tree.Jet_leadTrackPt[tree.hJCMVAV2idx[1]])
        Jet_leptonPtRel_0 = max(0.,tree.Jet_leptonPtRel[tree.hJCMVAV2idx[0]])
        Jet_leptonPtRel_1= max(0.,tree.Jet_leptonPtRel[tree.hJCMVAV2idx[1]])
        Jet_leptonDeltaR_0 = max(0.,tree.Jet_leptonDeltaR[tree.hJCMVAV2idx[0]])
        Jet_leptonDeltaR_1 = max(0.,tree.Jet_leptonDeltaR[tree.hJCMVAV2idx[0]])
        Jet_leptonPt_0 = max(0.,tree.Jet_leptonPt[tree.hJCMVAV2idx[0]])
        Jet_leptonPt_1= max(0.,tree.Jet_leptonPt[tree.hJCMVAV2idx[1]])
        rho_0=tree.rho
        rho_1=tree.rho
        
        nPVs_0=tree.nPVs
        nPVs_1=tree.nPVs
        
        # JEC factorized branches
        
        Jet_corr_JER_0 = tree.Jet_corr_JER[tree.hJCMVAV2idx[0]]
        Jet_corr_JER_1 = tree.Jet_corr_JER[tree.hJCMVAV2idx[1]]
        
        Jet_corr_0 = tree.Jet_corr[tree.hJCMVAV2idx[0]]
        Jet_corr_1 = tree.Jet_corr[tree.hJCMVAV2idx[1]]

        Jet_corr_JERUp_0 = tree.Jet_corr_JERUp[tree.hJCMVAV2idx[0]]
        Jet_corr_JERUp_1 = tree.Jet_corr_JERUp[tree.hJCMVAV2idx[1]]
        Jet_corr_JERDown_0 = tree.Jet_corr_JERDown[tree.hJCMVAV2idx[0]]
        Jet_corr_JERDown_1 = tree.Jet_corr_JERDown[tree.hJCMVAV2idx[1]]
        
        Jet_corr_PileUpDataMCUp_0 = tree.Jet_corr_PileUpDataMCUp[tree.hJCMVAV2idx[0]]
        Jet_corr_PileUpDataMCUp_1 = tree.Jet_corr_PileUpDataMCUp[tree.hJCMVAV2idx[1]]
        Jet_corr_PileUpDataMCDown_0 = tree.Jet_corr_PileUpDataMCDown[tree.hJCMVAV2idx[0]]
        Jet_corr_PileUpDataMCDown_1 = tree.Jet_corr_PileUpDataMCDown[tree.hJCMVAV2idx[1]]
        
        Jet_corr_PileUpPtRefUp_0 = tree.Jet_corr_PileUpPtRefUp[tree.hJCMVAV2idx[0]]
        Jet_corr_PileUpPtBBUp_0 = tree.Jet_corr_PileUpPtBBUp[tree.hJCMVAV2idx[0]]
        Jet_corr_PileUpPtEC1Up_0 = tree.Jet_corr_PileUpPtEC1Up[tree.hJCMVAV2idx[0]]
        Jet_corr_PileUpPtEC2Up_0 = tree.Jet_corr_PileUpPtEC2Up[tree.hJCMVAV2idx[0]]
        Jet_corr_PileUpPtHFUp_0 = tree.Jet_corr_PileUpPtHFUp[tree.hJCMVAV2idx[0]]
        
        Jet_corr_RelativeJEREC1Up_0 = tree.Jet_corr_RelativeJEREC1Up[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativeJEREC2Up_0 = tree.Jet_corr_RelativeJEREC2Up[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativeJERHFUp_0 = tree.Jet_corr_RelativeJERHFUp[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativeFSRUp_0 = tree.Jet_corr_RelativeFSRUp[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativeStatFSRUp_0 = tree.Jet_corr_RelativeStatFSRUp[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativeStatECUp_0 = tree.Jet_corr_RelativeStatECUp[tree.hJCMVAV2idx[0]]
        #Jet_corr_RelativeStatEC2Up_0 = tree.Jet_corr_RelativeStatEC2Up[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativeStatHFUp_0 = tree.Jet_corr_RelativeStatHFUp[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativePtBBUp_0 = tree.Jet_corr_RelativePtBBUp[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativePtEC1Up_0 = tree.Jet_corr_RelativePtEC1Up[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativePtEC2Up_0 = tree.Jet_corr_RelativePtEC2Up[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativePtHFUp_0 = tree.Jet_corr_RelativePtHFUp[tree.hJCMVAV2idx[0]]
        
        Jet_corr_AbsoluteScaleUp_0 = tree.Jet_corr_AbsoluteScaleUp[tree.hJCMVAV2idx[0]]
        Jet_corr_AbsoluteMPFBiasUp_0 = tree.Jet_corr_AbsoluteMPFBiasUp[tree.hJCMVAV2idx[0]]
        Jet_corr_AbsoluteStatUp_0 = tree.Jet_corr_AbsoluteStatUp[tree.hJCMVAV2idx[0]]
        Jet_corr_SinglePionECALUp_0 = tree.Jet_corr_SinglePionECALUp[tree.hJCMVAV2idx[0]]
        Jet_corr_SinglePionHCALUp_0 = tree.Jet_corr_SinglePionHCALUp[tree.hJCMVAV2idx[0]]
        Jet_corr_FragmentationUp_0 = tree.Jet_corr_FragmentationUp[tree.hJCMVAV2idx[0]]
        Jet_corr_TimePtEtaUp_0 = tree.Jet_corr_TimePtEtaUp[tree.hJCMVAV2idx[0]]
        Jet_corr_FlavorQCDUp_0 = tree.Jet_corr_FlavorQCDUp[tree.hJCMVAV2idx[0]]

        # Jet 2
        Jet_corr_PileUpPtRefUp_1 = tree.Jet_corr_PileUpPtRefUp[tree.hJCMVAV2idx[1]]
        Jet_corr_PileUpPtBBUp_1 = tree.Jet_corr_PileUpPtBBUp[tree.hJCMVAV2idx[1]]
        Jet_corr_PileUpPtEC1Up_1 = tree.Jet_corr_PileUpPtEC1Up[tree.hJCMVAV2idx[1]]
        Jet_corr_PileUpPtEC2Up_1 = tree.Jet_corr_PileUpPtEC2Up[tree.hJCMVAV2idx[1]]
        Jet_corr_PileUpPtHFUp_1 = tree.Jet_corr_PileUpPtHFUp[tree.hJCMVAV2idx[1]]
        
        Jet_corr_RelativeJEREC1Up_1 = tree.Jet_corr_RelativeJEREC1Up[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativeJEREC2Up_1 = tree.Jet_corr_RelativeJEREC2Up[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativeJERHFUp_1 = tree.Jet_corr_RelativeJERHFUp[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativeFSRUp_1 = tree.Jet_corr_RelativeFSRUp[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativeStatFSRUp_1 = tree.Jet_corr_RelativeStatFSRUp[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativeStatECUp_1 = tree.Jet_corr_RelativeStatECUp[tree.hJCMVAV2idx[1]]
        #Jet_corr_RelativeStatEC2Up_1 = tree.Jet_corr_RelativeStatEC2Up[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativeStatHFUp_1 = tree.Jet_corr_RelativeStatHFUp[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativePtBBUp_1 = tree.Jet_corr_RelativePtBBUp[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativePtEC1Up_1 = tree.Jet_corr_RelativePtEC1Up[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativePtEC2Up_1 = tree.Jet_corr_RelativePtEC2Up[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativePtHFUp_1 = tree.Jet_corr_RelativePtHFUp[tree.hJCMVAV2idx[1]]
        
        Jet_corr_AbsoluteScaleUp_1 = tree.Jet_corr_AbsoluteScaleUp[tree.hJCMVAV2idx[1]]
        Jet_corr_AbsoluteMPFBiasUp_1 = tree.Jet_corr_AbsoluteMPFBiasUp[tree.hJCMVAV2idx[1]]
        Jet_corr_AbsoluteStatUp_1 = tree.Jet_corr_AbsoluteStatUp[tree.hJCMVAV2idx[1]]
        Jet_corr_SinglePionECALUp_1 = tree.Jet_corr_SinglePionECALUp[tree.hJCMVAV2idx[1]]
        Jet_corr_SinglePionHCALUp_1 = tree.Jet_corr_SinglePionHCALUp[tree.hJCMVAV2idx[1]]
        Jet_corr_FragmentationUp_1 = tree.Jet_corr_FragmentationUp[tree.hJCMVAV2idx[1]]
        Jet_corr_TimePtEtaUp_1 = tree.Jet_corr_TimePtEtaUp[tree.hJCMVAV2idx[1]]
        Jet_corr_FlavorQCDUp_1 = tree.Jet_corr_FlavorQCDUp[tree.hJCMVAV2idx[1]]

        ## Down ##
        Jet_corr_PileUpDataMCDown_0 = tree.Jet_corr_PileUpDataMCDown[tree.hJCMVAV2idx[0]]
        Jet_corr_PileUpDataMCDown_1 = tree.Jet_corr_PileUpDataMCDown[tree.hJCMVAV2idx[1]]
        Jet_corr_PileUpDataMCDown_0 = tree.Jet_corr_PileUpDataMCDown[tree.hJCMVAV2idx[0]]
        Jet_corr_PileUpDataMCDown_1 = tree.Jet_corr_PileUpDataMCDown[tree.hJCMVAV2idx[1]]
        
        Jet_corr_PileUpPtRefDown_0 = tree.Jet_corr_PileUpPtRefDown[tree.hJCMVAV2idx[0]]
        Jet_corr_PileUpPtBBDown_0 = tree.Jet_corr_PileUpPtBBDown[tree.hJCMVAV2idx[0]]
        Jet_corr_PileUpPtEC1Down_0 = tree.Jet_corr_PileUpPtEC1Down[tree.hJCMVAV2idx[0]]
        Jet_corr_PileUpPtEC2Down_0 = tree.Jet_corr_PileUpPtEC2Down[tree.hJCMVAV2idx[0]]
        Jet_corr_PileUpPtHFDown_0 = tree.Jet_corr_PileUpPtHFDown[tree.hJCMVAV2idx[0]]
        
        Jet_corr_RelativeJEREC1Down_0 = tree.Jet_corr_RelativeJEREC1Down[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativeJEREC2Down_0 = tree.Jet_corr_RelativeJEREC2Down[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativeJERHFDown_0 = tree.Jet_corr_RelativeJERHFDown[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativeFSRDown_0 = tree.Jet_corr_RelativeFSRDown[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativeStatFSRDown_0 = tree.Jet_corr_RelativeStatFSRDown[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativeStatECDown_0 = tree.Jet_corr_RelativeStatECDown[tree.hJCMVAV2idx[0]]
        #Jet_corr_RelativeStatEC2Down_0 = tree.Jet_corr_RelativeStatEC2Down[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativeStatHFDown_0 = tree.Jet_corr_RelativeStatHFDown[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativePtBBDown_0 = tree.Jet_corr_RelativePtBBDown[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativePtEC1Down_0 = tree.Jet_corr_RelativePtEC1Down[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativePtEC2Down_0 = tree.Jet_corr_RelativePtEC2Down[tree.hJCMVAV2idx[0]]
        Jet_corr_RelativePtHFDown_0 = tree.Jet_corr_RelativePtHFDown[tree.hJCMVAV2idx[0]]
        
        Jet_corr_AbsoluteScaleDown_0 = tree.Jet_corr_AbsoluteScaleDown[tree.hJCMVAV2idx[0]]
        Jet_corr_AbsoluteMPFBiasDown_0 = tree.Jet_corr_AbsoluteMPFBiasDown[tree.hJCMVAV2idx[0]]
        Jet_corr_AbsoluteStatDown_0 = tree.Jet_corr_AbsoluteStatDown[tree.hJCMVAV2idx[0]]
        Jet_corr_SinglePionECALDown_0 = tree.Jet_corr_SinglePionECALDown[tree.hJCMVAV2idx[0]]
        Jet_corr_SinglePionHCALDown_0 = tree.Jet_corr_SinglePionHCALDown[tree.hJCMVAV2idx[0]]
        Jet_corr_FragmentationDown_0 = tree.Jet_corr_FragmentationDown[tree.hJCMVAV2idx[0]]
        Jet_corr_TimePtEtaDown_0 = tree.Jet_corr_TimePtEtaDown[tree.hJCMVAV2idx[0]]
        Jet_corr_FlavorQCDDown_0 = tree.Jet_corr_FlavorQCDDown[tree.hJCMVAV2idx[0]]

        # Jet 2
        Jet_corr_PileUpPtRefDown_1 = tree.Jet_corr_PileUpPtRefDown[tree.hJCMVAV2idx[1]]
        Jet_corr_PileUpPtBBDown_1 = tree.Jet_corr_PileUpPtBBDown[tree.hJCMVAV2idx[1]]
        Jet_corr_PileUpPtEC1Down_1 = tree.Jet_corr_PileUpPtEC1Down[tree.hJCMVAV2idx[1]]
        Jet_corr_PileUpPtEC2Down_1 = tree.Jet_corr_PileUpPtEC2Down[tree.hJCMVAV2idx[1]]
        Jet_corr_PileUpPtHFDown_1 = tree.Jet_corr_PileUpPtHFDown[tree.hJCMVAV2idx[1]]
        
        Jet_corr_RelativeJEREC1Down_1 = tree.Jet_corr_RelativeJEREC1Down[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativeJEREC2Down_1 = tree.Jet_corr_RelativeJEREC2Down[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativeJERHFDown_1 = tree.Jet_corr_RelativeJERHFDown[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativeFSRDown_1 = tree.Jet_corr_RelativeFSRDown[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativeStatFSRDown_1 = tree.Jet_corr_RelativeStatFSRDown[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativeStatECDown_1 = tree.Jet_corr_RelativeStatECDown[tree.hJCMVAV2idx[1]]
        #Jet_corr_RelativeStatEC2Down_1 = tree.Jet_corr_RelativeStatEC2Down[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativeStatHFDown_1 = tree.Jet_corr_RelativeStatHFDown[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativePtBBDown_1 = tree.Jet_corr_RelativePtBBDown[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativePtEC1Down_1 = tree.Jet_corr_RelativePtEC1Down[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativePtEC2Down_1 = tree.Jet_corr_RelativePtEC2Down[tree.hJCMVAV2idx[1]]
        Jet_corr_RelativePtHFDown_1 = tree.Jet_corr_RelativePtHFDown[tree.hJCMVAV2idx[1]]
        
        Jet_corr_AbsoluteScaleDown_1 = tree.Jet_corr_AbsoluteScaleDown[tree.hJCMVAV2idx[1]]
        Jet_corr_AbsoluteMPFBiasDown_1 = tree.Jet_corr_AbsoluteMPFBiasDown[tree.hJCMVAV2idx[1]]
        Jet_corr_AbsoluteStatDown_1 = tree.Jet_corr_AbsoluteStatDown[tree.hJCMVAV2idx[1]]
        Jet_corr_SinglePionECALDown_1 = tree.Jet_corr_SinglePionECALDown[tree.hJCMVAV2idx[1]]
        Jet_corr_SinglePionHCALDown_1 = tree.Jet_corr_SinglePionHCALDown[tree.hJCMVAV2idx[1]]
        Jet_corr_FragmentationDown_1 = tree.Jet_corr_FragmentationDown[tree.hJCMVAV2idx[1]]
        Jet_corr_TimePtEtaDown_1 = tree.Jet_corr_TimePtEtaDown[tree.hJCMVAV2idx[1]]
        Jet_corr_FlavorQCDDown_1 = tree.Jet_corr_FlavorQCDDown[tree.hJCMVAV2idx[1]]
        

        for key in regVars:
            #print '\n\tSetting Variable:', key
            theVars0[key][0] = eval("%s_0" %(key))
            theVars1[key][0] = eval("%s_1" %(key))

        ##### Evaluate the regression #####    
        Pt0 = max(0.0001, TMVA_reader['readerJet0'].EvaluateRegression("readerJet0")[0])
        Pt1 = max(0.0001, TMVA_reader['readerJet1'].EvaluateRegression("readerJet1")[0])
        
        rPt0 = Jet_pt_0*Pt0
        rPt1 = Jet_pt_1*Pt1
        
        JEC_systematics["hJetCMVAV2_pt_reg"][0] = Pt0
        JEC_systematics["hJetCMVAV2_pt_reg"][1] = Pt1

        JetCMVAV2_regWeight[0] = Pt0/Jet_pt_0
        JetCMVAV2_regWeight[1] = Pt1/Jet_pt_1
        
        hJ0.SetPtEtaPhiM(Pt0, Jet_eta_0, Jet_phi_0, Jet_m_0*(Pt0/Jet_pt_0))
        hJ1.SetPtEtaPhiM(Pt1, Jet_eta_1, Jet_phi_1, Jet_m_1*(Pt1/Jet_pt_1))
            
        JEC_systematics["HCMVAV2_reg_mass"][0] = (hJ0+hJ1).M()
        JEC_systematics["HCMVAV2_reg_pt"][0]   = (hJ0+hJ1).Pt()
        JEC_systematics["HCMVAV2_reg_eta"][0]  = (hJ0+hJ1).Eta()
        JEC_systematics["HCMVAV2_reg_phi"][0]  = (hJ0+hJ1).Phi()

        #print '\n\n\nJet1 pt reg:', Pt0, Jet_pt_0
        #print 'Jet2 pt reg:', Pt1, Jet_pt_1
        #print 'Hmass Reg:', JEC_systematics["HCMVAV2_reg_mass"][0], tree.H_reg_mass


        if 'Zee' in file or 'Zuu' in file: 
            newtree.Fill()
            continue

        for syst in JECsys:
            for sdir in ["Up", "Down"]:
                theVars0['Jet_pt'][0] = 0
                theVars1['Jet_pt'][0] = 0
                if syst == "JER":
                    formula1 = "Jet_rawPt_0*Jet_corr_0*Jet_corr_JER"+sdir+"_0"
                    formula2 = "Jet_rawPt_1*Jet_corr_1*Jet_corr_JER"+sdir+"_1"
                    theVars0['Jet_pt'][0] = eval(formula1)
                    theVars1['Jet_pt'][0] = eval(formula2)
                else:
                    formula1 = "Jet_rawPt_0*Jet_corr_"+syst+sdir+"_0*Jet_corr_JER_0"
                    formula2 = "Jet_rawPt_1*Jet_corr_"+syst+sdir+"_1*Jet_corr_JER_1"
                    theVars0['Jet_pt'][0] = eval(formula1)
                    theVars1['Jet_pt'][0] = eval(formula2)

                
                pt1 = max(0.0001, TMVA_reader['readerJet0'].EvaluateRegression("readerJet0")[0])
                pt2 = max(0.0001, TMVA_reader['readerJet1'].EvaluateRegression("readerJet1")[0])

                rPt0 = Jet_pt_0*pt1
                rPt1 = Jet_pt_1*pt2
                
                JEC_systematics["hJetCMVAV2_pt_reg"+syst+sdir][0] = pt1
                JEC_systematics["hJetCMVAV2_pt_reg"+syst+sdir][1] = pt2
                
                Jet_regWeight1 = pt1/Jet_pt_0
                Jet_regWeight2 = pt2/Jet_pt_1
                
                hJ0.SetPtEtaPhiM(pt1, Jet_eta_0, Jet_phi_0, Jet_m_0*Jet_regWeight1)
                hJ1.SetPtEtaPhiM(pt2, Jet_eta_1, Jet_phi_1, Jet_m_1*Jet_regWeight2)
                
                JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir][0] = (hJ0+hJ1).M()
                JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir][0] = (hJ0+hJ1).Pt()
                JEC_systematics["HCMVAV2_reg_eta_corr"+syst+sdir][0] = (hJ0+hJ1).Eta()
                JEC_systematics["HCMVAV2_reg_phi_corr"+syst+sdir][0] = (hJ0+hJ1).Phi()
                
                #print syst+sdir+' Jet1 pt reg:', pt1
                #print syst+sdir+' Jet2 pt reg:', pt2
                #print syst+sdir+'Hmass Reg:', JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir][0]

        # for key in regVars:
        #     for syst in JECsys:
        #         for sdir in ["Up", "Down"]:
        #             if 'Jet_pt' in key:
        #                 if syst == "JER":
        #                     formula1 = "Jet_rawPt_0*Jet_corr_0*Jet_corr_JER"+sdir+"_0"
        #                     formula2 = "Jet_rawPt_1*Jet_corr_1*Jet_corr_JER"+sdir+"_1"
        #                     theVarsJEC0[syst+sdir][key][0] = eval(formula1)
        #                     theVarsJEC1[syst+sdir][key][0] = eval(formula2)
        #                 else:
        #                     formula1 = "Jet_rawPt_0*Jet_corr_"+syst+sdir+"_0*Jet_corr_JER_0"
        #                     formula2 = "Jet_rawPt_1*Jet_corr_"+syst+sdir+"_1*Jet_corr_JER_1"
        #                     theVarsJEC0[syst+sdir][key][0] = eval(formula1)
        #                     theVarsJEC1[syst+sdir][key][0] = eval(formula2)
        #             else:
        #                 theVarsJEC0[syst+sdir][key][0] = eval("%s_0" %(key))
        #                 theVarsJEC1[syst+sdir][key][0] = eval("%s_1" %(key))
        
        # for syst in JECsys:
        #     for sdir in ["Up", "Down"]:
                
        #         print '\n CHeck witth unique BDT...'
        
        #         pt1 = max(0.0001, TMVA_reader['readerJet0_'+syst+sdir].EvaluateRegression("readerJet0_"+syst+sdir)[0])
        #         pt2 = max(0.0001, TMVA_reader['readerJet1_'+syst+sdir].EvaluateRegression("readerJet1_"+syst+sdir)[0])
        
        #         rPt0 = Jet_pt_0*pt1
        #         rPt1 = Jet_pt_1*pt2
        
        #         JEC_systematics["hJetCMVAV2_pt_reg"+syst+sdir][0] = pt1
        #         JEC_systematics["hJetCMVAV2_pt_reg"+syst+sdir][1] = pt2
        
        #         Jet_regWeight1 = pt1/Jet_pt_0
        #         Jet_regWeight2 = pt2/Jet_pt_1
        
        #         hJ0.SetPtEtaPhiM(pt1, Jet_eta_0, Jet_phi_0, Jet_m_0*Jet_regWeight1)
        #         hJ1.SetPtEtaPhiM(pt2, Jet_eta_1, Jet_phi_1, Jet_m_1*Jet_regWeight2)
                
        #         JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir][0] = (hJ0+hJ1).M()
        #         JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir][0] = (hJ0+hJ1).Pt()
        #         JEC_systematics["HCMVAV2_reg_eta_corr"+syst+sdir][0] = (hJ0+hJ1).Eta()
        #         JEC_systematics["HCMVAV2_reg_phi_corr"+syst+sdir][0] = (hJ0+hJ1).Phi()
                
        #         print syst+sdir+' Jet1 pt reg:', pt1
        #         print syst+sdir+' Jet2 pt reg:', pt2
        #         print syst+sdir+'Hmass Reg:', JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir][0]



        
        # Fill Tree
        newtree.Fill()
        
    newtree.AutoSave()
    output.Close()




