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

def red(msg): return "\033[0;31m{0}\033[0m".format(msg);

def main():
   parser = OptionParser()
   parser.add_option("--InDir", help="Directory with yields tables",    default="")
   parser.add_option("--Grid", help="Grid name: GG2StepWZ,Btt,GSL,Gtt,ComprGtt", default="")
   parser.add_option("--Tag", help="Tag name of HF files", default="")
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
   f = open(filepath+"Mc15Susy"+gridname+"_nom_"+tagname+"_Combined_UL_winter2016SameSign_output_upperlimit.txt","r") 
   
   mx=[]
   my=[]
   x1=[]
   y1=[]
   x2=[]
   y2=[]
   text1=[] 
   text2=[]
   SR = ""
    
   c = ROOT.TCanvas('c','Best Exclusion Plot', 0, 0, 650,640)
   gr = ROOT.TGraph()
   gr_SR1 = ROOT.TGraph()
   gr_SR2 = ROOT.TGraph()

   GetValues(f,SR,mx,my,x1,y1,x2,y2,text1,text2,gridname)
   
   gr = ROOT.TGraph(len(mx), array('d', mx), array('d', my))
   gr_SR1 = ROOT.TGraph(len(x1), array('d', x1), array('d', y1))
   gr_SR2 = ROOT.TGraph(len(x2), array('d', x2), array('d', y2))

   obs_line = ROOT.TGraph()
   exp_line = ROOT.TGraph()
   
   tag=tagname.split("_")[0]
      
   DrawGraphs(gr,gr_SR1,gr_SR2,mx,my,x1,y1,x2,y2,gridname,c)
   leg = ROOT.TLegend(0.20, 0.9, 0.40, 0.75)
   DrawLegend(leg,gr_SR1,gr_SR2,text1,text2,c)

   l=ROOT.TLine()
   DrawTitle(gridname,c)
   c.SaveAs(filepath+outname+".pdf")

def GetValues(f,SR,mx,my,x1,y1,x2,y2,text1,text2,gridname):
   for line in f:
      SR = line.split()[0]
      m0 = float(line.split()[1])
      print SR,"\t",m0
      if(SR==""):
         continue
      #print SR,"\t",m0,"\t",m12
      mx.append(m0)
      my.append(2000)
      if 'bS' in SR:
         x1.append(m0)
         y1.append(2000)
         text1.append(SR)
         continue
      if 'bM' in SR:
         x2.append(m0)
         y2.append(2000)
         text2.append(SR)
         continue
   print "Finished..."
   return

def GetxTitle(gridname):
   xTitle = "m_{#tilde{d}_{R}} [GeV]"
   return xTitle

def GetyTitle(gridname):
   yTitle = "m_{#tilde{g}} [GeV]"
   return yTitle

def DrawGraphs(gr,gr_SR1,gr_SR2,mx,my,x1,y1,x2,y2,gridname,c):
   c.cd()

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
   gr.Draw("apl")
   gr.GetYaxis().SetRangeUser(1999.9,2000.2)

   gr_SR1.SetMarkerColor(632)
   gr_SR1.SetMarkerStyle(34)
   gr_SR1.Draw("p same")
   
   gr_SR2.SetMarkerColor(600)
   gr_SR2.SetMarkerStyle(34)
   gr_SR2.Draw("p same")
   
   return

def DrawLegend(leg,gr_SR1,gr_SR2,text1,text2,c):
   c.cd()
   leg.SetBorderSize(0)
   leg.SetTextFont(42)
   leg.SetTextSize(0.03)
   leg.SetFillColor(0)
   leg.SetFillStyle(0)
   leg.SetLineColor(0)

   leg.AddEntry(gr_SR1,text1[0],"P")
   leg.AddEntry(gr_SR2,text2[0],"P")
   leg.Draw("same")

   return

def DrawTitle(gridname,c):
   c.cd()
   title = ROOT.TLatex()
   title.SetTextSize(0.03)
   title.SetTextColor(1)
   title.DrawLatex(600,2220,"#tilde{g} #tilde{g} production, #tilde{g}#rightarrow t#bar{t}#tilde{#chi}^{0}_{1}")
   return

def setAtlasStyle():
   AtlasStyle = "/home/pt1009/Atlas/atlasstyle-00-03-04/"
   if not os.path.exists(AtlasStyle):
      print red("{0} not found. Please set path for AtlasStyle".format(AtlasStyle)); return

   ROOT.gROOT.LoadMacro(AtlasStyle+"AtlasStyle.C")
   ROOT.gROOT.ProcessLine("SetAtlasStyle()")

if __name__ == "__main__":
    main()
