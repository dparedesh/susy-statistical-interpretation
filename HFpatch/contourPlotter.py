#!/usr/bin/env python

# contourPlotter.py #################
#
# Tools for making final contour plots. See contourPlotterExample.py
#
# By: Larry Lee - Dec 2017

import ROOT
ROOT.gROOT.SetBatch()

class contourPlotter:
	def __init__(self, plotName="test", xSize=800, ySize=600):
		self.plotName = plotName
		self.xSize    = xSize
		self.ySize    = ySize
		self.canvas   = ROOT.TCanvas(self.plotName,self.plotName,xSize,ySize)

		self.canvas.SetLeftMargin(0.2)
		self.canvas.SetRightMargin(0.07)
		self.canvas.SetTopMargin(0.07)

		self.xAxisLabel = "x label"
		self.yAxisLabel = "y label"

		self.processLabel = "Process Title -- Describe The Grid!"
		self.lumiLabel = "#sqrt{s}=XX TeV, YY fb^{-1}, All limits at 95% CL"

		self.bottomObject = 0
		self.legendObjects = []

		return


	def setXAxisLabel(self, label=""):
		self.xAxisLabel = label
		if self.bottomObject:
			self.bottomObject.GetXaxis().SetTitle(self.xAxisLabel)
		return

	def setYAxisLabel(self, label=""):
		self.yAxisLabel = label
		if self.bottomObject:
			self.bottomObject.GetYaxis().SetTitle(self.yAxisLabel)
		return

	def drawAxes(self, axisRange=[0,0,2000,2000]):
		self.canvas.cd()
		self.bottomObject = self.canvas.DrawFrame( *axisRange )
		self.bottomObject.SetTitle(";%s;%s"%(self.xAxisLabel,self.yAxisLabel) )
		self.bottomObject.GetYaxis().SetTitleOffset(1.8)
		self.canvas.Update()
		return

	def drawOneSigmaBand(self, band, color=ROOT.TColor.GetColor("#ffd700"), alpha=0.5, legendOrder=0):
		self.canvas.cd()
		band.SetFillColorAlpha(color,alpha)
		band.SetFillStyle(1001)
		band.SetLineStyle(1)
		band.SetLineWidth(1)
		band.SetLineColorAlpha(ROOT.kGray,0.5)
		band.Draw("F")
                band.Draw("L")
		self.canvas.Update()
		tmpLegendObject = band.Clone("1SigmaBand")
		tmpLegendObject.SetLineColor(ROOT.kBlack)
		tmpLegendObject.SetLineStyle(7)
		tmpLegendObject.SetLineWidth(1)
		if type(legendOrder) == int:
			self.legendObjects.append( ( legendOrder, tmpLegendObject, "Expected Limit (#pm1 #sigma_{exp})", "lf" ) )
		return

        def drawBand(self, band, color=ROOT.TColor.GetColor("#ffd700"),legend="Expected band", legendOrder=0):
                self.canvas.cd()
                band.SetFillColor(color)
                band.SetFillStyle(1001)
                band.SetLineStyle(1)
                band.SetLineWidth(1)
                band.SetLineColorAlpha(color,0.5)
                band.Draw("3")
                self.canvas.Update()
                tmpLegendObject = band.Clone(band.GetName())
                tmpLegendObject.SetLineColor(color)
                tmpLegendObject.SetLineStyle(1)
                tmpLegendObject.SetLineWidth(1)
                if type(legendOrder) == int:
                        self.legendObjects.append( ( legendOrder, tmpLegendObject,legend, "lf" ) )
                return




	def drawExpected(self, curve, color=ROOT.kBlack, alpha=0.9,width=1,legendOrder=None, title="Expected Limit", drawOption="L", outFileName="out_expect.txt"):
		self.canvas.cd()
		curve.SetLineColorAlpha(color,alpha)
		curve.SetLineStyle(7)
		curve.SetLineWidth(width)
		curve.Draw(drawOption)
		self.canvas.Update()
		x,y,n = curve.GetX(), curve.GetY(), curve.GetN()
		fout = open(outFileName,"w+")
		for i in xrange(n):
			print>>fout, ("%15s,%15s" %(x[i], y[i]))
		if type(legendOrder) == int:
			self.legendObjects.append( ( legendOrder, curve, title, "l" ) )
		return

	def drawObserved(self, curve, title="Observed Limit (#pm1 #sigma_{theory}^{SUSY})", color=ROOT.TColor.GetColor("#800000"), alpha=0.7, legendOrder=1, drawOption="L",outFileName="out_obs.txt"):
		self.canvas.cd()
		curve.SetLineColorAlpha(color,alpha)
		curve.SetLineStyle(1)
		curve.SetLineWidth(3)
		curve.Draw(drawOption)
		self.canvas.Update()
		x,y,n = curve.GetX(), curve.GetY(), curve.GetN()
		fout = open(outFileName,"w+")
		for i in xrange(n):
			print>>fout, ("%15s,%15s" %(x[i], y[i]))
		if type(legendOrder) == int:
			self.legendObjects.append( ( legendOrder, curve.Clone("Observed"), title, "L" ) )
		return

        def drawPoints(self,curve,color,marker=34,legendOrder=0):
                self.canvas.cd()
                curve.SetMarkerStyle(marker)
                curve.SetMarkerColor(color)               
                curve.Draw("P")
                self.canvas.Update()
                if type(legendOrder) == int:
                        self.legendObjects.append( ( legendOrder, curve.Clone(curve.GetName()),curve.GetName(), "P" ) )
                return


        def drawTheory(self, curve, title="Theory", color=ROOT.kBlue,legendOrder=0, drawOption="L"):
                self.canvas.cd()
                curve.SetLineColor(color)
                curve.SetLineStyle(1)
                curve.SetLineWidth(2)
                curve.Draw("L")
                self.canvas.Update()
                x,y,n = curve.GetX(), curve.GetY(), curve.GetN()
                tmpLegendObject = curve.Clone(curve.GetName())
                tmpLegendObject.SetLineColor(color)
                tmpLegendObject.SetLineStyle(3)
                tmpLegendObject.SetLineWidth(1)

                if type(legendOrder) == int:
                        self.legendObjects.append( ( legendOrder, curve.Clone(curve.GetName()), title, "L" ) )
                        self.legendObjects.append( ( legendOrder+1, tmpLegendObject,"Theoretical uncertainty", "L" ) )
                return


	def drawTheoryUncertaintyCurve(self, curve, color=ROOT.TColor.GetColor("#800000"), alpha=0.7,  style=3):
		self.canvas.cd()
		curve.SetLineColorAlpha(color,alpha)
		curve.SetLineStyle(style)
		curve.SetLineWidth(1)
		curve.Draw("L")
		self.canvas.Update()
		return

	def drawTextFromTGraph2D(self, graph, title="Grey numbers represent blah", color=ROOT.TColor.GetColor("#000000"), alpha=0.6, angle=30, size=0.015, format="%.1g", titlesize = 0.03,outFileName="out_CLs.txt"):
		self.canvas.cd()
		tmpText = ROOT.TLatex()
		tmpText.SetTextSize(size)
		tmpText.SetTextColorAlpha(color,alpha)
		tmpText.SetTextAngle(angle)
		x,y,z,n = graph.GetX(), graph.GetY(), graph.GetZ(), graph.GetN()
		fout = open(outFileName,"w+")
		for i in xrange(n):
#			print (x[i],y[i],format%z[i])
			tmpText.DrawLatex(x[i],y[i],format%z[i])
			print>>fout, ("%15s,%15s,%15s" %(x[i], y[i], z[i]))

		tmpText.SetTextSize(titlesize)
		tmpText.SetTextAngle(-90)
		tmpText.DrawLatexNDC(0.94,0.9,title)
		self.canvas.Update()
		return

	def drawShadedRegion(self, curve, color=ROOT.kGray, alpha=0.5, title="title", legendOrder=2):
		self.canvas.cd()
		curve.SetFillStyle(1001)
		curve.SetFillColorAlpha(color,alpha)
		curve.SetLineStyle(1)
		curve.SetLineWidth(1)
		curve.SetLineColorAlpha(ROOT.kGray,0.5)
		curve.Draw("F")
		curve.Draw("L")
		self.canvas.Update()
		if type(legendOrder) == int:
			self.legendObjects.append( ( legendOrder, curve.Clone("ShadedRegion_"+title), title, "F" ) )
		return

	def drawLine(self, coordinates, label = "", color = ROOT.kBlack, style = 7, labelLocation=0 , angle=0):
		self.canvas.cd()
		tmpLine = ROOT.TLine()
		tmpLine.SetLineColorAlpha(color,0.9)
		tmpLine.SetLineStyle(style)
		tmpLine.DrawLine(*coordinates)
		xmin,ymin,xmax,ymax = coordinates

		tmpLineLabel = ROOT.TLatex()
		tmpLineLabel.SetTextSize(0.028)
		tmpLineLabel.SetTextColor(color)
		tmpLineLabel.SetTextAngle(angle)
		if labelLocation:
			tmpLineLabel.DrawLatex(labelLocation[0],labelLocation[1],label)
		else:
			tmpLineLabel.DrawLatex(coordinates[0]+0.1*(coordinates[2]-coordinates[0]),
				coordinates[1]+0.15*(coordinates[3]-coordinates[1]),
				label)

		self.canvas.Update()
		return

	def decorateCanvas(self,size=0.028):
		self.canvas.cd()
		latexObject = ROOT.TLatex()
		latexObject.SetTextSize(size)
		latexObject.DrawLatexNDC(0.2,0.95,self.processLabel)

		latexObject.SetTextSize(0.043)
		latexObject.DrawLatexNDC(0.24, 0.85, self.lumiLabel)
		#ROOT.gPad.RedrawAxis()
		self.canvas.Update()
		return

	def createLegend(self, shape=(0.22,0.55,0.65,0.75) ):
		self.canvas.cd()
		legend=ROOT.TLegend(*shape)
		ROOT.SetOwnership( legend, 0 )
		legend.SetBorderSize(0)
		legend.SetFillStyle(0)
		legend.SetTextFont(42)

		self.legendObjects.sort(key=lambda x: x[0], reverse=False)
		for iItem, (legendOrder,item,title,style) in enumerate(self.legendObjects):
			legend.AddEntry(item,title,style)

		return legend

	def drawTheoryLegendLines(self, xyCoord, length=0.05, ySeparation=0.026, color=ROOT.TColor.GetColor("#800000"), alpha=0.7, style=3 ):
		self.canvas.cd()
		tmpLine = ROOT.TLine()
		tmpLine.SetLineColorAlpha(color,alpha)
		tmpLine.SetLineStyle(style)
		tmpLine.DrawLineNDC(xyCoord[0],xyCoord[1],xyCoord[0]+length,xyCoord[1])
		tmpLine.DrawLineNDC(xyCoord[0],xyCoord[1]+ySeparation,xyCoord[0]+length,xyCoord[1]+ySeparation)

        def drawExtraText(self,text,size=0.031):
                self.canvas.cd()
                latexObject = ROOT.TLatex()
                latexObject.SetTextSize(size)
                latexObject.DrawLatexNDC(0.24,0.7,text)
                self.canvas.Update()
                return

	def writePlot(self, format="pdf"):
		self.canvas.SaveAs(self.plotName+".pdf")
		self.canvas.SaveAs(self.plotName+".png")
		self.canvas.SaveAs(self.plotName+".eps")
		return
