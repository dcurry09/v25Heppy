############################################
#
# For Signal Efficiencies in the AN
#
###########################################

import ROOT

path = '/exports/uftrig01a/dcurry/heppy/v21/'


sample_list = ['ZH125_merged']


e_prep_cut = 'Vtype == 1 & vLeptons_pt[0] > 20. & vLeptons_pt[1] > 20. & Jet_pt_reg[0] > 20 & Jet_pt_reg[1] > 20 & HLT_BIT_HLT_Ele23_WPLoose_Gsf_v == 1'
m_prep_cut = 'Vtype == 0 & vLeptons_pt[0] > 20. & vLeptons_pt[1] > 20. & Jet_pt_reg[0] > 20 & Jet_pt_reg[1] > 20 & (HLT_BIT_HLT_IsoMu20_v || HLT_BIT_HLT_IsoTkMu20_v)'

e_vpt_cut = e_prep_cut+' & V_pt > 50.'
m_vpt_cut = m_prep_cut+' & V_pt > 50.'

e_csv1_cut = e_vpt_cut+' & Jet_btagCSV[0] > 0.46'
m_csv1_cut = m_vpt_cut+' & Jet_btagCSV[0] > 0.46'

e_csv2_cut = e_csv1_cut+' & Jet_btagCSV[1] > 0.46'
m_csv2_cut = m_csv1_cut+' & Jet_btagCSV[1] > 0.46'

e_mjj_cut = e_csv2_cut+' & HCSV_reg_mass > 90 & HCSV_reg_mass < 145'
m_mjj_cut = m_csv2_cut+' & HCSV_reg_mass > 90 & HCSV_reg_mass < 145'


for sample in sample_list:

    f = ROOT.TFile.Open(path+sample+".root")
    tree = f.Get("tree")

    total_evt = 1.* tree.GetEntries()

    e_prep_count = 1.* tree.GetEntries(e_prep_cut)
    m_prep_count = 1.* tree.GetEntries(m_prep_cut)

    print '==== Prep Eff ===='
    print "Total Events   : ", total_evt
    print "Muon Prep Count(%): ", m_prep_count,'('+str(round(m_prep_count/total_evt*100,2))+'%)'
    print "Ele Prep Count(%) : ", e_prep_count,'('+str(round(e_prep_count/total_evt*100,2))+'%)'

    e_vpt_count = 1.* tree.GetEntries(e_vpt_cut)
    m_vpt_count = 1.* tree.GetEntries(m_vpt_cut)
    
    print '\n\n==== V pT Eff ===='
    print "Muon Count(%): ", m_vpt_count,'('+str(round(m_vpt_count/m_prep_count*100,2))+'%)'
    print "Ele Count(%) : ", e_vpt_count,'('+str(round(e_vpt_count/e_prep_count*100,2))+'%)'
    
    e_csv1_count = 1.* tree.GetEntries(e_csv1_cut)
    m_csv1_count = 1.* tree.GetEntries(m_csv1_cut)

    print '\n\n==== CSV1 Eff ===='
    print "Muon Count(%): ", m_csv1_count,'('+str(round(m_csv1_count/m_vpt_count*100,2))+'%)'
    print "Ele Count(%) : ", e_csv1_count,'('+str(round(e_csv1_count/e_vpt_count*100,2))+'%)'
    

    e_csv2_count = 1.* tree.GetEntries(e_csv2_cut)
    m_csv2_count = 1.* tree.GetEntries(m_csv2_cut)

    print '\n\n==== CSV2 Eff ===='
    print "Muon Count(%): ", m_csv2_count,'('+str(round(m_csv2_count/m_csv1_count*100,2))+'%)'
    print "Ele Count(%) : ", e_csv2_count,'('+str(round(e_csv2_count/e_csv1_count*100,2))+'%)'
    
    e_mjj_count = 1.* tree.GetEntries(e_mjj_cut)
    m_mjj_count = 1.* tree.GetEntries(m_mjj_cut)

    print '\n\n==== Mjj Eff ===='
    print "Muon Count(%): ", m_mjj_count,'('+str(round(m_mjj_count/m_csv2_count*100,2))+'%)'
    print "Ele Count(%) : ", e_mjj_count,'('+str(round(e_mjj_count/e_csv2_count*100,2))+'%)'
    
