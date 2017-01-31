###########################################
#  Validation Plot Maker for quick plots in Zll channel
#
#  Usage:  Specify Input files (line 14) and where to save plots (line 20)
#
#  David Curry, 09.18.2015

from ROOT import *
from ROOT import gROOT
from matplotlib import interactive
import os
#from ROOT import RooAbsPdf
#from ROOT import RooRealProxy
ROOT.gROOT.SetBatch(True)

# PU weights
#ROOT.gSystem.CompileMacro("/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_1_1/src/VHbb/plugins/PU.C")


# ===== Specify Input =====

# ggZH125
#file_gg = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/regression/jan_zll_genJet_CSV/v14_11_2015_ggZH125.root')
#file_gg = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/regression/jan_ttbar/v14_11_2015_ggZH125.root')


# ZH125
file = TFile('/exports/uftrig01a/dcurry/heppy/files/prep_out/regression_ttbar_quark_ZH125_v3.root')
#file = TFile('/exports/uftrig01a/dcurry/heppy/files/prep_out/regression_metTEST_ZH125_v2.root')


# Previous MC signal Ntuple:  
file_old = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/v14_11_2015_ZH125.root')

# Recent data ntuples
file_zuu = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/v14/Zuu.root')
#file_zuu = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/regression/fromPier/withRegression_allData.root')

file_zee = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/v13/Zee.root')

# Background samples
file_DY = TFile(' /exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/regression/fromPier/withRegression_DY_merged.root')

file_ZZ = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/sys_out/v14_11_2015_ZZ_ttbar_weights.root')

file_ttbar =  TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/regression/fromPier/withRegression_ttbar.root')


# latest ntuple version for labeling
new_version = 'v21_ZH_MET'
old_version = 'v14'

# Outpath:
outdir = 'validation_plots/'+new_version+'/'

if not os.path.exists(outdir):
        os.makedirs(outdir)

###########################################


# Get the trees
tree = file.Get('tree')
tree_old = file_old.Get('tree')
#tree_zuu = file_zuu.Get('tree')
#tree_zee = file_zee.Get('tree')
#tree_gg  = file_gg.Get('tree')
#tree_dy  = file_DY.Get('tree')
#tree_zz  = file_ZZ.Get('tree')
#tree_ttbar = file_ttbar.Get('tree')


header = '#sqrt{s}=13TeV,  ZH125: Z(l^{-}l^{+})H(b#bar{b})'
title = 'ZH125_'+new_version
gg_title = 'ggZH125_'+new_version

zuu_header = '#sqrt{s}=13TeV,   Data: Z(l^{-}l^{+})H(b#bar{b})' 
zuu_title = 'zuu_'+new_version

zee_header = '#sqrt{s}=13TeV,   Z(e^{-}e^{+})H(b#bar{b})'
zee_title ='zee_'+new_version

dy2b_header = '#sqrt{s}=13TeV,   Drell-Yan+2b'
dy2b_title  = 'DY2b_'+new_version

dy1b_header = '#sqrt{s}=13TeV,   Drell-Yan+1b'
dy1b_title  = 'DY1b_'+new_version

dylf_header = '#sqrt{s}=13TeV,   Drell-Yan+udcsg'
dylf_title  = 'DYlight_'+new_version

ttbar_header = '#sqrt{s}=13TeV,   ttbar'
ttbar_title  = 'ttbar_'+new_version

zz_header = '#sqrt{s}=13TeV,   ZZ'
zz_title  = 'ZZ_'+new_version

# create output directory
if (ROOT.gSystem.AccessPathName(outdir)):
    ROOT.gSystem.mkdir(outdir)


# List of variables to plot:  var name, # of bins, x-axis range
variable_list = [ ['HCSV_mass', 50, 20, 220],
                  ['HCSV_pt', 50, 20, 220],
                  ['Jet_pt[hJCidx[0]]', 50, 20, 220],
                  ['Jet_pt[hJCidx[1]]',50, 20, 220],
                  ['met_pt', 50, 0, 200],
                  #['Jet_mcPt[Jet_mcIdx[hJCidx[0]]]', 50, 20, 220],
                  #['Jet_mcPt[Jet_mcIdx[hJCidx[1]]]', 50, 20, 220],
                  ['Jet_eta[hJCidx[0]]', 50, -2.4, 2.4],
                  ['Jet_eta[hJCidx[1]]', 50, -2.4, 2.4],
                  ['Sum$(Jet_pt>20&Jet_puId!=0)', 16, 1, 16],
                  ['Jet_btagCSV', 20, 0, 1],
		  ['V_pt', 50, 0, 300],
		  ['V_mass', 50, 0, 200],
		  ['Jet_corr', 50, 0, 1.5],
		  ['vLeptons_pt', 50, 0, 200],
		  ['vLeptons_eta', 50, -2.4, 2.4],
		  ['rho', 25, 0, 25]
		  ]



regression_variable_list = [ ['Jet_mcPt', 50, 0, 150],
                             ['Jet_pt', 50, 0, 150],
                             ['Jet_rawPt', 50, 0, 150],
                             ['Jet_eta', 25, -2.4, 2.4],
                             ['rho', 25, 0, 25],
                             ['Jet_mass', 25, 0, 225],
                             ['Jet_leadTrackPt', 25, 0, 250],
                             ['Jet_leptonPtRel', 25, 0, 60],
                             ['Jet_leptonPt', 25, 0 , 250],
                             ['Jet_leptonDeltaR', 25, 0, 5],
                             ['Jet_chEmEF', 25, 0, 1],
                             ['Jet_chHEF', 25, 0, 1],
                             ['Jet_neHEF', 25, 0, 1],
                             ['Jet_neEmEF', 25, 0, 1],
                             ['Jet_chMult', 25, 0, 70],
                             ['Jet_vtxPt', 25, 0, 200],
                             ['Jet_vtxMass', 25, 0, 5],
                             ['Jet_vtx3DVal', 25, 0, 10],
                             ]


# ==== Cuts ==================
cut = 'Vtype > -1 & Vtype < 2 & Jet_pt[hJCidx[0]] > 20. & Jet_pt[hJCidx[1]] > 20. & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4'
    
cut = cut + ' & vLeptons_pt[0] > 20 & vLeptons_pt[1] > 20 & vLeptons_eta[0] < 2.4 & vLeptons_eta[1] < 2.4'

# btag cut.. experimental
cut = cut + ' & Jet_btagCSV[hJCidx[0]] > 0.8 & Jet_btagCSV[hJCidx[1]] > 0.8'

# Semi Leptonic Cut
#cut = cut + ' & Jet_leptonPt[hJCidx[0]] > 0 & Jet_leptonPt[hJCidx[1]] > 0'
#cut = cut + ' & Jet_leptonPt[hJCidx[0]] < 0 & Jet_leptonPt[hJCidx[1]] < 0'


# Regression cut for ZHf stacked plots
#cut = cut +' & (HLT_ZeeHbbAll == 1 | HLT_ZmmHbbAll == 1) & Vtype > -1 & Vtype < 2 & Jet_pt[hJCidx[0]] > 20 & Jet_pt[hJCidx[1]] > 20 & abs( HVdPhi ) > 2.9 & V_mass > 75. & V_mass < 105. & Jet_btagCSV[hJCidx[0]] > 0.89 & Jet_btagCSV[hJCidx[1]] > 0.605' 


# === Data Cut ===
zuu_cut = cut + ' & json == 1'

zuu_hf_cut = cut + ' & abs( HVdPhi ) > 2.9 & V_mass > 75. & V_mass < 105.'

zuu_ptBalance_cut = zuu_hf_cut +' & nJet == 2 & Jet_btagCSV[hJCidx[0]] > 0.97 & Jet_btagCSV[hJCidx[1]] > 0.6 & json == 1'


# === DY Cuts ===
DY_2b_cut= cut+' & Sum$(GenJet_pt>20 && abs(GenJet_eta)<2.4 && GenJet_numBHadrons>0)>=2'

DY_1b_cut = cut + ' & Sum$(GenJet_pt>20 && abs(GenJet_eta)<2.4 && GenJet_numBHadrons>0)==1'

DY_lf_cut = cut + ' & Sum$(GenJet_pt>20 && abs(GenJet_eta)<2.4 && GenJet_numBHadrons>0)==0'

#DY_hf_regression_cut = 'sign(genWeight)*('+hf_cut+')'

DY_1b_ptBalance_cut = DY_1b_cut +' & nJet == 2 & Jet_btagCSV[hJCidx[0]] > 0.6 & Jet_btagCSV[hJCidx[1]] > 0.6'
DY_1b_ptBalance_cut ='sign(genWeight)*('+DY_1b_ptBalance_cut+')'

DY_2b_ptBalance_cut = DY_2b_cut +' & nJet == 2 & Jet_btagCSV[hJCidx[0]] > 0.5 & Jet_btagCSV[hJCidx[1]] > 0.5'
DY_2b_ptBalance_cut ='sign(genWeight)*('+DY_2b_ptBalance_cut+')'

DY_lf_ptBalance_cut = DY_lf_cut +' & nJet == 2 & Jet_btagCSV[hJCidx[0]] > 0.5 & Jet_btagCSV[hJCidx[1]] > 0.5'
DY_lf_ptBalance_cut ='sign(genWeight)*('+DY_lf_ptBalance_cut+')'

ttbar_ptBalance_cut = cut +' & nJet == 2 & Jet_btagCSV[hJCidx[0]] > 0.5 & Jet_btagCSV[hJCidx[1]] > 0.5'
ttbar_ptBalance_cut = 'sign(genWeight)*('+ttbar_ptBalance_cut+')'

# ===============



ptBalance_cut = cut+' & nJet == 2 & Jet_btagCSV[hJCidx[0]] > 0.97 & Jet_btagCSV[hJCidx[1]] > 0.97'
#& json ==1'
ptBalance_cut = 'sign(genWeight)*('+ptBalance_cut+')'

mc_cut = 'sign(genWeight)*('+cut+')'
#mc_cut = cut

v14_mc_cut = 'weight2(nTrueInt)*sign(genWeight)*('+cut+')'
print mc_cut

res_cut = cut+' & Jet_btagCSV[hJCidx[0]] > 0.89 & Jet_btagCSV[hJCidx[1]] > 0.89'
res_cut = 'sign(genWeight)*('+res_cut+')'

zuu_cut = cut + ' & json == 1'
# & HLT_BIT_HLT_IsoMu24_eta2p1_v == 1'

zee_cut = cut + ' & json == 1 & HLT_BIT_HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v == 1'

resolution_cut = cut+' & Jet_mcPt>0 & abs(Jet_pt-Jet_mcPt)/Jet_mcPt < 1 & abs(Jet_pt_reg-Jet_mcPt)/Jet_mcPt < 1 & abs(Jet_mcFlavour) == 5' 

resolution_cut = 'sign(genWeight)*('+resolution_cut+')'

ttbar_cut = cut +' & HCSV_pt > 100 & (V_mass < 75 || V_mass > 120) & Jet_btagCSV[hJCidx[0]] > 0.97 & Jet_btagCSV[hJCidx[1]] > 0.6'



# Jet flavor cuts
bJet_cut = cut +' & abs(Jet_hadronFlavour) == 5 & Math::sqrt( (GenJet_eta-Jet_eta)*(GenJet_eta-Jet_eta) + (GenJet_phi-Jet_phi)*(GenJet_phi-Jet_phi) )<0.4'

lJet_cut = cut +' & abs(Jet_hadronFlavour) != 4 & abs(Jet_hadronFlavour) != 5 & Math::sqrt((GenJet_eta-Jet_eta)*(GenJet_eta-Jet_eta)+ (GenJet_phi-Jet_phi)*(GenJet_phi-Jet_phi))<0.2'

# DY+LF cut
#lf_cut = cut +' & HCSV_pt > 100 & V_pt > 100. & Sum$(Jet_pt > 20 & abs(Jet_eta) < 2.4) < 4 & abs( HVdPhi ) > 2.9 & V_mass > 75. & V_mass < 105. & max(Jet_btagCSV[hJCidx[0]],Jet_btagCSV[hJCidx[1]]) < 0.89'

#lf_cut = 'sign(genWeight)*('+lf_cut+')'

# ==== Now make the plots ====

def doPlot(variable, nbins, bin_low, bin_high):

    print '\n----> Making plot for', variable

    stack  = THStack('stack', '')
    canvas = TCanvas('canvas') 

    # make the histogram and project into it
    hNew = TH1F('hNew', '' , nbins, bin_low, bin_high)
    hOld = TH1F('hOld', '' , nbins, bin_low, bin_high)
    
    tree.Project('hNew', variable, mc_cut)
    tree_old.Project('hOld', variable, v14_mc_cut)
    
    hNew.SetStats(0)
    hNew.SetLineColor(kRed)
    hOld.SetLineColor(kBlue)
    
    # Normalize Entries
    hNew.Scale(1 / hNew.Integral())
    #hNew.Scale(1 / hNew.GetEntries())
    hOld.Scale(1 / hOld.Integral())
    #hOld.Scale(1 / hOld.GetEntries())

    canvas.cd()
    stack.Add(hNew)
    stack.Add(hOld)
    stack.Draw('nostack')
    stack.GetXaxis().SetTitle(variable)
    
    l = TLatex()
    l.SetNDC()
    l.SetTextSize(0.03)
    l.DrawLatex(0.1, 0.93, header)
    l.Draw('same')

    leg = TLegend(0.62,0.6,0.9,0.9)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(hNew, new_version, 'l')
    leg.AddEntry(hOld, old_version, 'l')
    leg.Draw('same')
    
    if '[hJCidx[0]]' in variable:
        variable = variable.replace('[hJCidx[0]]', '0')
    if '[hJCidx[1]]' in variable:
        variable = variable.replace('[hJCidx[1]]', '1')
    if 'Jet_puId' in variable:
        variable = variable.replace('Sum$(Jet_pt>20&Jet_puId!=0)', 'aJets')
    canvas.SaveAs(outdir+variable+'_'+title+'.pdf')
    canvas.SaveAs(outdir+variable+'_'+title+'.png')
    
    #raw_input('press return to continue')

    # Delete objects.
    canvas.IsA().Destructor(canvas)
    hNew.IsA().Destructor(hNew)
    hOld.IsA().Destructor(hOld)

# ====== end doPlot() =======




def reg_res_plots(variable, nbins, bin_low, bin_high):

     print '\n----> Making plot for', variable

          
     canvas_nom = TCanvas('canvas_nom')
     canvas_reg = TCanvas('canvas_reg')
      
     # make the histogram and project into it
     hNom = TH2F('hNom', '' , nbins, bin_low, bin_high, 50, -0.1, 0.1)
     hReg = TH2F('hReg', '' , nbins, bin_low, bin_high, 50, -0.1, 0.1)
     
     tree_gg.Project('hNom', '((Jet_pt-Jet_mcPt)/Jet_mcPt):%s'%(variable), resolution_cut)
     tree_gg.Project('hReg', '((Jet_pt_reg-Jet_mcPt)/Jet_mcPt):%s'%(variable), resolution_cut)

     # get the profiles
     prof_reg = hReg.ProfileX()
     prof_reg.SetLineColor(kBlack)
     prof_nom = hNom.ProfileX()
     prof_nom.SetLineColor(kBlack)

     
     canvas_reg.cd()
     hReg.SetStats(0)
     hReg.Draw('COLZ')
     prof_reg.Draw('same')
     hReg.GetXaxis().SetTitle(variable)
     hReg.GetYaxis().SetTitle('(Jet_pt_reg-Jet_mcPt)/Jet_mcPt')
     canvas_reg.SaveAs(outdir+'pt_resolution_REG_'+variable+'.pdf')
     
     canvas_nom.cd()
     hNom.SetStats(0)
     hNom.Draw('COLZ')
     prof_nom.Draw('same')
     hNom.GetXaxis().SetTitle(variable)
     hNom.GetYaxis().SetTitle('(Jet_pt-Jet_mcPt)/Jet_mcPt')
     canvas_nom.SaveAs(outdir+'pt_resolution_NOM_'+variable+'_'+gg_title+'.pdf')
     
     # Delete objects.
     canvas_reg.IsA().Destructor(canvas_reg)
     canvas_nom.IsA().Destructor(canvas_nom)
     hNom.IsA().Destructor(hNom)
     hReg.IsA().Destructor(hReg)
                         

# resolution plots



# function to compare regression and nominal H mass
# Give a tree to compare and header title

def regression_plot(myTree, myHeader, myTitle, ptRegion, myCut, myPtBalance_cut):

    print '\n----> Making regression comparative plot for...', myTitle

    if ptRegion == 'high': myTitle = myTitle+'_highPt'


    stack  = THStack('stack', '')
    canvas = TCanvas('canvas')

    # make the histogram and project into it
    hReg = TH1F('hReg', '' , 50, 20, 220)
    hNom = TH1F('hNom', '' , 50, 20, 220)
    hFsr = TH1F('hFsr', '' , 50, 20, 220)

    if ptRegion == 'all':
        #myTree.Project('hReg', 'HCSV_reg_mass', myCut)
        #myTree.Project('hNom', 'HCSV_mass', myCut)
        myTree.Project('hReg', 'H.mass', myCut)
        myTree.Project('hNom', 'HCSV_mass', myCut)
	#myTree.Project('hFsr', 'H.masswithFSR', myCut)

        
    if ptRegion == 'high':
        myTree.Project('hReg', 'H.mass', myCut+' & H.pt > 100')
        myTree.Project('hNom', 'HCSV_mass', myCut+' & HCSV_pt > 100')
	#myTree.Project('hFsr', 'H.masswithFSR', myCut+' & H.pt > 100')
        #myTree.Project('hReg', 'HCSV_reg_mass', myCut+' & HCSV_pt > 100')
        #myTree.Project('hNom', 'HCSV_mass', myCut+' & HCSV_pt > 100')

    hReg.SetStats(0)
    hReg.SetLineColor(kRed)
    hFsr.SetLineColor(kGreen)

    canvas.cd()
    stack.Add(hReg)
    stack.Add(hNom)
    #stack.Add(hFsr)
    stack.Draw('nostack')
    stack.GetXaxis().SetTitle('m(jj) [GeV]')
 
    low = 95
    high = 135

    low_nom = 80
    high_nom = 130

    if 'ZZ' in myTitle:
        low = 70
        high = 120
        low_nom = 60
        high_nom = 110


    # ==== Bukin Fit ====
    mjj13TeV=RooRealVar("mjj13TeV","M(jet-jet)", 20, 220, "GeV")
    bC_p0=RooRealVar("bC_p0", "bC_p0", 90., 130.)
    bC_p1=RooRealVar("bC_p1", "bC_p1", 0., 40.0)
    bC_p2=RooRealVar("bC_p2", "bC_p2", -100, 100.)
    bC_p3=RooRealVar("bC_p3", "bC_p3", -100., 100.)
    bC_p4=RooRealVar("bC_p4", "bC_p4", -100., 100.)
    bukin_ = RooBukinPdf("bukin_", "Bukin function",mjj13TeV, bC_p0,bC_p1,bC_p2,bC_p3,bC_p4)

    # regressed
    signalHistogram= RooDataHist("signalHistogram", "Signal Histogram", RooArgList(mjj13TeV), hReg)
    bukin_.fitTo(signalHistogram, RooFit.Range(20, 220), RooFit.Save())
    
    plot=mjj13TeV.frame();
    signalHistogram.plotOn(plot, RooFit.MarkerColor(2));
    bukin_.plotOn(plot, RooFit.LineColor(2), RooFit.LineWidth(0));
    plot.Draw("sames")
    
    hReg_std = bC_p1.getVal()
    hReg_mu = bC_p0.getVal()
    hReg_metric = hReg_std/hReg_mu
    hReg_std=str(round(hReg_std,4))
    hReg_mu=str(round(hReg_mu,4))
    hReg_metric_str = str(round(hReg_metric,3))

    # nominal
    signalHistogram2= RooDataHist("signalHistogram2", "Signal Histogram", RooArgList(mjj13TeV), hNom)
    signalHistogram2.plotOn(plot, RooFit.MarkerColor(1));
    
    bukin_.fitTo(signalHistogram2, RooFit.Range(20, 220), RooFit.Save())
    bukin_.plotOn(plot, RooFit.LineColor(1), RooFit.LineWidth(0));
    plot.Draw("sames")

    hNom_std=bC_p1.getVal()
    hNom_mu=bC_p0.getVal()
    mass_metric1 = hNom_std/hNom_mu
    hNom_std=str(round(hNom_std,4))
    hNom_mu=str(round(hNom_mu,4))
    mass_metric1_str = str(round(mass_metric1,3))

    # FSR
    signalHistogram3 = RooDataHist("signalHistogram3", "Signal Histogram", RooArgList(mjj13TeV), hFsr)
    bukin_.fitTo(signalHistogram3, RooFit.Range(20, 220), RooFit.Save())
    
    plot=mjj13TeV.frame();
    signalHistogram3.plotOn(plot, RooFit.MarkerColor(kGreen));
    bukin_.plotOn(plot, RooFit.LineColor(kGreen), RooFit.LineWidth(0));
    #plot.Draw("sames")
    
    hFsr_std = bC_p1.getVal()
    hFsr_mu = bC_p0.getVal()
    hFsr_metric = hFsr_std/hFsr_mu
    hFsr_std=str(round(hFsr_std,4))
    hFsr_mu=str(round(hFsr_mu,4))
    hFsr_metric_str = str(round(hFsr_metric,3))

    # Percent Improvemnt
    percent_improvement = 100*(1 - (hReg_metric/mass_metric1))
    
    l = TLatex()
    l.SetNDC()
    l.SetTextSize(0.03)
    l.DrawLatex(0.1, 0.93, myHeader)
    l.Draw('same')
 
    leg = TLegend(0.62,0.6,0.9,0.9)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(hReg, 'Regressed', 'l')
    leg.AddEntry(0, '#sigma='+hReg_std, '')
    leg.AddEntry(0, '#mu='+hReg_mu, '')
    #leg.AddEntry(0, '#sigma/#mu='+hReg_metric_str, '')
    leg.AddEntry(hNom, 'Nominal', 'l')
    leg.AddEntry(0, '#sigma='+hNom_std, '')
    leg.AddEntry(0, '#mu='+hNom_mu, '')
    #leg.AddEntry(hFsr, 'Regressed+FSR', 'l')
    #leg.AddEntry(0, '#sigma='+hFsr_std, '')
    #leg.AddEntry(0, '#mu='+hFsr_mu, '')
    #leg.AddEntry(0, '#sigma/#mu='+mass_metric1_str, '')
    leg.AddEntry(0, '', '')
    x = leg.AddEntry(0, 'Improvement='+str(round(percent_improvement,1))+'%', '')
    x.SetTextColor(kRed)
    x.SetTextSize(0.03)
    leg.Draw('same')


    canvas.SaveAs(outdir+'regressed_Mass_'+myTitle+'.pdf')

    # Delete objects.
    canvas.IsA().Destructor(canvas)
    hReg.IsA().Destructor(hReg)
    hNom.IsA().Destructor(hNom)
    
    '''
    # ==== Now the pt balance =====
    stack  = THStack('stack', '')
    canvas = TCanvas('canvas')

    # make the histogram and project into it
    hReg = TH1F('hReg', '' , 20, 0, 2)
    hNom = TH1F('hNom', '' , 20, 0, 2)
    hFsr = TH1F('hFsr', '' , 20, 0, 2)
    
    if ptRegion == 'all':
	    myTree.Project('hReg', 'H.pt/V_pt', myPtBalance_cut)
	    myTree.Project('hNom', 'HNoReg.pt/V_pt', myPtBalance_cut)
	    myTree.Project('hFsr', 'H.ptwithFSR/V_pt', myPtBalance_cut)
            #myTree.Project('hReg', 'HCSV_reg_pt/V_pt', myCut)
            #myTree.Project('hNom', 'HCSV_pt/V_pt', myCut)
        

    if ptRegion == 'high':
	    myTitle = myTitle+'_highPt'
	    myTree.Project('hReg', 'H.pt/V_pt', myPtBalance_cut+' & H.pt > 100')
	    myTree.Project('hNom', 'HNoReg.pt/V_pt', myPtBalance_cut+' & HNoReg.pt > 100')
	    myTree.Project('hFsr', 'H.ptwithFSR/V_pt', myPtBalance_cut+' & H.ptwithFSR > 100')

    hReg.SetStats(1)
    hReg.SetLineColor(kRed)
    hFsr.SetLineColor(kGreen)
    
    canvas.cd()
    stack.Add(hReg)
    stack.Add(hNom)
    stack.Add(hFsr)
    stack.Draw('nostack')
    stack.GetXaxis().SetTitle('Pt Balance: p_{T}(jj) / p_{T}(ll)')
    stack.GetYaxis().SetTitle('Entries/0.13')
   
    # ==== Bukin Fit ====
    ptBal = RooRealVar("ptBal","M(jet-jet)",0,2,"GeV")
    bC_p0=RooRealVar("bC_p0", "bC_p0", 0., 2.)
    bC_p1=RooRealVar("bC_p1", "bC_p1", 0, 2.0)
    bC_p2=RooRealVar("bC_p2", "bC_p2", -1, 2.1)
    bC_p3=RooRealVar("bC_p3", "bC_p3", -1., 2.)
    bC_p4=RooRealVar("bC_p4", "bC_p4", -1., 2.)
    bukin_ = RooBukinPdf("bukin_", "Bukin function", ptBal, bC_p0,bC_p1,bC_p2,bC_p3,bC_p4)

    signalHistogram= RooDataHist("signalHistogram", "Signal Histogram", RooArgList(ptBal), hReg)
    bukin_.fitTo(signalHistogram, RooFit.Range(0.6, 2), RooFit.Save())
        
    plot = ptBal.frame();
    signalHistogram.plotOn(plot, RooFit.MarkerColor(2));
    bukin_.plotOn(plot, RooFit.LineColor(2), RooFit.LineWidth(0));
    plot.Draw("sames")
    
    hReg_std = bC_p1.getVal()
    hReg_mu = bC_p0.getVal()
    hReg_metric = hReg_std/hReg_mu
    hReg_std=str(round(hReg_std,4))
    hReg_mu=str(round(hReg_mu,4))
    hReg_metric_str = str(round(hReg_metric,3))
    
    signalHistogram2= RooDataHist("signalHistogram2", "Signal Histogram", RooArgList(ptBal), hNom)
    signalHistogram2.plotOn(plot, RooFit.MarkerColor(1));
    
    bukin_.fitTo(signalHistogram2, RooFit.Range(0, 2), RooFit.Save())
    bukin_.plotOn(plot, RooFit.LineColor(1), RooFit.LineWidth(0));
    plot.Draw("sames")
    
    hNom_std=bC_p1.getVal()
    hNom_mu=bC_p0.getVal()
    mass_metric1 = hNom_std/hNom_mu
    hNom_std=str(round(hNom_std,4))
    hNom_mu=str(round(hNom_mu,4))
    mass_metric1_str = str(round(mass_metric1,3))

    # FSR
    signalHistogram3= RooDataHist("signalHistogram3", "Signal Histogram", RooArgList(ptBal), hFsr)
    signalHistogram3.plotOn(plot, RooFit.MarkerColor(kGreen));
    
    bukin_.fitTo(signalHistogram3, RooFit.Range(0, 2), RooFit.Save())
    bukin_.plotOn(plot, RooFit.LineColor(kGreen), RooFit.LineWidth(0));
    plot.Draw("sames")
    
    hFsr_std=bC_p1.getVal()
    hFsr_mu=bC_p0.getVal()
    mass_metric1 = hFsr_std/hFsr_mu
    hFsr_std=str(round(hFsr_std,4))
    hFsr_mu=str(round(hFsr_mu,4))
    mass_metric1_str = str(round(mass_metric1,3))
    
    l = TLatex()
    l.SetNDC()
    l.SetTextSize(0.03)
    l.DrawLatex(0.1, 0.93, myHeader)
    l.Draw('same')

    leg = TLegend(0.62,0.6,0.9,0.9)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(hReg, 'Regressed', 'l')
    leg.AddEntry(0, 'RMS='+hReg_std, '')
    leg.AddEntry(0, 'Mean='+hReg_mu, '')
    #leg.AddEntry(0, '#sigma/#mu='+hReg_metric_str, '')
    leg.AddEntry(hNom, 'Nominal', 'l')
    leg.AddEntry(0, 'RMS='+hNom_std, '')
    leg.AddEntry(0, 'Mean='+hNom_mu, '')

    leg.AddEntry(hNom, 'Regressed+FSR', 'l')
    leg.AddEntry(0, 'RMS='+hFsr_std, '')
    leg.AddEntry(0, 'Mean='+hFsr_mu, '')
    
    #leg.AddEntry(0, '#sigma/#mu='+mass_metric1_str, '')
    leg.AddEntry(0, '', '')
    #x = leg.AddEntry(0, 'Improvement='+str(round(percent_improvement,1))+'%', '')
    #x.SetTextColor(kRed)
    #x.SetTextSize(0.03)
    leg.Draw('same')
    
    canvas.SaveAs(outdir+'pt_balance_'+myTitle+'.pdf')


    # Jet_corr compare plots
    #stack  = THStack('stack', '')
    #canvas = TCanvas('canvas')
    
    # make the histogram and project into it
    #hMC = TH1F('hMC', '' , 35, 0, 2)
    #hdata = TH1F('hdata', '' , 35, 0, 2)
    
    #myTree.Project('hMC', 'Jet_corr', ttbar_cut)
    #myTree.Project('hMC', 'Jet_pt/Jet_rawPt', mc_cut)
    #tree_zuu.Project('hdata', 'Jet_pt/Jet_rawPt', zuu_cut)

    #hMC.Scale(1 / hMC.Integral())
    #hdata.Scale(1 / hdata.Integral())
    
    #hMC.SetStats(0)
    #hMC.SetLineColor(kRed)
    
    #canvas.cd()
    #stack.Add(hMC)
    #stack.Add(hdata)
    #stack.Draw('nostack')
    #stack.GetXaxis().SetTitle('Jet_corr')
    
    #leg = TLegend(0.62,0.6,0.9,0.9)
    #leg.SetFillStyle(0)
    #leg.SetBorderSize(0)
    #leg.AddEntry(hMC, 'MC', 'l')
    #leg.AddEntry(hdata, 'Data', 'l')
    #leg.Draw('same')
    
    #canvas.SaveAs(outdir+'jet_corr_'+myTitle+'.pdf')
        
    # Resoltuion for B, and light Jets
    stack_b  = THStack('stack_b', '')
    canvas_b = TCanvas('canvas_b')
    
    # make the histogram and project into it
    low  = -1 
    high = 1
    nbins = 35
    
    hReg_b = TH1F('hReg_b', '' , nbins, low, high)
    hNom_b = TH1F('hNom_b', '' , nbins, low, high)
    
    temp_cut = res_cut+' & Jet_mcIdx > -1 & Jet_mcIdx < 15 & hJCidx > -1'
    #& abs(Jet_hadronFlavour[Jet_mcIdx[hJCidx[1]]]) != 4 & abs(Jet_hadronFlavour[Jet_mcIdx[hJCidx[1]]]) != 5'
    
    
    if ptRegion == 'all':
	    myTree.Project('hReg_b', '(hJet_pt_REG[0]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]', temp_cut)
	    myTree.Project('hNom_b', '(hJet_pt[0]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]', temp_cut)
	    #myTree.Project('hReg_b', '(hJet_pt_REG[1]-Jet_mcPt[1])/Jet_mcPt[1]', temp_cut)
	    #myTree.Project('hNom_b', '(hJet_pt[0]-Jet_mcPt[0])/Jet_mcPt[0]', temp_cut)
	    

    if ptRegion == 'high':
	    myTree.Project('hReg_b', '(Jet_pt_REG[0]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]', temp_cut+' & H.pt > 100')
	    myTree.Project('hNom_b', '(Jet_pt[hJCidx[0]]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]', temp_cut+' & HNoReg.pt > 100')
	    #myTree.Project('hReg_b', '(hJet_pt_REG-Jet_mcPt)/Jet_mcPt', res_cut +' & H.pt > 100')
	    #myTree.Project('hNom_b', '(hJet_pt-Jet_mcPt)/Jet_mcPt', res_cut+' & HNoReg.pt > 100')
	    

    #hReg_b.Scale(1 / hReg_b.Integral())
    #hNom_b.Scale(1 / hNom_b.Integral())

    canvas_b.cd()
    hReg_b.SetStats(0)
    hReg_b.SetLineColor(kRed)
    stack_b.Add(hReg_b)
    stack_b.Add(hNom_b)
    stack_b.Draw('nostack')
    stack_b.GetXaxis().SetTitle(' (Jet_pt-gen_pt)/gen_pt')
        
    res = RooRealVar("res","res",-1,1,"GeV")
    bC_p0=RooRealVar("bC_p0", "bC_p0", -0.5, 0.5)
    bC_p1=RooRealVar("bC_p1", "bC_p1", 0., 0.5)
    bC_p2=RooRealVar("bC_p2", "bC_p2", -1, 1.)
    bC_p3=RooRealVar("bC_p3", "bC_p3", -1., 1.)
    bC_p4=RooRealVar("bC_p4", "bC_p4", -1., 1.)
    bukin_ = RooBukinPdf("bukin_", "Bukin function", res, bC_p0,bC_p1,bC_p2,bC_p3,bC_p4)

    signalHistogram= RooDataHist("signalHistogram", "Signal Histogram", RooArgList(res), hReg_b)
    bukin_.fitTo(signalHistogram, RooFit.Range(-1, 1), RooFit.Save())
        
    plot = res.frame();
    signalHistogram.plotOn(plot, RooFit.MarkerColor(2));
    bukin_.plotOn(plot, RooFit.LineColor(2), RooFit.LineWidth(0));
    plot.Draw("sames")
       
    hReg_std = bC_p1.getVal()
    hReg_mu = bC_p0.getVal()
    hReg_metric = hReg_std/hReg_mu
    hReg_std=str(round(hReg_std,4))
    hReg_mu=str(round(hReg_mu,4))
    hReg_metric_str = str(round(hReg_metric,3))
    
    signalHistogram2= RooDataHist("signalHistogram2", "Signal Histogram", RooArgList(res), hNom_b)
    signalHistogram2.plotOn(plot, RooFit.MarkerColor(1));
    
    bukin_.fitTo(signalHistogram2, RooFit.Range(-1, 1), RooFit.Save())
    bukin_.plotOn(plot, RooFit.LineColor(1), RooFit.LineWidth(0));
    plot.Draw("sames")

    hNom_std=bC_p1.getVal()
    hNom_mu=bC_p0.getVal()
    mass_metric1 = hNom_std/hNom_mu
    hNom_std=str(round(hNom_std,4))
    hNom_mu=str(round(hNom_mu,4))
    mass_metric1_str = str(round(mass_metric1,3))

    l = TLatex()
    l.SetNDC()
    l.SetTextSize(0.03)
    l.DrawLatex(0.1, 0.93, myHeader)
    l.Draw('same')

    leg = TLegend(0.62,0.6,0.9,0.9)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(hReg, 'Regressed', 'l')
    leg.AddEntry(0, 'RMS='+hReg_std, '')
    leg.AddEntry(0, 'Mean='+hReg_mu, '')
    #leg.AddEntry(0, '#sigma/#mu='+hReg_metric_str, '')
    leg.AddEntry(hNom, 'Nominal', 'l')
    leg.AddEntry(0, 'RMS='+hNom_std, '')
    leg.AddEntry(0, 'Mean='+hNom_mu, '')
    #leg.AddEntry(0, '#sigma/#mu='+mass_metric1_str, '')
    leg.AddEntry(0, '', '')
    #x = leg.AddEntry(0, 'Improvement='+str(round(percent_improvement,1))+'%', '')
    #x.SetTextColor(kRed)
    #x.SetTextSize(0.03)
    leg.Draw('same')

    canvas_b.SaveAs(outdir+'jet_res_bJets_'+myTitle+'.pdf')



    # 2D Resoultion Plot 
    canvas_nom = TCanvas('canvas_nom')
    canvas_reg = TCanvas('canvas_reg')
    
    hNom = TH2F('hNom', '' , 20, 0.96, 1, 20, -0.1, 0.1)
    hReg = TH2F('hReg', '' , 20, 0.96, 1, 20, -0.1, 0.1)


    #temp_cut = res_cut+' & Jet_mcIdx > -1 & Jet_mcIdx < 15 & hJCidx > -1'
    #& abs(Jet_hadronFlavour[Jet_mcIdx[hJCidx[0]]]) == 5'
    #& abs(Jet_hadronFlavour[Jet_mcIdx[hJCidx[1]]]) != 4 & abs(Jet_hadronFlavour[Jet_mcIdx[hJCidx[1]]]) != 5'
    
    myTree.Project('hNom', '(Jet_pt_REG[0]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]:Jet_btagCSV[hJCidx[0]]', myCut)
    myTree.Project('hReg', '(Jet_pt[hJCidx[0]]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]:Jet_btagCSV[hJCidx[0]]', myCut)

    #myTree.Project('hNom', '(Jet_pt_REG[0]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]:Jet_btagCSV[hJCidx[0]]', temp_cut)
    #myTree.Project('hReg', '(Jet_pt[hJCidx[0]]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]:Jet_btagCSV[hJCidx[0]]',temp_cut)
    
    # get the profiles
    prof_reg = hReg.ProfileX()
    prof_reg.SetLineColor(kBlack)
    prof_nom = hNom.ProfileX()
    prof_nom.SetLineColor(kBlack)
    
    canvas_reg.cd()
    hReg.SetStats(0)
    hReg.Draw('COLZ')
    prof_reg.Draw('same')
    hReg.GetXaxis().SetTitle('Jet CSV, regressed')
    hReg.GetYaxis().SetTitle('(Jet_pt_reg-Jet_mcPt)/Jet_mcPt')
    canvas_reg.SaveAs(outdir+'2d_jet_regressed_resolution_'+myTitle+'.pdf')

    canvas_nom.cd()
    hNom.SetStats(0)
    hNom.Draw('COLZ')
    prof_nom.Draw('same')
    hNom.GetXaxis().SetTitle('Jet CSV, nominal')
    hNom.GetYaxis().SetTitle('(Jet_pt-Jet_mcPt)/Jet_mcPt')
    canvas_nom.SaveAs(outdir+'2d_jet_nominal_resolution_'+myTitle+'.pdf')
    
    '''

# ===== End regression plots ======


# ===== VType Plots ======

def vtype_plot(myTree, myTitle, ptRegion, myCut):

    canvas = TCanvas('canvas')
    stack  = THStack('stack', '')
        
    # make the histogram and project into it
    h = TH1F('h', '' , 7, -1, 6)
    
    if ptRegion == 'all':
        myTree.Project('h', 'Vtype', myCut)
        myTitle = myTitle+'_allPt'
        
    if ptRegion == 'high':
        myTitle = myTitle+'_highPt'
        myTree.Project('h', 'Vtype', myCut+' & V_pt > 150')
        
    canvas.cd()
    stack.Add(h)
    stack.Draw('nostack')
    stack.GetXaxis().SetTitle('VType')
    
    canvas.SaveAs(outdir+'VType_'+myTitle+'.pdf')
    
# ===== End VType Plots ======



# =====================================================================================

# Loop over variable list and plot for v13 comparison
for variable in variable_list:

    break
    #if variable[0] is not 'HCSV_mass': continue

    # arguments are: var name, nBins, bin low, bin high
    doPlot(variable[0], variable[1], variable[2], variable[3])



# Loop for resolution plots
for variable in regression_variable_list:

	
    #if variable[0] is not 'Jet_pt': continue
    break
    #  Argumentas are: reg_res_plots(variable, nbins, bin_low, bin_high)
    reg_res_plots(variable[0], variable[1], variable[2], variable[3])

# resolution plots



    
# Make regression plots for data and MC 
# (tree, header, plot title, pt region, cut)

regression_plot(tree, header, title, 'all', mc_cut, ptBalance_cut)
regression_plot(tree, header, title, 'high', mc_cut, ptBalance_cut)

#regression_plot(tree_gg, header, gg_title, 'all', mc_cut, ptBalance_cut)
#regression_plot(tree_gg, header, gg_title, 'high', mc_cut, ptBalance_cut)

#regression_plot(tree_zuu, zuu_header, zuu_title, 'all', zuu_cut, zuu_ptBalance_cut)

#regression_plot(tree_dy, dy2b_header, dy2b_title, 'all', DY_2b_cut, DY_2b_ptBalance_cut)

#regression_plot(tree_dy, dy1b_header, dy1b_title, 'all', DY_1b_cut, DY_1b_ptBalance_cut)

#regression_plot(tree_dy, dylf_header, dylf_title, 'all', DY_lf_cut, DY_lf_ptBalance_cut)

#regression_plot(tree_ttbar, ttbar_header, ttbar_title, 'all', ttbar_ptBalance_cut, ttbar_ptBalance_cut)


#regression_plot(tree_zz, zz_header, zz_title, 'all', mc_cut)
#regression_plot(tree_zz, zz_header, zz_title, 'high', mc_cut)

#regression_plot(tree_zuu, zuu_header, zuu_title, 'all', zuu_cut)
#regression_plot(tree_zuu, zuu_header, zuu_title, 'high', zuu_cut)

#regression_plot(tree_zee, zee_header, zee_title, 'all', zee_cut)
#regression_plot(tree_zee, zee_header, zee_title, 'high', zee_cut)

'''
# Make data vType Plots: (zee tree, zuu tree, ptRegion)
vtype_plot(tree_zee, zee_title, 'all', zee_cut)
vtype_plot(tree_zee, zee_title, 'high', zee_cut)
vtype_plot(tree_zuu, zuu_title, 'all', zuu_cut)
vtype_plot(tree_zuu, zuu_title, 'high', zuu_cut)
'''

'''
# Some quick plotting
c1 = TCanvas('c1')
s1 = THStack('s1', '')
h1 = TH1F('h1', '' , 50, 0, 200)
h2 = TH1F('h2', '' , 50, 0, 200)

tree.Project('h1', 'GenBQuarkFromH_pt')
tree.Project('h2', 'GenJet_wNuPt')


h2.SetLineColor(kRed)
s1.Add(h1)
s1.Add(h2)
s1.Draw('nostack')
'''

print '\n\n\t ========== Plotting Finished =========='


raw_input('press return to continue')
     
     
