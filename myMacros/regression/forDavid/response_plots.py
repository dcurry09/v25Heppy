###########################################
# Plot Maker for quick plots
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


# Root file of Histograms
#file = TFile('response_plots/ttbar_quark_v21.root')
file = TFile('response_plots/ttbar_v23.root')

outdir = 'response_plots/ttbar_ntuple_v23/'

regression_variable_list = [ #['Jet_mcPt', 50, 0, 150],
                             ['Jet_pt', 50, 0, 150],
                             ['Jet_corr', 50, 0, 3],
                             ['Jet_eta', 25, -2.4, 2.4],
                             ['nPvs', 25, 0, 25],
                             ['Jet_mt', 25, 0, 225],
                             ['Jet_leadTrackPt', 25, 0, 250],
                             ['Jet_leptonPtRel', 25, 0, 60],
                             ['Jet_leptonPt', 25, 0 , 250],
                             ['Jet_leptonDeltaR', 25, 0, 5],
                             #['Jet_chEmEF', 25, 0, 1],
                             ['Jet_chHEF', 25, 0, 1],
                             ['Jet_neHEF', 25, 0, 1],
                             ['Jet_neEmEF', 25, 0, 1],
                             #['Jet_chMult', 25, 0, 70],
                             ['Jet_vtxPt', 25, 0, 200],
                             ['Jet_vtxMass', 25, 0, 5],
                             ['Jet_vtx3dL', 25, 0, 10],
                             ['Jet_vtxNtrk', 25, 0, 10],
                             ['Jet_vtx3deL', 25, 0, 10],
                             ]



def reg_res_plots(variable, nbins, bin_low, bin_high):

     print '\n----> Making plot for', variable


     canvas_nom = TCanvas('canvas_nom')
     canvas_reg = TCanvas('canvas_reg')

     # Get the TH2F from the root file
     hReg = file.Get(variable)
     hNom = file.Get(variable+'_noReg')

     # make the histogram and project into it
     #hNom = TH2F('hNom', '' , nbins, bin_low, bin_high, 50, -0.1, 0.1)
     #hReg = TH2F('hReg', '' , nbins, bin_low, bin_high, 50, -0.1, 0.1)

     #tree_gg.Project('hNom', '((Jet_pt-Jet_mcPt)/Jet_mcPt):%s'%(variable), resolution_cut)
     #tree_gg.Project('hReg', '((Jet_pt_reg-Jet_mcPt)/Jet_mcPt):%s'%(variable), resolution_cut)

     # get the profiles
     prof_reg = hReg.ProfileX()
     prof_reg.SetLineColor(kRed)
     prof_reg.SetLineWidth(4)
     prof_nom = hNom.ProfileX()
     prof_nom.SetLineColor(kBlack)
     prof_nom.SetLineWidth(4)

     canvas_reg.cd()
     hReg.SetStats(0)
     #hReg.Draw('COLZ')
     hReg.Draw('BOX')
     prof_reg.Draw('same')
     prof_nom.Draw('same')
     hReg.GetXaxis().SetTitle(variable)
     hReg.GetYaxis().SetTitle('(Jet_pt-genJet_pt)/genJet_pt')
     canvas_reg.SaveAs(outdir+'/'+variable+'_pt_resolution_REG.pdf')
     canvas_reg.SaveAs(outdir+'/'+variable+'_pt_resolution_REG.png')

     #canvas_nom.cd()
     #hNom.SetStats(0)
     #hNom.Draw('COLZ')
     #prof_nom.Draw('same')
     #hNom.GetXaxis().SetTitle(variable)
     #hNom.GetYaxis().SetTitle('(Jet_pt-Jet_mcPt)/Jet_mcPt')
     #canvas_nom.SaveAs(outdir+'pt_resolution_NOM.pdf')

     #raw_input('..enter')
     
     # Delete objects.
     canvas_reg.IsA().Destructor(canvas_reg)
     canvas_nom.IsA().Destructor(canvas_nom)
     hNom.IsA().Destructor(hNom)
     hReg.IsA().Destructor(hReg)


# resolution plots

# Loop for resolution plots
for variable in regression_variable_list:

    #if variable[0] is not 'Jet_pt': continue
    #break
    #  Argumentas are: reg_res_plots(variable, nbins, bin_low, bin_high)
    reg_res_plots(variable[0], variable[1], variable[2], variable[3])

# resolution plots
