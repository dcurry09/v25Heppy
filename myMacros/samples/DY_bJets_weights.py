##########################################
# For calculating DY stitching Weights
#
#
##########################################

import ROOT
import numpy as np

#path = '/exports/uftrig01a/dcurry/heppy/v24/' 
path = '/exports/uftrig01a/dcurry/heppy/files/prep_out/v24_9_15_'


def getWeight(fileInc, fileB, region):

    countInc=0
    print 'region',region,'\n'
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

    weight = countInc/(countB+countInc)
    return weight




ZLLjetsHT0       = "DY_inclusive"
ZLLjetsHT100     = "DY_100to200"
ZLLjetsHT200     = "DY_200to400"
ZLLjetsHT400     = "DY_400to600"
ZLLjetsHT600     = "DY_600toInf"


ZLLBjets         = "DY_Bjets"
ZLLjetsBGenFilter= "DY_BgenFilter"

DYBJets          = "(lheNb>0)"
DYJetsBGenFilter = "(lheNb==0 && nGenStatus2bHad>0)"

HT0              = "(lheHT<100)"
HT100            = "(lheHT>100 && lheHT<200)"
HT200            = "(lheHT>200 && lheHT<400)"
HT400            = "(lheHT>400 && lheHT<600)"
HT600            = "(lheHT>600)"

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



print "weightZBjetsHT0=\t%.2f\n"   %getWeight(ZLLjetsHT0,     ZLLBjets, HT0+"&&"+DYBJets)
print "weightZBjetsHT100=\t%.2f\n" %getWeight(ZLLjetsHT100,   ZLLBjets, HT100+"&&"+DYBJets)
print "weightZBjetsHT200=\t%.2f\n" %getWeight(ZLLjetsHT200,   ZLLBjets, HT200+"&&"+DYBJets)
print "weightZBjetsHT400=\t%.2f\n" %getWeight(ZLLjetsHT400,   ZLLBjets, HT400+"&&"+DYBJets)
print "weightZBjetsHT600=\t%.2f\n" %getWeight(ZLLjetsHT600,   ZLLBjets, HT600+"&&"+DYBJets)

print "weightZBGenFilterHT0=\t%.2f\n"   %getWeight(ZLLjetsHT0,     ZLLjetsBGenFilter, HT0+"&&"+DYJetsBGenFilter)
print "weightZBGenFilterHT100=\t%.2f\n" %getWeight(ZLLjetsHT100,   ZLLjetsBGenFilter, HT100+"&&"+DYJetsBGenFilter)
print "weightZBGenFilterHT200=\t%.2f\n" %getWeight(ZLLjetsHT200,   ZLLjetsBGenFilter, HT200+"&&"+DYJetsBGenFilter)
print "weightZBGenFilterHT400=\t%.2f\n" %getWeight(ZLLjetsHT400,   ZLLjetsBGenFilter, HT400+"&&"+DYJetsBGenFilter)
print "weightZBGenFilterHT600=\t%.2f\n" %getWeight(ZLLjetsHT600,   ZLLjetsBGenFilter, HT600+"&&"+DYJetsBGenFilter)







data_list = ['Zuu', 'Zee']

signal_list = ['ZH125', 'ggZH125']

bkg_list = ['ZZ_2L2Q', 'WZ', 'ttbar']

DY_list = ['DY_inclusive', 'DY_100to200', 'DY_200to400', 'DY_400to600', 'DY_600toInf', 'DY_Bjets', 'DY_BgenFilter']
           #'DY_5to50_inclusive', 'DY_5to50_100to200', 'DY_5to50_200to400', 'DY_5to50_400to600', 'DY_5to50_600toInf']

ST_list = ['ST_t', 'ST_s', 'ST_tW_top', 'ST_tW_antitop']

#sample_list = signal_list + bkg_list + DY_list
sample_list = data_list


xsec_list = {'ZH125':0.04837, 'ggZH125': 0.01340, 'ZZ_2L2Q':3.32, 'WZ':0.16, 'ttbar':815.16,
             'DY_inclusive':6024.0, 'DY_100to200':171.46, 'DY_200to400':52.585, 'DY_400to600':6.76131, 'DY_600toInf':2.718,
             'ST_t':220.45, 'ST_s':10.32, 'ST_tW_antitop':35.6, 'ST_tW_top':35.6,
             'DY_inclusive':6024.0, 'DY_100to200':171.46, 'DY_200to400':52.585, 'DY_400to600':6.76131, 'DY_600toInf':2.718, 'DY_Bjets':1, 'DY_BgenFilter':1
             }


prep_cut = '(Vtype == 1 | Vtype == 0) & vLeptons_pt[0] > 15. & vLeptons_pt[1] > 15.'

nolepton = '!(Jet_leptonPt[hJCidx[0]] > 0. || Jet_leptonPt[hJCidx[1]] > 0.)'

semiLepton = '(Jet_leptonPt[hJCidx[0]] > 0. || Jet_leptonPt[hJCidx[1]] > 0.)'

Vpt_150 = ' & V_pt > 150.0'

Vpt_high = ' & V_pt > 140.0'

Vpt_low = ' & V_pt > 50 & V_pt < 90'

Vpt_med = ' & V_pt > 90 & V_pt < 140'

SR_cut = ' & Jet_btagCSV[hJCidx[0]] > 0.460 & Jet_btagCSV[hJCidx[1]] > 0.460 & V_mass > 75. & V_mass < 105. & abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4 & Jet_puId[hJCidx[0]] >= 4 & Jet_puId[hJCidx[1]] >= 4 & ((Jet_puId[hJCidx[1]] >= 7 & Jet_btagCSV[hJCidx[1]] >= 0.53 & Jet_btagCSV[hJCidx[1]] <= 0.55) || !(Jet_btagCSV[hJCidx[1]] > 0.53 & Jet_btagCSV[hJCidx[1]] < 0.55)) & vLeptons_pt[0] > 20. & vLeptons_pt[1] > 20. & ((Vtype == 1 & vLeptons_relIso03[0] < 0.15 & vLeptons_relIso03[1] < 0.15) || (Vtype == 0 & vLeptons_relIso04[0] < 0.25 & vLeptons_relIso04[1] < 0.25)) & (run <= 275125) & HCSV_reg_mass < 150. & HCSV_reg_mass > 90. & Jet_pt_reg[hJCidx[0]] > 20. & Jet_pt_reg[hJCidx[1]] > 20. & H_pt < 999. & H_pt > 0. & H_mass < 9999. & H_mass > 0. & V_pt < 2000.'

ele_cut = ' & Vtype == 1'

mu_cut = ' & Vtype == 0'

final_cut_semi = prep_cut  +' & '+ semiLepton +' & '+ Vpt_150+' & '+SR_cut  

final_cut_NOsemi = prep_cut +' & '+ nolepton +' & '+ Vpt_150+' & '+SR_cut

final_cut_semi_ele = semiLepton +' & '+ Vpt_150+' & '+SR_cut +' & Vtype == 1'

final_cut_semi_mu = semiLepton +' & '+ Vpt_150+' & '+SR_cut +' & Vtype == 0'

final_cut_NOsemi_mu = prep_cut +' & '+ nolepton +' & '+ Vpt_150+' & '+SR_cut +' & Vtype == 0'

final_cut_NOsemi_ele = prep_cut +' & '+ nolepton +' & '+ Vpt_150+' & '+SR_cut +' & Vtype == 1'


low_cut = prep_cut + SR_cut + Vpt_low
med_cut = prep_cut + SR_cut + Vpt_med
high_cut = prep_cut + SR_cut + Vpt_high

low_cut_ele = prep_cut + SR_cut + Vpt_low + ele_cut
med_cut_ele = prep_cut + SR_cut + Vpt_med + ele_cut
high_cut_ele = prep_cut + SR_cut + Vpt_high + ele_cut

low_cut_mu = prep_cut + SR_cut + Vpt_low + mu_cut
med_cut_mu = prep_cut + SR_cut + Vpt_med + mu_cut
high_cut_mu = prep_cut + SR_cut + Vpt_high + mu_cut

low_bkg_tot = 0
low_sig_tot = 0

med_bkg_tot = 0
med_sig_tot = 0

high_bkg_tot = 0
high_sig_tot = 0

low_bkg_ele = 0
low_sig_ele = 0
med_bkg_ele = 0
med_sig_ele = 0
high_bkg_ele = 0
high_sig_ele = 0

low_bkg_mu = 0
low_sig_mu = 0
med_bkg_mu = 0
med_sig_mu = 0
high_bkg_mu = 0
high_sig_mu = 0

lumi = 4340.0

for sample in sample_list:
    
    break
    print '\n Sample:', sample
    
    f = ROOT.TFile.Open(path+sample+".root")
    tree = f.Get("tree")

    posWeight = f.Get('CountPosWeight')
    negWeight = f.Get('CountNegWeight')

    xsec = xsec_list[sample]
    theScale = lumi*xsec / (posWeight.GetBinContent(1) - negWeight.GetBinContent(1))


    # For sig/bkg counts
    if sample == 'ZH125' or sample == 'ggZH125':
        low_sig_tot += 1.* tree.GetEntries(low_cut) * theScale
        med_sig_tot += 1.* tree.GetEntries(med_cut) * theScale
        high_sig_tot += 1.* tree.GetEntries(high_cut) * theScale

        low_sig_ele += 1.* tree.GetEntries(low_cut_ele) * theScale
        med_sig_ele += 1.* tree.GetEntries(med_cut_ele) * theScale
        high_sig_ele += 1.* tree.GetEntries(high_cut_ele) * theScale

        low_sig_mu += 1.* tree.GetEntries(low_cut_mu) * theScale
        med_sig_mu += 1.* tree.GetEntries(med_cut_mu) * theScale
        high_sig_mu += 1.* tree.GetEntries(high_cut_mu) * theScale

        
    else:
        low_bkg_tot += 1.* tree.GetEntries(low_cut) * theScale
        med_bkg_tot += 1.* tree.GetEntries(med_cut) * theScale
        high_bkg_tot += 1.* tree.GetEntries(high_cut) * theScale

        low_bkg_ele += 1.* tree.GetEntries(low_cut_ele) * theScale
        med_bkg_ele += 1.* tree.GetEntries(med_cut_ele) * theScale
        high_bkg_ele += 1.* tree.GetEntries(high_cut_ele) * theScale

        low_bkg_mu += 1.* tree.GetEntries(low_cut_mu) * theScale
        med_bkg_mu += 1.* tree.GetEntries(med_cut_mu) * theScale
        high_bkg_mu += 1.* tree.GetEntries(high_cut_mu) * theScale


        
    '''
    count_1semi_pt150 = 1.* tree.GetEntries(final_cut_semi)
    print "\n"+sample+" 1 semi pT 150 Count: ", count_1semi_pt150
    
    count_NOsemi_pt150 = 1.* tree.GetEntries(final_cut_NOsemi)
    print "\n"+sample+" NO semi pT 150 Count: ", count_NOsemi_pt150
    
    
    count = 1.* tree.GetEntries(final_cut_semi_ele)
    print "\n"+sample+" 1 semi pT 150 Electron Count: ", count

    count = 1.* tree.GetEntries(final_cut_semi_mu)
    print "\n"+sample+" 1 semi pT 150 Muon Count: ", count

    count = 1.* tree.GetEntries(final_cut_NOsemi_ele)
    print "\n"+sample+" NO semi pT 150 Electron Count: ", count
    
    count = 1.* tree.GetEntries(final_cut_NOsemi_mu)
    print "\n"+sample+" NO semi pT 150 Muon Count: ", count
    '''


    '''
    if sample == 'Zuu' or sample == 'Zee':
        f = ROOT.TFile.Open(path+sample+".root")
        tree = f.Get("tree")
        countInc = 1.* tree.GetEntries(prep_cut+'&json==1')
    '''

    #print "\n"+sample+" Event Count: ", countInc 


'''
print '============ Results ============='
print ' Low Sig:', low_sig_tot, ' , Low Ele:', low_sig_ele,' , Low Mu:', low_sig_mu
print ' Low Bkg:', low_bkg_tot, ' , Low Ele:', low_bkg_ele,' , Low Mu:', low_bkg_mu
sb_low = low_sig_tot/np.sqrt(low_bkg_tot)
print 'Low S/rootB:', sb_low

print ' \nMed Sig:', med_sig_tot, ' , Med Ele:', med_sig_ele,' , Med Mu:', med_sig_mu
print ' Med Bkg  :', med_bkg_tot, ' , Med Ele:', med_bkg_ele,' , Med Mu:', med_bkg_mu
sb_med = med_sig_tot/np.sqrt(med_bkg_tot)
print 'Med S/rootB:', sb_med

print ' \nHigh Sig:', high_sig_tot, ' , High Ele:', high_sig_ele,' , High Mu:', high_sig_mu
print ' High Bkg  :', high_bkg_tot, ' , high Ele:', high_bkg_ele,' , High Mu:', high_bkg_mu
sb_high = high_sig_tot/np.sqrt(high_bkg_tot)
print 'High S/rootB:', sb_high


print '\n Total from Categories S/rootB:', 
sb_tot = np.sqrt( (sb_low)*(sb_low) + (sb_med)*(sb_med) + (sb_high)*(sb_high) )
print sb_tot

print '\n Total from NO Categories S/rootB:'
sb_one = (low_sig_tot+med_sig_tot+high_sig_tot)/(np.sqrt(low_bkg_tot+med_bkg_tot+high_bkg_tot ) )
print sb_one
'''
