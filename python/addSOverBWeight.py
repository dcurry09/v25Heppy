
#!/usr/bin/env python

from ROOT import *
from optparse import OptionParser
import sys
import numpy
import os
import multiprocessing
from myutils import BetterConfigParser, TdrStyles, getRatio
import ConfigParser
import ROOT

## Usage: python addSOverBWeight.py [inputntuple] [outputntuple]
## Adds a branch, "sb_weight", with the per-event S/S+B weight for
## the events corresponding bin in the SR BDT Score distribution
## To be applied to all MC and data.

#ROOT.gSystem.SetBatch(True)


# ========================================
argv = sys.argv
parser = OptionParser()
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration file")
(opts, args) = parser.parse_args(argv)
config = BetterConfigParser()
config.read(opts.config)

outpath = '/afs/cern.ch/user/d/dcurry/www/TEST/'

# Make the dir and copy the website ini files
try:
    os.system('mkdir '+outpath)
except:
     print outpath+' already exists...'

temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outpath

os.system(temp_string2)
os.system(temp_string3)

ROOT.gSystem.Load('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/interface/VHbbNameSpace_h.so')

# =========================================

# sample prefix
prefix = 'v25_'

inpath = '/exports/uftrig01a/dcurry/heppy/files/MVA_out/'
outpath = '/exports/uftrig01a/dcurry/heppy/files/SoverB_out/'

config = BetterConfigParser()
config.read('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/python/13TeVconfig/general')
config.read('/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/python/13TeVconfig/cuts')

#signal_region_cut =  eval(config.get('Cuts','bdt_high_Zpt'))
signal_region_cut = '(Vtype==1 | Vtype==0) & Vtype > -1 & Vtype < 2 & Jet_btagCMVAV2[hJCMVAV2idx[0]] > -0.716 & Jet_btagCMVAV2[hJCMVAV2idx[1]] > -0.716 & V_mass>75. & V_mass < 105. & V_pt < 2000. & H_pt < 999. & H_pt > 0. & H_mass < 9999. & H_mass > 0. & V_pt > 150.& H_pt < 999. & H_pt > 0. & H_mass < 9999. & H_mass > 0. & V_pt < 2000. & Jet_puId[hJCMVAV2idx[0]] >= 4 & Jet_puId[hJCMVAV2idx[1]] >= 4 & (((Vtype==1) & vLeptons_relIso03[0] < 0.15 & vLeptons_relIso03[1] < 0.15 & vLeptons_pt[0] > 20. & vLeptons_pt[1] > 20.0) || ((Vtype==0) & vLeptons_relIso04[0] < 0.25 & vLeptons_relIso04[1] < 0.25 & vLeptons_pt[0] > 20. & vLeptons_pt[1] > 20.)) & run<=276811 & V_pt > -25.0 & HCMVAV2_reg_mass < 150. & HCMVAV2_reg_mass > 90. & Jet_pt_reg[hJCMVAV2idx[0]] > 20. & Jet_pt_reg[hJCMVAV2idx[1]] > 20.'

#event_weight = eval(config.get('Weights','weightF_bdt'))
event_weight ='sign(genWeight)*VHbb::puWeight_ichep(nTrueInt)*btagWeightCMVAV2[0]*((Vtype == 1)*eId90SFWeight[0]*eTrackerSFWeight[0]*eTrigSFWeight_ele27[0] + (Vtype == 0)*mIsoSFWeight[0]*vLeptons_SF_IdCutLoose[0]*vLeptons_SF_IdCutLoose[1]*vLeptons_SF_trk_eta[0]*vLeptons_SF_trk_eta[1]*mTrigSFWeight_ICHEP[0])*DY_specialWeight'

print 'Signal Region:', signal_region_cut
print 'event weight:', event_weight

var = "gg_plus_ZH125_highZpt.Nominal" # variable to use to categorize by S/B
xmin = -1.0
xmax = 1.0

'''
print '\nCreating TChains...'
# input for calculating S / S+B weight.  I have merged DY into one file. ZH and ttbar are as is.
tree_weight_BKG = TChain("tree")
tree_weight_BKG.Add(inpath+prefix+'DY_inclusive.root')
#tree_weight_BKG.Add(inpath+prefix+'DY_100to200.root')
tree_weight_BKG.Add(inpath+prefix+'DY_200to400.root')
tree_weight_BKG.Add(inpath+prefix+'DY_400to600.root')
tree_weight_BKG.Add(inpath+prefix+'DY_600toInf.root')
tree_weight_BKG.Add(inpath+prefix+'DY_Bjets.root')
tree_weight_BKG.Add(inpath+prefix+'DY_BgenFilter.root')
tree_weight_BKG.Add(inpath+prefix+'ttbar.root')
tree_weight_BKG.Add(inpath+prefix+'ZZ_2L2Q.root')
tree_weight_BKG.Add(inpath+prefix+'ST_s.root')
tree_weight_BKG.Add(inpath+prefix+'ST_tW_antitop.root')
tree_weight_BKG.Add(inpath+prefix+'WZ.root')

tree_weight_SIG = TChain("tree")
tree_weight_SIG.Add(inpath+prefix+'ZH125.root')
tree_weight_SIG.Add(inpath+prefix+'ggZH125.root')

#binedges = [-1.,    -0.886, -0.746, -0.606, -0.466, -0.326, -0.186, -0.046,  0.094,  0.234,  0.374,  0.514,  0.654,  0.794,  0.934,  1.   ] 
#binedge_array = numpy.zeros(len(binedges),dtype=float)
#for i in range(len(binedges)):
#    binedge_array[i] = binedges[i]

print '\nDrawing Weight Histograms...'
tree_weight_SIG.Draw("%s>>hSig" %var,"((%s)*(%s))" % (signal_region_cut,event_weight))
tree_weight_BKG.Draw("%s>>hBkg" %var,"((%s)*(%s))" % (signal_region_cut,event_weight))
'''
#hSig1 = TH1F("hSig","hSig", 15, -1, 1)
#hBkg1 = TH1F("hBkg","hBkg", 15, -1, 1)


# List of files to add btag weights to
bkg_list = ['DY_inclusive', 'ttbar', 'ZZ_2L2Q', 'WZ', 'ZZ']

data_list = ['Zuu', 'Zee']

signal_list = ['ZH125', 'ggZH125']

DY_list = ['DY_100to200', 'DY_200to400', 'DY_400to600', 'DY_600to800', 'DY_800to1200', 'DY_1200to2500', 'DY_2500toInf', 'DY_Bjets', 'DY_BgenFilter', 'DY_600toInf'
           #'DY_inclusive_nlo', 'DY_Pt100to250', 'DY_Pt250to400','DY_Pt400to650','DY_Pt650toInf'
           ]

ST_list = ['ST_s', 'ST_tW_top', 'ST_tW_antitop', 'ST_t', 'ST_t_antitop']


#file_list = bkg_list + data_list + signal_list + DY_list + ST_list
file_list = ['ZH125']


for file in file_list:
#def osSystem(file):

    print '\nAdding S/S+B weights to sample:', inpath+prefix+file+'.root'
    print 'Output File                  :', outpath+prefix+file+'.root'

    ifile = ROOT.TFile.Open(inpath+prefix+file+'.root', 'read')
    ofile = ROOT.TFile(outpath+prefix+file+'.root', 'recreate')

    ifile.cd()

    tree = ifile.Get('tree')

    obj = ROOT.TObject
    for key in ROOT.gDirectory.GetListOfKeys():
        ifile.cd()
        obj = key.ReadObj()
        if obj.GetName() == 'tree':
            continue
        ofile.cd()
        obj.Write(key.GetName())

    ofile.cd()

    otree = tree.CloneTree(0)

    sb_weight = numpy.zeros(1,dtype=float)
    otree.Branch("sb_weight",sb_weight,"sb_weight/D")

    #tree.SetBranchAddress.('gg_plus_ZH125_highZpt', gg_plus_ZH125_highZpt, 'Nominal:JER_up:JER_down:JES_up:JES_down:JER_up_high:JER_down_high:JER_up_low:JER_down_low:JER_up_central:JER_down_central:JER_up_forward:JER_down_forward:JEC_up_high:JEC_down_high:JEC_up_low:JEC_down_low:JEC_up_central:JEC_down_central:JEC_up_forward:JEC_down_forward/F')


    #for entry in tree:
    #    print entry.gg_plus_ZH125_highZpt.Nominal
        
    
    nentries = tree.GetEntries()
    print "total entries: %i " % nentries
    for ientry in range(nentries):
        
        if (ientry % 10000 == 0): 
            print "processing entry: %i" % ientry
            
        if ientry > 1000: continue

        tree.GetEntry(ientry)
        
        tree.Print()
        
        for p in tree.gg_plus_ZH125_highZpt:
            val = p.Nominal
        
        val_bin = hSig.FindBin(val)
        s = hSig.GetBinContent(val_bin)
        b = hBkg.GetBinContent(val_bin)
        sb_weight[0] = s / (s+b)
        
        print val,sb_weight[0]
        
        otree.Fill()
        


    #otree.Write()
    otree.AutoSave()
    ofile.Close()
    ifile.Close()
    print 'Finished...'    


# plot weights for validity checks
canv = TCanvas("canv","canv")
hTot = hSig.Clone()
hTot.Add(hBkg)
hSig.Divide(hTot) # S / S+B
hSig.Draw("hist")
canv.SaveAs("sb_weights.pdf")
canv.SetLogy(True)
canv.SaveAs("sb_weights_log.pdf")


