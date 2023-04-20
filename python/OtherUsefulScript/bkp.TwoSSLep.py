################################################################
## In principle all you have to setup is defined in this file ##
################################################################
from configManager import configMgr
from ROOT import kBlack,kWhite,kGray,kRed,kPink,kMagenta,kViolet,kBlue,kAzure,kCyan,kTeal,kGreen,kSpring,kYellow,kOrange
from configWriter import TopLevelXML,Measurement,ChannelXML,Sample
from systematic import Systematic
from math import sqrt
import sys

# Read options from command line
my_args = sys.argv
for i,w in enumerate(my_args):
  if 'TwoSSLep.py' in w:
    my_args=my_args[i+1:]
# default values
susy_model='mSUGRA' # or 'mSUGRA'
xsec_unc='nominal'
mode='AllChSRI'

for w in my_args:
  if(w.upper()=='GTT'): susy_model='Gtt'
  elif(w.upper()=='MSUGRA'): susy_model='mSUGRA'
  elif(w.lower()=='xsec-up'): xsec_unc='up'
  elif(w.lower()=='xsec-nom'): xsec_unc='nominal'
  elif(w.lower()=='xsec-down'): xsec_unc='down'
  elif(w.lower()=='mode-allchsri'): mode='AllChSRI'
  elif(w.lower()=='mode-allchsrii'): mode='AllChSRII'
  
if(susy_model=='Gtt' and (mode=='AllChSRI')): SigSample = open('SigSample_GTT12.txt', 'r')
elif(susy_model=='mSUGRA' and (mode=='AllChSRI')): SigSample = open('SigSample_MSUGRA12.txt', 'r')
elif(susy_model=='Gtt' and (mode=='AllChSRII')): SigSample = open('SigSampleSR2_GTT12.txt', 'r')
elif(susy_model=='mSUGRA' and (mode=='AllChSRII')): SigSample = open('SigSampleSR2_MSUGRA12.txt', 'r')

# Setup for ATLAS plotting
#from ROOT import gROOT
#gROOT.LoadMacro("./macros/AtlasStyle.C")
#import ROOT
#ROOT.SetAtlasStyle()

##########################
# Set observed and expected number of events in counting experiment
lumiError = 0.036 	# Relative luminosity uncertainty
##########################

# Setting the parameters of the hypothesis test
#configMgr.nTOYs=5000
configMgr.calculatorType=2 # 2=asymptotic calculator, 0=frequentist calculator
configMgr.testStatType=3   # 3=one-sided profile likelihood test statistic (LHC default)
configMgr.nPoints=20       # number of values scanned of signal-strength for upper-limit determination of signal strength.

##########################

# Set uncorrelated systematics for bkg and signal (1 +- relative uncertainties)
ucb_ChMisID = Systematic("ucb", configMgr.weights, 1.4,0.6, "user","userOverallSys")
ucb_TtX = Systematic("ucb", configMgr.weights,1.4,0.6, "user","userOverallSys")
ucb_Dibosons = Systematic("ucb", configMgr.weights, 1.4,0.6, "user","userOverallSys")
ucb_Fakes = Systematic("ucb", configMgr.weights, 1.4,0.6, "user","userOverallSys")

ucs = Systematic("ucs", configMgr.weights, 1.3,0.7, "user","userOverallSys")

# correlated systematic between background and signal (1 +- relative uncertainties)
#corb = Systematic("cor",configMgr.weights, [1.1],[0.9], "user","userHistoSys")
#cors = Systematic("cor",configMgr.weights, [1.15],[0.85], "user","userHistoSys")

# Give the analysis a name
configMgr.analysisName = "TwoSSLep_"+susy_model+'_xsec_'+xsec_unc+'_mode_'+mode
configMgr.outputFileName = "results/%s_Output.root"%configMgr.analysisName


# Define cuts
configMgr.cutsDict["SR"] = "1."

# Define weights
configMgr.weights = "1."

# bkg estimation in SRI
if(mode=='AllChSRI'):
    nbkgChMisId = 0.0110786 + 0.00944916
    nbkgTtX = 0.0935974 + 0.214508 + 0.127071
    nbkgDibosons = 0.0819813 
    nbkgFakes = 0.501798 + 0.0544298
    # stat err
    StatERRnbkgChMisId = sqrt(0.00663371**2 + 0.00594734**2)
    StatERRnbkgTtX = sqrt(0.0397955**2 + 0.0500718**2 + 0.037671**2)
    StatERRnbkgDibosons = sqrt(0.0612149**2)
    StatERRnbkgFakes = sqrt(0.2**2 + 0.37268**2 + 0.0573155**2)
    ndata = 1.
if(mode=='ElElChSRI'):
    nbkgChMisId = 0.0110786
    nbkgTtX = 0.0935974
    nbkgDibosons = 0.
    nbkgFakes = 0.
    # stat err
    StatERRnbkgChMisId = 0.00663371
    StatERRnbkgTtX = 0.0397955
    StatERRnbkgDibosons = 0.
    StatERRnbkgFakes = 0.2
    ndata = 1.
if(mode=='ElMuChSRI'):
    nbkgChMisId = 0.00944916
    nbkgTtX = 0.214508
    nbkgDibosons = 0.0819813
    nbkgFakes = 0.501798
    # stat err
    StatERRnbkgChMisId = 0.00594734
    StatERRnbkgTtX = 0.0500718
    StatERRnbkgDibosons = 0.0612149
    StatERRnbkgFakes = 0.37268
    ndata = 0.
if(mode=='MuMuChSRI'):
    nbkgChMisId = 0.
    nbkgTtX = 0.127071
    nbkgDibosons = 0.
    nbkgFakes = 0.0544298
    # stat err
    StatERRnbkgChMisId = 0.
    StatERRnbkgTtX = 0.037671
    StatERRnbkgDibosons = 0.
    StatERRnbkgFakes = 0.0573155
    ndata = 0.

if(mode=='AllChSRII'):
    nbkgChMisId = 0.00484878 + 0.00913124
    nbkgTtX = 0.0511571 + 0.162517 + 0.0761903
    nbkgDibosons = 0. 
    nbkgFakes = 0.0408169
    # stat err
    StatERRnbkgChMisId = sqrt(0.00541203**2 + 0.00514742**2)
    StatERRnbkgTtX = sqrt(0.0252978**2 + 0.0433248**2 + 0.0283649**2)
    StatERRnbkgDibosons = 0. 
    StatERRnbkgFakes = sqrt(0.2**2 + 0.366478**2 + 0.1**2)
    ndata = 0.
if(mode=='ElElChSRII'):
    nbkgChMisId = 0.00484878
    nbkgTtX = 0.0511571
    nbkgDibosons = 0.
    nbkgFakes = 0.
    # stat err
    StatERRnbkgChMisId = 0.00541203
    StatERRnbkgTtX = 0.0252978
    StatERRnbkgDibosons = 0.
    StatERRnbkgFakes = 0.2
    ndata = 0.
if(mode=='ElMuChSRII'):
    nbkgChMisId = 0.00913124
    nbkgTtX = 0.162517
    nbkgDibosons = 0.
    nbkgFakes = 0.408169
    # stat err
    StatERRnbkgChMisId = 0.00514742
    StatERRnbkgTtX = 0.0433248
    StatERRnbkgDibosons = 0.
    StatERRnbkgFakes = 0.366478
    ndata = 0.
if(mode=='MuMuChSRII'):   
    nbkgChMisId = 0.
    nbkgTtX = 0.0761903
    nbkgDibosons = 0.
    nbkgFakes = 0.
    # stat err
    StatERRnbkgChMisId = 0.
    StatERRnbkgTtX = 0.0283649
    StatERRnbkgDibosons = 0.
    StatERRnbkgFakes = 0.1
    ndata = 0.
    
#Define background samples
# List of background and their plotting colours
BSamples=[]
BkgChMisId = Sample("BkgChMisId",kGreen-9)
BkgChMisId.setStatConfig(True)
BkgChMisId.buildHisto([nbkgChMisId],"SR","cuts") # nbkg
BkgChMisId.buildStatErrors([StatERRnbkgChMisId],"SR","cuts") #nbkgErr
#BkgChMisId.addSystematic(corb)
BkgChMisId.addSystematic(ucb_ChMisID)
BSamples.append(BkgChMisId)
BkgTtX = Sample("BkgTtX",kViolet-9)
BkgTtX.setStatConfig(True)
BkgTtX.buildHisto([nbkgTtX],"SR","cuts") # nbkg
BkgTtX.buildStatErrors([StatERRnbkgTtX],"SR","cuts") #nbkgErr
#BkgTtX.addSystematic(corb)
BkgTtX.addSystematic(ucb_TtX)
BSamples.append(BkgTtX)
BkgDibosons = Sample("BkgDibosons",kBlue-9)
BkgDibosons.setStatConfig(True)
BkgDibosons.buildHisto([nbkgDibosons],"SR","cuts") # nbkg
BkgDibosons.buildStatErrors([StatERRnbkgDibosons],"SR","cuts") #nbkgErr
#BkgDibosons.addSystematic(corb)
BkgDibosons.addSystematic(ucb_Dibosons)
BSamples.append(BkgDibosons)
BkgFakes = Sample("BkgFakes",kRed-9)
BkgFakes.setStatConfig(True)
BkgFakes.buildHisto([nbkgFakes],"SR","cuts") # nbkg
BkgFakes.buildStatErrors([StatERRnbkgFakes],"SR","cuts") #nbkgErr
#BkgFakes.addSystematic(corb)
BkgFakes.addSystematic(ucb_Fakes)
BSamples.append(BkgFakes)

#sort in alphabetic order
#BSamples.sort(key=lambda x: x.name)

#List of bkg samples
bgdsamples=[]
for sam in BSamples:
   bgdsamples.append(sam)

Samples = []
nsig = []
statERR = []
for name in SigSample:
    name = name.rstrip('\n\t')
    if(name[0] == '#'):continue
    Samples.append(name.split()[0])
    n=float(name.split()[1])
    if(xsec_unc=='up'): n+=float(name.split()[3])
    elif(xsec_unc=='down'): n-=float(name.split()[3])
    nsig.append(n)  
    statERR.append(float(name.split()[2]))
    
sSamples =[]
for i,s in enumerate(Samples):
    _Samples = Sample(s,kBlue)
    _Samples.setNormFactor("mu_Sig",1.,0.,10.)
    _Samples.setStatConfig(True)
    _Samples.setNormByTheory()    
    _Samples.buildHisto([nsig[i]],"SR","cuts")
    _Samples.buildStatErrors([statERR[i]],"SR","cuts")
    #_Samples.addSystematic(cors)
    _Samples.addSystematic(ucs)
    sSamples.append(_Samples)
#*****************************************
 
dataSample = Sample("Data",kBlack)
dataSample.setData()
dataSample.buildHisto([ndata],"SR","cuts")

# #**************
# # Discovery fit
# #**************
# ## you run -w -f -i --> you can see mu_SIG: and this represent the signal (makes a discovery fit)
# ##         -i ; r1=GenerateFitAndPlot(configMgr.topLvls[1])
# ##  -->  the amount of expected signal is diplayed in red: is not correspond to the observed data
# ### --> to translate it into a qualitative exclusion:
# ###        -w -l -i --> the computed upper limit & expected limit (EXCLUSION)

# #Fit config instance
# discoveryFitConfig = configMgr.addTopLevelXML("Discovery")
# #Samples
# discoveryFitConfig.addSamples(bgdsamples)
# discoveryFitConfig.addSamples([dataSample])
# #add measurements
# meas=discoveryFitConfig.addMeasurement(name="NormalMeasurement",lumi=1.0,lumiErr=lumiError)
# meas.addPOI("mu_SIG")
# #Channel
# srBin = discoveryFitConfig.addChannel("cuts",["SR"],1,0.5,1.5)
# srBin.addDiscoverySamples(["SR"],[1.],[0.],[100.],[kMagenta]) 
# discoveryFitConfig.setSignalChannels([srBin])

# ##**************************************
# ## end discovery fit
# ##***************************************

# Background only fit
# Define top-level
exclusionFitConfig = configMgr.addTopLevelXML("Exclusion")
#Samples
exclusionFitConfig.addSamples(bgdsamples)
exclusionFitConfig.addSamples([dataSample])
#add measurements
meas = exclusionFitConfig.addMeasurement(name="NormalMeasurement",lumi=1.0,lumiErr=lumiError)
meas.addPOI("mu_Sig")    
#Channel
chan = exclusionFitConfig.addChannel("cuts",["SR"],1,0.5,1.5)
exclusionFitConfig.setSignalChannels([chan])  

#*********************
# Exclusion fit MSUGRA / Simplified Model grid
#*********************
for sig in sSamples:
    myTopLvl = configMgr.addTopLevelXMLClone(exclusionFitConfig,"Sig_%s"%sig.name)
    myTopLvl.addSamples(sig)  
    myTopLvl.setSignalSample(sig)
#**************************
# end exclusion fit MSUGRA
#**************************
 

   
# These lines are needed for the user analysis to run
# Make sure file is re-made when executing HistFactory
if configMgr.executeHistFactory:
    if os.path.isfile("data/%s.root"%configMgr.analysisName):
        os.remove("data/%s.root"%configMgr.analysisName) 
