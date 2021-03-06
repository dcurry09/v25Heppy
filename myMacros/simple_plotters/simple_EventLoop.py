###########################################

# Event Loop for quick plots
#
# by David Curry
#
# 7.22.1014
###########################################
 

from ROOT import *
from matplotlib import interactive
import numpy as np
from collections import Counter
import itertools as it

# Open root file of saved Hists
#file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/v12_07_2015_Zll.root')
#file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/v12_07_2015_DY_inclusive.root')
file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/v14/ZH125.root')
#file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/regression/jan_zll_genJet_boost/v14_11_2015_ggZH125.root')

tree = file.Get('tree')



# ===================================================
# Define Histograms

gen_mass = TH1F('gen_mass', '' , 100, 0, 200)
mass_reg = TH1F('mass_reg', '' , 100, 0, 200)



# ===================================================


# A more efficient way to count
count = Counter()


# ====== Loop over events =======
for iEvt in range(tree.GetEntries()):
    
    # for testing
    if iEvt > 10000: break
    
    tree.GetEntry(iEvt)
    
    if iEvt % 10000 is 0: print '-----> Event #', iEvt

    count['total_events'] += 1

    '''
    # Loop over GenJets and find the diJet mass
    if tree.GenJet_numBHadrons[0] > 0 and tree.GenJet_numBHadrons[1] > 0:
        
        t1 = TLorentzVector()
        t2 = TLorentzVector()
        
        t1.SetPtEtaPhiM(tree.GenJet_wNuPt[0], tree.GenJet_wNuEta[0], tree.GenJet_wNuPhi[0], tree.GenJet_wNuM[0])
        t2.SetPtEtaPhiM(tree.GenJet_wNuPt[1], tree.GenJet_wNuEta[1], tree.GenJet_wNuPhi[1], tree.GenJet_wNuM[1])

        mass = (t1+t2).M()
        gen_mass.Fill(mass)
    '''    

    # Loop over Gen b Quarks
    t1 = TLorentzVector()
    t2 = TLorentzVector()
    
    t1.SetPtEtaPhiM(tree.GenBQuarkFromH_pt[0], tree.GenBQuarkFromH_eta[0], tree.GenBQuarkFromH_phi[0], tree.GenBQuarkFromH_mass[0])
    t2.SetPtEtaPhiM(tree.GenBQuarkFromH_pt[1], tree.GenBQuarkFromH_eta[1], tree.GenBQuarkFromH_phi[1], tree.GenBQuarkFromH_mass[1])
    
    mass = (t1+t2).M()
    gen_mass.Fill(mass)
        


    # loop over jets and count the btagging efficiency
    # ie. the % of a time a b jet(flavour 5) makes it past the L/M/T cuts

    is_bJet_event  = False
    is_2bJet_event = False 
    count['bjet_event_count'] = 0

    for iJet in range(tree.nJet):

        count['total_Jets'] += 1

        if tree.Jet_btagCSV[iJet] > 0.6: count['total_csvJets'] += 1
        
        # for semiL Jets
        if tree.Jet_leptonPt[iJet] > 0 and tree.Jet_btagCSV[iJet] > 0.6:
            count['semiL_jet'] += 1
        

        jet_flav = abs(tree.Jet_mcFlavour[iJet])
        jet_csv  = tree.Jet_btagCSV[iJet]
        
        if jet_flav == 5:

            count['bjet_count'] += 1

            count['bjet_event_count'] += 1

            # count 2b events
            if count['bjet_event_count'] > 1 and not is_2bJet_event:
                count['2bjet_event'] += 1
                is_2bJet_event = True
            
            # count at least 1b events    
            if not is_bJet_event:
                count['bJet_event'] += 1
                is_bJet_event = True

            if jet_csv >= 0.97:  count['bjet_in_tight'] += 1
            if jet_csv >= 0.89:  count['bjet_in_med'] += 1
            if jet_csv >= 0.605: count['bjet_in_loose'] += 1
    

# end event loop


print '========== Analysis Results ==========='
print 'bJet Events : ', count['bJet_event'], '   (%', float(count['bJet_event'])/float(count['total_events'])*100,')'
print '2bJet Events: ', count['2bjet_event'], '   (%', float(count['2bjet_event'])/float(count['total_events'])*100,')'
print 'Total b Jets: ', count['bjet_count']
print '\t b Jets above tight CSV Cut : ', count['bjet_in_tight'], '  (%', float(count['bjet_in_tight'])/float(count['bjet_count'])*100,')'
print '\t b Jets above med CSV Cut   : ', count['bjet_in_med'], '  (%', float(count['bjet_in_med'])/float(count['bjet_count'])*100,')'
print '\t b Jets above loose CSV Cut : ', count['bjet_in_loose'], '  (%', float(count['bjet_in_loose'])/float(count['bjet_count'])*100,')'

print '\n\t Total Jets        : ', count['total_Jets']
print '\n\t Total csvJets        : ', count['total_csvJets']
print '\n\t Semi Leptonic Jets: ', count['semiL_jet']


gen_mass.Draw()

raw_input('press return to continue')



