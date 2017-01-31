#!/usr/bin/env python

import ROOT

ROOT.gROOT.SetBatch(True)

#target = '(Jet_pt-Jet_mcPt)/Jet_mcPt'
#target = '(Jet_pt[hJCidx[0]]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]'

#target_reg = '(Jet_reg_pt-Jet_mcPt)/Jet_mcPt'
#target_reg = '(Jet_pt_reg[hJCidx[0]]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]'


cut = 'Jet_mcIdx > -1 & Jet_mcIdx < 15 & hJCidx > -1 & Vtype > -1 & Vtype < 2 & Jet_pt[hJCidx[0]] > 20. & Jet_pt[hJCidx[1]] > 20. & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4'

cut = cut + ' & vLeptons_pt[0] > 20 & vLeptons_pt[1] > 20 & vLeptons_eta[0] < 2.4 & vLeptons_eta[1] < 2.4'

# btag cut.. experimental
#cut = cut + ' & Jet_btagCSV[hJCidx[0]] > 0.6 & Jet_btagCSV[hJCidx[1]] > 0.6'

cut = cut + ' & ((Jet_pt_reg[hJCidx[0]]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]) < 1'

print cut

variables = ['GenJet_wNuPt','Jet_corr','Jet_eta','rho','Jet_mass','Jet_leadTrackPt','Jet_leptonPtRel','Jet_leptonPt','Jet_leptonDeltaR','Jet_neHEF','Jet_neEmEF','Jet_chMult','Jet_vtxPt','Jet_vtxMass','Jet_vtx3DVal','Jet_vtxNtrk','Jet_vtx3DSig']

infile = ROOT.TFile.Open('/exports/uftrig01a/dcurry/heppy/files/prep_out/v23_7_18_ZH125.root')

tree = infile.Get("tree")

for var in variables:

	print("Drawing %s" %(var))

	tree.Draw("%s:%s >> %s"%(target_reg,var,var),cut,"goff")

	histo = infile.Get(var)
	histo.ProfileY()

	print("Profiling")

	profiled_histo = infile.Get("%s_pfy" %(var))

        print("creating a Canvas")

	c = ROOT.TCanvas(var,'', 600, 600)	
	histo.GetYaxis().SetTitle(target)
	histo.GetXaxis().SetTitle(var)
	histo.Draw('Box')
	profiled_histo.Draw("same")

	print("Saving the pdf file")

 	c.Print("plots/profiled_%s.pdf" %(var))
