#!/usr/bin/env python2.6                                                                                                                                     
import ROOT, os, re,sys
import math

from math import sqrt, pow
from ROOT import gStyle
from ROOT import gROOT
from ROOT import TStyle
from ROOT import TAttAxis
from array import array
from optparse import OptionParser
ROOT.gROOT.SetBatch()

def red(msg): return "\033[0;31m{0}\033[0m".format(msg);

def main():
   parser = OptionParser()
   parser.add_option("--InDir", help="Directory with CLs stored",    default="../HistFitterUser/")
   parser.add_option("--Grid", help="Grid name: GG2StepWZ,Btt,GSL,Gtt,ComprGtt", default="")
   parser.add_option("--Tag", help="Tag name of HF files", default="FakesYieldsOrig139.00fb_ALLRpc2L1b_Excl_winter2019SameSign_output_hypotest__1_harvest_fix_list_best")
   parser.add_option("--Out", help="Name of the output file", default="best")
   (options, args) = parser.parse_args()

   if not len(options.InDir) or not os.path.exists(options.InDir):
      print red("Please specify an input directory"); sys.exit(1)
   if not len(options.Grid):
      print red("Please specify an input grid name"); sys.exit(1)

   gStyle.SetOptStat(0)
   dirname = options.InDir
   gridname = options.Grid
   tagname = options.Tag
   outname = options.Out

   setAtlasStyle()
   plotBest(dirname,gridname,tagname,outname)

def plotBest(filepath,gridname,tagname,outname):
   f = open(filepath+"Mc16Susy"+gridname+"_nom_"+tagname+".txt","r") 
   
   mx=[]
   my=[]
   x1=[]
   y1=[]
   x2=[]
   y2=[]
   x3=[]
   y3=[]
   x4=[]
   y4=[]
   text1=[] 
   text2=[]
   text3=[]
   text4=[]
   SR = ""
   import axisLabelsProcessDescriptions
   labelsPerGrid = axisLabelsProcessDescriptions.getLabelsPerGrid()
   xLabel="{0}".format(labelsPerGrid["Mc16Susy"+gridname].xLabel) 
   yLabel="{0}".format(labelsPerGrid["Mc16Susy"+gridname].yLabel)
   processDescription="{0}".format(labelsPerGrid["Mc16Susy"+gridname].processDescription)
   forbiddenRegionCut=labelsPerGrid["Mc16Susy"+gridname].forbiddenCut
   forbiddenLabelX=labelsPerGrid["Mc16Susy"+gridname].forbiddenLabelXVal
   forbiddenLabelY=labelsPerGrid["Mc16Susy"+gridname].forbiddenLabelYVal
   forbiddenLabelText="{0}".format(labelsPerGrid["Mc16Susy"+gridname].forbiddenLabelText)

   if "Btt" in gridname:
       model = "SUSY_BTT"
       modelName = "SusyBtt"
    
       print ">>> In Btt model!!!"
    
       nBinsX = 500
       xMin = 600
       xMax = 1000
       nBinsY = 23
       yMin = 50
       yMax = 1000
    
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
    
       yMaxLine=m*950+q
       xMaxLine=950

   print xMin,yMin,xMax,yMax
   c = ROOT.TCanvas('c','Best Exclusion Plot', 800,600)
   c.DrawFrame(xMin,yMin,xMax,yMax)
   gr = ROOT.TGraph()
   gr_SR1 = ROOT.TGraph()
   gr_SR2 = ROOT.TGraph()

   GetValues(f,SR,mx,my,x1,y1,x2,y2,text1,text2,gridname)
   
   gr = ROOT.TGraph(len(mx), array('d', mx), array('d', my))
   gr_SR1 = ROOT.TGraph(len(x1), array('d', x1), array('d', y1))
   gr_SR2 = ROOT.TGraph(len(x2), array('d', x2), array('d', y2))
   obs_line = ROOT.TGraph()
   exp_line = ROOT.TGraph()
   
   r = ROOT.TFile.Open(filepath+"Mc16Susy"+gridname+"_nom_"+tagname+".root","r")
   obs_line = r.Get("Obs_0")
   exp_line = r.Get("Exp_0")
   leg = ROOT.TLegend(0.22,0.62,0.55,0.79)
   
   DrawGraphs(gr,gr_SR1,gr_SR2,obs_line,exp_line,mx,my,x1,y1,x2,y2,gridname,c,xMin,xMax,yMin,yMax)
   DrawLegend(leg,gr_SR1,gr_SR2,obs_line,exp_line,text1,text2,c)

   l=ROOT.TLine()
   DrawDiagonal(gridname,l,c,xMinLine,xMaxLine,yMinLine,yMaxLine,forbiddenLabelX,forbiddenLabelY,forbiddenLabelText,xMinLabel,xMaxLabel,yMinLabel,yMaxLabel,xMin,xMax,yMin,yMax)   
   DrawTitle(gridname,c,processDescription)
   c.SaveAs(filepath+outname+".pdf")
   c.SaveAs(filepath+outname+".png")
   c.SaveAs(filepath+outname+".eps")

def GetValues(f,SR,mx,my,x1,y1,x2,y2,text1,text2,gridname):
   #terrible momentary hack for compressed plot    
   for line in f:
      SR = line.split()[0]
      m0 = float(line.split()[1])
      m12 = float(line.split()[2])
      print SR,"\t",m0,"\t",m12
      if(SR==""):
         continue
      #print SR,"\t",m0,"\t",m12
      mx.append(m0)
      my.append(m12)
      if 'Rpc2L1b' in SR:
         x1.append(m0)
         y1.append(m12)
         text1.append(SR)
         continue
      if 'Rpc2L2b' in SR:
         x2.append(m0)
         y2.append(m12)
         text2.append(SR)
   print 'x1: ',len(x1)
   print 'x2: ',len(x2)

   print "Finished..."
   return

def GetxTitle(gridname):
   if 'Btt' in gridname:
      xTitle = "m_{#tilde{b}} [GeV]"
   else:
      xTitle = "m_{#tilde{g}} [GeV]"
   return xTitle

def GetyTitle(gridname):
   if 'ComprGtt' in gridname:
      yTitle = "#Deltam_{#tilde{#chi}^{0}_{1}} = m_{#tilde{#chi}^{0}_{1}} - (m_{#tilde{g}} - 2*m_t) [GeV]"
   else:
      yTitle = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
   return yTitle

def DrawGraphs(gr,gr_SR1,gr_SR2,obs_line,exp_line,mx,my,x1,y1,x2,y2,gridname,c,xMin,xMax,yMin,yMax):
   c.cd()
   #ci = ROOT.TColor.GetColor("#28373c")
   #obs_line.SetLineColor(ci)
   ci = ROOT.TColor.GetColor("#aa000");
   obs_line.SetLineColor(ci)
   obs_line.SetLineStyle(1)
   obs_line.SetLineWidth(2)
   
   ce = ROOT.TColor.GetColor("#28373c");
   exp_line.SetLineColor(ce)
   exp_line.SetLineStyle(7)
   exp_line.SetLineWidth(2)
   
   xTitle = GetxTitle(gridname)
   yTitle = GetyTitle(gridname)
   gr.GetXaxis().SetTitle(xTitle)
   gr.GetYaxis().SetTitle(yTitle)
   gr.GetXaxis().SetTitleFont(42)
   gr.GetYaxis().SetTitleFont(42)
   gr.GetXaxis().SetTitleSize(0.035)
   gr.GetYaxis().SetTitleSize(0.035)
   gr.GetXaxis().SetLabelFont(42)
   gr.GetYaxis().SetLabelFont(42)
   gr.GetXaxis().SetLabelSize(0.035)
   gr.GetYaxis().SetLabelSize(0.035)
   gr.SetLineColor(0)
   gr.SetMarkerColor(0)
   gr.GetXaxis().SetRangeUser(xMin,xMax)
   gr.GetYaxis().SetRangeUser(yMin,yMax)

   gr_SR1.SetMarkerColor(632)
   #if 'ComprGtt' in gridname:
   #   gr_SR1.SetMarkerColor(416)
   gr_SR1.SetMarkerStyle(34)

   gr_SR2.SetMarkerColor(600)
   #if 'ComprGtt' in gridname:
   #   gr_SR2.SetMarkerColor(616)
   gr_SR2.SetMarkerStyle(34)
   c.DrawFrame(xMin,yMin,xMax,yMax)
   c.Update()
   gr.Draw("apl same")
   gr_SR1.Draw("p same")
   obs_line.Draw("same")
   exp_line.Draw("same")
   gr_SR2.Draw("p same")


   
   return


def DrawLegend(leg,gr_SR1,gr_SR2,obs_line,exp_line,text1,text2,c):
   c.cd()
   leg.SetBorderSize(0)
   leg.SetTextFont(42)
   leg.SetTextSize(0.03)
   leg.SetFillColor(0)
   leg.SetFillStyle(0)
   leg.SetLineColor(0)

   leg.AddEntry(gr_SR1,text1[0],"P")
   leg.AddEntry(gr_SR2,text2[0],"P")
   leg.AddEntry(obs_line,"Observed exclusion","l")
   leg.AddEntry(exp_line,"Expected exclusion","l")
   leg.Draw("same")
   c.Update()

   return

def DrawDiagonal(gridname,l,c,xMinLine,xMaxLine,yMinLine,yMaxLine,forbiddenLabelX,forbiddenLabelY,forbiddenLabelText,xMinLabel,xMaxLabel,yMinLabel,yMaxLabel,xMin,xMax,yMin,yMax):
   c.cd()
   diag_text = ROOT.TLatex()
   diag_text.SetTextSize(0.03)
   diag_text.SetTextColor(921)
   l.SetLineColor(921)
   l.SetLineStyle(3)
   l.SetLineWidth(2)

   angle=math.degrees(math.atan2(((yMaxLabel-yMinLabel))/((yMax-yMin)/(600.0-600.0*0.17)),((xMaxLabel-xMinLabel))/((xMax-xMin)/(800.0-800.0*(0.2+0.07)))))
   diag_text.SetTextAngle(angle)
   diag_text.DrawLatex(forbiddenLabelX,forbiddenLabelY,forbiddenLabelText)

   l.SetX1(xMinLine)
   l.SetY1(yMinLine)
   l.SetX2(xMaxLine)
   l.SetY2(yMaxLine)
   l.Draw("same")
   c.Update()

   return 

def DrawTitle(gridname,c,processDescription):
   c.cd()
   title = ROOT.TLatex()
   title.SetTextSize(0.028)
   title.SetTextColor(1)

   title.DrawLatexNDC(0.2,0.97,processDescription)
   title.SetTextSize(0.037)
   title.DrawLatexNDC(0.24, 0.85, "#splitline{#it{#bf{ATLAS}} Internal}{#sqrt{s}=13 TeV, 139 fb^{-1}, All limits at 95% CL}")
   c.Update()
   return

def setAtlasStyle():
   AtlasStyle = "./"
   if not os.path.exists(AtlasStyle):
      print red("{0} not found. Please set path for AtlasStyle".format(AtlasStyle)); return

   ROOT.gROOT.LoadMacro(AtlasStyle+"AtlasStyle.C")
   ROOT.gROOT.ProcessLine("SetAtlasStyle()")

if __name__ == "__main__":
    main()
