#!/usr/bin/env python2.6
import ROOT, os, re
import math
import sys
from math import sqrt, pow
from ROOT import gStyle
from ROOT import gROOT
from ROOT import TStyle
from array import array
from optparse import OptionParser

import pathUtilities
import signalSameSignTools
signalRunnumberToMassesDict = signalSameSignTools.getRunnumbersMassesDictSSAllGrids()

debug = 1

def main():
    parser = OptionParser()
    parser.add_option('',"--file1", dest='file1', help="File1", default="test1.root")
    parser.add_option('',"--file2", dest='file2', help="File1", default="test2.root")
    parser.add_option('',"--output", dest='output', help="OutputName", default="output.root")
    (options, args) = parser.parse_args()

    file1 = options.file1 
    file2 = options.file2
    output = options.output 

    if not os.path.exists(file1):
        print "Input files 1 doesn't exist: "; 
        print file1;
        sys.exit(1)

    if not os.path.exists(file2):
        print "Input files 2 doesn't exist: "; 
        print file2;
        sys.exit(1)
        
    ####################
    ## File 1 Extraction
    ####################

    print 'using ',file1
    signal1_list=[]
    _file1 = ROOT.TFile.Open(file1)

    for key in _file1.GetListOfKeys():
        kname = key.GetName()
        if "ProcessID" in kname or "fitTo_signal" in kname:
            continue
        if debug : print kname
        signal1_list.append(kname)

    signal1_list.sort()

    ####################
    ## File 2 Extraction
    ####################

    print 'using ',file2
    signal2_list=[]
    _file2 = ROOT.TFile.Open(file2)

    for key in _file2.GetListOfKeys():
        kname = key.GetName()
        if "ProcessID" in kname or "fitTo_signal" in kname:
            continue
        if debug : print kname
        signal2_list.append(kname)

    signal2_list.sort()

    ####################
    ## Same points ?
    ####################

    if signal1_list != signal2_list :
        print "Signal points not the same ! Exit."; 
        sys.exit(1)

    ####################
    ## Get best SR
    ####################

    if "Rpc2L1b" in file1:
        SR1 = "Rpc2L1b"
        SR2 = "Rpc2L2b"
    elif "Rpc2L2b" in file1:
        SR1 = "Rpc2L1b"
        SR2 = "Rpc2L2b"

    out_txt = output.replace("root","txt")
    bestSR = open(out_txt,"write")

#    fFinal = ROOT.TFile(output,"recreate")
    
    for s in signal1_list:
        my_result1=_file1.Get(s)
        my_result2=_file2.Get(s)
        signalID = my_result1.GetName()
        mass = GetMass(signalID,"Mc16SusyBtt")

        if my_result1.CLs(0) <= my_result2.CLs(0) :
#            my_result1.Write()
            bestSR.write(SR1+"\t"+mass+"\t"+str(my_result1.CLs(0))+"\n")
        if my_result1.CLs(0) > my_result2.CLs(0) :
#            my_result2.Write()
            bestSR.write(SR2+"\t"+mass+"\t"+str(my_result2.CLs(0))+"\n")

#    fFinal.Close()
    bestSR.close()

def GetMass(signalID,grid=""):
    ID = signalID.strip('hypo_signal').strip('debug_signal')
    if ID in signalRunnumberToMassesDict[grid]:
        masses = signalRunnumberToMassesDict[grid][ID]
        return str(masses[0])+"\t"+str(masses[1])

if __name__ == "__main__":
    main()
