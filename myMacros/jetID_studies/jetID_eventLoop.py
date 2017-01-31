###########################################
# Event Loop for jet ID plots and stats
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
file = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/files/prep_out/02_21_2015_Zll.root')

# Set Trees
tree = file.Get('tree')

# List of input sample names
sample_list = ['bCSV', 'highPt', 'bCSV_Z30']


# Define Hist file to be saved
newfile = TFile('jetID_plots_3Jets.root','recreate')


# ===================================================
# Define Histograms

gen_mass  = TH1F('gen_mass', '', 50, 20, 220)
cmva_mass = TH1F('cmva_mass', '', 50, 20, 220)
pt_mass   = TH1F('pt_mass', '', 50, 20, 220)
z_mass    = TH1F('z_mass', '', 50, 20, 220)

hist_list = [gen_mass, cmva_mass, pt_mass, z_mass]
    
# ===================================================

def deltaR(phi1, phi2, eta1, eta2):

    deta = eta1 - eta2
    dphi = phi1 - phi2
    if dphi > np.pi: dphi - np.pi
    
    return sqrt(dphi*dphi + deta*deta)


# A more efficient way to count
count = Counter()

# Loop over events
for iEvt in range(tree.GetEntries()):
    
    # for testing
    if iEvt > 10000: break
     
    tree.GetEntry(iEvt)
    
    if iEvt % 10000 is 0: print 'Event #', iEvt

    # ==== Make Cuts ====
    #count['Total MC bJets'] += 2

    if tree.nJet < 3: continue

    if tree.hJets_pt[0] < 20: continue 
    if tree.hJets_pt[1] < 20: continue

    if abs(tree.hJets_eta[0]) > 2.4: continue
    if abs(tree.hJets_eta[1]) > 2.4: continue

    if tree.H_pt < 0: continue
    
    # ===================
    
    count['num_events'] += 1
    
    # Also make a cut on # of jets with secondary vertices info
    num_jets_vtx = 0
    for iJet in range(tree.nJet):
        
        if tree.Jet_vtxPosZ[iJet] != 0.:
            num_jets_vtx += 1
    
    # only let 2 or 3 jets with info through
    if num_jets_vtx < 2:
        count['num_events_novtx'] += 1
        continue
    
    if num_jets_vtx == 2:
        count['num_events_2jets_w/vtx'] += 1
        
    if num_jets_vtx == 3:
        count['num_events_3jets_w/vtx'] += 1

    if num_jets_vtx > 3:
        count['num_events_more3jets_w/vtx'] += 1
                
    #  Match the two Gen Higgs Jets to Jets in the event.  These will be our truth standard to live up to.
    gen_matched_list = []

    for gen_jet in range(0,2):
        for jet in range(tree.nJet):

            # Look in dR cone around Higgs GenJet
            dr = deltaR(tree.Jet_phi[jet], tree.GenBQuarkFromH_phi[gen_jet], tree.Jet_eta[jet], tree.GenBQuarkFromH_eta[gen_jet])
        
            if dr < 0.3:
                gen_matched_list.append(jet)
                break
    # end jet loop    
    
    # only look at events with two jets matched to Higgs b qaurks
    if len(gen_matched_list) != 2: continue


    # ==== Experimental H Tagging ====

    # fill list with all jet Z cooridinates.  After hJets, loop over additional(a) Jets
    z_list = []
    z_list.append(tree.hJets_vtxPosZ[0])
    z_list.append(tree.hJets_vtxPosZ[1])

    # CMVA
    cmva_list = []
    cmva_list.append(tree.hJets_btagCMVA[0])
    cmva_list.append(tree.hJets_btagCMVA[1])

    # Pt
    pt_list = []
    pt_list.append(tree.hJets_pt[0])
    pt_list.append(tree.hJets_pt[1])
    
    # loop over aJets
    for iJet in range(tree.naJets):

        z_list.append(tree.aJets_vtxPosZ[iJet])
        
        cmva_list.append(tree.aJets_btagCMVA[iJet])

        pt_list.append(tree.aJets_pt[iJet])
        
    # find difference amongst all values in z_list
    diff_list  = [abs(y - x) for x, y in it.combinations(z_list, 2)]
    index_list = [ [z_list.index(x), z_list.index(y)] for x, y in it.combinations(z_list, 2)] 
    print z_list
    print index_list
    
    # which two elements make up the smallest difference in z list?
    pos = diff_list.index(min(diff_list))
    index_winner_z = index_list[pos]
    
    # which to jets are highest CMVA?  Find highest sum CMVA amongst pairs
    diff_list_cmva  = [abs(y + x) for x, y in it.combinations(cmva_list, 2)]
    index_list_cmva = [ [cmva_list.index(x), cmva_list.index(y)] for x, y in it.combinations(cmva_list, 2)]
    
    pos_cmva = diff_list_cmva.index(max(diff_list_cmva))
    index_winner_cmva = index_list_cmva[pos_cmva]

    # which to jets are highest pt?  Find highest sum pt amongst pairs
    diff_list_pt  = [abs(y + x) for x, y in it.combinations(pt_list, 2)]
    index_list_pt = [ [pt_list.index(x), pt_list.index(y)] for x, y in it.combinations(pt_list, 2)]
        
    pos_pt = diff_list_pt.index(max(diff_list_pt))
    index_winner_pt = index_list_pt[pos_pt]


    #print '\nThe winning Jets are:', index_winner
    # print 'The winning cmva Jets are:', index_winner_cmva
    
    print 'Z index winner:', index_winner_z
    print 'Pt index winner:', index_winner_pt


    # Now find the higgs mass for each type of matching
    match_list = ['cmva', 'pt', 'gen', 'z'] 

    for i in match_list:
        
        if i == 'cmva':
            
            t1 = TLorentzVector()  
            t2 = TLorentzVector()
            
            # get dijet mass of winning jets
            if index_winner_cmva[0] == 0 or index_winner_cmva[0] == 1:
                t1.SetPtEtaPhiM(tree.hJets_pt[index_winner_cmva[0]], tree.hJets_eta[index_winner_cmva[0]], tree.hJets_phi[index_winner_cmva[0]], tree.hJets_mass[index_winner_cmva[0]])
                
            else: t1.SetPtEtaPhiM(tree.aJets_pt[index_winner_cmva[0]-2], tree.aJets_eta[index_winner_cmva[0]-2], tree.aJets_phi[index_winner_cmva[0]-2], tree.aJets_mass[index_winner_cmva[0]-2]) 
            
            if index_winner_cmva[1] == 0 or index_winner_cmva[1] == 1:
                t2.SetPtEtaPhiM(tree.hJets_pt[index_winner_cmva[1]], tree.hJets_eta[index_winner_cmva[1]], tree.hJets_phi[index_winner_cmva[1]], tree.hJets_mass[index_winner_cmva[1]])
                
            else: t2.SetPtEtaPhiM(tree.aJets_pt[index_winner_cmva[1]-2], tree.aJets_eta[index_winner_cmva[1]-2], tree.aJets_phi[index_winner_cmva[1]-2], tree.aJets_mass[index_winner_cmva[1]-2])
            
            mjj = (t1+t2).M()
            
            cmva_mass.Fill(mjj)
            
        if i =='pt':

            t1 = TLorentzVector()
            t2 = TLorentzVector()
            
            # get dijet mass of winning jets
            if index_winner_pt[0] == 0 or index_winner_pt[0] == 1:
                t1.SetPtEtaPhiM(tree.hJets_pt[index_winner_pt[0]], tree.hJets_eta[index_winner_pt[0]], tree.hJets_phi[index_winner_pt[0]], tree.hJets_mass[index_winner_pt[0]])
                
            else: t1.SetPtEtaPhiM(tree.aJets_pt[index_winner_pt[0]-2], tree.aJets_eta[index_winner_pt[0]-2], tree.aJets_phi[index_winner_pt[0]-2], tree.aJets_mass[index_winner_pt[0]-2])
            
            if index_winner_pt[1] == 0 or index_winner_pt[1] == 1:
                t2.SetPtEtaPhiM(tree.hJets_pt[index_winner_pt[1]], tree.hJets_eta[index_winner_pt[1]], tree.hJets_phi[index_winner_pt[1]], tree.hJets_mass[index_winner_pt[1]])
                
            else: t2.SetPtEtaPhiM(tree.aJets_pt[index_winner_pt[1]-2], tree.aJets_eta[index_winner_pt[1]-2], tree.aJets_phi[index_winner_pt[1]-2], tree.aJets_mass[index_winner_pt[1]-2])
            
            mjj = (t1+t2).M()
            
            pt_mass.Fill(mjj)

        if i == 'z':
            
             t1 = TLorentzVector()
             t2 = TLorentzVector()

             # get dijet mass of winning jets
             if index_winner_z[0] == 0 or index_winner_z[0] == 1:
                 t1.SetPtEtaPhiM(tree.hJets_pt[index_winner_z[0]], tree.hJets_eta[index_winner_z[0]], tree.hJets_phi[index_winner_z[0]], tree.hJets_mass[index_winner_z[0]])
                 
             else: t1.SetPtEtaPhiM(tree.aJets_pt[index_winner_z[0]-2], tree.aJets_eta[index_winner_z[0]-2], tree.aJets_phi[index_winner_z[0]-2], tree.aJets_mass[index_winner_z[0\
                                                                                                                                                                                    ]-2])
             
             if index_winner_z[1] == 0 or index_winner_z[1] == 1:
                 t2.SetPtEtaPhiM(tree.hJets_pt[index_winner_z[1]], tree.hJets_eta[index_winner_z[1]], tree.hJets_phi[index_winner_z[1]], tree.hJets_mass[index_winner_z[1]])
                 
             else: t2.SetPtEtaPhiM(tree.aJets_pt[index_winner_z[1]-2], tree.aJets_eta[index_winner_z[1]-2], tree.aJets_phi[index_winner_z[1]-2], tree.aJets_mass[index_winner_z[1\
                                                                                                                                                                                    ]-2])
             
             mjj = (t1+t2).M()
             
             z_mass.Fill(mjj)
             

        if i == 'gen':

             t1 = TLorentzVector()
             t2 = TLorentzVector()
            
             t1.SetPtEtaPhiM(tree.Jet_pt[gen_matched_list[0]], tree.Jet_eta[gen_matched_list[0]], tree.Jet_phi[gen_matched_list[0]], tree.Jet_mass[gen_matched_list[0]])
                            
             t2.SetPtEtaPhiM(tree.Jet_pt[gen_matched_list[1]], tree.Jet_eta[gen_matched_list[1]], tree.Jet_phi[gen_matched_list[1]], tree.Jet_mass[gen_matched_list[1]])
            
             mjj = (t1+t2).M()

             gen_mass.Fill(mjj)

             
    # end match list loop
    
    

    '''
    jet1_flav, jet2_flav = -999, -999
    # are the winning jets bTagged?
    if index_winner[0] == 0 or index_winner[0] == 1:
        jet1_flav = abs(tree.hJets_mcFlavour[index_winner[0]])
        
    else: jet1_flav = abs(tree.aJets_mcFlavour[index_winner[0]-2])
    
    if index_winner[1] == 0 or index_winner[1] == 1:
        jet2_flav = abs(tree.hJets_mcFlavour[index_winner[1]])
        
    else: jet2_flav = abs(tree.aJets_mcFlavour[index_winner[1]-2])

    
    print 'Jet1 Flavour = ', jet1_flav
    print 'Jet2 Flavour = ', jet2_flav
    print 'hJet1 Flavour =', tree.hJets_mcFlavour[0] 
    print 'hJet2 Flavour =', tree.hJets_mcFlavour[1]
    
    # keep track of jet assignment counts by me
    if abs(jet1_flav) == 5:
        count['jet1_matched_z'] += 1
        
    if abs(jet2_flav) == 5:
        count['jet2_matched_z'] += 1

        
    # How did CMVA btagging perform?
    jet1_flav, jet2_flav = -999, -999

    if index_winner_cmva[0] == 0 or index_winner_cmva[0] == 1:
        jet1_flav = abs(tree.hJets_mcFlavour[index_winner_cmva[0]])

    else: jet1_flav = abs(tree.aJets_mcFlavour[index_winner_cmva[0]-2])

    if index_winner_cmva[1] == 0 or index_winner_cmva[1] == 1:
        jet2_flav = abs(tree.hJets_mcFlavour[index_winner_cmva[1]])

    else: jet2_flav = abs(tree.aJets_mcFlavour[index_winner_cmva[1]-2])

    # keep track of jet assignment counts by me
    if abs(jet1_flav) == 5:
        count['jet1_matched_cmva'] += 1

    if abs(jet2_flav) == 5:
        count['jet2_matched_cmva'] += 1
    

    # and how is btagging with pt(the default in the tuple)?
    if abs(tree.hJets_mcFlavour[0]) == 5:
        count['jet1_matched_pt'] += 1
        
    if abs(tree.hJets_mcFlavour[1]) == 5:
        count['jet2_matched_pt'] += 1
        
    # print out    
    print '\n===== New Event ====='
    print 'Jet 1 secVtx X: ', tree.hJets_vtxPosX[0]
    print 'Jet 1 secVtx Y: ', tree.hJets_vtxPosY[0]
    print 'Jet 1 secVtx Z: ', tree.hJets_vtxPosZ[0]
    print 'Jet 1 pt: ', tree.hJets_pt[0]
    print 'Jet 1 phi: ', tree.hJets_phi[0]
    print 'Jet 1 eta: ', tree.hJets_eta[0]
    print '\nJet 2 secVtx X: ', tree.hJets_vtxPosX[1]
    print 'Jet 2 secVtx Y: ', tree.hJets_vtxPosY[1]
    print 'Jet 2 secVtx Z: ', tree.hJets_vtxPosZ[1]
    print 'Jet 2 pt: ', tree.hJets_pt[1]
    print 'Jet 2 phi: ', tree.hJets_phi[1]
    print 'Jet 2 eta: ', tree.hJets_eta[1]
    

    if tree.hJets_vtxPosX[1] == 0 and tree.hJets_vtxPosY[1] == 0:
        count['missing_jet2_vtx'] += 1
        

    count['test'] += 1
    #if count['test'] > 10: break
    '''
    


# End event Loop

#gen_mass.Draw()

#  ======== Write Hists ==========
for hist in hist_list:
    if isinstance(hist, list):
        newfile.mkdir('%s' % hist[0].GetName()).cd()
        for i in hist: i.Write()
    else: hist.Write()

del newfile
# ================================




print count

print 'bJet Match Percentage(Z)   : ', float(count['jet1_matched_z']+count['jet2_matched_z']) / float(count['Total MC bJets'])
print 'bJet Match Percentage(CMVA): ', float(count['jet1_matched_cmva']+count['jet2_matched_cmva']) / float(count['Total MC bJets'])
print 'bJet Match Percentage(pt): ', float(count['jet1_matched_pt']+count['jet2_matched_pt']) / float(count['Total MC bJets'])

raw_input('press return to continue')



