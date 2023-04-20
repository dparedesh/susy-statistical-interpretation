#!/usr/bin/env python
# run as:
# HistFitter.py -twf -u "--signalRegions SR0bee,SR0bem,SR0bmm,SR1bee,SR1bem,SR1bmm,SR3bee,SR3bem,SR3bmm --signalGridName Mc12SusyGtt --signalList signal156548 --F excl" python/summer2013SameSign.py

from configManager import configMgr
from systematic import Systematic
from optparse import OptionParser
import configWriter

from sets import Set   
import  ROOT, math, sys, os
# CHANGE NTOYS, appended path, signal File!!!!!!

import pathUtilities
import json
import signalSameSignTools
signalRunnumberToMassesDict = signalSameSignTools.getRunnumbersMassesDictSSAllGrids()

##importing usefull things to defined samples (to keep the  main scrip clean!!)
from Helper import setBlind,sampleType
from Helper import bkgsDef,sample
from Helper import GetBinnedFitOptions



## Getting input options
inputParser = OptionParser()
inputParser.add_option('', '--calculatorType', dest = 'calculatorType', default = 2, help='0 for frequentist, 2 for asymptotic')
inputParser.add_option('', '--sysList', dest = 'sysList', default = "", help='list of systematics')
inputParser.add_option('', '--signalGridName', dest = 'signalGridName', default = 'Mc15SusyGtt', help='name of the grid(e.g. gtt)')
inputParser.add_option('', '--lumiTag', dest = 'lumiTag', default = '2000',  help='lumi tag in the input files')
inputParser.add_option('', '--signalList', dest = 'signalList', default = 'signal370102', help='give it a list of signal runnumbers')
inputParser.add_option('', '--theoryUncertMode', dest = 'theoryUncertMode', default = "nom", help='sets theory (i.e. lumi uncert) nom/up/down')
inputParser.add_option('', '--additionalOutName', dest = 'additionalOutName', default = "", help='additional name for output file')
# important: the deault signalRegions are the one trhat are used by default by the upstream script. leave them to be the full list of "good" regions
inputParser.add_option('', '--signalRegions', dest = 'signalRegions', default = '', help='sets which signal regions to use,(one or several), 0b,1b and/or 3b')
inputParser.add_option('', '--binnedFitSR ', dest= 'binnedFitSR',default='cuts,1,0.5,1.5',help="Ex: <var>,7,800,1300. It means that HF will do a binned fit on the variable <var> with 7 bins, from 800 up to 1300 of <var> range")
inputParser.add_option('', '--controlRegions', dest = 'controlRegions', default = '', help='sets which control regions to use,(one or several)')
inputParser.add_option('', '--bkgToNormalize',dest='bkgToNormalize',action="store",default='WZ',help="background to normalize in the CR provided")
inputParser.add_option('', '--binnedFitCR',dest='binnedFitCR',default='nJets25,9,3.5,12.5',help="Ex: <var>,7,800,1300. It means that HF will do a binned fit on the CR on the variable <var> with 7 bins, from 800 up to 1300 of <var> range")
inputParser.add_option('', '--validationRegions', dest = 'validationRegions', default = "", help='sets which validation regions to use,(one or several)')
inputParser.add_option('', '--doBlind', dest = 'doBlind',action="store",  default ="", help='List of regions to blind (comma separated), i.e: ALL, SR, CR, VR. If empty, it will blind all')

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
print "-binnedFitCR: ",options.binnedFitCR
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
    systematicList='EG,JET,MU,MET,FT,PU,TRIG,FAKES,CHFLIP,MISCH,TH'

systematicList=systematicList.split(',')




#######################
##  Setting regions  ##
#######################

signalRegionList = options.signalRegions.split(",")
validationRegionList=[]
controlRegionList=[]


if len(signalRegionList)==1 and signalRegionList[0]=='': signalRegionList=[]

if options.controlRegions != "":
    controlRegionList = options.controlRegions.split(",")
    if len(controlRegionList)>1: 
        sys.exit("--> Sorry, current framework allows only one CR... ABORTING!")

else:
    controlRegionList=[]


if options.validationRegions != "":
    validationRegionList = options.validationRegions.split(",")
else:
    validationRegionList=[]


if myFitType!=FitType.Background:

    if len(signalRegionList)==0 or len(signalRegionList)>1: 
        sys.exit("--> Sorry, for exclusion or discovery fits you need to pass exactly one SR... ABORTING")

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

binnedFit=GetBinnedFitOptions(options.binnedFitSR,'SR')    
binnedFitCR=[]
if controlRegionList: binnedFitCR=GetBinnedFitOptions(options.binnedFitCR,'CR')


print "## Systematic list: ",systematicList
print "## Lumi tag: ",options.lumiTag
print "## Fit Type: ",myFitType



if myFitType==FitType.Discovery:
    options.signalGridName="Discovery"
    if options.binnedFitSR != "cuts,1,0.5,1.5":
        print "- Discovery fits are singled bin... changing to single bin"
        binnedFit=["cuts",1,0.5,1.5]




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

#importing theory systematics
theorySyst=None
with open(pathUtilities.pythonDirectory()+'/theorySystematics.json') as json_file:
    theorySyst=json.load(json_file)


#use data yiels from TTres:
useDataSample = False


#defining backgrounds

OtherMultiboson = sample('OtherMultiboson',ROOT.kGreen+2,"WW, ZZ, VH, VVV",True,sampleType.BKG,theorySyst['thUnc_OtherMultibosonUp'],theorySyst['thUnc_OtherMultibosonDown'])
ttH = sample('ttH',ROOT.kOrange,"t#bar{t}H",True,sampleType.BKG,theorySyst['thUnc_ttHUp'],theorySyst['thUnc_ttHDown'])
RareTop_NottH = sample('RareTop_NottH',ROOT.kCyan+1,"t(W)Z, t#bar{t}VV, 3t, 4t",True,sampleType.BKG,theorySyst['thUnc_RareTop_NottHUp'],theorySyst['thUnc_RareTop_NottHDown'])
ttW = sample('ttW',ROOT.kViolet-9,"t#bar{t}W",True,sampleType.BKG,theorySyst['thUnc_ttWUp'],theorySyst['thUnc_ttWDown'])
ttZ = sample('ttZ',ROOT.kAzure+7,"t#bar{t}Z",True,sampleType.BKG,theorySyst['thUnc_ttZUp'],theorySyst['thUnc_ttZDown'])
WZ  = sample('WZ',ROOT.kOrange+1,"WZ",True,sampleType.BKG,theorySyst['thUnc_WZUp'],theorySyst['thUnc_WZDown'])

Multiboson = sample('Multiboson',ROOT.kGreen+2,"Multiboson",True,sampleType.BKG,theorySyst['thUnc_MultibosonUp'],theorySyst['thUnc_MultibosonDown'])
ttV=sample('ttV',ROOT.kViolet-9,"t#bar{t}V",True,sampleType.BKG,theorySyst['thUnc_ttVUp'],theorySyst['thUnc_ttVDown'])
Multitop = sample('Multitop',ROOT.kGreen+2,"Multitop",True,sampleType.BKG,theorySyst['thUnc_MultitopUp'],theorySyst['thUnc_MultitopDown'])


MisCharge = sample('MisCharge',ROOT.kRed+2,'Charge-flip',False,sampleType.BKG)
MisCharge.setYields(yieldsCoded['mischCount'],yieldsCoded['mischStatErr'])
if "CHFLIP" in systematicList: MisCharge.setDataDrivenSystematics(yieldsCoded['mischSystErrUp'], yieldsCoded['mischSystErrDown'])


Fakes = sample('Fakes',ROOT.kOrange-9,"Fake/non-prompt",False,sampleType.BKG)
Fakes.setYields(yieldsCoded['fakeCount'], yieldsCoded['fakeStatErr'])
if 'FAKES' in systematicList: Fakes.setDataDrivenSystematics(yieldsCoded['fakeSystErrUp'], yieldsCoded['fakeSystErrDown'])

# adding bkgs to the tool...
# configuration here is usually used for limit setting: less splitting go faster!

allBkg.addSample(Multiboson)
allBkg.addSample(Multitop)
allBkg.addSample(ttV)
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



def runAll():

    inputFileDict = {}
    inputFileDict['data'] = ['InputTrees/data.'+lumiTag+'.root']
    inputFileDict['signal'] = ['InputTrees/signal.'+lumiTag+'.root']
    inputFileDict['background'] = ['InputTrees/background.'+lumiTag+'.root']


    print "## Reading input trees from : InputTrees/background."+lumiTag+".root"


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
    


def setupConfigMgr(inputFileDict):
    #-------------------------------
    # Parameters for hypothesis test
    #-------------------------------
    configMgr.analysisName = options.signalGridName+'_'+options.additionalOutName
    
    configMgr.nTOYs= 1000
    configMgr.calculatorType = int(options.calculatorType)
    configMgr.testStatType = 3   # 3=one-sided profile likelihood test statistic (LHC default)
    configMgr.nPoints = 40       # 40 number of values scanned of signal-strength for upper-limit determination of signal strength.
    #configMgr.scanRange = (0., 0.5)
   
    if isBlind.SR: configMgr.blindSR = True
    if isBlind.CR: configMgr.blindCR = True
    if isBlind.VR: configMgr.blindVR = True

    configMgr.useSignalInBlindedData = False


    configMgr.writeXML = True #True is for debugging
    configMgr.keepSignalRegionType = True #Force SR to remain a SR for bkgOnly fits  (in those cases, SRs are set by  hand latter as CRs)

    configMgr.outputLumi =float(lumiTag)/1000 
    configMgr.inputLumi = configMgr.outputLumi #deal with this at the sample level
    configMgr.setLumiUnits("fb-1")

    configMgr.histCacheFile = os.getenv("HFRUNDIR")+"/data/"+configMgr.analysisName+".root"
    configMgr.outputFileName = os.getenv("HFRUNDIR")+"/results/"+configMgr.analysisName+"_output.root"
    
    if not configMgr.readFromTree:
        print "READING FROM data/"+configMgr.analysisName+".root"
        inputFileDict['background'] = ["data/"+configMgr.analysisName+".root"]
        
    configMgr.nomName = "_nom"

    ##########
    ## CUTS ##
    ##########
    
    # define signal regions. please always enclose SRs between () to ease combination
    # note: this assumes events in ntuples already pass SS(10+10+(10)) selection

    print "******** Defining dictionary of cuts..."
    configMgr.cutsDict["MCId"] = "(MCId !=363507 && MCId !=363509)"

    #Full Run-2 SR
    configMgr.cutsDict["Rpc2L1b"] = "(nSigLep>=2 && nBJets20>=1 && nJets40>=6 && met/meff>0.25 && "+configMgr.cutsDict["MCId"]+")"
    configMgr.cutsDict["Rpc2L2b"] = "(nSigLep>=2 && nBJets20>=2 && nJets25>=6 && met>300000 && meff>1400000 && met/meff>0.14 && "+configMgr.cutsDict["MCId"]+")"
    configMgr.cutsDict["Rpc2L0b"] = "(nSigLep>=2 && nBJets20==0 && nJets40>=6 && met>200000 && meff>1000000 && met/meff>0.2 && "+configMgr.cutsDict["MCId"]+")"
    configMgr.cutsDict["Rpc3LSS1b"] = "(nSigLep>=3 && nBJets20>=1 && is3LSS>0 && is3LSSproc>0 && !isZee && met/meff>0.14 && "+configMgr.cutsDict["MCId"]+")"
    configMgr.cutsDict["Rpv2L"] = "(nSigLep>=2 && nBJets20>=0 && nJets40>=6 && meff>2600000 && "+configMgr.cutsDict["MCId"]+")"



    # validation/control region
    configMgr.cutsDict["VRWZ4j"] = "((nSigLep==3 && NlepBL==3 && nBJets20==0 && nJets25>=4 && mSFOS>81000 && mSFOS<101000 && met>50000 && met<250000 && meff>600000 && meff<1500000  && "+configMgr.cutsDict["MCId"]+") && !"+configMgr.cutsDict["Rpc2L1b"]+" && !"+configMgr.cutsDict["Rpc2L2b"]+" && !"+configMgr.cutsDict["Rpc2L0b"]+" && !"+configMgr.cutsDict["Rpv2L"]+")"  
    configMgr.cutsDict["VRWZ5j"] = "((nSigLep==3 && NlepBL==3 && nBJets20==0 && nJets25>=5 && meff>400000 && met>50000 && mSFOS>81000 && mSFOS<101000 && meff<1500000 && met<250000  && "+configMgr.cutsDict["MCId"]+") && !"+configMgr.cutsDict["Rpc2L1b"]+" && !"+configMgr.cutsDict["Rpc2L2b"]+" && !"+configMgr.cutsDict["Rpc2L0b"]+" && !"+configMgr.cutsDict["Rpv2L"]+")"
    configMgr.cutsDict["VRttV"] = "((nSigLep>=2 && NlepBL>=2 && nBJets20>=1 && nJets40>=3 && meff>600000 && meff<1500000 && met<250000 && isSS30 && dRl1j>1.1 && SumBJetPt/SumJetPt>0.4 && met/meff>0.1  && "+configMgr.cutsDict["MCId"]+") && !"+configMgr.cutsDict["Rpc2L1b"]+" && !"+configMgr.cutsDict["Rpc2L2b"]+" && !"+configMgr.cutsDict["Rpc2L0b"]+" && !"+configMgr.cutsDict["Rpv2L"]+")"



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
                for var,values in config.iteritems():
    
                    if srname in signalRegionList and var==binnedFit[0]: dataHand.buildHisto(dataCounts[srname][binnedFit[0]],srname,var,binnedFit[2],(binnedFit[3]-binnedFit[2])/float(binnedFit[1]))
                    if srname in controlRegionList and var==binnedFitCR[0]: dataHand.buildHisto(dataCounts[srname][binnedFitCR[0]],srname,var,binnedFitCR[2],(binnedFitCR[3]-binnedFitCR[2])/float(binnedFitCR[1]))
                    if srname in validationRegionList: dataHand.buildHisto(dataCounts[srname]["cuts"],srname,var)


    #This dict will contain all the MC samples, including signal
    backgroundDict = {}

    if len(signalRegionList)==1:
        my_mu_SIG = "mu_"+signalRegionList[0]
    else:
        my_mu_SIG = "mu_SIG"

    signalName=str(sigSample)

  


    #----------#
    #  Signal  #
    #----------#
    # signal sample is added just to exclusion fit
    # (ideally it should be added later, but doing here for practical reasons since all MC systematics will be added  just after)
    if myFitType==FitType.Exclusion:
        print "- Defining signal sample in exclusion fit: ",signalName       
        backgroundDict[signalName] = configWriter.Sample(signalName, ROOT.kPink)
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
                backgroundDict[bkgList[i].getName()].addInputs(inputFileDict['background'])
                backgroundDict[bkgList[i].getName()].setStatConfig(True) # all stat errors treated as one in the fit (it includes signal if provided)

                if len(controlRegionList)==0: backgroundDict[bkgList[i].getName()].setNormByTheory(True) # assigns lumi uncertainty 
                else:
                    if options.bkgToNormalize is not bkgList[i].getName(): backgroundDict[bkgList[i].getName()].setNormByTheory(True) # assigns lumi uncertainty
                    else:
                        print "-- This bkg will be normalized in the fit... Lumi uncertainty therefore will not be assigned"
                        normRegions=[]
                        normRegions.append((controlRegionList[0],binnedFitCR[0]))

                        backgroundDict[bkgList[i].getName()].setNormFactor("mu_"+options.bkgToNormalize,1.,0.,5.)
                        backgroundDict[bkgList[i].getName()].setNormRegions(normRegions)    

        

    #-------------------------------------------------------------#
    #     Adding systematics to all MC samples: signal  and bkg   #    
    #-------------------------------------------------------------

    #KINEMATIC SYSTEMATICS
    treeDict=GetTreeSystematics()

    #WEIGHT SYSTEMATICS
    weightDict=GetWeightSystematics()


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



    #------------------#
    # Build fit config #
    #------------------#


    print "##****** Preparing fit configuration **********##"
    if myFitType==FitType.Exclusion:   #change fit name based on signal points (valid just for exclusion fit)       
        grid = options.signalGridName
        if signalName.strip('signal') in signalRunnumberToMassesDict[grid]:
            masses = signalRunnumberToMassesDict[grid][signalName.strip('signal')]
            fcName=fcName+'_{0}_{1}'.format(masses[0],masses[1])


        
            
    print "Setting fcName to",fcName,"sigSample is",sigSample
    myFitConfig = configMgr.addFitConfig(fcName)

    myFitConfig.statErrThreshold = 0.00001  #None

    measurement = myFitConfig.addMeasurement(name = "NormalMeasurement", lumi=1.0, lumiErr=0.017)


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
        # signalName has NO masses, like signal123456. masses must be added to the jsons downstream by a separate python script
        myFitConfig.hypoTestName = signalName

        
    #----------------#
    # Build channels #
    #----------------#

    #-------------------#
    # Adding CRs to fit # --> just for those CRs explicitelly provided in the command line
    #-------------------#

    controlRegionChannels=[]
    for controlRegionName in controlRegionList:
        print "- Adding CR :",controlRegionName

        cChan = myFitConfig.addChannel(binnedFitCR[0], [controlRegionName],binnedFitCR[1],binnedFitCR[2],binnedFitCR[3]);
        cChan.useOverflowBin=True
        cChan.useUnderflowBin=True

        # Adding data-driven samples for this channel
        for bkg in dataDrivenList:
            print "- Adding data-driven samples for channel : ",bkg.getName()

            dataDrivenSample=createDataDrivenSample(bkg,controlRegionName,binnedFitCR[0],binnedFitCR[1],binnedFitCR[2],binnedFitCR[3])

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

        sChan = myFitConfig.addChannel(binnedFit[0], [cutname], binnedFit[1],binnedFit[2],binnedFit[3])
        if binnedFit[1] != 1: sChan.useOverflowBin = True

        if myFitType==FitType.Discovery:
            print "--Adding discovery dummy sample..."
            sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
            sChan.getSample('DiscoveryMode_'+cutname).setNormFactor(my_mu_SIG, 1., 0., 100)
            #measurement.addPOI(my_mu_SIG)

        # Adding data-driven samples for this channel
        for bkg in dataDrivenList:
            print "- Adding data-driven samples for channel : ",bkg.getName()
        
            dataDrivenSample=createDataDrivenSample(bkg,cutname,binnedFit[0],binnedFit[1],binnedFit[2],binnedFit[3])
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
    dataDriven_sample.setStatConfig(True)

    #Systematic from data-driven will affect only the normalization of the samples (this is temporal)
    if bkg.getDataDrivenSystematicUp(region) and bkg.getDataDrivenSystematicDown(region):
        print "Adding systematics for this sample..."
        systDataDriven=Systematic("syst_"+bkg.getName()+"_"+region, "1.", 1+bkg.getDataDrivenSystematicUp(region)["cuts"][0],1-bkg.getDataDrivenSystematicDown(region)["cuts"][0], "user","userOverallSys")

        dataDriven_sample.addSystematic(systDataDriven)
    else:
        print "Systematic for this sample has not been assigned..."


    return dataDriven_sample


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

    for i in range(len(bkgList)):

        if bkgList[i].getSampleType()==sampleType.BKG:

            if bkgList[i].getMC()==True:

                if sChan.hasSample(bkgList[i].getName()):
                    print "--> Adding theory syst to ",bkgList[i].getName()
                    systTemp=Systematic("theoryUncert_"+bkgList[i].getName()+"_"+cutname, "1.", 1+bkgList[i].getTheorySystematicUp(cutname),1-bkgList[i].getTheorySystematicDown(cutname), "user","userOverallSys")
                    sChan.getSample(bkgList[i].getName()).addSystematic(systTemp)


def GetTreeSystematics():

    treeDict={}

    if 'EG' in systematicList:
        print "Adding EG tree syst"
        treeDict.update({
                'EG_Scale':('EG_SCALE_ALL__1up',"EG_SCALE_ALL__1down","histoSys"),
                'EG_Resolution':("EG_RESOLUTION_ALL__1up","EG_RESOLUTION_ALL__1down","histoSys")})

    if 'JET' in systematicList:
        print "Adding JET tree syst"
        treeDict.update({
                'JET_scale_NP1':("JET_GroupedNP_1__1up","JET_GroupedNP_1__1down","histoSys"),
                'JET_scale_NP2':("JET_GroupedNP_2__1up","JET_GroupedNP_2__1down","histoSys"),
                'JET_scale_NP3':("JET_GroupedNP_3__1up","JET_GroupedNP_3__1down","histoSys"),
                'JET_EtaIntercalibration_NonClosure_highE':("JET_EtaIntercalibration_NonClosure_highE__1up","JET_EtaIntercalibration_NonClosure_highE__1down","histoSys"),
                'JET_EtaIntercalibration_NonClosure_negEta':("JET_EtaIntercalibration_NonClosure_negEta__1up","JET_EtaIntercalibration_NonClosure_negEta__1down","histoSys"),
                'JET_EtaIntercalibration_NonClosure_posEta':("JET_EtaIntercalibration_NonClosure_posEta__1up","JET_EtaIntercalibration_NonClosure_posEta__1down","histoSys"),
                'JET_JER_DataVsMC':("JET_JER_DataVsMC__1up","JET_JER_DataVsMC__1down","histoSys"),
                'JET_JER_EffectiveNP_1':('JET_JER_EffectiveNP_1__1up','JET_JER_EffectiveNP_1__1down',"histoSys"),
                'JET_JER_EffectiveNP_2':('JET_JER_EffectiveNP_2__1up','JET_JER_EffectiveNP_2__1down',"histoSys"),
                'JET_JER_EffectiveNP_3':('JET_JER_EffectiveNP_3__1up','JET_JER_EffectiveNP_3__1down',"histoSys"),
                'JET_JER_EffectiveNP_4':('JET_JER_EffectiveNP_4__1up','JET_JER_EffectiveNP_4__1down',"histoSys"),
                'JET_JER_EffectiveNP_5':('JET_JER_EffectiveNP_5__1up','JET_JER_EffectiveNP_5__1down',"histoSys"),
                'JET_JER_EffectiveNP_6':('JET_JER_EffectiveNP_6__1up','JET_JER_EffectiveNP_6__1down',"histoSys"),
                'JET_JER_EffectiveNP_7restTerm':('JET_JER_EffectiveNP_7restTerm__1up','JET_JER_EffectiveNP_7restTerm__1down',"histoSys"),
                'JET_AFII': ("JET_RelativeNonClosure_AFII__1up", "JET_RelativeNonClosure_AFII__1down","histoSys")
                })

    if "MU" in systematicList:
        print "Adding MU tree syst"
        treeDict.update({
                'Mu_ID':("MUON_ID__1up","MUON_ID__1down","histoSys"),
                'Mu_MS':("MUON_MS__1up","MUON_MS__1down","histoSys"),
                'Mu_Sagitta_Res': ("MUON_SAGITTA_RESBIAS__1up","MUON_SAGITTA_RESBIAS__1down","histoSys"),
                'Mu_Sagitta_Rho': ("MUON_SAGITTA_RHO__1up","MUON_SAGITTA_RHO__1down","histoSys"),
                'Mu_Scale':( "MUON_SCALE__1up","MUON_SCALE__1down","histoSys")})
    if 'MET' in systematicList:
        print "Adding MET tree syst"
        treeDict.update({
                'MET_Soft_reso_Para':("MET_SoftTrk_ResoPara","nom","histoSysOneSideSym"),
                'MET_Soft_reso_Perp':("MET_SoftTrk_ResoPerp","nom","histoSysOneSideSym"),
                'MET_Soft_Scale':("MET_SoftTrk_ScaleUp","MET_SoftTrk_ScaleDown","histoSys")})

    return treeDict

def GetWeightSystematics():

    #---------
    # weights 
    #---------

    #N.B. lumiScaling has to be set to UP,DOWN and nominal in the correct position!!!
    # this takes care of the signal theory unc
    if options.theoryUncertMode.lower() == 'up':
        configMgr.weights = ("wmu_nom","wel_nom","wtrig_nom","wjet_nom","mcweight","wpu_nom_bkg","wpu_nom_sig","MC_campaign_weight", "lumiScaling_UP")
    elif options.theoryUncertMode.lower() == 'down':
        configMgr.weights = ("wmu_nom","wel_nom","wtrig_nom","wjet_nom","mcweight","wpu_nom_bkg","wpu_nom_sig","MC_campaign_weight", "lumiScaling_DOWN")
    else:
        configMgr.weights = ("wmu_nom","wel_nom","wtrig_nom","wjet_nom","mcweight","wpu_nom_bkg","wpu_nom_sig","MC_campaign_weight", "lumiScaling")

    # configure the rest of the weight-based systematics (muon, electrons, jets)
    muon_bad_stat_UpWeights = replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_bad_stat_up")
    muon_bad_stat_DownWeights = replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_bad_stat_down")
    muon_bad_sys_UpWeights = replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_bad_sys_up")
    muon_bad_sys_DownWeights = replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_bad_sys_down")
    muon_stat_UpWeights = replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_stat_up")
    muon_stat_DownWeights = replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_stat_down")
    muon_sys_UpWeights = replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_sys_up")
    muon_sys_DownWeights = replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_sys_down")
    muon_stat_lowpt_UpWeights = replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_stat_lowpt_up")
    muon_stat_lowpt_DownWeights = replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_stat_lowpt_down")
    muon_sys_lowpt_UpWeights = replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_sys_lowpt_up")
    muon_sys_lowpt_DownWeights = replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_sys_lowpt_down")
    muon_iso_stat_UpWeights =  replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_iso_stat_up")
    muon_iso_stat_DownWeights =  replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_iso_stat_down")
    muon_iso_sys_UpWeights =  replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_iso_sys_up")
    muon_iso_sys_DownWeights =  replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_iso_sys_down")
    muon_ttva_stat_UpWeights =  replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_ttva_stat_up")
    muon_ttva_stat_DownWeights =  replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_ttva_stat_down")
    muon_ttva_sys_UpWeights =  replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_ttva_sys_up")
    muon_ttva_sys_DownWeights =  replaceStringInTuple(configMgr.weights, "wmu_nom", "wmu_ttva_sys_down")

    muon_trig_stat_UpWeights = replaceStringInTuple(configMgr.weights, "wtrig_nom", "wmu_trig_stat_up")
    muon_trig_stat_DownWeights = replaceStringInTuple(configMgr.weights, "wtrig_nom", "wmu_trig_stat_down")
    muon_trig_sys_UpWeights = replaceStringInTuple(configMgr.weights, "wtrig_nom", "wmu_trig_sys_up")
    muon_trig_sys_DownWeights = replaceStringInTuple(configMgr.weights, "wtrig_nom", "wmu_trig_sys_down")
    
    el_cf_UpWeights = replaceStringInTuple(configMgr.weights, "wel_nom", "wel_cid_up")
    el_cf_DownWeights = replaceStringInTuple(configMgr.weights, "wel_nom", "wel_cid_down")
    el_id_UpWeights =  replaceStringInTuple(configMgr.weights, "wel_nom", "wel_id_up")
    el_id_DownWeights =  replaceStringInTuple(configMgr.weights, "wel_nom", "wel_id_down")
    el_iso_UpWeights =  replaceStringInTuple(configMgr.weights, "wel_nom", "wel_iso_up")
    el_iso_DownWeights =  replaceStringInTuple(configMgr.weights, "wel_nom", "wel_iso_down")
    el_reco_UpWeights =  replaceStringInTuple(configMgr.weights, "wel_nom", "wel_reco_up")
    el_reco_DownWeights =  replaceStringInTuple(configMgr.weights, "wel_nom", "wel_reco_down")
    el_trig_UpWeights =  replaceStringInTuple(configMgr.weights, "wtrig_nom", "wel_trig_up")
    el_trig_DownWeights =  replaceStringInTuple(configMgr.weights, "wtrig_nom", "wel_trig_down")

    jet_b_UpWeights =  replaceStringInTuple(configMgr.weights, "wjet_nom", "wjet_b_up")
    jet_b_DownWeights =  replaceStringInTuple(configMgr.weights, "wjet_nom", "wjet_b_down")
    jet_c_UpWeights =  replaceStringInTuple(configMgr.weights, "wjet_nom", "wjet_c_up")
    jet_c_DownWeights =  replaceStringInTuple(configMgr.weights, "wjet_nom", "wjet_c_down")
    jet_light_UpWeights =  replaceStringInTuple(configMgr.weights, "wjet_nom", "wjet_light_up")
    jet_light_DownWeights =  replaceStringInTuple(configMgr.weights, "wjet_nom", "wjet_light_down")

    jet_extra1_UpWeights =  replaceStringInTuple(configMgr.weights, "wjet_nom", "wjet_extra1_up")
    jet_extra1_DownWeights =  replaceStringInTuple(configMgr.weights, "wjet_nom", "wjet_extra1_down")

    jet_extra2_UpWeights =  replaceStringInTuple(configMgr.weights, "wjet_nom", "wjet_extra2_up")
    jet_extra2_DownWeights =  replaceStringInTuple(configMgr.weights, "wjet_nom", "wjet_extra2_down")

    jet_jvt_UpWeights = replaceStringInTuple(configMgr.weights, "wjet_nom", "wjet_jvt_up")
    jet_jvt_DownWeights = replaceStringInTuple(configMgr.weights, "wjet_nom", "wjet_jvt_down")

    trig_UpWeights = replaceStringInTuple(configMgr.weights, "wtrig_nom", "wtrig_up")
    trig_DownWeights = replaceStringInTuple(configMgr.weights, "wtrig_nom", "wtrig_down")

    chflip_UpWeights = replaceStringInTuple(configMgr.weights, "wel_nom", "wchflip_up")
    chflip_DownWeights = replaceStringInTuple(configMgr.weights, "wel_nom", "wchflip_down")

    pu_UpWeights_bkg =  replaceStringInTuple(configMgr.weights, "wpu_nom_bkg", "wpu_up_bkg")
    pu_DownWeights_bkg =  replaceStringInTuple(configMgr.weights, "wpu_nom_bkg", "wpu_down_bkg")

    pu_UpWeights_sig = replaceStringInTuple(configMgr.weights, "wpu_nom_sig", "wpu_up_sig")
    pu_DownWeights_sig =  replaceStringInTuple(configMgr.weights, "wpu_nom_sig", "wpu_down_sig")

    # attention: the "," at the end here is CRUCIAL
    pdf_UpWeights =  configMgr.weights+ ("wpdf_up",)
    pdf_DownWeights =  configMgr.weights+ ("wpdf_down",)


    weightDict={}

    if "MU" in systematicList:
        print "Adding MU weight syst"
        weightDict.update({
                "muStat": (muon_stat_UpWeights, muon_stat_DownWeights,"overallSys"),
                "muSys": ( muon_sys_UpWeights, muon_sys_DownWeights,"overallSys"),
                "muStat_lowpt": (muon_stat_lowpt_UpWeights, muon_stat_lowpt_DownWeights,"overallSys"),
                "muSys_lowpt": ( muon_sys_lowpt_UpWeights, muon_sys_lowpt_DownWeights,"overallSys"),
                "muIsoStat": ( muon_iso_stat_UpWeights, muon_iso_stat_DownWeights,"overallSys"),
                "muIsoSys": ( muon_iso_sys_UpWeights, muon_iso_sys_DownWeights,"overallSys"),
                "muBadStat":( muon_bad_stat_UpWeights, muon_bad_stat_DownWeights,"overallSys"),
                "muBadSys":( muon_bad_sys_UpWeights, muon_bad_sys_DownWeights,"overallSys"),
                "muTTVAStat": ( muon_ttva_stat_UpWeights, muon_ttva_stat_DownWeights,"overallSys"),
                "muTTVASys": ( muon_ttva_sys_UpWeights, muon_ttva_sys_DownWeights,"overallSys")})
    if 'EG' in systematicList:
        print "AddinG EG weight syst"
        weightDict.update({
                "elID": ( el_id_UpWeights, el_id_DownWeights,"overallSys"),
                "elIso": ( el_iso_UpWeights, el_iso_DownWeights,"overallSys"),
                "elReco": ( el_reco_UpWeights, el_reco_DownWeights,"overallSys"),
                "elChID": ( el_cf_UpWeights, el_cf_DownWeights,"overallSys")})
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
        weightDict.update({ "pileupSIG": (pu_UpWeights_sig, pu_DownWeights_sig,"overallSys")})
        weightDict.update({ "pileupBKG": (pu_UpWeights_bkg, pu_DownWeights_bkg,"overallSys")})

    if 'TRIG'  in systematicList:
        print "Adding Trigger weight syst"
        weightDict.update({"TRIG":(trig_UpWeights, trig_DownWeights,"overallSys")})

    if 'CHFLIP'  in systematicList:
        print "Adding Charge Flip Tagger weight syst"
        weightDict.update({"CHFLIP":(chflip_UpWeights, chflip_DownWeights,"overallSys")})

    if 'PDF'  in systematicList:
        print "Adding PDF weight syst"
        weightDict.update({"PDF":(pdf_UpWeights, pdf_DownWeights,"overallSys")})

    return weightDict

runAll()
