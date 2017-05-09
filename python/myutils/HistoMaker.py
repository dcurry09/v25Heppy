import sys,os
import pickle
import ROOT 
from array import array
from printcolor import printc
from BetterConfigParser import BetterConfigParser
from TreeCache import TreeCache
from math import sqrt
from copy import copy
import numpy as np
#from array import *
import array as ar
#from builtins import any as b_any

class HistoMaker:
    def __init__(self, samples, path, config, optionsList,GroupDict=None):
        self.path = path
        self.config = config
        self.optionsList = optionsList
        self.nBins = optionsList[0]['nBins']
        self.lumi=0.
        self.cuts = []
        self.weight = []
        self.sys_cuts = []

        for options in optionsList:
            self.cuts.append(options['cut'])
            self.weight.append(options['weight'])
            #self.sys_cuts.append(options['sys_cut'])
            
        print '  with Cuts  : ', self.cuts[0]
        print '  and Weights: ', self.weight[0]

        self.tc = TreeCache(self.cuts, samples, path, config)

        self._rebin = False
        self.mybinning = None
        self.GroupDict=GroupDict
        self.calc_rebin_flag = False
        VHbbNameSpace=config.get('VHbbNameSpace','library')
        ROOT.gSystem.Load(VHbbNameSpace)
        
        

    def get_histos_from_tree(self,job,cutOverWrite=None):

        #if self.lumi == 0: 
        #    raise Exception("You're trying to plot with no lumi")
         
        hTreeList=[]
        
        #get the conversion rate in case of BDT plots
        TrainFlag = eval(self.config.get('Analysis','TrainFlag'))
        if TrainFlag:
            BDT_test_cut = 'evt%2!=0'
            #print '\n======== Filling Datacard with BDT Test Events =========='
        else: 
            BDT_test_cut = 'evt%2==0'
            #print '\n======== Filling Datacard with BDT Train Events =========='

        plot_path   = self.config.get('Directories','plotpath')
        addOverFlow = eval(self.config.get('Plot_general','addOverFlow'))
        
        # Get the tree for this sample(not actually cut yet)
        CuttedTree = self.tc.get_tree(job,'1')
        
        # Get the lumiweighted cross section and genWeight from the tree
        if job.type != 'DATA':
            xSec = self.tc.get_scale(job, self.config)
            
            '''
            # FOr temp DY special weights
            if 'Vpt100to250' in job.name:
                 xSec = xSec*(1.0-0.66)
            if 'Vpt250to400' in job.name:
                xSec = xSec*(1.0-0.85)
            if 'Vpt400to650' in job.name:
                xSec =xSec*(1.0-0.98)
            if 'Vpt650toInf' in job.name:
                xSec =xSec*(1.0-1.0)
            '''    
            
            
        if job.type == 'DATA':
            xSec = 1
            
        #print '-----> Job Name, Type: ', job.name, job.type
        #print '       xSec: ', xSec
        #print '       Tree: ', CuttedTree
        #print '    Entries: ', CuttedTree.GetEntries()
        #print '    treeCut: ', options['cut']
        
        eval(self.config.get('Analysis','TrainFlag'))                        
        for options in self.optionsList:
            
            name = job.name
            
            if self.GroupDict is None:
                group=job.group
            else:
                group=self.GroupDict[job.name]
                
                    
            treeVar = options['var']
            name    = options['name']
            #print 'Options:', options
            #print 'Type: ', job.type
            #print 'Name: ', name
            
            if self._rebin or self.calc_rebin_flag:
                nBins = self.nBins
            else:
                nBins = int(options['nBins'])

            xMin = float(options['xMin'])
            xMax = float(options['xMax'])

            if cutOverWrite:
                treeCut=cutOverWrite
            else:
                treeCut='%s'%(options['cut'])
                
            # Add the JEC/JER sys cuts by hand
            if 'gg_plus_' in treeVar or 'VV' in treeVar:
                if '_up' in treeVar or '_down' in treeVar:
                    if options['sys_cut']:
                        treeCut='%s'%(options['sys_cut'])
                        print treeVar
                        print '\n\t!!!! JER/JEC Tree SYS Cut:', treeCut

            if 'minCMVA' in treeVar:
                if options['sys_cut']:
                     treeCut='%s'%(options['sys_cut'])
                     print treeVar
                     print '\n\t!!!! JER/JEC Tree SYS Cut:', treeCut


            weightF = '%s'%(options['weight'])    
            
            ##############################
            #Add any special weights here
            if 'Zudsg' in job.name or 'Zcc' in job.name or 'Z1b' in job.name or 'Z2b' in job.name:
                weightF = weightF+'*VHbb::LOtoNLOWeightBjetSplitEtabb(abs(Jet_eta[hJCidx[0]]-Jet_eta[hJCidx[1]]),Sum$(GenJet_pt>20 && abs(GenJet_eta)<2.4 && GenJet_numBHadrons))'
                weightF = weightF+'*VHbb::ptWeightEWK_Zll(nGenVbosons[0], GenVbosons_pt[0], VtypeSim, nGenTop, nGenHiggsBoson)'
                weightF = weightF+'*('+job.specialweight+')'
            if '2L2Q' in job.name:
                print '\n\t----> Adding ZZ_2L2Q special weights...'
                weightF = weightF+'*('+job.specialweight+')'
            if 'ttbar' in job.name:
                weightF = weightF+'*VHbb::ttbar_reweight(GenTop_pt[0],GenTop_pt[1],nGenTop)'
            #if 'ZH' in job.name and not 'ggZH' in job.name:
                #weightF = weightF+'*VHbb::ptWeightEWK_Zll_v25(nGenVbosons[0], GenVbosons_pt[0], VtypeSim)'

            ### For temp Inclusive testing ###
            if 'Zudsg' == job.name or 'Z1b' == job.name or 'Z2b' == job.name:
                print '\n\t----> Adding Inclusive lheHT cut...'
                treeCut = treeCut+' & lheHT < 100'
                
            # For high/low SF
            if str(self.config.get('Plot_general', 'doSF')) == 'True':
                                              
                if 'V_new_pt >= 50' in treeCut:
                    print '\n\t !!! Adding RateParam !!!'
                    if 'Zudsg' in job.name or 'Zcc' in job.name: weightF = weightF+'*(1.01)'
                    if 'Z1b' in job.name: weightF = weightF+'*(0.89)'
                    if 'Z2b' in job.name: weightF = weightF+'*(1.10)'
                    if 'ttbar' in job.name: weightF = weightF+'*(1.0065)'
                    
                if 'V_new_pt >= 150' in treeCut:
                    print '\n\t !!! Adding RateParam !!!'
                    if 'Zudsg' in job.name or 'Zcc' in job.name: weightF = weightF+'*(1.04)'
                    if 'Z1b' in job.name: weightF = weightF+'*(0.59)'
                    if 'Z2b' in job.name: weightF = weightF+'*(1.437)'
                    if 'ttbar' in job.name: weightF = weightF+'*(1.0309)'

                        
            print '\n-----> Making histograms for variable:', treeVar
            print 'Job.name:', job.name
            print 'weightF:', weightF
            print 'nBins:', nBins, xMin, xMax
            

            if job.type != 'DATA':
                
                if CuttedTree.GetEntries():
                    
                    #if 'trainBDT' in treevar:
                    #    drawoption = '(%s)*(%s & %s)'%(weightF,treeCut,BDT_train_cut)
                    
                    if 'gg_plus' in treeVar or 'VV' in treeVar:
                        print '\n----> Filling Histogram with BDT Test Events Only...'
                        drawoption = '(sign(genWeight))*(%s)*(%s & %s)'%(weightF, treeCut, BDT_test_cut)
                        
                    elif 'vtx' in treeVar or 'EmEF' in treeVar or '_lepton' in treeVar:
                        drawoption = '(sign(genWeight))*(%s)*(%s)' % (weightF,treeCut+' && '+treeVar+' > 0')
                        '''    
                        elif 'minCSV' in treeVar:
                        if 'Zudsg' in job.name or 'Zcc' in job.name: 
                        xMin = 0.0
                            xMax = 0.55
                        if 'Z1b' in job.name or 'Z2b' in job.name or 'ttbar' in job.name:
                            xMin = 0.4
                            xMax = 1.0
                            drawoption = '(sign(genWeight))*(%s)*(%s)' % (weightF,treeCut)
                            '''        
                    else: 
                        #drawoption = '(sign(genWeight))*(%s)*(%s)*(%s)' % (weightF,treeCut,xSec)
                        drawoption = '(sign(genWeight))*(%s)*(%s)' % (weightF,treeCut)
                      
                    print 'Draw Option:',drawoption

                    CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job.name,nBins,xMin,xMax), drawoption, "goff,e")
                    

                    full = True

                else:
                    full=False

            elif job.type == 'DATA':

                print '\n----> Job Type: Data...'
                print '            Name: ', job.name
                
                print '\n---->Drawing Tree for variable: ',treeVar
                print '  with Cuts: ', treeCut
                
   
                if 'gg_plus' in treeVar or 'VV' in treeVar:
                    if options['blind']:
                        #treeCut = treeCut + ' & '+treeVar+'<0.3'
                        
                        print '\n\n====== BLINDED ======'
                        print treeCut
                   
                        CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job.name,nBins,xMin,xMax), '%s' %treeCut, "goff,e")
                    else:
                        CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job.name,nBins,xMin,xMax), '%s' %treeCut, "goff,e")

                        
                elif '_corr' in treeVar:
                    print 'VAR:',treeVar
                    if '[0]' in treeVar:
                        new_treeVar = 'Jet_pt[hJCidx[0]]/Jet_rawPt[hJCidx[0]]'
                    if '[1]' in treeVar:
                        new_treeVar = 'Jet_pt[hJCidx[1]]/Jet_rawPt[hJCidx[1]]'
                    CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(new_treeVar,job.name,nBins,xMin,xMax), '%s' %treeCut, "goff,e")
                    

                elif 'vtx' in treeVar or 'EmEF' in treeVar or '_lepton' in treeVar:
                    CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job.name,nBins,xMin,xMax), '%s' %treeCut+' && '+treeVar+' > 0', "goff,e")
                    
                    
                #else:
                #    if options['blind']:
                #        print '!!!!BLINDING!!!'
                #        CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job.name,nBins,xMin,xMax), '%s & V_pt < 50.' %treeCut, "goff,e")

                elif 'LHE' in treeVar or 'HT' in treeVar or 'lhe' in treeVar:
                    CuttedTree.Draw('%s>>%s(%s,%s,%s)' %('Jet_pt[hJCidx[1]]',job.name,nBins,xMin,xMax), '%s' %treeCut+' && Jet_pt[hJCidx[1]] < 0.0', "goff,e")
                    
                    
                else:
                    print '!!!!NOT BLINDING!!!'
                    CuttedTree.Draw('%s>>%s(%s,%s,%s)' %(treeVar,job.name,nBins,xMin,xMax), '%s' %treeCut, "goff,e")
                    


                print CuttedTree
                
                '''
                hReg_metric = hReg.GetRMS()/hReg.GetMean()
                hNom_metric = hNom.GetRMS()/hNom.GetMean()
                percent_improvement = (1-(hReg_metric/hNom_metric))*100
                hReg_std = str(round(hReg.GetRMS(),3))
                hReg_mu  = str(round(hReg.GetMean(),3))
                hNom_std = str(round(hNom.GetRMS(),3))
                hNom_mu  = str(round(hNom.GetMean(),3))
                '''

                full = True

            if full:
                hTree = ROOT.gDirectory.Get(job.name)
                print '\nJob name: ',job.name
                print 'hTree: ', hTree
                
                # Get Stats
                #hTree.GetRMS()
                #hTree.GetMean()
                #print '\t Mean: ', hTree.GetMean()
                #print '\t RMS : ', hTree.GetRMS()
                

            else:
                hTree = ROOT.TH1F('%s'%name,'%s'%name,nBins,xMin,xMax)
                hTree.Sumw2()
                
            # NOW scale the histograms    
            if job.type != 'DATA':

                if 'gg_plus' in treeVar or 'VV' in treeVar:
                    if TrainFlag:
                        MC_rescale_factor=2.
                        print 'I RESCALE BY 2.0'
                    else: 
                        MC_rescale_factor = 1.
    
                    ScaleFactor = self.tc.get_scale(job, self.config)*MC_rescale_factor

                    # for LHE scale shapes we need a different norm
                    if 'LHE_weights_scale_wgt[0]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 0)*MC_rescale_factor
                    elif 'LHE_weights_scale_wgt[1]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 1)*MC_rescale_factor
                    elif 'LHE_weights_scale_wgt[2]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 2)*MC_rescale_factor
                    elif 'LHE_weights_scale_wgt[3]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 3)*MC_rescale_factor
                    
                    print '\n-----> Histogram Scale Factor: ', ScaleFactor
                else: 
                    ScaleFactor = self.tc.get_scale(job, self.config)
                    
                    # for LHE scale shapes we need a different norm
                    if 'LHE_weights_scale_wgt[0]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 0)
                    elif 'LHE_weights_scale_wgt[1]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 1)
                    elif 'LHE_weights_scale_wgt[2]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 2)
                    elif 'LHE_weights_scale_wgt[3]' in weightF:
                        ScaleFactor = self.tc.get_scale_LHEscale(job, self.config, 3)
                    
                    print '\n-----> Histogram Scale Factor: ', ScaleFactor
                
                if ScaleFactor != 0:
                    hTree.Scale(ScaleFactor)

     
            #print '\t-->import %s\t Integral: %s'%(job.name,hTree.Integral())
            if addOverFlow:
            	uFlow = hTree.GetBinContent(0)+hTree.GetBinContent(1)
            	oFlow = hTree.GetBinContent(hTree.GetNbinsX()+1)+hTree.GetBinContent(hTree.GetNbinsX())
            	uFlowErr = ROOT.TMath.Sqrt(ROOT.TMath.Power(hTree.GetBinError(0),2)+ROOT.TMath.Power(hTree.GetBinError(1),2))
            	oFlowErr = ROOT.TMath.Sqrt(ROOT.TMath.Power(hTree.GetBinError(hTree.GetNbinsX()),2)+ROOT.TMath.Power(hTree.GetBinError(hTree.GetNbinsX()+1),2))
            	hTree.SetBinContent(1,uFlow)
            	hTree.SetBinContent(hTree.GetNbinsX(),oFlow)
            	hTree.SetBinError(1,uFlowErr)
            	hTree.SetBinError(hTree.GetNbinsX(),oFlowErr)

            hTree.SetDirectory(0)
            gDict = {}

            if self._rebin:
                gDict[group] = self.mybinning.rebin(hTree)
                del hTree
            else: 
                #print 'not rebinning %s'%job.name 
                gDict[group] = hTree

            hTreeList.append(gDict)

        CuttedTree.IsA().Destructor(CuttedTree)
        del CuttedTree
        return hTreeList


       
    @property
    def rebin(self):
        return self._rebin

    @property
    def rebin(self, value):
        if self._rebin and value:
            return True
        elif self._rebin and not value:
            self.nBins = self.norebin_nBins
            self._rebin = False
        elif not self._rebin and value:
            if self.mybinning is None:
                raise Exception('define rebinning first')
            else:
                self.nBins = self.rebin_nBins
                self._rebin = True
                return True
        elif not self._rebin and not self.value:
            return False

    def calc_rebin(self, bg_list, nBins_start=1000, tolerance=0.35):
        self.calc_rebin_flag = True
        self.norebin_nBins = copy(self.nBins)
        self.rebin_nBins = nBins_start
        self.nBins = nBins_start
        i=0

        #add all together:
        print '\n\t...calculating rebinning on list:', bg_list
        
        for job in bg_list:

            #print 'Rebinner BKG_sample:', job.name

            htree = self.get_histos_from_tree(job)[0].values()[0]
            #print 'Rebinner htree:', htree
            
            if not i:
                totalBG = copy(htree)
            else:
                totalBG.Add(htree,1)
            del htree
            i+=1

        ErrorR=0
        ErrorL=0
        TotR=0
        TotL=0
        binR=self.rebin_nBins
        binL=1
        rel=1.0

        #---- from right
        while rel > tolerance:
            TotR+=totalBG.GetBinContent(binR)
            ErrorR=sqrt(ErrorR**2+totalBG.GetBinError(binR)**2)
            binR-=1
            if binR < 0: break
            if TotR < 1.: continue
            if not TotR <= 0 and not ErrorR == 0:
                rel=ErrorR/TotR
                #print rel
        #print 'upper bin is %s'%binR

        #---- from left
        rel=1.0
        while rel > tolerance:
            TotL+=totalBG.GetBinContent(binL)
            ErrorL=sqrt(ErrorL**2+totalBG.GetBinError(binL)**2)
            binL+=1
            if binL > nBins_start: break
            if TotL < 1.: continue
            if not TotL <= 0 and not ErrorL == 0:
                rel=ErrorL/TotL
                #print rel
        #it's the lower edge
        binL+=1
        #print 'lower bin is %s'%binL

        inbetween=binR-binL
        stepsize=int(inbetween)/(int(self.norebin_nBins)-2)
        modulo = int(inbetween)%(int(self.norebin_nBins)-2)

        #print 'stepsize %s'% stepsize
        #print 'modulo %s'%modulo
        binlist=[binL]
        for i in range(0,int(self.norebin_nBins)-3):
            binlist.append(binlist[-1]+stepsize)
        binlist[-1]+=modulo
        binlist.append(binR)
        binlist.append(self.rebin_nBins+1)
       # print 'binning set to %s'%binlist
        self.mybinning = Rebinner(int(self.norebin_nBins),array('d',[-1.0]+[totalBG.GetBinLowEdge(i) for i in binlist]),True)
        self._rebin = True
        print '\t > rebinning is set <\n'

    @staticmethod
    def orderandadd(histo_dicts,setup):
        ordered_histo_dict = {}
        for sample in setup:
            nSample = 0
            for histo_dict in histo_dicts:
                if histo_dict.has_key(sample):
                    if nSample == 0:
                        ordered_histo_dict[sample] = histo_dict[sample].Clone()
                    else:
                        #printc('magenta','','\t--> added %s to %s'%(sample,sample))
                        ordered_histo_dict[sample].Add(histo_dict[sample])
                    nSample += 1
        del histo_dicts
        return ordered_histo_dict 

    



class Rebinner:
    def __init__(self,nBins,lowedgearray,active=True):
        self.lowedgearray=lowedgearray
        self.nBins=nBins
        self.active=active
    def rebin(self, histo):
        if not self.active: return histo
        #print histo.Integral()
        print '!!!!! Rebinning FInal Step !!!!!'
        ROOT.gDirectory.Delete('hnew')
        histo.Rebin(self.nBins,'hnew',self.lowedgearray)
        binhisto=ROOT.gDirectory.Get('hnew')
        #print binhisto.Integral()
        newhisto=ROOT.TH1F('new','new',self.nBins,self.lowedgearray[0],self.lowedgearray[-1])
        newhisto.Sumw2()
        for bin in range(1,self.nBins+1):
            newhisto.SetBinContent(bin,binhisto.GetBinContent(bin))
            newhisto.SetBinError(bin,binhisto.GetBinError(bin))
        newhisto.SetName(binhisto.GetName())
        newhisto.SetTitle(binhisto.GetTitle())
        print newhisto.Integral()
        del histo
        del binhisto
        return copy(newhisto)
