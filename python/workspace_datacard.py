#!/usr/bin/env python
import os, sys, ROOT, warnings, pickle
ROOT.gROOT.SetBatch(True)
from array import array
from math import sqrt
from copy import copy, deepcopy
#suppres the EvalInstace conversion warning bug
warnings.filterwarnings( action='ignore', category=RuntimeWarning, message='creating converter.*' )
from optparse import OptionParser
from myutils import BetterConfigParser, Sample, progbar, printc, ParseInfo, Rebinner, HistoMaker

btag = 'CSV'
#batg = 'CMVAV2'

def useSpacesInDC(fileName):
    file_ = open(fileName,"r+")

    old = file_.read()
    ## get the maximum width of each colum (excluding the first lines)
    lineN = 0
    maxColumnWidth = [0]
    for line in old.split('\n'):
        lineN += 1
        if lineN<10: continue #skip the first 10 lines
        words = line.split('\t')
        for i in range(len(words)):
            if i>=len(maxColumnWidth): maxColumnWidth.append(0)
            if len(words[i])>maxColumnWidth[i]: maxColumnWidth[i]=len(words[i])
    ## replace the tabs with the new formatting (excluding the first lines)
    #newfile = open("newFile.txt","w+")
    lineN = 0
    file_.seek(0)
    for line in old.split('\n'):
        lineN += 1
        if lineN<10: #in the first 10 lines just replace '\t' with ' '
            file_.write(line.replace('\t',' ')+'\n')
            continue
        words = line.split('\t')
        newLine=""
        for i in range(len(words)): #use the new format!
            newLine += words[i].ljust(maxColumnWidth[i]+1)
        file_.write(newLine+'\n')
    file_.close()
    return



#--CONFIGURE---------------------------------------------------------------------
argv = sys.argv
parser = OptionParser()
parser.add_option("-V", "--variable", dest="variable", default="",
                      help="variable for shape analysis")
parser.add_option("-C", "--config", dest="config", default=[], action="append",
                      help="configuration file")
(opts, args) = parser.parse_args(argv)
config = BetterConfigParser()
config.read(opts.config)
var=opts.variable
#-------------------------------------------------------------------------------

# Add external macros
#ROOT.gSystem.CompileMacro("../plugins/PU.C")

#--read variables from config---------------------------------------------------
# 7 or 8TeV Analysis
anaTag = config.get("Analysis","tag")

# Directories:
Wdir=config.get('Directories','Wdir')
vhbbpath=config.get('Directories','vhbbpath')
samplesinfo=config.get('Directories','samplesinfo')
path = config.get('Directories','dcSamples')
outpath=config.get('Directories','limits')
try:
    os.stat(outpath)
except:
    os.mkdir(outpath)

# parse histogram config:
treevar = config.get('dc:%s'%var,'var')
name = config.get('dc:%s'%var,'wsVarName')
title = name

#print config.get('dc:%s'%var,'range')
nBins       = int(config.get('dc:%s'%var,'range').split(',')[0])
xMin        = float(config.get('dc:%s'%var,'range').split(',')[1])
xMax        = float(config.get('dc:%s'%var,'range').split(',')[2])
ROOToutname = config.get('dc:%s'%var,'dcName')
RCut        = config.get('dc:%s'%var,'cut')
signals     = config.get('dc:%s'%var,'signal').split(' ')
datas       = config.get('dc:%s'%var,'data')
Datacardbin = config.get('dc:%s'%var,'dcBin')
anType      = config.get('dc:%s'%var,'type')
setup       = eval(config.get('LimitGeneral','setup'))
doSYS       = config.get('dc:%s'%var,'doSYS')
doBin       = config.get('dc:%s'%var,'doBin')

# CHange setup for VV analysis
if 'VV' in anType:
    setup = ['VVHF', 'VVLF', 'ZH', 'ggZH', 'DYlight','DY1b', 'DY2b', 'TT', 'ST']

#Systematics:
if config.has_option('LimitGeneral','addSample_sys'):
    addSample_sys = eval(config.get('LimitGeneral','addSample_sys'))
    additionals = [addSample_sys[key] for key in addSample_sys]
else:
    addSample_sys = None
    additionals = []

#find out if BDT or MJJ:
bdt = False
mjj = False
cr = False

if 'BDT' in str(anType):
    bdt = True
    systematics = eval(config.get('LimitGeneral','sys_BDT'))
elif str(anType) == 'Mjj':
    mjj = True
    systematics = eval(config.get('LimitGeneral','sys_Mjj'))
elif 'cr' in str(anType):
    cr = True
    systematics = eval(config.get('LimitGeneral','sys_BDT'))
else:
    bdt = True
    systematics = eval(config.get('LimitGeneral','sys_BDT'))

print '\nSystematics:', systematics

# Turn off Systematics if selected
#print 'doSYS:', doSYS
#if doSYS == 'False':
#    print '!!Turning off SYS!!'
#    systematics = []
    

sys_cut_suffix=eval(config.get('LimitGeneral','sys_cut_suffix'))
sys_cut_include=[]
if config.has_option('LimitGeneral','sys_cut_include'):
    sys_cut_include=eval(config.get('LimitGeneral','sys_cut_include'))


#systematicsnaming = eval(config.get('LimitGeneral','systematicsnaming'))

if 'high' in ROOToutname or 'HighPt' in ROOToutname:
    systematicsnaming = eval(config.get('LimitGeneral','systematicsnaming_high'))
elif 'med' in ROOToutname or 'MedPt' in ROOToutname:
    systematicsnaming = eval(config.get('LimitGeneral','systematicsnaming_med'))
elif 'low' in ROOToutname or 'LowPt' in ROOToutname:
    systematicsnaming = eval(config.get('LimitGeneral','systematicsnaming_low'))
else:
    systematicsnaming = eval(config.get('LimitGeneral','systematicsnaming'))

print '\nSystematicsnaming:', systematicsnaming

sys_factor_dict = eval(config.get('LimitGeneral','sys_factor'))
sys_affecting = eval(config.get('LimitGeneral','sys_affecting'))

# weightF:
weightF = config.get('Weights','weightF')

if doSYS == 'False':
    weightF_systematics = []
else:
    weightF_systematics = eval(config.get('LimitGeneral','weightF_sys'))

# rescale stat shapes by sqrtN
rescaleSqrtN=eval(config.get('LimitGeneral','rescaleSqrtN'))

# get nominal cutstring:
#treecut = config.get('Cuts',RCut) + ' & '+ bdt_name +' > ' + bdt_split
treecut = config.get('Cuts',RCut)
print '\n\n\t\t TreeCut: ', treecut


# Train flag: splitting of samples
TrainFlag = eval(config.get('Analysis','TrainFlag'))

# toy data option:
toy=eval(config.get('LimitGeneral','toy'))

# blind data option:
blind=eval(config.get('LimitGeneral','blind'))
blind = False

# additional blinding cut:
addBlindingCut = None
if config.has_option('LimitGeneral','addBlindingCut'):
    addBlindingCut = config.get('LimitGeneral','addBlindingCut')
    print '\n\t-----> adding add. blinding cut...'

#change nominal shapes by syst
change_shapes = None
if config.has_option('LimitGeneral','change_shapes'):
    change_shapes = eval(config.get('LimitGeneral','change_shapes'))
    print '\n\t-----> changing the shapes...'

#on control region cr never blind. Overwrite whatever is in the config
if 'cr' in str(anType):
    if blind:
        print '@WARNING: Changing blind to false since you are running for control region.'
    blind = False
if blind: 
    printc('red','', 'I AM BLINDED!')    

#get List of backgrounds in use:
backgrounds = eval(config.get('LimitGeneral','BKG'))

if 'VV' in str(anType):
    #treevar == 'VV_bdt.nominal':
    backgrounds = eval(config.get('LimitGeneral','VV_BKG'))

#Groups for adding samples together
GroupDict = eval(config.get('LimitGeneral','Group'))

#naming for DC
Dict= eval(config.get('LimitGeneral','Dict'))

#treating statistics bin-by-bin:
binstat = eval(config.get('LimitGeneral','binstat'))

print '\treevar::', treevar

# Use the rebinning:
rebin_active=eval(config.get('LimitGeneral','rebin_active'))
#rebin_active = False

if 'Jet' in treevar:
   if rebin_active:
        print '@WARNING: Changing rebin_active to false since you are running for control region.'
   rebin_active = False

# ignore stat shapes
ignore_stats = eval(config.get('LimitGeneral','ignore_stats'))

#max_rel = float(config.get('LimitGeneral','rebin_max_rel'))
signal_inject=config.get('LimitGeneral','signal_inject')

# add signal as background
add_signal_as_bkg=config.get('LimitGeneral','add_signal_as_bkg')
if not add_signal_as_bkg == 'None':
    setup.append(add_signal_as_bkg)
#----------------------------------------------------------------------------

#--Setup--------------------------------------------------------------------
#Assign Pt region for sys factors
if 'HighPtLooseBTag' in ROOToutname:
    pt_region = 'HighPtLooseBTag'
elif 'high' in ROOToutname or 'HighPt' in ROOToutname:
    pt_region = 'HighPt'
elif 'med' in ROOToutname or 'MedPt' in ROOToutname:
    pt_region = 'MedPt'
elif 'low' in ROOToutname or 'LowPt' in ROOToutname:
    pt_region = 'LowPt'
elif 'ATLAS' in ROOToutname:
    pt_region = 'HighPt'
elif 'MJJ' in ROOToutname:
    pt_region = 'HighPt' 
else:
    print "Unknown Pt region"
    pt_region = 'AllPt'
    #sys.exit()
    

# Set rescale factor of 2 in case of TrainFlag
if TrainFlag:
    MC_rescale_factor=1.
    #print 'I RESCALE BY 2.0'
else: MC_rescale_factor = 1.

#systematics up/down

if doSYS == 'False':
    UD = []
else:
    UD = ['Up','Down']

#Parse samples configuration
info = ParseInfo(samplesinfo,path)

# get all the treeCut sets
all_samples        = info.get_samples(signals+backgrounds+additionals)
signal_samples     = info.get_samples(signals) 
background_samples = info.get_samples(backgrounds) 
data_sample_names  = config.get('dc:%s'%var,'data').split(' ')
data_samples       = info.get_samples(data_sample_names)

print '\n-----> Collecting all Samples...'
print '         Signals     : ', signals
print '         Backgrounds : ', backgrounds
print '         Data        : ', data_sample_names


#-------------------------------------------------------------------------------------------------

optionsList=[]

def appendList(): optionsList.append({'cut':copy(_cut),'var':copy(_treevar),'name':copy(_name),'nBins':nBins,'xMin':xMin,'xMax':xMax,'weight':copy(_weight),'blind':blind,'sys_cut':copy(_sys_cut)})

#nominal
_cut = treecut
_treevar = treevar
_name = title
_weight = weightF

#new
_sys_cut = treecut
appendList()


#the 4 sys
#for syst in ['JER', 'JEC']:

print '\n\t-----> Adding New Systematic Cuts....'

for syst in systematics:
    for Q in UD:

        print '\n\t-----> Systematic: ', syst+Q

        #default:
        _cut = treecut
        _name = title
        _weight = weightF
        _treevar = treevar
        
        # new
        _sys_cut = treecut

        # Lepton Efficiency
        if '_eff_' in syst:
            _weight = _weight.replace('eId90SFWeight', 'eId90SFWeight'+Q)
            _weight = _weight.replace('eTrigSFWeight_ele27', 'eTrigSFWeight_ele27'+Q)
            _weight = _weight.replace('mIsoSFWeight', 'mIsoSFWeight'+Q)
            _weight = _weight.replace('vLeptons_SF_IdCutLoose[0]*vLeptons_SF_IdCutLoose[1]', 'mIdSFWeight'+Q+'[0]')
            _weight = _weight.replace('mTrigSFWeight_ICHEP', 'mTrigSFWeight'+Q)
        
        # Pu weight
        if 'weight_pileUp' in syst:
            _weight = weightF.replace('puWeight', 'puWeight%s' % Q)

        # LHE Scale Variations(muF, muR)
        if 'CMS_vhbb_LHE_weights_scaleMuF' in syst:
            if Q is 'Up':
                _weight = _weight + '*(LHE_weights_scale_wgt[0])'
            if Q is 'Down':
                _weight = _weight + '*(LHE_weights_scale_wgt[1])'    
        if 'CMS_vhbb_LHE_weights_scaleMuR' in syst:
            if Q is 'Up':
                _weight = _weight + '*(LHE_weights_scale_wgt[2])'
            if Q is 'Down':
                _weight = _weight + '*(LHE_weights_scale_wgt[3])'
                    
        #if 'btag' in syst:
        #    sys_temp = syst.replace('btagWeightCSV', 'btagWeightCSV_%s'%(Q.lower()))
        #    _weight = _weight.replace('*btagWeightCSV', '*%s'%(sys_temp))            
                
        # for NEW 2016 weights
        # if 'JER' not in syst and 'JEC' not in syst and syst != 'weight_pileUp' and '_eff_' not in syst:

        if 'btag' in syst:    
            if '_lf_' in syst:
                if 'LowCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_LFLowCentral%s'%(Q))
                if 'HighCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_LFHighCentral%s'%(Q))
                if 'LowForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_LFLowForward%s'%(Q))
                if 'HighForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_LFHighForward%s'%(Q))

            if '_hf_' in syst:
                if 'LowCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_HFLowCentral%s'%(Q))
                if 'HighCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_HFHighCentral%s'%(Q))
                if 'LowForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_HFLowForward%s'%(Q))
                if 'HighForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_HFHighForward%s'%(Q))
        
            if 'lfstats1' in syst:
                if 'LowCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_LFStats1LowCentral%s'%(Q))
                if 'HighCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_LFStats1HighCentral%s'%(Q))
                if 'LowForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_LFStats1LowForward%s'%(Q))
                if 'HighForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_LFStats1HighForward%s'%(Q))

            if 'hfstats1' in syst:
                if 'LowCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_HFStats1LowCentral%s'%(Q))
                if 'HighCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_HFStats1HighCentral%s'%(Q))
                if 'LowForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_HFStats1LowForward%s'%(Q))
                if 'HighForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_HFStats1HighForward%s'%(Q))
    
            if 'lfstats2' in syst:
                if 'LowCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_LFStats2LowCentral%s'%(Q))
                if 'HighCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_LFStats2HighCentral%s'%(Q))
                if 'LowForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_LFStats2LowForward%s'%(Q))
                if 'HighForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_LFStats2HighForward%s'%(Q))

            if 'hfstats2' in syst:
                if 'LowCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_HFStats2LowCentral%s'%(Q))
                if 'HighCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_HFStats2HighCentral%s'%(Q))
                if 'LowForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_HFStats2LowForward%s'%(Q))
                if 'HighForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_HFStats2HighForward%s'%(Q))
            
            if 'cferr1' in syst:
                if 'LowCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_cErr1LowCentral%s'%(Q))
                if 'HighCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_cErr1HighCentral%s'%(Q))
                if 'LowForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_cErr1LowForward%s'%(Q))
                if 'HighForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_cErr1HighForward%s'%(Q))

            if 'cferr2' in syst:
                if 'LowCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_cErr2LowCentral%s'%(Q))
                if 'HighCentral' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_cErr2HighCentral%s'%(Q))
                if 'LowForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_cErr2LowForward%s'%(Q))
                if 'HighForward' in syst:
                    _weight   = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_cErr2HighForward%s'%(Q))


        '''            
        if 'JEC' in syst:    
                
            if 'low' in syst:
                _weight = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_JEC%s_low'%(Q))
            if 'high' in syst:
                _weight = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_JEC%s_high'%(Q))
            if 'central' in syst:
                _weight = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_JEC%s_central'%(Q))
            if 'forward' in syst:
                _weight = _weight.replace('*bTagWeightCSV_Moriond', '*bTagWeightCSV_Moriond_JEC%s_forward'%(Q))
        '''
        
        if 'JER' in syst or 'JEC' in syst:
            if 'JEC' in syst: syst = syst.replace('JEC_', '')
            #print 'New JEC SYST:', syst
            if bdt == True:
                _treevar = treevar.replace('.nominal','.%s_%s'%(syst,Q.lower()))

                # Set the new string cut for JEC/JER mass and jet values.  Loop over JEC sys list and create string cut.
                JECsys = {"JER",
                          "PileUp",
                          "Relative",
                          "AbsoluteMisc"}
                new_Hcut90  = 'HCMVAV2_reg_mass>90.'
                new_Hcut150 = 'HCMVAV2_reg_mass<150.'
                new_Jcut    = '(Jet_pt_reg[hJCMVAV2idx[0]]>20.&Jet_pt_reg[hJCMVAV2idx[1]]>20.)'
                for sys in JECsys:
                    new_Hcut150 = new_Hcut150+'||HCMVAV2_reg_mass_corr'+sys+Q+'<150'
                    new_Hcut90  = new_Hcut90+'||HCMVAV2_reg_mass_corr'+sys+Q+'>90'
                    new_Jcut    = new_Jcut+'||(hJetCMVAV2_pt_reg'+sys+Q+'[0]>20 && hJetCMVAV2_pt_reg'+sys+Q+'[1]>20)'
                print '\n New Hcut', new_Hcut150
        

                if 'VV' not in anType:
                    _cut = _cut.replace('HCMVAV2_reg_mass < 150.', '('+new_Hcut150+')')
                    _cut = _cut.replace('HCMVAV2_reg_mass > 90.', '('+new_Hcut90+')')
                    _cut = _cut.replace('Jet_pt_reg[hJCMVAV2idx[0]] > 20. & Jet_pt_reg[hJCMVAV2idx[1]] > 20.', '('+new_Jcut+')')

                _sys_cut = _sys_cut.replace('HCMVAV2_reg_mass', 'HCMVAV2_reg_mass_corr%s%s'%(syst,Q))
                _sys_cut = _sys_cut.replace('Jet_pt_reg[hJCMVAV2idx[0]]', 'hJetCMVAV2_pt_reg%s%s[0]'%(syst,Q))
                _sys_cut = _sys_cut.replace('Jet_pt_reg[hJCMVAV2idx[1]]', 'hJetCMVAV2_pt_reg%s%s[1]'%(syst,Q))

                # if 'VV' in anType:
                #     _cut = _cut.replace('HCSV_reg_mass < 160.', '(HCSV_reg_mass<160.||HCSV_reg_corrJERUp_mass_low<160.||HCSV_reg_corrJERDown_mass_low<160.||HCSV_reg_corrJECDown_mass_low<160.||HCSV_reg_corrJECUp_mass_low<160.|| HCSV_reg_corrJERUp_mass_high<160.||HCSV_reg_corrJERDown_mass_high<160.||HCSV_reg_corrJECDown_mass_high<160.||HCSV_reg_corrJECUp_mass_high<160. || HCSV_reg_corrJERUp_mass_central<160.||HCSV_reg_corrJERDown_mass_central<160.||HCSV_reg_corrJECDown_mass_central<160.||HCSV_reg_corrJECUp_mass_central<160. || HCSV_reg_corrJERUp_mass_forward<160.||HCSV_reg_corrJERDown_mass_forward<160.||HCSV_reg_corrJECDown_mass_forward<160.||HCSV_reg_corrJECUp_mass_forward<160.)')

            # Now for CR
            else:
                JECsys = {"JER",
                          "PileUp",
                          "Relative",
                          "AbsoluteMisc"}
                new_Hcut90  = 'HCMVAV2_reg_mass<90.'
                new_Hcut150 = 'HCMVAV2_reg_mass>150.'
                new_Jcut    = '(Jet_pt_reg[hJCMVAV2idx[0]]>20.&Jet_pt_reg[hJCMVAV2idx[1]]>20.)'
                for sys in JECsys:
                    new_Hcut150 = new_Hcut150+'||HCMVAV2_reg_mass_corr'+sys+Q+'>150'
                    new_Hcut90  = new_Hcut90+'||HCMVAV2_reg_mass_corr'+sys+Q+'<90'
                    new_Jcut    = new_Jcut+'||(hJetCMVAV2_pt_reg'+sys+Q+'[0]>20 && hJetCMVAV2_pt_reg'+sys+Q+'[1]>20)'
                print '\n New Jcut', new_Jcut

                if 'VV' not in anType:
                    if 'Zhf' in name: ## (<!ZHbb|H_sel!>_reg_mass < 90. || <!ZHbb|H_sel!>_reg_mass > 150.)
                        _cut = _cut.replace('HCMVAV2_reg_mass > 150.', '('+new_Hcut150+')')
                        _cut = _cut.replace('HCMVAV2_reg_mass < 90.', '('+new_Hcut90+')')
                        _cut = _cut.replace('Jet_pt_reg[hJCMVAV2idx[0]] > 20. & Jet_pt_reg[hJCMVAV2idx[1]] > 20.', '('+new_Jcut+')')
                    else:
                        _cut = _cut.replace('Jet_pt_reg[hJCMVAV2idx[0]] > 20. & Jet_pt_reg[hJCMVAV2idx[1]] > 20.', '('+new_Jcut+')')


                _sys_cut = _sys_cut.replace('HCMVAV2_reg_mass', 'HCMVAV2_reg_mass_corr%s%s'%(syst,Q))
                _sys_cut = _sys_cut.replace('Jet_pt_reg[hJCMVAV2idx[0]]', 'hJetCMVAV2_pt_reg%s%s[0]'%(syst,Q))
                _sys_cut = _sys_cut.replace('Jet_pt_reg[hJCMVAV2idx[1]]', 'hJetCMVAV2_pt_reg%s%s[1]'%(syst,Q))

            
        else:
            _treevar = treevar
        
        print '----> New Weights       :',syst, ' : ', _weight            
        print '--->  New tree variable : ', _treevar
        print '----> New tree cut      : ', _cut
        print '----> New SYS cut      : ', _sys_cut

        
        #append
        appendList()


## This is now incorporated in main SYS loop(line 243)
#UEPS
#for weightF_sys in weightF_systematics:
    #for _weight in [config.get('Weights','%s_UP' %(weightF_sys)),config.get('Weights','%s_DOWN' %(weightF_sys))]:
    #    _sys_cut = _sys_cut
    #    _treevar = treevar
    #    _name = title
    #    appendList()

print optionsList


print '\n-----> Run MC HistoMaker...'
mc_hMaker = HistoMaker(all_samples,path,config,optionsList,GroupDict)

print 'mc_hMaker:', mc_hMaker

print '\n-----> Run Data HistoMaker...'
data_hMaker = HistoMaker(data_samples,path,config,[optionsList[0]])

#Calculate lumi
lumi = 0.
nData = 0
for job in data_samples:
    nData += 1
    lumi += float(job.lumi)

if nData > 1:
    lumi = lumi/float(nData)

mc_hMaker.lumi = lumi
data_hMaker.lumi = lumi

#if addBlindingCut:
#    for i in range(len(mc_hMaker.optionsList)):
#        mc_hMaker.optionsList[i]['cut'] += ' & %s' %addBlindingCut
#    for i in range(len(data_hMaker.optionsList)):
#        data_hMaker.optionsList[i]['cut'] += ' & %s' %addBlindingCut

print 'BKG Samples:', background_samples
if rebin_active:
    mc_hMaker.calc_rebin(background_samples)
    #transfer rebinning info to data maker
    data_hMaker.norebin_nBins = copy(mc_hMaker.norebin_nBins)
    data_hMaker.rebin_nBins = copy(mc_hMaker.rebin_nBins)
    data_hMaker.nBins = copy(mc_hMaker.nBins)
    data_hMaker._rebin = copy(mc_hMaker._rebin)
    data_hMaker.mybinning = deepcopy(mc_hMaker.mybinning)

all_histos = {}
data_histos = {}

print '\n----> Fetching Histograms for samples:', all_samples


for job in all_samples:
    
    print '\n----> job.name:', job.name 

    if not GroupDict[job.name] in sys_cut_include:
        # manual overwrite
        if addBlindingCut:
            all_histos[job.name] = mc_hMaker.get_histos_from_tree(job,treecut+'& %s'%addBlindingCut)
        else:
            all_histos[job.name] = mc_hMaker.get_histos_from_tree(job,treecut)
    else:
        all_histos[job.name] = mc_hMaker.get_histos_from_tree(job)


  
for job in data_samples:
    print '\t-----> Data Histogram: ', job 
    data_histos[job.name] = data_hMaker.get_histos_from_tree(job)[0]['DATA']
    #data_histos[job.name] = data_hMaker.get_histos_from_tree(job)
    
i=0
print 'BKG Samples2:', background_samples
for job in background_samples: 
    print '\nBKG_sample:', job.name
    htree = all_histos[job.name][0].values()[0]

    #if not i: 
    #    hDummy = copy(htree) 
    #else: 
    #    hDummy.Add(htree,1) 
    
    del htree 
    i+=1


'''
if signal_inject:
    print '!!! Signal Inject !!!'
    signal_inject = info.get_samples([signal_inject])
    sig_hMaker = HistoMaker(signal_inject,path,config,optionsList,GroupDict)
    sig_hMaker.lumi = lumi
    if rebin_active:
        sig_hMaker.norebin_nBins = copy(mc_hMaker.norebin_nBins)
        sig_hMaker.rebin_nBins = copy(mc_hMaker.rebin_nBins)
        sig_hMaker.nBins = copy(mc_hMaker.nBins)
        sig_hMaker._rebin = copy(mc_hMaker._rebin)
        sig_hMaker.mybinning = deepcopy(mc_hMaker.mybinning)

for job in signal_inject: 
    htree = sig_hMaker.get_histos_from_tree(job)
    hDummy.Add(htree[0].values()[0],1) 
    del htree 
'''

print '\n\t The Data Histos:', data_histos

nData = 0
for job in data_histos:
    if nData == 0:
        print '----> adding ', job, ' to theData..'
        theData = data_histos[job]
        nData = 1
    else:
        print '----> adding ', job, ' to theData..'
        theData.Add(data_histos[job])
 


#-- Write Files-----------------------------------------------------------------------------------

# generate the TH outfile:
outfile = ROOT.TFile(outpath+'vhbb_TH_'+ROOToutname+'.root', 'RECREATE')
outfile.mkdir(Datacardbin,Datacardbin)
outfile.cd(Datacardbin)

# generate the Workspace:
WS = ROOT.RooWorkspace('%s'%Datacardbin,'%s'%Datacardbin) #Zee
print '\n\n-----> Workspace Initialized....'

disc= ROOT.RooRealVar(name,name,xMin,xMax)
obs = ROOT.RooArgList(disc)
ROOT.gROOT.SetStyle("Plain")

#order and add all together
final_histos = {}
print '\n-----> Ordering and Adding Histos'
print 'all_histos:', all_histos
print 'setup:', setup
print 'all samples:', all_samples
final_histos['nominal'] = HistoMaker.orderandadd([all_histos['%s'%job][0] for job in all_samples],setup) 

print '\n------> Final Histograms: ', final_histos

#SYSTEMATICS:
ind = 1

for syst in systematics:
    print '\n\t-----> Preparing Systematics, Ordering Histograms for : ', syst
    for Q in UD:
        final_histos['%s_%s'%(systematicsnaming[syst],Q)] = HistoMaker.orderandadd([all_histos[job.name][ind] for job in all_samples],setup)
        ind+=1

print '\n------> Final Histograms with SYS: ', final_histos

#for weightF_sys in weightF_systematics: 
#    print '\n\t-----> Preparing Weighted Systematics for: ', weightF_sys
#    for Q in UD:
#        final_histos['%s_%s'%(systematicsnaming[weightF_sys],Q)]= HistoMaker.orderandadd([all_histos[job.name][ind] for job in all_samples],setup)
#        ind+=1


if change_shapes:
    print '\n-----> Changing Histogram Shapes...'
    for key in change_shapes:
        syst,val=change_shapes[key].split('*')
        final_histos[syst][key].Scale(float(val))
        print 'scaled %s times %s val'%(syst,val)


def get_alternate_shape(hNominal,hAlternate):
    hVar = hAlternate.Clone()
    hNom = hNominal.Clone()
    hAlt = hNom.Clone()
    hNom.Add(hVar,-1.)
    hAlt.Add(hNom)
    for bin in range(0,hNominal.GetNbinsX()+1):
        if hAlt.GetBinContent(bin) < 0.: hAlt.SetBinContent(bin,0.)
    return hVar,hAlt

def get_alternate_shapes(all_histos,asample_dict,all_samples):
    alternate_shapes_up = []
    alternate_shapes_down = []
    for job in all_samples:
        nominal = all_histos[job.name][0]
        if job.name in asample_dict:
            alternate = copy(all_histos[asample_dict[job.name]][0])
            hUp, hDown = get_alternate_shape(nominal[nominal.keys()[0]],alternate[alternate.keys()[0]])
            alternate_shapes_up.append({nominal.keys()[0]:hUp})
            alternate_shapes_down.append({nominal.keys()[0]:hDown})
        else:
            newh=nominal[nominal.keys()[0]].Clone('%s_%s_Up'%(nominal[nominal.keys()[0]].GetName(),'model'))
            alternate_shapes_up.append({nominal.keys()[0]:nominal[nominal.keys()[0]].Clone()})
            alternate_shapes_down.append({nominal.keys()[0]:nominal[nominal.keys()[0]].Clone()})
    return alternate_shapes_up, alternate_shapes_down




if addSample_sys:
    print '\n-----> Applying Altertnate Shapes to Histograms...'        
    aUp, aDown = get_alternate_shapes(all_histos,addSample_sys,all_samples)
    final_histos['%s_Up'%(systematicsnaming['model'])]= HistoMaker.orderandadd(aUp,setup)
    del aUp
    final_histos['%s_Down'%(systematicsnaming['model'])]= HistoMaker.orderandadd(aDown,setup)



if not ignore_stats:

    print '\n-----> Applying sytematics(ignore_stats is true) to Histograms...'        

    #make statistical shapes:
    if not binstat:

        for Q in UD:
            final_histos['%s_%s'%(systematicsnaming['stats'],Q)] = {}

        for job,hist in final_histos['nominal'].items():

            print '\n\t-----> binStat(True): Making shapes for ', job
            
            errorsum=0
            for j in range(hist.GetNbinsX()+1):
                errorsum=errorsum+(hist.GetBinError(j))**2
            errorsum=sqrt(errorsum)
            total=hist.Integral()
            for Q in UD:
                final_histos['%s_%s'%(systematicsnaming['stats'],Q)][job] = hist.Clone()

                for j in range(hist.GetNbinsX()+1):
                    if Q == 'Up':
                        if rescaleSqrtN and total:
                            final_histos['%s_%s'%(systematicsnaming['stats'],Q)][job].SetBinContent(j,max(0,hist.GetBinContent(j)+hist.GetBinError(j)/total*errorsum))
                        else:
                            final_histos['%s_%s'%(systematicsnaming['stats'],Q)][job].SetBinContent(j,max(0,hist.GetBinContent(j)+hist.GetBinError(j)))
                    if Q == 'Down':
                        if rescaleSqrtN and total:
                            final_histos['%s_%s'%(systematicsnaming['stats'],Q)][job].SetBinContent(j,max(0,hist.GetBinContent(j)-hist.GetBinError(j)/total*errorsum))
                        else:
                            final_histos['%s_%s'%(systematicsnaming['stats'],Q)][job].SetBinContent(j,max(0,hist.GetBinContent(j)-hist.GetBinError(j)))
    else:
        
        print "==== Running Statistical uncertainty ===="

        threshold =  0.60 #stat error / sqrt(value). It was 0.5
        
        print "threshold", threshold

        binsBelowThreshold = {}

        for bin in range(0,nBins):
            
            # Turn off Bin Stat if selected
            if doBin == 'False': continue
            
            for Q in UD:
                final_histos['%s_bin%s_%s'%(systematicsnaming['stats'],bin,Q)] = {}

            for job,hist in final_histos['nominal'].items():
            
                #binsBelowThreshold[job] = []
                if not job in binsBelowThreshold.keys(): binsBelowThreshold[job] = [] #NEW Add
                
                print "binsBelowThreshold",binsBelowThreshold
                print "hist.GetBinContent(bin)",hist.GetBinContent(bin)
                print "hist.GetBinError(bin)",hist.GetBinError(bin)

                print '\n\t-----> Making shapes for:',job
                #binsBelowThreshold[job].append(bin) # NEW remove

                if 'ST' in job: continue
                
                if hist.GetBinContent(bin) > 0.:
                    
                    #print '\n\t\t-----> Bin content for job is > 0'
   
                    if hist.GetBinError(bin)/sqrt(hist.GetBinContent(bin)) > threshold and hist.GetBinContent(bin) >= 1.:
                        binsBelowThreshold[job].append(bin)
                 
                    elif hist.GetBinError(bin)/(hist.GetBinContent(bin)) > threshold and hist.GetBinContent(bin) < 1.:
                        binsBelowThreshold[job].append(bin)

                for Q in UD:
                    final_histos['%s_bin%s_%s'%(systematicsnaming['stats'],bin,Q)][job] = hist.Clone()
                    if Q == 'Up':
                        final_histos['%s_bin%s_%s'%(systematicsnaming['stats'],bin,Q)][job].SetBinContent(bin,max(0,hist.GetBinContent(bin)+hist.GetBinError(bin)))
                    if Q == 'Down':
                        final_histos['%s_bin%s_%s'%(systematicsnaming['stats'],bin,Q)][job].SetBinContent(bin,max(0,hist.GetBinContent(bin)-hist.GetBinError(bin)))



#write shapes in WS:
for key in final_histos:
    for job, hist in final_histos[key].items():

        print '\n-----> Writing shapes to workspace: ', job

        if 'nominal' == key:
            hist.SetName('%s'%(Dict[job]))
            hist.Write()
            rooDataHist = ROOT.RooDataHist('%s' %(Dict[job]),'%s'%(Dict[job]),obs, hist)
            getattr(WS,'import')(rooDataHist)

        for Q in UD:
            if Q in key:
                theSyst = key.replace('_%s'%Q,'')
            else:
                continue
            if systematicsnaming['stats'] in key:
                nameSyst = '%s_%s_%s' %(theSyst,Dict[job],Datacardbin)
            elif systematicsnaming['model'] in key:
                nameSyst = '%s_%s' %(theSyst,Dict[job])
            else:
                nameSyst = theSyst
            hist.SetName('%s%s%s' %(Dict[job],nameSyst,Q))
            hist.Write()
            rooDataHist = ROOT.RooDataHist('%s%s%s' %(Dict[job],nameSyst,Q),'%s%s%s'%(Dict[job],nameSyst,Q),obs, hist)
            getattr(WS,'import')(rooDataHist)

'''
if toy or signal_inject: 
    hDummy.SetName('data_obs')
    hDummy.Write()
    rooDataHist = ROOT.RooDataHist('data_obs','data_obs',obs, hDummy)
'''
#else:
    
# original code
#temp_data_dict = theData[0]
#temp_data_dict.values()[0].SetName('data_obs')
#temp_data_dict.values()[0].Write()
#rooDataHist = ROOT.RooDataHist('data_obs','data_obs',obs, temp_data_dict.values()[0])
#theData = temp_data_dict.values()[0]
    
theData.SetName('data_obs')
theData.Write()
rooDataHist = ROOT.RooDataHist('data_obs','data_obs',obs, theData)
print 'Final Data Histogram: ', theData

getattr(WS,'import')(rooDataHist)

#WS.writeToFile(outpath+'vhbb_WS_'+ROOToutname+'.root')

# now we have a Dict final_histos with sets of all grouped MCs for all systematics:
# nominal, ($SYS_Up/Down)*4, weightF_sys_Up/Down, stats_Up/Down

print '\n\t ========== PRINTOUT PRETTY TABLE ===========\n'
#header
printout = ''
printout += '%-25s'%'Process'
printout += ':'
for item, val in final_histos['nominal'].items():
    printout += '%-12s'%item
print printout+'\n'
for key in final_histos:
    printout = ''
    printout += '%-25s'%key
    printout += ':'
    for item, val in final_histos[key].items():
        printout += '%-12s'%str('%0.5f'%val.Integral())
    print printout

#-----------------------------------------------------------------------------------------------------------

# -------------------- write DATAcard: ----------------------------------------------------------------------

DCprocessseparatordict = {'WS':':','TH':'/'}

# create two datacards: for TH and WS
print '\n\n------> Creating Datacards...'

for DCtype in ['TH']:
    
    columns=len(setup)
    f = open(outpath+'vhbb_DC_%s_%s.txt'%(DCtype,ROOToutname),'w')
    print '\n\n------> Writing to File: ', f
    
    fileName = outpath+'vhbb_DC_%s_%s.txt'%(DCtype,ROOToutname)

    f.write('imax\t1\tnumber of channels\n')
    f.write('jmax\t%s\tnumber of backgrounds (\'*\' = automatic)\n'%(columns-1))
    f.write('kmax\t*\tnumber of nuisance parameters (sources of systematical uncertainties)\n\n')
    f.write('shapes * * vhbb_%s_%s.root $CHANNEL%s$PROCESS $CHANNEL%s$PROCESS$SYSTEMATIC\n\n'%(DCtype,ROOToutname,DCprocessseparatordict[DCtype],DCprocessseparatordict[DCtype]))
    f.write('bin\t%s\n\n'%Datacardbin)

    #if toy or signal_inject:
    #    f.write('observation\t%s\n\n'%(hDummy.Integral()))
    #else:
    f.write('observation\t%s\n\n'%(theData.Integral()))
        
    # datacard bin
    f.write('bin')
    for c in range(0,columns): f.write('\t%s'%Datacardbin)
    f.write('\n')
    
    # datacard process
    f.write('process')
    for c in setup: f.write('\t%s'%Dict[c])
    f.write('\n')
    f.write('process')
    
    #print 'anType:', anType
    
    if 'VV' not in str(anType):
        for c in range(-1,columns-1): f.write('\t%s'%c)
    else:
        for c in range(0,columns): f.write('\t%s'%c)
        
    f.write('\n')

    # datacard yields
    f.write('rate')
    for c in setup: 
        f.write('\t%s'%final_histos['nominal'][c].Integral())
    f.write('\n')
    
    # get list of systematics in use
    if 'All' in pt_region:
        InUse = eval(config.get('Datacard','InUse'))
    else:
       InUse = eval(config.get('Datacard','InUse_%s'%pt_region))
        
    # Turn of SYS if selected
    if doSYS == 'False':
        InUse = []
    
    print 'In Use:', InUse

    # write non-shape systematics
    for item in InUse:

        f.write(item)

        what=eval(config.get('Datacard',item))

        #print 'What:', what
        
        f.write('\t%s'%what['type'])

        for c in setup:
            if c in what:
                if '_eff_e' in item and 'Zuu' in data_sample_names: f.write('\t-')
                elif '_eff_m' in item and 'Zee' in data_sample_names: f.write('\t-')
                elif '_trigger_e' in item and 'Zuu' in data_sample_names: f.write('\t-')
                elif '_trigger_m' in item and 'Zee' in data_sample_names: f.write('\t-')
                else:
                    f.write('\t%s'%what[c])
            else:
                f.write('\t-')
        f.write('\n')

    # Write statistical shape variations
    #if not ignore_stats and str(anType) != 'cr':
    if not ignore_stats:
        print '\n\t-----> Writing shape systematics to datacard...'
        #print '\t\t binsbelowthreshold[]:', binsBelowThreshold
        
        if binstat:   
            for c in setup:

                # Turn off Bin Stat if selected
                #if doBin == 'False': continue
                #continue
                
                for bin in range(0,nBins):
                    if bin in binsBelowThreshold[c]:
                        
                        print '\n\t\t-----> Writing shape for:', c
                        
                        #if 'bin13' in '%s_bin%s_%s_%s\tshape'%(systematicsnaming['stats'],bin,Dict[c],Datacardbin): continue
                        #if 'bin11' in '%s_bin%s_%s_%s\tshape'%(systematicsnaming['stats'],bin,Dict[c],Datacardbin): continue
                                                
                        f.write('%s_bin%s_%s_%s\tshape'%(systematicsnaming['stats'],bin,Dict[c],Datacardbin))
                        
                        for it in range(0,columns):
                            if it == setup.index(c):
                                f.write('\t1.0')
                            else:
                                f.write('\t-')
                        f.write('\n')
        else:
            for c in setup:

                print '\n\t\t-----> Writing shape for:', c
            
    
                f.write('%s_%s_%s\tshape'%(systematicsnaming['stats'],Dict[c],Datacardbin))
                for it in range(0,columns):
                    if it == setup.index(c):
                        f.write('\t1.0')
                    else:
                        f.write('\t-')
                f.write('\n')

    # UEPS systematics
    #for weightF_sys in weightF_systematics:
    #    f.write('%s\tshape' %(systematicsnaming[weightF_sys]))
    #    for it in range(0,columns): f.write('\t1.0')
    #    f.write('\n')

    # additional sample systematics
    if addSample_sys:
        alreadyAdded = []
        for newSample in addSample_sys.iterkeys():
            for c in setup:
                if not c == GroupDict[newSample]: continue
                if Dict[c] in alreadyAdded: continue
                f.write('%s_%s\tshape'%(systematicsnaming['model'],Dict[c]))
                for it in range(0,columns):
                    if it == setup.index(c):
                         f.write('\t1.0')
                    else:
                         f.write('\t-')
                f.write('\n')
                alreadyAdded.append(Dict[c])

    # regular systematics
    for sys in systematics:

        if 'eff_e' in sys and 'Zuu' in data_sample_names: continue
        elif '_eff_m' in sys and 'Zee' in data_sample_names: continue

        sys_factor=sys_factor_dict[sys]
        f.write('%s\tshape'%systematicsnaming[sys])

        for c in setup:
            if c in sys_affecting[sys]:
                f.write('\t%s'%sys_factor)
            else:
                f.write('\t-')
        f.write('\n')

    #rateParams=eval(config.get('Datacard','rateParams_%s_%s'%(str(anType), pt_region)))
    #if str(anType) == 'cr' or str(anType) == 'BDT': # and treevar != 'VV_bdt.nominal':
        
    if 'Low' in pt_region:
        rateParams = eval(config.get('Datacard','rateParams_low'))
    elif 'High' in pt_region:
        rateParams = eval(config.get('Datacard','rateParams_high'))
    else:
        rateParams = eval(config.get('Datacard','rateParams'))

    #if treevar == 'VV_bdt.nominal':
    #    rateParams = eval(config.get('Datacard','rateParams'))

        rateParams_Unc = eval(config.get('Datacard','rateParams_Unc'))
    for rateParam in rateParams:
        dictProcs = eval(config.get('Datacard', rateParam))
        for proc in dictProcs.keys():
            #f.write(rateParam+'\trateParam\t'+Datacardbin+'\t'+proc+'\t'+str(dictProcs[proc])+'\t'+str(rateParams_Unc[proc])+'\n')
            f.write(rateParam+'\trateParam\t'+Datacardbin+'\t'+proc+'\t'+str(dictProcs[proc])+'\n')


    
    f.close()
    
    useSpacesInDC(fileName)

# --------------------------------------------------------------------------




outfile.Close()

#  LocalWords:  syst anType
