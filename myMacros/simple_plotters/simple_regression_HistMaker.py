

###########################################
# Plot Maker for quick plots
#
# by David Curry
#
# 7.22.1014
###########################################

import sys
import os
from ROOT import *
from ROOT import gROOT
from matplotlib import interactive


# ====== Choose a channel =======

Zll = False
Zll = True

Zvv = False
#Zvv = True

Wlv = False
#Wlv = True

# ===============================


# Open root file of saved Hists

if Zll:

    # Most recennt Jet regression with v12
    file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v13_10_2015_ZH125v11_train_Zll_noMET.root')


if Zvv: file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/02_21_2015_Zvv_bJets_noMET.root')
if Wlv: file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/02_21_2015_Wlv_bJets_noMET.root')

#if Zll: file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/02_21_2015_Zll_bJets_noMET_noOpt.root')
#if Zvv: file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/02_21_2015_Zvv_bJets_noMET_noOpt.root')
#if Wlv: file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/02_21_2015_Wlv_bJets_noMET_noOpt.root')


#with semiLeptonic training cuts(semileptPt > 0)
#file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/01_7_2015_ZH_HBB_ZLL_v6_1_29_15_10_Var_semiLept.root')
#file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/01_7_2015_ZH_HBB_ZLL_v6_1_29_15_All_Var_semiLept.root')

if Zll:

    # Most recent Jet regression in v12
    file_old =TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/v13_10_2015_ZH125.root')


if Zvv: file_old =TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/02_21_2015_Zvv.root')
if Wlv: file_old =TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/02_21_2015_Wlv.root')

tree  = file.Get('tree')
tree_old = file_old.Get('tree') 

train_file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/v11_04_17_2015_ttbar.root')
tree_train = train_file.Get('tree')

test_file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/v11_04_17_2015_Zll.root')
tree_test = test_file.Get('tree')

# Plotting Option ======

if Zll: header = '#sqrt{s}=13TeV,   Z(l^{-}l^{+})H(b#bar{b}),   CMS Simulation'
if Wlv: header = '#sqrt{s}=13TeV,   W(lv)H(b#bar{b}),   CMS Simulation,   H_pt > 100'
if Zvv: header = '#sqrt{s}=13TeV,   Z(vv)H(b#bar{b}),   CMS Simulation,   H_pt > 100'

title = 'v12_Hpt0'

node = False
#node = True

diJet_mass = False
diJet_mass = True

diJet_mass_two = False
#diJet_mass_two = True

jet_Pt = False
#jet_Pt = True

response = False
#response =True

pt_balance = False
pt_balance = True

# ======================


# Quick Drawing

c1 = TCanvas('c1')
c2 = TCanvas('c2')
s1 = THStack('s1', 'Gen Jet2 Pt')
s2 = THStack('s2', 'Jet2 Pt')
h1 = TH1F('h1', '' , 50, 0, 200)
h2 = TH1F('h2', '' , 50, 0, 200)
h3 = TH1F('h3', '' , 50, 0, 200)
h4 = TH1F('h4', '' , 50, 0, 200)

cut = 'H_pt < 100 & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4 & Jet_mcPt[hJCidx[0]] > 20. & Jet_mcPt[hJCidx[1]] > 20. & abs(Jet_mcFlavour[hJCidx[0]])==5 & abs(Jet_mcFlavour[hJCidx[1]])==5'

cut_no_aJet  = cut+' & naJidx == 0'

cut_aJet  = cut+' & naJidx > 0'

c1.cd()
tree.Project('h1', 'Jet_mcPt[hJCidx[1]]', cut_no_aJet)
tree.Project('h2', 'Jet_mcPt[hJCidx[1]]', cut_aJet)
norm1 = h1.GetEntries()
h1.Scale(1/norm1)
norm2 = h2.GetEntries()
h2.Scale(1/norm2)
h2.SetLineColor(kRed)
s1.Add(h1)
s1.Add(h2)
s1.Draw('nostack')

leg1 = TLegend(0.62,0.6,0.9,0.9)
leg1.SetFillStyle(0)
leg1.SetBorderSize(0)
leg1.AddEntry(h1, 'No Additional Jets', 'l')
leg1.AddEntry(h2, 'Additional Jets > 0', 'l')
leg1.Draw('same')

c2.cd()
tree.Project('h3', 'Jet_pt[hJCidx[1]]', cut_no_aJet)
tree.Project('h4', 'Jet_pt[hJCidx[1]]', cut_aJet)
norm1 = h3.GetEntries()
h3.Scale(1/norm1)
norm2 = h4.GetEntries()
h4.Scale(1/norm2)
h4.SetLineColor(kRed)
s2.Add(h3)
s2.Add(h4)
s2.Draw('nostack')

leg2 = TLegend(0.62,0.6,0.9,0.9)
leg2.SetFillStyle(0)
leg2.SetBorderSize(0)
leg2.AddEntry(h3, 'No Additional Jets', 'l')
leg2.AddEntry(h4, 'Additional Jets > 0', 'l')
leg2.Draw('same')

# ======== Node Cuts ===========
if node:

    cut  = 'H_pt > 0 & Jet_pt[hJCidx[0]] > 20. & Jet_pt[hJCidx[1]] > 20. & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4'

    # only test on odd events
    cut = cut +' & evt%2 != 0'
    
    # V cut(Zll)
    #if Zll: cut = cut +' & V_mass < 105 & V_mass > 75 & deltaR_jj < 1.6'

    # MET(Zll)
    #if Zll: cut = cut +' & met_pt < 60'
    
    # CMVA cut
    #cut = cut +' & Jet_btagCSV[hJCidx[0]] > 0.8 & Jet_btagCSV[hJCidx[1]] > 0.8'

    cNode = TCanvas('cNode')
    sNode = THStack('sNode', '')

    # Loop over regressed files with differnet Node Cut
    node_list = [2, 3, 5, 10, 15, 20, 100, 500, 1000, 2000, 3000, 5000, 1000000]

    file5 = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v11_04_17_2015_Zllv11_train_Zll_noMET_nCuts5.root')
    file20 = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v11_04_17_2015_Zllv11_train_Zll_noMET_nCuts20.root')
    file100 = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v11_04_17_2015_Zllv11_train_Zll_noMET_nCuts100.root')
    file500 = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v11_04_17_2015_Zllv11_train_Zll_noMET_nCuts500.root')
    file1000 = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v11_04_17_2015_Zllv11_train_Zll_noMET_nCuts1000.root')
    file3000 = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v11_04_17_2015_Zllv11_train_Zll_noMET_nCuts3000.root')
    file5000 = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v11_04_17_2015_Zllv11_train_Zll_noMET_nCuts5000.root')
    file100000 = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v11_04_17_2015_Zllv11_train_Zll_noMET_nCuts100000.root')
    
    tree5 = file5.Get('tree')
    tree20 = file20.Get('tree')
    tree100 = file100.Get('tree')
    tree500 = file500.Get('tree')
    tree1000 = file1000.Get('tree')
    tree3000 = file3000.Get('tree')
    tree5000 = file5000.Get('tree')
    tree100000 = file100000.Get('tree')

    h5 = TH1F('h5', '' , 50, 20, 220)
    h20 = TH1F('h20', '' , 50, 20, 220)
    h100 = TH1F('h100', '' , 50, 20, 220)
    h500 = TH1F('h500', '' , 50, 20, 220)
    h1000 = TH1F('h1000', '' , 50, 20, 220)
    h3000 = TH1F('h3000', '' , 50, 20, 220)
    h5000 = TH1F('h5000', '' , 50, 20, 220)
    h100000 = TH1F('h100000', '' , 50, 20, 220)

    tree5.Project('h5', 'H_mass', cut)
    tree20.Project('h20','H_mass', cut)
    tree100.Project('h100','H_mass', cut)
    tree500.Project('h500','H_mass', cut)
    tree1000.Project('h1000','H_mass', cut)
    tree3000.Project('h3000','H_mass', cut)
    tree5000.Project('h5000','H_mass', cut)
    tree100000.Project('h100000','H_mass', cut)

    h5.SetLineColor(kGreen)
    h20.SetLineColor(kBlue)
    h100.SetLineColor(kBlue)
    h500.SetLineColor(kBlack)
    h1000.SetLineColor(kBlue)
    h3000.SetLineColor(kBlue)
    h5000.SetLineColor(kYellow)
    h100000.SetLineColor(kRed)
    
    # add to the stack
    #sNode.Add(h5)
    sNode.Add(h20)
    #sNode.Add(h100)
    #sNode.Add(h500)
    #sNode.Add(h1000)
    #sNode.Add(h3000)
    sNode.Add(h5000)
    #sNode.Add(h100000)
    
    # end node loop    
    sNode.Draw('nostack')
    sNode.SetTitle('')
    sNode.GetYaxis().SetTitle('Entries/4[GeV]')
    sNode.GetXaxis().SetTitle('m(jj) [GeV]')
    
    
    
# ===================================================
if diJet_mass:
    
    cMass = TCanvas('cMass')
    sMass = THStack('sMass', '')
    
    mass     = TH1F('mass', '' , 50, 20, 220)
    mass_reg = TH1F('mass_reg', '' , 50, 20, 220)

    mass_reg_addJ = TH1F('mass_reg_addJ', '' , 50, 20, 220)
    mass_addJ     = TH1F('mass_addJ', '' , 50, 20, 220)
    
    mRes     = TH1F('mRes', '' , 100, -1, 1)
    mRes_reg = TH1F('mRes_reg', '' , 100, -1, 1)
    #mRes_reg_all = TH1F('mRes_reg_all', '' , 100, -1, 1)


    # ======================================================================
    # Cuts
    
    cut  = 'H_pt > 0 & Jet_pt[hJCidx[0]] > 20. & Jet_pt[hJCidx[1]] > 20. & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4'
    
    # only test on odd events
    cut = cut +' & evt%2 != 0' 

    # additional Jet
    #cut = cut+ ' & naJidx > 1 '
    
    # V cut(Zll)
    if Zll: cut = cut +' & V_mass < 105 & V_mass > 75'
    
    # MET(Zll)
    if Zll: cut = cut +' & met_pt < 60'

    # MET(Wlv)
    #if Wlv: cut = cut +' & met_pt > 45'

    # MET(Zvv)
    #if Zvv: cut = cut +' & met_pt > 130'
    
    # CMVA cut
    cut = cut +' & Jet_btagCSV[hJCidx[0]] > 0.76 & Jet_btagCSV[hJCidx[1]] > 0.7'

    # btagged jets
    #cut = cut +' & abs(Jet_mcFlavour[hJCidx[0]]) == 5 & abs(Jet_mcFlavour[hJCidx[1]]) == 5'

    # with both jets semileptonic
    #cut = cut +' & hJets_leptonPt[0] > 0 | hJets_leptonPt[1] > 0'
    
    # with both jets no semileptonic
    #cut = cut +' & hJets_leptonPt[0] < 0 & hJets_leptonPt[1] < 0'
    
    # with both jets no soft lepton
    #cut = cut+' & (hJet_SoftLeptIdlooseMu[0]!=1 & hJet_SoftLeptId95[0]!=1) & (hJet_SoftLeptIdlooseMu[1]!=1 & hJet_SoftLeptId95[1]!=1)'

    # =====================================================================

    
    # project the branch into a histogram, (hist, branch, cuts)
    tree.Project('mass_reg', 'H_mass', cut)
    tree_old.Project('mass', 'H_mass', cut)
    tree.Project('mass_reg_addJ', 'H_mass_addJet', cut)
    tree.Project('mass_addJ', 'H_mass_addJet_noReg', cut)

    print '==== Mass Entries ===='
    print 'Regressed : ', mass_reg.GetEntries()
    print 'Baseline  : ', mass.GetEntries()

    # experimental!
    #tree_SL.Project('mass_reg', 'H.mass', cut+' & hJet_isSemiLept[0]<1 & hJet_isSemiLept[1]<1')
    #tree_SL.Draw('H.mass>>+mass_reg', cut+' & hJet_isSemiLept[0]<1 & hJet_isSemiLept[1]<1')
    
    # ============
    
    mass.SetStats(0)
    #mass.SetMaximum(300)
    #pt.SetTitle('BDT Regression: Jet p_{t}')
    mass_reg.SetLineColor(kRed)
    mass_reg_addJ.SetLineColor(kGreen)
    mass_addJ.SetLineColor(kBlack)
    
    sMass.Add(mass)
    sMass.Add(mass_reg)
    #sMass.Add(mass_reg_addJ)
    #sMass.Add(mass_addJ)
    sMass.Draw('nostack')

    sMass.SetTitle('')
    sMass.GetYaxis().SetTitle('Entries/4[GeV]')
    sMass.GetXaxis().SetTitle('m(jj) [GeV]')

    # Regression Metric ==================
    
    
    #project prediction and target difference
    #mae     = TH1F('mae', '' , 100, 0, 50)
    #mae_all = TH1F('mae_all', '' , 100, 0, 50)

    #Sum, Sum_all = 0,0
    #tree.Project('mae', 'abs(genH.mass - H.mass)', cut) 
    #for bin in range(100):
    #    Sum += mae.GetBinContent(bin)*bin
    
    #tree_all.Project('mae_all', 'abs(genH.mass - H.mass)', cut)
    #for bin in range(100):
    #    Sum_all += mae_all.GetBinContent(bin)*bin
    
    #metric = Sum/mae.GetEntries()
    #metric_all = Sum_all/mae_all.GetEntries()
    #print 'Metric     =', metric
    #print 'Metric_all =', metric_all 
        
    
    # Get Gaussian variables =============

    fit_min = 90
    fit_max = 145 

    mass.Fit('gaus', 'Q','same', 90, 135)
    fit=mass.GetFunction('gaus')
    fit.SetLineColor(kBlue)
    mass_std = fit.GetParameter(2)
    mass_mu = fit.GetParameter(1) 
    mass_metric = mass_std/mass_mu
    mass_std=str(round(mass_std,4))
    mass_mu=str(round(mass_mu,4))
    mass_metric = str(round(mass_metric,4))
     
    mass_reg.Fit('gaus', 'Q', 'same', fit_min, fit_max)
    fit2=mass_reg.GetFunction('gaus')
    mass_reg_std=fit2.GetParameter(2)
    mass_reg_mu=fit2.GetParameter(1)
    mass_metric1 = mass_reg_std/mass_reg_mu
    mass_reg_std=str(round(mass_reg_std,4))
    mass_reg_mu=str(round(mass_reg_mu,4))
    mass_metric1 = str(round(mass_metric1,4))

    # regressed metric
    print mass_metric1
    '''
    mass_reg_addJ.Fit('gaus', '', 'same', fit_min, fit_max)
    fit3=mass_reg_addJ.GetFunction('gaus')
    fit3.SetLineColor(kGreen)
    mass_reg_addJ_std=fit3.GetParameter(2)
    mass_reg_addJ_mu=fit3.GetParameter(1)
    mass_reg_addJ_std=str(round(mass_reg_addJ_std,4))
    mass_reg_addJ_mu=str(round(mass_reg_addJ_mu,4))    

    mass_addJ.Fit('gaus', '', 'same', fit_min, fit_max)
    fit3=mass_addJ.GetFunction('gaus')
    fit3.SetLineColor(kBlack)
    mass_addJ_std=fit3.GetParameter(2)
    mass_addJ_mu=fit3.GetParameter(1)
    mass_addJ_std=str(round(mass_addJ_std,4))
    mass_addJ_mu=str(round(mass_addJ_mu,4))
    '''
    
    # ====================================
    leg = TLegend(0.62,0.6,0.9,0.9)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(mass, 'Baseline', 'l')
    leg.AddEntry(0, '#sigma='+mass_std, '')
    leg.AddEntry(0, '#mu='+mass_mu, '')
    leg.AddEntry(0, '#sigma/#mu='+mass_metric, '')
    
    #leg.AddEntry(mass_addJ, 'Baseline(add Jet)', 'l')
    #leg.AddEntry(0, '#sigma='+mass_addJ_std, '')
    #leg.AddEntry(0, '#mu='+mass_addJ_mu, '')
    
    leg.AddEntry(mass_reg, 'Regressed', 'l')
    leg.AddEntry(0, '#sigma='+mass_reg_std, '')
    leg.AddEntry(0, '#mu='+mass_reg_mu, '')
    leg.AddEntry(0, '#sigma/#mu='+mass_metric1, '')
    
    #leg.AddEntry(mass_reg_addJ, 'Regressed(add Jet)', 'l')
    #leg.AddEntry(0, '#sigma='+mass_reg_addJ_std, '')
    #leg.AddEntry(0, '#mu='+mass_reg_addJ_mu, '')

    leg.Draw('same')
        
    l_1 = TLatex()
    l_1.SetNDC()
    l_1.SetTextSize(0.03)
    l_1.DrawLatex(0.1, 0.93, header)
    l_1.Draw('same')

    cMass.SaveAs('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/myMacros/plots/regression/dijet_mass_'+title+'.pdf')
    
    # ===================================================
    

if pt_balance:

    cbal = TCanvas('cbal')
    sbal = THStack('sbal', '')
    
    pt_bal     = TH1F('pt_bal', '' , 50, 0, 2)
    pt_bal_reg = TH1F('pt_bal_reg', '' , 50, 0, 2)
    
    # V cut(Zll)
    cut = cut +' & V_mass < 105 & V_mass > 75'
    
    # project the branch into a histogram, (hist, branch, cuts)
    tree.Project('pt_bal_reg', 'H_pt/V_pt', cut)
    tree_old.Project('pt_bal', 'H_pt/V_pt', cut)
    
    pt_bal.SetStats(0)
    pt_bal_reg.SetLineColor(kRed)
    sbal.Add(pt_bal)
    sbal.Add(pt_bal_reg)
    sbal.Draw('nostack')
    
    sbal.SetTitle('')
    sbal.GetYaxis().SetTitle('Entries')
    sbal.GetXaxis().SetTitle('Pt Balance: p_{T}(jj) / p_{T}(ll)')

    # Get Gaussian variables =============
    pt_bal.Fit('gaus', '','same', 0.7, 1.3)
    fit=pt_bal.GetFunction('gaus')
    fit.SetLineColor(kBlue)
    pt_bal_std = fit.GetParameter(2)
    pt_bal_mu = fit.GetParameter(1)
    pt_bal_metric = pt_bal_std/pt_bal_mu
    pt_bal_std = str(round(pt_bal_std,4))
    pt_bal_mu = str(round(pt_bal_mu,4))
    pt_bal_metric = str(round(pt_bal_metric,4))
    
    pt_bal_reg.Fit('gaus', '', 'same', 0.7, 1.3)
    fit2=pt_bal_reg.GetFunction('gaus')
    pt_bal_reg_std=fit2.GetParameter(2)
    pt_bal_reg_mu=fit2.GetParameter(1)
    pt_bal_metric1 = pt_bal_reg_std/pt_bal_reg_mu
    pt_bal_reg_std=str(round(pt_bal_reg_std,4))
    pt_bal_reg_mu=str(round(pt_bal_reg_mu,4))
    pt_bal_metric1 = str(round(pt_bal_metric1,4))
    
    l_1 = TLatex()
    l_1.SetNDC()
    l_1.SetTextSize(0.03)
    l_1.DrawLatex(0.1, 0.93, header)
    l_1.Draw('same')
    
    leg4 = TLegend(0.62,0.50,0.87,0.87)
    leg4.SetFillStyle(0)
    leg4.SetBorderSize(0)
    leg4.AddEntry(pt_bal, 'Baseline', 'l')
    leg4.AddEntry(0, '#sigma='+pt_bal_std, '')
    leg4.AddEntry(0, '#mu='+pt_bal_mu, '')
    leg4.AddEntry(pt_bal_reg, 'Regressed', 'l')
    leg4.AddEntry(0, '#sigma='+pt_bal_reg_std, '')
    leg4.AddEntry(0, '#mu='+pt_bal_reg_mu, '')
    leg4.Draw('same')

    cbal.SaveAs('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/myMacros/plots/regression/pt_balance_'+title+'.pdf')
    
# ======================================================================================
    
    
if jet_Pt:

    cPt1 = TCanvas('cPt1')
    sPt1 = THStack('sPt1', '')

    jet_pt     = TH1F('jet_pt', '' , 50, -1, 1)
    jet_pt_reg = TH1F('jet_pt_reg', '' , 50, -1, 1)

    # If Manual fitting ========

    #tree2.Project('jet_pt_reg', '(10^(2.576+0.033*hJet_pt[0]-0.0002*(hJet_pt[0])^2+2.6*10^(-7)*(hJet_pt[0])^3)-hJet_mcPt[0])/hJet_mcPt[0]', 'hJet_pt[0]>0 && hJet_mcPt[0]>0')
    # ==========================

    #cut = '(hJet_SoftLeptIdlooseMu==1||hJet_SoftLeptId95==1)'

    #cut = ''

    # project the branch into a histogram, (hist, branch, cuts)
    tree.Project('jet_pt_reg', '(Jet_pt_reg[0]-Jet_mcPt[hJCidx[0]])/Jet_mcPt[hJCidx[0]]', cut)
    tree.Project('jet_pt', '(Jet_pt[hJCidx[0]]-Jet_mcPt[hJCidx[0]])/Jet_mcPt[hJCidx[0]]', cut)
    
    print '==== Entries ===='
    print 'Baseline    : ', jet_pt.GetEntries() 
    print 'Regressed   : ', jet_pt_reg.GetEntries()
    

    jet_pt.SetStats(0)
    jet_pt_reg.SetLineColor(kRed)
    sPt1.Add(jet_pt)
    sPt1.Add(jet_pt_reg)
    sPt1.Draw('nostack')

    sPt1.SetTitle('')
    sPt1.GetYaxis().SetTitle('Entries')
    sPt1.GetXaxis().SetTitle('(Jet1_pt-Jet1_genPt)/Jet1_genPt')

    #jet_pt_reg.Draw('same')


    l_1 = TLatex()
    l_1.SetNDC()
    l_1.SetTextSize(0.03)
    l_1.DrawLatex(0.1, 0.93, header)
    l_1.Draw('same')

    # Get Gaussian variables =============

    f1 = TF1('f1', '([0]/[2])*exp(-0.5*(x-[1])**2/[2]**2)*([3]/[4])*exp(-0.5*(x-[1])**2/[4]**2)')
 
    f1.SetParameter(0,1)
    f1.SetParameter(1,0)
    f1.SetParameter(2,1)
    f1.SetParameter(3,0)
    f1.SetParameter(4,1)

    jet_pt.Fit('gaus','Q', 'same', -0.15, 0.15)
    fit=jet_pt.GetFunction('gaus')
    fit.SetLineColor(kBlue)
    jet_pt_std = fit.GetParameter(2)
    jet_pt_mu  = fit.GetParameter(1)
    jet_pt_std=str(round(jet_pt_std,4))
    jet_pt_mu=str(round(jet_pt_mu,4))
    
    jet_pt_reg.Fit('gaus','Q', 'same', -0.15, 0.15)
    fit2=jet_pt_reg.GetFunction('gaus')
    jet_pt_reg_std = fit2.GetParameter(2)
    jet_pt_reg_mu  = fit2.GetParameter(1)
    jet_pt_reg_std=str(round(jet_pt_reg_std,4))
    jet_pt_reg_mu=str(round(jet_pt_reg_mu,4))
    # ====================================
    
    leg1 = TLegend(0.62,0.50,0.87,0.87)
    leg1.SetFillStyle(0)
    leg1.SetBorderSize(0)
    leg1.AddEntry(jet_pt, 'Baseline', 'l')
    leg1.AddEntry(0, '#sigma='+jet_pt_std, '')
    leg1.AddEntry(0, '#mu='+jet_pt_mu, '')
    leg1.AddEntry(jet_pt_reg, 'Regressed', 'l')
    leg1.AddEntry(0, '#sigma='+jet_pt_reg_std, '')
    leg1.AddEntry(0, '#mu='+jet_pt_reg_mu, '')
    leg1.Draw('same')

    cPt1.SaveAs('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/VHbb/myMacros/plots/regression/jet1_Pt_resolution_'+title+'.pdf')


    #  Jet 2
    cPt2 = TCanvas('cPt2')
    sPt2 = THStack('sPt2', '')
    jet2_pt     = TH1F('jet2_pt', '' , 50, -1, 1)
    jet2_pt_reg = TH1F('jet2_pt_reg', '' , 50, -1, 1)

    # If Manual fitting ========

    #tree2.Project('jet_pt_reg', '(10^(2.576+0.033*hJet_pt[0]-0.0002*(hJet_pt[0])^2+2.6*10^(-7)*(hJet_pt[0])^3)-hJet_mcPt[0])/hJet_mcPt[0]', 'hJet_pt[0]>0 && hJet_mcPt[0]>0')
    # ==========================

    #cut = '(hJet_SoftLeptIdlooseMu==1||hJet_SoftLeptId95==1)'

    #cut = ''

    # project the branch into a histogram, (hist, branch, cuts)
    tree.Project('jet2_pt_reg', '(Jet_pt_reg[1]-Jet_mcPt[hJCidx[1]])/Jet_mcPt[hJCidx[1]]', cut)
    tree.Project('jet2_pt', '(Jet_pt[hJCidx[1]]-Jet_mcPt[hJCidx[1]])/Jet_mcPt[hJCidx[1]]', cut)
    
    print '==== Entries Jet 2 ===='
    print 'Baseline    : ', jet2_pt.GetEntries()
    print 'Regressed   : ', jet2_pt_reg.GetEntries()

    jet2_pt.SetStats(0)
    jet2_pt_reg.SetLineColor(kRed)
    sPt2.Add(jet2_pt)
    sPt2.Add(jet2_pt_reg)
    sPt2.Draw('nostack')

    sPt2.SetTitle('')
    sPt2.GetYaxis().SetTitle('Entries')
    sPt2.GetXaxis().SetTitle('(Jet2_pt-Jet2_genPt)/Jet2_genPt')
    
    l_1 = TLatex()
    l_1.SetNDC()
    l_1.SetTextSize(0.03)
    l_1.DrawLatex(0.1, 0.93, header)
    l_1.Draw('same')

    # Get Gaussian variables =============

    f1 = TF1('f1', '([0]/[2])*exp(-0.5*(x-[1])**2/[2]**2)*([3]/[4])*exp(-0.5*(x-[1])**2/[4]**2)')
 
    f1.SetParameter(0,1)
    f1.SetParameter(1,0)
    f1.SetParameter(2,1)
    f1.SetParameter(3,0)
    f1.SetParameter(4,1)

    jet2_pt.Fit('gaus','Q', 'same', -0.3, 0.15)
    fit=jet2_pt.GetFunction('gaus')
    fit.SetLineColor(kBlue)
    jet_pt_std = fit.GetParameter(2)
    jet_pt_mu  = fit.GetParameter(1)
    jet_pt_std=str(round(jet_pt_std,4))
    jet_pt_mu=str(round(jet_pt_mu,4))
    
    jet2_pt_reg.Fit('gaus','Q', 'same', -0.15, 0.25)
    fit2=jet2_pt_reg.GetFunction('gaus')
    jet_pt_reg_std = fit2.GetParameter(2)
    jet_pt_reg_mu  = fit2.GetParameter(1)
    jet_pt_reg_std=str(round(jet_pt_reg_std,4))
    jet_pt_reg_mu=str(round(jet_pt_reg_mu,4))
    # ====================================
    
    leg2 = TLegend(0.62,0.50,0.87,0.87)
    leg2.SetFillStyle(0)
    leg2.SetBorderSize(0)
    leg2.AddEntry(jet_pt, 'Baseline', 'l')
    leg2.AddEntry(0, '#sigma='+jet_pt_std, '')
    leg2.AddEntry(0, '#mu='+jet_pt_mu, '')
    leg2.AddEntry(jet_pt_reg, 'Regressed', 'l')
    leg2.AddEntry(0, '#sigma='+jet_pt_reg_std, '')
    leg2.AddEntry(0, '#mu='+jet_pt_reg_mu, '')
    leg2.Draw('same')

    cPt2.SaveAs('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/VHbb/myMacros/plots/regression/jet2_Pt_resolution_'+title+'.pdf')




# ===========================================

if response:

    feature_list = ['hJets_rawPt', 'hJets_mass', 'hJets_chEmEF', 'hJets_chHEF', 'rho', 'hJets_eta', 'hJets_neHEF', 'met_phi', 'hJets_chEmEF']

    for i, var in enumerate(feature_list):
        print 'Looping over feature:', var
        
        c = TCanvas('c')
        h = TH2F('h', '', 25, 0, 600, 25, -1, -1)
        h_old = TH2F('h_old', '', 25, 0, 200, 25, -1, -1)
        tree_old.Project('h_old', '(hJets_mcPt[0]/hJets_pt[0]):hJets_rawPt[0]')
        tree.Project('h', '(hJets_mcPt[0]/hJets_pt[0]):hJets_rawPt[0]')
        
        p_old = h_old.ProfileX()
        p = h.ProfileX()
        p.SetStats(0)
        p.SetLineColor(kRed)
        p.SetMinimum(0.85)
        p.SetMaximum(1.2)
        p.Draw()
        p_old.Draw('same')

        p.GetXaxis().SetTitle('hJets_rawPt')
        p.GetYaxis().SetTitle('hJets_mcPt[0] / hJets_pt[0]')
        
        # set the legend
        leg = TLegend(0.6,0.75,0.85,0.9)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.AddEntry(p, 'Regressed', 'l')
        leg.AddEntry(p_old, 'Baseline', 'l')
        leg.Draw('same')
        
        line = TLine(0, 1, 450, 1);
        line.SetLineColor(kGreen)
        line.Draw('same')

        c.SaveAs('plots/response/hJets_rawPt.pdf')
        
        gROOT.Clear()
        h.Delete()
        h_old.Delete()
        c.Delete()
        # =========================================================

        c = TCanvas('c')
        h = TH2F('h', '', 25, 0, 600, 25, -1, -1)
        h_old = TH2F('h_old', '', 25, 0, 200, 25, -1, -1)
        tree_old.Project('h_old', '(hJets_mcPt[0]/hJets_pt[0]):hJets_mass[0]')
        tree.Project('h', '(hJets_mcPt[0]/hJets_pt[0]):hJets_mass[0]')
        
        p_old = h_old.ProfileX()
        p = h.ProfileX()
        p.SetStats(0)
        p.SetLineColor(kRed)
        p.SetMinimum(0.8)
        p.Draw()
        p_old.Draw('same')
        
        p.GetXaxis().SetTitle('hJets_mass')
        p.GetYaxis().SetTitle('hJets_mcPt[0] / hJets_pt[0]')
        
        # set the legend
        leg = TLegend(0.6,0.75,0.85,0.9)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.AddEntry(p, 'Regressed', 'l')
        leg.AddEntry(p_old, 'Baseline', 'l')
        leg.Draw('same')
        
        line = TLine(0, 1, 80, 1);
        line.SetLineColor(kGreen)
        line.Draw('same')
        
        c.SaveAs('plots/response/hJets_mass.pdf')

        gROOT.Clear()
        h.Delete()
        h_old.Delete()

        # =================================================================        
        
        c = TCanvas('c')
        h = TH2F('h', '', 25, 0, 600, 25, -1, -1)
        h_old = TH2F('h_old', '', 25, 0, 200, 25, -1, -1)
        tree_old.Project('h_old', '(hJets_mcPt[0]/hJets_pt[0]):hJets_chEmEF[0]')
        tree.Project('h', '(hJets_mcPt[0]/hJets_pt[0]):hJets_chEmEF[0]')
        
        p_old = h_old.ProfileX()
        p = h.ProfileX()
        p.SetStats(0)
        p.SetLineColor(kRed)
        p.SetMinimum(0)
        p.SetMaximum(2)
        p.Draw()
        p_old.Draw('same')
        
        p.GetXaxis().SetTitle('hJets_chEmEF')
        p.GetYaxis().SetTitle('hJets_mcPt[0] / hJets_pt[0]')
        
        # set the legend
        leg = TLegend(0.6,0.75,0.85,0.9)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.AddEntry(p, 'Regressed', 'l')
        leg.AddEntry(p_old, 'Baseline', 'l')
        leg.Draw('same')
        
        line = TLine(0, 1, 550, 1);
        line.SetLineColor(kGreen)
        line.Draw('same')
        
        c.SaveAs('plots/response/hJets_chEmEF.pdf')
        
        gROOT.Clear()
        h.Delete()
        h_old.Delete()
        
        # ====================================================
        
        c = TCanvas('c')
        h = TH2F('h', '', 25, 0, 600, 25, -1, -1)
        h_old = TH2F('h_old', '', 25, 0, 200, 25, -1, -1)
        tree_old.Project('h_old', '(hJets_mcPt[0]/hJets_pt[0]):hJets_chHEF[0]')
        tree.Project('h', '(hJets_mcPt[0]/hJets_pt[0]):hJets_chHEF[0]')
        
        p_old = h_old.ProfileX()
        p = h.ProfileX()
        p.SetStats(0)
        p.SetLineColor(kRed)
        p.SetMinimum(0.6)
        p.SetMaximum(1.6)
        p.Draw()
        p_old.Draw('same')
        
        p.GetXaxis().SetTitle('hJets_chHEF')
        p.GetYaxis().SetTitle('hJets_mcPt[0] / hJets_pt[0]')
        
        # set the legend
        leg = TLegend(0.62,0.6,0.9,0.9)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.AddEntry(p, 'Regressed', 'l')
        leg.AddEntry(p_old, 'Baseline', 'l')
        leg.Draw('same')
        
        line = TLine(0, 1, 1.2, 1);
        line.SetLineColor(kGreen)
        line.Draw('same')
        
        c.SaveAs('plots/response/hJets_chHEF.pdf')
        
        gROOT.Clear()
        h.Delete()
        h_old.Delete()

        # =================================================================
        
        c = TCanvas('c')
        h = TH2F('h', '', 25, 0, 600, 25, -1, -1)
        h_old = TH2F('h_old', '', 25, 0, 200, 25, -1, -1)
        tree_old.Project('h_old', '(hJets_mcPt[0]/hJets_pt[0]):rho')
        tree.Project('h', '(hJets_mcPt[0]/hJets_pt[0]):rho')
        
        p_old = h_old.ProfileX()
        p = h.ProfileX()
        p.SetStats(0)
        p.SetLineColor(kRed)
        p.SetMinimum(0.8)
        p.SetMaximum(1.3)
        p.Draw()
        p_old.Draw('same')
        
        p.GetXaxis().SetTitle('rho')
        p.GetYaxis().SetTitle('hJets_mcPt[0] / hJets_pt[0]')
        
        # set the legend
        leg = TLegend(0.6,0.75,0.85,0.9)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.AddEntry(p, 'Regressed', 'l')
        leg.AddEntry(p_old, 'Baseline', 'l')
        leg.Draw('same')
        
        line = TLine(5, 1, 55, 1);
        line.SetLineColor(kGreen)
        line.Draw('same')
        
        c.SaveAs('plots/response/rho.pdf')
        
        gROOT.Clear()
        h.Delete()
        h_old.Delete()
        
        # =================================================================
        
        c = TCanvas('c')
        h = TH2F('h', '', 25, 0, 200, 25, -1, -1)
        h_old = TH2F('h_old', '', 25, 0, 200, 25, -1, -1)
        tree_old.Project('h_old', '(hJets_mcPt[0]/hJets_pt[0]):hJets_eta[0]')
        tree.Project('h', '(hJets_mcPt[0]/hJets_pt[0]):hJets_eta[0]')
        
        p_old = h_old.ProfileX()
        p = h.ProfileX()
        p.SetStats(0)
        p.SetLineColor(kRed)
        p.SetMinimum(0.7)
        p.SetMaximum(1.1)
        p.Draw()
        p_old.Draw('same')
        
        p.GetXaxis().SetTitle('hJets_eta')
        p.GetYaxis().SetTitle('hJets_mcPt[0] / hJets_pt[0]')
        
        # set the legend
        leg = TLegend(0.6,0.75,0.85,0.9)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.AddEntry(p, 'Regressed', 'l')
        leg.AddEntry(p_old, 'Baseline', 'l')
        leg.Draw('same')
        
        line = TLine(-2.5, 1, 2.5, 1);
        line.SetLineColor(kGreen)
        line.Draw('same')
        
        c.SaveAs('plots/response/hJets_eta.pdf')
        
        gROOT.Clear()
        h.Delete()
        h_old.Delete()
         
        # =================================================================
        
        c = TCanvas('c')
        h = TH2F('h', '', 25, 0, 600, 25, -1, -1)
        h_old = TH2F('h_old', '', 25, 0, 200, 25, -1, -1)
        tree_old.Project('h_old', '(hJets_mcPt[0]/hJets_pt[0]):hJets_neHEF[0]')
        tree.Project('h', '(hJets_mcPt[0]/hJets_pt[0]):hJets_neHEF[0]')
        
        p_old = h_old.ProfileX()
        p = h.ProfileX()
        p.SetStats(0)
        p.SetLineColor(kRed)
        p.SetMinimum(0.8)
        p.SetMaximum(1.5)
        p.Draw()
        p_old.Draw('same')
        
        p.GetXaxis().SetTitle('hJets_neHEF')
        p.GetYaxis().SetTitle('hJets_mcPt / hJets_pt')
        
        # set the legend
        leg = TLegend(0.6,0.75,0.85,0.9)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.AddEntry(p, 'Regressed', 'l')
        leg.AddEntry(p_old, 'Baseline', 'l')
        leg.Draw('same')
        
        line = TLine(0, 1, 0.83, 1);
        line.SetLineColor(kGreen)
        line.Draw('same')
        
        c.SaveAs('plots/response/hJets_neHEF.pdf')
        
        gROOT.Clear()
        h.Delete()
        h_old.Delete()

        # =================================================================
        
        c = TCanvas('c')
        h = TH2F('h', '', 25, 0, 600, 25, -1, -1)
        h_old = TH2F('h_old', '', 25, 0, 200, 25, -1, -1)
        tree_old.Project('h_old', '(hJets_mcPt[0]/hJets_pt[0]):met_phi')
        tree.Project('h', '(hJets_mcPt[0]/hJets_pt[0]):met_phi')
        
        p_old = h_old.ProfileX()
        p = h.ProfileX()
        p.SetStats(0)
        p.SetLineColor(kRed)
        p.SetMinimum(0.8)
        p.SetMaximum(1.5)
        p.Draw()
        p_old.Draw('same')
        
        p.GetXaxis().SetTitle('met_phi')
        p.GetYaxis().SetTitle('hJets_mcPt[0] / hJets_pt[0]')
        
        # set the legend
        leg = TLegend(0.6,0.75,0.85,0.9)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.AddEntry(p, 'Regressed', 'l')
        leg.AddEntry(p_old, 'Baseline', 'l')
        leg.Draw('same')
        
        line = TLine(-3.14, 1, 3.14, 1);
        line.SetLineColor(kGreen)
        line.Draw('same')
        
        c.SaveAs('plots/response/met_phi.pdf')
        
        gROOT.Clear()
        h.Delete()
        h_old.Delete()
        
        # =================================================================

        c = TCanvas('c')
        h = TH2F('h', '', 25, 0, 600, 25, -1, -1)
        h_old = TH2F('h_old', '', 25, 0, 200, 25, -1, -1)
        tree_old.Project('h_old', '(hJets_mcPt[0]/hJets_pt[0]):hJets_chEmEF[0]')
        tree.Project('h', '(hJets_mcPt[0]/hJets_pt[0]):hJets_chEmEF[0]')
        
        p_old = h_old.ProfileX()
        p = h.ProfileX()
        p.SetStats(0)
        p.SetLineColor(kRed)
        p.SetMinimum(0.8)
        p.SetMaximum(1.5)
        p.Draw()
        p_old.Draw('same')
        
        p.GetXaxis().SetTitle('hJets_chEmEF')
        p.GetYaxis().SetTitle('hJets_mcPt / hJets_pt')
        
        # set the legend
        leg = TLegend(0.6,0.75,0.85,0.9)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.AddEntry(p, 'Regressed', 'l')
        leg.AddEntry(p_old, 'Baseline', 'l')
        leg.Draw('same')
        
        line = TLine(0, 1, 0.65, 1);
        line.SetLineColor(kGreen)
        line.Draw('same')
        
        c.SaveAs('plots/response/hJets_chEmEF.pdf')
        
        gROOT.Clear()
        h.Delete()
        h_old.Delete()

        # =================================================================
        
        c = TCanvas('c')
        h = TH2F('h', '', 25, 0, 600, 25, -1, -1)
        h_old = TH2F('h_old', '', 25, 0, 200, 25, -1, -1)
        tree_old.Project('h_old', '(hJets_mcPt[0]/hJets_pt[0]):met_sumEt')
        tree.Project('h', '(hJets_mcPt[0]/hJets_pt[0]):met_sumEt')
        
        p_old = h_old.ProfileX()
        p = h.ProfileX()
        p.SetStats(0)
        p.SetLineColor(kRed)
        p.SetMinimum(0.8)
        p.SetMaximum(1.2)
        p.Draw()
        p_old.Draw('same')
        
        p.GetXaxis().SetTitle('met_sumEt')
        p.GetYaxis().SetTitle('hJets_mcPt / hJets_pt')
        
        # set the legend
        leg = TLegend(0.6,0.75,0.85,0.9)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.AddEntry(p, 'Regressed', 'l')
        leg.AddEntry(p_old, 'Baseline', 'l')
        leg.Draw('same')
        
        line = TLine(520, 1, 4230, 1);
        line.SetLineColor(kGreen)
        line.Draw('same')
        
        c.SaveAs('plots/response/met_sumEt.pdf')
        
        gROOT.Clear()
        h.Delete()
        h_old.Delete()
        
        # =================================================================

        c = TCanvas('c')
        h = TH2F('h', '', 25, 0, 600, 25, -1, -1)
        h_old = TH2F('h_old', '', 25, 0, 200, 25, -1, -1)
        tree_old.Project('h_old', '(hJets_mcPt[0]/hJets_pt[0]):hJets_neEmEF[0]')
        tree.Project('h', '(hJets_mcPt[0]/hJets_pt[0]):hJets_neEmEF[0]')
        
        p_old = h_old.ProfileX()
        p = h.ProfileX()
        p.SetStats(0)
        p.SetLineColor(kRed)
        p.SetMinimum(0.8)
        p.SetMaximum(1.2)
        p.Draw()
        p_old.Draw('same')

        p.GetXaxis().SetTitle('hJets_neEmEF')
        p.GetYaxis().SetTitle('hJets_mcPt / hJets_pt')
        
        # set the legend
        leg = TLegend(0.6,0.75,0.85,0.9)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.AddEntry(p, 'Regressed', 'l')
        leg.AddEntry(p_old, 'Baseline', 'l')
        leg.Draw('same')
        
        line = TLine(0, 1, 0.85, 1);
        line.SetLineColor(kGreen)
        line.Draw('same')

        c.SaveAs('plots/response/neEmEF.pdf')

        gROOT.Clear()
        h.Delete()
        h_old.Delete()
                                 


        
        
        if i == 0: break
        
        '''
        new = 'h_'+var
        new_reg = 'h_reg_'+var

        newC = 'c'+var
        newC = TCanvas(str(newC))
        
        new = TH2F(str(new), '', 25, 0, 600, 25, -1, -1) 
        new_reg = TH2F(str(new_reg), '', 25, 0, 600, 25, -1, 1)
        
        p_string = 'hJets_mcPt/hJets_pt:'+var
        tree_old.Project(str(new), p_string)
        tree.Project(str(new_reg), p_string)

        new.SetStats(0)
        new.GetYaxis().SetTitle('Regressed Jet pT [GeV]')
        new.GetXaxis().SetTitle('Generated Jet pT [GeV]')
        
        new.Draw()
        '''


# ================================================

# Function Mapping/ Fitting
'''
tree2.Draw('log(hJet_genPt[0]):hJet_pt[0] >> h1', 'hJet_pt[0]>0 && hJet_genPt[0]>0 && hJet_pt[0]<300')

f1 = TF1('f1', 'pol3', 20, 300)

h1.Fit('f1', 'r')
'''


#jet_pt = TH1F('jet_pt', '' , 100, 0, 250)

#tree2.Project('jet_pt', 'hJet_genPt[0]:hJet_pt[0]', 'hJet_pt[0]>0 && hJet_genPt[0]>0')

#jet_pt.Draw()


# ===========================================
# Look at various counts
'''
# Number Events with Bjets assigned.
tree.Draw('>>elist', 'abs(hJet_flavour[0]) == 5 && abs(hJet_flavour[1]) == 5')
print elist.GetN()


# Number of mistagged Bjets
h1 = TH1F('h1', '', 2, 0, 2)
#tree.Draw('abs(hJet_flavour) == 5 >> h1')
tree.Project('h1', 'abs(hJet_flavour) == 5')

print 'Total Jets:', h1.GetEntries()
print 'B Jets    :', h1.GetBinContent(2)
print 'Ratio     :', h1.GetBinContent(2)/h1.GetEntries()
'''


raw_input('press return to continue')



