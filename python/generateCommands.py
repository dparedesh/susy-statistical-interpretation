#!/usr/bin/env python

#these paths must be absolute
#where histfitter is

from argparse import ArgumentParser
import pathUtilities, FillJsonFilesWithMissingInfo, signalSameSignTools

import os

histFitterDir = pathUtilities.histFitterSource()
# where results of histfitter are stored
histFitterUserDir=pathUtilities.histFitterUser()

####### to define before running #######

lumiTag='138965'   #in pb-1
#runNameTag =  '_CISF2Test2_'
runNameTag =  '_FullRun2Strong_'

########################################


runNameTag += lumiTag
runMacro='fitConfigSS3L.py'
plottingMacro='plotContours.py'
plottingMacroBest='plotBestGrid.py'

runToys = False
doUL=False

Nominal="Nominal"
Up="Up"
Down="Down"

#theoryUnc=[Up,Down,Nominal]
theoryUnc=[Nominal]

doBlind=""

#Need to run independently in every SR before activating the makeBest option. 
makeBest=False

gridList = None

jobLength = 1
jobLengthUL = 1

import sys
sys.path.append(pathUtilities.histFitterTopDirectory())
excludedPoints = [
#        "mc16_13TeV:mc16_13TeV.376777.MGPy8EG_A14N23LO_GG_2stepWZ_1000_650_475_300.deriv.DAOD_SUSY2.e7140_a875_r9364_p3736/",
#        "mc16_13TeV:mc16_13TeV.376781.MGPy8EG_A14N23LO_GG_2stepWZ_1000_950_925_900.deriv.DAOD_SUSY2.e7140_a875_r9364_p3736/",
#		"mc16_13TeV:mc16_13TeV.377108.MadGraphPythia8EvtGen_A14N_GG_2stepWZ_1100_950_875_800.deriv.DAOD_SUSY2.e7467_s3126_r9364_p3840/",
#		"mc16_13TeV:mc16_13TeV.377109.MadGraphPythia8EvtGen_A14N_GG_2stepWZ_1100_1000_950_900.deriv.DAOD_SUSY2.e7467_s3126_r9364_p3840/",
#"mc16_13TeV:mc16_13TeV.376749.MGPy8EG_A14N23LO_GG_Rpvlampp331_1600_800.deriv.DAOD_SUSY2.e7163_a875_r9364_p3759/"
        ]
NotexcludedPoints = []

targetregionDict=[]


parser =  ArgumentParser(description='This script is designed for the SUSY SS3L analsys')
parser.add_argument("--fit",action='store_true',help="Perform the fit.") 
parser.add_argument("--fitmodel",help="Kind of fit to be done", choices=["excl","disc","bkg"]) 
parser.add_argument("--Sys",default=None,help="Chose the sys you want to include. Usually ALL or NONE. Otherwise choose the one that you want to test among: EG,JET,MU,MET,FT,PU,TRIG,FAKES,CHFLIP,MISCH,TH") 
parser.add_argument("--merge",action='store_true',help="Necessary step to merge results before plotting. Note that this is needed also if you do not run in batch, since some file renaming is performed.") 
parser.add_argument("--doBlind",default=None,help="Provide a comma separated list of the regions to blind. Avariable options are SR,CR,VR or ALL")
parser.add_argument("--doUL",action='store_true',help="Compute upper limits for --fit option, merge UL results for --merge. If --plot, it will draw the gray numbers of the UL on the cross-section in the 2D contour plots") 
parser.add_argument("--plot",action='store_true',help="Produce the contour exclusion plot.") 
parser.add_argument("--drawCLs",action='store_true',help="Show gray numbers CLs on the exclusion plots")
parser.add_argument("--drawCLsExp",action='store_true',help="Show gray numbers CLs (expected) on the exclusion plots")
parser.add_argument("--makeBest",action=None,help="Provide a comma separated list of the regions to combine") 
parser.add_argument("--Model", default=None,help="Model to process. e.g: Mc16SusyC1N2_offshellWZ. Choices can be viewd in susyGridFile dir. The model must have a file in that dir to tell pkg the signals that this model had")
parser.add_argument("--SigNameSchema" ,default="SP:4,LSP:5", help="signal sample naming schema which is used to get correct mass from a sample name. SR:X,LSP:Y. X and Y means the position for a  string splitted by '_'")
parser.add_argument("--SR",default=None,help="Provide a comma separated list of the SRs to process. If more than one, they will be statistically combined in the fit. The region must be previosly defined in the file fitConfig.py. Examples:Rpc2L2b,Rpc2L0b,Rpc2L1b,Rpc3LSS1b,Rpv2L")
parser.add_argument("--VR",default=None,help="Provide a comma separated list of the regions to be used as VRs. If more than one they will be used simultaneously in the fit. The region must be previosly defined in the file fitConfig.py")
parser.add_argument("--CR",default=None,help="Provide a comma separated list of the regions to be used as CRs. If more than one they will be used simultaneously in the fit.  The region must be previosly defined in the file fitConfig.py")
parser.add_argument("--extraFitConfig",default=None,help="All extra options to be passed to the fitConfig.py file. Check available options in that file. Argument must be passed in quotas, i.e. --extraFitConfig '--bkgToNormalize WZ:CRWZ5j,ttV:CRttV'")
parser.add_argument("--extraHarvestToContours",default=None,help="Extra options to be passed to harvestToContours.py. Check available options in that HF script. Argument must be passed in quotas, i.e. --extraHarvestToContours '--interpolation cubic'")
parser.add_argument("--batch",action="store_true",help="Run the fits on lxbatch using bsub-compatible queue by default (HTCondor if --extra options are given). In this case, inputs must be on eos (or other xrdcp-compatible filesystem), so you don't kill afs with multiple parallel access. Set pathUtilities.eosDataDirectory properly. HistFitter is run locally on the worker nodes, and the contents of the results/ folder are copied back to HFRUNDIR at the end of the job. The data/ folder is not copied.")
parser.add_argument("--extra",help="provides system, queue and storage required for batch. Default setup is <syst:bsub,queue:8nh,storage:20000>",default="syst:bsub,queue:8nh,storage:20000")
parser.add_argument("--resubmit",help="Name of the file with failed jobs. Will work only with --batch  and --extra system:condor")
parser.add_argument("--makeBestGrid",action="store_true",help="This is to combine results for more than one grid (model). For example Gtt and GttCompr. Not coded yet!!")
parser.add_argument("--yields",action='store_true',help="Additionally extract signal yields for 'Main' result (i.e. no slots) and nom variation.") 
parser.add_argument("--yieldsSamples",default=None,help="Provide comma separated list of samples to be shown at tables. Work in progress...")
parser.add_argument("--SysBreak",action='store_true',help="Get Sys breakdown tables") 
parser.add_argument("--FitResults",action='store_true',help="Get Fitresults and ranking and pulling plots") 
parser.add_argument("--allPostFit",action='store_true',help="Set --yields, --merge and --plot to True.") 
parser.add_argument("--parallize",action='store_true',help="parallize all signal points, only active it when doing exclusion fit") 
parser.add_argument("--signalGroupIndex",help="Give the index to id the file") 
parser.add_argument("--signalList",help="Give the input signal as format as signal370102_SP_LSP") 
parser.add_argument("--WithSigMass",help="True will include mass information to tree name",action='store_true')
parser.add_argument("--debug",help="Performs an interactive fit on one single dataset. The argument *must* be the dataset number (Ex. --debug 372320). The script will loop over all the grids and find the DSID for you. All other fit parameters in the main script apply.") 
parser.add_argument("--dry",action='store_true',help="Set dry option") 
parser.add_argument("--draw1D",action="store_true",help="Draw upper limits on the cross-section as a function of the generated mass point")

options = parser.parse_args()

if runNameTag.count(".") >= 1:
    print("Don't use dots in the runNameTag... they will complicate lifes later... ABORTING!") 
    sys.exit(1)

condor_queues=["espresso","microcentury","longlunch","workday","tomorrow","testmatch","nextweek"]
bsub_queues=['8nm','1nh','8nh','1nd','2nd','1nw','2nw']

#Fill batch_options to submit jobs, i.e: system, queue, storage.
batch_opt={'syst':'','queue':'','storage':''}
if options.extra is not None:
    for k in options.extra.split(","):
        if 'syst' in k or 'queue' in k or 'storage' in k:
            batch_opt[k.split(':')[0]]=k.split(':')[1]

    if 'condor' in batch_opt['syst']:
        if batch_opt['queue'] not in condor_queues:
            print('The chosen queue is not compatible with the condor system. Choose among:',condor_queues)
            sys.exit(1)

        if batch_opt['storage']=='':
            batch_opt['storage']='20000'

    if 'bsub' in batch_opt['syst'] and batch_opt['queue'] not in bsub_queues:
        print('The chosen queue is not compatible with the bsub system. Choose among: ',bsub_queues)
        sys.exit(1)


systematicList=str(options.Sys)

sysname=systematicList

if sysname is not None: sysname.replace(',','_')
else: sysname = "NONE"

runNameTag = runNameTag+"_"+sysname

if options.doUL:
    doUL = True

combinedRegions={}
if options.makeBest is not None:    
    makeBest = True
    fullList=list(set(options.makeBest.split(","))) #save only unique values for SRs

    if ',' in options.SR:
        print("Sorry, for makeBest option *NO* statistical combination of SRs is allowed... Aborting!")
        sys.exit(1)

    if options.SR in fullList: fullList.remove(options.SR) 

    if len(fullList)==0:
        print "There are no signal regions to combine (check the names that you are providing to --makeBest argument)... Aborting"
        sys.exit(1)

    print "The following signal regions will be combined with ",options.SR," : ",fullList

    combinedRegions[options.SR]=fullList

debugDS=""
if options.debug is not None:
    # last argument must be dataset to debug
    if options.debug is not "":
        debugDS=options.debug
        print "ASKED TO DEBUG DSID",debugDS, runNameTag
        runNameTag=runNameTag+"_debug"
    else:
        print("The dataset number must be provided. Ex: --debug 372320")
        sys.exit(1)   

if options.resubmit is not None:
    if not os.path.isfile(options.resubmit):
        print('File with failed jobs does not exist -> Aborting.')
        sys.exit(1)

#signal regions must be always taken first!!
if options.SR is not None:
    signalRegions=options.SR.split(",")
    for s_reg in signalRegions:
        targetregionDict.append(s_reg)

if options.CR is not None:
    controlRegions=options.CR.split(",")
    for c_reg in controlRegions:
        targetregionDict.append(c_reg)

if options.VR is not None:
    validationRegions=options.VR.split(",")
    for v_reg in validationRegions:
        targetregionDict.append(v_reg)



#Model must be used just for exclusion fits
if options.Model is not None:
    gridList=options.Model

    from massCheck import massCheck
    print "Running grid {0}".format(gridList)
    massCheck(pathUtilities.histFitterTopDirectory()+'/susyGridFiles/'+gridList,SigNameSchema=options.SigNameSchema)

else:
    if options.fitmodel=="disc": gridList="Discovery"
    elif options.fitmodel=="excl":
        sys.exit("--> You need to provide a model for an exclusion fit... ABORTING!")
    else: gridList="bkgOnly"
  

tagRegion=""
for targetregion in targetregionDict:
    tagRegion+="_"+targetregion


runNameTag=runNameTag+tagRegion


jobsSubmitted=''

blindtag=''
fittypetag = options.fitmodel


if options.doBlind is not None:
    blindtag="blind"+options.doBlind.replace(',','_') 
    runNameTag=runNameTag+'_'+blindtag

def main():
    

    if not (options.fit or options.merge or options.plot or options.yields or options.SysBreak or options.FitResults or options.allPostFit):
        parser.error("Please specify at least one argument :--fit, --merge, --plot, --yields, --SysBreak, --FitResults, --allPostFit + [--dry]")
 

    grid=gridList

    targetregions=tagRegion


    from odict import odict
    extraOptionsDict = odict()

    # this is the "main" line in the exclusion plots, with the yellow band
    extraOptionsDict[runNameTag] =" "# the MAIN result 

    if options.SR is not None: extraOptionsDict[runNameTag] +=" --signalRegions "+str(options.SR)
    if options.CR is not None: extraOptionsDict[runNameTag] +=" --controlRegions "+str(options.CR)
    if options.VR is not None: extraOptionsDict[runNameTag] +=" --validationRegions "+str(options.VR)

    if options.Sys is not None: 
        extraOptionsDict[runNameTag] +=" --sysList " + str(options.Sys) 
    else:
        extraOptionsDict[runNameTag] +=" --sysList None"

    if options.doBlind is not None: extraOptionsDict[runNameTag] +=" --doBlind "+str(options.doBlind)     
    if options.extraFitConfig is not None: extraOptionsDict[runNameTag] +=" "+str(options.extraFitConfig) 

    gridPointDict={}
    if options.fitmodel=="excl": gridPointDict = makeGridPointDict(grid)
    else: gridPointDict["bkgOnly"]="bkgOnly"

            
    # start fits
    if options.fit:

        for theoryUncert in theoryUnc:

            # also parallize the slots
            for extraOptions in extraOptionsDict:

                # exclude up and down for slots
                if not theoryUncert==Nominal and "Slot" in extraOptions:
                    continue

                signalGroupIndex=0
                # also parallize the signal groups. first for exclusion
                if options.fitmodel=="excl":
                    if options.parallize:
                        if len(options.signalList)==0:# or len(options.signalGroupIndex)==0:
                            print "Need input signal list and signalGroupIndex"
                            sys.exit(1) 
                        runSequentially(grid, extraOptionsDict,extraOptions,options.signalList,theoryUncert, False, options.dry)

                        if doUL and theoryUncert==Nominal: 
                            runSequentially(grid, extraOptionsDict,extraOptions,options.signalList,theoryUncert, True, options.dry)

                    else:
                        for subListConcat in yieldSubList(gridPointDict[grid][theoryUncert], jobLength):
        
                            if options.batch:

                                runBatch(runNameTag,grid, extraOptionsDict,extraOptions,subListConcat,theoryUncert, False ,signalGroupIndex,options.dry,targetregions,blindtag)

                                if doUL and theoryUncert==Nominal:
                                    runBatch(runNameTag,grid,extraOptionsDict,extraOptions,subListConcat,theoryUncert, True ,signalGroupIndex,options.dry,targetregions,blindtag)

                            else:
       
                                runSequentially(grid, extraOptionsDict,extraOptions,subListConcat,theoryUncert, False, options.dry)

                                if doUL and theoryUncert==Nominal:
                                    runSequentially(grid, extraOptionsDict,extraOptions,subListConcat,theoryUncert, True, options.dry)


                            signalGroupIndex+=1
                else:
                    if theoryUncert==Nominal:

                        signalGroupIndex=0

                        if options.batch:
                            runBatch(runNameTag,grid, extraOptionsDict,extraOptions,"bkgOnly",theoryUncert, False ,signalGroupIndex,options.dry,targetregions,blindtag)
                        else:
                            runSequentially(grid, extraOptionsDict,extraOptions,"bkgOnly",theoryUncert, False, options.dry)

                        signalGroupIndex+=1


        
        #create file with submitted jobs (needed to check the job' status in condor)
        if options.resubmit is None and options.batch and 'condor' in batch_opt['syst']:

            outputJobs=open(pathUtilities.pythonDirectory()+'/Jobs_'+grid+runNameTag+"_"+options.fitmodel+".txt",'w')
            outputJobs.write(jobsSubmitted)
            outputJobs.close()
        
   

    if options.yields or options.allPostFit:
	print red("This option has not been tested!!: yields or allPostFit")

        import subprocess

        
        # additionally extract signal yields for "Main" result (i.e. no slots) and nom variation
        import CollectSignalYields, subprocess,os
        cmd = 'mkdir -p '+pathUtilities.histFitterUser()+'/Yields/'+grid+targetregions+fittypetag
        subprocess.call(cmd+'\n',shell=True)
        CollectSignalYields.CollectYields(grid,Nominal,runNameTag,"",targetregions,fittypetag)
        CollectSignalYields.CollectSignalYields(grid,Nominal,runNameTag,"",targetregions,fittypetag)
        


    if options.FitResults:
	print red("This option has not been tested!!: FitResults")
	
        import CollectSignalYields, subprocess,os
        cmd = 'mkdir -p '+pathUtilities.histFitterUser()+'/NP_Info/'+grid+targetregions+fittypetag
        cmd1 = 'mkdir -p '+pathUtilities.histFitterUser()+'/RankingPlots/'+grid+targetregions+fittypetag
        subprocess.call(cmd+'\n'+cmd1+'\n',shell=True)
        CollectSignalYields.NPInfo(grid,Nominal,runNameTag,"",targetregions,fittypetag)

    if options.SysBreak:
	print red("This option has not been tested!!: SysBreak")

        import CollectSignalYields, subprocess,os
        cmd = 'mkdir -p '+pathUtilities.histFitterUser()+'/Sys_BreakDown/'+grid+targetregions+fittypetag
        subprocess.call(cmd+'\n',shell=True)
        CollectSignalYields.SysBreakDown(grid,Nominal,runNameTag,"",targetregions,fittypetag)
   


    if options.merge or options.allPostFit:
        runMerging(grid, extraOptionsDict, options.dry) 
    

        
    # plot always sequentially, once per grid
    if options.plot or options.allPostFit:
        runPlottingSequentially(grid, extraOptionsDict, True, True, True, options.dry) 

def generateMergeCommands(grid, extraOptionsDict,extraOptions,theoryUncert):

    commands=[]
    tag=theoryUncert+extraOptions

    import glob,os

    pattern=grid+"_"+tag+"_excl_"
    patternUL=grid+"_"+tag+"_UL_"

    print "Pattern", pattern


    firstJobFileName=glob.glob(os.getenv("HFRUNDIR")+"/results/"+pattern+"Job*_output.root")[0]

    print "got template filenames",firstJobFileName


    #replacing Job* for empty string to get general merged job.
    #Avoid hardcoding Job00 since sometimes Job00 fail causing the crash of the code.
    localName=firstJobFileName.split("/")[-1]
    subList=localName.split("_")
    l = [subList.index(i) for i in subList if 'Job' in i]

    if len(l)==1:
        localName=localName.replace("_"+subList[l[0]],"")
    else:
        print "- There is more than one _Job_ string in filename... ABORTING. Don't use _Job*_ to name your jobs since this is already used to tag the code"
        sys.exit(1)


    newFileName=localName[:]
    print "- Name of merged file: ",newFileName

    commands.append("mkdir -p $HFRUNDIR/results/merged")
    commands.append("hadd -f $HFRUNDIR/results/merged/"+newFileName.replace("output.root","output_hypotest.root")+" $HFRUNDIR/results/"+pattern+"Job*_output_hypotest.root ;")
    commands.append("ln -sf $HFRUNDIR/results/merged/"+newFileName.replace("output.root","output_hypotest.root")+" $HFRUNDIR/results/ ;")

    # upper limit only for nominal non slot
    if theoryUncert==Nominal and not "Slot" in extraOptions and doUL:

        newFileNameUL=newFileName[:] #.replace("excl","UL")[:]

        print "preparing UL merges",newFileNameUL

        commands.append("hadd -f $HFRUNDIR/results/merged/"+newFileNameUL.replace("output.root","output_hypotest.root").replace(Nominal,'upperlimit')+" $HFRUNDIR/results/"+patternUL+"Job*_output_upperlimit.root ;")
        commands.append("ln -sf $HFRUNDIR/results/merged/"+newFileNameUL.replace("output.root","output_hypotest.root").replace(Nominal,'upperlimit')+" $HFRUNDIR/results/ ;")

   
    return commands


def generateHistFitterCommands(grid, extraOptionsDict,extraOptions,subListConcat,theoryUncert,doUL=False,doWorkspace=True,signalGroupIndex=0):
    commandsList = []
    mergeCommandDict = {}

    if options.parallize:
        signalGroupIndex = options.signalGroupIndex


    setupCommand =  'cd {0}  \n '.format(histFitterDir)

    ULtag="_"+fittypetag

    exclMode = 'p'
    if doUL:
        exclMode = 'pl'
        if doWorkspace==False: exclMode="l"

        ULtag="_UL"


    if options.debug is not None:
        exclMode+='f'

    #print "   in sublist loop ",subListConcat
    outNameStem = theoryUncert+extraOptions

    if fittypetag =="excl":
        if runToys : commandsList.append('{0} HistFitter.py -twfx -u " --lumiTag {7} --signalGridName {1} --additionalOutName {5}{10}_Job{8:02d} --signalList {2}  --theoryUncertMode {3} {4}" {9}/python/{11} \n HistFitter.py -p -{6} -u " --lumiTag {7} --signalGridName {1}  --additionalOutName {5}{10}_Job{8:02d} --signalList {2}  --theoryUncertMode {3} {4} --SigNameSchema {12}"  {9}/python/{11};'.format(setupCommand, grid, subListConcat, theoryUncert, extraOptionsDict[extraOptions], outNameStem, exclMode,lumiTag,signalGroupIndex,pathUtilities.histFitterTopDirectory(),ULtag,runMacro,options.SigNameSchema))         

        else:

            if doWorkspace: 
                commandsList.append('{0} HistFitter.py -F {10} -D \'corrMatrix\' -twfx -u " --lumiTag {6} --signalGridName {1} --additionalOutName {5}{9}_Job{7:02d} --signalList {2}  --theoryUncertMode {3} {4} --SigNameSchema {12}" -d {8}/python/{11} \n'.format(setupCommand, grid, subListConcat, theoryUncert, extraOptionsDict[extraOptions], outNameStem,lumiTag,int(signalGroupIndex),pathUtilities.histFitterTopDirectory(),ULtag, fittypetag,runMacro,options.SigNameSchema))
            else:
                commandsList.append('cp -r {3}/results/{0}_{1}_excl_Job{2:02d}_output.root {3}/results/{0}_{1}_UL_Job{2:02d}_{3}_output.root \n'.format(grid,outNameStem,int(signalGroupIndex),pathUtilities.histFitterSource()))
                commandsList.append('cp -r {3}/results/{0}_{1}_excl_Job{2:02d}_output_hypotest.root {3}/results/{0}_{1}_UL_Job{2:02d}_output_hypotest.root \n'.format(grid,outNameStem,int(signalGroupIndex),pathUtilities.histFitterSource()))
                commandsList.append('mkdir -p {3}/results/{0}_{1}_UL_Job{2:02d} \n'.format(grid,outNameStem,int(signalGroupIndex),pathUtilities.histFitterSource()))
                commandsList.append('cp -r {3}/results/{0}_{1}_excl_Job{2:02d}/*{4}* {3}/results/{0}_{1}_UL_Job{2:02d}/ \n'.format(grid,outNameStem,int(signalGroupIndex),pathUtilities.histFitterSource(),subListConcat))
                commandsList.append(setupCommand)

            commandsList.append('{12} HistFitter.py -F {10} -{5} -u " --lumiTag {6} --signalGridName {0}  --additionalOutName {4}{9}_Job{7:02d} --signalList {1}  --theoryUncertMode {2} {3}  --SigNameSchema {13}" -d {8}/python/{11}'.format(grid, subListConcat, theoryUncert, extraOptionsDict[extraOptions], outNameStem, exclMode,lumiTag,int(signalGroupIndex),pathUtilities.histFitterTopDirectory(),ULtag, fittypetag,runMacro,setupCommand,options.SigNameSchema))

    else:

        #before,after,corrMatrix, allPlots
        commandsList.append('{0} HistFitter.py -F {10} -D \'before,after,corrMatrix\' -twfx -u " --lumiTag {7} --signalGridName {1} --additionalOutName {5}{9} --signalList {2}  --theoryUncertMode {3} {4}  --SigNameSchema {12}" -d {8}/python/{11}'.format(setupCommand, grid, subListConcat, theoryUncert, extraOptionsDict[extraOptions], outNameStem, exclMode,lumiTag,pathUtilities.histFitterTopDirectory(),ULtag, fittypetag,runMacro,options.SigNameSchema))       

    #print "returning commands ",commandsList

    return commandsList

def runSequentially(grid, extraOptionsDict,extraOptions,subListConcat,theoryUncert, doupper,dryRun=False):
    import subprocess, os
    commandsList=[]

    #When running locally if doupper=True then there is no need of creating again the workspace (this option helps to save time)
    buildWorkspace=True
    if doupper==True: 
        buildWorkspace=False


    if debugDS=="":
        commandsList = generateHistFitterCommands(grid, extraOptionsDict,extraOptions,subListConcat,theoryUncert,doupper,buildWorkspace)

    else:
        # check here if the DS we look for is in this bunch
        if debugDS in subListConcat:
            print "replacing list of signals with the one to debug: ",debugDS
            subListConcat="signal"+debugDS
            commandsList = generateHistFitterCommands(grid, extraOptionsDict,extraOptions,subListConcat,theoryUncert,doupper,buildWorkspace)

    for command in commandsList:
        #print command
        if not dryRun: 
            print "launching command... "
            print command;
            subprocess.call(command+"\n", shell=True)

def runMerging(grid, extraOptionsDict, dryRun=False):

    commands=[]

    print "#########  Generating merging commands... ######## "
    for theoryUncert in theoryUnc:        
        # also parallize the slots
        for extraOptions in extraOptionsDict:
            # exclude up/down for slots
            if theoryUncert==Nominal or not "Slot" in extraOptions:
                commands+=generateMergeCommands(grid, extraOptionsDict,extraOptions,theoryUncert)


    print "########## Launching merging commands... ########"
    import subprocess
    for command in commands:
        print command
        if not dryRun: 
            subprocess.call(command, shell=True)
    

def runBatch(runNameTag,gridName, extraOptionsDict,extraOptions,subListConcat,theoryUncert, doupper, signalGroupIndex,dryRun,targetregions,blindtag):


    if pathUtilities.isFreiburg():
        setupcommand='''#!/bin/bash


export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase;
source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh;
lsetup "root 6.18.04-x86_64-centos7-gcc8-opt"
export PYTHONPATH={0}:$PYTHONPATH
export HFRUNDIR=$TMPDIR

printenv

'''.format(pathUtilities.pythonDirectory())

        copyInputs='''


cd $HFRUNDIR

mkdir InputTrees

echo "copying files"

ln -s {0}/data.{1}.root InputTrees/data.{1}.root 
ln -s {0}/background.{1}.root InputTrees/background.{1}.root
ln -s {0}/signal.{1}.root InputTrees/signal.{1}.root
ls -la InputTrees

'''.format(pathUtilities.remoteDataDirectory(),lumiTag)
        
    # LXPLUS
    else:
        setupcommand='''#!/bin/bash
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source /cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/user/atlasLocalSetup.sh
export HFRUNDIR={0}
export PYTHONPATH={1}:$PYTHONPATH
SUSYDIR="{2}"
'''.format(histFitterDir,pathUtilities.pythonDirectory(),histFitterDir)

        setupcommand+='''
echo "Now sourcing setup:"
XCWD=$PWD
cd $SUSYDIR

export BUILD="x86_64-slc6-gcc62-opt"
export PYTHONBUILD="x86_64-slc6-gcc62-opt"
export ROOTVERSION="6.10.06"
export PYTHONVERSION="2.7.13"
export GCCVERSION="6.2.0"
if [[ `hostname -f` = b*.cern.ch ]] || [[ `hostname -f` = l*.cern.ch ]]; then
    echo "INFO: hostname matches l*.cern.ch: setting up gcc and python from afs"
    echo "Setting up gcc version ${GCCVERSION} ..."
    source /cvmfs/sft.cern.ch/lcg/contrib/gcc/${GCCVERSION}/x86_64-slc6/setup.sh 
    echo "Setting up python version ${PYTHONVERSION} ..."
    export PATH="/cvmfs/atlas-nightlies.cern.ch/repo/sw/master/sw/lcg/releases/LCG_93/Python/${PYTHONVERSION}/$PYTHONBUILD/bin:${PATH}"
    export LD_LIBRARY_PATH="/cvmfs/atlas-nightlies.cern.ch/repo/sw/master/sw/lcg/releases/LCG_93/Python/${PYTHONVERSION}/$PYTHONBUILD/lib:${LD_LIBRARY_PATH}"
fi
if [ ! $ROOTSYS ]; then
  echo "Setting up ROOT ${ROOTVERSION} ..."
  echo "With build ${BUILD} ..."
  export CWD=$PWD
  lsetup 'root 6.18.04-x86_64-centos7-gcc8-opt'
  cd $CWD
fi

scriptname=${BASH_SOURCE:-$0}

VERSION="trunk"
if [ ! $ROOTSYS ]; then
  echo "Warning: No valid Root environment (ROOTSYS) defined. Please do so first!"
  return
fi

if [[ "$(root-config --version | cut -d "." -f 1)" == "5" ]]; then
  echo "NOTE: ROOT5 installation detected - be aware that this version of HistFitter is developed against ROOT6."
  echo "We cannot guarantee you will not run into issues."
fi

if [ ! $LD_LIBRARY_PATH ]; then
  echo "Warning: so far you haven't setup your ROOT enviroment properly (no LD_LIBRARY_PATH)"
  return
fi
if [ -z ${ZSH_NAME} ] && [ "$(dirname ${BASH_ARGV[0]})" == "." ]; then
  if [ ! -f setup.sh ]; then
    echo ERROR: must "cd where/HistFitter/is" before calling "source setup.sh" for this version of bash!
    HF=; export HF
    return 1
  fi
  HF=$(pwd); export HF
else
scriptname=${BASH_SOURCE:-$0}
  DIR=$( cd "$( dirname "${scriptname}" )" && pwd )
HF=${DIR}; export HF
fi
HISTFITTER=$HF; export HISTFITTER
SUSYFITTER=$HF; export SUSYFITTER
HISTFITTER_VERSION=$VERSION
export HISTFITTER_VERSION
echo "Setting \$HISTFITTER to ${HISTFITTER}"
export PATH=$HISTFITTER/bin:$HISTFITTER/scripts:${PATH}
export LD_LIBRARY_PATH=$HISTFITTER/lib:${LD_LIBRARY_PATH}
export PYTHONPATH=$HISTFITTER/python:$HISTFITTER/scripts:$HISTFITTER/macros:$HISTFITTER/lib:$PYTHONPATH
export ROOT_INCLUDE_PATH=$HISTFITTER/include:${ROOT_INCLUDE_PATH}
export SVNTEST="svn+ssh://svn.cern.ch/reps/atlastest"
export SVNROOT="svn+ssh://svn.cern.ch/reps/atlasoff"
export SVNPHYS="svn+ssh://svn.cern.ch/reps/atlasphys"
export ROOT_INCLUDE_PATH=$HISTFITTER/src:${ROOT_INCLUDE_PATH}

export LC_ALL=C

cd $XCWD

echo "current directory:"
pwd
'''

        copyInputs='''

cd {2}
source ./setup.sh

cd $HFRUNDIR

mkdir -p  InputTrees

echo "copying files in HFRUNDIR"

ln -s {0}/*.{1}.root InputTrees/

ls -ll InputTrees/

echo ">> ===================="
echo ">> Now running command"
echo ">> ===================="

'''.format(pathUtilities.eosDataDirectory(),lumiTag,histFitterDir)
        
    copyOutputs='cp -r results data {0}/ \n\n'.format(pathUtilities.histFitterResults())

    script=setupcommand
    script+=copyInputs

    import subprocess, os
    
    commandsList = generateHistFitterCommands(gridName, extraOptionsDict,extraOptions,subListConcat,theoryUncert,doupper,True,signalGroupIndex)


    if len(commandsList):

        ulTag=fittypetag

        basename=gridName+'_'+theoryUncert+extraOptions+'_'+ulTag

        if ulTag=='excl':
            if doupper: ulTag='UL' 
            basename =gridName+'_'+theoryUncert+extraOptions+'_'+ulTag+'_Job%02d'%signalGroupIndex


        removeOldOutput='''
rm -rf {0}/{1}

'''.format(pathUtilities.histFitterResults()+'/results/',basename+"*")

        script+=removeOldOutput

        for command in commandsList:
            if command.endswith(";"):
                command=command[:-1]
            script += command+"\n"
            script += "\n"

        script +=copyOutputs

        if not os.path.exists('scripts'):
            os.makedirs('scripts')
        if not os.path.exists('scripts/logs'):
            os.makedirs('scripts/logs')


        path=os.path.abspath("scripts")


        scriptFile=open('scripts/'+basename+'.sh','w')
        scriptFile.write(script)
        scriptFile.close()

        os.chmod('scripts/'+basename+'.sh',0o777)

        bsubcommand=''

        if pathUtilities.isFreiburg():
            bsubcommand='sbatch -p short --time=300 --mem=4000 -o '+path+'/logs/'+basename+'.out -e '+path+'/logs/'+basename+'.err '+path+'/'+basename+'.sh'
            
        # LXPLUS
        elif 'bsub' in batch_opt['syst']:

            bsubcommand='bsub -q '+batch_opt['queue']+' -o '+path+'/logs/'+basename+'.out  -e  '+path+'/logs/'+basename+'.err  '+path+'/'+basename+'.sh'
        elif 'condor' in batch_opt['syst']:

            submitFile='''executable = {1}/{0}.sh
arguments  = $(ClusterID) $(ProcId)
output     = {1}/output/{0}.$(ClusterID).$(ProcId).out
error      = {1}/error/{0}.$(ClusterID).$(ProcId).err
log        = {1}/log/{0}.$(ClusterID).$(ProcId).log
request_disk ={3}

+JobFlavour = "{2}"
queue'''.format(basename,path,batch_opt['queue'],batch_opt['storage'])

            scriptHTCondor=open('scripts/'+basename+'_toSubmit.sh','w')
            scriptHTCondor.write(submitFile)
            scriptHTCondor.close()
            os.chmod('scripts/'+basename+'_toSubmit.sh',0o777)

            if not os.path.exists('scripts/output'):
                os.makedirs('scripts/output')
            if not os.path.exists('scripts/log'):
                os.makedirs('scripts/log')
            if not os.path.exists('scripts/error'):
                os.makedirs('scripts/error')

            submitJob=True

            if options.resubmit is not None:
                failedJobs=[line.strip() for line in open(options.resubmit)]
                if basename not in failedJobs:
                    submitJob=False
            else:
                job=basename+" "+subListConcat
                global jobsSubmitted

                jobsSubmitted+=job+"\n"

            if submitJob:
                bsubcommand='condor_submit '+path+'/'+basename+'_toSubmit.sh'

	    print bsubcommand

            if not dryRun:
                subprocess.call(bsubcommand, shell=True)

        
        elif 'HTCondor' in batch_opt['syst']:
            if theoryUncert!=Nominal:
                sys.exit(1)
            Fitmodel = options.fitmodel
            if blindtag != "":
                ul_tag = "Blind"
                ul = "--doBlind"
            elif doupper:
                ul_tag = "UL"
                ul = "--doUL"
            else:
                ul_tag = ""
                ul = ""
            sysname=systematicList.replace(',','_')
            func = "fit"

            cmd0 = 'cd ' + pathUtilities.histFitterTopDirectory() + '/run/'
            cmd1 = 'export path=`pwd`'
            cmd2 = 'echo $path'
            cmd3 = 'cp Job_HF_2021.sh ./JOB/Job_HF_2021_{0}_'.format(options.SR) + str(signalGroupIndex) + '.sh'
            cmd4 = 'sed -i "s/EXTRAOPTION/' + '--parallize --signalGroupIndex ' + str(signalGroupIndex) + ' --signalList ' + str(subListConcat) + '/g" ./JOB/Job_HF_2021_{0}_'.format(options.SR) + str(signalGroupIndex) +  '.sh'
            cmd5 = 'hep_sub ./JOB/Job_HF_2021_{0}_'.format(options.SR) + str(signalGroupIndex)  +  '.sh -o ./LOG/Log_{0}_'.format(options.SR)  + str(signalGroupIndex) + '.txt' + ' -e ./LOG/Err_{0}_'.format(options.SR) + str(signalGroupIndex) +  '.txt'
            print cmd1
            print cmd2
            print cmd3
            print cmd4
            print cmd5
            subprocess.call(cmd0+"\n"+cmd1+"\n"+cmd2+"\n"+cmd3+"\n"+cmd4+"\n"+cmd5,shell=True)

        else:
            print("System is incompatible with the ones required. Use --batch --extra syst:bsub or syst:condor")
            sys.exit(1)

def runPlottingSequentially(grid, extraOptionsDict, makeList=True, makeHist=True, makePlot=True, dryRun=False):
    import subprocess, os, ROOT
    os.chdir(pathUtilities.macrosDirectory())
    from ROOT import gSystem, gROOT
    ROOT.gROOT.SetMacroPath( ROOT.gROOT.GetMacroPath()+":"+pathUtilities.macrosDirectory())
    ROOT.gInterpreter.AddIncludePath(pathUtilities.macrosDirectory())
    os.chdir(pathUtilities.histFitterUser())

    makeListCommands,  makeFillJsonCommands, makeTreeCommands, makeJsonBestCommands, makePlotCommands = generatePlottingCommands(grid, extraOptionsDict)


    print "########################  Generating JSON files from hypotest.root #######################"
    if makeList:
        gROOT.Reset("a")
        gSystem.Load('libSusyFitter.so')
        for command in makeListCommands:
            print command
            if not dryRun: 
                subprocess.call(command, shell=True)
        gROOT.Reset("a")
 
    
    if makeHist:

        print "############################ Now make json to be ROOT ##########################"

        print "1) Filling JSON files with missing info (no UL): m0, m12, xsec... needed for next steps"
        for command in [c for c in makeFillJsonCommands]:
          
            print command
            if not dryRun: 
                FillJsonFilesWithMissingInfo.FillJsonFilesWithMissingInfo(command.split(" ")[0],command.split(" ")[1],options.SigNameSchema)
        
        print "2) Producing BEST JSON SRs"
        for command in [c for c in makeJsonBestCommands ]:
            print command
            if not dryRun:
                subprocess.call(command, shell=True)
           
        print "3) Producing contour plots"
        for command in [c for c in makeTreeCommands ]:
            print command
            if not dryRun: 
                subprocess.call(command, shell=True)            

    
    if makePlot:
        print "############################ Now make contour ##########################"
        gROOT.Reset("a")
        gSystem.Load('libSusyFitter.so')
        for command in makePlotCommands:
            print command
            if not dryRun: 
                ##ROOT.gInterpreter.ProcessLine(command)
                subprocess.call(command, shell=True)
        gROOT.Reset("a")
    
   
    
# adds escaped quotes to a string, or converts an object to str
def quotes(obj):
    if isinstance(obj, basestring):
        return "\""+obj+"\""
    return str(obj)

# simple structure to manage arguments of plotting macro, which are a lot
class plotInputCommand:
    def __init__(self):
        self.nominalFileName = None
        self.theoryUpFileName = None 
        self.theoryDownFileName = None
        self.upperLimitFile = None
        self.lumi = float(lumiTag)
        self.SR = None
        self.model= None
        self.drawCLs = False
        self.drawCLsExp = False
        self.drawXS = False
        self.Sys = None
        self.outputNamePlot = None
        self.draw1D = False
        self.bestJSONfile = None
        self.SRs = None
        self.makeBest = False

    def toArgs(self):
        # returns a list of arguments to be passed to a C function, with quotes properly escaped
        result=""
        result+="--nominalFileName " + pathUtilities.histFitterUser() + "/" + quotes(self.nominalFileName) + " "
        result+="--lumi " + quotes(self.lumi) + " "
        result+="--model "+self.model+" "
        result+="--outputNamePlot "+self.outputNamePlot+" " 
        if self.drawCLs: result+=" --drawCLs "
        if self.drawCLsExp: result+=" --drawCLsExp "
        if self.drawXS:  result+=" --drawXS " 
        if self.draw1D:  result+=" --draw1D "
        if self.makeBest: result+=" --makeBest "

        return result

    def toArgsBest(self):
        # returns a list of arguments to be passed to a C function, with quotes properly escaped
        result=""
        result+="--nominalFileName " + pathUtilities.histFitterUser() + "/" + quotes(self.nominalFileName) + " "
        result+="--bestJSONfile "+ pathUtilities.histFitterUser() + "/" + quotes(self.bestJSONfile) + " "
        result+="--lumi " + quotes(self.lumi) + " "
        result+="--model "+self.model+" "
        result+="--outputNamePlot "+self.outputNamePlot+" "
        result+="--SRs "+self.SRs+" "

        return result


def generatePlottingCommands(grid, extraOptionsDict):
    makeListCommands = []
    makeFillJsonCommands = []
    makeJsonBestCommands = [] #commands for comparing 2 SRs and taking the best value of CLs
    makeTreeCommands = []
    makePlotCommands = []

    from plottingConfig import modelDict

    model=modelDict[grid]

    forbiddenFunction=model.forbiddenFunction
    xMin, xMax, yMin, yMax = model.getRangeForContours()
    rangeHarvest = " --xMin "+xMin+" --xMax "+xMax+" --yMin "+yMin+" --yMax "+yMax if (xMin is not None or yMin is not None) else ""


    if options.WithSigMass:
        optionsJSON=" -f \"hypo_signal%f"
        for itr in range(len(list(options.SigNameSchema.split(",")))):
            if itr==len(list(options.SigNameSchema.split(",")))-1:
                optionsJSON = optionsJSON + "_%f\""
            else:
                optionsJSON = optionsJSON + "_%f"

        if len(list(options.SigNameSchema.split(",")))==1: optionsJSON = optionsJSON + " -p \"chan:m0\" -c \"1\""
        elif len(list(options.SigNameSchema.split(",")))==2: optionsJSON = optionsJSON + " -p \"chan:m0:m12\" -c \"1\""
        else:
            print("!!!!!!!!Error: current did not support hypo name with 3 part of information !!!!!")
            sys.exit()
    else:
        optionsJSON=" -f \"hypo_signal%f\"  -p \"chan\" -c \"1\""
    optionsToHarvest=""
    if options.draw1D==False: optionsToHarvest = " -x m0 -y m12 -l "+forbiddenFunction + rangeHarvest

    if options.extraHarvestToContours is not None: optionsToHarvest += str(options.extraHarvestToContours)

    hypotestHarvest="hypotest__1_harvest"
    outputNamePlot=None
    bestJSONfile=None

    # once set of plotting arguments per grid
    theArgs=plotInputCommand()
    for extraOption in extraOptionsDict:
        for theoryUncert in [Nominal]:

            baseNameExcl = grid+'_'+theoryUncert+extraOption+"_excl_output"
            baseNameUL =   grid+'_'+"UpperLimit"+extraOption+"_excl_output"

            # exclude up/down for "Slot" variations, since plots would be too crowded.
            # this means that for individual SRs, we will have only the nominal prediction
            if not  ((theoryUncert == Up or theoryUncert == Down) and 'Slot' in extraOption): 

                if makeBest==False:
                    #Generating JSON files. As code needs to be run independently for every SR before getting the best SR 
                    #there is no need of redo the JSON files and filling the missing info  when making the best SR.
                    #theory variations and ULs will be looked for internally by the script                       
                    makeListCommands.append("GenerateJSONOutput.py -i "+histFitterDir+"/results/{0}_hypotest.root {1} -a \"\" ".format(baseNameExcl,optionsJSON))

                    # fill missing info in the nominal case. If theory variations exists, then they will be filled as well. Same for UL
                    makeFillJsonCommands.append('{0}_{1}_list.json {0}_{1}_fix_list.json'.format(baseNameExcl,hypotestHarvest))

                    if options.draw1D==True:
                        # create the TGraphs for the 1D case
                        makeTreeCommands.append('python {2}/jsonToBands.py -i {0}_{1}_fix_list.json -o {3}_{1}_fix_list.root'.format(baseNameUL,hypotestHarvest,pathUtilities.pythonDirectory(),baseNameUL.replace("UpperLimit",Nominal)))
                    else:
                        # create contours with the output file above, theory lines included if input exists. Same for UL. 
                        makeTreeCommands.append("harvestToContours.py -i {0}_{1}_fix_list.json -o {0}_{1}_fix_list.root {2}".format(baseNameExcl,hypotestHarvest,optionsToHarvest))

                    if not "Slot" in extraOption:
                        inputFilePlotting='{0}_{1}_fix_list.root'.format(baseNameExcl,hypotestHarvest)
                        outputNamePlot = baseNameExcl


                else: #makeBest=True
                    if options.SR in combinedRegions and options.draw1D==False:
 
                        if options.makeBestGrid:
                                print red("Grid combination as for example the one for Gtt and GttCompr in the past paper not done yet!!")
                                print red("You will do it once the time comes... Sorry!")
                                sys.exit(1) 
                        else:
                                
                                #Combining only SRs for the same Model.
                                #input files must already exist since they are created when makeBest=False for every SR. No need to recreat them again. 
                                #Create first the best JSON file. This file is needed to create the plots of which SR is chosen per grid point.
                                #The script internally will look for UL and get the best JSON files for UL as well.
                                localCommand = 'multiplexJSON.py -t -d -m m0,m12 -i {0}_{1}_fix_list.json '.format(baseNameExcl,hypotestHarvest)

                                for reg in combinedRegions[options.SR]:
                                    localCommand +='{0}_{1}_fix_list.json '.format(baseNameExcl.replace(options.SR,reg),hypotestHarvest)
                                               
                                localCommand += ' -o {0}_{1}_fix_list_best.json'.format(baseNameExcl,hypotestHarvest)

                                makeJsonBestCommands.append(localCommand)

                                bestJSONfile = '{0}_{1}_fix_list_best.json'.format(baseNameExcl,hypotestHarvest)

                                ''' 
                                This is an alternative way to get the best contour graphs: create first the best JSON file and then the contour as in the usual way. 
                                However, official recomendation is to get the best contour using as input directly the graph for evey region as done with multiplexContours.py
                                '''
                                # create contours with best JSON file. Contours are not used for drawing the final plots, but this step is done mainly
                                # to get the best CLs values and ULs per signal points and draw the grey numbers in the final contour plot. 
                                makeJsonBestCommands.append("harvestToContours.py -i {0}_{1}_fix_list_best.json -o {0}_{1}_fix_list_best_CLs.root {2}".format(baseNameExcl,hypotestHarvest,optionsToHarvest))
                                

                                #Combining only SRs for the same Model.
                                #input files must already exist since they are created when makeBest=False for every SR. No need to recreat again. 
                                #Official recomendation from HistFitter team is combine graphs as done with multiplexContours.py
                                localCommand='multiplexContours.py --plotUsedContours --ignoreInteriorLines  -i {0}_{1}_fix_list.root '.format(baseNameExcl,hypotestHarvest)  

                                for reg in combinedRegions[options.SR]:
                                    localCommand += '{0}_{1}_fix_list.root '.format(baseNameExcl.replace(options.SR,reg),hypotestHarvest)

                                localCommand +=' -o {0}_{1}_fix_list_best_contours.root'.format(baseNameExcl,hypotestHarvest)

                                makeJsonBestCommands.append(localCommand)

                                #now, we need to merge the files with the contours with the one with the best CLs and ULs. 
				makeJsonBestCommands.append("hadd -f  {0}_{1}_fix_list_best.root {0}_{1}_fix_list_best_contours.root {0}_{1}_fix_list_best_CLs.root".format(baseNameExcl,hypotestHarvest))

                    else:
                        print "-> Can't get best SRs as dictionary with combinedRegions does not contain the key. If no combination is needed please use makeBest=False... ABORTING"
                        sys.exit(1)


                    if not "Slot" in extraOption:
                        inputFilePlotting='{0}_{1}_fix_list_best.root'.format(baseNameExcl,hypotestHarvest)
                        outputNamePlot = baseNameExcl+"_Best"


        	if not "Slot" in extraOption:
	    	    if theoryUncert == Nominal:
                	theArgs.nominalFileName=inputFilePlotting
                        theArgs.outputNamePlot = outputNamePlot
                        theArgs.bestJSONfile = bestJSONfile




    theArgs.drawCLs=options.drawCLs if options.draw1D==False else False
    theArgs.drawCLsExp=options.drawCLsExp if options.draw1D==False else False
    theArgs.drawXS=options.doUL if options.draw1D==False else False
    theArgs.model = options.Model
    theArgs.draw1D = options.draw1D
    theArgs.SRs = options.makeBest
    theArgs.makeBest = makeBest

    makePlotCommands.append("python {0}/{2} {1}".format(pathUtilities.macrosDirectory(), theArgs.toArgs(), plottingMacro))
    if makeBest==True:
        makePlotCommands.append("python {0}/{1} {2}".format(pathUtilities.macrosDirectory(), plottingMacroBest, theArgs.toArgsBest()))

    return makeListCommands, makeFillJsonCommands, makeTreeCommands, makeJsonBestCommands, makePlotCommands

# Smaller Utils
def makeGridPointDict(grid):

    gridDict = {}
    gridDict[grid] = {}

    for theoryUncert in theoryUnc:
        gridDict[grid][theoryUncert] = ''
        gridFile = open(pathUtilities.histFitterTopDirectory()+'/susyGridFiles/'+grid)
        for point in gridFile:
            if point.startswith('mc') and not (point.strip() in excludedPoints):
                # gets dataset number
                mass = signalSameSignTools.getUglyCaseBashingMasses(grid, point.split('.')[1], point.split('.')[2].split('_'), options.SigNameSchema)
                if options.WithSigMass:
                    gridDict[grid][theoryUncert] += 'signal{0}_{1}_{2};'.format(point.split('.')[1], mass[0],mass[1])
                else:
                    gridDict[grid][theoryUncert] += 'signal{0};'.format(point.split('.')[1])
        gridDict[grid][theoryUncert] = gridDict[grid][theoryUncert].strip(';')

    gridFile.close()
 
    print "List of signals to process: ",gridDict
   
    return gridDict

def yieldSubList(points, length):
    # the length determines the number of points in each subjob.
    pointsList = points.split(';')
    for subList in [pointsList[x:x+length] for x in range(0,len(pointsList), length)]:
        subListConcat = ''
        for point in subList:
            subListConcat += point+';'

        yield subListConcat.strip(';')



def red(msg): return "\033[0;31m{0}\033[0m".format(msg);

if __name__ == '__main__':
    main()
