# Plot Maker for quick Profile plots in ttbar CR
#
# by David Curry
#
# 7.22.1014
###########################################

import sys
import os
import re
from ROOT import *
from matplotlib import interactive
from ROOT import gROOT
import ConfigParser


# ===== Get the weights and SF for ttbar =====
Config = ConfigParser.ConfigParser()
Config.read('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/python/13TeVconfig/general')
weightF = Config.get('Weights', 'weightF')
Config.read('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/python/13TeVconfig/samples.ini')
SF = 1.184
lumi = 2320.00
xSec = 831.76
# ==================================


# Where to save
outdir = 'Zll_validation_plots/TMVA/'

# TTbar from MC
file_mc = TFile('/exports/uftrig01a/dcurry/heppy/files/MVA_out/v21_5_22_ttbar.root')

# TTbar from Data(Zuu for now)
file_data = TFile('/exports/uftrig01a/dcurry/heppy/files/MVA_out/v21_5_22_Zuu.root')

tree_data = file_data.Get('tree') 

tree_mc =  file_mc.Get('tree')

# TMVA tree
file = TFile.Open('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/data/MVA_gg_plus_ZH125_tightHmass.root', 'read')
tree = gDirectory.Get('TrainTree')

# ttbar cut
cut = 'abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4 & vLeptons_pt[0] > 20. & vLeptons_pt[1] > 20. & vLeptons_relIso04[0] < 0.15 & vLeptons_relIso04[1] < 0.15 & (HLT_BIT_HLT_IsoMu20_v || HLT_BIT_HLT_IsoTkMu20_v) & Vtype == 0 & Jet_pt_reg[hJCidx[0]] > 20. & Jet_pt_reg[hJCidx[1]] > 20. & HCSV_reg_pt > 100. & (V_mass < 75. || V_mass > 120.) & V_mass > 10. & Jet_btagCSV[hJCidx[0]] > 0.935 & Jet_btagCSV[hJCidx[1]] > 0.460' 

# Get the full normalization
posWeight = file_mc.Get('CountPosWeight')
negWeight = file_mc.Get('CountNegWeight')

theScale = lumi*xSec*SF / (posWeight.GetBinContent(1) - negWeight.GetBinContent(1))

cut_mc = cut + '*(puWeight*bTagWeight*'+str(theScale)+')'


# list of training vars
var_tmva_list = [['HCSV_reg_mass', 30, 90, 150],
            ['HCSV_reg_pt', 30, 20, 220],
            ['HVdPhi_reg', 30, 0, 3.14],
            ['Jet_btagCSV_hJCidx_0__', 30, 0.5, 1],
            ['Jet_btagCSV_hJCidx_1__', 30, 0.5, 1],
            ['Jet_pt_reg_hJCidx_0__', 30, 20, 150],
            ['Jet_pt_reg_hJCidx_1__', 30, 20, 150],
            ['V_mass', 30, 70, 105],
            ['Sum__Jet_pt_reg_30__abs_Jet_eta__2.4__Jet_puId__7__Jet_id_0__aJCidx___hJCidx_0_____aJCidx___hJCidx_1____', 10, 0, 10],
            ['V_pt', 30, 50, 200],
            ['_HCSV_reg_pt_D_V_pt_', 20, 0, 2] ,
            ['abs_Jet_eta_hJCidx_0___M_Jet_eta_hJCidx_1___', 30, 0, 2],
            ['softActivityVH_njets5', 10, 0, 10],
            ['HCSV_dR_reg', 30, 0, 2]
            ]

var_list = [['HCSV_reg_mass', 30, 90, 150],
            ['HCSV_reg_pt', 30, 20, 220],
            ['HVdPhi_reg', 30, 0, 3.14],
            ['Jet_btagCSV[hJCidx[0]]', 30, 0.5, 1],
            ['Jet_btagCSV[hJCidx[1]]', 30, 0.5, 1],
            ['Jet_pt_reg[hJCidx[0]]', 30, 20, 150],
            ['Jet_pt_reg[hJCidx[1]]', 30, 20, 150],
            ['V_mass', 30, 70, 105],
            ['Sum$(Jet_pt_reg>30&&abs(Jet_eta)<2.4&&Jet_puId==7&&Jet_id>0&&aJCidx!=(hJCidx[0])&&(aJCidx!=(hJCidx[1])))', 10, 0, 10],
            ['V_pt', 30, 50, 200],
            ['HCSV_reg_pt/V_pt', 20, 0, 2] ,
            ['abs(Jet_eta[hJCidx[0]]-Jet_eta[hJCidx[1]])', 30, 0, 2],
            ['softActivityVH_njets5', 10, 0, 10],
            ['HCSV_dR_reg', 30, 0, 2],
            ['gg_plus_ZH125_tightHmass.nominal', 20, -1, 1]
            ]

for var in var_tmva_list:

    #break
    
    canvas = TCanvas('canvas')
    
    tree.Draw(var[0])
    
    canvas.SaveAs('Zll_validation_plots/TMVA/'+var[0]+'.pdf')

    canvas.IsA().Destructor(canvas)



# Now profiles of worst input var vs all other vars and BDT output

worst_var = 'Jet_btagCSV[hJCidx[1]]'


for var in var_list:
    
    break
    
    if var[0] == worst_var: continue
    
    canvas = TCanvas('canvas')
    
    h  = TH2F('h', '' , 20, 0.5, 1, var[1], var[2], var[3])
    hd = TH2F('hd', '' , 20, 0.5, 1, var[1], var[2], var[3]) 
    
    tree_mc.Project('h', var[0]+':'+worst_var, cut_mc)
    tree_data.Project('hd', var[0]+':'+worst_var, cut)

    # make the profile
    prof = h.ProfileX()
    prof.SetLineColor(kBlack)
    prof.SetMinimum(var[2])
    prof.SetMaximum(var[3])

    profd = hd.ProfileX()
    profd.SetLineColor(kRed)

    prof.SetStats(0)
    prof.Draw('same')
    profd.Draw('same')
    prof.GetXaxis().SetTitle(worst_var)
    prof.GetYaxis().SetTitle(var[0])

    leg = TLegend(0.62,0.6,0.9,0.9)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(prof, 'Simulation', 'l')
    leg.AddEntry(profd, 'Data', 'l')
    leg.Draw('same')

    
    #raw_input('Press return to continue...')
    
    canvas.SaveAs('Zll_validation_plots/TMVA/profiles/profile_'+var[0]+'.pdf')
    canvas.IsA().Destructor(canvas)
    h.IsA().Destructor(h)
    hd.IsA().Destructor(hd)
    prof.IsA().Destructor(prof)
    profd.IsA().Destructor(profd)


# And now vs Mjj

mjj_var = 'HCSV_reg_mass'

for var in var_list:
    
    break
    
    if var[0] == worst_var: continue
    
    canvas = TCanvas('canvas')
    
    h  = TH2F('h', '' , 30, 90, 145, var[1], var[2], var[3])
    hd = TH2F('hd', '' , 30, 90, 145, var[1], var[2], var[3]) 
    
    tree_mc.Project('h', var[0]+':'+mjj_var, cut_mc)
    tree_data.Project('hd', var[0]+':'+mjj_var, cut)

    # make the profile
    prof = h.ProfileX()
    prof.SetLineColor(kBlack)
    prof.SetMinimum(var[2])
    prof.SetMaximum(var[3])

    profd = hd.ProfileX()
    profd.SetLineColor(kRed)

    prof.SetStats(0)
    prof.Draw('same')
    profd.Draw('same')
    prof.GetXaxis().SetTitle(mjj_var)
    prof.GetYaxis().SetTitle(var[0])

    leg = TLegend(0.62,0.6,0.9,0.9)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(prof, 'Simulation', 'l')
    leg.AddEntry(profd, 'Data', 'l')
    leg.Draw('same')

    
    #raw_input('Press return to continue...')
    
    canvas.SaveAs('Zll_validation_plots/TMVA/profiles/profile_mjj_'+var[0]+'.pdf')
    canvas.IsA().Destructor(canvas)
    h.IsA().Destructor(h)
    hd.IsA().Destructor(hd)
    prof.IsA().Destructor(prof)
    profd.IsA().Destructor(profd)




# ======================================



# TMVA SIG vs BKG eff plots
'''
file = TFile.Open('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/data/MVA_gg_plus_ZH125_tightHmass.root', 'read')

#file.cd('Method_BDT/gg_plus_ZH125_tightHmass')

#test_eff = gDirectory.Get('gg_plus_ZH125_tightHmass_effBvsS')

test_eff  = gDirectory.Get('Method_BDT/gg_plus_ZH125_tightHmass/MVA_gg_plus_ZH125_tightHmass_effBvsS')
train_eff = gDirectory.Get('Method_BDT/gg_plus_ZH125_tightHmass/MVA_gg_plus_ZH125_tightHmass_trainingEffBvsS') 

print test_eff
print train_eff

cEff = TCanvas('cEff')
sEff  = THStack('sEff', '')

sEff.Add(test_eff)
sEff.Add(train_eff)
sEff.Draw('nostack')
sEff.GetXaxis().SetTitle('Signal Efficiency')
sEff.GetYaxis().SetTitle('Background Efficiency')

test_eff.SetLineColor(6)
test_eff.SetLineStyle(1)

train_eff.SetLineColor(6)
train_eff.SetLineStyle(7)

leg = TLegend(0.15,0.6,0.5,0.9)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.AddEntry(train_eff, 'train BDT Zll', 'l')
leg.AddEntry(test_eff, 'test BDT Zll', 'l')
leg.Draw('same')

cEff.SaveAs('Zll_validation_plots/TMVA/BDT_EffBvsS.pdf')
'''

# =========================================================================================================

raw_input('Press return to continue...')


