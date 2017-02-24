##########################################
# For calculating DY stitching Weights
#
#
##########################################

import ROOT
import numpy as np

path = '/exports/uftrig01a/dcurry/heppy/files/vtype_out/v25_' 


def getWeight(fileInc, fileB, region):

    countInc=0
    #print 'region',region,'\n'
    #for file in fileInc:
    f = ROOT.TFile.Open(path+fileInc+".root")
    tree = f.Get("tree")
    #print tree
    #countInc    = countInc + 1.* tree.Draw("",region)
    countInc    = 1.* tree.GetEntries(region)
    print 'Count Inc', countInc

    f.Close()
    
    countB=0
    #for file in fileB:
    f = ROOT.TFile.Open(path+fileB+".root")
    tree = f.Get("tree")
    #countB      = countB + 1.* tree.Draw("",region)
    countB      = 1.* tree.GetEntries(region)
    #print 'countB',countB,'\n'
    f.Close()

    # for DY b jet stitching
    weight = countInc/(countB+countInc)

    # for norm sample splitting
    #weight = countB/countInc

    return weight



def getWeight_nom(file_list):

    countInc=0
    for file in file_list:
        print 'Adding file to inclusive:', file, path+file+".root"
        f = ROOT.TFile.Open(path+file+".root")
        tree = f.Get("tree")
        countInc = countInc + 1.* tree.GetEntries()
        print 'Count Inc', countInc
        
    f.Close()


    for file in file_list:
        countB=0
        f = ROOT.TFile.Open(path+file+".root")
        tree = f.Get("tree")
        countB = 1.* tree.GetEntries()
        weight = 1-countInc/(countB+countInc)

        print 'Weight for File:', file
        print weight




ZLLjetsHT0       = "DY_inclusive"
ZLLjetsHT70      = "DY_70to100"
ZLLjetsHT100     = "DY_100to200"
ZLLjetsHT200     = "DY_200to400"
ZLLjetsHT400     = "DY_400to600"
ZLLjetsHT600     = "DY_600to800"
ZLLjetsHT600     = "DY_800to1200"
ZLLjetsHT600     = "DY_1200to2500"
ZLLjetsHT600     = "DY_2500toInf"

ZLLBjets         = "DY_Bjets"
ZLLjetsBGenFilter= "DY_BgenFilter"

DYBJets          = "(lheNb>0)"
DYJetsBGenFilter = "(lheNb==0 && nGenStatus2bHad>0)"

HT0              = "(lheHT<70)"
HT70             = "(lheHT>70 && lheHT<100)"
HT100            = "(lheHT>100 && lheHT<200)"
HT200            = "(lheHT>200 && lheHT<400)"
HT400            = "(lheHT>400 && lheHT<600)"
HT600            = "(lheHT>600&&lheHT<800)"
HT800            = "(lheHT>800&&lheHT<1200)"
HT1200           = "(lheHT>1200&&lheHT<2500)"
HT2500           = "(lheHT>2500)"

# For Vpt NLO sampels
ZLLjetsPt0       = "DY_inclusive_nlo"
ZLLjetsPt100     = "DY_Pt100to250"
ZLLjetsPt250     = "DY_Pt250to400"
ZLLjetsPt400     = "DY_Pt400to650"
ZLLjetsPt650     = "DY_Pt650toInf"

#Pt0              = "(lheV_pt<100)"
Pt100            = "(lheV_pt>100 && lheV_pt<250)"
Pt250            = "(lheV_pt>250 && lheV_pt<400)"
Pt400            = "(lheV_pt>400 && lheV_pt<650)"
Pt650            = "(lheV_pt>650)"

#print "weightZBjetsPt100=\t%.2f\n" %getWeight(ZLLjetsPt100,   ZLLjetsPt0, Pt100+"&&(Vtype == 1 | Vtype == 0) & vLeptons_pt[0] > 15. & vLeptons_pt[1] > 15.")
#print "weightZBjetsPt250=\t%.2f\n" %getWeight(ZLLjetsPt250,   ZLLjetsPt0, Pt250+"&&(Vtype == 1 | Vtype == 0) & vLeptons_pt[0] > 15. & vLeptons_pt[1] > 15.")
#print "weightZBjetsPt400=\t%.2f\n" %getWeight(ZLLjetsPt400,   ZLLjetsPt0, Pt400+"&&(Vtype == 1 | Vtype == 0) & vLeptons_pt[0] > 15. & vLeptons_pt[1] > 15.")
#print "weightZBjetsPt650=\t%.2f\n" %getWeight(ZLLjetsPt650,   ZLLjetsPt0, Pt650+"&&(Vtype == 1 | Vtype == 0) & vLeptons_pt[0] > 15. & vLeptons_pt[1] > 15.")



#print "weightZBjetsHT0=\t%.2f\n"   %getWeight(ZLLjetsHT0,     ZLLBjets, HT0+"&&"+DYBJets)
# print "weightZBjetsHT70=\t%.2f\n" %getWeight(ZLLjetsHT70,   ZLLBjets, HT70+"&&"+DYBJets)
# print "weightZBjetsHT100=\t%.2f\n" %getWeight(ZLLjetsHT100,   ZLLBjets, HT100+"&&"+DYBJets)
# print "weightZBjetsHT200=\t%.2f\n" %getWeight(ZLLjetsHT200,   ZLLBjets, HT200+"&&"+DYBJets)
# print "weightZBjetsHT400=\t%.2f\n" %getWeight(ZLLjetsHT400,   ZLLBjets, HT400+"&&"+DYBJets)
# print "weightZBjetsHT600=\t%.2f\n" %getWeight(ZLLjetsHT600,   ZLLBjets, HT600+"&&"+DYBJets)
# print "weightZBjetsHT800=\t%.2f\n" %getWeight(ZLLjetsHT800,   ZLLBjets, HT800+"&&"+DYBJets)
# print "weightZBjetsHT1200=\t%.2f\n" %getWeight(ZLLjetsHT1200,   ZLLBjets, HT1200+"&&"+DYBJets)
# print "weightZBjetsHT2500=\t%.2f\n" %getWeight(ZLLjetsHT2500,   ZLLBjets, HT2500+"&&"+DYBJets)

# #print "weightZBGenFilterHT0=\t%.2f\n"   %getWeight(ZLLjetsHT0,     ZLLjetsBGenFilter, HT0+"&&"+DYJetsBGenFilter)
# print "weightZBGenFilterHT70=\t%.2f\n" %getWeight(ZLLjetsHT70,   ZLLjetsBGenFilter, HT70+"&&"+DYJetsBGenFilter)
# print "weightZBGenFilterHT100=\t%.2f\n" %getWeight(ZLLjetsHT100,   ZLLjetsBGenFilter, HT100+"&&"+DYJetsBGenFilter)
# print "weightZBGenFilterHT200=\t%.2f\n" %getWeight(ZLLjetsHT200,   ZLLjetsBGenFilter, HT200+"&&"+DYJetsBGenFilter)
# print "weightZBGenFilterHT400=\t%.2f\n" %getWeight(ZLLjetsHT400,   ZLLjetsBGenFilter, HT400+"&&"+DYJetsBGenFilter)
# print "weightZBGenFilterHT600=\t%.2f\n" %getWeight(ZLLjetsHT600,   ZLLjetsBGenFilter, HT600+"&&"+DYJetsBGenFilter)
# print "weightZBGenFilterHT800=\t%.2f\n" %getWeight(ZLLjetsHT800,   ZLLjetsBGenFilter, HT800+"&&"+DYJetsBGenFilter)
# print "weightZBGenFilterHT1200=\t%.2f\n" %getWeight(ZLLjetsHT1200,   ZLLjetsBGenFilter, HT1200+"&&"+DYJetsBGenFilter)
# print "weightZBGenFilterHT2500=\t%.2f\n" %getWeight(ZLLjetsHT2500,   ZLLjetsBGenFilter, HT2500+"&&"+DYJetsBGenFilter)



dy2b_file_list = ['DY2J_ext1', 'DY2J_ext2', 'DY2J_ext3','DY2J_ext4']

#getWeight_nom(dy2b_file_list)



zee_list = ['prep_Zee_B_ext1', 'prep_Zee_B_ext2', 'prep_Zee_B_ext3', 
            'prep_Zee_D_ext1', 'prep_Zee_D_ext2',
            'prep_Zee_E_ext1', 
            'prep_Zee_C_ext1',  
            'prep_Zee_F_ext1',  
            'prep_Zee_G_ext3', 'prep_Zee_G_ext4',  
            'prep_Zee_H_ext1', 'prep_Zee_H_ext2',  'prep_Zee_H_ext3', 'prep_Zee_H_ext4']

sample_list = zee_list

path = '/exports/uftrig01a/dcurry/heppy/files/vtype_out/'

count_B, count_D, count_G, count_H2, count_H3 = 0,0,0,0,0

for sample in sample_list:
    
    print '\n Sample:', sample
    
    f = ROOT.TFile.Open(path+sample+".root")
    tree = f.Get("tree")
    
    countB      = 1.* tree.GetEntries()
    print 'countB',countB
    f.Close()
    
    if 'Zee_B' in sample: 
        count_B += countB
        print 'DoubleEG__Run2016B-23Sep2016-v3:', count_B

    if 'Zee_D' in sample: 
        count_D += countB
        print 'DoubleEG__Run2016D-23Sep2016-v1', count_D

    if 'Zee_G' in sample: 
        count_G += countB
        print 'DoubleEG__Run2016G-23Sep2016-v1', count_G
    
    if 'Zee_H_ext3' in sample or 'Zee_H_ext4' in sample: 
        count_H2 += countB
        print 'VHBB_HEPPY_V25_DoubleEG__Run2016H-PromptReco-v2', count_H2
        
    if 'Zee_H_ext2' in sample:
        count_H3 += countB
        print 'VHBB_HEPPY_V25_DoubleEG__Run2016H-PromptReco-v3', count_H3


#     # For sig/bkg counts
#     if sample == 'ZH125' or sample == 'ggZH125':
#         low_sig_tot += 1.* tree.GetEntries(low_cut) * theScale
#         med_sig_tot += 1.* tree.GetEntries(med_cut) * theScale
#         high_sig_tot += 1.* tree.GetEntries(high_cut) * theScale

#         low_sig_ele += 1.* tree.GetEntries(low_cut_ele) * theScale
#         med_sig_ele += 1.* tree.GetEntries(med_cut_ele) * theScale
#         high_sig_ele += 1.* tree.GetEntries(high_cut_ele) * theScale

#         low_sig_mu += 1.* tree.GetEntries(low_cut_mu) * theScale
#         med_sig_mu += 1.* tree.GetEntries(med_cut_mu) * theScale
#         high_sig_mu += 1.* tree.GetEntries(high_cut_mu) * theScale

        
#     else:
#         low_bkg_tot += 1.* tree.GetEntries(low_cut) * theScale
#         med_bkg_tot += 1.* tree.GetEntries(med_cut) * theScale
#         high_bkg_tot += 1.* tree.GetEntries(high_cut) * theScale

#         low_bkg_ele += 1.* tree.GetEntries(low_cut_ele) * theScale
#         med_bkg_ele += 1.* tree.GetEntries(med_cut_ele) * theScale
#         high_bkg_ele += 1.* tree.GetEntries(high_cut_ele) * theScale

#         low_bkg_mu += 1.* tree.GetEntries(low_cut_mu) * theScale
#         med_bkg_mu += 1.* tree.GetEntries(med_cut_mu) * theScale
#         high_bkg_mu += 1.* tree.GetEntries(high_cut_mu) * theScale


        
#     '''
#     count_1semi_pt150 = 1.* tree.GetEntries(final_cut_semi)
#     print "\n"+sample+" 1 semi pT 150 Count: ", count_1semi_pt150
    
#     count_NOsemi_pt150 = 1.* tree.GetEntries(final_cut_NOsemi)
#     print "\n"+sample+" NO semi pT 150 Count: ", count_NOsemi_pt150
    
    
#     count = 1.* tree.GetEntries(final_cut_semi_ele)
#     print "\n"+sample+" 1 semi pT 150 Electron Count: ", count

#     count = 1.* tree.GetEntries(final_cut_semi_mu)
#     print "\n"+sample+" 1 semi pT 150 Muon Count: ", count

#     count = 1.* tree.GetEntries(final_cut_NOsemi_ele)
#     print "\n"+sample+" NO semi pT 150 Electron Count: ", count
    
#     count = 1.* tree.GetEntries(final_cut_NOsemi_mu)
#     print "\n"+sample+" NO semi pT 150 Muon Count: ", count
#     '''


#     '''
#     if sample == 'Zuu' or sample == 'Zee':
#         f = ROOT.TFile.Open(path+sample+".root")
#         tree = f.Get("tree")
#         countInc = 1.* tree.GetEntries(prep_cut+'&json==1')
#     '''

#     #print "\n"+sample+" Event Count: ", countInc 


# '''
# print '============ Results ============='
# print ' Low Sig:', low_sig_tot, ' , Low Ele:', low_sig_ele,' , Low Mu:', low_sig_mu
# print ' Low Bkg:', low_bkg_tot, ' , Low Ele:', low_bkg_ele,' , Low Mu:', low_bkg_mu
# sb_low = low_sig_tot/np.sqrt(low_bkg_tot)
# print 'Low S/rootB:', sb_low

# print ' \nMed Sig:', med_sig_tot, ' , Med Ele:', med_sig_ele,' , Med Mu:', med_sig_mu
# print ' Med Bkg  :', med_bkg_tot, ' , Med Ele:', med_bkg_ele,' , Med Mu:', med_bkg_mu
# sb_med = med_sig_tot/np.sqrt(med_bkg_tot)
# print 'Med S/rootB:', sb_med

# print ' \nHigh Sig:', high_sig_tot, ' , High Ele:', high_sig_ele,' , High Mu:', high_sig_mu
# print ' High Bkg  :', high_bkg_tot, ' , high Ele:', high_bkg_ele,' , High Mu:', high_bkg_mu
# sb_high = high_sig_tot/np.sqrt(high_bkg_tot)
# print 'High S/rootB:', sb_high


# print '\n Total from Categories S/rootB:', 
# sb_tot = np.sqrt( (sb_low)*(sb_low) + (sb_med)*(sb_med) + (sb_high)*(sb_high) )
# print sb_tot

# print '\n Total from NO Categories S/rootB:'
# sb_one = (low_sig_tot+med_sig_tot+high_sig_tot)/(np.sqrt(low_bkg_tot+med_bkg_tot+high_bkg_tot ) )
# print sb_one
# '''
