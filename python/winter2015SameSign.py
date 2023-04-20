#!/usr/bin/env python
# run as:
# HistFitter.py -twf -u "--signalRegions SR0bee,SR0bem,SR0bmm,SR1bee,SR1bem,SR1bmm,SR3bee,SR3bem,SR3bmm --signalGridName Mc12SusyGtt --signalList signal156548 --fitMode SRonly" python/summer2013SameSign.py

from configManager import configMgr
from systematic import Systematic
from optparse import OptionParser
    
import  ROOT, math, sys, os

# CHANGE NTOYS, appended path, signal File!!!!!!

import pathUtilities
import signalSameSignTools
signalRunnumberToMassesDict = signalSameSignTools.getRunnumbersMassesDictSSAllGrids()


 # global variables, input flags with defaults
bkgOnlyFitConfig = None

inputParser = OptionParser()
inputParser.add_option('', '--calculatorType', dest = 'calculatorType', default = 2, help='0 for frequentist, 2 for asymptotic')
inputParser.add_option('', '--sysList', dest = 'sysList', default = "ALL", help='list of systematics')
inputParser.add_option('', '--signalGridName', dest = 'signalGridName', default = 'Mc15SusyGtt', help='name of the grid(e.g. gtt)')
inputParser.add_option('', '--lumiTag', dest = 'lumiTag', default = '2000', help='lumi tag in the input files')
inputParser.add_option('', '--signalList', dest = 'signalList', default = 'signal370102', help='give it a list of signal runnumbers')
inputParser.add_option('', '--useStat', dest = 'useStat', default = "MergedSamples", help='MergedSamples, PerSample, None')
inputParser.add_option('', '--fitMode', dest = 'fitMode', default = "SR", help='pre-defined fit configurations: SR_discovery')
inputParser.add_option('', '--theoryUncertMode', dest = 'theoryUncertMode', default = "nom", help='sets theory (i.e. lumi uncert) nom/up/down')
inputParser.add_option('', '--additionalOutName', dest = 'additionalOutName', default = "", help='additional name for output file')
# important: the deault signalRegions are the one trhat are used by default by the upstream script. leave them to be the full list of "good" regions
inputParser.add_option('', '--signalRegions', dest = 'signalRegions', default = 'SR0b3j,SR0b5j,SR3b,SR1b', help='sets which signal regions to use,(one or several), 0b,1b and/or 3b')
inputParser.add_option('', '--controlRegions', dest = 'controlRegions', default = '', help='sets which control regions to use,(one or several)')
inputParser.add_option('', '--validationRegions', dest = 'validationRegions', default = "", help='sets which validation regions to use,(one or several)')
inputParser.add_option('', '--useComplexFakeUncertainty', dest = 'useComplexFakeUncertainty', default = 'False', help='whether to use the simplified (bit worse) or fully correlated fake uncertainties (facotr ~2 slower)')
inputParser.add_option('', '--useCoarseGranularity', dest = 'useCoarseGranularity', default = "False", help='do we merge all the diboson and all the top+X backgroudns together?')
inputParser.add_option('', '--jobTag',dest='jobTag',default='winter2015SameSign',help="Job Tag: example: winter2015SS")

import select
configArgs = []

userArgs= configMgr.userArg.split(' ')
for i in userArgs:
    configArgs.append(i)



(options, args) = inputParser.parse_args(configArgs)

lumiTag=options.lumiTag

fitMode = options.fitMode.split("_")
signalRegionList = options.signalRegions.split(",")
controlRegionList = options.controlRegions.split(",")

if options.validationRegions != "":
    validationRegionList = options.validationRegions.split(",")
else:
    validationRegionList=[]

systematicList=options.sysList
if systematicList=='ALL':
    #systematicList='EG,JET,MU,MET,FT,PU,TRIG,CHFLIP,TH'
    systematicList='EG,JET,MU,MET,FT,PU,TRIG,CHFLIP,FAKES,MISCH,TH'

print "got systematics from command line ",systematicList,options.sysList
print "got lumiTag from command line ",options.lumiTag
print "got fitMode from command line ",options.fitMode

systematicList=systematicList.split(',')

print "Will do a fit with systematics:",systematicList


splitTopV = True

if options.useComplexFakeUncertainty == 'True': useComplexFakeUncertainty = True
else: useComplexFakeUncertainty = False

if options.useCoarseGranularity == 'True': useCoarseGranularity = True
else: useCoarseGranularity = False

blindFit='blind' in fitMode
discoveryFit = (("discovery" in fitMode) or ("disc" in fitMode))

if blindFit:
    print "Will do a BLIND FIT"
if discoveryFit:
    print "Will do a DISCOVERY FIT"

if discoveryFit:
    options.signalGridName="Discovery"

dataCounts={
    'Rpc2L1bS':([14.], "cuts",0.5),
    'Rpc2L1bH':([13.], "cuts",0.5),
    'Rpc2L2bS':([3.], "cuts",0.5),
    'Rpc2L2bH':([0.], "cuts",0.5),
    'Rpc2L0bS':([7.], "cuts",0.5),
    'Rpc2L0bH':([3.], "cuts",0.5),
    'Rpc3L0bS':([9.], "cuts",0.5),
    'Rpc3L0bH':([3.], "cuts",0.5),
    'Rpc3L1bS':([20.], "cuts",0.5),
    'Rpc3L1bH':([4.], "cuts",0.5),
    'Rpc2Lsoft2b' :([5.], "cuts",0.5),
    'Rpc2Lsoft1b':([4.], "cuts",0.5),
    'Rpc3LSS1b':([1.], "cuts",0.5),
    'Rpv2L1bS':([26.], "cuts",0.5),
    'Rpv2L1bM' :([9.], "cuts",0.5),
    'Rpv2L1bH':([2.], "cuts",0.5),
    'Rpv2L2bH':([1.], "cuts",0.5),
    'Rpv2L0b' :([2.], "cuts",0.5),
    'Rpv2L2bS' :([20.], "cuts",0.5),
    'VRWZ4j':  ([1.],'cuts',0.5),
    'VRWZ5j':  ([1.],'cuts',0.5),
    'VRWW':  ([1.],'cuts',0.5),
    'VRttW': ([1.],'cuts',0.5),
    'VR3bRpcS': ([1.],'cuts',0.5),
    'VR3bRpcH': ([1.],'cuts',0.5),
    'VR3bRpvS': ([1.],'cuts',0.5),
    'VR3bRpvH': ([1.],'cuts',0.5),
    'VRttW': ([1.],'cuts',0.5),
    'VRttW': ([1.],'cuts',0.5),
    'VRttZ': ([1.],'cuts',0.5)
    }

## hard coded fakes and misCh ##

fakeBinned={
    #'SRbin_1b': (0,0,0)
}

fakeBinnedErr={
    #'SRbin_1b': (0,0,0)
}

fakeBinnedSystErr={
    #'SRbin_1b': (0,0,0)
}

fakeCount={
    'Rpc2Lsoft2b': ([1.72],'cuts',0.5),
    'Rpv2L1bS': ([6.22],'cuts',0.5),
    'Rpv2L1bH': ([0.15],'cuts',0.5),
    'Rpv2L1bM': ([1.25],'cuts',0.5),
    'Rpv2L2bH': ([0.15],'cuts',0.5),
    'VRWZ4j': ([48.87],'cuts',0.5),
    'Rpc3LSS1b': ([0.89],'cuts',0.5),
    'VRttZ': ([22.32],'cuts',0.5),
    'VRttW': ([17.51],'cuts',0.5),
    'Rpv2L0b': ([0.18],'cuts',0.5),
    'Rpc3L0bS': ([0.23],'cuts',0.5),
    'Rpc2L0bS': ([1.55],'cuts',0.5),
    'Rpc2Lsoft1b': ([3.53],'cuts',0.5),
    'Rpc3L1bS': ([4.23],'cuts',0.5),
    'Rpc3L1bH': ([0.47],'cuts',0.5),
    'Rpc3L0bH': ([0.15],'cuts',0.5),
    'Rpc2L0bH': ([0.87],'cuts',0.5),
    'Rpc2L1bH': ([2.26],'cuts',0.5),
    'VRWZ5j': ([17.00],'cuts',0.5),
    'VRWW': ([13.31],'cuts',0.5),
    'Rpc2L2bH': ([0.15],'cuts',0.5),
    'Rpc2L2bS': ([0.49],'cuts',0.5),
    'VR3bRpcS': ([1.29],'cuts',0.5),
    'VR3bRpcH': ([0.],'cuts',0.5),
    'VR3bRpvS': ([2.73],'cuts',0.5),
    'VR3bRpvH': ([2.25],'cuts',0.5),
    'Rpv2L2bS' :([8.07], "cuts",0.5),
    'Rpc2L1bS': ([2.59],'cuts',0.5)
    }

fakeStatErr={
    'Rpc2Lsoft2b': [0.58],
    'Rpv2L1bS': [1.54],
    'Rpv2L1bH': [0.15],
    'Rpv2L1bM': [0.65],
    'Rpv2L2bH': [0.15],
    'VRWZ4j': [3.84],
    'Rpc3LSS1b': [0.14],
    'VRttZ': [2.40],
    'VRttW': [3.12],
    'Rpv2L0b': [0.21],
    'Rpc3L0bS': [0.15],
    'Rpc2L0bS': [0.52],
    'Rpc2Lsoft1b': [0.97],
    'Rpc3L1bS': [1.28],
    'Rpc3L1bH': [0.24],
    'Rpc3L0bH': [0.15],
    'Rpc2L0bH': [0.48],
    'Rpc2L1bH': [0.59],
    'VRWZ5j': [1.79],
    'VRWW': [1.66],
    'Rpc2L2bH': [0.15],
    'Rpc2L2bS': [0.32],
    'VR3bRpcS': [0.657],
    'VR3bRpcH': [0.],
    'VR3bRpvS': [1.38],
    'VR3bRpvH': [1.49],
    'Rpv2L2bS': [1.92],
    'Rpc2L1bS': [0.91]
    }

fakeSystErr={
    'Rpc2Lsoft2b': [1.36/1.72],
    'Rpv2L1bS': [5.68/6.22],
    'Rpv2L1bH': [0.00],
    'Rpv2L1bM': [1.02/1.25],
    'Rpv2L2bH': [0.00],
    'VRWZ4j': [29.90/48.87],
    'Rpc3LSS1b': [0.72/0.89],
    'VRttZ': [13.36/22.32],
    'VRttW': [15.46/17.51],
    'Rpv2L0b': [0.29/0.18],
    'Rpc3L0bS': [0.18/0.23],
    'Rpc2L0bS': [0.81/1.55],
    'Rpc2Lsoft1b': [2.22/3.53],
    'Rpc3L1bS': [2.86/4.23],
    'Rpc3L1bH': [0.38/0.47],
    'Rpc3L0bH': [0.00],
    #'Rpc2L0bH': [0.76/0.87],
    'Rpc2L0bH': [0.38/0.87],
    'Rpc2L1bH': [1.76/2.26],
    'VRWZ5j': [11.60/17.00],
    'VRWW': [10.00/13.31],
    'Rpc2L2bH': [0.00],
    #'Rpc2L2bS': [0.55/0.49],
    'Rpc2L2bS': [0.27/0.49],
    'VR3bRpcS': [0.847/1.29],
    'VR3bRpcH': [0.],
    'VR3bRpvS': [1.73/2.73],
    'VR3bRpvH': [2.56/2.25],
    'Rpv2L2bS': [6.66/8.07],
    #'Rpc2L1bS': [1.97/2.59]
    'Rpc2L1bS': [1./2.59]
    }

mischCount={
    'Rpc2Lsoft2b': ([0.08],'cuts',0.5),
    'VRWZ4j': ([0.00],'cuts',0.5),
    'Rpc3L0bS': ([0.00],'cuts',0.5),
    'Rpc2L0bS': ([0.05],'cuts',0.5),
    'Rpc3L1bS': ([0.00],'cuts',0.5),
    'Rpv2L0b': ([0.03],'cuts',0.5),
    'VRttZ': ([0.00],'cuts',0.5),
    'VRttW': ([3.41],'cuts',0.5),
    'Rpc2L0bH': ([0.01],'cuts',0.5),
    'Rpc2L1bH': ([0.25],'cuts',0.5),
    'VRWZ5j': ([0.00],'cuts',0.5),
    'Rpc2L2bH': ([0.02],'cuts',0.5),
    'Rpc3L1bH': ([0.00],'cuts',0.5),
    'Rpc2Lsoft1b': ([0.08],'cuts',0.5),
    'Rpc2L2bS': ([0.10],'cuts',0.5),
    'Rpc2L1bS': ([0.25],'cuts',0.5),
    'Rpc3L0bH': ([0.00],'cuts',0.5),
    'VRWW': ([1.74],'cuts',0.5),
    'Rpv2L1bS': ([0.74],'cuts',0.5),
    'Rpv2L1bH': ([0.02],'cuts',0.5),
    'Rpc3LSS1b': ([0.39],'cuts',0.5),
    'Rpv2L2bH': ([0.03],'cuts',0.5),
    'VR3bRpcS': ([0.139],'cuts',0.5),
    'VR3bRpcH': ([0.],'cuts',0.5),
    'VR3bRpvS': ([0.704],'cuts',0.5),
    'VR3bRpvH': ([0.0778],'cuts',0.5),
    'Rpv2L2bS' :([0.46], "cuts",0.5),
    'Rpv2L1bM': ([0.10],'cuts',0.5)
    }

mischStatErr={
    'Rpc2Lsoft2b': [0.01],
    'VRWZ4j': [0.00],
    'Rpc3L0bS': [0.00],
    'Rpc2L0bS': [0.01],
    'Rpc3L1bS': [0.00],
    'Rpv2L0b': [0.02],
    'VRttZ': [0.00],
    'VRttW': [0.10],
    'Rpc2L0bH': [0.00],
    'Rpc2L1bH': [0.03],
    'VRWZ5j': [0.00],
    'Rpc2L2bH': [0.01],
    'Rpc3L1bH': [0.00],
    'Rpc2Lsoft1b': [0.01],
    'Rpc2L2bS': [0.01],
    'Rpc2L1bS': [0.02],
    'Rpc3L0bH': [0.00],
    'VRWW': [0.10],
    'Rpv2L1bS': [0.04],
    'Rpv2L1bH': [0.01],
    'Rpc3LSS1b': [0.03],
    'Rpv2L2bH': [0.01],
    'VR3bRpcS': [0.0122],
    'VR3bRpcH': [0.],
    'VR3bRpvS': [0.029],
    'VR3bRpvH': [0.0164],
    'Rpv2L2bS': [0.03],
    'Rpv2L1bM': [0.01]
   }

mischSystErr={
    'Rpc2Lsoft2b': [0.02/0.08],
    'VRWZ4j': [0.00],
    'Rpc3L0bS': [0.00],
    'Rpc2L0bS': [0.01/0.05],
    'Rpc3L1bS': [0.00],
    'Rpv2L0b': [0.00],
    'VRttZ': [0.00],
    'VRttW': [0.48/3.41],
    'Rpc2L0bH': [0.00],
    'Rpc2L1bH': [0.04/0.25],
    'VRWZ5j': [0.00],
    'Rpc2L2bH': [0.],
    'Rpc3L1bH': [0.00],
    'Rpc2Lsoft1b': [0.02/0.08],
    'Rpc2L2bS': [0.02],
    'Rpc2L1bS': [0.04/0.25],
    'Rpc3L0bH': [0.00],
    'VRWW': [0.24/1.74],
    'Rpv2L1bS': [0.11/0.74],
    'Rpv2L1bH': [0.00],
    'Rpc3LSS1b': [0.07/0.39],
    'Rpv2L2bH': [0.01/0.03],
    'VR3bRpcS': [0.0241/0.139],
    'VR3bRpcH': [0.],
    'VR3bRpvS': [0.107/0.704],
    'VR3bRpvH': [0.0128/0.0778],
    'Rpv2L2bS': [0.07/0.46],
    'Rpv2L1bM': [0.02/0.10]
    }

def runAll():

    #ttreeDirectory = pathUtilities.currentTreeDirectory()

    inputFileDict = {}
    inputFileDict['data'] = ['InputTrees/data.'+lumiTag+'.root']
    inputFileDict['signal'] = ['InputTrees/signal.'+lumiTag+'.root']
    inputFileDict['background'] = ['InputTrees/background.'+lumiTag+'.root']

    setupConfigMgr(inputFileDict)

    if options.signalList=="bkgOnly":
        doFitConfig(inputFileDict,"bkgOnly")
    else:
        signalGridName = options.signalGridName
        signalNamesList = options.signalList.split(';')
        if not discoveryFit:
            for signalName in signalNamesList:
                doFitConfig(inputFileDict,signalGridName+"_"+signalName, signalName)
        else:
            print "Configuring DISCOVERY FIT"
            doFitConfig(inputFileDict,"Discovery","")


def setupConfigMgr(inputFileDict):
    #-------------------------------
    # Parameters for hypothesis test
    #-------------------------------
    configMgr.analysisName = options.signalGridName+'_'+options.additionalOutName+'_'+options.jobTag
    
    configMgr.nTOYs= 1000
    configMgr.calculatorType = int(options.calculatorType)
    configMgr.testStatType = 3   # 3=one-sided profile likelihood test statistic (LHC default)
    configMgr.nPoints = 40       # number of values scanned of signal-strength for upper-limit determination of signal strength.
    #configMgr.scanRange = (0., 20.)
    configMgr.blindSR = False
    configMgr.blindCR = False
    configMgr.blindVR = False

    if blindFit:
        #    # ADS: hack to avoid usage of data
        configMgr.blindSR = True
        configMgr.blindCR = True
        configMgr.blindVR = True
        configMgr.useSignalInBlindedData = False 

    configMgr.writeXML = False #True is for debugging
    configMgr.keepSignalRegionType = True #Force SR to remain a SR for bkgOnly fits    

    configMgr.outputLumi =float(lumiTag)/1000 
    configMgr.inputLumi = configMgr.outputLumi #deal with this at the sample level
    configMgr.setLumiUnits("fb-1")

    configMgr.histCacheFile = os.getenv("HFRUNDIR")+"/data/"+configMgr.analysisName+".root"
    configMgr.outputFileName = os.getenv("HFRUNDIR")+"/results/"+configMgr.analysisName+"_output.root"
    
    if not configMgr.readFromTree:
        inputFileDict['background'] = ["data/"+configMgr.analysisName+".root"]
        
    configMgr.nomName = "_nom"

    ##########
    ## CUTS ##
    ##########
    
    # define signal regions. please always enclose SRs between () to ease combination
    # note: this assumes events in ntuples already pass SS(10+10+(10)) selection

    configMgr.cutsDict["Rpc2L1bS"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=1 && nJets25>=6 && met>150000 && meff>600000 && met/meff>0.25)"
    configMgr.cutsDict["Rpc2L1bH"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=1 && nJets25>=6 && met>250000 && met/meff>0.2)"

    configMgr.cutsDict["Rpc2L2bS"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=2 && nJets25>=6 && met>200000 && meff>600000 && met/meff>0.25)"
    configMgr.cutsDict["Rpc2L2bH"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=2 && nJets25>=6 && met>0 && meff>1800000 && met/meff>0.15)"
    
    configMgr.cutsDict["Rpc2L0bS"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20==0 && nJets25>=6 && met>150000 && met/meff>0.25)"
    configMgr.cutsDict["Rpc2L0bH"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20==0 && nJets40>=6 && met>250000 && meff>900000)"

    configMgr.cutsDict["Rpc3L0bS"] = "(nSigLep>=3 && Pt_l>20000 && Pt_subl>20000 && nBJets20==0 && nJets40>=4 && met>200000 && meff>600000)"
    configMgr.cutsDict["Rpc3L0bH"] = "(nSigLep>=3 && Pt_l>20000 && Pt_subl>20000 && nBJets20==0 && nJets40>=4 && met>200000 && meff>1600000)"

    configMgr.cutsDict["Rpc3L1bS"] = "(nSigLep>=3 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=1 && nJets40>=4 && met>200000 && meff>600000)"
    configMgr.cutsDict["Rpc3L1bH"] = "(nSigLep>=3 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=1 && nJets40>=4 && met>200000 && meff>1600000)"

    configMgr.cutsDict["Rpc2Lsoft2b"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_l<100000 && Pt_subl>10000 && nBJets20>=2 && nJets25>=6 && met>200000 && meff>600000  && met/meff>0.25)"
    configMgr.cutsDict["Rpc2Lsoft1b"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_l<100000 && Pt_subl>10000 && nBJets20>=1 && nJets25>=6 && met>100000 && met/meff>0.3)"

    configMgr.cutsDict["Rpc3LSS1b"] = "(nSigLep>=3 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=1 && is3LSS>0 && is3LSSproc>0 && !isZee)"
    configMgr.cutsDict["Rpv2L1bH"] = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=1 && nJets50>=6 && meff>2200000)"

    configMgr.cutsDict["AuxRpv2L2bS"] = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=2 && nJets50>=3 && meff>1200000)"
    configMgr.cutsDict["Rpv2L2bS"] = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=2 && nJets50>=3 && meff>1200000 && SSNegative>1)"

    configMgr.cutsDict["Rpv2L1bS"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=1 && nJets50>=4 && meff>1200000 && SSNegative>1)"
    configMgr.cutsDict["AuxRpv2L1bS"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=1 && nJets50>=4 && meff>1200000)"
    configMgr.cutsDict["Rpv2L1bM"] = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=1 && nJets50>=4 && meff>1800000 && SSNegative>1)"
    configMgr.cutsDict["AuxRpv2L1bM"] = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=1 && nJets50>=4 && meff>1800000)"
   
    configMgr.cutsDict["Rpv2L0b"]  = "(nSigLep==2 && Pt_l>20000 && Pt_subl>20000 && nBJets20==0 && nJets40>=6 && meff>1800000 && !isZee)"
    configMgr.cutsDict["AuxRpv2L0b"]  = "(nSigLep==2 && Pt_l>20000 && Pt_subl>20000 && nBJets20==0 && nJets40>=6 && meff>1800000)"
    configMgr.cutsDict["Rpv2L2bH"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=2 && nJets40>=6 && meff>2000000 && !isZee)"
    configMgr.cutsDict["AuxRpv2L2bH"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=2 && nJets40>=6 && meff>2000000)"

    if len(signalRegionList)>1:
        # we have more than one SR to be combined, must make sure they are orthogonal
        configMgr.cutsDict["Rpc2L0bS"]="("+configMgr.cutsDict["Rpc2L0bS"]+"&& !"+configMgr.cutsDict["Rpc2L0bH"]+")"
        configMgr.cutsDict["Rpc2L1bS"]="("+configMgr.cutsDict["Rpc2L1bS"]+"&& !"+configMgr.cutsDict["Rpc2L1bH"]+")"
        configMgr.cutsDict["Rpc2L2bS"]="("+configMgr.cutsDict["Rpc2L2bS"]+"&& !"+configMgr.cutsDict["Rpc2L2bH"]+")"
        configMgr.cutsDict["Rpc3L0bS"]="("+configMgr.cutsDict["Rpc3L0bS"]+"&& !"+configMgr.cutsDict["Rpc3L0bH"]+")"
        configMgr.cutsDict["Rpc3L1bS"]="("+configMgr.cutsDict["Rpc3L1bS"]+"&& !"+configMgr.cutsDict["Rpc3L1bH"]+")"

    # validation/control region

    configMgr.cutsDict["VRWW"] = "(nSigLep==2 && NlepBL==2 &&  nBJets20==0 && nJets50>=2 && met>55000 && meff>650000 && !isZee && Pt_subl>30000 && (dRl1j>0.7 && dRl2j>0.7) && dRll>1.3) && !"+configMgr.cutsDict["Rpc2L0bS"]+" && !"+configMgr.cutsDict["Rpc2L0bH"]+" && !"+configMgr.cutsDict["AuxRpv2L0b"] 
   
    configMgr.cutsDict["VRWZ4j"] = "(nSigLep==3 && NlepBL==3 && Pt_l>20000 && Pt_subl>20000 && nBJets20==0 && nJets25>=4 && meff>450000 && met/sumPtLep<0.7) && !"+configMgr.cutsDict["Rpc2L0bS"]+" && !"+configMgr.cutsDict["Rpc2L0bH"]+" && !"+configMgr.cutsDict["Rpc3L0bS"]+" && !"+configMgr.cutsDict["Rpc3L0bH"]
    configMgr.cutsDict["VRWZ5j"] = "(nSigLep==3 && NlepBL==3 && Pt_l>20000 && Pt_subl>20000 && nBJets20==0 && nJets25>=5 && meff>450000 && met/sumPtLep<0.7) && !"+configMgr.cutsDict["Rpc2L0bS"]+" && !"+configMgr.cutsDict["Rpc2L0bH"]+" && !"+configMgr.cutsDict["Rpc3L0bS"]+" && !"+configMgr.cutsDict["Rpc3L0bH"]

    configMgr.cutsDict["VRttW"] = "(nSigLep==2 && NlepBL==2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=1 && ((SSChannel==1 && nJets25>=3) || (SSChannel==2 && nJets40>=4) || (SSChannel==3 && nJets40>=4)) && met>45000 && meff>550000 && Pt_subl>40000 && sumPtBJet/sumPtJet>0.25) && !"+configMgr.cutsDict["Rpc2L1bS"]+" && !"+configMgr.cutsDict["Rpc2L1bH"]+" && !"+configMgr.cutsDict["Rpc2L2bS"]+" && !"+configMgr.cutsDict["Rpc2L2bH"]+" && !"+configMgr.cutsDict["AuxRpv2L1bM"]+" && !"+configMgr.cutsDict["AuxRpv2L1bS"]+" && !"+configMgr.cutsDict["Rpv2L1bH"]+"&& !"+configMgr.cutsDict["AuxRpv2L2bH"] 

    configMgr.cutsDict["VRttZ"] = "(nSigLep>=3 && Pt_l>20000 && Pt_subl>20000 && mSFOS > 81000 && mSFOS<101000 && nBJets20>=1 && nJets35>=3 && meff>450000) && !"+configMgr.cutsDict["AuxRpv2L1bM"]+" && !"+configMgr.cutsDict["AuxRpv2L1bS"]+" && !"+configMgr.cutsDict["Rpv2L1bH"]+" && !"+configMgr.cutsDict["AuxRpv2L2bH"]+" && !"+configMgr.cutsDict["AuxRpv2L2bS"]+" && !"+configMgr.cutsDict["Rpc2L2bS"]+" && !"+configMgr.cutsDict["Rpc2L2bH"]+" && !"+configMgr.cutsDict["Rpc2L1bS"]+" && !"+configMgr.cutsDict["Rpc2L1bH"]+" && !"+configMgr.cutsDict["Rpc2Lsoft1b"]+" && !"+configMgr.cutsDict["Rpc2Lsoft2b"]+" && !"+configMgr.cutsDict["Rpc3L1bS"]+" && !"+configMgr.cutsDict["Rpc3L1bH"]

    configMgr.cutsDict["VR3bRpvH"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=3 && nJets40>=6 && meff<1800000 && !isZee)"
    configMgr.cutsDict["VR3bRpvS"] = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=3 && nJets50>=3 && meff<1200000 && SSNegative>1)"
    configMgr.cutsDict["VR3bRpcS"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=3 && nJets25>=6 && met>50000 && met<150000 && meff<1200000 && met/meff>0.2*(met/150000))"
    configMgr.cutsDict["VR3bRpcH"]  = "(nSigLep>=2 && Pt_l>20000 && Pt_subl>20000 && nBJets20>=3 && nJets25>=6 && met<250000 && meff<1200000)"


def doFitConfig(inputFileDict, fcName, sigSample=""):

    #---------
    # weights 
    #---------

   #N.B. lumiScaling has to be set to UP,DOWN and nominal in the correct position!!!
   # this takes care of the signal theory unc
    if options.theoryUncertMode.lower() == 'up':
        configMgr.weights = ("wmu_nom","wel_nom","wtrig_nom","wchflip_nom","wjet_nom","mcweight","wttV_nom","wpu_nom_bkg","wpu_nom_sig", "lumiScaling_UP")
    elif options.theoryUncertMode.lower() == 'down':
        configMgr.weights = ("wmu_nom","wel_nom","wtrig_nom","wchflip_nom","wjet_nom","mcweight","wttV_nom","wpu_nom_bkg","wpu_nom_sig", "lumiScaling_DOWN")
    else:
        configMgr.weights = ("wmu_nom","wel_nom","wtrig_nom","wchflip_nom","wjet_nom","mcweight","wttV_nom","wpu_nom_bkg","wpu_nom_sig", "lumiScaling")
        
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

    chflip_UpWeights = replaceStringInTuple(configMgr.weights, "wchflip_nom", "wchflip_up")
    chflip_DownWeights = replaceStringInTuple(configMgr.weights, "wchflip_nom", "wchflip_down")

    pu_UpWeights_bkg =  replaceStringInTuple(configMgr.weights, "wpu_nom_bkg", "wpu_up_bkg")
    pu_DownWeights_bkg =  replaceStringInTuple(configMgr.weights, "wpu_nom_bkg", "wpu_down_bkg")

    pu_UpWeights_sig = replaceStringInTuple(configMgr.weights, "wpu_nom_sig", "wpu_up_sig")
    pu_DownWeights_sig =  replaceStringInTuple(configMgr.weights, "wpu_nom_sig", "wpu_down_sig")

    ttV_UpWeights = replaceStringInTuple(configMgr.weights, "wttV_nom", "wttV_up")
    ttV_DownWeights = replaceStringInTuple(configMgr.weights, "wttV_nom", "wttV_down")

    # attention: the "," at the end here is CRUCIAL
    pdf_UpWeights =  configMgr.weights+ ("wpdf_up",)
    pdf_DownWeights =  configMgr.weights+ ("wpdf_down",)


    #---------------#
    # Build samples #
    #---------------#
    import configWriter
    backgroundDict = {}

    if len(signalRegionList)==1:
        my_mu_SIG = "mu_"+signalRegionList[0]
    else:
        my_mu_SIG = "mu_SIG"

    signalName=str(sigSample)

    if len(sigSample)>0 and not discoveryFit:          

        backgroundDict[signalName] = configWriter.Sample(signalName, ROOT.kPink)
        #backgroundDict[signalName].setFileList(inputFileDict['signal'])
        backgroundDict[signalName].addInputs(inputFileDict['signal'])
        backgroundDict[signalName].setNormByTheory() # assigns lumi uncertainty
        backgroundDict[signalName].setNormFactor(my_mu_SIG, 1., 0., 10)           

    #backgroundDict['ttW'] = configWriter.Sample("ttW", ROOT.kAzure+9)
    #backgroundDict['ttW'].setFileList(inputFileDict['background'])

    #backgroundDict['ttZ'] = configWriter.Sample("ttZ", ROOT.kSpring-5)
    #backgroundDict['ttZ'].setFileList(inputFileDict['background'])

    backgroundDict['ttV'] = configWriter.Sample("ttV", ROOT.kSpring-3)
    #backgroundDict['ttV'].setFileList(inputFileDict['background'])
    backgroundDict['ttV'].addInputs(inputFileDict['background'])

    backgroundDict['ttH'] = configWriter.Sample("ttH", ROOT.kSpring-4)
    #backgroundDict['ttH'].setFileList(inputFileDict['background'])
    backgroundDict['ttH'].addInputs(inputFileDict['background'])

    backgroundDict['FourTop'] = configWriter.Sample("FourTop", ROOT.kSpring-2)
    #backgroundDict['FourTop'].setFileList(inputFileDict['background'])
    backgroundDict['FourTop'].addInputs(inputFileDict['background'])

    backgroundDict['Rare'] = configWriter.Sample("Rare", ROOT.kSpring+8)
    #backgroundDict['Rare'].setFileList(inputFileDict['background'])
    backgroundDict['Rare'].addInputs(inputFileDict['background'])

    backgroundDict['Diboson'] = configWriter.Sample("Diboson", ROOT.kViolet+8)
    #backgroundDict['Diboson'].setFileList(inputFileDict['background'])
    backgroundDict['Diboson'].addInputs(inputFileDict['background'])
    
    #backgroundDict['WW'] = configWriter.Sample("WW", ROOT.kViolet+7)
    #backgroundDict['WW'].setFileList(inputFileDict['background'])

    #backgroundDict['WZ'] = configWriter.Sample("WZ", ROOT.kViolet+6)
    #backgroundDict['WZ'].setFileList(inputFileDict['background'])

    #backgroundDict['ZZ'] = configWriter.Sample("ZZ", ROOT.kViolet+5)
    #backgroundDict['ZZ'].setFileList(inputFileDict['background'])

    fakeBg=configWriter.Sample("Fakes", ROOT.kYellow)    

    for srname,config in fakeCount.iteritems():
        fakeBg.buildHisto(config[0],srname,config[1],config[2])
        fakeBg.buildStatErrors(fakeStatErr[srname],srname,"cuts")

    for srname,config in fakeBinned.iteritems():
        fakeBg.buildHisto(fakeBinned[srname],srname,"meff",800000,700000)
        fakeBg.buildHisto(fakeBinned[srname],srname,"MT2",0,60000)
        fakeBg.buildHisto(fakeBinned[srname],srname,"met",250000,100000)
        fakeBg.buildStatErrors(fakeBinnedErr[srname],srname,"meff")
        fakeBg.buildStatErrors(fakeBinnedErr[srname],srname,"MT2")
        fakeBg.buildStatErrors(fakeBinnedErr[srname],srname,"met")
        
    backgroundDict["Fakes"]=fakeBg

    mischBg=configWriter.Sample("MisCharge", ROOT.kYellow+2)    

    for srname,config in mischCount.iteritems():
        mischBg.buildHisto(config[0],srname,config[1],config[2])
        mischBg.buildStatErrors(mischStatErr[srname],srname,"cuts")

    backgroundDict["MisCharge"]=mischBg
        
    for background in backgroundDict:
        # all stat errors treated as one in the fit
        backgroundDict[background].setStatConfig(True)
        #backgroundDict[background].addSystematic(Systematic("mcstat_"+background, "_nom", "_nom", "_nom", "tree", "shapeStat"))
        
    if len(sigSample)>0  and not discoveryFit:
        print "Turning on mcstat for ",signalName
        # these lines separate the stat error for signals from the rest of the samples
        #backgroundDict[signalName].setStatConfig(False)
        #backgroundDict[signalName].addSystematic(Systematic("mcstat_"+signalName, "_nom", "_nom", "_nom", "tree", "shapeStat"))
        
    # this should have no effect, since in discovery fit the signal sample is not used...
    if len(sigSample)>0  and discoveryFit:
        backgroundDict[signalName].setStatConfig(False)


    ###########################################

    # theory syst on backgrounds

    #if 'TH' in systematicList:
        # WZ and WWjj set later at the channel level
        #backgroundDict['WZ'].addSystematic(Systematic("theoryUncertWZ", configMgr.weights, 1.3, 0.7, "user", "userOverallSys"))
        #backgroundDict['WWjj'].addSystematic(Systematic("theoryUncertWWjj", configMgr.weights, 1.3, 0.7, "user", "userOverallSys"))
        #backgroundDict['Triboson'].addSystematic(Systematic("theoryUncertVVV", configMgr.weights, 1.5, 0.5, "user", "userOverallSys"))
        # ttV set aftwerwards region by region
        #backgroundDict['ttV'].addSystematic(Systematic("theoryUncerttop", configMgr.weights, 1.3, 0.7, "user", "userOverallSys"))
        #backgroundDict['FourTop'].addSystematic(Systematic("theoryUncertFourTop", configMgr.weights, 1.5, 0.5, "user", "userOverallSys"))
        #backgroundDict['ttH'].addSystematic(Systematic("theoryUncertTTH", configMgr.weights, 1.5, 0.5, "user", "userOverallSys"))
        #backgroundDict['Diboson'].addSystematic(Systematic("theoryUncertDiboson", configMgr.weights, 1.3, 0.7, "user", "userOverallSys"))

    #KINEMATIC SYSTEMATICS

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
                'JET_EtaIntercalibration':("JET_EtaIntercalibration_NonClosure__1up","JET_EtaIntercalibration_NonClosure__1down","histoSys"),
                'JET_reso':("JET_JER_SINGLE_NP__1up","nom","histoSysOneSideSym"),
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

    #WEIGHT SYSTEMATICS

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
                #"muTrigStat": ( muon_trig_stat_UpWeights, muon_trig_stat_DownWeights,"overallSys"),              
                #"muTrigSys": ( muon_trig_sys_UpWeights, muon_trig_sys_DownWeights,"overallSys")})
    if 'EG' in systematicList:
        print "AddinG EG weight syst"
        weightDict.update({
                "elID": ( el_id_UpWeights, el_id_DownWeights,"overallSys"),
                "elIso": ( el_iso_UpWeights, el_iso_DownWeights,"overallSys"),
                "elReco": ( el_reco_UpWeights, el_reco_DownWeights,"overallSys"),
                "elChID": ( el_cf_UpWeights, el_cf_DownWeights,"overallSys")})
                #"elTrig": ( el_trig_UpWeights, el_trig_DownWeights,"overallSys")})
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

    if 'ttVSF' in systematicList:
        print "Adding ttVHF scale factor syst"
        weightDict.update({"ttVSF":(ttV_UpWeights, ttV_DownWeights, "overallSys")})    


    for background in backgroundDict:
        
        # these systematics are not assigned for fakes and misCharge
        if (not background.startswith("Fake")) and (not background.startswith("MisCharge")):
            backgroundDict[background].setNormByTheory(True) # assigns lumi uncertainty 
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
        
 
    ################ data ##########
    useDataSample = False
    if useDataSample:
        dataSample = configWriter.Sample("data_nom", ROOT.kBlack)
        dataSample.setData()
        dataSample.setFileList(inputFileDict['data'])
    
    # use hard-coded data
    else:
        from math import sqrt as sqrt
        dataHand=configWriter.Sample("Data", ROOT.kYellow) 
        dataHand.setData()
        for srname,config in dataCounts.iteritems():
            dataHand.buildHisto(config[0],srname,config[1],config[2])
            print "built histo with contents ",config[0][0]



    #------------------#
    # Build fit config #
    #------------------#

    if len(sigSample)>0:          
        grid = options.signalGridName
        if signalName.strip('signal') in signalRunnumberToMassesDict[grid]:
            masses = signalRunnumberToMassesDict[grid][signalName.strip('signal')]
            fcName=fcName+'_{0}_{1}'.format(masses[0],masses[1])
            
    print "Setting fcName to",fcName,"sigSample is",sigSample
    myFitConfig = configMgr.addFitConfig(fcName)

    if options.useStat:
        myFitConfig.statErrThreshold = 0.01 
    else:
        myFitConfig.statErrThreshold = None

    measurement = myFitConfig.addMeasurement(name = "NormalMeasurement", lumi=1.0, lumiErr=0.032)
    if not discoveryFit:
        measurement.addPOI(my_mu_SIG)

    # add data
    if useDataSample: myFitConfig.addSamples(dataSample)
    else: myFitConfig.addSamples(dataHand)

    # add bgs and signals
    for background in backgroundDict:
        myFitConfig.addSamples(backgroundDict[background]) # this includes signal, if not doing discovery

    if len(sigSample)>0 and not discoveryFit:          
        myFitConfig.setSignalSample(backgroundDict[signalName])
        # these must be the same, or CombineWorkSpaces will complain later due to a badly thought ReplaceAll...
        # signalName has NO masses, like signal123456. masses must be added to the jsons downstream by a separate python script
        myFitConfig.hypoTestName = signalName

        
    #----------------#
    # Build channels #
    #----------------#
    ############## starting to define signal regions ###########################
    #

    # list of VRs from command line, cuts and ranges from dictionary filled above 
    for validationRegionName in validationRegionList:
        legendTitle = ''
        #if validationRegionName.startswith("VRttZ"):
        vChan = myFitConfig.addValidationChannel("cuts", [validationRegionName],  1,0.5,1.5)
        vChan.useOverflowBin = False
        vChan.title = '{0} Region'.format(validationRegionName)
        addDataDrivenSyst(vChan,validationRegionName)
        addSRTheorySyst(vChan,validationRegionName)

    ############## starting to define signal regions ###########################
    for signalRegionName in signalRegionList:
        print signalRegionName
        ### Rpc2L1bS ###
        if signalRegionName.startswith("Rpc2L1bS"):
            cutnamebase="Rpc2L1bS"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  3, 800000, 2300000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                # add here fake and misch systematics
                if(len(validationRegionList) !=0):
                    addDataDrivenSyst(sChan,validationRegionList[0])
                    addSRTheorySyst(sChan,validationRegionList[0])
                else:
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### Rpc2L1bH ###
        elif signalRegionName.startswith("Rpc2L1bH"):
            cutnamebase="Rpc2L1bH"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  3, 800000, 2300000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                # add here fake and misch systematics                                                                                                                                                                                        
                if(len(validationRegionList) !=0):
                    addDataDrivenSyst(sChan,validationRegionList[0])
                    addSRTheorySyst(sChan,validationRegionList[0])
                else:
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### Rpc2L2bS ###
        elif signalRegionName.startswith("Rpc2L2bS"):
            cutnamebase="Rpc2L2bS"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist: 
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)   
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100) 
                        measurement.addPOI("mu_Disc_%s" % cutname) 
                    # add here fake and misch systematics
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)      
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### Rpc2L2bH ###
        elif signalRegionName.startswith("Rpc2L2bH"):
            cutnamebase="Rpc2L2bH"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist: 
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)   
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100) 
                        measurement.addPOI("mu_Disc_%s" % cutname) 
                    # add here fake and misch systematics
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)      
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
       ### Rpc2L0bS ###
        elif signalRegionName.startswith("Rpc2L0bS"):
            cutnamebase="Rpc2L0bS"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  3, 700000, 1600000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### Rpc2L0bH ###
        elif signalRegionName.startswith("Rpc2L0bH"):
            cutnamebase="Rpc2L0bH"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  3, 1500000, 3000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False        
        ### Rpc3L0bS ###
        elif signalRegionName.startswith("Rpc3L0bS"):
            cutnamebase="Rpc3L0bS"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("MT2", [cutname],  3, 0, 300000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### Rpc3L0bH ###
        elif signalRegionName.startswith("Rpc3L0bH"):
            cutnamebase="Rpc3L0bH"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("MT2", [cutname],  3, 0, 300000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### Rpc3L1bS ###
        elif signalRegionName.startswith("Rpc3L1bS"):
            cutnamebase="Rpc3L1bS"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("MT2", [cutname],  3, 0, 300000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### Rpc3L1bH ###
        elif signalRegionName.startswith("Rpc3L1bH"):
            cutnamebase="Rpc3L1bH"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("MT2", [cutname],  3, 0, 300000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
         ### Rpc2Lsoft2b ###
        elif signalRegionName.startswith("Rpc2Lsoft2b"):
            cutnamebase="Rpc2Lsoft2b"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  3, 1500000, 3000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### Rpc2Lsoft1b ###
        elif signalRegionName.startswith("Rpc2Lsoft1b"):
            cutnamebase="Rpc2Lsoft1b"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  3, 1500000, 3000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
         ### Rpc3LSS1b ###
        elif signalRegionName.startswith("Rpc3LSS1b"):
            cutnamebase="Rpc3LSS1b"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  3, 1500000, 3000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### Rpv2L1bM ###
        elif signalRegionName.startswith("Rpv2L1bM"):
            cutnamebase="Rpv2L1bM"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### Rpv2L2bH ###
        elif signalRegionName.startswith("Rpv2L2bH"):
            cutnamebase="Rpv2L2bH"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### Rpv2L1bS ###
        elif signalRegionName.startswith("Rpv2L1bS"):
            cutnamebase="Rpv2L1bS"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False        
        ### Rpv2L1bH ###
        elif signalRegionName.startswith("Rpv2L1bH"):
            cutnamebase="Rpv2L1bH"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False        
        ### Rpv2L0b ###
        elif signalRegionName.startswith("Rpv2L0b"):
            cutnamebase="Rpv2L0b"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ###Rpv2L2bS###
        elif signalRegionName.startswith("Rpv2L2bS"):
            cutnamebase="Rpv2L2bS"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False

        ############################ VALIDATION REGIONS ############################
        ### VRttW ###
        elif signalRegionName.startswith("VRttW"):
            cutnamebase="VRttW"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    # add here fake and misch systematics                                                                                                                           
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### VRWW ###
        elif signalRegionName.startswith("VRWW"):
            cutnamebase="VRWW"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    # add here fake and misch systematics                                                                                                                           
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)

                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### VRWZ4j ###
        elif signalRegionName.startswith("VRWZ4j"):
            cutnamebase="VRWZ4j"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    # add here fake and misch systematics                                                                                                                           
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)

                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### VRWZ5j ###
        elif signalRegionName.startswith("VRWZ5j"):
            cutnamebase="VRWZ5j"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    # add here fake and misch systematics
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)

                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### VR3bRpcS###
        elif signalRegionName.startswith("VR3bRpcS"):
            cutnamebase="VR3bRpcS"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    # add here fake and misch systematics
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### VR3bRpcH###
        elif signalRegionName.startswith("VR3bRpcH"):
            cutnamebase="VR3bRpcH"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### VR3bRpvS###
        elif signalRegionName.startswith("VR3bRpvS"):
            cutnamebase="VR3bRpvS"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### VR3bRpvH###
        elif signalRegionName.startswith("VR3bRpvH"):
            cutnamebase="VR3bRpvH"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
        ### VRttZ ###
        elif signalRegionName.startswith("VRttZ"):
            cutnamebase="VRttZ"
            chanlist=['']
            if 'split' in signalRegionName:
                chanlist=['ee','em','mm']
            for chan in chanlist:
                cutname=cutnamebase+chan
                if 'bin' in signalRegionName:
                    sChan = myFitConfig.addChannel("meff", [cutname],  4, 600000, 2000000)
                    sChan.useOverflowBin = True
                else:
                    sChan = myFitConfig.addChannel("cuts", [cutname],  1,0.5,1.5)
                    if discoveryFit:
                        sChan.addDiscoverySamples([cutname],[1.],[0.],[100.],[ROOT.kMagenta])
                        sChan.getSample('DiscoveryMode_'+cutname).setNormFactor("mu_Disc_%s" % cutname, 1., 0., 100)
                        measurement.addPOI("mu_Disc_%s" % cutname)
                    # add here fake and misch systematics                                                                                                                           
                    addDataDrivenSyst(sChan,cutname)
                    addSRTheorySyst(sChan,cutname)
                myFitConfig.setSignalChannels(sChan)
                sChan.logY = False
              
        elif signalRegionName == "": continue
        else:
            raise Exception("ERROR unexpected signal region {0}".format(signalRegionName))
            
#################### Setting Style ##############################
        
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
    if configMgr.blindVR:
        entry = leg.AddEntry("","Toy Data (%.1f fb^{-1}, #sqrt{s}=13 TeV)"%configMgr.outputLumi,"p") 
    else:
        entry = leg.AddEntry("","Data", "p") 
    entry.SetMarkerColor(myFitConfig.dataColor)
    entry.SetMarkerStyle(20)

    #entry = leg.AddEntry("","tt + W","f")
    #entry.SetLineColor(ROOT.kBlack)
    #entry.SetLineWidth(1)
    #entry.SetFillColor(backgroundDict['ttW'].color)
    #entry.SetFillStyle(compFillStyle)
    
    #entry = leg.AddEntry("","tt + Z","f") 
    #entry.SetLineColor(ROOT.kBlack)
    #entry.SetLineWidth(1)
    #entry.SetFillColor(backgroundDict['ttZ'].color)
    #entry.SetFillStyle(compFillStyle)

    entry = leg.AddEntry("","tt + V","f")
    entry.SetLineColor(ROOT.kBlack)
    entry.SetLineWidth(1)
    entry.SetFillColor(backgroundDict['ttV'].color)
    entry.SetFillStyle(compFillStyle)

    entry = leg.AddEntry("","tt + H","f")
    entry.SetLineColor(ROOT.kBlack)
    entry.SetLineWidth(1)
    entry.SetFillColor(backgroundDict['ttH'].color)
    entry.SetFillStyle(compFillStyle)

    entry = leg.AddEntry("","Diboson","f") 
    entry.SetLineColor(ROOT.kBlack)
    entry.SetLineWidth(1)
    entry.SetFillColor(backgroundDict['Diboson'].color)
    entry.SetFillStyle(compFillStyle)

    #entry = leg.AddEntry("","WW","f")
    #entry.SetLineColor(ROOT.kBlack)
    #entry.SetLineWidth(1)
    #entry.SetFillColor(backgroundDict['WW'].color)
    #entry.SetFillStyle(compFillStyle)

    #entry = leg.AddEntry("","WZ","f")
    #entry.SetLineColor(ROOT.kBlack)
    #entry.SetLineWidth(1)
    #entry.SetFillColor(backgroundDict['WZ'].color)
    #entry.SetFillStyle(compFillStyle)

    #entry = leg.AddEntry("","ZZ","f")
    #entry.SetLineColor(ROOT.kBlack)
    #entry.SetLineWidth(1)
    #entry.SetFillColor(backgroundDict['ZZ'].color)
    #entry.SetFillStyle(compFillStyle)

    entry = leg.AddEntry("","Fakes","f") 
    entry.SetLineColor(ROOT.kBlack)
    entry.SetLineWidth(1)
    entry.SetFillColor(backgroundDict['Fakes'].color)
    entry.SetFillStyle(compFillStyle)

    entry = leg.AddEntry("","MisCharge","f") 
    entry.SetLineColor(ROOT.kBlack)
    entry.SetLineWidth(1)
    entry.SetFillColor(backgroundDict['MisCharge'].color)
    entry.SetFillStyle(compFillStyle)

    entry = leg.AddEntry("","Rare","f") 
    entry.SetLineColor(ROOT.kBlack)
    entry.SetLineWidth(1)
    entry.SetFillColor(backgroundDict['Rare'].color)
    entry.SetFillStyle(compFillStyle)

    entry = leg.AddEntry("","FourTop","f")
    entry.SetLineColor(ROOT.kBlack)
    entry.SetLineWidth(1)
    entry.SetFillColor(backgroundDict['FourTop'].color)
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

def addBinnedDataDrivenSyst(sChan,cutname):
    if sChan.hasSample("Fakes") and 'FAKES' in systematicList:
        print "Adding FAKES syst in "+cutname
        print fakeBinnedSystErr[cutname][0]
        print fakeBinnedSystErr[cutname][1]
        print fakeBinnedSystErr[cutname][2]
        sysfake=Systematic("syst_fake_"+cutname, "1.", 1+fakeBinnedSystErr[cutname][0],1-fakeBinnedSystErr[cutname][0], "user","histoSys")
        sChan.getSample("Fakes").addSystematic(sysfake)
        #sChan.getSample("Fakes").addShapeSys(sysfake,"Nominal_binned_fake_syst","High_binned_fake_syst","Low_binned_fake_syst")
    else:
        print "WARNING: no Fakes bg for region",cutname
    #if sChan.hasSample("MisCharge") and 'MISCH' in systematicList:
     #   print "Adding MISCH syst"
      #  sysmisch=Systematic("syst_misch_"+cutname, "1.", 1+mischSystErr[cutname][0],1-mischSystErr[cutname][0], "user","userOverallSys")
       # sChan.getSample("MisCharge").addSystematic(sysmisch)
    #else:
     #   print "WARNING: no MisCharge bg for region ",cutname

    
def addDataDrivenSyst(sChan,cutname):
    if sChan.hasSample("Fakes") and 'FAKES' in systematicList:
        print "Adding FAKES syst in "+cutname
        print fakeSystErr[cutname][0]
        sysfake=Systematic("syst_fake_"+cutname, "1.", 1+fakeSystErr[cutname][0],1-fakeSystErr[cutname][0], "user","userOverallSys")
        sChan.getSample("Fakes").addSystematic(sysfake)
    else:
        print "WARNING: no Fakes bg for region",cutname
    if sChan.hasSample("MisCharge") and 'MISCH' in systematicList:
        print "Adding MISCH syst"
        sysmisch=Systematic("syst_misch_"+cutname, "1.", 1+mischSystErr[cutname][0],1-mischSystErr[cutname][0], "user","userOverallSys")
        sChan.getSample("MisCharge").addSystematic(sysmisch)
    else:
        print "WARNING: no MisCharge bg for region ",cutname

# this is to add SR-speciic theory uncertainties
def  addSRTheorySyst(sChan,cutname):

    from math import sqrt as sqrt
   
    thUnc_ttV = {
        "Rpc2L0bH"    : 0.2865, #0.14, 0.2500
        "Rpc2L0bS"    : 0.2981, #0.13, 0.2683
        "Rpc2L1bH"    : 0.1401, #0.14, 0.0052
        "Rpc2L1bS"    : 0.1715, #0.14, 0.0990
        "Rpc2L2bH"    : 0.2168, #0.16, 0.1463
        "Rpc2L2bS"    : 0.1500, #0.15, 0.0000
        "Rpc2Lsoft1b" : 0.2265, #0.13, 0.1855
        "Rpc2Lsoft2b" : 0.1411, #0.14, 0.0174
        "Rpc3LSS1b"   : 0.1300, #0.13, 0.0000
        "Rpc3L1bS"    : 0.1304, #0.13, 0.0099
        "Rpc3L1bH"    : 0.1406, #0.14, 0.0132
        "Rpc3L0bH"    : 0.3205, #0.16, 0.2777
        "Rpc3L0bS"    : 0.1669, #0.14, 0.0909
        "Rpv2L0b"     : 0.3377, #0.18, 0.2857
        "Rpv2L1bM"    : 0.3054, #0.14, 0.2714
        "Rpv2L2bH"    : 0.1512, #0.15, 0.0189
        "Rpv2L1bH"    : 0.1788, #0.17, 0.0555
        "Rpv2L1bS"    : 0.1401, #0.14, 0.0061   
        "Rpv2L2bS"    : 0.1525, #0.14, 0.0604
        "VRttW"       : 0.1300,   
        "VRWW"        : 0.1300,
        "VRWZ4j"      : 0.1300,
        "VRWZ5j"      : 0.1300,
        "VR3bRpcS"    : 0.2395,
        "VR3bRpcH"    : 0.2528,
        "VR3bRpvS"    : 0.2438,
        "VR3bRpvH"    : 0.2422,
        "VRttZ"       : 0.1300,
        }

    
    systtV=Systematic("theoryUncertTTbarV_"+cutname, "1.", 1+thUnc_ttV[cutname],1-thUnc_ttV[cutname], "user","userOverallSys")

    # FIXME top ->ttV
    if sChan.hasSample("ttZ") and 'TH' in systematicList:
        print "Adding ttV syst for ttZ"
        sChan.getSample("ttZ").addSystematic(systtV)

    if sChan.hasSample("ttW") and 'TH' in systematicList:
        print "Adding ttV syst for ttW"
        sChan.getSample("ttW").addSystematic(systtV)

    if sChan.hasSample("ttV") and 'TH' in systematicList:
        print "Adding ttV syst for ttV"
        sChan.getSample("ttV").addSystematic(systtV)

    thUnc_Diboson = {
        "Rpc2L0bH"    : 0.32,
        "Rpc2L0bS"    : 0.34,
        "Rpc2L1bH"    : 0.35,
        "Rpc2L1bS"    : 0.35,
        "Rpc2L2bH"    : 0.34,
        "Rpc2L2bS"    : 0.34,
        "Rpc2Lsoft1b" : 0.37,
        "Rpc2Lsoft2b" : 0.36,
        "Rpc3LSS1b"   : 0.24,
        "Rpc3L1bS"    : 0.31,
        "Rpc3L1bH"    : 0.31,
        "Rpc3L0bH"    : 0.27,
        "Rpc3L0bS"    : 0.30,  
        "Rpv2L0b"     : 0.34,
        "Rpv2L1bM"    : 0.31,
        "Rpv2L1bH"    : 0.34,
        "Rpv2L1bS"    : 0.29,
        "Rpv2L2bH"    : 0.34,
        "Rpv2L2bS"    : 0.32,
        "VRttW"       : 0.31,
        "VRWW"        : 0.31,
        "VRWZ4j"      : 0.34,
        "VRWZ5j"      : 0.37,
        "VR3bRpcS"    : 0.2973,
        "VR3bRpcH"    : 0.2984,
        "VR3bRpvS"    : 0.3378,
        "VR3bRpvH"    : 0.3374,
        "VRttZ"       : 0.33,
        }

    sysDiboson=Systematic("theoryUncertDiboson_"+cutname, "1.", 1+thUnc_Diboson[cutname],1-thUnc_Diboson[cutname], "user","userOverallSys")

    if sChan.hasSample("Diboson") and 'TH' in systematicList:
        print "Adding Diboson syst to Diboson"
        sChan.getSample("Diboson").addSystematic(sysDiboson)

    if sChan.hasSample("WZ") and 'TH' in systematicList:
        print "Adding Diboson syst to WZ"
        sChan.getSample("WZ").addSystematic(sysDiboson)

    if sChan.hasSample("ZZ") and 'TH' in systematicList:
        print "Adding Diboson syst to ZZ"
        sChan.getSample("ZZ").addSystematic(sysDiboson)

    if sChan.hasSample("WW") and 'TH' in systematicList:
        print "Adding Diboson syst to WW"
        sChan.getSample("WW").addSystematic(sysDiboson)

    thUnc_Rare={
        'Rpc2L1bS'    : 0.50,
        'Rpc2L1bH'    : 0.50,
        'Rpc2L2bS'    : 0.50, 
        'Rpc2L2bH'    : 0.50, 
        'Rpc2L0bS'    : 0.50,
        'Rpc2L0bH'    : 0.50,
        'Rpc3L0bS'    : 0.50,
        'Rpc3L0bH'    : 0.50,
        'Rpc3L1bS'    : 0.50,
        'Rpc3L1bH'    : 0.50,
        'Rpc2Lsoft2b' : 0.50,
        'Rpc2Lsoft1b' : 0.50,
        'Rpc3LSS1b'   : 0.50,
        'Rpv2L1bS'    : 0.50,
        'Rpv2L1bM'    : 0.50,
        'Rpv2L1bH'    : 0.50,
        'Rpv2L2bH'    : 0.50,
        'Rpv2L0b'     : 0.50,
        'Rpv2L2bS'    : 0.50,
        'VRWW'        : 0.11,
        'VRWZ4j'      : 0.25,
        'VRWZ5j'      : 0.25,
        'VRttW'       : 0.20,
        "VR3bRpcS"    : 0.30,
        "VR3bRpcH"    : 0.30,
        "VR3bRpvS"    : 0.50,
        "VR3bRpvH"    : 0.50,
        'VRttZ'        :0.50,
        }

    sysRare=Systematic("theoryUncertRare_"+cutname, "1.", 1+thUnc_Rare[cutname],1-thUnc_Rare[cutname], "user","userOverallSys")

    if sChan.hasSample("Rare") and 'TH' in systematicList:
        print "Adding Rare syst to Rare"
        sChan.getSample("Rare").addSystematic(sysRare)

    if sChan.hasSample("FourTop") and 'TH' in systematicList:
        print "Adding Rare syst to FourTop"
        sChan.getSample("FourTop").addSystematic(sysRare)

    if sChan.hasSample("ttH") and 'TH' in systematicList:
        print "Adding Rare syst to ttH"
        sChan.getSample("ttH").addSystematic(sysRare)

runAll()
