#!/usr/bin/env python2.6
import ROOT, os, re
import math
import sys
from math import sqrt, pow
from ROOT import gStyle
from ROOT import gROOT
from ROOT import TStyle
from ROOT import TFile
from ROOT import TGraph2D
from array import array
from optparse import OptionParser
# ROOT.gSystem.Load("libSusyFitter.so")

import pathUtilities
import signalSameSignTools
import FillJsonFilesWithMissingInfo
signalRunnumberToMassesDict = signalSameSignTools.getRunnumbersMassesDictSSAllGrids()
ROOT.gROOT.SetBatch()

debug = 0

def main():
    parser = OptionParser()
    parser.add_option('',"--FileName", dest='FileName', help="File with yields tables", default="")
    parser.add_option('',"--DirName", dest='DirName', help="Directory", default="/storage/users/pt1009/SS_HistFitter/run2/macroSS/1DPlot/")
    parser.add_option('',"--OutputName", dest='OutputName', help="OutputName", default="UpperCrossSections_Test")
    parser.add_option('',"--takeBest", dest='takeBest', help="Take best exclusion (True/False)", default="False")
    (options, args) = parser.parse_args()

    dirname = options.DirName 
    takeBest = options.takeBest
    filename = options.FileName
    outputname = filename.replace(".root", "__1_harvest_fix_list")
    print options.DirName+"../../HistFitterUser/"+outputname+"_Obs_UpperLimit.root"
    Out_File = TFile(options.DirName+"../../HistFitterUser/"+outputname+"_Obs_UpperLimit.root", "RECREATE");
    fout_Exp = open(options.DirName+"../../HistFitterUser/"+outputname+"_Exp_UpperLimit.txt", "w+")
    fout_Obs = open(options.DirName+"../../HistFitterUser/"+outputname+"_Obs_UpperLimit.txt", "w+")
    
    if not len(options.FileName):
        print red("Please specify an input filename"); sys.exit(1)

    if not os.path.exists(dirname+options.FileName):
        print red("Input file doesn't exist: "); 
        print dirname+options.FileName;
        sys.exit(1)


    preobs=[]
    exp=[]
    obs=array('d')
    expd=[]
    expu=[]
    exp2d=[]
    exp2u=[]
    cross=[]
    crossplus=[]
    crossminus=[]
    xMass = array('d')
    yMass = array('d')
    prexMass =[]
    signal_list=[]

    print 'using',filename
    _file = ROOT.TFile.Open(dirname+filename)

    for key in _file.GetListOfKeys():
        kname = key.GetName()
        if "ProcessID" in kname:
            continue
        if debug : print kname
        signal_list.append(kname)

    signal_list.sort()

    for s in signal_list:
        my_result=_file.Get(s)
        signalID=my_result.GetName()                
        print "signalID", signalID

        if "debug" in signalID : continue # when HF fails the fit
        
        grid = filename.split("_")[0]
        if "Rpv" in filename:
            grid = grid+"_"+filename.split("_")[1]
        print "signalID ",signalID," in grid ",grid
        DSmass = GetDSMass(signalID,grid)
        LSPmass = GetLSPMass(signalID,grid)

        runnumber = signalID.strip('hypo_signal').strip('debug_signal')
        if "Mc16" in filename:
            MC_Version = "16"
        else:
            MC_Version = "15"
        dbentry = FillJsonFilesWithMissingInfo.lookForSample(runnumber,MC_Version)
        xsec= float(dbentry[2])
        kfac= float(dbentry[4])
        feff= float(dbentry[3])
        
        # check here if signal name is correct and one gets limits
        if debug : 
            print "The computed upper limit for signal named ", mass, "with correspinding gluino mass", mass, " is: ", my_result.UpperLimit()
            print "expected Upper limit ", my_result.GetExpectedUpperLimit(0.)
            print "expected Upper limit -1 sigma ", my_result.GetExpectedUpperLimit(-1.)
            print "expected Upper limit +1 sigma ", my_result.GetExpectedUpperLimit(1.)
            print "expected Upper limit -2 sigma ", my_result.GetExpectedUpperLimit(-2.)
            print "expected Upper limit +2 sigma ", my_result.GetExpectedUpperLimit(2.)       
        import string

#        exp.append(my_result.GetExpectedUpperLimit(0)*xsec*kfac*feff*1000.0)
#        obs.append(my_result.UpperLimit()*xsec*kfac*feff*1000.0)
#
#        exp_num = my_result.GetExpectedUpperLimit(0)*xsec*kfac*feff*1000.0
#        obs_num = my_result.UpperLimit()*xsec*kfac*feff*1000.0

        exp.append(my_result.GetExpectedUpperLimit(0)*xsec*kfac*1000.0)
        obs.append(my_result.UpperLimit()*xsec*kfac*1000.0)

        exp_num = my_result.GetExpectedUpperLimit(0)*xsec*kfac*1000.0
        obs_num = my_result.UpperLimit()*xsec*kfac*1000.0
        print>>fout_Obs, ("%15s,%15s,%15s" %(LSPmass, DSmass, obs_num))
        print>>fout_Exp, ("%15s,%15s,%15s" %(LSPmass, DSmass, exp_num))

        xMass.append(float(DSmass))
        yMass.append(float(LSPmass))

    UpperLimits_gr = TGraph2D("upperLimits_gr", "upperLimits_gr", len(xMass), xMass, yMass, obs)
    Out_File.cd()
    UpperLimits_gr.Write()
    Out_File.Close()

def GetLSPMass(signalID,grid=""):    
    ID = signalID.strip('hypo_signal').strip('debug_signal')
    if ID in signalRunnumberToMassesDict[grid]:
        masses = signalRunnumberToMassesDict[grid][ID]
        return str(masses[1])

def GetDSMass(signalID,grid=""):    
    ID = signalID.strip('hypo_signal').strip('debug_signal')
    if ID in signalRunnumberToMassesDict[grid]:
        masses = signalRunnumberToMassesDict[grid][ID]
        return str(masses[0])

if __name__ == "__main__":
    main()
