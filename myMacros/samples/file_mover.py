#! /usr/bin/env python

# ===================================================
# Python script to move files from DAS to servers. Also combines files
#
# Must be on lxplus with voms actiavted!!
#
# 2/15/2015 David Curry
# ===================================================

import sys
import os
import re
import fileinput
import subprocess as sp
import numpy as np
from matplotlib import interactive
import multiprocessing
from ROOT import *


# ====== User Options =======

#channel = 'Zll'
#channel = 'Zvv'
#channel = 'Wlv'

#xrootd_path = '/store/user/arizzi/VHBBHeppyV21/'

#Lucas files
luca_path = '/store/user/perrozzi/VHBBHeppyV24bis/'

# AllPass Eff Signal Samples
SigEff_path = '/store/user/arizzi/VHBBHeppyV21passall/'

#eos_path  = xrootd_path
eos_path = '/store/user/arizzi/VHBBHeppyV25/'

eos_path2 = '/store/user/tboccali/Ntuples_v25/'

eos_path3 = '/store/group/phys_higgs/hbb/ntuples/V25/'

# final combined destination on uftrig
uftrig_path = '/exports/uftrig01a/dcurry/heppy/v25/'

# final path on EOS
#eos_final_path = '/store/user/dcurry/heppy/v24/'

# ===========================

# Define what files to move from DAS to CERN eos
file_list  = []
file_names = []
DY_names   = [] 


# ======== Data =========


# Zuu
'''
file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016B-PromptReco-v2/160910_205020/0000/')
file_names.append('Zuu_B_ext1')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016B-PromptReco-v2/160910_205020/0001/')
file_names.append('Zuu_B_ext2')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016B-PromptReco-v2/160910_205020/0002/')
file_names.append('Zuu_B_ext3')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016B-PromptReco-v2/160910_205020/0003/')
file_names.append('Zuu_B_ext4')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016C-PromptReco-v2/160910_205128/0000/')
file_names.append('Zuu_C_ext1')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016C-PromptReco-v2/160910_205128/0001/')
file_names.append('Zuu_C_ext2')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016D-PromptReco-v2/160910_205212/0000/')
file_names.append('Zuu_D_ext1')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016D-PromptReco-v2/160910_205212/0001/')
file_names.append('Zuu_D_ext2')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016E-PromptReco-v2/160910_205250/0000/')
file_names.append('Zuu_E_ext1')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016E-PromptReco-v2/160910_205250/0001/')
file_names.append('Zuu_E_ext2')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016F-PromptReco-v1/160910_205402/0000/')
file_names.append('Zuu_F_ext1')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016G-PromptReco-v1/160910_205443/0000/')
file_names.append('Zuu_G_ext1')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016G-PromptReco-v1/160910_205443/0001/')
file_names.append('Zuu_G_ext2')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016G-PromptReco-v1/160910_205443/0002/')
file_names.append('Zuu_G_ext3')

# !!! Maybe ignore Zuu_D_ext2 if ext1 merges succesfully!!!!
'''
Zuu_merge_list = ['Zuu_B_ext1', 'Zuu_B_ext2', 'Zuu_B_ext3', 'Zuu_B_ext4', 'Zuu_C_ext1', 'Zuu_C_ext2', 'Zuu_D_ext1', 'Zuu_D_ext2',
                  'Zuu_E_ext1', 'Zuu_E_ext2', 'Zuu_F_ext1', 'Zuu_G_ext1', 'Zuu_G_ext2', 'Zuu_G_ext3'
                  ]


# Zee
'''
file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016B-PromptReco-v2/160910_204523/0000/')
file_names.append('Zee_B_ext1') 

file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016B-PromptReco-v2/160910_204523/0001/')
file_names.append('Zee_B_ext2')

file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016B-PromptReco-v2/160910_204523/0002/')
file_names.append('Zee_B_ext3')

file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016B-PromptReco-v2/160910_204523/0003/')
file_names.append('Zee_B_ext4')
'''
#file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016C-PromptReco-v2/160910_204634/0000/')
#file_names.append('Zee_C_ext1')

#file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016C-PromptReco-v2/160910_204634/0001/')
#file_names.append('Zee_C_ext2')

#file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016D-PromptReco-v2/160910_204714/0000/')
#file_names.append('Zee_D_ext1')

#file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016D-PromptReco-v2/160910_204714/0001/')
#file_names.append('Zee_D_ext2')


#file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016E-PromptReco-v2/160910_204822/0000/')
#file_names.append('Zee_E_ext1')

#file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016E-PromptReco-v2/160910_204822/0001/')
#file_names.append('Zee_E_ext2')
'''
file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016F-PromptReco-v1/160910_204902/0000/')
file_names.append('Zee_F_ext1')


file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016G-PromptReco-v1/160910_204938/0000/')
file_names.append('Zee_G_ext1')

file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016G-PromptReco-v1/160910_204938/0001/')
file_names.append('Zee_G_ext2')

file_list.append(eos_path+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016G-PromptReco-v1/160910_204938/0002/')
file_names.append('Zee_G_ext3')
'''


Zee_merge_list = ['Zee_B_ext1', 'Zee_B_ext2', 'Zee_B_ext3', 'Zee_B_ext4', 'Zee_C_ext1', 'Zee_C_ext2', 'Zee_D_ext1', 'Zee_D_ext2',
                  'Zee_E_ext1', 'Zee_E_ext2', 'Zee_F_ext1', 'Zee_G_ext1', 'Zee_G_ext2', 'Zee_G_ext3'
                  ]




# ==== ZH ====
#file_list.append(eos_path3+'ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V25_ZH_HToBB_ZToNuNu_M125_13TeV_powheg_Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_154431/0000/')
#file_names.append('ZH125')

#file_list.append(eos_path+'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V21bis_ZH_HToBB_ZToLL_M125_13TeV_powheg_Py8__fall15MAv2-pu25ns15v1_76r2as_v12_ext1-v1/160518_230023/000/')
#file_names.append('ZH125_ext1')

#ZH125_merge_list = ['ZH125']


#file_list.append(eos_path3+'ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V25_ggZH_HToBB_ZToLL_M125_13TeV_powheg_Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_154839/0000/')
#file_names.append('ggZH125')

#file_list.append(eos_path+'ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V24_ggZH_HToBB_ZToLL_M125_13TeV_powheg_Py8__spr16MAv2-puspr16_HLT_80r2as_v14_ext1-v1/160909_073813/0000')
#file_names.append('ggZH125_ext1')

#file_list.append(eos_path+'ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V24_ggZH_HToBB_ZToLL_M125_13TeV_powheg_Py8__spr16MAv2-puspr16_HLT_80r2as_v14_ext2-v3/160909_072228/0000')
#file_names.append('ggZH125_ext2')

#ggZH125_merge_list = ['ggZH125', 'ggZH125_ext1', 'ggZH125_ext2']


# For efficiencies
#file_list.append(eos_path+'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V21_passAll_ZH_HToBB_ZToLL_M125_13TeV_powheg_Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160322_112154/0000/')
#file_names.append('ZH125_allPass')

#file_list.append(eos_path+'ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V21_passAll_ggZH_HToBB_ZToLL_M125_13TeV_powheg_Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160322_111010/0000/')
#file_names.append('ggZH125_allPass')


# ==== Drell-Yan ====


#file_list.append(eos_path3+'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v2/170128_125729/0000')
#file_names.append('DY_inclusive')

#file_list.append(eos_path+'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V23_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__spr16MAv2-puspr16_80r2as_2016_MAv2_v0_ext1-v1/160717_081716/0001/')
#file_names.append('DY_inclusive_ext2')

#file_list.append(eos_path+'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21bis_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12_ext1-v1/160518_234314/0002/')
#file_names.append('DY_inclusive_ext3')

#file_list.append(eos_path+'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21bis_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12_ext1-v1/160518_234314/0003/')
#file_names.append('DY_inclusive_ext4')

#file_list.append(eos_path+'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21bis_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12_ext1-v1/160518_234314/0004/')
#file_names.append('DY_inclusive_ext5')

#file_list.append(eos_path+'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21bis_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12_ext1-v1/160518_234314/0005/')
#file_names.append('DY_inclusive_ext6')

#DY_inclusive_merge_list = ['DY_inclusive_ext1','DY_inclusive_ext2']


#file_list.append(eos_path3+'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_125920/0000/')
#file_names.append('DY_100to200_ext1')

#file_list.append(eos_path3+'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_125832/0000/')
#file_names.append('DY_100to200_ext2')
 
DY_100to200_merge_list = ['DY_100to200_ext1','DY_100to200_ext2']


#file_list.append(eos_path3+'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_125549/0000/')
#file_names.append('DY_200to400_ext1')

#file_list.append(eos_path3+'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_125637/0000/')
#file_names.append('DY_200to400_ext2')

DY_200to400_merge_list = ['DY_200to400_ext1','DY_200to400_ext2']



#file_list.append(eos_path3+'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_130054/0000/')
#file_names.append('DY_400to600_ext1')

#file_list.append(eos_path3+'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_130143/0000/')
#file_names.append('DY_400to600_ext2')

DY_400to600_merge_list = ['DY_400to600_ext1','DY_400to600_ext2']



#file_list.append(eos_path3+'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v2/170128_151803/0000/')
#file_names.append('DY_600to800_ext1')

#DY_600toInf_merge_list = ['DY_600toInf_ext1','DY_600toInf_ext2']

#file_list.append(eos_path3+'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_151850/0000/')
#file_names.append('DY_800to1200')

#file_list.append(eos_path3+'DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_151610/0000/')
#file_names.append('DY_1200to2500')

#file_list.append(eos_path3+'DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_151714/0000/')
#file_names.append('DY_2500toInf')


# Dedicated DY Bjet Sample
#file_list.append(eos_path+'DYBJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V24_DYBJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__spr16MAv2-puspr16_80r2as_2016_MAv2_v0-v1/160909_072347/0000/')
#file_names.append('DY_Bjets')

#file_list.append(eos_path+'DYJetsToLL_BGenFilter_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V24_DYJetsToLL_BGenFilter_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__spr16MAv2-puspr16_80r2as_2016_MAv2_v0-v1/160909_071917/0000/')
#file_names.append('DY_BgenFilter')


# NLO DY samples
################################################################################################
#file_list.append(luca_path+'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V24bis_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__spr16MAv2-puspr16_HLT_80r2as_v14-v1/160912_112708/0000/')
#file_names.append('DY_inclusive_nlo')

'''
file_list.append(eos_path+'DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V24_DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__spr16MAv2-puspr16_HLT_80r2as_v14_ext1-v1/160927_125041/0000/')
file_names.append('DY_Pt100to250')

file_list.append(eos_path+'DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V24_DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__spr16MAv2-puspr16_HLT_80r2as_v14_ext1-v1/160927_125124/0000/')
file_names.append('DY_Pt250to400')

file_list.append(eos_path+'DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V24_DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__spr16MAv2-puspr16_HLT_80r2as_v14_ext1-v1/160927_125203/0000/')
file_names.append('DY_Pt400to650')

file_list.append(eos_path+'DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V24_DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__spr16MAv2-puspr16_HLT_80r2as_v14_ext1-v1/160927_125248/0000/')
file_names.append('DY_Pt650toInf')
'''
################################################################################################


'''
# Low HT DY samples
file_list.append(eos_path+'DYJetsToLL_M-5to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/')
file_names.append('DY_5to50_inclusive')

file_list.append(eos_path+'DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21bis_DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160518_234427/0000/')
file_names.append('DY_5to50_100to200')

file_list.append(eos_path+'DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21bis_DYJetsToLL_M-5to50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12_ext1-v1/160518_234506/0000/')
file_names.append('DY_5to50_100to200_ext1')


file_list.append(eos_path+'DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21bis_DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12_ext1-v1/160518_234621/0000/')
file_names.append('DY_5to50_200to400')

file_list.append(eos_path+'DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21bis_DYJetsToLL_M-5to50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12_ext1-v1/160518_234621/0000/')
file_names.append('DY_5to50_200to400_ext1')

file_list.append(eos_path+'DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21bis_DYJetsToLL_M-5to50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160518_234656/0000/')
file_names.append('DY_5to50_400to600')


file_list.append(eos_path+'DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21bis_DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12-v1/160518_234735/0000/')
file_names.append('DY_5to50_600toInf')

file_list.append(eos_path+'DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V21bis_DYJetsToLL_M-5to50_HT-600toInf_TuneCUETP8M1_13TeV-madgraphMLM-Py8__fall15MAv2-pu25ns15v1_76r2as_v12_ext1-v1/160518_234813/0000/')
file_names.append('DY_5to50_600toInf_ext1')
'''

# ==== TTbar ====
#file_list.append(eos_path+'TT_TuneCUETP8M1_13TeV-powheg-pythia8/VHBB_HEPPY_V24_TT_TuneCUETP8M1_13TeV-powheg-Py8__spr16MAv2-puspr16_HLT_80r2as_v14_ext3-v1/160909_063406/0000/')
#file_names.append('ttbar_ext1')

#file_list.append(eos_path+'TT_TuneCUETP8M1_13TeV-powheg-pythia8/VHBB_HEPPY_V24_TT_TuneCUETP8M1_13TeV-powheg-Py8__spr16MAv2-puspr16_HLT_80r2as_v14_ext3-v1/160909_063406/0001/')
#file_names.append('ttbar_ext2')

#file_list.append(eos_path+'TT_TuneCUETP8M1_13TeV-powheg-pythia8/VHBB_HEPPY_V24_TT_TuneCUETP8M1_13TeV-powheg-Py8__spr16MAv2-puspr16_HLT_80r2as_v14_ext3-v1/160909_063406/0002/')
#file_names.append('ttbar_ext3')

#ttbar_merge_list = ['ttbar_ext3']


# ==== Diboson ====

#file_list.append(eos_path2+'ZZ_TuneCUETP8M1_13TeV-pythia8/VHBB_HEPPY_V25_ZZ_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170130_111722/0000/')
#file_names.append('ZZ')

#file_list.append(eos_path2+'WZ_TuneCUETP8M1_13TeV-pythia8/VHBB_HEPPY_V25_WZ_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170130_121302/0000/')
#file_names.append('WZ')

#file_list.append(eos_path+'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/VHBB_HEPPY_V24_ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_Py8__spr16MAv2-puspr16_80r2as_2016_MAv2_v0-v1/160909_070825/0000/')
#file_names.append('ZZ_2L2Q')


# ==== Single Top ===

#file_list.append(eos_path2+'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/VHBB_HEPPY_V25_ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170130_112035/0000/')
#file_names.append('ST_s')


file_list.append(eos_path2+'ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/VHBB_HEPPY_V25_ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170130_115321/0000/')
file_names.append('ST_t_ext1')

#file_list.append(eos_path2+'ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/VHBB_HEPPY_V25_ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170130_115127/0000')
#file_names.append('ST_t_antitop')

#file_list.append(eos_path2+'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/VHBB_HEPPY_V25_ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170130_115710/0000/')
#file_names.append('ST_tW_antitop')

#file_list.append(eos_path2+'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/VHBB_HEPPY_V25_ST_tW_top_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M2T4__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170130_120558/0000/')
#file_names.append('ST_tW_top')



# ==== gJets ====
#file_list.append(eos_path+'/GJets_HT-100to200_Tune4C_13TeV-madgraph-tauola_VHBB_HEPPY_V11_GJets_HT-100to200_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1_150408_090712.root')
 
#file_names.append('gJets_100to200')

#file_list.append(eos_path+'/GJets_HT-200to400_Tune4C_13TeV-madgraph-tauola_VHBB_HEPPY_V11_GJets_HT-200to400_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1_150408_090732.root')

#file_names.append('gJets_200to400')

#file_list.append(eos_path+'/GJets_HT-400to600_Tune4C_13TeV-madgraph-tauola_VHBB_HEPPY_V11_GJets_HT-400to600_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1_150408_090747.root')

#file_names.append('gJets_400to600')

#file_list.append(eos_path+'/GJets_HT-600toInf_Tune4C_13TeV-madgraph-tauola_VHBB_HEPPY_V11_GJets_HT-600toInf_Tune4C_13TeV-madgraph-tauola__Phys14DR-PU20bx25_PHYS14_25_V1-v1_150408_092425.root')

#file_names.append('gJets_600toInf')


# ==== QCD ====
#file_list.append(eos_path+'/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_083753/0000/')

#file_names.append('qcd_1000to1500')

#file_list.append(eos_path+'/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_083609/0000/')

#file_names.append('qcd_100to200')

#file_list.append(eos_path+'/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_093151/0000/')

#file_names.append('qcd_1500to2000')

#file_list.append(eos_path+'/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151024_184123/0000/')

#file_names.append('qcd_2000toInf')

#file_list.append(eos_path+'/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151025_083635/0000/')

#file_names.append('qcd_200to300')

#file_list.append(eos_path+'/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V14_QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8__RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/151026_081050/0000/')

#file_names.append('qcd_300to500')


# =================================================




# FOR xrootd grid
# Use for Multiple files from EOS to uftrig.

# initiate voms
#os.system('voms-proxy-init --voms cms')


isLxplus = False
#isLxplus = True

isUftrig = False
isUftrig = True

eos1_list = []
eos2_list = ['ZZ', 'WZ', 'ST_s', 'ST_t_ext1', 'ST_t_antitop', 'ST_tW_antitop', 'ST_tW_top']
eos3_list = ['ZH125', 'ggZH125', 'DY_inclusive', 'DY_100to200_ext1','DY_100to200_ext2', 'DY_200to400_ext1','DY_200to400_ext2', 'DY_400to600_ext1','DY_400to600_ext2', 'DY_600to800_ext1', 'DY_800to1200', 'DY_1200to2500', 'DY_2500toInf']

def print_fileNames(file):

    index = file_list.index(file)
    name = file_names[index]
    
    temp_name = name+'_hadd.txt'

    temp_dir = uftrig_path+'split_files/'+name+'/'

    #t9 = "ssh dcurry@uftrig01.cern.ch mkdir /exports/uftrig01a/dcurry/heppy/v21/split_files/ZH125"
    #os.system(t9)

    print '\n-----> Copying Files in Directory: ', file
    print '-----> UFtrig Destination: ', temp_dir    

    os.system('rm '+temp_name) 
    
    if name in eos1_list:
        temp_string = "xrdfs stormgf1.pi.infn.it ls -l -u "+file+" | grep tree | awk '{print ""$5""}' >> "+temp_name

    elif name in eos2_list:
        temp_string = "xrdfs stormgf1.pi.infn.it ls -l -u "+file+" | grep tree | awk '{print ""$5""}' >> "+temp_name
        
    elif name in eos3_list:
        temp_string = "xrdfs 188.184.38.46 ls -l -u "+file+" | grep tree | awk '{print ""$5""}' >> "+temp_name

    #print temp_string
    os.system(temp_string)
    

if isLxplus:
    # define the multiprocessing object
    p = multiprocessing.Pool()
    results = p.imap(print_fileNames, file_list)
    p.close()
    p.join()


# for xrootd Grid
def osSystem(file):

    index = file_list.index(file)
    name = file_names[index]

    temp_name = name+'_hadd.txt'
    print temp_name
    temp_dir = uftrig_path+'split_files/'+name+'/'
    print temp_dir

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    input_file = ''
    with open(temp_name) as temp_file:

        for i, line in enumerate(temp_file):

            x = line.replace('\n', ' ')
            
            print '-----> Copying file:', x
            
            #os.system('xrdcp -f '+x+' '+temp_dir)
            

    # Now merge the files
    os.system('rm '+temp_name)
    
    temp_string = "ls "+temp_dir+" | grep root  >> "+temp_name

    os.system(temp_string)
        
    input_file = ''
    
    # for directories with over ~1000 files
    input_file_ext  = ''
    input_file_ext2 = ''

    with open(temp_name) as temp_file:

        for i, line in enumerate(temp_file):
            
            line = temp_dir + line
            
            x = line.replace('\n', ' ')
            
            if 'ttbar' in name:
                #print '\n---> Splitting input files...'
                if i < 350:
                    input_file += x
                if i > 750:
                    input_file_ext += x
                if i < 750 and i > 350:
                    input_file_ext2 += x

            elif 'ST_t_ext1' in name:
                #print '\n---> Splitting input files...'
                if i < 100:
                    input_file += x
                if i >= 100 and i < 200:
                    input_file_ext += x
                if i >= 200:
                    input_file_ext2 += x

            elif '600to800' in name:
                #print '\n---> Splitting input files...'
                if i < 50:
                    input_file += x
                if i >= 50 and 1 < 100:
                    input_file_ext += x
                if i >= 100:
                    input_file_ext2 += x

            else:
                input_file += x
                
                    
    merge = "hadd -f %s %s" % (uftrig_path+name+'.root', input_file)
    
    print '----> Merging Files into', uftrig_path+name+'.root','.  This may take a while....'
    
    os.system(merge)

    if '600to800' in name or 'ttbar' in name or 'ST_t_ext1' in name:
        # Now for really large ttbar files
        merge_ext = "hadd -f %s %s" % (uftrig_path+name+'_NewExt.root', input_file_ext)
        print '----> Merging Files into', uftrig_path+name+'_NewExt.root','.  This may take a while....'
        os.system(merge_ext)
    
        merge_ext2 = "hadd -f %s %s" % (uftrig_path+name+'_NewExt2.root', input_file_ext2)
        print '----> Merging Files into', uftrig_path+name+'_NewExt2.root','.  This may take a while....'
        os.system(merge_ext2)

    print '\n----> Finished Merging: ', uftrig_path+name+'.root'
    

if isUftrig:

    # define the multiprocessing object
    p = multiprocessing.Pool()
    results = p.imap(osSystem, file_list)
    p.close()
    p.join()



# Little more work for datasets from multiple folders

Zuu_merge_list = ['prep_Zuu_B_ext1', 'prep_Zuu_B_ext2', 'prep_Zuu_B_ext3', 'prep_Zuu_B_ext4', 'prep_Zuu_C_ext1', 'prep_Zuu_C_ext2', 'prep_Zuu_D_ext1', 'prep_Zuu_D_ext2',
                  'prep_Zuu_E_ext1', 'prep_Zuu_E_ext2', 'prep_Zuu_F_ext1', 'prep_Zuu_G_ext1', 'prep_Zuu_G_ext2', 'prep_Zuu_G_ext3']

Zee_merge_list = ['prep_Zee_B_ext1', 'prep_Zee_B_ext2', 'prep_Zee_B_ext3', 'prep_Zee_B_ext4', 'prep_Zee_C_ext1', 'prep_Zee_C_ext2', 'prep_Zee_D_ext1', 'prep_Zee_D_ext2',
                  'prep_Zee_E_ext1', 'prep_Zee_E_ext2', 'prep_Zee_F_ext1', 'prep_Zee_G_ext1', 'prep_Zee_G_ext2', 'prep_Zee_G_ext3']

ttbar_merge_list = ['prep_ttbar_ext1', 'prep_ttbar_ext2', 'prep_ttbar_ext3',
                    'prep_ttbar_ext1_NewExt', 'prep_ttbar_ext2_NewExt',
                    'prep_ttbar_ext1_NewExt2', 'prep_ttbar_ext2_NewExt2']

ST_t_merge_list = ['prep_ST_t_ext1', 'prep_ST_t_ext1_NewExt', 'prep_ST_t_ext1_NewExt2']

DY_600to800_merge_list = ['prep_DY_600to800_ext1', 'prep_DY_600to800_ext1_NewExt', 'prep_DY_600to800_ext1_NewExt2']

merge_list = [
    #['Zuu.root', Zuu_merge_list],
    #['Zee.root', Zee_merge_list],
    #['DY_inclusive.root', DY_inclusive_merge_list],
    #['DY_100to200.root', DY_100to200_merge_list], 
    #['DY_200to400.root',DY_200to400_merge_list], 
    #['DY_400to600.root',DY_400to600_merge_list], 
    #['DY_600toInf.root',DY_600toInf_merge_list],
    #['ttbar.root',ttbar_merge_list]
    #['ZH125.root', ZH125_merge_list],
    #['ggZH125.root', ggZH125_merge_list],
    #['ST_t',ST_t_merge_list],
    #['DY_600to800.root', DY_600to800_merge_list],
    ]




#for list in merge_list:
def merge(list):

    outfile_name = list[0]

    input_file = ''

    for sample in list[1]:
        input_file += ' '+uftrig_path+sample+'.root'
        
    merge = "hadd -f %s %s" % (uftrig_path+outfile_name, input_file)
    print '----> Merging Files into', uftrig_path+outfile_name,'.  This may take a while....'
    os.system(merge)

# define the multiprocessing object
p = multiprocessing.Pool()
results = p.imap(merge, merge_list)
p.close()
p.join()


'''
# Zuu
for sample in zuu_names:
    zuu_input_file += ' '+uftrig_path+sample+'.root'

merge = "hadd -f %s %s" % (uftrig_path+'Zuu.root', zuu_input_file)
print '----> Merging Files into', uftrig_path+'Zuu.root','.  This may take a while....'
os.system(merge)

# Zee
zee_input_file = ''
for sample in zee_names:
    zee_input_file += ' '+uftrig_path+sample+'.root'

merge = "hadd -f %s %s" % (uftrig_path+'Zee.root', zee_input_file)
print '----> Merging Files into', uftrig_path+'Zee.root','.  This may take a while....'
os.system(merge)

#DY inclusive
for sample in DY_inclusive_merge_list:
    input_file += ' '+uftrig_path+sample+'.root'

merge = "hadd -f %s %s" % (uftrig_path+'Zuu.root', input_file)
print '----> Merging Files into', uftrig_path+'Zuu.root','.  This may take a while....'
os.system(merge)
'''









'''
# Use for Multiple files from EOS to uftrig.
def osSystem(file):

    index = file_list.index(file)
    name = file_names[index]
    
    temp_name = name+'_hadd.txt'

    os.system('rm '+temp_name) 

    temp_dir = uftrig_path+'split_files/'+name+'/'

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    print '\n-----> Copying Files in Directory: ', file
    print '-----> UFtrig Destination: ', temp_dir    
    

    #temp_string = "/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select ls "+file+" | grep root  >> "+temp_dir

    temp_string = "cmsLs "+file+" | grep root  >> "+temp_name

    print temp_string
    
    os.system(temp_string)
    
    input_file = ''
    with open(temp_name) as temp_file:

        for i, line in enumerate(temp_file):

            x = line.replace('\n', ' ')
            
            print '-----> Copying file:', x
            
            os.system('cmsStage -f '+file+x+' '+temp_dir+x)


    # Now merge the files
    os.system('rm '+temp_name)
    
    temp_string = "ls "+temp_dir+" | grep root  >> "+temp_name

    os.system(temp_string)
        
    input_file = ''
    with open(temp_name) as temp_file:

        for i, line in enumerate(temp_file):
            
            if i < 500: continue
            
            line = temp_dir + line
            
            x = line.replace('\n', ' ')

            input_file += x
        
    merge = "hadd -f %s %s" % (uftrig_path+name+'.root', input_file)
    
    print '----> Merging Files into', uftrig_path+name+'.root','.  This may take a while....'
    
    os.system(merge)
    
    os.system('rm '+temp_name)
    
    # prep the merged file
    #os.system('./runAll.sh '+ name +' 13TeV prep')
    
    # remove the split files
    #os.system('rm -rf '+temp_dir)

# define the multiprocessing object
p = multiprocessing.Pool()
results = p.imap(osSystem, file_list)
p.close()
p.join()
'''





# ==== Use for hadding multiple EOS files on to uftrig
'''
for index, file in enumerate(file_list):

    print '-----> Looping over file path:', file, ' \nand name: ',file_names[index]
    
    os.system('rm hadd')

    print '----> Printing file names/paths to hadd...'

    temp_string = "cmsLs "+file+" | grep root | awk '{print ""$5""}' >> hadd" 
    os.system(temp_string)

    input_file = ''
    with open('hadd') as temp_file:

        for i, line in enumerate(temp_file):

            #if i is 5: break

            line = 'root://eoscms//eos/cms' + line

            x = line.replace('\n', ' ')

            input_file += x


    merge = "hadd -f %s %s" % (uftrig_path+file_names[index]+'.root', input_file)

    print '----> Merging Files into', uftrig_path+file_names[index]+'.root','.  This may take a while....'

    os.system(merge)
'''



# Misc Fucntions
'''
# If using DAS to move oto EOS

# initiate voms
os.system('voms-proxy-init --voms cms')

eos_path = '/store/user/dcurry/heppy/files/sys_out/'

uftrig_path = '/exports/uftrig01a/dcurry/heppy/files/sys_out/'

prefix = 'v24_9_15_'

data_list = ['Zuu', 'Zee']

signal_list = ['ZH125', 'ggZH125']

bkg_list = ['WZ', 'ttbar', 'ZZ_2L2Q']

DY_list = [ 'DY_inclusive', 'DY_100to200', 'DY_200to400', 'DY_400to600', 'DY_600toInf', 'DY_Bjets', 'DY_BgenFilter',
            'DY_inclusive_nlo', 'DY_Pt100to250', 'DY_Pt250to400', 'DY_Pt400to650', 'DY_Pt650toInf'
            ]

ST_list = ['ST_t', 'ST_s', 'ST_tW_top', 'ST_tW_antitop']

#file_list = signal_list + bkg_list + data_list + DY_list + ST_list
file_list = DY_list + ST_list

# xrdcp the files
#for name, file in zip(file_names, file_list):
for name in file_list:

    print '\n-----> Copying file: ', uftrig_path+prefix+name+'.root'
    print '-----> EOS Destination: ', eos_path+prefix+name+'.root\n'

    os.system('xrdcp '+uftrig_path+prefix+name+'.root'+' root://eoscms//eos/cms'+eos_path+prefix+name+'.root')


# Now login into uftrig
#os.system('ssh -Y dcurry@uftrig01.cern.ch')

#os.system('bbar6_heppy && cmsenv')

'''








