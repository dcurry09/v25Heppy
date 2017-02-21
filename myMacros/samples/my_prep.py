#! /usr/bin/env python
import os, pickle, sys, ROOT
ROOT.gROOT.SetBatch(True)
import time
import multiprocessing


#pathIN  = '/exports/uftrig01a/dcurry/heppy/v25/'
#pathOUT = '/exports/uftrig01a/dcurry/heppy/v25/'

pathIN  = '/exports/uftrig01a/dcurry/heppy/files/vtype_out/'
pathOUT = '/exports/uftrig01a/dcurry/heppy/files/prep_out/'

file_list = [
    #'Zuu_B_ext1', 'Zuu_B_ext2', 'Zuu_B_ext3',
    #'Zuu_C_ext1', 'Zee_C_ext1',
    #'Zuu_D_ext1', 'Zuu_D_ext2', 
    #'Zuu_E_ext1', 'Zee_E_ext1', 
    #'Zuu_F_ext1', 'Zee_F_ext1',
    #'Zuu_G_ext1', 'Zuu_G_ext2', 'Zee_G_ext1', 'Zee_G_ext2',
    #'Zuu_H_ext1', 'Zuu_H_ext2', 'Zee_H_ext1', 'Zee_H_ext2', 
    #'Zuu_H_ext3', 'Zuu_H_ext4', 'Zee_H_ext3', 'Zee_H_ext4',
    
    #'Zee_B_ext1', 'Zee_B_ext2', 'Zee_B_ext3',
    #'Zee_C_ext1',
    #'Zee_D_ext1', 'Zee_D_ext2',
    #'Zee_E_ext1',
    #'Zee_F_ext1',
    #'Zee_G_ext1', 'Zee_G_ext2',
    #'Zee_G_ext3', 'Zee_G_ext4'
    #'Zee_H_ext1', 'Zee_H_ext2', 'Zee_H_ext3', 'Zee_H_ext4'
    
    #'ttbar_ext1', 'ttbar_ext2',
    #'ttbar_ext1_NewExt', 'ttbar_ext2_NewExt',
    #'ttbar_ext1_NewExt2', 'ttbar_ext2_NewExt2',
    #'ttbar_ext1_NewExt3', 'ttbar_ext2_NewExt3',
    #'ttbar_ext1_NewExt4', 'ttbar_ext2_NewExt4',
    #'ttbar_ext1_NewExt5', 'ttbar_ext2_NewExt5',

    #'ST_t_ext1', 'ST_t_ext1_NewExt', 'ST_t_ext1_NewExt2',

    #'DY_600to800_ext1', 'DY_600to800_ext1_NewExt', 'DY_600to800_ext1_NewExt2'
    
    'DY_2J', 'DY_2J_NewExt1', 'DY_2J_NewExt2', 'DY_2J_NewExt3', 'DY_2J_NewExt4', 'DY_2J_NewExt5', 'DY_2J_NewExt6', 'DY_2J_NewExt7', 'DY_2J_NewExt8'
    
    #'DY2J'

    ]

newprefix = 'prep_' 

#prefix = ''
prefix = 'prep_'

Aprefix = ''


# CUTS
zee_data_triggers = 'HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v'

zuu_data_triggers = '(HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v || HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v || HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v || HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v)'

#prep_cut = '((abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4) || (abs(Jet_eta[hJCMVAV2idx[0]]) < 2.4 & abs(Jet_eta[hJCMVAV2idx[1]]) < 2.4)) & ((Jet_pt_reg[hJCidx[0]] > 18 & Jet_pt_reg[hJCidx[1]] > 18) || (Jet_pt_reg[hJCMVAV2idx[0]] > 18 & Jet_pt_reg[hJCMVAV2idx[1]] > 18)) & Vtype != 2'

prep_cut = '((abs(Jet_eta[hJCidx[0]]) < 2.4 & abs(Jet_eta[hJCidx[1]]) < 2.4) || (abs(Jet_eta[hJCMVAV2idx[0]]) < 2.4 & abs(Jet_eta[hJCMVAV2idx[1]]) < 2.4)) & ((Jet_pt_reg[hJCidx[0]\
] > 18 & Jet_pt_reg[hJCidx[1]] > 18) || (Jet_pt_reg[hJCMVAV2idx[0]] > 18 & Jet_pt_reg[hJCMVAV2idx[1]] > 18)) & ((Vtype_new < 2 & Vtype_new > -1) || (Vtype < 2 & Vtype > -1)) & (V_new_pt > 50 || V_pt > 50)'

zee_cut = prep_cut + ' & Vtype != 2 & json == 1 & HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v==1'
#zee_cut = prep_cut + ' & Vtype != 2 & json == 1'

zuu_cut = prep_cut + ' & Vtype != 2 & json == 1 & (HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v==1 || HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v==1 || HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v==1 || HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v==1)'
#zuu_cut = prep_cut + ' & Vtype != 2 & json == 1'

#ttbar_cut = prep_cut + ' & Vtype != 2 & (HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v==1 || (HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v || HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v || HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v || HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v))'

ttbar_cut = prep_cut + ' & (HLT_BIT_HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v==1 || (HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v || HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_v || HLT_BIT_HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v || HLT_BIT_HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v))'




def copytree(pathIN,pathOUT,prefix,newprefix,file,Aprefix,Acut):

    start = time.time()

    print "##### COPY TREE - BEGIN ######"
    print "Input File : %s/%s%s.root " %(pathIN,prefix,file)
    print "Output File : %s/%s%s%s.root" %(pathOUT,newprefix,Aprefix,file)

    input = ROOT.TFile.Open("%s/%s%s.root" %(pathIN,prefix,file),'read')
    output = ROOT.TFile.Open("%s/%s%s%s.root" %(pathOUT,newprefix,Aprefix,file),'recreate')
    
    # if 'DY2J' in file:
    #     pathIN  = '/exports/uftrig01a/dcurry/heppy/btag_out/'
    #     pathOUT = '/exports/uftrig01a/dcurry/heppy/btag_out/'
    #     prefix = 'V25_'
    #     input = ROOT.TFile.Open("%s/%s%s.root" %(pathIN,prefix,file),'read')
    #     output = ROOT.TFile.Open("%s/%s%s%s_ext1.root" %(pathOUT,prefix,file),'recreate')
    #     output = ROOT.TFile.Open("%s/%s%s%s_ext2.root" %(pathOUT,prefix,file),'recreate')

    input.cd()

    obj = ROOT.TObject
    for key in ROOT.gDirectory.GetListOfKeys():
        input.cd()
        obj = key.ReadObj()
        #print obj.GetName()
        if obj.GetName() == 'tree':
            continue
        output.cd()
        #print key.GetName()
        obj.Write(key.GetName())

    inputTree = input.Get("tree")
    nEntries = inputTree.GetEntries()

    # Turn of branches we do not need
    #inputTree = branch_reduce(inputTree)
    
    output.cd()
    print '\n\t copy file: %s with cut: %s' %(file,Acut)
    outputTree = inputTree.CopyTree(Acut)
    kEntries = outputTree.GetEntries()
    #printc('blue','',"\t before cuts\t %s" %nEntries)
    #printc('green','',"\t survived\t %s" %kEntries)
    outputTree.AutoSave()
    output.ls()
    print "Writing output file"
    output.Write()
    print "Closing output file"
    output.Close()
    print "Closing input file"
    input.Close()

    print "##### COPY TREE - END ######"

    end = time.time()

    print '\n-----> Total Prep Time: ', end - start


def branch_reduce(tree):

    print '\n     ----> Reducing Branches...'

    #tree.SetBranchStatus('Flag*', 0)

    #tree.SetBranchStatus('HLT*', 0)

    #tree.SetBranchStatus('met_shifted*', 0)

    tree.SetBranchStatus('H3cj*', 0)

    tree.SetBranchStatus('ungroomed*', 0)

    #tree.SetBranchStatus('selLeptons*', 0)

    tree.SetBranchStatus('TauGood*', 0)

    #tree.SetBranchStatus('GenHad*', 0)

    tree.SetBranchStatus('htt*', 0)

    #tree.SetBranchStatus('GenWZ*', 0)

    #tree.SetBranchStatus('GenBQuarkFromHafter*', 0)

    tree.SetBranchStatus('trimmedFat*', 0)

    #tree.SetBranchStatus('GenBQuarkFromTop*', 0)

    tree.SetBranchStatus('Fat*', 0)

    tree.SetBranchStatus('Subjet*', 0)

    tree.SetBranchStatus('Discarded*', 0)

    return tree


def myPrep(file):

    if 'Zuu' in file:
        copytree(pathIN,pathOUT,prefix,newprefix,file,Aprefix,zuu_cut)

    elif 'Zee' in file:
        copytree(pathIN,pathOUT,prefix,newprefix,file,Aprefix,zee_cut)

    else: 
        copytree(pathIN,pathOUT,prefix,newprefix,file,Aprefix,ttbar_cut)

# define the multiprocessing object
p = multiprocessing.Pool()
results = p.imap(myPrep, file_list)
p.close()
p.join()
