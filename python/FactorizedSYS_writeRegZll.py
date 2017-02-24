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

    regWeight = '/afs/cern.ch/user/c/cvernier/public/forDavid/TMVARegression_BDTG.weights.xml'

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
        "PileUpPtBB",
        "PileUpPtEC1",
        "PileUpPtEC2",
        "PileUpPtHF",
        
        "RelativeJEREC1",
        "RelativeJEREC2",
        "RelativeJERHF",
        "RelativeFSR",
        "RelativeStatFSR",
        "RelativeStatEC",
        "RelativeStatEC2",
        "RelativeStatHF",
        "RelativePtBB",
        "RelativePtEC1",
        "RelativePtEC2",
        "RelativePtHF",
        
        "AbsoluteScale",
        "AbsoluteMPFBias",
        "AbsoluteStat",
        "SinglePionECAL",
        "SinglePionHCAL",
        "Fragmentation",
        "TimePtEta",
        "FlavorQCD"
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
    
    output.cd()
    
    newtree = tree.CloneTree(0)        

    JEC_systematics = {}

    # for the dijet mass/pt
    JEC_systematics['HCMVAV2_reg_mass'] = np.zeros(1, dtype=float)
    newtree.Branch('HCMVAV2_reg_mass', JEC_systematics['HCMVAV2_reg_mass'], 'HCMVAV2_reg_mass/F')
    
    JEC_systematics['HCMVAV2_reg_pt'] = np.zeros(1, dtype=float)
    newtree.Branch('HCMVAV2_reg_pt', JEC_systematics['HCMVAV2_reg_mass'], 'HCMVAV2_reg_pt/F')
    
    # For the dijet Jets
    JEC_systematics['hJetCMVAV2_pt_reg'] = np.zeros(2, dtype=float)
    newtree.Branch('hJetCMVAV2_pt_reg', JEC_systematics['hJetCMVAV2_pt_reg'], 'hJetCMVAV2_pt_reg[2]/F')
    
    for syst in ["JER", "JEC"]:
        for sdir in ["Up", "Down"]:
            if 'JEC' in syst:
                for fact in JECsys:
                    JEC_systematics["HCMVAV2_reg_mass_corr"+syst+fact+sdir] = np.zeros(1, dtype=float)
                    newtree.Branch("HCMVAV2_reg_mass_corr"+syst+fact+sdir, JEC_systematics["HCMVAV2_reg_mass_corr"+syst+fact+sdir], "HCMVAV2_reg_mass_corr"+syst+fact+sdir+"/F")

                    JEC_systematics["HCMVAV2_reg_pt_corr"+syst+fact+sdir] = np.zeros(1, dtype=float)
                    newtree.Branch("HCMVAV2_reg_pt_corr"+syst+fact+sdir, JEC_systematics["HCMVAV2_reg_pt_corr"+syst+fact+sdir], "HCMVAV2_reg_pt_corr"+syst+fact+sdir+"/F")
                
                    JEC_systematics["hJetCMVAV2_pt_reg"+syst+fact+sdir] = np.zeros(2, dtype=float)
                    newtree.Branch("hJetCMVAV2_pt_reg"+syst+fact+sdir, JEC_systematics["hJetCMVAV2_pt_reg"+syst+fact+sdir], "hJetCMVAV2_pt_reg"+syst+fact+sdir+"[2]/F")
            else:
                JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir] = np.zeros(1, dtype=float)
                newtree.Branch("HCMVAV2_reg_mass_corr"+syst+sdir, JEC_systematics["HCMVAV2_reg_mass_corr"+syst+sdir], "HCMVAV2_reg_mass_corr"+syst+sdir+"/F")
                
                JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir] = np.zeros(1, dtype=float)
                newtree.Branch("HCMVAV2_reg_pt_corr"+syst+sdir, JEC_systematics["HCMVAV2_reg_pt_corr"+syst+sdir], "HCMVAV2_reg_pt_corr"+syst+sdir+"/F")
                
                JEC_systematics["hJetCMVAV2_pt_reg"+syst+sdir] = np.zeros(2, dtype=float)
                newtree.Branch("hJetCMVAV2_pt_reg"+syst+sdir, JEC_systematics["hJetCMVAV2_pt_reg"+syst+sdir], "hJetCMVAV2_pt_reg"+syst+sdir+"[2]/F")



    # jet reg weights
    JetCMVAV2_regWeight = array('f',[0]*2)
    newtree.Branch('JetCMVAV2_regWeight',JetCMVAV2_regWeight,'JetCMVAV2_regWeight[2]/F')
    
    # define all the readers
    TMVA_reader = {}
    tmva_vars = {}
    theForms = {}
    theVars0 = {}
    theVars1 = {}
    
    
    TMVA_reader['readerJet0'] = ROOT.TMVA.Reader("!Color:!Silent" )
    TMVA_reader['readerJet1'] = ROOT.TMVA.Reader("!Color:!Silent" )

    
    for syst in ["JER", "JEC"]:
        for sdir in ["Up", "Down"]:
            if 'JEC' in syst:
                for fact in JECsys:
                    TMVA_reader['readerJet0_'+syst+fact+sdir] = ROOT.TMVA.Reader("!Color:!Silent")    
                    TMVA_reader['readerJet1_'+syst+fact+sdir] = ROOT.TMVA.Reader("!Color:!Silent")
            else:
                TMVA_reader['readerJet0_'+syst+sdir] = ROOT.TMVA.Reader("!Color:!Silent")
                TMVA_reader['readerJet1_'+syst+sdir] = ROOT.TMVA.Reader("!Color:!Silent")


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


    def addVarsToReaderJEC(reader,theVars,theForms,i,syst=""):

            print '\n======== Adding Variables to Reader for Jet', i, ' ========'
            print 'Systematic:', syst

            for key in regVars:

                var = regDict[key]
                theVars[key+syst] = array( 'f', [ 0 ] )

                reader.AddVariable(key,theVars[key+syst])
                formulaX = var
                brakets = ""
                if i == 1: brakets = "[hJCMVAV2idx[0]]"
                if 1 == 2: brakets = "[hJCMVAV2idx[1]]"
                else: pass

                formulaX = formulaX.replace(brakets,"[X]")

                if syst == "":
                    pass
                elif syst == "JERUp":
                    formulaX = formulaX.replace("Jet_pt[X]","Jet_rawPt[X]*Jet_corr[X]*Jet_corr_JERUp[X]")
                elif syst == "JERDown":
                    formulaX = formulaX.replace("Jet_pt[X]","Jet_rawPt[X]*Jet_corr[X]*Jet_corr_JERDown[X]")
                else:
                    formulaX = formulaX.replace("Jet_pt[X]","Jet_rawPt[X]*Jet_corr_"+syst+"[X]*Jet_corr_JER[X]")

                print 'Adding var: %s to with reference %s readerJet%s' %(key, formulaX, i)

                formula = formulaX.replace("[X]",brakets)
                formula = formula.replace("[0]","[%.0f]" %i)
                theForms['form_reg_%s_%.0f'%(key+syst,i)] = formula

                #theForms['form_reg_%s_%.0f'%(key,i)] = ROOT.TTreeFormula("form_reg_%s_%.0f"%(key,i),'%s' %(formula),tree)
                #theForms['form_reg_%s_%.0f'%(key,i)].GetNdata()



    # Init the TKVA readers

    addVarsToReader(TMVA_reader['readerJet0'],theVars0,theForms,0)
    addVarsToReader(TMVA_reader['readerJet1'],theVars1,theForms,1)
    TMVA_reader['readerJet0'].BookMVA("readerJet0", regWeight)
    TMVA_reader['readerJet1'].BookMVA("readerJet1", regWeight)
    
    if 'Zee' not in file or 'Zuu' not in file:
        for syst in ["JER", "JEC"]:
            for sdir in ["Up", "Down"]:
                if 'JEC' in syst:
                    for fact in JECsys:
                        addVarsToReader(TMVA_reader['readerJet0_'+syst+fact+sdir],theVars0,theForms,0,fact+sdir)
                        addVarsToReader(TMVA_reader['readerJet1_'+syst+fact+sdir],theVars0,theForms,1,fact+sdir)
                        TMVA_reader['readerJet0_'+syst+fact+sdir].BookMVA('readerJet0_'+syst+fact+sdir, regWeight)
                        TMVA_reader['readerJet1_'+syst+fact+sdir].BookMVA('readerJet1_'+syst+fact+sdir, regWeight)
                else:
                    addVarsToReader(TMVA_reader['readerJet0_'+syst+sdir],theVars0,theForms,0,syst+sdir)
                    addVarsToReader(TMVA_reader['readerJet1_'+syst+sdir],theVars0,theForms,1,syst+sdir)
                    TMVA_reader['readerJet0_'+syst+sdir].BookMVA('readerJet0_'+syst+sdir, regWeight)
                    TMVA_reader['readerJet1_'+syst+sdir].BookMVA('readerJet1_'+syst+sdir, regWeight)
    

print tree

for entry in range(0,nEntries):
        

            tree.GetEntry(entry)
	    #Event[0]=tree.evt
            
            if entry % 10000 is 0: print '-----> Event # ', entry
            
            if entry > 10000: break


            
            
            hJ0.SetPtEtaPhiM(Jet_pt_0,Jet_eta_0,Jet_phi_0,Jet_m_0)
            hJ1.SetPtEtaPhiM(Jet_pt_1,Jet_eta_1,Jet_phi_1,Jet_m_1)
            
            Jet_e_0 = hJ0.E()
            Jet_e_1 = hJ1.E()
            Jet_mt_0 = hJ0.Mt()
            Jet_mt_1 = hJ1.Mt()
                        
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
            
	    for key in regVars:
                #print key	
                if 'Jet_pt' not in key:
                    theVars0[key][0] = eval("%s_0" %(key)) 
                    theVars1[key][0] = eval("%s_1" %(key))
                
                if 'Jet_pt' in key:
                    for syst in ["JER", "JEC"]:
                        for sdir in ["Up", "Down"]:
                                
                            if syst == "JER":
                                formula1 = "Jet_rawPt[hJCMVAV2idx[0]]*Jet_corr[hJCMVAV2idx[0]]*Jet_corr_JER"+sdir+"[hJCMVAV2idx[0]]"
                                formula2 = "Jet_rawPt[hJCMVAV2idx[1]]*Jet_corr[hJCMVAV2idx[1]]*Jet_corr_JER"+sdir+"[hJCMVAV2idx[1]]"
                                theVars0[key+syst+fact+sdir][0] = eval(formula1)
                                theVars1[key+syst+fact+sdir][0] = eval(formula2)
                            if syst == "JEC":
                                for fact in JECsys:
                                    formula1 = "Jet_rawPt[hJCMVAV2idx[0]]*Jet_corr_"+fact+sdir+"[hJCMVAV2idx[0]]*Jet_corr_JER[hJCMVAV2idx[0]]"
                                    formula2 = "Jet_rawPt[hJCMVAV2idx[1]]*Jet_corr_"+fact+sdir+"[hJCMVAV2idx[1]]*Jet_corr_JER[hJCMVAV2idx[1]]"
                                    theVars0[key+syst+fact+sdir][0] = eval(formula1)
                                    theVars1[key+syst+fact+sdir][0] = eval(formula2)

                            
            ##### Evaluate the regression #####    
            Pt0 = max(0.0001,readerJet0.EvaluateRegression( "jet0Regression" )[0])
            Pt1 = max(0.0001,readerJet1.EvaluateRegression( "jet1Regression" )[0])
                
            rPt0 = Jet_pt_0*Pt0
            rPt1 = Jet_pt_1*Pt1
                
            hJet_pt_reg[0] = Pt0
            hJet_pt_reg[1] = Pt1
                            
            Jet_regWeight[0] = Pt0/Jet_pt_0
            Jet_regWeight[1] = Pt1/Jet_pt_1
                
            hJ0.SetPtEtaPhiM(Pt0,Jet_eta_0,Jet_phi_0, Jet_m_0*Jet_regWeight[0])
            hJ1.SetPtEtaPhiM(Pt1,Jet_eta_1,Jet_phi_1, Jet_m_1*Jet_regWeight[1])
                
            #print '\nJet1 pt reg:', Pt0
            #print 'Jet2 pt reg:', Pt1

            H.HiggsFlag = 1
            H.mass = (hJ0+hJ1).M()
            H.pt = (hJ0+hJ1).Pt()
            H.eta = (hJ0+hJ1).Eta()
            H.phi = (hJ0+hJ1).Phi()
            H.dR = hJ0.DeltaR(hJ1)
            H.dPhi = hJ0.DeltaPhi(hJ1)
            H.dEta = abs(hJ0.Eta()-hJ1.Eta())
            
            
            # Fill Tree
            newtree.Fill()
        
newtree.AutoSave()
output.Close()


# Write Histograms
for hist in hist_list:
    if isinstance(hist, list):
        newfile.mkdir('%s' % hist[0].GetName()).cd()
        for i in hist: i.Write()
    else: hist.Write()

for ihist in hist_list_noReg:
    if isinstance(ihist, list):
        newfile.mkdir('%s' % ihist[0].GetName()).cd()
        for i in ihist: i.Write()
    else: ihist.Write()


for hist in extra_hist_list:
    if isinstance(hist, list):
        newfile.mkdir('%s' % hist[0].GetName()).cd()
        for i in hist: i.Write()
    else: hist.Write()

del newfile


print count
