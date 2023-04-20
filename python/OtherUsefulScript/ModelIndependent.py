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
print 'Arguments',my_args
for i,w in enumerate(my_args):
  if 'ModelIndependent.py' in w:
    my_args=my_args[i+1:]
# default values
mode='SRI'

print 'Arguments after cleaning',my_args
for w in my_args:
  if(w.lower()=='mode-allchsri'): 
    print 'Set SR1'
    mode='SRI'
  elif(w.lower()=='mode-allchsrii'): 
    print 'Set SR2'
    mode='SRII'
  else:
    print 'Unknown argument',w,'of size',len(w)


##########################
# Set observed and expected number of events in counting experiment
lumiError = 0.036 	# Relative luminosity uncertainty
##########################

#run with nominal / up / down cross section
configMgr.fixSigXSec=False


# Setting the parameters of the hypothesis test
configMgr.nTOYs=3000
configMgr.calculatorType=0 # 2=asymptotic calculator, 0=frequentist calculator
configMgr.testStatType=3   # 3=one-sided profile likelihood test statistic (LHC default)
configMgr.nPoints=20       # number of values scanned of signal-strength for upper-limit determination of signal strength.

##########################
if(mode=='SRI'):
    all_err = 1.14/3.43 # syst and stat on bkg
    print " \n XXX   all_err =", all_err
    #### Set error on bkg
    ucb_bkg = Systematic("ucb_bkg", configMgr.weights, 1.+all_err,1.-all_err, "user","userOverallSys")
    
elif(mode=='SRII'):
    all_err = 0.47/1.04 # syst and stat on bkg
    print " \n XXX   all_err =", all_err
    #### Set error on bkg
    ucb_bkg = Systematic("ucb_bkg", configMgr.weights, 1.+all_err,1.-all_err, "user","userOverallSys")

# Give the analysis a name
configMgr.analysisName = "ModelIndependent"+'_mode_'+mode
configMgr.outputFileName = "results/%s_Output.root"%configMgr.analysisName


# Define cuts
configMgr.cutsDict["SR"] = "1."

# Define weights
configMgr.weights = "1."

# bkg estimation in SRI
if(mode=='SRI'):
    nbkg = 3.43
    ndata = 4.

elif(mode=='SRII'):
    nbkg = 1.04
    ndata = 2.
    
#Define background samples
# List of background and their plotting colours

Bkg = Sample("Bkg",kGreen-9)
Bkg.setStatConfig(True)
Bkg.buildHisto([nbkg],"SR","cuts") # nbkg
Bkg.addSystematic(ucb_bkg)

nsig = 1
sigSample = Sample("Sig",kPink)
sigSample.setNormFactor("mu_Sig",1.,0.,10.)
sigSample.setStatConfig(True)
sigSample.setNormByTheory() 
sigSample.buildHisto([nsig],"SR","cuts")
 
dataSample = Sample("Data",kBlack)
dataSample.setData()
dataSample.buildHisto([ndata],"SR","cuts")


# Background only fit
# Define top-level
exclusionFitConfig = configMgr.addTopLevelXML("SplusB")
#Samples
exclusionFitConfig.addSamples([Bkg,sigSample,dataSample])  
#exclusionFitConfig.setSignalSample(sigSample)

#add measurements
meas = exclusionFitConfig.addMeasurement(name="NormalMeasurement",lumi=1.0,lumiErr=lumiError)
meas.addPOI("mu_Sig")    

meas.addParamSetting("Lumi","const",1.0)

#Channel
chan = exclusionFitConfig.addChannel("cuts",["SR"],1,0.,1.)
exclusionFitConfig.setSignalChannels([chan])  

# These lines are needed for the user analysis to run
# Make sure file is re-made when executing HistFactory
if configMgr.executeHistFactory:
    if os.path.isfile("data/%s.root"%configMgr.analysisName):
        os.remove("data/%s.root"%configMgr.analysisName) 
