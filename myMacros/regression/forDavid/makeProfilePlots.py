#!/usr/bin/env python

#import ROOT
from ROOT import *
from ROOT import gROOT
from matplotlib import interactive

ROOT.gROOT.SetBatch(True)

#target = '(Jet_pt-Jet_mcPt)/Jet_mcPt'
target = '(hJet_pt[0]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]'

#target_reg = '(Jet_reg_pt-Jet_mcPt)/Jet_mcPt'
target_reg = '(hJet_pt_REG[0]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]'


cut = 'Jet_mcIdx > -1 & Jet_mcIdx < 15 & hJCidx > -1 & Vtype > -1 & Vtype < 2 & Jet_pt[hJCidx[0]] > 20. & Jet_pt[hJCidx[1]] > 20. & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4'

cut = cut + ' & vLeptons_pt[0] > 20 & vLeptons_pt[1] > 20 & vLeptons_eta[0] < 2.4 & vLeptons_eta[1] < 2.4'

# btag cut.. experimental
cut = cut + ' & Jet_btagCSV[hJCidx[0]] > 0.9 & Jet_btagCSV[hJCidx[1]] > 0.9'

cut = cut + ' & abs((hJet_pt_REG[0]-GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]])/GenJet_wNuPt[Jet_mcIdx[hJCidx[0]]]) < 0.4'

print cut

variables = ['GenJet_wNuPt', 'Jet_pt', 'Jet_corr','Jet_eta','rho','Jet_mass','Jet_leadTrackPt','Jet_leptonPtRel','Jet_leptonPt','Jet_leptonDeltaR','Jet_neHEF','Jet_neEmEF','Jet_chMult','Jet_vtxPt','Jet_vtxMass','Jet_vtx3DVal','Jet_vtxNtracks','Jet_vtx3DSig']

#variables = ['Jet_eta']

infile = TFile.Open('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/regression/feb_zll_genJet/v14_11_2015_ggZH125.root')

tree = infile.Get("tree")

for var in variables:



	print("Drawing %s" %(var))

	if var == 'Jet_eta':
		tree.Draw("%s:%s >> %s"%(target_reg,var,var), cut, "goff")
		# make the nominal version
		tree.Draw("%s:%s >> %s"%(target,var,var+'_nom'), cut, "goff")
	
		
	else:
		if 'Pt' in var or 'pt' in var:
			tree.Draw("%s:%s >> %s"%(target_reg,var,var), cut+' & %s>0 & %s<250'%(var,var),"goff")
			# make the nominal version
			tree.Draw("%s:%s >> %s"%(target,var,var+'_nom'),cut+' & %s>0 & %s<250'%(var,var),"goff")
		else:	
			tree.Draw("%s:%s >> %s"%(target_reg,var,var), cut+' & %s>0'%(var),"goff")
			# make the nominal version
			tree.Draw("%s:%s >> %s"%(target,var,var+'_nom'),cut+' & %s>0'%(var),"goff")

	

	histo = infile.Get(var)
	histo.ProfileX()
	
	print("Profiling")
	
	profiled_histo = infile.Get("%s_pfx" %(var))

        print("creating a Canvas")
	c = TCanvas(var,'', 600, 600)	
	histo.SetStats(0)
	histo.GetYaxis().SetTitle('(Jet pT - GenJet pT)/GenJet pT')
	histo.GetXaxis().SetTitle(var)
	histo.Draw('BOX')
	profiled_histo.Draw('same')
	
	histo_nom = infile.Get(var+'_nom')
	histo_nom.ProfileX()
	profiled_histo_nom = infile.Get("%s_pfx" %(var+'_nom'))
	profiled_histo.SetLineColor(1)
	profiled_histo.SetLineWidth(3)
	profiled_histo_nom.SetLineColor(28)
	profiled_histo_nom.SetLineWidth(3)
	
	profiled_histo_nom.Draw("SAME")

	m_one_line = TLine(histo.GetXaxis().GetBinCenter(histo.FindFirstBinAbove(0,1)), 0, histo.GetXaxis().GetBinCenter(histo.FindLastBinAbove(0,1)), 0)
	m_one_line.SetLineStyle(1)
	m_one_line.SetLineColor(2)
	m_one_line.Draw("Same")
	
	print("Saving the pdf file")

 	c.Print("plots/profiled_%s.pdf" %(var))
