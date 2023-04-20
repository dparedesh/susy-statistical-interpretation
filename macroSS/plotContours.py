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

ROOT.gROOT.SetBatch()

parser = argparse.ArgumentParser()
parser.add_argument("--nominalFileName", type = str, help="input nominal file name", default="m0m12_nofloat_exp.root")
parser.add_argument("--model",help="input model")
parser.add_argument("--lumi", type = float, help="", default=20)
parser.add_argument("--drawCLs",action="store_true",help="if True it will draw the  gray numbers with the CLs value",default=False)
parser.add_argument("--drawCLsExp",action="store_true",help="if True it will draw the  gray numbers with the expected CLs value",default=False)
parser.add_argument("--drawXS",action="store_true",help="if True it will draw gray numbers with the upper limit on the cross-section",default=False)
parser.add_argument("--outputNamePlot",type=str,help="Get name of the output plot",default=None)
parser.add_argument("--draw1D",action="store_true",help="option used just to produce brazilian plots",default=False)
parser.add_argument("--makeBest",action="store_true",help="This is to say to the tool the name of the output curves to be taken. Those names are different from the output taken from harvestToContours.py and from multiplexContours.py")

args = parser.parse_args()

drawTheorySysts = False
labelAtlas="#bf{Internal}"

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
        theoryLegend = model.theoryLegend

        xMinLine = model.xMinLine
        yMinLine = model.yMinLine
        xMaxLine = model.xMaxLine
        yMaxLine = model.yMaxLine

        yMaxLabel = model.yMaxLabel
        yMinLabel = model.yMinLabel
        xMaxLabel = model.xMaxLabel
        xMinLabel = model.xMinLabel
        extraText = model.extraText

        modelName = model.modelName
        outputNamePlot = args.outputNamePlot

        #harvestToContours.py and multiplexContours.py produce plots with different names...
        if args.makeBest:
            obs_up = "Obs_u1s"
            obs_dn = "Obs_d1s"
            expected_band = "ExpectedBand"
            expected = "Exp"
            observed = "Obs"
        else:
            obs_up = "Obs_0_Up"
            obs_dn = "Obs_0_Down"
            expected = "Exp_0"
            observed = "Obs_0"
            expected_band = "Band_1s_0"  

	plotTag=""
        if args.drawCLs: plotTag="_CLs"
        elif args.drawCLsExp: plotTag="_CLsExp"	
	elif args.drawXS: plotTag="_xsec"	

	# Open the files that we need
	plot = contourPlotter.contourPlotter(outputNamePlot+plotTag,800,600)
        plot.setXAxisLabel(xLabel)
        plot.setYAxisLabel(yLabel)
	plot.processLabel = processDescription
	args.lumi=args.lumi/1000.0
	lumitag = str(args.lumi)
	plot.lumiLabel = "#splitline{{#it{{ATLAS}} {1} }}{{#bf{{#splitline{{#sqrt{{s}}=13 TeV, {0:d} fb^{{-1}}}}{{All limits at 95% CL}}}}}}".format(int(round(args.lumi)),labelAtlas)

        plot.drawAxes( [xMin,yMin,xMax,yMax] )
        ROOT.gPad.SetTicks()

        legendPosition=(0.5,0.70,0.88,0.91)


	f = ROOT.TFile(args.nominalFileName)
	f.ls

	## Main Result
        if args.draw1D:
            plot.canvas.SetLogy()

            plot.drawBand( f.Get("Band_2s_0"),ROOT.TColor.GetColor("#ffe938"),"Expected #pm 2#sigma",legendOrder=5)
            plot.drawBand( f.Get("Band_1s_0"),ROOT.kGreen, "Expected #pm 1#sigma",legendOrder=4)

            plot.drawExpected( f.Get("Exp_0"), alpha=1,width=2,legendOrder=3, outFileName=pathUtilities.histFitterUser()+"/"+outputNamePlot+"_Exp_"+"Limit.txt" )
            plot.drawObserved( f.Get("Obs_0"), title="Observed Limit",legendOrder=2, alpha=1, outFileName=pathUtilities.histFitterUser()+"/"+outputNamePlot+"_Obs_"+"Limit.txt" )

            # draw previous limits
            if '36fb' in previousLimits: 
                plot.drawObserved(previousLimits['36fb'].plot, color=ROOT.kMagenta, title=previousLimits['36fb'].legend,alpha=1, legendOrder=6)

            # draw theory
            plot.drawTheory(f.Get("theory"),color=ROOT.kBlue,title=theoryLegend)
            plot.drawTheoryUncertaintyCurve( f.Get("theory_up"),color=ROOT.kBlue )
            plot.drawTheoryUncertaintyCurve( f.Get("theory_down"),color=ROOT.kBlue )

            legendPosition=(0.57,0.5,0.79,0.91)

            plot.decorateCanvas(size=0.025)
         
        else:      

 	    if args.drawCLs:
                plot.drawTextFromTGraph2D( f.Get("CLs_gr"), angle=30, title = "Grey Numbers Represent Observed CLs Value" , outFileName=pathUtilities.histFitterUser()+"/"+outputNamePlot+"_Obs_"+"CLs.txt", format="%.2g")
            elif args.drawCLsExp: 
		plot.drawTextFromTGraph2D( f.Get("CLsexp_gr"), angle=30, title = "Grey Numbers Represent Expected CLs Value" , outFileName=pathUtilities.histFitterUser()+"/"+outputNamePlot+"_Exp_"+"CLs.txt", format="%.2g")
            elif args.drawXS:
	        plot.drawTextFromTGraph2D( f.Get("excludedXsec_gr"), angle=30, title = "Numbers give 95% CL excluded model cross sections [fb]" , outFileName=pathUtilities.histFitterUser()+"/"+outputNamePlot+"_Obs_"+"UpperLimitsXsec.txt", format="%.2g")

	    plot.drawOneSigmaBand( f.Get(expected_band) )


	    plot.drawExpected( f.Get(expected),outFileName=pathUtilities.histFitterUser()+"/"+outputNamePlot+"_Exp_"+"Limit.txt" )
	    plot.drawObserved( f.Get(observed), title="Observed Limit (#pm1 #sigma_{theory}^{SUSY})" if drawTheorySysts else "Observed Limit",outFileName=pathUtilities.histFitterUser()+"/"+outputNamePlot+"_Obs_"+"Limit.txt" )

            #we can always loop over all the previous limits, but doing like this since we only want to see the ones from 36fb-1
            if "36fb" in previousLimits: # default previous limit
                plot.drawShadedRegion(previousLimits['36fb'].plot, color=ROOT.kCyan-9, title=previousLimits['36fb'].legend,legendOrder=1)
            if "20.3fb" in previousLimits and (modelName == "SusySS2StepWZ" or modelName == "SusySS2StepSL"): # For Rpc SS grids
                plot.drawShadedRegion(previousLimits['20.3fb'].plot, color=ROOT.kCyan-9, title=previousLimits['20.3fb'].legend,legendOrder=1)
            if "139fb" in previousLimits and (modelName == "SusyGG_Rpv331"): # For Rpv331
                plot.drawShadedRegion(previousLimits['139fb'].plot, color=ROOT.kCyan-9, title=previousLimits['139fb'].legend,legendOrder=1)

            
	    if drawTheorySysts:
                plot.drawTheoryUncertaintyCurve( f.Get(obs_up) )
                plot.drawTheoryUncertaintyCurve( f.Get(obs_dn) )
                plot.drawTheoryLegendLines( xyCoord=(0.515,0.792), length=0.065 )
           
        
	    ## Draw Lables
	    print xMinLine, yMinLine, xMaxLine, yMaxLine, forbiddenLabelText
	    coordinates=[xMinLine,yMinLine,xMaxLine,yMaxLine]
	    lablelocation_cus=[forbiddenLabelX,forbiddenLabelY+0.1]
	    plot.drawLine(coordinates, label = forbiddenLabelText, labelLocation=lablelocation_cus ,angle=math.degrees(math.atan2(((yMaxLabel-yMinLabel))/((yMax-yMin)/(600.0-600.0*0.17)),((xMaxLabel-xMinLabel))/((xMax-xMin)/(800.0-800.0*(0.2+0.07))))))
	    if modelName == "SusyGG2StepWZ":
		plot.drawLine([1000,1000,1800,1800], label = "m(#tilde{g}) < m(#tilde{#chi}_{1}^{0})", labelLocation=[1400,1470] ,angle=math.degrees(math.atan2(((yMaxLabel-yMinLabel))/((yMax-yMin)/(600.0-600.0*0.17)),((xMaxLabel-xMinLabel))/((xMax-xMin)/(800.0-800.0*(0.2+0.07))))))
 
       
            plot.decorateCanvas( )

        print legendPosition

        # Draw legend
        legend = plot.createLegend(shape=legendPosition )
        legend.SetTextSize(0.035)
        legend.Draw()
       
        if extraText is not None: plot.drawExtraText(extraText)

        ROOT.gPad.RedrawAxis()
        plot.canvas.Update()	

	plot.writePlot( )


if __name__ == "__main__":
		main()

