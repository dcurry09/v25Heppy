###########################################
# Plot Maker for quick plots
#
# by David Curry
#
# 7.22.1014
###########################################


from ROOT import *
from matplotlib import interactive

# Open root file of saved Hists
#file_2jet  = TFile('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/VHbb/myMacros/jetID_plots_2Jets.root')
file_2jet  = TFile('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/VHbb/myMacros/jetID_plots_3Jets.root')

# Headers
header = '#sqrt{s}=13TeV,   Z(l^{-}l^{+})H(b#bar{b}),   CMS Simulation,   3 Jets'


# Get Hists
gen_mass  = file_2jet.Get('gen_mass')
cmva_mass = file_2jet.Get('cmva_mass')
pt_mass   = file_2jet.Get('pt_mass')
z_mass    = file_2jet.Get('z_mass')

cmass_2jet = TCanvas('cmass_2jet')

s2jet = THStack('s2jet', '')

s2jet.Add(gen_mass)
s2jet.Add(cmva_mass)
s2jet.Add(pt_mass)
s2jet.Add(z_mass)

gen_mass.SetLineColor(kRed)
gen_mass.SetStats(0)
cmva_mass.SetLineColor(kGreen)
z_mass.SetLineColor(kBlack)

s2jet.Draw('nostack')
s2jet.SetTitle('')
s2jet.GetYaxis().SetTitle('Entries')
s2jet.GetXaxis().SetTitle('m(jj) [GeV]')

l_1 = TLatex()
l_1.SetNDC()
l_1.SetTextSize(0.03)
l_1.DrawLatex(0.1, 0.93, header)
l_1.Draw('same')

leg = TLegend(0.62,0.6,0.9,0.9)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.AddEntry(gen_mass, 'Gen Matched Jets', 'l')
leg.AddEntry(cmva_mass, 'Highest CMVA', 'l')
leg.AddEntry(pt_mass, 'Highest Pt', 'l')
leg.AddEntry(z_mass, 'Closest Z', 'l')
leg.Draw('same')

cmass_2jet.SaveAs('/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_6_2_1/src/VHbb/myMacros/plots/jetId/2Jet_mass.pdf')

raw_input('press return to continue')



