#!/usr/bin/env python
# run as:
# HistFitter.py -twf -u "--signalRegions SR0bee,SR0bem,SR0bmm,SR1bee,SR1bem,SR1bmm,SR3bee,SR3bem,SR3bmm --signalGridName Mc12SusyGtt --signalList signal156548 --F excl" python/summer2013SameSign.py

from configManager import configMgr
from systematic import Systematic
from optparse import OptionParser
import configWriter
import copy

from sets import Set   
import  ROOT, math, sys, os
# CHANGE NTOYS, appended path, signal File!!!!!!

import pathUtilities
import json
import signalSameSignTools

##importing usefull things to defined samples (to keep the  main scrip clean!!)
from Helper import setBlind,sampleType
from Helper import bkgsDef,sample
from Helper import GetBinnedFitOptions
from Helper import CheckVarExistInBinningDict


## Getting input options
inputParser = OptionParser()
inputParser.add_option('', '--calculatorType', dest = 'calculatorType', default = 2, help='0 for frequentist, 2 for asymptotic')
inputParser.add_option('', '--sysList', dest = 'sysList', default = "", help='list of systematics')
inputParser.add_option('', '--signalGridName', dest = 'signalGridName', default = 'Mc15SusyGtt', help='name of the grid(e.g. gtt)')
inputParser.add_option('', '--lumiTag', dest = 'lumiTag', default = '2000',  help='lumi tag in the input files')
inputParser.add_option('', '--signalList', dest = 'signalList', default = 'signal370102_SP_LSP', help='give it a list of signal runnumbers and their mass of SP and LSP')
inputParser.add_option('', '--theoryUncertMode', dest = 'theoryUncertMode', default = "nom", help='sets theory (i.e. lumi uncert) nom/up/down')
inputParser.add_option('', '--additionalOutName', dest = 'additionalOutName', default = "", help='additional name for output file')
# important: the deault signalRegions are the one trhat are used by default by the upstream script. leave them to be the full list of "good" regions
inputParser.add_option('', '--signalRegions', dest = 'signalRegions', default = '', help='sets which signal regions to use,(one or several), 0b,1b and/or 3b')
inputParser.add_option('', '--binnedFitSR ', dest= 'binnedFitSR',default='',help="Ex: <SR1>:<var1>,<SR2>:<var2>,...,  where <var1> is the variabled to be fitted in <SR1> and so on... If more than one SR, they must be comma separated.")
inputParser.add_option('', '--controlRegions', dest = 'controlRegions', default = '', help='sets which control regions to use,(one or several)')
inputParser.add_option('', '--bkgToNormalize',dest='bkgToNormalize',default='',help="backgrounds to normalize in the CR provided, i.e <bkg1>:<CR1>,<bkg2>:<CR2>")
inputParser.add_option('', '--extraSampleWeight',dest='extraSampleWeight',default='',help="Comma separated list of the extra weight(s) to be applied to the *MC* bkg samples, i.e <bkg1>:<weight1>,<bkg2>:<weight2>. Currently HF  does *NOT* allow for systematic variations for this weight. This weight for the concerned sample is added *INTERNALLY* by HF for all systematic variations as part of the nominal weight, therefore systematics for this weight will require the internal patching of HF to take out this weight from the whole set of systematics for the concerned sample. If you need systematics the best solution is to create a dummy branch for all MC processes, and add this weight as a part of the general nominal weight for all samples.")
inputParser.add_option('', '--NF',dest="NF",default='',help="Comma separaeted list of the bkgs samples for which a normalisation SF (read from a json file) should be applied,  i.e <bkg1>,<bkg2>,...")
inputParser.add_option('', '--binnedFitCR',dest='binnedFitCR',default='',help="Ex: <CR1>:<var1>,<CR2>:<var2>,...,  where <var1> is the variabled to be fitted in <CR1> and so on... If more than one CR, they must be comma separated.")
inputParser.add_option('', '--binnedFitVR',dest='binnedFitVR',default='',help="Ex: <VR1>:<var1>,<VR2>:<var2>,...,  where <var1> is the variabled to be fitted in <VR1> and so on... If more than one VR, they must be comma separated.")
inputParser.add_option('', '--validationRegions', dest = 'validationRegions', default = "", help='sets which validation regions to use,(one or several)')
inputParser.add_option('', '--doBlind', dest = 'doBlind',action="store",  default ="", help='List of regions to blind (comma separated), i.e: ALL, SR, CR, VR. If empty, it will blind all')
inputParser.add_option('', "--SigNameSchema" ,default="SP:4,LSP:5", help="signal sample naming schema which is used to get correct mass from a sample name. SR:X,LSP:Y. X and Y means the position for a  string splitted by '_'")

import select
configArgs = []

userArgs= configMgr.userArg.split(' ')
for i in userArgs:
    configArgs.append(i)

(options, args) = inputParser.parse_args(configArgs)


## Printing input arguments
print "## You are providing the following options (if an option is not provided, then the default value will be shown):"
print "-lumiTag :",options.lumiTag
print "-calculatorType: ",options.calculatorType
print "-signalGridName: ",options.signalGridName
print "-signalList: ",options.signalList
print "-theoryUncertMode: ",options.theoryUncertMode
print "-additionalOutName: ",options.additionalOutName
print "-signalRegions: ",options.signalRegions
print "-binnedFitSR: ",options.binnedFitSR
print "-controlRegions: ",options.controlRegions
print "-bkgToNormalize: ",options.bkgToNormalize
print "-extraSampleWeight",options.extraSampleWeight
print "--NF",options.NF
print "-binnedFitCR: ",options.binnedFitCR
print "-binnedFitVR: ",options.binnedFitVR
print "-validationRegions: ",options.validationRegions
print "-doBlind: ",options.doBlind
print "-sysList: ",options.sysList


lumiTag=options.lumiTag


#############################
##   Setting systematics   ##
#############################

systematicList=options.sysList
if systematicList=='ALL':
    #systematicList='EG,JET,MU,MET,FT,PU,TRIG,CHFLIP,TH'
    systematicList='EG,JET,MU,MET,FT,PU,TRIG,FAKES,CHFLIP,TH'


systematicList=systematicList.split(',')

#adding flat uncertainty (needed for optimisation studies)
flat = 0
for fl in systematicList:
    if 'FLAT' in fl: flat = float(fl[4:])*0.01 #need to pass relative variation


#######################
##  Setting regions  ##
#######################

signalRegionList = options.signalRegions.split(",")
validationRegionList=[]
controlRegionList=[]


if len(signalRegionList)==1 and signalRegionList[0]=='': signalRegionList=[]

if options.controlRegions != "":
    controlRegionList = options.controlRegions.split(",")
    #if len(controlRegionList)>1:  upgrade to allow more than 1 CR
    #    sys.exit("--> Sorry, current framework allows only one CR... ABORTING!")

else:
    controlRegionList=[]


if options.validationRegions != "":
    validationRegionList = options.validationRegions.split(",")
else:
    validationRegionList=[]


if myFitType!=FitType.Background:
    # upgrading code to allow multiple SRs in the fit
    if len(signalRegionList)==0:  #or len(signalRegionList)>1: 
        sys.exit("--> Sorry, for exclusion or discovery fits you need to pass at least one SR... ABORTING")

    if len(validationRegionList)>0: 
        sys.exit("--> Sorry VRs can not be used in exclusion or discovery fits... ABORTING!")
   
else: 
    #if bkg-only fit do some conversions depending on what you are providing:

    # 1. SRs will be used as VRs.
    if controlRegionList and signalRegionList:
        print "- Converting SRs to VRs as fit is bkg-only..."
        validationRegionList+=list(signalRegionList)
        signalRegionList=[]

    # 2. VRs to SRs
    elif len(controlRegionList)==0 and len(signalRegionList)==0 and len(validationRegionList)>0:
        print "- Converting VRs to SRs as fit is bkg-only... However it will be used as CR later..."
        signalRegionList=list(validationRegionList)
        validationRegionList=[]
    
 

print "## Setting regions :"
print '- SRs: ',signalRegionList
print '- CR: ',controlRegionList
print '- VRs: ',validationRegionList


print "## Setting regions to blind:"
isBlind = setBlind(options.doBlind)


####################################
## Setting options for binned fits #
####################################


binnedFitSR=GetBinnedFitOptions(options.binnedFitSR,signalRegionList)    
binnedFitCR={}
if controlRegionList: binnedFitCR = GetBinnedFitOptions(options.binnedFitCR,controlRegionList)
binnedFitVR={}
if validationRegionList: binnedFitVR = GetBinnedFitOptions(options.binnedFitVR,validationRegionList)


print "## Systematic list: ",systematicList
print "## Lumi tag: ",options.lumiTag
print "## Fit Type: ",myFitType



if myFitType==FitType.Discovery:

    if len(signalRegionList) != 1:
       sys.exit("--> For discovery fits only one SR is allowed... ABORTING!")
       
    options.signalGridName="Discovery"

    for sr in signalRegionList:
        if binnedFitSR[sr] != "cuts":
          print "- Discovery fits are single bin... changing to single bin"
          binnedFitSR[sr]="cuts"


##########################################
## Setting options for bkgs to normalise #
##########################################

bkgNorm={}
if options.bkgToNormalize is not "":
    for bkg in options.bkgToNormalize.split(','):

        temp_bkg = bkg.split(':')
        bkgNorm[temp_bkg[0]] = temp_bkg[1]



##############################################################
## Setting options for additional weights for MC bkg samples #
##############################################################

extraSampleWeight={}
if options.extraSampleWeight is not "":
    for bkg in options.extraSampleWeight.split(','):

        temp_bkg = bkg.split(':')
        extraSampleWeight[temp_bkg[0]] = temp_bkg[1]



##############################################################
## Setting options for NFs for MC bkg samples #
##############################################################

NF=[]
if options.NF is not "":
    NF = options.NF.split(',')


#######################################
# Defining object with all samples   ##
#######################################

allBkg=bkgsDef()

########################################
##                                    ##
##---- to define before running ------##
##                                    ##

## Getting hardcoded yields: fakes, charge-flip and data
#dataCounts,fakeCount, fakeStatErr, fakeSystErrUp, fakeSystErrDown
#mischCount, mischStatErr, mischSystErrUp, mischSystErrDown
# They are all keys in the dictionary yieldsCoded

yieldsCoded=None

with open(pathUtilities.pythonDirectory()+'/hardCodedYields.json') as json_file:
    yieldsCoded=json.load(json_file)

dataCounts=yieldsCoded['dataCounts']



# getting dictionary of NF and their uncertainties
NF_dict={}

if 'NF' in yieldsCoded: NF_dict = yieldsCoded['NF']

#checking that samples for NF exist in dictionary
for sam in NF:
   if sam not in NF_dict:
         print  "- Given sample does not exist in NF dictionary of json file: ",sam
         sys.exit("- Aborting!")


# getting binning:
binning = yieldsCoded['binning']


CheckVarExistInBinningDict(binnedFitSR,binning)
CheckVarExistInBinningDict(binnedFitCR,binning)

#importing theory systematics
theorySyst=None
with open(pathUtilities.pythonDirectory()+'/theorySystematics.json') as json_file:
    theorySyst=json.load(json_file)


#use data yiels from TTres:
useDataSample = False


#defining backgrounds

### Full Run-2 Strong bkgs 1st wave
#### irreducibel bkgs
#OtherMultiboson = sample('OtherMultiboson',ROOT.kGreen+2,"WW, ZZ, VH, VVV",True,sampleType.BKG,theorySyst['thUnc_OtherMultibosonUp'],theorySyst['thUnc_OtherMultibosonDown'])
#ttH = sample('ttH',ROOT.kOrange,"t#bar{t}H",True,sampleType.BKG,theorySyst['thUnc_ttHUp'],theorySyst['thUnc_ttHDown'])
#RareTop_NottH = sample('RareTop_NottH',ROOT.kCyan+1,"t(W)Z, t#bar{t}VV, 3t, 4t",True,sampleType.BKG,theorySyst['thUnc_RareTop_NottHUp'],theorySyst['thUnc_RareTop_NottHDown'])
#ttW = sample('ttW',ROOT.kViolet-9,"t#bar{t}W",True,sampleType.BKG,theorySyst['thUnc_ttWUp'],theorySyst['thUnc_ttWDown'])
#ttZ = sample('ttZ',ROOT.kAzure+7,"t#bar{t}Z",True,sampleType.BKG,theorySyst['thUnc_ttZUp'],theorySyst['thUnc_ttZDown'])
#WZ  = sample('WZ',ROOT.kOrange+1,"WZ",True,sampleType.BKG,theorySyst['thUnc_WZUp'],theorySyst['thUnc_WZDown'])
#
#Multiboson = sample('Multiboson',ROOT.kGreen+2,"Multiboson",True,sampleType.BKG,theorySyst['thUnc_MultibosonUp'],theorySyst['thUnc_MultibosonDown'])
#ttV=sample('ttV',ROOT.kViolet-9,"t#bar{t}V",True,sampleType.BKG,theorySyst['thUnc_ttVUp'],theorySyst['thUnc_ttVDown'])
#Multitop = sample('Multitop',ROOT.kGreen+2,"Multitop",True,sampleType.BKG,theorySyst['thUnc_MultitopUp'],theorySyst['thUnc_MultitopDown'])
#
#### fakes bkgs
#MisCharge = sample('MisCharge',ROOT.kRed+2,'Charge-flip',False,sampleType.BKG)
#MisCharge.setYields(yieldsCoded['mischCount'],yieldsCoded['mischStatErr'])
#if "CHFLIP" in systematicList: MisCharge.setDataDrivenSystematics(yieldsCoded['mischSystErrUp'], yieldsCoded['mischSystErrDown'])
#Fakes = sample('Fakes',ROOT.kOrange-9,"Fake/non-prompt",False,sampleType.BKG)
#Fakes.setYields(yieldsCoded['fakeCount'], yieldsCoded['fakeStatErr'])
#if 'FAKES' in systematicList: Fakes.setDataDrivenSystematics(yieldsCoded['fakeSystErrUp'], yieldsCoded['fakeSystErrDown'])


## Full Run-2 strong bkgs 
### irreducible
Multitop = sample('Multitop',ROOT.kCyan+1,"Other top(s)",True,sampleType.BKG)
SM4tops = sample('SM4tops',ROOT.kOrange,"SM4tops",True,sampleType.BKG)
OtherMultiboson = sample('OtherMultiboson',ROOT.kGreen+2,"WW, ZZ, VVV",True,sampleType.BKG)
ttW = sample('ttW',ROOT.kViolet-9,"t#bar{t}W",True,sampleType.BKG)
ttZ = sample('ttZ',ROOT.kAzure+7,"t#bar{t}Z",True,sampleType.BKG)
WZ  = sample('WZ',ROOT.kOrange+1,"WZ",True,sampleType.BKG)

### fakes estimated by MC
TTbarSgTop = sample('TTbarSgTop',ROOT.kRed+2,'t#bar{t} & SingleTop', True, sampleType.BKG)
Vjets = sample('VJets', ROOT.kOrange-9, 'V+jets', True, sampleType.BKG) # for shuhui: newHF ntuples
### fakes esrimated by DD method (should not use together with above processes
MisCharge = sample('MisCharge',ROOT.kRed+2,'Charge-flip',False,sampleType.BKG)
MisCharge.setYields(yieldsCoded['mischCount'],yieldsCoded['mischStatErr'])
if "CHFLIP" in systematicList: MisCharge.setDataDrivenSystematics(yieldsCoded['mischSystErrUp'], yieldsCoded['mischSystErrDown'])
Fakes = sample('Fakes',ROOT.kOrange-9,"Fake/non-prompt",False,sampleType.BKG)
Fakes.setYields(yieldsCoded['fakeCount'], yieldsCoded['fakeStatErr'])
if 'FAKES' in systematicList: Fakes.setDataDrivenSystematics(yieldsCoded['fakeSystErrUp'], yieldsCoded['fakeSystErrDown'])


# adding bkgs to the tool...
# configuration here is usually used for limit setting: less splitting go faster!

allBkg.addSample(Multitop)
allBkg.addSample(SM4tops)
allBkg.addSample(OtherMultiboson)
allBkg.addSample(ttW)
allBkg.addSample(ttZ)
allBkg.addSample(WZ)
#allBkg.addSample(TTbarSgTop)
#allBkg.addSample(Vjets)
allBkg.addSample(MisCharge)
allBkg.addSample(Fakes)


#configuration here normally used for tables

'''
allBkg.addSample(OtherMultiboson)
allBkg.addSample(ttH)
allBkg.addSample(RareTop_NottH)
allBkg.addSample(ttW)
allBkg.addSample(ttZ)
allBkg.addSample(WZ)
allBkg.addSample(MisCharge)
allBkg.addSample(Fakes)
'''

##                                    ##
##  End of "to define before running" ##
##                                    ##
########################################




## Global variables
bkgList=allBkg.bkgList
dataDrivenList=allBkg.dataDrivenList
sigList=options.signalList.split(';') # shuhui: to add theory uncertainties on signal samples


def main():

    inputFileDict = {}

    readingNtuples(inputFileDict)


    setupConfigMgr(inputFileDict)

   
    if myFitType==FitType.Background:
        print "## Configuring a bkg-only fit"

        doFitConfig(inputFileDict,"bkgOnly")
    else:
        signalGridName = options.signalGridName
        signalNamesList = options.signalList.split(';')

        if myFitType==FitType.Exclusion:
            print "## Configuring an exclusion fit"

            for signalName in signalNamesList:
                doFitConfig(inputFileDict,signalGridName+"_"+signalName, signalName)
        else:
            print "## Configuring a discovery fit"
            doFitConfig(inputFileDict,"Discovery")
    
def readingNtuples(inputFileDict):

    inputFileDict['data'] = [pathUtilities.histFitterSource()+'/InputTrees/data.'+lumiTag+'.root']
    inputFileDict['signal'] = [pathUtilities.histFitterSource()+'/InputTrees/signal.'+lumiTag+'.root']

    print "## Reading input trees from : {0}/InputTrees/signal.".format(pathUtilities.histFitterSource())+lumiTag+".root"
    

    # reading individual ntuples for MC bkgs:
    for i in range(len(bkgList)):

        if bkgList[i].getSampleType()==sampleType.BKG:

            if bkgList[i].getMC()==True:

                inputFileDict[bkgList[i].getName()] = [pathUtilities.histFitterSource()+'/InputTrees/'+bkgList[i].getName()+'.'+lumiTag+'.root']

                print "## Reading input trees from : {0}/InputTrees/{1}.{2}.root".format(pathUtilities.histFitterSource(),bkgList[i].getName(),lumiTag)

    return

def setupConfigMgr(inputFileDict):
    #-------------------------------
    # Parameters for hypothesis test
    #-------------------------------
    configMgr.analysisName = options.signalGridName+'_'+options.additionalOutName
    
    configMgr.nTOYs= 1000
    configMgr.calculatorType = int(options.calculatorType)
    configMgr.testStatType = 3   # 3=one-sided profile likelihood test statistic (LHC default)
    configMgr.nPoints = 40       # number of values scanned of signal-strength for upper-limit determination of signal strength.
    #configMgr.scanRange = (0., 20.)
   
    if isBlind.SR: configMgr.blindSR = True
    if isBlind.CR: configMgr.blindCR = True
    if isBlind.VR: configMgr.blindVR = True

    configMgr.useSignalInBlindedData = False


    configMgr.writeXML = True #True is necessary for 2nd wave and below
    configMgr.keepSignalRegionType = True #Force SR to remain a SR for bkgOnly fits  (in those cases, SRs are set by  hand latter as CRs)

    configMgr.outputLumi =float(lumiTag)/1000 
    configMgr.inputLumi = configMgr.outputLumi #deal with this at the sample level
    configMgr.setLumiUnits("fb-1")

    configMgr.histCacheFile = os.getenv("HFRUNDIR")+"/data/"+configMgr.analysisName+".root"
    configMgr.outputFileName = os.getenv("HFRUNDIR")+"/results/"+configMgr.analysisName+"_output.root"
    
    if not configMgr.readFromTree:
        print "READING FROM data/"+configMgr.analysisName+".root"
        inputFileDict['background'] = ["data/"+configMgr.analysisName+".root"]  ## To fix !!!
        
    configMgr.nomName = "_nom"

    ##########
    ## CUTS ##
    ##########
    
    # define signal regions. please always enclose SRs between () to ease combination
    # note: this assumes events in ntuples already pass SS(10+10+(10)) selection

    print "******** Defining dictionary of cuts..."

    # validation/control region
    configMgr.cutsDict["CRWZ2j"] = "(nSigLep==3 && NlepBL==3 && nBJets20==0 && (nJets25==2 || nJets25==3) && met>30000 && met<150000 && meff<1500000 && ht_lept>130000 && mSFOS>81000 && mSFOS<101000 && isSS15)"
    configMgr.cutsDict["VRWZ2j"] = "(nSigLep==3 && NlepBL==3 && nBJets20==0 && (nJets25==2 || nJets25==3) && met>30000 && met<150000 && meff<1500000 && ht_lept>130000 && mSFOS>81000 && mSFOS<101000 && isSS15)"
    configMgr.cutsDict["VRWZge4j"] = "(nSigLep==3 && NlepBL==3 && nBJets20==0 && nJets25>=4 && met>30000 && met<150000 && meff<1500000 && ht_lept>130000 && mSFOS>81000 && mSFOS<101000 && isSS15)"
    configMgr.cutsDict["VRWZ4j"] = "(nSigLep==3 && NlepBL==3 && nBJets20==0 && nJets25>=4 && meff>600000 && meff<1500000 && met>30000 && met<250000 && mSFOS>81000 && mSFOS<101000 && met/meff<0.2)"
    configMgr.cutsDict["VRWZ6j"] = "(nSigLep==3 && NlepBL==3 && nBJets20==0 && nJets25>=6 && meff>400000 && meff<1500000 && met>30000 && met<250000 && mSFOS>81000 && mSFOS<101000 && met/meff<0.15)"
    configMgr.cutsDict["VRTTV"] = "(nSigLep>=2 && NlepBL>=2 && nBJets20>=1 && nJets40>=3 && meff>600000 && meff<1500000 && met>30000 && met<250000 && isSS30 && dRl1j>1.1 && (ht_bjet/ht_jet)>0.4 && (met/meff)>0.1 && Pt_subl>30000)"
    configMgr.cutsDict["VRTTW"] = "(nSigLep==2 && NlepBL==2 && SSChannel==1 && nBJets20>=2 && nJets25>=2 && meff<1500000 && met>30000 && met<250000 && Pt_l>40000 && Pt_subl>25000)"
    configMgr.cutsDict["VRTTW3j"] = "(nSigLep==2 && NlepBL==2 && SSChannel==3 && nBJets20>=2 && nJets25>=3 && meff<1500000 && met>30000 && met<250000 && Pt_l>25000 && Pt_subl>25000)"

    # extra VRs
    configMgr.cutsDict["VRTTV1b6j"] = "(nSigLep>=2 && NlepBL>=2 && nBJets20>=1 && nJets40>=6 && meff<1500000 && met>30000 && met<250000 && isSS30 && (met/meff)<0.15)"
    configMgr.cutsDict["VRTTV6j"] = "(nSigLep>=2 && NlepBL>=2 && nJets40>=6 && meff<1200000 && met>30000 && met<250000 && isSS30 && met/meff<0.15)"
    configMgr.cutsDict["VRTTV2b"] = "(nSigLep>=2 && NlepBL>=2 && nBJets20>=2 && nJets40>=3 && meff>600000 && meff<1500000 && met>30000 && met<250000 && isSS30 && dRl1j>1 && (ht_bjet/ht_jet)>0.3 && (met/meff)>0.12)"
    configMgr.cutsDict["VRTTW1b"] = "(nSigLep==2 && NlepBL==2 && nBJets20>=1 && nJets40>=3 && meff>550000 && meff<1500000 && met>30000 && met<250000 && Pt_l>30000 && Pt_subl>30000 && dRl1j>1 && (ht_bjet/ht_jet)>0.42 && (met/meff)>0.15)"
    configMgr.cutsDict["VRTTZ"] = "(nSigLep>=3 && NlepBL>=3 && nBJets20>=1 && nJets40>=4 && meff>500000 && meff<1500000 && met>30000 && met<250000 && Pt_l>20000 && Pt_subl>20000 && (ht_bjet/ht_jet)>0.13 && mSFOS>81000 && mSFOS<101000 && met/meff<0.2)"
    configMgr.cutsDict["VRWW"] = "(nSigLep==2 && NlepBL==2 && nBJets20==0 && nJets50>=2 && meff>650000 && meff<1500000 && met>55000 && met<250000 && (!(mllSS>81000 && SSChannel==2 && mllSS<101000)) && dRl1j>0.7 && dRl2j>0.7 && dRSS>1.3)"
    configMgr.cutsDict["VRWZ2j1b"] = "(nSigLep==3 && NlepBL==3 && nBJets20>=1 && nJets25==2 && met>30000 && met<250000 && meff<1500000 && mSFOS>81000 && mSFOS<101000 && Pt_l>20000 && Pt_subl>20000 && Pt_thirdl>20000)"

    # Full Run-2 strong SRs:    
    # RPV LQD
    configMgr.cutsDict["RpvLQD"] = "(nSigLep==2)&&(nJets50>=5)&&(nBJets20>=0)&&(meff>=2600000)"
    # RPV UDD
    configMgr.cutsDict["RpvUDD1b"] = "(nSigLep==2)&&(nJets50>=6)&&(nBJets20==1)&&(ht_jet>=1600000)"
    configMgr.cutsDict["RpvUDD2b"] = "(nSigLep==2)&&(nJets25>=2)&&(nBJets20==2)&&(ht_jet>=1700000)"
    configMgr.cutsDict["RpvUDDge2b"] = "(nSigLep==2)&&(nJets50>=5)&&(nBJets20>=2)&&(ht_jet>=1600000)"
    configMgr.cutsDict["RpvUDDge3b"] = "(nSigLep==2)&&(nJets50>=4)&&(nBJets20>=3)&&(meff>=1600000)"
    # RPC GG 2-step via slep
    configMgr.cutsDict["RpcGGslep1"] = "(nSigLep>=3 && nJets40 >=4 && nBJets20==0 && (mSFOS < 81000 || mSFOS > 101000) && met > ht_jet*0.4 && Pt_subl > 30*1000 && met > ht_lept*1.4)"
    configMgr.cutsDict["RpcGGslep2"] = "(nSigLep>=3 && nJets40 >=4 && nBJets20==0 && (mSFOS < 81000 || mSFOS > 101000) && met/ht_jet > 0.3 && Pt_subl > 70000 && dPhiLLmet > 0.7 && met> 150000)"
    configMgr.cutsDict["RpcGGslep3"] = "(nSigLep>=3 && nJets40 >=4 && nBJets20==0 && (mSFOS < 81000 || mSFOS > 101000) &&  ht_jet > 1200000 && met > 100000)"
    # RPC GG 2-step via WZ
    configMgr.cutsDict["RpcGGwz1"] = "(nSigLep>=2 && nBJets20==0 && nJets40>=6 && met>150000 && meff>2100000)"
    configMgr.cutsDict["RpcGGwz2"] = "(nSigLep>=2 && nBJets20==0 && nJets40>=6 && met>190000 && meff>1300000 && dPhiLLmet>0.8)"
    configMgr.cutsDict["RpcGGwz3"] = "(nSigLep>=2 && nBJets20==0 && nJets25>=6 && met>200000 && dPhiLLmet>0.2 && met_Sig>6 && meff/ht_lept>8 && NlepBL>=3)"
    # RPC SS 2-step via slep 
    configMgr.cutsDict["RpcSSslep1"] = "(nSigLep==3 && NlepBL==3 && Pt_l>40000 && Pt_subl>40000 && Pt_thirdl>40000 && nBJets20==0 && nJets25>=2 && Pt_jet>60000 && Pt_subjet>60000 && met>=200000 && meff>=2000000 && dPhiLLmet>=0.3 && dRll>=0.5 && !(mSFOS>81000 && mSFOS<101000))" 
    configMgr.cutsDict["RpcSSslep1excl"] = "(nSigLep==3 && NlepBL==3 && Pt_l>40000 && Pt_subl>40000 && Pt_thirdl>40000 && nBJets20==0 && nJets25>=2 && Pt_jet>60000 && Pt_subjet>60000 && met>=200000 && meff>=1000000 && dPhiLLmet>=0.3 && dRll>=0.5 && !(mSFOS>81000 && mSFOS<101000))" 
    configMgr.cutsDict["RpcSSslep2"] = "(nSigLep==3 && NlepBL==3 && Pt_l>40000 && Pt_subl>40000 && Pt_thirdl>40000 && nBJets20==0 && nJets25>=2 && Pt_jet>60000 && Pt_subjet>60000 && met>=200000 && meff>=1000000 && met/ht_lept>=0.7 && dPhiLLmet>=0.5 && dRll>=0.2 && !(mSFOS>81000 && mSFOS<101000))" 
    configMgr.cutsDict["RpcSSslep3"] = "(nSigLep==3 && NlepBL==3 && Pt_l<=60000 && nBJets20==0 && nJets25>=3 && Pt_jet>60000 && Pt_subjet>60000 && met>=100000 && meff>=600000 && ht_lept/ht_jet<=0.6 && dPhiLLmet>=1.4 && !(mSFOS>81000 && mSFOS<101000))" 
    configMgr.cutsDict["RpcSSslep4"] = "(nSigLep==3 && NlepBL==3 && Pt_l>30000 && Pt_subl>30000 && Pt_thirdl>30000 && nBJets20==0 && nJets25>=3 && Pt_jet>60000 && Pt_subjet>60000 && met>=100000 && meff>=700000 && met/ht_lept>=0.7 && ht_lept/ht_jet<=0.6 && dPhiLLmet>=1.4 && !(mSFOS>81000 && mSFOS<101000))" 
    # RPC SS 2-step via WZ
    configMgr.cutsDict["RpcSSwz1"]= "(nSigLep>=3)&& !(mSFOS>81000 && mSFOS<101000)&& (nBJets20==0)&& (meff>=0)&& (nJets25>=4)&& (met/meff >=0.200000)&& (ht_lept/ht_jet <=0.200000)"
    configMgr.cutsDict["RpcSSwz2"]= "(nSigLep>=3)&& (mSFOS>81000 && mSFOS<101000)&& (nBJets20==0)&& (meff>=800000)&& (met>=150000)&& (nJets25>=6)&& (met/ht_lept >=1.200000)&& (ht_lept/ht_jet <=0.300000)"
    configMgr.cutsDict["RpcSSwz3"]= "(nSigLep>=3)&& (mSFOS>81000 && mSFOS<101000)&& (nBJets20==0)&& (meff>=900000)&& (met>=200000)&& (nJets40>=5)&& (met/ht_lept >=1.100000)&& (ht_lept/ht_jet <=0.400000)"
    configMgr.cutsDict["RpcSSwz4"]= "(nSigLep>=3)&& (nBJets20==0)&& (meff>=1500000)&& (met>=250000)&& (nJets40>=5)&& (met/ht_lept >=0.300000)&& (ht_lept/ht_jet <=0.700000)"






def doFitConfig(inputFileDict, fcName, sigSample=""):

    '''
    The sintax is the following: define samples, then channels, then do fit configuration

    '''

    #---------------#
    # Build samples #
    #---------------#

    #-------#
    # Data  #
    #-------#
    # if binned regions are used they should come from a TTree -> useDataSample=True

    print "- Defining data samples.."

    if useDataSample:
        dataSample = configWriter.Sample("data_nom", ROOT.kBlack)
        dataSample.setData()
        dataSample.setFileList(inputFileDict['data'])

    # use hard-coded data
    else:
        dataHand=configWriter.Sample("Data", ROOT.kYellow)
        dataHand.setData()

        for srname,config in dataCounts.iteritems():
            if (srname in signalRegionList) or (srname in controlRegionList) or (srname in validationRegionList):

                variable = "cuts"
                if srname in signalRegionList: variable = binnedFitSR[srname]
                if srname in controlRegionList: variable = binnedFitCR[srname]
                if srname in validationRegionList: variable = binnedFitVR[srname]

                temp_binning = binning[srname][variable]

                for var,values in config.iteritems():
    
                    if ( (srname in signalRegionList) or (srname in controlRegionList) or (srname in validationRegionList)) and var==variable: 
                        dataHand.buildHisto(dataCounts[srname][variable],srname,var,temp_binning[1],(temp_binning[2]-temp_binning[1])/float(temp_binning[0]))
                    if srname in validationRegionList: dataHand.buildHisto(dataCounts[srname]["cuts"],srname,var)


    #This dict will contain all the MC samples, including signal
    backgroundDict = {}

    if len(signalRegionList)==1:
        my_mu_SIG = "mu_"+signalRegionList[0]
    else:
        my_mu_SIG = "mu_SIG"

    if len(list(sigSample.split("_")))>0: # the input signal format is: signalDSID_X_Y_Z...
        signalName=str(sigSample).split('_')[0]
    else: # the input signal format is: signalDSID
        signalName=str(sigSample)

  


    #----------#
    #  Signal  #
    #----------#
    # signal sample is added just to exclusion fit
    # (ideally it should be added later, but doing here for practical reasons since all MC systematics will be added  just after)
    if myFitType==FitType.Exclusion:
        print "- Defining signal sample in exclusion fit: ",signalName       
        backgroundDict[signalName] = configWriter.Sample(str(sigSample), ROOT.kPink)
        backgroundDict[signalName].addInputs(inputFileDict['signal'])
        backgroundDict[signalName].setNormByTheory() # assigns lumi uncertainty
        backgroundDict[signalName].setNormFactor(my_mu_SIG, 1., 0., 10)           
        backgroundDict[signalName].setStatConfig(True)  # all stat errors treated as one in the fit (it includes signal if provided)

    #-----------#
    #  MC Bkgs  # (as data-driven are hard-coded, and sometimes they can be binned, they are added later for every region)
    #-----------#
    for i in range(len(bkgList)):

        if bkgList[i].getSampleType()==sampleType.BKG:

            if bkgList[i].getMC()==True: 
                print '- Defining bkg MC sample: ',bkgList[i].getName()

                backgroundDict[bkgList[i].getName()] = configWriter.Sample(bkgList[i].getName(), bkgList[i].getColor())
                backgroundDict[bkgList[i].getName()].addInputs(inputFileDict[bkgList[i].getName()])
                backgroundDict[bkgList[i].getName()].setStatConfig(True) # all stat errors treated as one in the fit (it includes signal if provided)


                if bkgList[i].getName() in extraSampleWeight:  #adding additional weight for each sample
                    backgroundDict[bkgList[i].getName()].addSampleSpecificWeight(extraSampleWeight[bkgList[i].getName()])

                if bkgList[i].getName() in NF:  #adding SF for each sample
                    backgroundDict[bkgList[i].getName()].addSampleSpecificWeight(str(NF_dict[bkgList[i].getName()][0])) #getting nominal=0; syst_up=1; syst_down=2

                if len(controlRegionList)==0: backgroundDict[bkgList[i].getName()].setNormByTheory(True) # assigns lumi uncertainty 
                else:
                    if bkgList[i].getName() not in bkgNorm: backgroundDict[bkgList[i].getName()].setNormByTheory(True) # assigns lumi uncertainty
                    else:
                        print "-- This bkg will be normalized in the fit... Lumi uncertainty therefore will not be assigned"
                        normRegions=[]
                        normRegions.append((bkgNorm[bkgList[i].getName()],binnedFitCR[bkgNorm[bkgList[i].getName()]])) # shuhui: fix a typo binning->binned

                        backgroundDict[bkgList[i].getName()].setNormFactor("mu_"+bkgList[i].getName(),1.,0.,5.)
                        backgroundDict[bkgList[i].getName()].setNormRegions(normRegions)    

    

    ### fast check to see if sample provided for NF exist in added background
    for sam in NF:
        if sam not in backgroundDict:
             print "- The sample with NF have not been added to the fit: ",sam
             sys.exit("--> Aborting!")

    #-------------------------------------------------------------#
    #     Adding systematics to all MC samples: signal  and bkg   #    
    #-------------------------------------------------------------

    #KINEMATIC SYSTEMATICS
    treeDict = GetTreeSystematics()

    #WEIGHT SYSTEMATICS
    weightDict = GetWeightSystematics(str(sigSample))


    for background in backgroundDict:
        
        # these systematics are not assigned for datadriven bkgs
        if background not in allBkg.getDataDrivenBkgNames():
            # weight-based systematics
            for sysName,sysConfig in weightDict.iteritems():
                # exclude PU syst for signal
                if (not 'BKG' in sysName) and (not 'SIG' in sysName):
                    backgroundDict[background].addSystematic(Systematic(sysName, configMgr.weights, sysConfig[0], sysConfig[1], "weight", sysConfig[2]))
                else:
                    if ('BKG' in sysName) and (not 'signal' in background):
                        backgroundDict[background].addSystematic(Systematic(sysName, configMgr.weights, sysConfig[0], sysConfig[1], "weight", sysConfig[2]))
            # tree-based systematics 
            for sysName,sysConfig in treeDict.iteritems():

                backgroundDict[background].addSystematic(Systematic(sysName,"_nom","_"+sysConfig[0],"_"+sysConfig[1],"tree", sysConfig[2]))

            # flat systematic is required 
            if flat is not 0: 
                backgroundDict[background].addSystematic(Systematic("FlatSyst_"+background,"1.", 1+flat, 1-flat, "user","userOverallSys"))
    
            # systematic on NF is required     
            if background  in NF:   #NF_dict['bkg'] = [nom,relative_up,relative_down]
                backgroundDict[background].addSystematic(Systematic("NF_"+background,'1.0', 1+NF_dict[background][1], 1-NF_dict[background][2], "user","userOverallSys")) 

    #------------------#
    # Build fit config #
    #------------------#


    print "##****** Preparing fit configuration **********##"
    if myFitType==FitType.Exclusion:   #change fit name based on signal points (valid just for exclusion fit)       
        grid = options.signalGridName
        signalRunnumberToMassesDict = signalSameSignTools.getRunnumberMassesDictSS(grid, options.SigNameSchema)
        if sigSample.strip('signal') in signalRunnumberToMassesDict:
            masses = signalRunnumberToMassesDict[sigSample.strip('signal')]
            fcName=fcName+'_{0}_{1}'.format(masses[0],masses[1])


        
            
    print "Setting fcName to",fcName,"sigSample is",sigSample
    myFitConfig = configMgr.addFitConfig(fcName)

    myFitConfig.statErrThreshold = 0.00001  #None

    measurement = myFitConfig.addMeasurement(name = "NormalMeasurement", lumi=1.0, lumiErr=0.017) #0.017


    # add data to fitConfiguration
    
    print '## Adding data to fitConfiguration...'
    if useDataSample: myFitConfig.addSamples(dataSample)
    else: myFitConfig.addSamples(dataHand)
   

    #if myFitType!=FitType.Discovery:  #for discovery the parameter name is different, i.e. mu_disc... (these lines can be easily ignored)
    measurement.addPOI(my_mu_SIG) #it must be added even if fit is bkg-only


    # add MC bkgs and signals
    print "## Adding signal and MC background to fitConfiguration"
    for background in backgroundDict:
        print "-",background
        myFitConfig.addSamples(backgroundDict[background]) # this includes signal for exclusion fits

    # say to myFitConfig which one is the signal sample (valid just for exclusion fit)
    if myFitType==FitType.Exclusion:          
        myFitConfig.setSignalSample(backgroundDict[signalName])
        # these must be the same, or CombineWorkSpaces will complain later due to a badly thought ReplaceAll...
        # if the input signalName has NO masses, like signal123456. masses must be added to the jsons downstream by a separate python script
        # if the input got masses, like signalDSID_SP_LSP. The masses also need to be added later on
        myFitConfig.hypoTestName = str(sigSample)

        
    #----------------#
    # Build channels #
    #----------------#

    #-------------------#
    # Adding CRs to fit # --> just for those CRs explicitelly provided in the command line
    #-------------------#

    controlRegionChannels=[]
    for controlRegionName in controlRegionList:
        print "- Adding CR :",controlRegionName

        variable = binnedFitCR[controlRegionName]
        binningCR = binning[controlRegionName][variable]

        cChan = myFitConfig.addChannel(variable, [controlRegionName],binningCR[0],binningCR[1],binningCR[2]);
        cChan.useOverflowBin=True
        cChan.useUnderflowBin=True

        # Adding data-driven samples for this channel
        for bkg in dataDrivenList:
            print "- Adding data-driven samples for channel : ",bkg.getName()

            dataDrivenSample=createDataDrivenSample(bkg,controlRegionName,variable,binningCR[0],binningCR[1],binningCR[2])

            cChan.addSample(dataDrivenSample)


        if 'TH' in systematicList: addSRTheorySyst(cChan,controlRegionName)
        controlRegionChannels.append(cChan)


    if len(controlRegionChannels)>0:
        myFitConfig.addBkgConstrainChannels(controlRegionChannels)
        print "## Control regions explicitelly provided have been added :",controlRegionChannels
    else:
        print "## This setup does not have control regions 'explicitely defined' in the command line..."


    #-------------------#
    # Adding VRs to fit #
    #-------------------#
    # if fit is bkg-only and there are CRs defined, then the  SRs are provided will be used as VRs
    validationRegionChannels=[]
    for validationRegionName in validationRegionList:
        legendTitle = ''
        print "- Adding VR :",validationRegionName

        vChan = myFitConfig.addChannel("cuts", [validationRegionName],  1,0.5,1.5)
        vChan.title = '{0} Region'.format(validationRegionName)

     
        # Adding data-driven samples for this channel
        for bkg in dataDrivenList:
            print "- Adding data-driven samples for channel : ",bkg.getName()
            

            dataDrivenSample=createDataDrivenSample(bkg,validationRegionName)
            vChan.addSample(dataDrivenSample)

        if 'TH' in systematicList: addSRTheorySyst(vChan,validationRegionName)
        validationRegionChannels.append(vChan)


    if len(validationRegionChannels)>0: 
        myFitConfig.addValidationChannels(validationRegionChannels)
        print "## The following validation regions have been added: ",validationRegionList
    else: print "## This configuration does not have validation regions..."

    #-------------------#
    # Adding SRs to fit #
    #-------------------#
    # Be careful, if fit is bkg-only then SRs will be configured here as CRs...

    for signalRegionName in signalRegionList:
        print "-- Adding SR: ",signalRegionName
        cutname=signalRegionName

        variable = binnedFitSR[cutname]
        binningSR = binning[cutname][variable]

        sChan = myFitConfig.addChannel(variable, [cutname], binningSR[0],binningSR[1],binningSR[2])
        if binningSR[0] != 1: sChan.useOverflowBin = True

        if myFitType==FitType.Discovery:
            print "--Adding discovery dummy sample..."
            sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
            sChan.getSample('DiscoveryMode_'+cutname).setNormFactor(my_mu_SIG, 1., 0., 100)
            #measurement.addPOI(my_mu_SIG)

        # Adding data-driven samples for this channel
        for bkg in dataDrivenList:
            print "- Adding data-driven samples for channel : ",bkg.getName()
        
            dataDrivenSample=createDataDrivenSample(bkg,cutname,variable,binningSR[0],binningSR[1],binningSR[2])
            sChan.addSample(dataDrivenSample)


        if 'TH' in systematicList: addSRTheorySyst(sChan,cutname)

        if myFitType!=FitType.Background: myFitConfig.setSignalChannels(sChan)
        else:
            print "-- As fit is bkg-only, the SR will be used as CR..."
            myFitConfig.addBkgConstrainChannels(sChan)

        sChan.logY = False

              
      

            
    #--------------------------#
    #  Setting Style for plots #
    #--------------------------#
        
    # Set global plotting colors/styles
    myFitConfig.dataColor = ROOT.kBlack
    myFitConfig.totalPdfColor = ROOT.kBlack
    myFitConfig.errorFillColor = ROOT.kBlack
    myFitConfig.errorFillStyle = 3004
    #  myFitConfig.errorFillStyle = 3353
    myFitConfig.errorLineStyle = ROOT.kDashed
    myFitConfig.errorLineColor = ROOT.kBlack
    myFitConfig.ShowLumi = True;
    
    c = ROOT.TCanvas()
    compFillStyle = 1001 # see ROOT for Fill styles
    leg = ROOT.TLegend(0.6, 0.48, 0.881, 0.87, "")
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextSize(0.035)
    leg.SetTextFont(42)

    entry = ROOT.TLegendEntry()
    if configMgr.blindVR or configMgr.blindSR:
        entry = leg.AddEntry("","Data (%.1f fb^{-1}, #sqrt{s}=13 TeV)"%configMgr.outputLumi,"p") 
    else:
        entry = leg.AddEntry("","Data", "p") 
    entry.SetMarkerColor(myFitConfig.dataColor)
    entry.SetMarkerStyle(20)


    for i in range(len(bkgList)):

        type_of_sample=bkgList[i].getSampleType()

        if type_of_sample==sampleType.BKG:

            entry=leg.AddEntry("",bkgList[i].getLegendName(),"f")
            entry.SetLineColor(ROOT.kBlack)
            entry.SetLineWidth(1)
            entry.SetFillColor(bkgList[i].getColor())
            entry.SetFillStyle(compFillStyle)




    if myFitConfig.signalSample and not myFitConfig.signalSample.startswith("Discovery"):
        if myFitConfig.signalSample=="signal156548":
            sigName="gtt, (gl, #chi^{0}_{1}) = (1000, 1) GeV"
        elif myFitConfig.signalSample=="signal173836":
            sigName="2-steps via slepton, (gl, #chi^{0}_{1}) = (1145, 425) GeV"
        elif myFitConfig.signalSample=="signal172181":
            sigName="sb->top chargino, (sb, #chi^{#pm}_{1}) = (500, 150) GeV"
        elif  myFitConfig.signalSample=="signal148208":
            sigName="1-step x1/2, (#tilde{g}, #chi^{0}_{1}) = (585, 345) GeV"
        elif  myFitConfig.signalSample=="signal177352":
            sigName="#tilde{g} -> #tilde{t} c, (#tilde{g}, #tilde{t}) = (700, 400) GeV"
        elif  myFitConfig.signalSample=="signal174344":
            sigName="#tilde{g} -> #tilde{t} t, (#tilde{g}, #tilde{t}) = (945, 417) GeV"
        elif  myFitConfig.signalSample=="signal173789":
            sigName="2-step via sleptons, (#tilde{g}, #chi^{0}_{1}) = (825, 405) GeV"
        elif  myFitConfig.signalSample=="signal172175":
            sigName="#tilde{b} -> t #chi^{#pm}_{1}, N60, (#tilde{g}, #chi^{#pm}_{1}) = (450, 200) GeV"

        else:
            sigName=myFitConfig.signalSample

        entry = leg.AddEntry("",sigName,"lf")
        sigColor=myFitConfig.getSample(myFitConfig.signalSample).color
        entry.SetLineColor(sigColor)
        entry.SetFillColor(sigColor)
        entry.SetFillStyle(compFillStyle)

    
    myFitConfig.tLegend = leg
    c.Close()
    return


def createDataDrivenSample(bkg,region,var="cuts",nbins=1,low=0.5,up=1.5):

    dataDriven_sample = configWriter.Sample(bkg.getName(), bkg.getColor())


    if bkg.getYields(region,var) == -1:
        print "This sample does exist in dictionary, will set it to 0..."
        yields = [0]*nbins
        stat = [0]*nbins
    else:
        yields = bkg.getYields(region,var)
        stat = bkg.getStatUnc(region,var)

    print yields


    dataDriven_sample.buildHisto(yields,region,var,low,(up-low)/float(nbins));
    dataDriven_sample.buildStatErrors(stat,region,var)
    dataDriven_sample.setStatConfig(False)

    #Systematic from data-driven will affect only the normalization of the samples (this is temporal)
    if bkg.getDataDrivenSystematicUp(region) and bkg.getDataDrivenSystematicDown(region):
        print "Adding systematics for this sample..."
        systDataDriven=Systematic("syst_"+bkg.getName()+"_"+region, "1.", 1+bkg.getDataDrivenSystematicUp(region)["cuts"][0],1-bkg.getDataDrivenSystematicDown(region)["cuts"][0], "user","userOverallSys")

        dataDriven_sample.addSystematic(systDataDriven)
    else:
        print "Systematic for this sample has not been assigned..."


    return dataDriven_sample

def replaceElementList(inlist,old,new):

    outList=copy.deepcopy(inlist)

    if old in inlist:
        index = inlist.index(old)
        outList[index] = new

    return outList

def replaceStringInTuple(inTuple, oldString, newString):
    outTuple = ()
    for entry in inTuple:
        if not entry == oldString:
            outTuple += (entry,)
        else: outTuple += (newString,)
    return outTuple

def removeStringFromTuple(inTuple,removeString):
    outTuple = ()
    for entry in inTuple:
        if not entry == removeString:
            outTuple += (entry,)
    return outTuple


# this is to add SR-specific theory uncertainties
def  addSRTheorySyst(sChan,cutname):

    sourceList = ['muRmuF','muR','muF','PdfAlpha','QSF','CKKW','CSSKIN','PartonShower','HardScatter','Radiation','Scale','Xsec']
    for i in range(len(bkgList)):

        if bkgList[i].getSampleType()==sampleType.BKG:

            if bkgList[i].getMC()==True:

                if sChan.hasSample(bkgList[i].getName()):

                    if sChan.channelName.split("_")[0] in ["VRTTV1b6j","VRTTV6j","VRTTV2b","VRTTW1b","VRTTZ","VRWW","VRWZ2j1b","VRWZge4j"]: 
                        # Add 30% theory syst to extra VRs
                        print "--> Adding theory syst to",bkgList[i].getName()
                        systTemp=Systematic("theoryUncert_"+bkgList[i].getName(), "1.", 1.0+0.3,1.0-0.3, "user","userOverallSys")
                        sChan.getSample(bkgList[i].getName()).addSystematic(systTemp)

                    else: # Add theory syst to CR/SRs and nominal VRs
                        for SysSrc in sourceList:

                            if bkgList[i].getName()=='OtherMultiboson':

                                sysname = 'WWSS'+SysSrc ### WW DSID list: 364286, 364287
                                if 'thUnc_'+sysname+'Up' in theorySyst and 'thUnc_'+sysname+'Down' in theorySyst: # shuhui: check if sysname exits in theory uncertainty json
                                    print "--> Adding thUnc_"+sysname
                                    sChan.getSample(bkgList[i].getName()).addSystematic(Systematic('theoryUncert_'+sysname, configMgr.weights, configMgr.weights+['('+str(1.0+(float(theorySyst['thUnc_'+sysname+'Up'][cutname])))+'*(MCId==364287 || MCId==364286)+1.0*(MCId!=364287 && MCId!=364286))'],configMgr.weights+['('+str(1.0-(float(theorySyst['thUnc_'+sysname+'Down'][cutname])))+'*(MCId==364287 || MCId==364286)+1.0*(MCId!=364287 && MCId!=364286))'], "weight","overallSys"))                            

                                if SysSrc=='Xsec': # Add Xsec unc  to remaining samples in OtherMultiboson
                                    sysname2 = bkgList[i].getName()+SysSrc 
                                    if 'thUnc_'+sysname2+'Up' in theorySyst and 'thUnc_'+sysname2+'Down' in theorySyst: # shuhui: check if sysname exits in theory uncertainty json
                                        print "--> Adding thUnc_"+sysname2
                                        sChan.getSample(bkgList[i].getName()).addSystematic(Systematic('theoryUncert_'+sysname2+'noWWSS', configMgr.weights, configMgr.weights+['('+str(1.0+(float(theorySyst['thUnc_'+sysname2+'Up'][cutname])))+'*(MCId!=364287 && MCId!=364286)+1.0*(MCId==364287 || MCId==364286))'],configMgr.weights+['('+str(1.0-(float(theorySyst['thUnc_'+sysname2+'Down'][cutname])))+'*(MCId!=364287 && MCId!=364286)+1.0*(MCId==364287 || MCId==364286))'], "weight","overallSys"))

                            elif bkgList[i].getName()=='SM4tops':
#                                print "--> Adding theory syst to",bkgList[i].getName()
                                sysname = 'FourTop'+SysSrc ### 4tops DSID:412043
                                if 'thUnc_'+sysname+'Up' in theorySyst and 'thUnc_'+sysname+'Down' in theorySyst: # shuhui: check if sysname exits in theory uncertainty json
                                    print "--> Adding thUnc_"+sysname
                                    sChan.getSample(bkgList[i].getName()).addSystematic(Systematic('theoryUncert_'+sysname, configMgr.weights, configMgr.weights+['('+str(1.0+(float(theorySyst['thUnc_'+sysname+'Up'][cutname])))+'*(MCId==412043)+1.0*(MCId!=412043))'],configMgr.weights+['('+str(1.0-(float(theorySyst['thUnc_'+sysname+'Down'][cutname])))+'*(MCId==412043)+1.0*(MCId!=412043))'], "weight","overallSys"))                                    

                            elif bkgList[i].getName()=='Multitop':
                                if SysSrc=='Xsec': # Xsec unc 
                                    sysname2 = bkgList[i].getName()+SysSrc ### Add Xsec unc to remaining samples in Multitop
                                    if 'thUnc_'+sysname2+'Up' in theorySyst and 'thUnc_'+sysname2+'Down' in theorySyst: # shuhui: check if sysname exits in theory uncertainty json
                                        print "--> Adding thUnc_"+sysname2
                                        sChan.getSample(bkgList[i].getName()).addSystematic(Systematic('theoryUncert_'+sysname2+'no4tops', "1.", 1.0+(float(theorySyst['thUnc_'+sysname2+'Up'][cutname])),1.0-(float(theorySyst['thUnc_'+sysname2+'Down'][cutname])), "user","overallSys"))                                                                

                            elif bkgList[i].getName()=='ttW':
                                #print "--> Adding theory syst to ",bkgList[i].getName()
                                sysname = bkgList[i].getName()+SysSrc
                                if 'thUnc_'+sysname+'Up' in theorySyst and 'thUnc_'+sysname+'Down' in theorySyst: # shuhui: check if sysname exits in theory uncertainty json
                                    print "--> Adding thUnc_"+sysname
                                    systTemp=Systematic("theoryUncert_"+sysname, "1.", 1.0+(float(theorySyst['thUnc_'+sysname+'Up'][cutname])),1.0-(float(theorySyst['thUnc_'+sysname+'Down'][cutname])), "user","userOverallSys")
                                    sChan.getSample(bkgList[i].getName()).addSystematic(systTemp)
                                
                                if SysSrc=='Xsec': ### Add 50% flavour uncertianties to >=3b events
                                    sChan.getSample(bkgList[i].getName()).addSystematic(Systematic('theoryUncert_'+bkgList[i].getName()+'Flavour', configMgr.weights, configMgr.weights+['(1.5*(nBJets20>=3)+1.0*(nBJets20<3))'],configMgr.weights+['(0.5*(nBJets20>=3)+1.0*(nBJets20<3))'], "weight","overallSys"))                                                                

                            else:
                                #print "--> Adding theory syst to ",bkgList[i].getName()
                                sysname = bkgList[i].getName()+SysSrc
                                if 'thUnc_'+sysname+'Up' in theorySyst and 'thUnc_'+sysname+'Down' in theorySyst: # shuhui: check if sysname exits in theory uncertainty json
                                    print "--> Adding thUnc_"+sysname
                                    systTemp=Systematic("theoryUncert_"+sysname, "1.", 1.0+(float(theorySyst['thUnc_'+sysname+'Up'][cutname])),1.0-(float(theorySyst['thUnc_'+sysname+'Down'][cutname])), "user","userOverallSys")
                                    sChan.getSample(bkgList[i].getName()).addSystematic(systTemp)


    # shuhui: add theory uncertainties on signal samples
    if len(sigList)>0 and 'bkgOnly' not in sigList:
        for j in range(len(sigList)): # shuhui: add theory uncertainties on signal samples
            print "--> Adding signal theory syst to ",sigList[j]
            systTemp=Systematic("theoryUncert_signal", "1.", 1.0+(float(theorySyst['thUnc_signalUp'][cutname])),1.0-(float(theorySyst['thUnc_signalDown'][cutname])), "user","userOverallSys")
            sChan.getSample(sigList[j]).addSystematic(systTemp)


def GetTreeSystematics():

    treeDict={}

    if 'EG' in systematicList:
        print "Adding EG tree syst"
        treeDict.update({
                'EG_Scale_ALL':('EG_SCALE_ALL__1up',"EG_SCALE_ALL__1down","histoSys"),
                'EG_Scale_AF2':('EG_SCALE_AF2__1up',"EG_SCALE_AF2__1down","histoSys"),
                'EG_Resolution':("EG_RESOLUTION_ALL__1up","EG_RESOLUTION_ALL__1down","histoSys")})

    if 'JET' in systematicList:
        print "Adding JET tree syst"
        treeDict.update({
                'JET_EtaIntercalibration_Modelling':("JET_EtaIntercalibration_Modelling__1up","JET_EtaIntercalibration_Modelling__1down","histoSys"),
                'JET_EtaIntercalibration_NonClosure_2018data':("JET_EtaIntercalibration_NonClosure_2018data__1up","JET_EtaIntercalibration_NonClosure_2018data__1down","histoSys"),
                'JET_EtaIntercalibration_NonClosure_highE':("JET_EtaIntercalibration_NonClosure_highE__1up","JET_EtaIntercalibration_NonClosure_highE__1down","histoSys"),
                'JET_EtaIntercalibration_NonClosure_negEta':("JET_EtaIntercalibration_NonClosure_negEta__1up","JET_EtaIntercalibration_NonClosure_negEta__1down","histoSys"),
                'JET_EtaIntercalibration_NonClosure_posEta':("JET_EtaIntercalibration_NonClosure_posEta__1up","JET_EtaIntercalibration_NonClosure_posEta__1down","histoSys"),
                'JET_EtaIntercalibration_TotalStat':("JET_EtaIntercalibration_TotalStat__1up","JET_EtaIntercalibration_TotalStat__1down","histoSys"),
                'JET_Flavor_Composition':("JET_Flavor_Composition__1up","JET_Flavor_Composition__1down","histoSys"),
                'JET_Flavor_Response':("JET_Flavor_Response__1up","JET_Flavor_Response__1down","histoSys"),
                #'JET_PunchThrough_MC16': ("JET_PunchThrough_MC16__1up", "JET_PunchThrough_MC16__1down","histoSys"),
                'JET_RelativeNonClosure_AFII': ("JET_RelativeNonClosure_AFII__1up", "JET_RelativeNonClosure_AFII__1down","histoSys"),
                'JET_BJES_Response':("JET_BJES_Response__1up","JET_BJES_Response__1down","histoSys"),
                'JET_EffectiveNP_Detector1':("JET_EffectiveNP_Detector1__1up","JET_EffectiveNP_Detector1__1down","histoSys"),
                'JET_EffectiveNP_Detector2':("JET_EffectiveNP_Detector2__1up","JET_EffectiveNP_Detector2__1down","histoSys"),
                'JET_EffectiveNP_Mixed1':("JET_EffectiveNP_Mixed1__1up","JET_EffectiveNP_Mixed1__1down","histoSys"),
                'JET_EffectiveNP_Mixed2':("JET_EffectiveNP_Mixed2__1up","JET_EffectiveNP_Mixed2__1down","histoSys"),
                'JET_EffectiveNP_Mixed3':("JET_EffectiveNP_Mixed3__1up","JET_EffectiveNP_Mixed3__1down","histoSys"),
                'JET_EffectiveNP_Modelling1':("JET_EffectiveNP_Modelling1__1up","JET_EffectiveNP_Modelling1__1down","histoSys"),
                'JET_EffectiveNP_Modelling2':("JET_EffectiveNP_Modelling2__1up","JET_EffectiveNP_Modelling2__1down","histoSys"),
                'JET_EffectiveNP_Modelling3':("JET_EffectiveNP_Modelling3__1up","JET_EffectiveNP_Modelling3__1down","histoSys"),
                'JET_EffectiveNP_Modelling4':("JET_EffectiveNP_Modelling4__1up","JET_EffectiveNP_Modelling4__1down","histoSys"),
                'JET_EffectiveNP_Statistical1':("JET_EffectiveNP_Statistical1__1up","JET_EffectiveNP_Statistical1__1down","histoSys"),
                'JET_EffectiveNP_Statistical2':("JET_EffectiveNP_Statistical2__1up","JET_EffectiveNP_Statistical2__1down","histoSys"),
                'JET_EffectiveNP_Statistical3':("JET_EffectiveNP_Statistical3__1up","JET_EffectiveNP_Statistical3__1down","histoSys"),
                'JET_EffectiveNP_Statistical4':("JET_EffectiveNP_Statistical4__1up","JET_EffectiveNP_Statistical4__1down","histoSys"),
                'JET_EffectiveNP_Statistical5':("JET_EffectiveNP_Statistical5__1up","JET_EffectiveNP_Statistical5__1down","histoSys"),
                'JET_EffectiveNP_Statistical6':("JET_EffectiveNP_Statistical6__1up","JET_EffectiveNP_Statistical6__1down","histoSys"),
                'JET_JER_DataVsMC_AFII':("JET_JER_DataVsMC_AFII__1up","JET_JER_DataVsMC_AFII__1down","histoSys"),
                'JET_JER_DataVsMC_MC16':("JET_JER_DataVsMC_MC16__1up","JET_JER_DataVsMC_MC16__1down","histoSys"),
                'JET_JER_EffectiveNP_1':('JET_JER_EffectiveNP_1__1up','JET_JER_EffectiveNP_1__1down',"histoSys"),
                'JET_JER_EffectiveNP_2':('JET_JER_EffectiveNP_2__1up','JET_JER_EffectiveNP_2__1down',"histoSys"),
                'JET_JER_EffectiveNP_3':('JET_JER_EffectiveNP_3__1up','JET_JER_EffectiveNP_3__1down',"histoSys"),
                'JET_JER_EffectiveNP_4':('JET_JER_EffectiveNP_4__1up','JET_JER_EffectiveNP_4__1down',"histoSys"),
                'JET_JER_EffectiveNP_5':('JET_JER_EffectiveNP_5__1up','JET_JER_EffectiveNP_5__1down',"histoSys"),
                'JET_JER_EffectiveNP_6':('JET_JER_EffectiveNP_6__1up','JET_JER_EffectiveNP_6__1down',"histoSys"),
                'JET_JER_EffectiveNP_7restTerm':('JET_JER_EffectiveNP_7restTerm__1up','JET_JER_EffectiveNP_7restTerm__1down',"histoSys"),
                'JET_SingleParticle_HighPt': ("JET_SingleParticle_HighPt__1up", "JET_SingleParticle_HighPt__1down","histoSys"),
                'JET_Pileup_OffsetMu': ("JET_Pileup_OffsetMu__1up", "JET_Pileup_OffsetMu__1down","histoSys"),
                'JET_Pileup_OffsetNPV': ("JET_Pileup_OffsetNPV__1up", "JET_Pileup_OffsetNPV__1down","histoSys"),
                'JET_Pileup_PtTerm': ("JET_Pileup_PtTerm__1up", "JET_Pileup_PtTerm__1down","histoSys"),
                'JET_Pileup_RhoTopology': ("JET_Pileup_RhoTopology__1up", "JET_Pileup_RhoTopology__1down","histoSys")
                })

    if "MU" in systematicList:
        print "Adding MU tree syst"
        treeDict.update({
                'Mu_ID':("MUON_ID__1up","MUON_ID__1down","histoSys"),
                'Mu_MS':("MUON_MS__1up","MUON_MS__1down","histoSys"),
                'Mu_Sagitta_Res': ("MUON_SAGITTA_RESBIAS__1up","MUON_SAGITTA_RESBIAS__1down","histoSys"),
                #'Mu_Sagitta_Rho': ("MUON_SAGITTA_RHO__1up","MUON_SAGITTA_RHO__1down","histoSys"),
                'Mu_Scale':( "MUON_SCALE__1up","MUON_SCALE__1down","histoSys")})
    if 'MET' in systematicList:
        print "Adding MET tree syst"
        treeDict.update({
                'MET_Soft_reso_Para':("MET_SoftTrk_ResoPara","nom","histoSysOneSideSym"),
                'MET_Soft_reso_Perp':("MET_SoftTrk_ResoPerp","nom","histoSysOneSideSym"),
                'MET_Soft_Scale':("MET_SoftTrk_Scale__1up","MET_SoftTrk_Scale__1down","histoSys")})



    return treeDict

def GetWeightSystematics(signalName=''):

    #---------
    # weights 
    #---------

    #nomWeight = ["wmu_nom","wel_nom","wtrig_nom","wjet_nom","mcweight","wpu_nom_bkg","wpu_nom_sig","MC_campaign_weight","lumiScaling"]
    #nomWeight =  ["totweight","lumiScaling"] 
    nomWeight = ["wmu_nom","wel_nom","wtrig_nom","wjet_nom","mcweight","wpu_nom","mccampaignweight","lumiScaling"] # shuhui: for new HF trees

    #N.B. lumiScaling has to be set to UP,DOWN and nominal in the correct position!!!
    # this takes care of the signal theory unc
    if options.theoryUncertMode.lower() == 'up':
        configMgr.weights = replaceElementList(nomWeight,"lumiScaling","lumiScaling_up")
    elif options.theoryUncertMode.lower() == 'down':
        configMgr.weights = replaceElementList(nomWeight,"lumiScaling","lumiScaling_down")
    else:
        configMgr.weights = nomWeight

        if options.signalGridName == 'Mc16SusyC1N2N1_GGMHinoZh':
            if myFitType==FitType.Exclusion:
                signalRunnumberToMassesDict = signalSameSignTools.getRunnumberMassesDictSS(options.signalGridName, options.SigNameSchema)
                if signalName.strip('signal') in signalRunnumberToMassesDict:
                    masses = signalRunnumberToMassesDict[signalName.strip('signal')]
                    if int(masses[1]) != 50:
                        configMgr.weights = configMgr.weights + ["GGM_BR{0}Weight".format(int(masses[1]))]
                        print "- Extra weights are used: GGM_BR{0}Weight".format(int(masses[1]))

        '''
        if options.signalGridName == 'Mc16SusyC1N2N1_GGMHinoZh':
            if myFitType==FitType.Exclusion:
                signalRunnumberToMassesDict = signalSameSignTools.getRunnumberMassesDictSS(options.signalGridName, options.SigNameSchema)
                if signalName.strip('signal') in signalRunnumberToMassesDict:
                    masses = signalRunnumberToMassesDict[signalName.strip('signal')]
                    if int(masses[1]) != 50:
                        configMgr.weights = ["lumiScaling", "totweight", "GGM_BR{0}Weight".format(int(masses[1]))]
                        print "- Extra weights are used: GGM_BR{0}Weight".format(int(masses[1]))
                    else:
                        configMgr.weights = ["lumiScaling", "totweight"]
                else:
                    configMgr.weights = ["lumiScaling", "totweight"]
            else:
                configMgr.weights = ["lumiScaling", "totweight"]
        else:
            configMgr.weights = ["lumiScaling", "totweight"]
#        configMgr.weights = ["wmu_nom","wel_nom","wtrig_nom","wjet_nom","mcweight","wpu_nom_bkg","wpu_nom_sig","MC_campaign_weight", "lumiScaling"]
        '''

    
    # configure the rest of the weight-based systematics (muon, electrons, jets)
    muon_bad_sys_UpWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_bad_sys_up")
    muon_bad_sys_DownWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_bad_sys_down")
    muon_stat_UpWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_stat_up")
    muon_stat_DownWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_stat_down")
    muon_sys_UpWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_sys_up")
    muon_sys_DownWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_sys_down")
    muon_stat_lowpt_UpWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_stat_lowpt_up")
    muon_stat_lowpt_DownWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_stat_lowpt_down")
    muon_sys_lowpt_UpWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_sys_lowpt_up")
    muon_sys_lowpt_DownWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_sys_lowpt_down")
    muon_iso_stat_UpWeights =  replaceElementList(configMgr.weights, "wmu_nom", "wmu_iso_stat_up")
    muon_iso_stat_DownWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_iso_stat_down")
    muon_iso_sys_UpWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_iso_sys_up")
    muon_iso_sys_DownWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_iso_sys_down")
    muon_ttva_stat_UpWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_ttva_stat_up")
    muon_ttva_stat_DownWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_ttva_stat_down")
    muon_ttva_sys_UpWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_ttva_sys_up")
    muon_ttva_sys_DownWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_ttva_sys_down")

    muon_trig_stat_UpWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_trig_stat_up")
    muon_trig_stat_DownWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_trig_stat_down")
    muon_trig_sys_UpWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_trig_sys_up")
    muon_trig_sys_DownWeights = replaceElementList(configMgr.weights, "wmu_nom", "wmu_trig_sys_down")
    
    el_cf_UpWeights = replaceElementList(configMgr.weights, "wel_nom", "wchflip_up")
    el_cf_DownWeights = replaceElementList(configMgr.weights, "wel_nom", "wchflip_down")
    el_id_UpWeights = replaceElementList(configMgr.weights, "wel_nom", "wel_id_up")
    el_id_DownWeights = replaceElementList(configMgr.weights, "wel_nom", "wel_id_down")
    el_iso_UpWeights = replaceElementList(configMgr.weights, "wel_nom", "wel_iso_up")
    el_iso_DownWeights = replaceElementList(configMgr.weights, "wel_nom", "wel_iso_down")
    el_reco_UpWeights = replaceElementList(configMgr.weights, "wel_nom", "wel_reco_up")
    el_reco_DownWeights = replaceElementList(configMgr.weights, "wel_nom", "wel_reco_down")

    el_trig_UpWeights = replaceElementList(configMgr.weights, "wel_nom", "wel_trig_up")
    el_trig_DownWeights = replaceElementList(configMgr.weights, "wel_nom", "wel_trig_down")
    el_trigEff_UpWeights = replaceElementList(configMgr.weights, "wel_nom", "wel_trigEff_up")
    el_trigEff_DownWeights = replaceElementList(configMgr.weights, "wel_nom", "wel_trigEff_down")

    jet_b_UpWeights = replaceElementList(configMgr.weights, "wjet_nom", "wjet_b_up")
    jet_b_DownWeights = replaceElementList(configMgr.weights, "wjet_nom", "wjet_b_down")
    jet_c_UpWeights = replaceElementList(configMgr.weights, "wjet_nom", "wjet_c_up")
    jet_c_DownWeights = replaceElementList(configMgr.weights, "wjet_nom", "wjet_c_down")
    jet_light_UpWeights = replaceElementList(configMgr.weights, "wjet_nom", "wjet_light_up")
    jet_light_DownWeights = replaceElementList(configMgr.weights, "wjet_nom", "wjet_light_down")

    jet_extra1_UpWeights = replaceElementList(configMgr.weights, "wjet_nom", "wjet_extra1_up")
    jet_extra1_DownWeights = replaceElementList(configMgr.weights, "wjet_nom", "wjet_extra1_down")

    jet_extra2_UpWeights = replaceElementList(configMgr.weights, "wjet_nom", "wjet_extra2_up")
    jet_extra2_DownWeights = replaceElementList(configMgr.weights, "wjet_nom", "wjet_extra2_down")

    jet_jvt_UpWeights = replaceElementList(configMgr.weights, "wjet_nom", "wjet_jvt_up")
    jet_jvt_DownWeights = replaceElementList(configMgr.weights, "wjet_nom", "wjet_jvt_down")

    #trig_UpWeights = replaceElementList(configMgr.weights, "wtrig_nom", "wtrig_up")
    #trig_DownWeights = replaceElementList(configMgr.weights, "wtrig_nom", "wtrig_down")

    pu_UpWeights = replaceElementList(configMgr.weights, "wpu_nom", "wpu_up")
    pu_DownWeights = replaceElementList(configMgr.weights, "wpu_nom", "wpu_down")

    #pu_UpWeights_bkg = replaceElementList(configMgr.weights, "wpu_nom_bkg", "wpu_up_bkg")
    #pu_DownWeights_bkg = replaceElementList(configMgr.weights, "wpu_nom_bkg", "wpu_down_bkg")

    #pu_UpWeights_sig = replaceElementList(configMgr.weights, "wpu_nom_sig", "wpu_up_sig")
    #pu_DownWeights_sig = replaceElementList(configMgr.weights, "wpu_nom_sig", "wpu_down_sig")

    # attention: the "," at the end here is CRUCIAL
    pdf_UpWeights =  configMgr.weights+ ["wpdf_up"]
    pdf_DownWeights =  configMgr.weights+ ["wpdf_down"]
    

    weightDict={}

    
    if "MU" in systematicList:
        print "Adding MU weight syst"
        weightDict.update({
                "muStat": ( muon_stat_UpWeights, muon_stat_DownWeights,"overallSys"),
                "muSys": ( muon_sys_UpWeights, muon_sys_DownWeights,"overallSys"),
                "muStat_lowpt": ( muon_stat_lowpt_UpWeights, muon_stat_lowpt_DownWeights,"overallSys"),
                "muSys_lowpt": ( muon_sys_lowpt_UpWeights, muon_sys_lowpt_DownWeights,"overallSys"),
                "muIsoStat": ( muon_iso_stat_UpWeights, muon_iso_stat_DownWeights,"overallSys"),
                "muIsoSys": ( muon_iso_sys_UpWeights, muon_iso_sys_DownWeights,"overallSys"),
                "muBadSys": ( muon_bad_sys_UpWeights, muon_bad_sys_DownWeights,"overallSys"),
                "muTTVAStat": ( muon_ttva_stat_UpWeights, muon_ttva_stat_DownWeights,"overallSys"),
                "muTTVASys": ( muon_ttva_sys_UpWeights, muon_ttva_sys_DownWeights,"overallSys")})
    if 'EG' in systematicList:
        print "AddinG EG weight syst"
        weightDict.update({
                "elID": ( el_id_UpWeights, el_id_DownWeights,"overallSys"),
                "elIso": ( el_iso_UpWeights, el_iso_DownWeights,"overallSys"),
                "elReco": ( el_reco_UpWeights, el_reco_DownWeights,"overallSys"),
                "elChFlip": ( el_cf_UpWeights, el_cf_DownWeights,"overallSys")})
    if 'FT' in systematicList:
        print "Adding FT weight syst"
        weightDict.update({
                "FT_B": ( jet_b_UpWeights, jet_b_DownWeights,"overallSys"),
                "FT_C": ( jet_c_UpWeights, jet_c_DownWeights,"overallSys"),
                "FT_Extra1": ( jet_extra1_UpWeights, jet_extra1_DownWeights,"overallSys"),
                "FT_Extra2": ( jet_extra2_UpWeights, jet_extra2_DownWeights,"overallSys"),
                "FT_Light": ( jet_light_UpWeights, jet_light_DownWeights,"overallSys"),
                "JET_JVT": ( jet_jvt_UpWeights, jet_jvt_DownWeights,"overallSys")})

    if 'PU'  in systematicList:
        print "Adding PU weight syst"
        # different PU configurations are tested here
        weightDict.update({ "pileup": ( pu_UpWeights, pu_DownWeights,"overallSys")})
        #weightDict.update({ "pileupSIG": ( pu_UpWeights_sig, pu_DownWeights_sig,"overallSys")})
        #weightDict.update({ "pileupBKG": ( pu_UpWeights_bkg, pu_DownWeights_bkg,"overallSys")})

    if 'TRIG'  in systematicList:
        print "Adding Trigger weight syst"
        weightDict.update({
                "TRIG_muStat": (muon_trig_stat_UpWeights, muon_trig_stat_DownWeights,"overallSys"),
                "TRIG_muSys": (muon_trig_sys_UpWeights, muon_trig_sys_DownWeights,"overallSys"),
                "TRIG_elEff": (el_trig_UpWeights, el_trig_DownWeights,"overallSys"),
                "TRIG_elEffeff": (el_trigEff_UpWeights, el_trigEff_DownWeights,"overallSys")})


    if 'PDF'  in systematicList:
        print "Adding PDF weight syst"
        weightDict.update({"PDF":(pdf_UpWeights, pdf_DownWeights,"overallSys")})
    

    return weightDict

if __name__ == "__main__":
    main()
