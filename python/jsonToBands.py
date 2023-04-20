#!/usr/bin/env python
### jsonToBands.py #####################
#
# This script is designed to read the mass points 'm0' and all 'excludedXsec*' from the json file
# and create expected, observed, and 1 and 2-sigma bands in TGraphs. 
# Also, it will save the plots for theory x-section, including one with uncertainty included.  
#
# This script is *not* used to create 2D exclusion contours, but only when the goal is to plot the upper-limit on x-sections 
# as a function of the generated mass point 'm0'
#
# The results TGraphs are written in the output file, with name given in the option  -o 
#######################################

import os
import sys
import json
import ROOT
from ROOT import TFile, TGraphAsymmErrors, TGraph
import pandas as pd
import numpy as np
import pathUtilities

import argparse

ROOT.gROOT.SetBatch()

parser = argparse.ArgumentParser()

parser.add_argument("--inputFile","-i",  type = str, help="input json file", default = "test.json")
parser.add_argument("--outputFile","-o", type = str, help="output ROOT file", default = "test.root")

args = parser.parse_args()

def main():

    os.chdir(pathUtilities.histFitterUser())

    filename = args.inputFile
    fileout = args.outputFile

    if not os.path.exists(filename):
	print "File {0} does not exist".format(filename); sys.exit(1)

    print "Reading {0} \n".format(filename)

    # read json in dataframe
    df = pd.read_json(filename)

    # keep only parameters we are interested
    cols = [c for c in list(df.columns) if ('excludedXsec' in c or 'xsec' in c)]
    cols.append('m0')

    df = df[cols]

    # sorting by m0: needed for plotting
    df = df.sort_values(by=['m0'])


    print df

    toPb=0.001

    # getting input for TGraphs: arrays, and convert to pb if needed
    m0 =  convert(df['m0'])
    obs = convert(df["excludedXsec"],toPb)           
    exp = convert(df["excludedXsecExp"],toPb)
    exp1s = convert(df["excludedXsecPlus1Sig"],toPb) 
    exp1m = convert(df["excludedXsecMinus1Sig"],toPb)
    exp2s = convert(df["excludedXsecPlus2Sig"],toPb) 
    exp2m = convert(df["excludedXsecMinus2Sig"],toPb)

    xsec = convert(df['xsec'],toPb)
    xsecUp = convert(df['xsecUp'],toPb)
    xsecDown = convert(df['xsecDown'],toPb)

    # Creating TGraphs and saving in output file
    fout = TFile(fileout, "recreate")

    # the  "_0" is added to the plot names to keep consistence with the ones produced by harvestToContours.py
    # so that they can be read by the same plotting macro
    pObs = createTGraph("Obs_0",m0,obs)
    pExp = createTGraph("Exp_0",m0,exp)
    exp1s = createTGraphAsym("Band_1s_0",m0,exp,exp1s-exp,exp-exp1m)
    exp2s = createTGraphAsym("Band_2s_0",m0,exp,exp2s-exp,exp-exp2m)

    pxsec = createTGraph("theory",m0,xsec)
    pxsecUp = createTGraph("theory_up",m0,xsecUp)
    pxsecDown = createTGraph("theory_down",m0,xsecDown)

    pObs.Write()
    pExp.Write()
    exp1s.Write()
    exp2s.Write()
    pxsec.Write()
    pxsecUp.Write()
    pxsecDown.Write()

    fout.Close()

    return

def createTGraph(name,x,y):

    pG = TGraph(len(x),x,y)
    pG.SetName(name)

    return  pG

def createTGraphAsym(name,x,y,y2,y1):

    xe = np.array(len(x) * [0],dtype='double')

    pG=TGraphAsymmErrors(len(x),x,y,xe,xe,y1,y2)

    pG.SetName(name)

    return pG

def convert(df,toPb=1):

    return np.array(df,dtype='double')*toPb



if __name__ == "__main__":
    main()
