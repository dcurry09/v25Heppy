#!/usr/bin/env python

import ROOT
import os
from ROOT import *

ROOT.gROOT.SetBatch(True)

infile = ROOT.TFile.Open('/exports/uftrig01a/dcurry/heppy/files/prep_out/v23_7_18_ZH125.root')
tree = infile.Get("tree")

cut = 'Vtype > -1 & Vtype < 2 & Jet_pt[hJCidx[0]] > 20. & Jet_pt[hJCidx[1]] > 20. & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4'

cut = cut + ' & vLeptons_pt[0] > 20 & vLeptons_pt[1] > 20 & vLeptons_eta[0] < 2.4 & vLeptons_eta[1] < 2.4'

path = '/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/myMacros/validation_plots/plots/btag_profiles/'
outpath = '/afs/cern.ch/user/d/dcurry/www/80x_validation/btag_profiles/'

# Make the dir and copy the website ini files
try:
    os.system('mkdir '+outpath)
except:
     print outpath+' already exists...'

temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outpath

os.system(temp_string2)
os.system(temp_string3)




variables = ['Jet_btagWeightCSV',
             'Jet_btagWeightCSV_up_jes',
             'Jet_btagWeightCSV_up_lf',
             'Jet_btagWeightCSV_down_lf',
             'Jet_btagWeightCSV_up_hf',
             'Jet_btagWeightCSV_down_hf',
             'Jet_btagWeightCSV_up_hfstats1',
             'Jet_btagWeightCSV_down_hfstats1',
             'Jet_btagWeightCSV_up_hfstats2',
             'Jet_btagWeightCSV_down_hfstats2',
             'Jet_btagWeightCSV_up_lfstats1',
             'Jet_btagWeightCSV_down_lfstats1',
             'Jet_btagWeightCSV_up_lfstats2',
             'Jet_btagWeightCSV_down_lfstats2',
             'Jet_btagWeightCSV_up_cferr1',
             'Jet_btagWeightCSV_down_cferr1',
             'Jet_btagWeightCSV_up_cferr2',
             'Jet_btagWeightCSV_down_cferr2'
             ]


y_variables = ['Jet_eta', 'Jet_pt']

for var in variables:


    print("Drawing %s" %(var))

    cEta = TCanvas('cEta')
    cPt  = TCanvas('cPt')
    
    # make the histogram and project into it
    hEta = TH2F('hEta', '' , 30, 0.5, 1.5, 30, -2.4, 2.4)
    hPt  = TH2F('hPt', '' , 30, 0.5, 1.5, 30, 20, 120)

    #tree.Draw("Jet_eta:%s >> %s(25,0.5,1.5)"%(var,var),cut,"goff")

    tree.Project('hEta', 'Jet_eta:%s'%(var), cut)
    tree.Project('hPt', 'Jet_pt:%s'%(var), cut)

    # get the profiles
    prof_eta = hEta.ProfileX()
    prof_eta.SetLineColor(kBlack)
    prof_eta.SetLineWidth(2)
    prof_pt  = hPt.ProfileX()
    prof_pt.SetLineColor(kBlack)
    prof_pt.SetLineWidth(2)
     

    cEta.cd()
    hEta.SetStats(0)
    hEta.Draw('COLZ')
    prof_eta.Draw('same')
    hEta.GetXaxis().SetTitle(var)
    hEta.GetYaxis().SetTitle('Jet #eta')
    cEta.SaveAs(outpath+"profiled_%s_eta.pdf" %(var))
    cEta.SaveAs(outpath+"profiled_%s_eta.png" %(var))

    cPt.cd()
    hPt.SetStats(0)
    hPt.Draw('COLZ')
    prof_pt.Draw('same')
    hPt.GetXaxis().SetTitle(var)
    hPt.GetYaxis().SetTitle('Jet pT')
    cPt.SaveAs(outpath+"profiled_%s_pt.pdf" %(var))
    cPt.SaveAs(outpath+"profiled_%s_pt.png" %(var))
    

    # Delete objects.
    cEta.IsA().Destructor(cEta)
    cPt.IsA().Destructor(cPt)
    hEta.IsA().Destructor(hEta)
    hPt.IsA().Destructor(hPt)






