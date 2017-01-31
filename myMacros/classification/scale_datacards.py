import os
from ROOT import *

oldLumi = 2.32
newLumi = 20.0

dirName = "20fb"

old_dir = "/afs/cern.ch/work/d/dcurry/public/bbar_heppy/CMSSW_7_1_5/src/VHbb/limits/5_30_DC_v2/" 


oldFileNames = [
    old_dir+"vhbb_TH_BDT_M125_Zee_HighPt.root",
    old_dir+"vhbb_TH_Zhf.root",
    old_dir+"vhbb_TH_Zlf.root",
    old_dir+"vhbb_TH_ttbar.root",
    old_dir+"vhbb_TH_BDT_M125_Zuu_HighPt.root",
    ]


def scaleDC(oldFileName, newFileName, scale):
    print "DC - Opening: ",oldFileName+" . Writing:",newFileName
    fOld = open(oldFileName)
    fNew = open(newFileName, 'w')

    for line in fOld.readlines():
        if 'rate' == line[:4] or 'observation' == line[:11]:
            newLine = ""
            for word in line.split("\t"):
                try:
                    num = eval(word)
                except:
                    num = 0.0
                if num>0:
                    word = str(num*scale)
                newLine = newLine + word + " "
            line = newLine
        fNew.write(line)

    fOld.close()
    fNew.close()

def scaleHistos(oldFileName, newFileName, scale):

    print "Opening: ",oldFileName+" . Writing:",newFileName

    fileOld = TFile(oldFileName)
    fileOld.ls()

    if 'Zee_HighPt' in oldFileName:
        Dir = fileOld.Get("ZeeHighPt_13TeV")

    if 'Zuu_HighPt' in oldFileName:
        Dir = fileOld.Get("ZuuHighPt_13TeV")

    if 'LowPt'in oldFileName:
        Dir = fileOld.Get("ZeeLowPt_13TeV")    
        
    if 'Zhf' in oldFileName:
         Dir = fileOld.Get("Zhf")

    if 'Zlf' in oldFileName:
        Dir = fileOld.Get("Zlf")

    if 'ttbar' in oldFileName:
        Dir = fileOld.Get("ttbar")

    print 'dir:',dir

    assert(type(Dir)==TDirectoryFile)
    fileNew = TFile(newFileName,"recreate")

    if 'Zee_HighPt' in oldFileName:
        newDir = fileNew.mkdir("ZeeHighPt_13TeV")
    
    if 'Zuu_HighPt' in oldFileName:
        newDir = fileNew.mkdir("ZuuHighPt_13TeV")

    if 'LowPt' in oldFileName:
        newDir = fileNew.mkdir("ZeeLowPt_13TeV")

    if 'Zhf' in oldFileName:
        newDir = fileNew.mkdir("Zhf")

    if 'Zlf' in oldFileName:
        newDir = fileNew.mkdir("Zlf")

    if 'ttbar' in oldFileName:
        newDir = fileNew.mkdir("ttbar")

    newDir.cd()
    for i in Dir.GetListOfKeys():
        obj = i.ReadObj()
        obj = obj.Clone(obj.GetName())
        obj.Scale(scale)
        if obj.GetName()=="TTCMS_vhbb_bTagHFWeightHFStats1Up":
            print obj.GetName(), obj.GetMaximum() 
        obj.Write()
    fileNew.Close()
    return

scale = newLumi/oldLumi

oldFileName = oldFileNames[0]
try:
    os.mkdir(oldFileName.split("vhbb_")[0]+dirName)
except:
    pass

for oldFileName in oldFileNames:
    newFileName = oldFileName.replace("vhbb_",dirName+"/vhbb_")
    oldFileNameDC = (oldFileName.replace("vhbb_TH","vhbb_DC_TH")).replace(".root",".txt")
    newFileNameDC = (newFileName.replace("vhbb_TH","vhbb_DC_TH")).replace(".root",".txt")
    
    scaleHistos(oldFileName, newFileName, scale)
    scaleDC(oldFileNameDC, newFileNameDC, scale)
