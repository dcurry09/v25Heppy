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
#from BetterConfigParser import BetterConfigParser
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='creating converter.*' )
argv = sys.argv

count = Counter()


def deltaPhi(phi1, phi2): 
    result = phi1 - phi2
    while (result > math.pi): result -= 2*math.pi
    while (result <= -math.pi): result += 2*math.pi
    return result

do = True

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





#input  = TFile.Open('/exports/uftrig01a/dcurry/heppy/v23/DY_inclusive.root', 'read')
input  = TFile.Open('/exports/uftrig01a/dcurry/heppy/files/sys_out/v25_ZH125.root', 'read')

output = TFile.Open('/exports/uftrig01a/dcurry/heppy/files/prep_out/regression_v25_ZH_noMET.root', 'recreate')

#with MET
#regWeight = '/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/myMacros/regression/forDavid/weights_zh/TMVARegression_BDTG.weights.xml'

# no MET
regWeight = '/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/myMacros/regression/forDavid/fordavid_nomet/TMVARegression_BDTG.weights.xml'

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
           #"met_pt",
           #"Jet_met_proj"
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
H = ROOT.H()
HNoReg = ROOT.H()
HwithM = ROOT.H()	
tree.SetBranchStatus('H',0)
output.cd()
newtree = tree.CloneTree(0)        


regDict = {"Jet_pt":"Jet_pt[0]",
           #"Jet_corr":"Jet_corr[0]",
           "nPVs":"nPVs[0]",
           "Jet_eta":"Jet_eta[0]",
           "Jet_mt":"Jet_mt[0]",
           "Jet_leadTrackPt": "Jet_leadTrackPt[0]",
           "Jet_leptonPtRel":"Jet_leptonPtRel[0]",
           "Jet_leptonPt":"Jet_leptonPt[0]",
           "Jet_leptonDeltaR":"Jet_leptonDeltaR[0]",
           "Jet_neHEF":"Jet_neHEF[0]",
           #"Jet_chHEF+Jet_neHEF":"Jet_chHEF[0]+Jet_neHEF[0]",
           "Jet_neEmEF":"Jet_neEmEF[0]",
           "Jet_vtxPt":"Jet_vtxPt[0]",
           "Jet_vtxMass":"Jet_vtxMass[0]",
           "Jet_vtx3dL":"Jet_vtx3dl[0]",
           "Jet_vtxNtrk":"Jet_vtxNtrk[0]",
           "Jet_vtx3deL":"Jet_vtx3deL[0]",
           #"met_pt":"met_pt",
           #"Jet_met_proj":"Jet_met_proj"
           } 





# ====== Output histograms ======
newfile = TFile("response_plots/ttbar_v23_highPt.root","recreate")

Jet_pt = TH2D('Jet_pt', '', 30 ,20,300, 10, -.1, .1)
Jet_corr = TH2D('Jet_corr', '', 30, 0.8, 1.4, 10, -.1, .1)
nPvs = TH2D('nPvs', '', 30 , 0, 25, 10, -.1, .1)
Jet_eta = TH2D('Jet_eta', '', 30, -2.4, 2.4, 10, -.1, .1)
Jet_mt = TH2D('Jet_mt', '', 30, 0, 225, 10, -.1, .1)
Jet_leadTrackPt = TH2D('Jet_leadTrackPt', '', 30, 0, 100, 10, -.1, .1)
Jet_leptonPtRel = TH2D('Jet_leptonPtRel', '', 30, 0, 5, 10, -.1, .1)
Jet_leptonPt = TH2D('Jet_leptonPt', '', 30, 0, 75, 10, -.1, .1)
Jet_leptonDeltaR = TH2D('Jet_leptonDeltaR', '', 30, 0, 0.5, 10, -.1, .1)
Jet_chHEF = TH2D('Jet_chHEF', '', 30, 0, 0.5, 10, -.1, .1)
Jet_neHEF = TH2D('Jet_neHEF', '', 30, 0, 0.5, 10, -.1, .1)
Jet_neEmEF = TH2D('Jet_neEmEF', '', 30, 0, 1, 10, -.1, .1)
Jet_vtxPt = TH2D('Jet_vtxPt', '', 30, 0, 100, 10, -.1, .1)
Jet_vtxMass = TH2D('Jet_vtxMass', '', 30, 0, 5, 10, -.1, .1)
Jet_vtx3dL = TH2D('Jet_vtx3dL', '', 30, 0, 10, 10, -.1, .1)
Jet_vtxNtrk = TH2D('Jet_vtxNtrk', '', 10, 0, 10, 10, -.1, .1)
Jet_vtx3deL = TH2D('Jet_vtx3deL', '', 30, 0, 10, 10, -.1, .1)


Jet_pt_noReg = TH2D('Jet_pt_noReg', '', 30 ,20,300, 10, -.1, .1)
Jet_corr_noReg = TH2D('Jet_corr_noReg', '', 30, 0.8, 1.4, 10, -.1, .1)
nPvs_noReg = TH2D('nPvs_noReg', '', 30 , 0, 25, 10, -.1, .1)
Jet_eta_noReg = TH2D('Jet_eta_noReg', '', 30, -2.4, 2.4, 10, -.1, .1)
Jet_mt_noReg = TH2D('Jet_mt_noReg', '', 30, 0, 225, 10, -.1, .1)
Jet_leadTrackPt_noReg = TH2D('Jet_leadTrackPt_noReg', '', 30, 0, 100, 10, -.1, .1)
Jet_leptonPtRel_noReg = TH2D('Jet_leptonPtRel_noReg', '', 30, 0, 5, 10, -.1, .1)
Jet_leptonPt_noReg = TH2D('Jet_leptonPt_noReg', '', 30, 0, 75, 10, -.1, .1)
Jet_leptonDeltaR_noReg = TH2D('Jet_leptonDeltaR_noReg', '', 30, 0, 0.5, 10, -.1, .1)
Jet_chHEF_noReg = TH2D('Jet_chHEF_noReg', '', 30, 0, 0.5, 10, -.1, .1)
Jet_neHEF_noReg = TH2D('Jet_neHEF_noReg', '', 30 , 0, 0.5, 10, -.1, .1)
Jet_neEmEF_noReg = TH2D('Jet_neEmEF_noReg', '', 30, 0, 1, 10, -.1, .1)
Jet_vtxPt_noReg = TH2D('Jet_vtxPt_noReg', '', 30, 0, 100, 10, -.1, .1)
Jet_vtxMass_noReg = TH2D('Jet_vtxMass_noReg', '', 30, 0, 5, 10, -.1, .1)
Jet_vtx3dL_noReg = TH2D('Jet_vtx3dL_noReg', '', 30, 0, 10, 10, -.1, .1)
Jet_vtxNtrk_noReg = TH2D('Jet_vtxNtrk_noReg', '', 10, 0, 10, 10, -.1, .1)
Jet_vtx3deL_noReg = TH2D('Jet_vtx3deL_noReg', '', 30, 0, 10, 10, -.1, .1)


met_projection_Hpt = TH2D('met_projection_Hpt', '', 50, 20, 300, 25, 0, 1) 

hist_list = [Jet_pt, Jet_corr, nPvs, Jet_eta, Jet_mt, Jet_leadTrackPt, Jet_leptonPtRel, Jet_leptonPt, 
             Jet_leptonDeltaR, Jet_chHEF, Jet_neHEF, Jet_neEmEF, Jet_vtxPt, Jet_vtxMass, Jet_vtx3dL, Jet_vtxNtrk, Jet_vtx3deL             
             ]
                 
hist_list_noReg = [Jet_pt_noReg, Jet_corr_noReg, nPvs_noReg, Jet_eta_noReg, Jet_mt_noReg, Jet_leadTrackPt_noReg, Jet_leptonPtRel_noReg, Jet_leptonPt_noReg,
                   Jet_leptonDeltaR_noReg, Jet_chHEF_noReg, Jet_neHEF_noReg, Jet_neEmEF_noReg, Jet_vtxPt_noReg, Jet_vtxMass_noReg, Jet_vtx3dL_noReg, Jet_vtxNtrk_noReg, 
                   Jet_vtx3deL_noReg
                   ]


extra_hist_list = [met_projection_Hpt]

# ==============================


		
    
#Regression branches
applyRegression = True
newtree.Branch( 'H', H , 'HiggsFlag/I:mass/F:masswithFSR/F:pt/F:ptwithFSR/F:eta/F:phi/F:dR/F:dPhi/F:dEta/F' )
newtree.Branch( 'HNoReg', HNoReg , 'HiggsFlag/I:mass/F:masswithFSR/F:pt/F:eta/F:phi/F:dR/F:dPhi/F:dEta/F' )
newtree.Branch( 'HwithM', HwithM , 'HiggsFlag/I:mass/F:masswithFSR/F:pt/F:eta/F:phi/F:dR/F:dPhi/F:dEta/F' )	
Event = array('f',[0])
rho25 = array('f',[0])
HVMass_Reg = array('f',[0])
newtree.Branch('HVMass_Reg',HVMass_Reg,'HVMass_Reg/F')
fRho25 = ROOT.TTreeFormula("rho",'rho',tree)

# matched genJets
Jet_mcPt = array('f',[0]*2)
Jet_mcPhi = array('f',[0]*2)
Jet_mcEta = array('f',[0]*2)
newtree.Branch('Jet_mcPt',Jet_mcPt,'Jet_mcPt[2]/F')
newtree.Branch('Jet_mcEta',Jet_mcEta,'Jet_mcEta[2]/F')
newtree.Branch('Jet_mcPhi',Jet_mcPhi,'Jet_mcPhi[2]/F')

Jet_MET_dPhiArray = [array('f',[0]),array('f',[0])]
Jet_rawPtArray = [array('f',[0]),array('f',[0])]

Jet_regWeight = array('f',[0]*2)
newtree.Branch('Jet_regWeight',Jet_regWeight,'Jet_regWeight[2]/F')


# For the higgs Jets
hJet_pt_REG = array('f',[0]*2)
newtree.Branch('hJet_pt_REG',hJet_pt_REG,'hJet_pt_REG[2]/F')

hJet_pt = array('f',[0]*2)
newtree.Branch('hJet_pt',hJet_pt,'hJet_pt[2]/F')

readerJet0 = ROOT.TMVA.Reader("!Color:!Silent" )
readerJet1 = ROOT.TMVA.Reader("!Color:!Silent" )

hJ0 = ROOT.TLorentzVector()
hJ1 = ROOT.TLorentzVector()

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
#print theForms	 
    

print tree

for entry in range(0,nEntries):
        

            tree.GetEntry(entry)
	    #Event[0]=tree.evt
            
            if entry % 10000 is 0: print '-----> Event # ', entry
            
            if entry > 100000: break
            
            if tree.nJet < 2: continue
            if tree.nhJCidx != 2: continue

    	    Jet_pt_0 = tree.Jet_pt[tree.hJCidx[0]]
            Jet_pt_1 = tree.Jet_pt[tree.hJCidx[1]]
            Jet_eta_0 = tree.Jet_eta[tree.hJCidx[0]]
            Jet_eta_1 = tree.Jet_eta[tree.hJCidx[1]]
            Jet_m_0 = tree.Jet_mass[tree.hJCidx[0]]
            Jet_m_1 = tree.Jet_mass[tree.hJCidx[1]]
            Jet_phi_0 = tree.Jet_phi[tree.hJCidx[0]]
            Jet_phi_1 = tree.Jet_phi[tree.hJCidx[1]]
            Jet_btagCSV_0 = tree.Jet_btagCSV[tree.hJCidx[0]]
            Jet_btagCSV_1 = tree.Jet_btagCSV[tree.hJCidx[1]]

            #if Jet_pt_0 < 100: continue
            
            # Set the higgs jets
            hJet_pt[0] = Jet_pt_0
            hJet_pt[1] = Jet_pt_1
            
            hJ0.SetPtEtaPhiM(Jet_pt_0,Jet_eta_0,Jet_phi_0,Jet_m_0)
            hJ1.SetPtEtaPhiM(Jet_pt_1,Jet_eta_1,Jet_phi_1,Jet_m_1)

            Jet_e_0 = hJ0.E()
            Jet_e_1 = hJ1.E()
            Jet_mt_0 = hJ0.Mt()
            Jet_mt_1 = hJ1.Mt()
            Jet_met_dPhi_0 =   deltaPhi(tree.met_phi,Jet_phi_0)
            Jet_met_dPhi_1 =   deltaPhi(tree.met_phi,Jet_phi_1)
            
            met_pt_0 = tree.met_pt
            met_pt_1 = tree.met_pt
            
            Jet_met_proj_0 = projectionMETOntoJet(met_pt_0, tree.met_phi,Jet_pt_0, Jet_phi_0)
            Jet_met_proj_1 = projectionMETOntoJet(met_pt_0, tree.met_phi,Jet_pt_1, Jet_phi_1)
            
            met_projection_Hpt.Fill(Jet_pt_0, Jet_met_proj_0)
            
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
            #Jet_mcPt_0 = tree.Jet_mcPt[tree.hJCidx[0]]
            #Jet_mcPt_1 = tree.Jet_mcPt[tree.hJCidx[1]]
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


            # for matched genJets
            minDr0 = 0.4;
            minDr1 = 0.4;
            for m in range(0,tree.nGenJet):

                if tree.GenJet_numBHadrons[m] < 1: continue

                hQ = ROOT.TLorentzVector()
                hQ.SetPtEtaPhiM(tree.GenJet_wNuPt[m], tree.GenJet_wNuEta[m], tree.GenJet_wNuPhi[m], tree.GenJet_wNuM[m]);
                
                if hQ.DeltaR(hJ0)<minDr0 :
                    Jet_mcPt[0] = tree.GenJet_wNuPt[m]
                    Jet_mcEta[0] = tree.GenJet_wNuEta[m]
                    Jet_mcPhi[0] = tree.GenJet_wNuPhi[m]
                    minDr0 = hQ.DeltaR(hJ0)
                    if tree.Jet_btagCSV[tree.hJCidx[0]] > 0:
                        count['num_allMatched_jets'] += 1
                    if tree.Jet_btagCSV[tree.hJCidx[0]] < 0.8:
                        count['num_allMatched_jets_0.46'] += 1
                        

                if hQ.DeltaR(hJ1)< minDr1:
                    Jet_mcPt[1] = tree.GenJet_wNuPt[m]
                    Jet_mcEta[1] = tree.GenJet_wNuEta[m]
                    Jet_mcPhi[1] = tree.GenJet_wNuPhi[m]
                    minDr1 = hQ.DeltaR(hJ1)
                    if tree.Jet_btagCSV[tree.hJCidx[1]] > 0:
                        count['num_allMatched_jets'] += 1
                    if tree.Jet_btagCSV[tree.hJCidx[1]] < 0.8:
                        count['num_allMatched_jets_0.46'] += 1
                    

            #if sample == 'Zuu' or sample == 'Zee':
            #    Jet_corr_0 = Jet_pt_0/Jet_rawPt_0
            #    Jet_corr_1 = Jet_pt_1/Jet_rawPt_1
                
            #else:
            Jet_corr_0 = tree.Jet_corr[tree.hJCidx[0]]
            Jet_corr_1 = tree.Jet_corr[tree.hJCidx[1]]
            
            
            #corrRes0 = corrPt(Jet_pt_0,Jet_eta_0,Jet_mcPt_0)
            #corrRes1 = corrPt(Jet_pt_1,Jet_eta_1,Jet_mcPt_1)
            #Jet_rawPt_0 *= corrRes0
            #Jet_rawPt_1 *= corrRes1
            Jet_rawPtArray[0][0] = Jet_rawPt_0
            Jet_rawPtArray[1][0] = Jet_rawPt_1

	
	    for key in regVars:
                #print key	
                
                if key == 'Jet_chHEF+Jet_neHEF':
                    theVars0[key][0] = eval("Jet_chHEF_0+Jet_neHEF_0")
                    theVars1[key][0] =  eval("Jet_chHEF_1+Jet_neHEF_1")
                    
                else:
                    theVars0[key][0] = eval("%s_0" %(key)) 
                    theVars1[key][0] = eval("%s_1" %(key))


	    if applyRegression:

                
                HNoReg.HiggsFlag = 1
                HNoReg.mass = (hJ0+hJ1).M()
                HNoReg.mass = tree.HCSV_mass
                HNoReg.pt = (hJ0+hJ1).Pt()
                HNoReg.eta = (hJ0+hJ1).Eta()
                HNoReg.phi = (hJ0+hJ1).Phi()
                HNoReg.dR = hJ0.DeltaR(hJ1)
                HNoReg.dPhi = hJ0.DeltaPhi(hJ1)
                HNoReg.dEta = abs(hJ0.Eta()-hJ1.Eta())
	        HNoRegwithFSR = ROOT.TLorentzVector()
                HNoRegwithFSR.SetPtEtaPhiM(HNoReg.pt,HNoReg.eta,HNoReg.phi,HNoReg.mass)
                
                HNoRegwithFSR = addAdditionalJets(HNoRegwithFSR,tree)
		HNoReg.masswithFSR = HNoRegwithFSR.M()
                
                
                Pt0 = max(0.0001,readerJet0.EvaluateRegression( "jet0Regression" )[0])
                Pt1 = max(0.0001,readerJet1.EvaluateRegression( "jet1Regression" )[0])
                
                rPt0 = Jet_pt_0*Pt0
                rPt1 = Jet_pt_1*Pt1
                
                # for built-in regression
                #rPt0 = tree.Jet_pt_reg[tree.hJCidx[0]]
                #rPt1 = tree.Jet_pt_reg[tree.hJCidx[1]]
                
                hJet_pt_REG[0] = Pt0
                hJet_pt_REG[1] = Pt1
                
                
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
		#hJ0.SetPtEtaPhiM(rPt0,Jet_eta_0,Jet_phi_0,4.8)#tree.Jet_mass[0])
                #hJ1.SetPtEtaPhiM(rPt1,Jet_eta_1,Jet_phi_1,4.8)#tree.Jet_mass[1])
                


                '''
                # Store the response in plots during runtime
                genVec = ROOT.TLorentzVector()
                minDr = 0.4
                gen_winner = -999
                for genJet in range(tree.nGenJet):
                #for genQ in range(tree.nGenBQuarkFromH):
                    
                    genVec.SetPtEtaPhiM(tree.GenJet_wNuPt[genJet], tree.GenJet_wNuEta[genJet], tree.GenJet_wNuPhi[genJet], tree.GenJet_wNuM[genJet])
                    #genVec.SetPtEtaPhiM(tree.GenBQuarkFromH_pt[genQ], tree.GenBQuarkFromH_eta[genQ], tree.GenBQuarkFromH_phi[genQ], tree.GenBQuarkFromH_mass[genQ]);
                 
                    if genVec.DeltaR(hJ0) < minDr:
                        minDr = genVec.DeltaR(hJ0)
                        gen_winner = genJet



                #print gen_winner
                # now fill plots for matched genJet/quark
                if gen_winner != -999:
         
                    #gen_pt = tree.GenBQuarkFromH_pt[gen_winner]
                    gen_pt = tree.GenJet_wNuPt[gen_winner]
                
                    Jet_pt.Fill( Pt0, (Pt0 - gen_pt)/gen_pt)
                    Jet_pt_noReg.Fill( Jet_pt_0, (Jet_pt_0 - gen_pt)/gen_pt)
                    
                    Jet_corr.Fill( Jet_corr_0, (Pt0 - gen_pt)/gen_pt)
                    Jet_corr_noReg.Fill( Jet_corr_0, (Jet_pt_0 - gen_pt)/gen_pt)

                    nPvs.Fill(nPVs_0,  (Pt0 - gen_pt)/gen_pt)
                    nPvs_noReg.Fill(nPVs_0, (Jet_pt_0 - gen_pt)/gen_pt)
                     
                    Jet_eta.Fill(Jet_eta_0,  (Pt0 - gen_pt)/gen_pt)
                    Jet_eta_noReg.Fill(Jet_eta_0,  (Jet_pt_0 - gen_pt)/gen_pt)

                    Jet_mt.Fill(Jet_mt_0, (Pt0 - gen_pt)/gen_pt)
                    Jet_mt_noReg.Fill(Jet_mt_0, (Jet_pt_0 - gen_pt)/gen_pt)

                    Jet_leadTrackPt.Fill(Jet_leadTrackPt_0, (Pt0 - gen_pt)/gen_pt)
                    Jet_leadTrackPt_noReg.Fill(Jet_leadTrackPt_0, (Jet_pt_0 - gen_pt)/gen_pt)
                    
                    Jet_leptonPtRel.Fill(Jet_leptonPtRel_0, (Pt0 - gen_pt)/gen_pt)
                    Jet_leptonPtRel_noReg.Fill(Jet_leptonPtRel_0, (Jet_pt_0 - gen_pt)/gen_pt)

                    Jet_leptonPt.Fill(Jet_leptonPt_0, (Pt0 - gen_pt)/gen_pt)
                    Jet_leptonPt_noReg.Fill(Jet_leptonPt_0, (Jet_pt_0 - gen_pt)/gen_pt)

                    Jet_leptonDeltaR.Fill(Jet_leptonDeltaR_0, (Pt0 - gen_pt)/gen_pt)
                    Jet_leptonDeltaR_noReg.Fill(Jet_leptonDeltaR_0, (Jet_pt_0 - gen_pt)/gen_pt)
                    
                    Jet_chHEF.Fill(Jet_chHEF_0, (Pt0 - gen_pt)/gen_pt)
                    Jet_chHEF_noReg.Fill(Jet_chHEF_0, (Jet_pt_0 - gen_pt)/gen_pt)

                    Jet_neHEF.Fill(Jet_neHEF_0, (Pt0 - gen_pt)/gen_pt)
                    Jet_neHEF_noReg.Fill(Jet_neHEF_0, (Jet_pt_0 - gen_pt)/gen_pt)

                    Jet_neEmEF.Fill(Jet_neEmEF_0, (Pt0 - gen_pt)/gen_pt)
                    Jet_neEmEF_noReg.Fill(Jet_neEmEF_0, (Jet_pt_0 - gen_pt)/gen_pt)

                    Jet_vtxPt.Fill(Jet_vtxPt_0, (Pt0 - gen_pt)/gen_pt)
                    Jet_vtxPt_noReg.Fill(Jet_vtxPt_0, (Jet_pt_0 - gen_pt)/gen_pt)

                    Jet_vtxMass.Fill(Jet_vtxMass_0, (Pt0 - gen_pt)/gen_pt)
                    Jet_vtxMass_noReg.Fill(Jet_vtxMass_0, (Jet_pt_0 - gen_pt)/gen_pt)

                    Jet_vtx3dL.Fill(Jet_vtx3dL_0, (Pt0 - gen_pt)/gen_pt , Jet_vtx3dL_0)
                    Jet_vtx3dL_noReg.Fill(Jet_vtx3dL_0, (Jet_pt_0 - gen_pt)/gen_pt , Jet_vtx3dL_0)

                    Jet_vtxNtrk.Fill(Jet_vtxNtrk_0, (Pt0 - gen_pt)/gen_pt)
                    Jet_vtxNtrk_noReg.Fill(Jet_vtxNtrk_0, (Jet_pt_0 - gen_pt)/gen_pt)

                    Jet_vtx3deL.Fill(Jet_vtx3deL_0, (Pt0 - gen_pt)/gen_pt)
                    Jet_vtx3deL_noReg.Fill(Jet_vtx3deL_0, (Jet_pt_0 - gen_pt)/gen_pt)

                    
                '''
    
                # FSR DiJet
		HRegwithFSR = ROOT.TLorentzVector()
                HRegwithFSR.SetPtEtaPhiM(H.pt,H.eta,H.phi,H.mass)
                HRegwithFSR = addAdditionalJets(HRegwithFSR,tree)
		H.masswithFSR = HRegwithFSR.M()
                H.ptwithFSR = HRegwithFSR.Pt()
                
		#HwithM.mass = (hJ0+hJ1).M()
		#print HwithM.mass
                #HwithM.pt = (hJ0+hJ1).Pt()
                #HwithM.eta = (hJ0+hJ1).Eta()
                #HwithM.phi = (hJ0+hJ1).Phi()
                #HwithM.dR = hJ0.DeltaR(hJ1)
                #HwithM.dPhi = hJ0.DeltaPhi(hJ1)
                #HwithM.dEta = abs(hJ0.Eta()-hJ1.Eta())
		#HRegwithMwithFSR = ROOT.TLorentzVector()
                #HRegwithMwithFSR.SetPtEtaPhiM(HwithM.pt,HwithM.eta,HwithM.phi,HwithM.mass)
                
                #HRegwithMwithFSR = addAdditionalJets(HRegwithMwithFSR,tree)
		#H.masswithFSR = HRegwithMwithFSR.M()
                             
                '''
                if (Jet_regWeight[0] > 5. or Jet_regWeight[1] > 5. ) :
                    print 'Event %.0f' %(Event[0])
                    print 'corr 0 %.2f' %(Jet_regWeight[0])
                    print 'corr 1 %.2f' %(Jet_regWeight[1])
                    print 'Pt0 %.2f' %(Pt0)
                    print 'Pt1 %.2f' %(Pt1)
                    print 'rE0 %.2f' %(rE0)
                    print 'rE1 %.2f' %(rE1)
                    print 'Mass %.2f' %(H.mass)
                '''    
            
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
