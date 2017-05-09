##########################################
# For calculating DY stitching Weights
#
#
##########################################

import ROOT
import numpy as np

path = '/exports/uftrig01a/dcurry/heppy/files/btag_out/v25_' 



def getWeight(fileInc, fileB, region):

    countInc=0
    # print 'region',region,'\n'
    for file in fileInc:
        print 'file inc is', file
        f = ROOT.TFile.Open(path+file+".root")
        # print 'adding',file
        tree = f.Get("tree")
        #if file in SampleCuts:
        #    print'taking additional', SampleCuts[file], ' cut for', file
        #    region = region +'&('+SampleCuts[file]+')'
        countInc    = countInc + 1.* tree.Draw("",region)
        print 'countInc',countInc,'\n'
        #countInc    = 1.* tree.GetEntries(region)
        f.Close()

    countB=0
    for file in fileB:
        print 'fileB inc is', file
        f = ROOT.TFile.Open(path+file+".root")
        # print 'adding',file
        tree = f.Get("tree")
        #if file in SampleCuts:
        #    print'taking additional', SampleCuts[file], ' cut for', file
        #    #region = region +'&('+SampleCuts[file]+')'
        #    countB      = countB + 1.* tree.Draw("",region +'&('+SampleCuts[file]+')')
        #else:
        countB      = countB + 1.* tree.Draw("",region)
        print 'nEvents for file', file, 'is:', countB
        #print 'countB',countB,'\n'
        #countB      = 1.* tree.GetEntries(region)
        f.Close()
    print 'countInc is', countInc
    print 'countB is', countB
    weight = countInc/(countB+countInc)
    return weight

def getExtWeight(files):

    Weights = []

    countWeights = 0
    for file in files:
        f = ROOT.TFile.Open(path+file+".root")
        tree = f.Get("tree")
        nevents = 1.* tree.Draw("","1")
        print '#Events for', file, ' are', nevents
        countWeights = countWeights + nevents
        Weights.append(nevents)
        f.Close()

    #    print 'countWeights is'
    for weight, file in zip(Weights, files):
        print 'Weight for sample', file, 'is', weight/countWeights


ZLLjetsHT0       = "DY_inclusive"
#ZLLjetsHT70      = "DY_70to100"
ZLLjetsHT100     = "DY_100to200"
ZLLjetsHT200     = "DY_200to400"
ZLLjetsHT400     = "DY_400to600"
ZLLjetsHT600     = ["DY_600to800_ext1","DY_600to800_ext2","DY_600to800_ext3","DY_600to800_ext4","DY_600to800_ext5","DY_600to800_ext6"]
ZLLjetsHT600_ext1 = "DY_600to800_ext1"
ZLLjetsHT600_ext2 = "DY_600to800_ext2"
ZLLjetsHT600_ext3 = "DY_600to800_ext3"
ZLLjetsHT800      = ["DY_800to1200_ext1","DY_800to1200_ext2"]
ZLLjetsHT800_ext1 = "DY_800to1200_ext1" 
ZLLjetsHT800_ext2 = "DY_800to1200_ext2"

ZLLjetsHT1200    = "DY_1200to2500"
ZLLjetsHT2500    = "DY_2500toInf"



ZlljetsHTbinned = [
    ZLLjetsHT0, ZLLjetsHT100, ZLLjetsHT200, ZLLjetsHT400, ZLLjetsHT600_ext1, ZLLjetsHT600_ext2, ZLLjetsHT600_ext3,
    ZLLjetsHT800_ext1, ZLLjetsHT800_ext2, ZLLjetsHT1200, ZLLjetsHT2500
    ]


ZLLBjets = ["DY_Bjets", "DY_Bjets_Vpt100to200", "DY_Bjets_Vpt200toInf", "DY_Bjets_Vpt100to200_ext2", "DY_Bjets_Vpt200toInf_ext2"]

DY_Bjets_Vpt100to200 = ["DY_Bjets_Vpt100to200", "DY_Bjets_Vpt100to200_ext2"]

DY_Bjets_Vpt200toInf = ["DY_Bjets_Vpt200toInf", "DY_Bjets_Vpt200toInf_ext2"]

DYBJets          = "(lheNb>0)"
DYJetsBGenFilter = "(lheNb==0 && nGenStatus2bHad>0)"

VPT0              = "(lheV_pt<100)"
VPT100            = "(lheV_pt>100 && lheV_pt<200)"
VPT200            = "(lheV_pt>200)"


#print "weightZBjetsVpt0=\t%.2f\n"   %getWeight(ZlljetsHTbinned, ZLLBjets, VPT0)
#print "weightZBjetsVpt100=\t%.2f\n"   %getWeight(ZlljetsHTbinned, ZLLBjets, VPT100)
#print "weightZBjetsVpt200=\t%.2f\n"   %getWeight(ZlljetsHTbinned, ZLLBjets, VPT200)

getExtWeight(ZLLjetsHT600)

#getExtWeight(ZLLjetsHT800)

#getExtWeight(DY_Bjets_Vpt100to200)

#getExtWeight(DY_Bjets_Vpt200toInf)
