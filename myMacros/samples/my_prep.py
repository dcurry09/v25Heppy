#! /usr/bin/env python
import os, pickle, sys, ROOT
ROOT.gROOT.SetBatch(True)
import time
import multiprocessing


pathIN  = '/exports/uftrig01a/dcurry/heppy/v24/'
pathOUT = '/exports/uftrig01a/dcurry/heppy/v24/'

file_list = [
    #'Zuu_B_ext1', 'Zuu_B_ext2', 'Zuu_B_ext3', 'Zuu_B_ext4', 'Zuu_C_ext1', 'Zuu_C_ext2', 'Zuu_D_ext1', 'Zuu_D_ext2',
    #'Zuu_E_ext1', 'Zuu_E_ext2', 'Zuu_F_ext1', 'Zuu_G_ext1', 'Zuu_G_ext2', 'Zuu_G_ext3',
    #'Zee_B_ext1', 'Zee_B_ext2', 'Zee_B_ext3', 'Zee_B_ext4', 'Zee_C_ext1', 'Zee_C_ext2', 'Zee_D_ext1', 'Zee_D_ext2',
    #'Zee_E_ext1', 'Zee_E_ext2', 'Zee_F_ext1', 'Zee_G_ext1', 'Zee_G_ext2', 'Zee_G_ext3'
    
    #'ttbar_ext1', 'ttbar_ext2', 'ttbar_ext3',
    #'ttbar_ext1_NewExt', 'ttbar_ext2_NewExt', 'ttbar_ext3_NewExt',
    #'ttbar_ext1_NewExt2', 'ttbar_ext2_NewExt2', 'ttbar_ext3_NewExt2'
    
    #'ST_t_ext1', 'ST_t_ext1_NewExt', 'ST_t_ext1_NewExt2'
    #'DY_600to800_ext1', 'DY_600to800_ext1_NewExt', 'DY_600to800_ext1_NewExt2'
    ]

newprefix = 'prep_' 

prefix = ''

Aprefix = ''


# CUTS
prep_cut = 'abs(Jet_eta[hJCMVAV2idx[0]]) < 2.4 & abs(Jet_eta[hJCMVAV2idx[1]]) < 2.4 & vLeptons_pt[0] > 20. & vLeptons_pt[1] > 20.'

zee_cut = prep_cut + ' & Vtype == 1 & json == 1'
# & HLT_BIT_HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf_v'

zuu_cut = prep_cut + ' & Vtype == 0 & json == 1'
# & HLT_BIT_HLT_DoubleIsoMu17_eta2p1_v'

ttbar_cut = prep_cut + ' & Vtype > -1 & Vtype < 2'

def copytree(pathIN,pathOUT,prefix,newprefix,file,Aprefix,Acut):

    start = time.time()

    print "##### COPY TREE - BEGIN ######"
    print "Input File : %s/%s%s.root " %(pathIN,prefix,file)
    print "Output File : %s/%s%s%s.root" %(pathOUT,newprefix,Aprefix,file)

    input = ROOT.TFile.Open("%s/%s%s.root" %(pathIN,prefix,file),'read')
    output = ROOT.TFile.Open("%s/%s%s%s.root" %(pathOUT,newprefix,Aprefix,file),'recreate')

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

    tree.SetBranchStatus('selLeptons*', 0)

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
