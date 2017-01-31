from ROOT import *
from ROOT import gROOT
from matplotlib import interactive


#Get old file, old tree and set top branch address
oldfile = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/v10_PU20bx25/DY_inclusive.root')

oldtree  = oldfile.Get("tree")
nentries = oldtree.GetEntries()

#Create a new file + a clone of old tree in new file
newfile = TFile('/exports/uftrig01a/dcurry/data/bbar/13TeV/heppy/v10_PU20bx25/DY_inclusive_0to100.root', 'recreate')

newtree = oldtree.CloneTree(0)

for i in range(nentries):
 
    if i%5000 == 0: print '---> Looping over event # ', i
    
    oldtree.GetEntry(i)
    
    if oldtree.lheHT < 100: 
        newtree.Fill()
        

#newtree.Print()
newtree.AutoSave()
del oldfile
del newfile
