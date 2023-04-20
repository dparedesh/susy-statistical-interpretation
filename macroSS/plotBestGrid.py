#!/usr/bin/env python

##########################################
#
# Tools for making final SS contour plots
#
##########################################

import ROOT, argparse, sys, os, math
from array import array
import contourPlotter
import pathUtilities
import pandas as pd
import numpy as np


ROOT.gROOT.SetBatch()

parser = argparse.ArgumentParser()
parser.add_argument("--nominalFileName", type = str, help="input nominal file name with observed and expected contours", default="test.root")
parser.add_argument("--bestJSONfile", type = str, help="input json file with the best signal regions", default="test.json")
parser.add_argument("--model",type=str,help="input model")
parser.add_argument("--lumi", type = float, help="", default=139)
parser.add_argument("--outputNamePlot",type=str,help="Get name of the output plot",default=None)
parser.add_argument("--SRs",type=str,help="Comma separated list of signal regions used to get the best contours and best json files")

args = parser.parse_args()

#can plot up to 10 signal regions. For more, just add the required color here.
color=[ROOT.kRed,ROOT.kBlue,ROOT.kGreen+1,ROOT.kMagenta,ROOT.kOrange+1,ROOT.kAzure+10,ROOT.kViolet+6,ROOT.kYellow,ROOT.kGreen-1,ROOT.kRed-5]
labelATLAS=""#bf{{Internal}}

def main():
	"""Main function for driving the whole thing..."""
	print(">>>Welcome to Final Coutour Plotter!!!")

	# Print out the settings
	for setting in dir(args):
		if not setting[0]=="_":
			print( ">>> ... Setting: {: >20} {: >40}".format(setting, eval("args.%s"%setting) ) )


        ## Getting plot configuration for the model
        from plottingConfig import modelDict

        model=modelDict[args.model]

        xMin = model.xMin
        yMin = model.yMin
        xMax = model.xMax
        yMax = model.yMax
        xLabel = model.xLabel
        yLabel = model.yLabel
        processDescription = model.processDescription
        forbiddenLabelX = model.forbiddenLabelX
        forbiddenLabelY = model.forbiddenLabelY
        forbiddenLabelText = model.forbiddenLabelText
        previousLimits = model.previousLimits

        xMinLine = model.xMinLine
        yMinLine = model.yMinLine
        xMaxLine = model.xMaxLine
        yMaxLine = model.yMaxLine

        yMaxLabel = model.yMaxLabel
        yMinLabel = model.yMinLabel
        xMaxLabel = model.xMaxLabel
        xMinLabel = model.xMinLabel

        modelName = model.modelName
        outputNamePlot = args.outputNamePlot

	plotTag="_Grid"

	plot = contourPlotter.contourPlotter(outputNamePlot+plotTag,800,600)
        plot.setXAxisLabel(xLabel)
        plot.setYAxisLabel(yLabel)
	plot.processLabel = processDescription
	args.lumi=args.lumi/1000.0
	lumitag = str(args.lumi)
	plot.lumiLabel = "#splitline{{#it{{ATLAS}} {1} }}{{#bf{{#splitline{{#sqrt{{s}}=13 TeV, {0:d} fb^{{-1}}}}{{All limits at 95% CL}}}}}}".format(int(round(args.lumi)),labelATLAS)


        ## getting SRs
        SRs=args.SRs.split(",")

        print SRs

        ## getting the grid points per signal region
        bestJSON=pd.read_json(args.bestJSONfile)

        # keep only parameters we are interested
        bestJSON = bestJSON[['m0','m12','fID']]

        # drawing axis based on xMax 
        xMax=bestJSON['m0'].max()
        plot.drawAxes( [xMin,yMin,xMax,yMax] )
        ROOT.gPad.SetTicks()

        pGs={}

        # separating dfs per signal region and creating graphs per signal region
        for i in range(len(SRs)):

            # cleaning name of region...
            bestJSON['fID']=bestJSON['fID'].apply(lambda x: SRs[i] if '_'+SRs[i]+'_' in x else x)

            df = bestJSON[bestJSON['fID']==SRs[i]]

            print df

            pG=createTGraph(SRs[i],np.array(df['m0'],dtype='float'),np.array(df['m12'],dtype='float'))
            pGs[SRs[i]]=pG

            plot.drawPoints(pG,color[i],legendOrder=i)

        ## for some reason it does not plot the first signal region. So, plotting again
        plot.drawPoints(pGs[SRs[0]],color[0],legendOrder=None)
 
        ## getting and plotting the expected and observed best contours
        f = ROOT.TFile(args.nominalFileName)
        f.ls
        
        plot.drawExpected( f.Get("Exp"), alpha=1,width=2,legendOrder=1 )
	plot.drawObserved( f.Get("Obs"), legendOrder=1,title="Observed Limit")
        
	## Draw Lables
	coordinates=[xMinLine,yMinLine,xMaxLine,yMaxLine]
	lablelocation_cus=[forbiddenLabelX,forbiddenLabelY+0.1]
	plot.drawLine(coordinates,color=ROOT.kGray+2, label = forbiddenLabelText, labelLocation=lablelocation_cus ,angle=math.degrees(math.atan2(((yMaxLabel-yMinLabel))/((yMax-yMin)/(600.0-600.0*0.17)),((xMaxLabel-xMinLabel))/((xMax-xMin)/(800.0-800.0*(0.2+0.07))))))
 
       
        plot.decorateCanvas( )

        legendPosition=(0.60,0.70,0.98,0.91)

        # Draw legend
        legend = plot.createLegend(shape=legendPosition )
        legend.SetTextSize(0.035)
        legend.Draw()

	plot.writePlot( )
 
        # writting txt file with best SR per signal point using the clean df bestJSON:
        # sorting first
        bestJSON=bestJSON.sort_values(["m0", "m12"], ascending = (True, True))
        
        #print bestJSON
        bestJSON.to_csv(outputNamePlot+plotTag+'.txt',index = False, sep=',',header=False)
        


def createTGraph(name,x,y):

    pG = ROOT.TGraph(len(x),x,y)
    pG.SetName(name)

    return  pG


if __name__ == "__main__":
		main()

