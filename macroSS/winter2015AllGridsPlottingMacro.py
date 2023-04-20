#!/usr/bin/env python

##########################################
#
# Tools for making final SS contour plots
#
##########################################

import ROOT, argparse, sys, os, math
from array import array
import contourPlotter

ROOT.gROOT.SetBatch()

parser = argparse.ArgumentParser()
parser.add_argument("--nominalFileName", type = str, help="input nominal file name", default="m0m12_nofloat_exp.root")
parser.add_argument("--theoryUpFileName",type = str, help="input theory up file name", default="m0m12_nofloat_exp.root")
parser.add_argument("--theoryDownFileName", type = str, help="input theory down file name", default="m0m12_nofloat_exp.root")
parser.add_argument("--upperLimitFile", type = str, help="", default="Merged_Output_hypotest_SM_SS_twostepCN_sleptons_SR4_combined_ul__1_harvest_list")
parser.add_argument("--fileNameSR3b", type = str, help="", default="None")
parser.add_argument("--fileNameSR3bDesc", type = str, help="", default="None")
parser.add_argument("--fileNameSR1b", type = str, help="", default="None")
parser.add_argument("--fileNameSR1bDesc", type = str, help="", default="None")
parser.add_argument("--fileNameSR0b3j", type = str, help="", default="None")
parser.add_argument("--fileNameSR0b3jDesc", type = str, help="", default="None")
parser.add_argument("--fileNameSR0b5j", type = str, help="", default="None")
parser.add_argument("--fileNameSR0b5jDesc", type = str, help="", default="None")
parser.add_argument("--prefix", type = str, help="", default="")
parser.add_argument("--lumi", type = float, help="", default=20)
parser.add_argument("--showsig", type = bool, help="", default=True)
parser.add_argument("--discexcl", type = int, help="", default=1)
parser.add_argument("--showtevatron", type = int, help="", default=0)
parser.add_argument("--xLabel", type = str, help="", default="notSpecified")
parser.add_argument("--yLabel", type = str, help="", default="notSpecified")
parser.add_argument("--processDescription", type = str, help="", default="unknown grid")
parser.add_argument("--forbiddenRegionCut", type = float, help="", default=0)
parser.add_argument("--forbiddenLabelX", type = float, help="", default=0)
parser.add_argument("--forbiddenLabelY", type = float, help="", default=0)
parser.add_argument("--forbiddenLabelText", type = str, help="", default="None")
parser.add_argument("--showSingleSR", type = bool, help="", default=False)
parser.add_argument("--hname0", type = str, help="", default="sigp1clsf")
parser.add_argument("--hname0_exp", type = str, help="", default="sigp1expclsf")
parser.add_argument("--hname0_1su", type = str, help="", default="sigclsu1s")
parser.add_argument("--hname0_1sd", type = str, help="", default="sigclsd1s")
parser.add_argument("--hname1", type = str, help="", default="sigp0")
parser.add_argument("--hname1_exp", type = str, help="", default="sigp0")
parser.add_argument("--fnameMass", type = str, help="", default="mSugraGridtanbeta10_gluinoSquarkMasses.root")

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
        
        signalRegion=args.nominalFileName.split("/")[-1].split("_")[3]
        if 'best' in args.nominalFileName:
            signalRegion='BEST'


	if "None" not in args.forbiddenLabelText:

		xMinLine = yMin + args.forbiddenRegionCut
		xMaxLine = yMax + args.forbiddenRegionCut
		yMinLine = xMin - args.forbiddenRegionCut
		yMaxLine = xMax - args.forbiddenRegionCut
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

	if "SusyGtt" in args.nominalFileName:
		model = "SUSY_GTT"
		modelName = "Gtt"

		print ">>> In Gtt model!!!"
		
		nBinsX = 1100
		xMin = 750
		xMax = 1850
		nBinsY = 1600
		yMin = 100
		yMax = 1900

		xMinLine = yMin + args.forbiddenRegionCut
		xMaxLine = yMax + args.forbiddenRegionCut
		yMinLine = xMin - args.forbiddenRegionCut
		yMaxLine = xMax - args.forbiddenRegionCut
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

	if "SusyComprGtt" in args.nominalFileName:
		model = "SUSY_COMPR_GTT"
		modelName = "ComprGtt"
	
		print ">>> In Gtt COMPR model!!!"
	
		nBinsX = 1100
		xMin = 750
		xMax = 2000
		nBinsY = 1600
		yMin = 5
		yMax = 150

		xMinLine = yMin + args.forbiddenRegionCut
		xMaxLine = yMax + args.forbiddenRegionCut
		yMinLine = xMin - args.forbiddenRegionCut
		yMaxLine = xMax - args.forbiddenRegionCut
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




	if "SusyBtt" in args.nominalFileName:
		model = "SUSY_BTT"
		modelName = "SusyBtt"

		print ">>> In Btt model!!!"

		nBinsX = 500
		xMin = 425
		xMax = 950
		nBinsY = 23
		yMin = 60
		yMax = 700

		xMinLine = yMin + args.forbiddenRegionCut
		xMaxLine = yMax + args.forbiddenRegionCut
		yMinLine = xMin - args.forbiddenRegionCut
		yMaxLine = xMax - args.forbiddenRegionCut
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

	if "SusyGSL" in args.nominalFileName:
		model = "SUSY_GSL"
		modelName = "SusyGSL"

		print ">>> In GSL model!!!"

		nBinsX = 19;
		xMin = 600;
		xMax = 2200;
		nBinsY = 24;
		yMin = 200;
		yMax = 2200;

		xMinLine = yMin + args.forbiddenRegionCut
		xMaxLine = yMax + args.forbiddenRegionCut
		yMinLine = xMin - args.forbiddenRegionCut
		yMaxLine = xMax - args.forbiddenRegionCut
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

	if "SusyGG2StepWZ" in args.nominalFileName:
		model = "SUSY_GG2STEPWZ"
		modelName = "SusyGG2StepWZ"

		print ">>> In 2-stepWZ model!!!"

		nBinsX = 19;
		xMin = 700;
		xMax = 2000;
		nBinsY = 24;
		yMin = 100;
		yMax = 2000;

		xMinLine = yMin + args.forbiddenRegionCut
		xMaxLine = yMax + args.forbiddenRegionCut
		yMinLine = xMin - args.forbiddenRegionCut
		yMaxLine = xMax - args.forbiddenRegionCut
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


	if "SusyGG_Rpv331" in args.nominalFileName:
		model = "SUSY_GG_RPV331"
		modelName = "SusyGG_Rpv331"

		print ">>> In SusyGG_Rpv331 model!!!"

		nBinsX = 19
		xMin = 800
		xMax = 1800
		nBinsY = 24
		yMin = 400
		yMax = 1600

		xMinLine = yMin + args.forbiddenRegionCut
		xMaxLine = yMax + args.forbiddenRegionCut
		yMinLine = xMin - args.forbiddenRegionCut
		yMaxLine = xMax - args.forbiddenRegionCut
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

	if "SusyGG_Rpv321" in args.nominalFileName:
		model = "SUSY_GG_RPV321"
		modelName = "SusyGG_Rpv321"

		print ">>> In SusyGG_Rpv321 model!!!"

		nBinsX = 19
		xMin = 800
		xMax = 1600
		nBinsY = 24
		yMin = 400
		yMax = 1600

		xMinLine = yMin + args.forbiddenRegionCut
		xMaxLine = yMax + args.forbiddenRegionCut
		yMinLine = xMin - args.forbiddenRegionCut
		yMaxLine = xMax - args.forbiddenRegionCut
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

	if "SusyTT2Step" in args.nominalFileName:
		model = "SUSY_TT2STEP"
		modelName = "SusyTT2Step"

		print ">>> In SusyTT2Step model!!!"

		nBinsX = 19
		xMin = 500
		xMax = 900
		nBinsY = 24
		yMin = 200
		yMax = 600

		xMinLine = yMin + args.forbiddenRegionCut
		xMaxLine = yMax + args.forbiddenRegionCut
		yMinLine = xMin - args.forbiddenRegionCut
		yMaxLine = xMax - args.forbiddenRegionCut
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

	if "SusyGG_RpvLQD" in args.nominalFileName:
		model = "SUSYGG_RpvLQD"
		modelName = "SusyGG_RpvLQD"

		print ">>> In SusyGG_RpvLQD model!!!"

		nBinsX = 19
		xMin = 1000
		xMax = 2300
		nBinsY = 24
		yMin = 100
		yMax = 2600

		xMinLine = yMin + args.forbiddenRegionCut
		xMaxLine = yMax + args.forbiddenRegionCut
		yMinLine = xMin - args.forbiddenRegionCut
		yMaxLine = xMax - args.forbiddenRegionCut
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

################### Trying to get previous limits on the plot ##############################

	if modelName == "SusyGG2StepWZ" or modelName == "SusyBtt" or modelName == "SusyGSL": 
		PreLimit_XAxis = GetPreLimit_XAxis(modelName)
		PreLimit_YAxis = GetPreLimit_YAxis(modelName)
		PreLimit_title = GetPreLimit_title(modelName)
		PreLimit_XAxis.append(xMin)
		PreLimit_YAxis.append(yMin)
		PreLimit = ROOT.TGraph(len(PreLimit_XAxis),array('f', PreLimit_XAxis),array('f', PreLimit_YAxis))
	if modelName == "SusyGG2StepWZ":
		Ad_PreLimit_XAxis = Ad_GetPreLimit_XAxis(modelName)
		Ad_PreLimit_YAxis = Ad_GetPreLimit_YAxis(modelName)
		Ad_PreLimit_XAxis.append(xMin)
		Ad_PreLimit_YAxis.append(yMin)
		Ad_PreLimit_title = Ad_GetPreLimit_title(modelName)
		Ad_PreLimit = ROOT.TGraph(len(Ad_PreLimit_XAxis),array('f', Ad_PreLimit_XAxis),array('f', Ad_PreLimit_YAxis))

	
	# Open the files that we need
	plot = contourPlotter.contourPlotter(model+'_'+signalRegion,800,600)
	plot.processLabel = args.processDescription
	args.lumi=args.lumi/1000.0
	lumitag = str(args.lumi)
	plot.lumiLabel = "#splitline{{ATLAS Preliminary}}{{#bf{{#sqrt{{s}}=13 TeV, {0} fb^{{-1}}, All limits at 95% CL}}}}".format(lumitag)

	f = ROOT.TFile(args.nominalFileName)
	f.ls

	## Axes

	plot.drawAxes( [xMin,yMin,xMax,yMax] )

	## Main Result

	plot.drawTextFromTGraph2D( f.Get("CLs_gr"), angle=30, title = "Grey Numbers Represent Observed CLs Value" )

	plot.drawOneSigmaBand( f.Get("Band_1s_0") )
	plot.drawExpected( f.Get("Exp_0") )
	plot.drawObserved( f.Get("Obs_0"), title="Observed Limit (#pm1 #sigma_{theory}^{SUSY})" if drawTheorySysts else "Observed Limit")
	if modelName == "SusyGG2StepWZ" or modelName == "SusyBtt" or modelName == "SusyGSL":
		plot.drawShadedRegion(PreLimit, color=ROOT.kBlue, title=PreLimit_title, legendOrder=1)
	if modelName == "SusyGG2StepWZ":
		plot.drawShadedRegion(Ad_PreLimit, color=ROOT.kMagenta+2, title=Ad_PreLimit_title, legendOrder=1)

	## Draw Lines
	plot.setXAxisLabel(args.xLabel)
	plot.setYAxisLabel(args.yLabel)

	plot.createLegend(shape=(0.22,0.58,0.55,0.77) ).Draw()

	## Draw Lables
	print xMinLine, yMinLine, xMaxLine, yMaxLine
	coordinates=[xMinLine,yMinLine,xMaxLine,yMaxLine]
	lablelocation_cus=[args.forbiddenLabelX,args.forbiddenLabelY]
	plot.drawLine(coordinates, label = args.forbiddenLabelText, labelLocation = lablelocation_cus, angle=180/3.1415927*math.atan2((yMaxLabel-yMinLabel)/(yMax-yMin),(xMaxLabel-xMinLabel)/(xMax-xMin)))

	if drawTheorySysts:
		fup = ROOT.TFile(args.theoryUpFileName)
		plot.drawTheoryUncertaintyCurve( fup.Get("Obs_0") )
		fdown = ROOT.TFile(args.theoryDownFileName)
		plot.drawTheoryUncertaintyCurve( fdown.Get("Obs_0") )

		plot.drawTheoryLegendLines( xyCoord=(0.234,0.6625), length=0.057 )
	
	plot.decorateCanvas( )
	plot.writePlot( )


def GetPreLimit_XAxis(modelName):
	if modelName == "SusyGG2StepWZ":
		PreLimit_XAxis=[700,708,721,724,745,751,772,779,790,807,834,861,889,916,944,971,1003,1026,1045,1052,1054,1058,1062,1066,1069,1070,1065,1072,1081,1084,1092,1100,1108,1109,1116,1121,1126,1131,1134,1133,1131,1130,1128,1126,1125,1123,1123]
		return PreLimit_XAxis
	if modelName == "SusyGtt":
		PreLimit_XAxis=[1035,1051,1079,1090,1106,1134,1161,1169,1189,1189,1196,1199,1202,1205,1207,1207,1206,1205,1205,1202,1197,1193,750]
		return PreLimit_XAxis
	if modelName == "SusyGSL":
		PreLimit_XAxis=[500,732,761,768,792,1012,1034,1048,1082,1118,1152,1178,1188,1198,1214,1222,1230,1246,1258,1263,1275,1282,1287,1292,1292,1298,1304,1309,1313,1315,1317,1318,1320,1321,1322,1324,1325,1326,1327,1327]
		return PreLimit_XAxis
	if modelName == "SusyBtt":
		PreLimit_XAxis=[425,439,453,460,467,481,494,508,510,519,522,532,536,537,541]
		return PreLimit_XAxis

def GetPreLimit_YAxis(modelName):
	if modelName == "SusyGG2StepWZ":
		PreLimit_YAxis=[425,441,459,460,476,480,494,501,511,529,541,542,541,539,537,538,546,543,529,511,507,494,476,459,441,424,406,389,376,371,354,336,319,316,301,284,266,249,231,214,196,179,161,144,126,109,90]
		return PreLimit_YAxis
	if modelName == "SusyGtt":
		PreLimit_YAxis=[680,681,682,679,675,666,648,638,597,597,556,515,474,433,391,350,309,268,227,186,145,100,400]
		return PreLimit_YAxis
	if modelName == "SusyGSL":
		PreLimit_YAxis=[390,638,662,670,688,828,838,840,847,850,851,838,829,812,788,774,762,738,721,712,688,662,638,612,608,588,562,538,512,488,462,438,412,388,362,338,312,288,262,100]
		return PreLimit_YAxis
	if modelName == "SusyBtt":
		PreLimit_YAxis=[138,136,133,129,126,120,116,115,115,100,97,86,77,72,55]
		return PreLimit_YAxis

def GetPreLimit_title(modelName):
	if modelName == "SusyGG2StepWZ":
		PreLimit_title = "SS/3L observed limit 2015 \n [arXiv:1602.09058]"
		return PreLimit_title
	if modelName == "SusyGtt":
		PreLimit_title = "SS/3L obs. limit 2015 \n [arXiv:1602.09058]"
		return PreLimit_title
	if modelName == "SusyGSL":
		PreLimit_title = "SS/3L obs. limit 2015 \n [arXiv:1602.09058]"
		return PreLimit_title
	if modelName == "SusyBtt":
		PreLimit_title = "SS/3L obs. limit 2015 \n [arXiv:1602.09058]"
		return PreLimit_title

def Ad_GetPreLimit_XAxis(modelName):
	if modelName == "SusyGG2StepWZ":
		Ad_PreLimit_XAxis=[1416.3,1416.3,1414.8,1412.5,1411.2,1409.2,1406.2,1404.2,1402.4,1400.6,1398.7,1397.1,1395.4,1393,1388.9,1384,1383.8,1377.4,1372.3,1368.3,1364.1,1358.8,1356.2,1352,1344.5,1336.7,1328.8,1325.9,1307.3,1301.2,1277.5,1273.8,1246.2,1230.5,1218.8,1191.2,1163.8,1136.2,1132.7,1108.8,1100.4,1081.2,1053.8,1030.5,1026.2,998.8,971.2,959.4,943.8,916.2,908.2,700]
		return Ad_PreLimit_XAxis

def Ad_GetPreLimit_YAxis(modelName):
	if modelName == "SusyGG2StepWZ":
		Ad_PreLimit_YAxis=[91.2,108.8,126.2,143.8,152.6,161.2,178.8,196.2,213.8,231.2,248.8,266.2,283.8,301.2,318.8,336.2,337.3,353.8,371.2,388.8,406.2,423.8,431.2,441.2,458.8,476.2,489.7,493.8,511.2,515.7,528.8,530.7,541.4,546.2,549.8,553.6,552.4,548.3,546.2,535.2,528.8,519.5,513.1,511.2,510.8,504.7,496.7,493.8,488,479,476.2,350.0]
		return Ad_PreLimit_YAxis

def Ad_GetPreLimit_title(modelName):
	if modelName == "SusyGG2StepWZ":
		Ad_PreLimit_title = "Multijet observed limit 2015 \n [arXiv:1602.06194]"
		return Ad_PreLimit_title



if __name__ == "__main__":
		main()

