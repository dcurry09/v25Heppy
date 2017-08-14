###########################################
# Plot Maker for quick plots in Zll channel
#
# by David Curry
#
# 2.25.2015
###########################################

import sys
import os
import re
import fileinput
import subprocess
import numpy as np
from decimal import *
from ROOT import *
from ROOT import gROOT
from matplotlib import interactive
import ROOT



# Get the MVAout file
file = TFile('/exports/uftrig01a/dcurry/heppy/files/btag_MVA_out/v25_ZH125.root')
tree = file.Get('tree')

file_ZZ = TFile('/exports/uftrig01a/dcurry/heppy/files/btag_MVA_out/v25_ZZ_2L2Q_ext1.root')
tree_ZZ = file_ZZ.Get('tree')


ROOT.gSystem.Load('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/interface/VHbbNameSpace_h.so')

tight = '0.9432'
med = '0.4432'
loose = '-0.5884'

btag1 = tight
#btag1 = loose

btag2 = '0.75'
#btag2 = loose


# plot cuts
cut = 'HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v & Vtype_new == 1 & Jet_btagCMVAV2[hJCMVAV2idx[0]] > '+btag1+' & Jet_btagCMVAV2[hJCMVAV2idx[1]] > '+btag2+' & V_new_mass>75. & V_new_mass < 105. & V_new_pt > 150 & Jet_puId[hJCMVAV2idx[0]] >= 4 & Jet_puId[hJCMVAV2idx[1]] >= 4.0 & (((Vtype_new==1) & vLeptons_new_relIso03[0] < 0.15 & vLeptons_new_relIso03[1] < 0.15 & HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v & (abs(vLeptons_new_eta[0]) >= 1.57 || abs(vLeptons_new_eta[0]) <= 1.44) & (abs(vLeptons_new_eta[1])>=1.57 || abs(vLeptons_new_eta[1])<=1.44)) || ((Vtype_new==0) & vLeptons_new_relIso04[0] < 0.25 & vLeptons_new_relIso04[1] < 0.25 & (HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v || HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v || HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v || HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v))) & vLeptons_new_pt[0] > 20 & vLeptons_new_pt[1] > 20 & V_new_pt > -25.0 & Jet_pt_reg[hJCMVAV2idx[0]] > 20. & Jet_pt_reg[hJCMVAV2idx[1]] > 20. & & V_pt < 2000. & H_pt < 999 & H_pt > 0. & H_mass < 9999. & H_mass > 0. & abs(VHbb::deltaPhi(HCMVAV2_reg_phi,V_new_phi))>2.5 & HCMVAV2_reg_mass > 60. & HCMVAV2_reg_mass < 160. & met_pt < 60. & VHbb::deltaR(Jet_eta[hJCMVAV2idx[0]], Jet_phi[hJCMVAV2idx[0]], Jet_eta[hJCMVAV2idx[1]], Jet_phi[hJCMVAV2idx[1]]) < 1.6'

print '\n-----> BDT plot Cut: ', cut

mu_weights  = 'mIdSFWeight[0]*mIsoSFWeight[0]*mTrackerSFWeight[0]*mTrigSFWeight_doubleMu80x[0]*bTagWeightCMVAv2_Moriond[0]*puWeight*Signal_ewkWeight[0]'

ele_weights = 'eId90SFWeight[0]*eTrackerSFWeight[0]*eTrigSFWeight_doubleEle80x[0]*bTagWeightCMVAv2_Moriond[0]*puWeight*Signal_ewkWeight[0]'

#xSec = '0.047182569'
lumi = 35900.00
xsec = 0.047182569
posWeight = file.Get('CountPosWeight')
negWeight = file.Get('CountNegWeight')

theScale = lumi*xsec/(posWeight.GetBinContent(1)-negWeight.GetBinContent(1))

xsec_ZZ = 3.22*0.324904182666
posWeight_ZZ = file_ZZ.Get('CountPosWeight')
negWeight_ZZ = file_ZZ.Get('CountNegWeight')
theScale_ZZ = lumi*xsec_ZZ/(posWeight_ZZ.GetBinContent(1)-negWeight_ZZ.GetBinContent(1))

final_weight = 'sign(genWeight)*('+ele_weights+')'



#final_weight = 0.0005

print '\nFinal Weight:', final_weight
print 'the Scale:', theScale
print 'the Scale ZZ:', theScale_ZZ

drawoption = '(%s)*(%s)'%(final_weight, cut)
drawoption_ZZ = '(%s)*(%s)'%(final_weight, cut+' & Sum$(abs(GenWZQuark_pdgId)==5)>=2')
#drawoption_ZZ = drawoption

print 'Draw Option:', drawoption

# Make the plot
c1 = TCanvas('c1')
s1 = THStack('s1', '')

hTree = TH1F('hTree', '', 10, 60, 160)
hTree_ZZ  = TH1F('hTree_ZZ', '', 10, 60, 160)


tree.Draw('HCMVAV2_reg_mass>>hTree', drawoption,"goff,e")
tree_ZZ.Draw('HCMVAV2_reg_mass>>hTree_ZZ', drawoption_ZZ,"goff,e")

hTree.Scale(theScale)
tree.Project('hSingle', 'HCMVAV2_reg_mass', final_weight+'*('+cut+')')

print '\n\tZH Events Passing Selection:', hTree.GetEntries()*theScale
print '\n\tVVHF Events Passing Selection:', hTree_ZZ.GetEntries()*theScale_ZZ
hTree.Draw()



#tree.Draw('Jet_btagCMVAV2[hJCMVAV2idx[1]]>>hZH_CMVA')
#raw_input('\n\n\t....press return to continue')
#c1.Delete()
#c1 = TCanvas('c1')
#tree_ZZ.Draw('Jet_btagCMVAV2[hJCMVAV2idx[1]]>>hZZ_CMVA')
#raw_input('\n\n\t....press return to continue')
#hZH_CMVA = TH1F('hZH_CMVA', '', 50, -1, 1)
#hZZ_CMVA = TH1F('hZZ_CMVA', '', 50, -1, 1)


raw_input('\n\n\t....press return to continue')
