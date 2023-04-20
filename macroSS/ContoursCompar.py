#!/usr/bin/env python

##########################################
#
# Tools for making final SS contour plots
#
##########################################

import ROOT, argparse, sys, os, math
from array import array
import contourPlotter
import axisLabelsProcessDescriptions

ROOT.gROOT.SetBatch()

parser = argparse.ArgumentParser()
parser.add_argument("--FileName", type = str, help="input file names, seperated by ;", default="file1.root;file2.root")

args = parser.parse_args()

drawTheorySysts = True

def main():
	"""Main function for driving the whole thing..."""
	print(">>>Welcome to Final Coutour Plotter!!!")

	# Print out the settings
	for setting in dir(args):
		if not setting[0]=="_":
			print( ">>> ... Setting: {: >20} {: >40}".format(setting, eval("args.%s"%setting) ) )

	# Find which grid we are working with

	model=""
	modelName = ""
	nBinsX = 19
	xMin = 800
	xMax = 2000
	nsY = 24
	yMin = 0
	yMax = 900

	yMinLine =0
	yMaxLine =0
	xMinLine =0
	xMaxLine =0

	if "SusyGtt" in args.FileName:
		model = "SUSY_GTT"
		modelName = "Gtt"

	if "SusyComprGtt" in args.FileName:
		model = "SUSY_COMPR_GTT"
		modelName = "ComprGtt"
	
	if "SusyBtt" in args.FileName:
		model = "SUSY_BTT"
		modelName = "SusyBtt"

	if "SusyGSL" in args.FileName:
		model = "SUSY_GSL"
		modelName = "SusyGSL"

	if "SusyGG2StepWZ" in args.FileName:
		model = "SUSY_GG2STEPWZ"
		modelName = "SusyGG2StepWZ"

	if "SusyGG_Rpv321" in args.FileName:
		model = "SUSY_GG_RPV321"
		modelName = "SusyGG_Rpv321"

	if "SusyTT2Step" in args.FileName:
		model = "SUSY_TT2STEP"
		modelName = "SusyTT2Step"

	labelsPerGrid = axisLabelsProcessDescriptions.getLabelsPerGrid()
	forbiddenRegionCut=labelsPerGrid["Mc15"+modelName].forbiddenCut*1.0
	forbiddenLabelX=labelsPerGrid["Mc15"+modelName].forbiddenLabelXVal*1.0
	forbiddenLabelY=labelsPerGrid["Mc15"+modelName].forbiddenLabelYVal*1.0
	forbiddenLabelText="{0}".format(labelsPerGrid["Mc15"+modelName].forbiddenLabelText)
	xLabel="{0}".format(labelsPerGrid["Mc15"+modelName].xLabel)
	yLabel="{0}".format(labelsPerGrid["Mc15"+modelName].yLabel)
	processDescription="{0}".format(labelsPerGrid["Mc15"+modelName].processDescription)


	if "SusyGtt" in args.FileName:
		model = "SUSY_GTT"
		modelName = "Gtt"

		print ">>> In Gtt model!!!"
		
		nBinsX = 1100
		xMin = 750
		xMax = 1850
		nBinsY = 1600
		yMin = 100
		yMax = 1900

		xMinLine = yMin + forbiddenRegionCut
		xMaxLine = yMax + forbiddenRegionCut
		yMinLine = xMin - forbiddenRegionCut
		yMaxLine = xMax - forbiddenRegionCut
		if xMinLine < xMin:
			xMinLine = xMin
		if yMinLine < yMin:
			yMinLine = yMin
		if xMaxLine > xMax:
			xMaxLine = xMax
		if yMaxLine > xMax:
			yMaxLine = yMax

		xMinLabel=xMinLine
		xMaxLabel=xMaxLine
		yMinLabel=yMinLine
		yMaxLabel=yMaxLine

		m = (yMaxLine-yMinLine)/(xMaxLine-xMinLine)
		q = yMinLine-m*xMinLine

		yMaxLine=m*1400+q
		xMaxLine=1400

	if "SusyComprGtt" in args.FileName:
		model = "SUSY_COMPR_GTT"
		modelName = "ComprGtt"
	
		print ">>> In Gtt COMPR model!!!"
	
		nBinsX = 1100
		xMin = 750
		xMax = 2000
		nBinsY = 1600
		yMin = 5
		yMax = 150

		xMinLine = yMin + forbiddenRegionCut
		xMaxLine = yMax + forbiddenRegionCut
		yMinLine = xMin - forbiddenRegionCut
		yMaxLine = xMax - forbiddenRegionCut
		if xMinLine < xMin:
			xMinLine = xMin
		if yMinLine < yMin:
			yMinLine = yMin
		if xMaxLine > xMax:
			xMaxLine = xMax
		if yMaxLine > xMax:
			yMaxLine = yMax

		xMinLabel=xMinLine
		xMaxLabel=xMaxLine
		yMinLabel=yMinLine
		yMaxLabel=yMaxLine

		m = (yMaxLine-yMinLine)/(xMaxLine-xMinLine)
		q = yMinLine-m*xMinLine

		yMaxLine=m*650+q
		xMaxLine=2000




	if "SusyBtt" in args.FileName:
		model = "SUSY_BTT"
		modelName = "SusyBtt"

		print ">>> In Btt model!!!"

		nBinsX = 19
		nBinsY = 400
		xMax = 950
		nBinsY = 23
		yMin = 1
		yMax = 700

		xMinLine = yMin + forbiddenRegionCut
		xMaxLine = yMax + forbiddenRegionCut
		yMinLine = xMin - forbiddenRegionCut
		yMaxLine = xMax - forbiddenRegionCut
		if xMinLine < xMin:
			xMinLine = xMin
		if yMinLine < yMin:
			yMinLine = yMin
		if xMaxLine > xMax:
			xMaxLine = xMax
		if yMaxLine > xMax:
			yMaxLine = yMax

		xMinLabel=xMinLine
		xMaxLabel=xMaxLine
		yMinLabel=yMinLine
		yMaxLabel=yMaxLine

		m = (yMaxLine-yMinLine)/(xMaxLine-xMinLine)
		q = yMinLine-m*xMinLine

		yMaxLine=m*650+q
		xMaxLine=650

	if "SusyGSL" in args.FileName:
		model = "SUSY_GSL"
		modelName = "SusyGSL"

		print ">>> In GSL model!!!"

		nBinsX = 20
		xMin = 600
		xMax = 2300
		nBinsY = 23
		yMin = 200
		yMax = 2200

		xMinLine = yMin + forbiddenRegionCut
		xMaxLine = yMax + forbiddenRegionCut
		yMinLine = xMin - forbiddenRegionCut
		yMaxLine = xMax - forbiddenRegionCut
		if xMinLine < xMin:
			xMinLine = xMin
		if yMinLine < yMin:
			yMinLine = yMin
		if xMaxLine > xMax:
			xMaxLine = xMax
		if yMaxLine > xMax:
			yMaxLine = yMax

		xMinLabel=xMinLine
		xMaxLabel=xMaxLine
		yMinLabel=yMinLine
		yMaxLabel=yMaxLine

		m = (yMaxLine-yMinLine)/(xMaxLine-xMinLine)
		q = yMinLine-m*xMinLine

		yMaxLine=m*1600+q
		xMaxLine=1600

	if "SusyGG2StepWZ" in args.FileName:
		model = "SUSY_GG2STEPWZ"
		modelName = "SusyGG2StepWZ"

		print ">>> In 2-stepWZ model!!!"

		nBinsX = 19;
		xMin = 700;
		xMax = 2000;
		nBinsY = 24;
		yMin = 100;
		yMax = 2000;

		xMinLine = yMin + forbiddenRegionCut
		xMaxLine = yMax + forbiddenRegionCut
		yMinLine = xMin - forbiddenRegionCut
		yMaxLine = xMax - forbiddenRegionCut
		if xMinLine < xMin:
			xMinLine = xMin
		if yMinLine < yMin:
			yMinLine = yMin
		if xMaxLine > xMax:
			xMaxLine = xMax
		if yMaxLine > xMax:
			yMaxLine = yMax

		xMinLabel=xMinLine
		xMaxLabel=xMaxLine
		yMinLabel=yMinLine
		yMaxLabel=yMaxLine

		m = (yMaxLine-yMinLine)/(xMaxLine-xMinLine)
		q = yMinLine-m*xMinLine

		yMaxLine=m*1350+q
		xMaxLine=1350


	if "SusyGG_Rpv321" in args.FileName:
		model = "SUSY_GG_RPV321"
		modelName = "SusyGG_Rpv321"

		print ">>> In SusyGG_Rpv321 model!!!"

		nBinsX = 19
		xMin = 800
		xMax = 1600
		nBinsY = 24
		yMin = 400
		yMax = 1600

		xMinLine = yMin + forbiddenRegionCut
		xMaxLine = yMax + forbiddenRegionCut
		yMinLine = xMin - forbiddenRegionCut
		yMaxLine = xMax - forbiddenRegionCut
		if xMinLine < xMin:
			xMinLine = xMin
		if yMinLine < yMin:
			yMinLine = yMin
		if xMaxLine > xMax:
			xMaxLine = xMax
		if yMaxLine > xMax:
			yMaxLine = yMax

		xMinLabel=xMinLine
		xMaxLabel=xMaxLine
		yMinLabel=yMinLine
		yMaxLabel=yMaxLine

		m = (yMaxLine-yMinLine)/(xMaxLine-xMinLine)
		q = yMinLine-m*xMinLine

		yMaxLine=m*1400+q
		xMaxLine=1400

	if "SusyTT2Step" in args.FileName:
		model = "SUSY_TT2STEP"
		modelName = "SusyTT2Step"

		print ">>> In SusyTT2Step model!!!"

		nBinsX = 19
		xMin = 500
		xMax = 900
		nBinsY = 24
		yMin = 200
		yMax = 600

		xMinLine = yMin + forbiddenRegionCut
		xMaxLine = yMax + forbiddenRegionCut
		yMinLine = xMin - forbiddenRegionCut
		yMaxLine = xMax - forbiddenRegionCut
		if xMinLine < xMin:
			xMinLine = xMin
		if yMinLine < yMin:
			yMinLine = yMin
		if xMaxLine > xMax:
			xMaxLine = xMax
		if yMaxLine > xMax:
			yMaxLine = yMax

		xMinLabel=xMinLine
		xMaxLabel=xMaxLine
		yMinLabel=yMinLine
		yMaxLabel=yMaxLine

		m = (yMaxLine-yMinLine)/(xMaxLine-xMinLine)
		q = yMinLine-m*xMinLine

		yMaxLine=m*1400+q
		xMaxLine=1400

	
	# Open the files that we need
	plot = contourPlotter.contourPlotter(model,800,600)
	plot.processLabel = processDescription
	lumitag = 36.1
	plot.lumiLabel = "#sqrt{{s}}=13 TeV, {0} fb^{{-1}}, All limits at 95% CL".format(lumitag)
	plot.drawAxes( [xMin,yMin,xMax,yMax] )

	Files = args.FileName.split(";")
	Tag = 1

	for filename in Files:
		print filename
		f = ROOT.TFile(filename)
		if Tag==1:
			plot.drawObserved( f.Get("Obs_0"), title="Observed Limit with [25,25,10]")
		else:
			#f1 = ROOT.TFile(filename)
			plot.drawObserved( f.Get("Obs_0"), title="Observed Limit with [20,20,10]", color=ROOT.kBlack)
		f.Close()
		Tag = Tag + 1

	## Draw Lines
	plot.setXAxisLabel(xLabel)
	plot.setYAxisLabel(yLabel)

	plot.createLegend(shape=(0.22,0.58,0.55,0.77) ).Draw()

	## Draw Lables
	print xMinLine, yMinLine, xMaxLine, yMaxLine
	coordinates=[xMinLine,yMinLine,xMaxLine,yMaxLine]
	lablelocation_cus=[forbiddenLabelX,forbiddenLabelY]
	plot.drawLine(coordinates, label = forbiddenLabelText, labelLocation = lablelocation_cus, angle=180.0/3.1415927*math.atan2((yMaxLabel-yMinLabel)/(yMax-yMin),(xMaxLabel-xMinLabel)/(xMax-xMin)))
	
	plot.decorateCanvas( )
	plot.writePlot( )


if __name__ == "__main__":
		main()

