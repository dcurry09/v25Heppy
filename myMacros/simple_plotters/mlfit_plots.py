

from ROOT import *
import sys

gStyle.SetOptStat(0)

ifile = TFile(sys.argv[1])
channel = sys.argv[2] 
sample = sys.argv[3]

print ifile, channel, sample


# For Zll this is ../limits/mlfit.root ch1_Zmm_TT_low TT

print 'File directory:', "shapes_prefit/%s/%s" % (channel,sample)

h_pre = ifile.Get("shapes_prefit/%s/%s" % (channel,sample))
h_post = ifile.Get("shapes_fit_b/%s/%s" % (channel,sample))

print 'prefit:', h_pre

h_pre.SetLineColor(ROOT.kBlue)
h_post.SetLineColor(ROOT.kRed)

canv = TCanvas("canv","canv")

h_pre.SetMaximum(1.2*max(h_pre.GetMaximum(),h_post.GetMaximum()))

h_pre.Draw("ep")
h_post.Draw("ep same")
h_pre.Draw("hist same")
h_post.Draw("hist same")

leg = TLegend(0.1,0.7,0.3,0.9)
leg.AddEntry(h_pre,"%s %s prefit" % (channel, sample))
leg.AddEntry(h_post,"%s %s postfit" % (channel, sample))
leg.Draw("same")

print "prefit Integral = ",h_pre.Integral()
print "postfit Integral = ",h_post.Integral()
print "Ratio = ",(h_post.Integral()/h_pre.Integral())

raw_input()
canv.SaveAs("%s_%s.pdf" % (channel, sample))
canv.SaveAs("%s_%s.png" % (channel, sample))
