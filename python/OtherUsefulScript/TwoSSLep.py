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
  if 'TwoSSLep.py' in w:
    my_args=my_args[i+1:]
# default values
susy_model='Gtt'
mode='SRII'
is_batch=False
jobID=0
print 'Arguments after cleaning',my_args
for w in my_args:
  print 'reading argument',w
  if(w.upper()=='GTT'): 
    print 'Set model Gtt'
    susy_model='Gtt'
  elif(w.upper()=='MSUGRA'): 
    print 'Set model mSUGRA'
    susy_model='mSUGRA'
  elif(w.lower()=='mode-allchsri'): 
    print 'Set SR1'
    mode='SRI'
  elif(w.lower()=='mode-allchsrii'): 
    print 'Set SR2'
    mode='SRII'
  elif(w.lower()=='batch'): is_batch=True
  elif(w.lower()[0:6]=='jobid='): jobID=int(w.lower()[7:])
  else:
    print 'Unknown argument',w,'of size',len(w)


if(susy_model=='Gtt' and (mode=='SRI')): SigSample = open('SigSample_GTT.txt', 'r')
elif(susy_model=='mSUGRA' and (mode=='SRI')): SigSample = open('SigSample_MSUGRA.txt', 'r')
elif(susy_model=='Gtt' and (mode=='SRII')): SigSample = open('SigSampleSR2_GTT.txt', 'r')
elif(susy_model=='mSUGRA' and (mode=='SRII')): SigSample = open('SigSampleSR2_MSUGRA.txt', 'r')

print 'SigSample = ',SigSample

##########################
# Set observed and expected number of events in counting experiment
lumiError = 0.036 	# Relative luminosity uncertainty
##########################

#run with nominal / up / down cross section
configMgr.fixSigXSec=True


# Setting the parameters of the hypothesis test
#configMgr.nTOYs=3000
configMgr.calculatorType=2 # 2=asymptotic calculator, 0=frequentist calculator
configMgr.testStatType=3   # 3=one-sided profile likelihood test statistic (LHC default)
configMgr.nPoints=20       # number of values scanned of signal-strength for upper-limit determination of signal strength.

##########################
if(mode=='SRI'):
    all_sys=0.82/3.43 # relative (*100 -> in %)
    jes_sys=0.057     # to obtain the absolute one * totalBKG value
    all_no_jes_sys=sqrt(all_sys**2 - jes_sys**2)
    #### Set uncorrelated systematics for bkg and signal (1 +- relative uncertainties)
    ucb_bkg = Systematic("ucb_bkg", configMgr.weights, 1.+all_no_jes_sys,1.-all_no_jes_sys, "user","userOverallSys")
    #not here since is corr
    #ucs = Systematic("ucs", configMgr.weights, 1.3,0.7, "user","userOverallSys")
    ##### correlated systematic between background and signal (1 +- relative uncertainties)
    # JES err
    corb_bkg = Systematic("cor_jes", configMgr.weights, 1.+jes_sys,1.-jes_sys, "user","userOverallSys")
    cors = Systematic("cor_jes", configMgr.weights, 1.3,0.7, "user","userOverallSys")   
elif(mode=='SRII'):
    all_sys=0.26/1.04 # relative (*100 -> in %)
    jes_sys=0.106     # to obtian the absolute one * totalBKG value
    all_no_jes_sys=sqrt(all_sys**2 - jes_sys**2)
    #### Set uncorrelated systematics for bkg and signal (1 +- relative uncertainties)
    ucb_bkg = Systematic("ucb_bkg", configMgr.weights, 1.+all_no_jes_sys,1.-all_no_jes_sys, "user","userOverallSys")
    #not here since is corr
    #ucs = Systematic("ucs", configMgr.weights, 1.3,0.7, "user","userOverallSys")
    ##### correlated systematic between background and signal (1 +- relative uncertainties)
    # JES err
    corb_bkg = Systematic("cor_jes", configMgr.weights, 1.+jes_sys,1.-jes_sys, "user","userOverallSys")
    cors = Systematic("cor_jes", configMgr.weights, 1.3,0.7, "user","userOverallSys")   

# Give the analysis a name
configMgr.analysisName = "TwoSSLep_"+susy_model+'_mode_'+mode
configMgr.outputFileName = "results/%s_Output.root"%configMgr.analysisName


# Define cuts
configMgr.cutsDict["SR"] = "1."

# Define weights
configMgr.weights = "1."

# bkg estimation in SRI
if(mode=='SRI'):
    nbkg = 3.43
    stat_bkg = 0.8 
    ndata = 4.

elif(mode=='SRII'):
    nbkg = 1.04
    stat_bkg = 0.38
    ndata = 2.
    
#Define background samples
# List of background and their plotting colours

BSamples=[]
Bkg = Sample("Bkg",kGreen-9)
Bkg.setStatConfig(True)
Bkg.buildHisto([nbkg],"SR","cuts") # nbkg
Bkg.buildStatErrors([stat_bkg],"SR","cuts") #nbkgErr
Bkg.addSystematic(corb_bkg)
Bkg.addSystematic(ucb_bkg)
BSamples.append(Bkg)

#sort in alphabetic order
#BSamples.sort(key=lambda x: x.name)

#List of bkg samples
bgdsamples=[]
for sam in BSamples:
   bgdsamples.append(sam)

Samples = []
nsig = []
stat_sig = []
syst_sig=[]
for name in SigSample:
    name = name.rstrip('\n\t')
    if(name[0] == '#'):continue
    Samples.append(name.split()[0])
    n=float(name.split()[1])
    syst_sig.append(float(name.split()[3]))
    nsig.append(n)  
    stat_sig.append(float(name.split()[2]))
    

sSamples =[]
for i,s in enumerate(Samples):
    _Samples = Sample(s,kBlue)
    _Samples.setNormFactor("mu_Sig",1.,0.,50.)
    _Samples.setStatConfig(True)
    _Samples.setNormByTheory()    
    _Samples.buildHisto([nsig[i]],"SR","cuts")
    _Samples.buildStatErrors([stat_sig[i]],"SR","cuts")
    _Samples.addSystematic(cors)
    # print 'Arguments:',[1.+syst_sig[i]/nsig[i]],[1.-syst_sig[i]/nsig[i]]
    xsecupT = 1.+syst_sig[i]/nsig[i]
    xsecdownT = 1.-syst_sig[i]/nsig[i]
    xsecsys = Systematic("SigXSec", configMgr.weights,xsecupT,xsecdownT, "user","userOverallSys")
    _Samples.addSystematic(xsecsys)
    #_Samples.addSystematic(ucs)
    sSamples.append(_Samples)
#*****************************************
 
dataSample = Sample("Data",kBlack)
dataSample.setData()
dataSample.buildHisto([ndata],"SR","cuts")


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
chan = exclusionFitConfig.addChannel("cuts",["SR"],1,0.,1.)
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
