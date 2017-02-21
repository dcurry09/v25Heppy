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

eos_path = '/store/user/arizzi/VHBBHeppyV25/'

eos_path2 = '/store/user/tboccali/Ntuples_v25/'

eos_path3 = '/store/group/phys_higgs/hbb/ntuples/V25/'

eos_path4 = '/pnfs/lcg.cscs.ch/cms/trivcat/store/user/jpata/VHBBHeppyV25/'

eos_path5 = '/pnfs/lcg.cscs.ch/cms/trivcat/store/user/perrozzi/VHBBHeppyV25/'

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

######## Double Muon ########
'''
file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016B-23Sep2016-v1/170130_130120/0000/')
file_names.append('Zuu_B_ext1')

file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016B-23Sep2016-v3/170130_130159/0000/')
file_names.append('Zuu_B_ext2')

file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016B-23Sep2016-v3/170130_130159/0001')
file_names.append('Zuu_B_ext3')

#file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V24_DoubleMuon__Run2016B-PromptReco-v2/160910_205020/0003/')
#file_names.append('Zuu_B_ext4')

#file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016C-23Sep2016-v1/170130_130237/0000/')
#file_names.append('Zuu_C_ext1')

#file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V24_DoubleMuon__Run2016C-PromptReco-v2/160910_205128/0001/')
#file_names.append('Zuu_C_ext2')

file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016D-23Sep2016-v1/170130_130315/0000/')
file_names.append('Zuu_D_ext1')

file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016D-23Sep2016-v1/170130_130315/0001/')
file_names.append('Zuu_D_ext2')

file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016E-23Sep2016-v1/170130_130352/0000/')
file_names.append('Zuu_E_ext1')

#file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V24_DoubleMuon__Run2016E-PromptReco-v2/160910_205250/0001/')
#file_names.append('Zuu_E_ext2')

file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016F-23Sep2016-v1/170130_130429/0000/')
file_names.append('Zuu_F_ext1')

file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016G-23Sep2016-v1/170130_130511/0000/')
file_names.append('Zuu_G_ext1')

file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016G-23Sep2016-v1/170130_130511/0001/')
file_names.append('Zuu_G_ext2')

#file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V24_DoubleMuon__Run2016G-PromptReco-v1/160910_205443/0002/')
#file_names.append('Zuu_G_ext3')

file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016H-PromptReco-v1/170130_130549/0000/')
file_names.append('Zuu_H_ext1')

file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016H-PromptReco-v3/170130_130708/0000/')
file_names.append('Zuu_H_ext2')
'''

#file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016H-PromptReco-v2/170130_130628/0000/')
#file_names.append('Zuu_H_ext3')

#file_list.append(eos_path4+'DoubleMuon/VHBB_HEPPY_V25_DoubleMuon__Run2016H-PromptReco-v2/170130_130628/0001/')
#file_names.append('Zuu_H_ext4')

##############################

######### Single Muon ########
'''
file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016B-23Sep2016-v1/170130_115425/0000/')
file_names.append('Zuu_B_ext1')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016B-23Sep2016-v3/170130_115523/0000/')
file_names.append('Zuu_B_ext2')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016B-23Sep2016-v3/170130_115523/0001/')
file_names.append('Zuu_B_ext3')

#file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016B-PromptReco-v2/160910_205020/0003/')
#file_names.append('Zuu_B_ext4')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016C-23Sep2016-v1/170130_115611/0000/')
file_names.append('Zuu_C_ext1')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016C-23Sep2016-v1/170205_165447/0000/')
file_names.append('Zuu_C_ext2')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016C-23Sep2016-v1/170206_075442/0000/')
file_names.append('Zuu_C_ext3')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016D-23Sep2016-v1/170130_115700/0000/')
file_names.append('Zuu_D_ext1')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016D-23Sep2016-v1/170130_115700/0001/')
file_names.append('Zuu_D_ext2')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016E-23Sep2016-v1/170130_115749/0000/')
file_names.append('Zuu_E_ext1')

#file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016E-PromptReco-v2/160910_205250/0001/')
#file_names.append('Zuu_E_ext2')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016F-23Sep2016-v1/170130_115838/0000/')
file_names.append('Zuu_F_ext1')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016G-23Sep2016-v1/170130_115926/0000/')
file_names.append('Zuu_G_ext1')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016G-23Sep2016-v1/170130_115926/0001/')
file_names.append('Zuu_G_ext2')

#file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V24_SingleMuon__Run2016G-PromptReco-v1/160910_205443/0002/')
#file_names.append('Zuu_G_ext3')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016H-PromptReco-v2/170130_120108/0000/')
file_names.append('Zuu_H_ext1')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016H-PromptReco-v2/170130_120108/0001/')
file_names.append('Zuu_H_ext2')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016H-PromptReco-v1/170130_120015/0000/')
file_names.append('Zuu_H_ext3')

file_list.append(eos_path+'SingleMuon/VHBB_HEPPY_V25_SingleMuon__Run2016H-PromptReco-v3/170130_120157/0000/')
file_names.append('Zuu_H_ext4')
'''
#############################


######### Double Zee ########

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016B-23Sep2016-v2/170130_125400/0000/')
#file_names.append('Zee_B_ext1') 

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016B-23Sep2016-v3/170130_125457/0000/')
#file_names.append('Zee_B_ext2')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016B-23Sep2016-v3/170130_125457/0001/')
#file_names.append('Zee_B_ext3')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V24_SingleElectron__Run2016B-PromptReco-v2/160910_204523/0003/')
#file_names.append('Zee_B_ext4')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016C-23Sep2016-v1/170130_125536/0000/')
#file_names.append('Zee_C_ext1')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V24_SingleElectron__Run2016C-PromptReco-v2/160910_204634/0001/')
#file_names.append('Zee_C_ext2')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016D-23Sep2016-v1/170130_125620/0000/')
#file_names.append('Zee_D_ext1')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016D-23Sep2016-v1/170130_125620/0001/')
#file_names.append('Zee_D_ext2')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016E-23Sep2016-v1/170130_125701/0000/')
#file_names.append('Zee_E_ext1')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V24_SingleElectron__Run2016E-PromptReco-v2/160910_204822/0001/')
#file_names.append('Zee_E_ext2')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016F-23Sep2016-v1/170130_125743/0000/')
#file_names.append('Zee_F_ext1')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016G-23Sep2016-v1/170130_125824/0000/')
#file_names.append('Zee_G_ext1')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016G-23Sep2016-v1/170130_125824/0001/')
#file_names.append('Zee_G_ext2')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016G-23Sep2016-v1/170210_153735/0000/')
#file_names.append('Zee_G_ext3')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016G-23Sep2016-v1/170210_153735/0001/')
#file_names.append('Zee_G_ext4')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016H-PromptReco-v1/170130_125909/0000/')
#file_names.append('Zee_H_ext1')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016H-PromptReco-v3/170130_130041/0000/')
#file_names.append('Zee_H_ext2')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016H-PromptReco-v2/170130_125954/0000/')
#file_names.append('Zee_H_ext3')

#file_list.append(eos_path4+'DoubleEG/VHBB_HEPPY_V25_DoubleEG__Run2016H-PromptReco-v2/170130_125954/0001/')
#file_names.append('Zee_H_ext4')


###################################

######## Single Ele ###############
'''
file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016B-23Sep2016-v2/170130_140232/0000/')
file_names.append('Zee_B_ext1') 

file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016B-23Sep2016-v3/170130_140355/0000/')
file_names.append('Zee_B_ext2')

file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016B-23Sep2016-v3/170130_140355/0001/')
file_names.append('Zee_B_ext3')

#file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016B-PromptReco-v2/160910_204523/0003/')
#file_names.append('Zee_B_ext4')

file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016C-23Sep2016-v1/170130_140552/0000/')
file_names.append('Zee_C_ext1')

#file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016C-PromptReco-v2/160910_204634/0001/')
#file_names.append('Zee_C_ext2')

file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016D-23Sep2016-v1/170130_140740/0000/')
file_names.append('Zee_D_ext1')

file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016D-23Sep2016-v1/170130_140740/0001/')
file_names.append('Zee_D_ext2')

file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016E-23Sep2016-v1/170130_141059/0000/')
file_names.append('Zee_E_ext1')

#file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016E-PromptReco-v2/160910_204822/0001/')
#file_names.append('Zee_E_ext2')

file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016F-23Sep2016-v1/170130_141324/0000/')
file_names.append('Zee_F_ext1')

file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016G-23Sep2016-v1/170130_141517/0000/')
file_names.append('Zee_G_ext1')

file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016G-23Sep2016-v1/170130_141517/0001/')
file_names.append('Zee_G_ext2')

#file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V24_SingleElectron__Run2016G-PromptReco-v1/160910_204938/0002/')
#file_names.append('Zee_G_ext3')

file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016H-PromptReco-v1/170130_141632/0000/')
file_names.append('Zee_H_ext1')

file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016H-PromptReco-v3/170130_141941/0000/')
file_names.append('Zee_H_ext2')

file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016H-PromptReco-v2/170130_141828/0000/')
file_names.append('Zee_H_ext3')

file_list.append(eos_path5+'SingleElectron/VHBB_HEPPY_V25_SingleElectron__Run2016H-PromptReco-v2/170130_141828/0001/')
file_names.append('Zee_H_ext4')
'''
################################################




# ==== ZH ====

'''
#file_list.append(eos_path3+'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V25_ZH_HToBB_ZToLL_M125_13TeV_powheg_Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_125104/0000/')
#file_names.append('ZH125_ext1')

#file_list.append(eos_path3+'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V25_ZH_HToBB_ZToLL_M125_13TeV_powheg_Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_125152/0000/')
#file_names.append('ZH125_ext2')

ZH125_merge_list = ['ZH125_ext1', 'ZH125_ext2']


file_list.append(eos_path3+'ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/VHBB_HEPPY_V25_ggZH_HToBB_ZToLL_M125_13TeV_powheg_Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_154839/0000/')
file_names.append('ggZH125')


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
file_list.append(eos_path3+'DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v2/170128_125729/0000')
file_names.append('DY_inclusive')

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

file_list.append(eos_path3+'DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_130358/0000/')
file_names.append('DY_70to100')

#DY_70to100_merge_list = ['DY_70to100']

file_list.append(eos_path3+'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_125920/0000/')
file_names.append('DY_100to200_ext1')

file_list.append(eos_path3+'DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_125832/0000/')
file_names.append('DY_100to200_ext2')
 
DY_100to200_merge_list = ['DY_100to200_ext1','DY_100to200_ext2']


file_list.append(eos_path3+'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_125549/0000/')
file_names.append('DY_200to400_ext1')

file_list.append(eos_path3+'DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_125637/0000/')
file_names.append('DY_200to400_ext2')

DY_200to400_merge_list = ['DY_200to400_ext1','DY_200to400_ext2']

file_list.append(eos_path3+'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_130054/0000/')
file_names.append('DY_400to600_ext1')

file_list.append(eos_path3+'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_130143/0000/')
file_names.append('DY_400to600_ext2')

DY_400to600_merge_list = ['DY_400to600_ext1','DY_400to600_ext2']

file_list.append(eos_path3+'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v2/170128_151803/0000/')
file_names.append('DY_600to800_ext1')

file_list.append(eos_path3+'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_151850/0000/')
file_names.append('DY_800to1200_ext1')

file_list.append(eos_path3+'DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_151610/0000/')
file_names.append('DY_1200to2500')

file_list.append(eos_path3+'DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_151714/0000/')
file_names.append('DY_2500toInf')


# Dedicated DY Bjet Sample
file_list.append(eos_path3+'DYBJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYBJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_153101/0000/')
file_names.append('DY_Bjets')

file_list.append(eos_path3+'DYJetsToLL_BGenFilter_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/VHBB_HEPPY_V25_DYJetsToLL_BGenFilter_M-50_TuneCUETP8M1_13TeV-madgraphMLM-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_153211/0000/')
file_names.append('DY_BgenFilter')
'''

##### NLO samples #####
#file_list.append(eos_path3+'DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYJetsToLL_Pt-50To100_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v3/170128_130507/0000/')
#file_names.append('DY_Pt50to100')

#file_list.append(eos_path3+'DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v2/170128_130853/0000/')
#file_names.append('DY_Pt100to250_ext1')

# file_list.append(eos_path3+'DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYJetsToLL_Pt-100To250_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_151938/0000/')
# file_names.append('DY_Pt100to250_ext1')

# file_list.append(eos_path3+'DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_152134/0000/')
# file_names.append('DY_Pt250to400_ext1')

# file_list.append(eos_path3+'DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_152225/0000/')
# file_names.append('DY_Pt250to400_ext2')

# file_list.append(eos_path3+'DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYJetsToLL_Pt-250To400_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext2-v1/170128_152314/0000/')
# file_names.append('DY_Pt250to400_ext3')

# file_list.append(eos_path3+'DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_152416/0000/')
# file_names.append('DY_Pt400to650_ext1')

# file_list.append(eos_path3+'DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_152506/0000/')
# file_names.append('DY_Pt400to650_ext2')

# file_list.append(eos_path3+'DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext2-v1/170128_152637/0000/')
# file_names.append('DY_Pt400to650_ext3')

# file_list.append(eos_path3+'DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170128_152725/0000/')
# file_names.append('DY_Pt650toInf_ext1')

# file_list.append(eos_path3+'DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_152819/0000/')
# file_names.append('DY_Pt650toInf_ext2')

#file_list.append(eos_path3+'DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYJetsToLL_Pt-650ToInf_TuneCUETP8M1_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext2-v1/170128_152940/0000/')
#file_names.append('DY_Pt650toInf_ext3')

#file_list.append(eos_path3+'DYToLL_0J_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYToLL_0J_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170128_130942/0000/')
#file_names.append('DY_0J')

#file_list.append(eos_path3+'DYToLL_1J_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25/170206_153522/0000/')
#file_names.append('DY_1J_ext1')

#file_list.append(eos_path3+'DYToLL_1J_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25/170206_153522/0001/')
#file_names.append('DY_1J_ext2')

file_list.append(eos_path3+'DYToLL_2J_13TeV-amcatnloFXFX-pythia8/VHBB_HEPPY_V25_DYToLL_2J_13TeV-amcatnloFXFX-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v2/170128_151520/0000/')
file_names.append('DY_2J')

#####################

'''
# ==== TTbar ====

file_list.append(eos_path3+'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/VHBB_HEPPY_V25_TT_TuneCUETP8M2T4_13TeV-powheg-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170202_212737/0000/')
file_names.append('ttbar_ext1')

file_list.append(eos_path3+'TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/VHBB_HEPPY_V25_TT_TuneCUETP8M2T4_13TeV-powheg-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170202_212737/0001/')
file_names.append('ttbar_ext2')

#file_list.append(eos_path+'TT_TuneCUETP8M1_13TeV-powheg-pythia8/VHBB_HEPPY_V24_TT_TuneCUETP8M1_13TeV-powheg-Py8__spr16MAv2-puspr16_HLT_80r2as_v14_ext3-v1/160909_063406/0002/')
#file_names.append('ttbar_ext3')

#ttbar_merge_list = ['ttbar_ext3']


# ==== Diboson ====

file_list.append(eos_path2+'ZZ_TuneCUETP8M1_13TeV-pythia8/VHBB_HEPPY_V25_ZZ_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170130_111722/0000/')
file_names.append('ZZ')

file_list.append(eos_path2+'WZ_TuneCUETP8M1_13TeV-pythia8/VHBB_HEPPY_V25_WZ_TuneCUETP8M1_13TeV-Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170130_121302/0000/')
file_names.append('WZ')

file_list.append(eos_path2+'ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_pythia8/VHBB_HEPPY_V25_ZZTo2L2Q_13TeV_amcatnloFXFX_madspin_Py8__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170130_140220/0000/')
file_names.append('ZZ_2L2Q')


# ==== Single Top ===

file_list.append(eos_path2+'ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/VHBB_HEPPY_V25_ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170130_112035/0000/')
file_names.append('ST_s')

#file_list.append(eos_path2+'ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/VHBB_HEPPY_V25_ST_t-channel_top_4f_inclusiveDecays_13TeV-powhegV2-madspin-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170130_115321/0000/')
#file_names.append('ST_t_ext1')

#file_list.append(eos_path2+'ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/VHBB_HEPPY_V25_ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170130_115127/0000')
#file_names.append('ST_t_antitop')

file_list.append(eos_path2+'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/VHBB_HEPPY_V25_ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M1__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6_ext1-v1/170130_115710/0000/')
file_names.append('ST_tW_antitop')

file_list.append(eos_path2+'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M2T4/VHBB_HEPPY_V25_ST_tW_top_5f_inclusiveDecays_13TeV-powheg-Py8_TuneCUETP8M2T4__RunIISummer16MAv2-PUMoriond17_80r2as_2016_TrancheIV_v6-v1/170130_120558/0000/')
file_names.append('ST_tW_top')
'''

# =================================================

# FOR xrootd grid
# Use for Multiple files from EOS to uftrig.

# initiate voms
#os.system('voms-proxy-init --voms cms')

isLxplus = False
#isLxplus = True

isUftrig = False
#isUftrig = True


eos2_list = ['ZZ', 'WZ', 'ST_s', 'ST_t_ext1', 'ST_t_antitop', 'ST_tW_antitop', 'ST_tW_top', 'ZZ_2L2Q']
eos3_list = ['ZH125_ext1', 'ZH125_ext2', 'ggZH125', 'DY_inclusive', 'DY_100to200_ext1','DY_100to200_ext2', 'DY_200to400_ext1','DY_200to400_ext2', 'DY_400to600_ext1','DY_400to600_ext2', 'DY_600to800_ext1', 'DY_800to1200_ext1', 'DY_1200to2500', 'DY_2500toInf', 'ttbar_ext1', 'ttbar_ext2' ,'DY_Bjets', 'DY_BgenFilter', 'DY_70to100',
             'DY_Pt100to250_ext1', 'DY_Pt100to250_ext2', 'DY_Pt50to100',
             'DY_Pt250to400_ext1', 'DY_Pt250to400_ext2','DY_Pt250to400_ext3',
             'DY_Pt400to650_ext1', 'DY_Pt400to650_ext2','DY_Pt400to650_ext3',
             'DY_Pt650toInf_ext1', 'DY_Pt650toInf_ext2', 'DY_Pt650toInf_ext3',
             'DY_0J', 'DY_1J_ext1', 'DY_1J_ext2', 'DY_2J'
             ]

eos4_list = ['Zee_B_ext1', 'Zee_B_ext2', 'Zee_B_ext3', #'Zee_B_ext4',
             'Zee_C_ext1', #'Zee_C_ext2',
             'Zee_D_ext1', 'Zee_D_ext2',
             'Zee_E_ext1', #'Zee_E_ext2',
             'Zee_F_ext1',
             'Zee_G_ext1', 'Zee_G_ext2', 'Zee_G_ext3', 'Zee_G_ext4',
             'Zee_H_ext1', 'Zee_H_ext2', 'Zee_H_ext3', 'Zee_H_ext4',
             
             'Zuu_B_ext1', 'Zuu_B_ext2', 'Zuu_B_ext3', #'Zuu_B_ext4',
             'Zuu_C_ext1', 'Zuu_C_ext2', 'Zuu_C_ext3',
             'Zuu_D_ext1', 'Zuu_D_ext2',
             'Zuu_E_ext1', #'Zuu_E_ext2',
             'Zuu_F_ext1',
             'Zuu_G_ext1', 'Zuu_G_ext2', #'Zuu_G_ext3'
             'Zuu_H_ext1', 'Zuu_H_ext2', 'Zuu_H_ext3', 'Zuu_H_ext4'
             ]

eos_list = []



def print_fileNames(file):

    index = file_list.index(file)
    name = file_names[index]

    print name
    
    temp_name = name+'_hadd.txt'

    temp_dir = uftrig_path+'split_files/'+name+'/'

    print '\n-----> Copying Files in Directory: ', file
    print '-----> UFtrig Destination: ', temp_dir    

    os.system('rm '+temp_name) 
    
    #if name in eos1_list:
    #temp_string = "xrdfs stormgf1.pi.infn.it ls -l -u "+file+" | grep tree | awk '{print ""$5""}' >> "+temp_name

    if name in eos2_list or name in eos_list:
        temp_string = "xrdfs stormgf1.pi.infn.it ls -l -u "+file+" | grep tree | awk '{print ""$5""}' >> "+temp_name
        
    elif name in eos3_list:
        temp_string = "xrdfs 188.184.38.46 ls -l -u "+file+" | grep tree | awk '{print ""$5""}' >> "+temp_name

    elif name in eos4_list:
        temp_string = "xrdfs storage01.lcg.cscs.ch ls -l -u "+file+" | grep tree | awk '{print ""$5""}' >> "+temp_name
        
    print temp_string
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
            
            os.system('xrdcp -f '+x+' '+temp_dir)
            

    # Now merge the files
    os.system('rm '+temp_name)
    
    temp_string = "ls "+temp_dir+" | grep root  >> "+temp_name

    os.system(temp_string)
        
    input_file = ''
    
    # for directories with over ~1000 files
    input_file_ext  = ''
    input_file_ext2 = ''
    input_file_ext3 = ''
    input_file_ext4 = ''
    input_file_ext5 = ''
    input_file_ext6 = ''
    input_file_ext7 = ''
    input_file_ext8 = ''
    input_file_ext9 = ''
    input_file_ext10 = ''

    with open(temp_name) as temp_file:

        for i, line in enumerate(temp_file):
            
            line = temp_dir + line
            
            x = line.replace('\n', ' ')
            
            if 'ttbar' in name or 'DY_2J' in name:
                print '\n---> Splitting input files...'
                if i < 100:
                    input_file += x
                if i >= 100 and i < 200:
                    input_file_ext += x
                if i < 300 and i >= 200:
                    input_file_ext2 += x
                if i >= 300  and i < 400:
                    input_file_ext3 += x
                if i >= 400  and i < 500:
                    input_file_ext4 += x
                if i >= 500 and i < 600:
                    input_file_ext5 += x
                if i >= 600 and i < 700:
                    input_file_ext6 += x
                if i >= 700 and i < 800:
                    input_file_ext7 += x
                if i >= 800 and i < 900:
                    input_file_ext8 += x
                if i >= 900:
                    input_file_ext9 += x
                

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
                if i >= 50 and i < 100:
                    input_file_ext += x
                if i >= 100:
                    input_file_ext2 += x

            else:
                input_file += x
                
                    
    merge = "hadd -f %s %s" % (uftrig_path+name+'.root', input_file)
    
    print '----> Merging Files into', uftrig_path+name+'.root','.  This may take a while....'
    
    os.system(merge)
    
    if '600to800' in name or 'ttbar' in name or 'ST_t_ext1' in name or 'DY_2J' in name:
        # Now for really large ttbar files
        merge_ext = "hadd -f %s %s" % (uftrig_path+name+'_NewExt1.root', input_file_ext)
        print '----> Merging Files into', uftrig_path+name+'_NewExt1.root','.  This may take a while....'
        os.system(merge_ext)
    
        merge_ext2 = "hadd -f %s %s" % (uftrig_path+name+'_NewExt2.root', input_file_ext2)
        print '----> Merging Files into', uftrig_path+name+'_NewExt2.root','.  This may take a while....'
        os.system(merge_ext2)

        merge_ext3 = "hadd -f %s %s" % (uftrig_path+name+'_NewExt3.root', input_file_ext3)
        print '----> Merging Files into', uftrig_path+name+'_NewExt3.root','.  This may take a while....'
        os.system(merge_ext3)

        merge_ext4 = "hadd -f %s %s" % (uftrig_path+name+'_NewExt4.root', input_file_ext4)
        print '----> Merging Files into', uftrig_path+name+'_NewExt4.root','.  This may take a while....'
        os.system(merge_ext4)

        merge_ext5 = "hadd -f %s %s" % (uftrig_path+name+'_NewExt5.root', input_file_ext5)
        print '----> Merging Files into', uftrig_path+name+'_NewExt5.root','.  This may take a while....'
        os.system(merge_ext5)

        merge_ext6 = "hadd -f %s %s" % (uftrig_path+name+'_NewExt6.root', input_file_ext6)
        print '----> Merging Files into', uftrig_path+name+'_NewExt6.root','.  This may take a while....'
        os.system(merge_ext6)

        merge_ext7 = "hadd -f %s %s" % (uftrig_path+name+'_NewExt7.root', input_file_ext7)
        print '----> Merging Files into', uftrig_path+name+'_NewExt7.root','.  This may take a while....'
        os.system(merge_ext7)

        merge_ext8 = "hadd -f %s %s" % (uftrig_path+name+'_NewExt8.root', input_file_ext8)
        print '----> Merging Files into', uftrig_path+name+'_NewExt8.root','.  This may take a while....'
        os.system(merge_ext8)

        merge_ext9 = "hadd -f %s %s" % (uftrig_path+name+'_NewExt9.root', input_file_ext9)
        print '----> Merging Files into', uftrig_path+name+'_NewExt9.root','.  This may take a while....'
        os.system(merge_ext9)
        

    print '\n----> Finished Merging: ', uftrig_path+name+'.root'

    #if 'Zee_B_ext1' not in name: os.system("rm -r "+temp_dir)
    
    
if isUftrig:

    # define the multiprocessing object
    p = multiprocessing.Pool()
    results = p.imap(osSystem, file_list)
    p.close()
    p.join()



# Little more work for datasets from multiple folders

Zuu_merge_list = ['prep_Zuu_B_ext1', 'prep_Zuu_B_ext2', 'prep_Zuu_B_ext3', #'prep_Zuu_B_ext4', 
                  'prep_Zuu_C_ext1', #'prep_Zuu_C_ext2', 
                  'prep_Zuu_D_ext1', 'prep_Zuu_D_ext2',
                  'prep_Zuu_E_ext1', #'prep_Zuu_E_ext2', 
                  'prep_Zuu_F_ext1', 
                  'prep_Zuu_G_ext1', 'prep_Zuu_G_ext2', #'prep_Zuu_G_ext3',
                  'prep_Zuu_H_ext1', 'prep_Zuu_H_ext2', 'prep_Zuu_H_ext3', 'prep_Zuu_H_ext4']

Zee_merge_list = ['prep_Zee_B_ext1', 'prep_Zee_B_ext2', 'prep_Zee_B_ext3', #'prep_Zee_B_ext4',
                  'prep_Zee_C_ext1', #'prep_Zee_C_ext2',
                  'prep_Zee_D_ext1', 'prep_Zee_D_ext2',
                  'prep_Zee_E_ext1', #'prep_Zee_E_ext2',
                  'prep_Zee_F_ext1',
                  'prep_Zee_G_ext1', 'prep_Zee_G_ext2', 'prep_Zee_G_ext3', 'prep_Zee_G_ext4',
                  'prep_Zee_H_ext1', 'prep_Zee_H_ext2', 'prep_Zee_H_ext3', 'prep_Zee_H_ext4']
                  

ttbar_merge_list = ['prep_ttbar_ext1', 'prep_ttbar_ext2',
                    'prep_ttbar_ext1_NewExt', 'prep_ttbar_ext2_NewExt',
                    'prep_ttbar_ext1_NewExt2', 'prep_ttbar_ext2_NewExt2',
                    'prep_ttbar_ext1_NewExt3', 'prep_ttbar_ext2_NewExt3',
                    'prep_ttbar_ext1_NewExt4', 'prep_ttbar_ext2_NewExt4'
                    #'prep_ttbar_ext1_NewExt5', 'prep_ttbar_ext2_NewExt5',
                    ]



ST_t_merge_list = ['prep_ST_t_ext1', 'prep_ST_t_ext1_NewExt', 'prep_ST_t_ext1_NewExt2']

DY_600to800_merge_list = ['prep_DY_600to800_ext1', 'prep_DY_600to800_ext1_NewExt', 'prep_DY_600to800_ext1_NewExt2']

DY_100to200_merge_list = ['DY_100to200_ext1', 'DY_100to200_ext2']

DY_200to400_merge_list = ['DY_200to400_ext1', 'DY_200to400_ext2']

DY_400to600_merge_list = ['DY_400to600_ext1', 'DY_400to600_ext2']

ZH125_merge_list = ['ZH125_ext1', 'ZH125_ext2']

DY_Pt100to250_list = ['DY_Pt100to250_ext1']

DY_Pt250to400_list = ['DY_Pt250to400_ext1', 'DY_Pt250to400_ext2','DY_Pt250to400_ext3']

DY_Pt400to650_list = ['DY_Pt400to650_ext1', 'DY_Pt400to650_ext2','DY_Pt400to650_ext3']

DY_Pt650toInf_list = ['DY_Pt650toInf_ext1', 'DY_Pt650toInf_ext1', 'DY_Pt650toInf_ext3']

DY_1J_list = ['DY_1J_ext1', 'DY_1J_ext2']

#DY_2J_list = ['prep_DY_2J', 'prep_DY_2J_NewExt2', 'prep_DY_2J_NewExt3', 'prep_DY_2J_NewExt4', 'prep_DY_2J_NewExt5']

DY_2J_ext1_list = ['prep_DY_2J', 'prep_DY_2J_NewExt1']

DY_2J_ext2_list = ['prep_DY_2J_NewExt2', 'prep_DY_2J_NewExt3']

DY_2J_ext3_list = ['prep_DY_2J_NewExt4', 'prep_DY_2J_NewExt5']

DY_2J_ext4_list = ['prep_DY_2J_NewExt6', 'prep_DY_2J_NewExt7', 'prep_DY_2J_NewExt8']

#DY_2J_ext5_list = ['prep_DY_2J_NewExt8', 'prep_DY_2J_NewExt9']






merge_list = [
    #['Zuu.root', Zuu_merge_list],
    #['Zee.root', Zee_merge_list]
    #['DY_inclusive.root', DY_inclusive_merge_list],
    #['DY_100to200.root',DY_100to200_merge_list], 
    #['DY_200to400.root',DY_200to400_merge_list], 
    #['DY_400to600.root',DY_400to600_merge_list], 
    #['DY_600to800.root',DY_600to800_merge_list],
    #['ttbar.root',ttbar_merge_list]
    #['ZH125.root',ZH125_merge_list],
    #['ggZH125.root', ggZH125_merge_list],
    #['ST_t',ST_t_merge_list],
    #['DY_Pt100to250.root',DY_Pt100to250_list],
    #['DY_Pt250to400.root',DY_Pt250to400_list],
    #['DY_Pt400to650.root',DY_Pt400to650_list],
    #['DY_Pt650toInf.root',DY_Pt650toInf_list]
    #['DY1J.root',DY_1J_list],
    ['DY2J_ext1.root',DY_2J_ext1_list],
    ['DY2J_ext2.root',DY_2J_ext2_list],
    ['DY2J_ext3.root',DY_2J_ext3_list],
    ['DY2J_ext4.root',DY_2J_ext4_list]
    ]




#for list in merge_list:
def merge(list):

    outfile_name = list[0]

    input_file = ''

    for sample in list[1]:
        #input_file += ' '+uftrig_path+sample+'.root'
        input_file += ' /exports/uftrig01a/dcurry/heppy/files/btag_out/'+sample+'.root'

    #merge = "hadd -f %s %s" % (uftrig_path+outfile_name, input_file)
    merge = "hadd -f %s %s" % ('/exports/uftrig01a/dcurry/heppy/files/btag_out/v25_'+outfile_name, input_file)
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








