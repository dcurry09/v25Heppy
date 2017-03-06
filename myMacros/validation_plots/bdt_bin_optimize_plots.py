import sys
import os
import re
from ROOT import *
from matplotlib import interactive
from ROOT import gROOT
gROOT.SetBatch(True)

## Store the plots on website ##
outpath = '/afs/cern.ch/user/d/dcurry/www/v25_BDT_binOptimize/'
try: os.system('mkdir '+outpath)
except: print outpath+' already exists...'
temp_string2 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/.htaccess '+outpath
temp_string3 = 'cp /afs/cern.ch/user/d/dcurry/www/zllHbbPlots/index.php '+outpath
os.system(temp_string2)
os.system(temp_string3)
###################################

inpath = '/afs/cern.ch/work/d/dcurry/public/v25Heppy/CMSSW_7_4_7/src/VHbb/limits/bdt_param_optimize/'

bdt_bin_list = ['10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','30']

binDict = {}

stack_SoverB  = THStack('stack_SoverB', '')
canvas_SoverB = TCanvas('canvas_SoverB')

leg1 = TLegend(0.1,0.4,0.3,0.6)
leg1.SetFillStyle(0)
leg1.SetBorderSize(0)

for bin in bdt_bin_list:
    
    print '\n # of BDT Bins:', bin
    
    file = TFile.Open(inpath+'BDT_bins'+bin+'/vhbb_TH_BDT_Zuu_HighPt.root', 'read')
    file.cd('ZuuHighPt_13TeV')
    
    binDict[bin+'_BKG'] = gDirectory.Get('Zj2b')
    Z1b     = gDirectory.Get('Zj1b')
    Zlight  = gDirectory.Get('Zj0b')
    ttbar   = gDirectory.Get('TT')
    
    binDict[bin+'_SIG']   = gDirectory.Get('ZH')
    ggZH125 = gDirectory.Get('ggZH')
    
    stack  = THStack('stack', '')
    canvas = TCanvas('canvas')
    
    # # Add the backgrounds
    binDict[bin+'_BKG'].Add(Z1b)
    binDict[bin+'_BKG'].Add(Zlight)
    binDict[bin+'_BKG'].Add(ttbar)
    binDict[bin+'_BKG'].SetLineColor(kBlue)
    binDict[bin+'_BKG'].SetLineStyle(1)
    
     # Add the signals
    binDict[bin+'_SIG'].Add(ggZH125)
    binDict[bin+'_SIG'].SetLineColor(kRed)
    binDict[bin+'_SIG'].SetLineStyle(1)
    
    leg = TLegend(0.1,0.4,0.3,0.6)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(binDict[bin+'_BKG'], 'BKG', 'l')
    leg.AddEntry(binDict[bin+'_SIG'], 'SIG', 'l')

    canvas.cd()
    canvas.SetLogy()
    stack.Add(binDict[bin+'_BKG'])
    stack.Add(binDict[bin+'_SIG'])
    stack.Draw('nostackHIST')
    leg.Draw('same')
    
    canvas.SaveAs(outpath+'bdt_'+bin+'bins_SR.pdf')
    canvas.SaveAs(outpath+'bdt_'+bin+'bins_SR.png')

    
    # Nopw add to the SoverB Plot
    #binDict[bin+'_SIG'].Divide(binDict[bin+'_BKG'])
    

    canvas.Close()
    stack.Delete()
    file.Close()


# Now all bins on one plot
color_list = [5,41,596,840,922,18,416]#,2,3,46,402]

stack_SoverB  = THStack('stack', '')
canvas_SoverB = TCanvas('canvas')
canvas_SoverB.cd()
gStyle.SetPalette(1)

# Lop over Bins
file1 = TFile.Open(inpath+'BDT_bins10/vhbb_TH_BDT_Zuu_HighPt.root', 'read')
file1.cd('ZuuHighPt_13TeV')
Z2b     = gDirectory.Get('Zj2b')
Z1b     = gDirectory.Get('Zj1b')
Zlight  = gDirectory.Get('Zj0b')
ttbar   = gDirectory.Get('TT')
ZH125   = gDirectory.Get('ZH')
ggZH125 = gDirectory.Get('ggZH')
# # Add the backgrounds
Z2b.Add(Z1b)
Z2b.Add(Zlight)
Z2b.Add(ttbar)
# Add the signals
ZH125.Add(ggZH125)
ZH125.SetStats(0)
ZH125.GetXaxis().SetTitle('# BDT Bins')
ZH125.GetYaxis().SetTitle('S/B')
ZH125.SetLineStyle(1)
ZH125.SetMarkerStyle(20)
ZH125.SetMarkerColor(kBlue)
ZH125.Divide(Z2b)
ZH125.Draw("PLC")
leg1.AddEntry(ZH125, '10 Bins', 'l')
canvas_SoverB.Update()



file2 = TFile.Open(inpath+'BDT_bins15/vhbb_TH_BDT_Zuu_HighPt.root', 'read')
file2.cd('ZuuHighPt_13TeV')
Z2b     = gDirectory.Get('Zj2b')
Z1b     = gDirectory.Get('Zj1b')
Zlight  = gDirectory.Get('Zj0b')
ttbar   = gDirectory.Get('TT')
ZH125   = gDirectory.Get('ZH')
ggZH125 = gDirectory.Get('ggZH')
# # Add the backgrounds
Z2b.Add(Z1b)
Z2b.Add(Zlight)
Z2b.Add(ttbar)
# Add the signals
ZH125.Add(ggZH125)
ZH125.Divide(Z2b)
ZH125.SetLineStyle(1)
ZH125.SetMarkerStyle(22)
ZH125.SetMarkerColor(kRed)
ZH125.SetLineColor(kRed)
ZH125.Draw("SAME PLC")
leg1.AddEntry(ZH125, '15 Bins', 'l')
canvas_SoverB.Update()


file3 = TFile.Open(inpath+'BDT_bins25/vhbb_TH_BDT_Zuu_HighPt.root', 'read')
file3.cd('ZuuHighPt_13TeV')
Z2b     = gDirectory.Get('Zj2b')
Z1b     = gDirectory.Get('Zj1b')
Zlight  = gDirectory.Get('Zj0b')
ttbar   = gDirectory.Get('TT')
ZH125   = gDirectory.Get('ZH')
ggZH125 = gDirectory.Get('ggZH')
# # Add the backgrounds
Z2b.Add(Z1b)
Z2b.Add(Zlight)
Z2b.Add(ttbar)
ZH125.SetMarkerStyle(23)
ZH125.SetMarkerColor(kGreen)
ZH125.SetLineColor(kGreen)
# Add the signals
ZH125.Add(ggZH125)
ZH125.Divide(Z2b)
leg1.AddEntry(ZH125, '25 Bins', 'l')
ZH125.Draw("SAME PLC PMC")

leg1.Draw('same')




canvas_SoverB.SaveAs(outpath+'bdt_'+bin+'bins_SoverB.pdf')

canvas_SoverB.SaveAs(outpath+'bdt_'+bin+'bins_SoverB.png')
