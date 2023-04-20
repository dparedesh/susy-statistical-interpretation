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
   f = open(filepath+"Mc15Susy"+gridname+"_"+tagname+"_best_SR_perpoint.txt","r") 
   
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
    
   c = ROOT.TCanvas('c','Best Exclusion Plot', 0, 0, 650,640)
   gr = ROOT.TGraph()
   gr_SR1 = ROOT.TGraph()
   gr_SR2 = ROOT.TGraph()

   GetValues(f,SR,mx,my,x1,y1,x2,y2,x3,y3,x4,y4,text1,text2,text3,text4,gridname)
   
   gr = ROOT.TGraph(len(mx), array('d', mx), array('d', my))
   gr_SR1 = ROOT.TGraph(len(x1), array('d', x1), array('d', y1))
   gr_SR2 = ROOT.TGraph(len(x2), array('d', x2), array('d', y2))
   if "Gtt" in gridname:
      gr_SR3 = ROOT.TGraph(len(x3), array('d', x3), array('d', y3))
      gr_SR4 = ROOT.TGraph(len(x4), array('d', x4), array('d', y4))

   obs_line = ROOT.TGraph()
   exp_line = ROOT.TGraph()
   
   tag=tagname.split("_")[0]
   r = ROOT.TFile.Open(filepath+"Susy"+gridname+"_observed_exclusion_line_"+tag+".root","r")
   obs_line = r.Get("obs_exclusion_line")
   exp_line = r.Get("exp_exclusion_line")
   
   if "Gtt" in gridname:
      DrawGraphsGtt(gr,gr_SR1,gr_SR2,gr_SR3,gr_SR4,obs_line,exp_line,mx,my,x1,y1,x2,y2,x3,y3,x4,y4,gridname,c)
   else:
      DrawGraphs(gr,gr_SR1,gr_SR2,obs_line,exp_line,mx,my,x1,y1,x2,y2,gridname,c)
   if 'Compr' in gridname:
      leg = ROOT.TLegend(0.67, 0.3, 0.77, 0.5)
   else:
      leg = ROOT.TLegend(0.20, 0.9, 0.40, 0.75)
   if "Gtt" in gridname:
      DrawLegendGtt(leg,gr_SR1,gr_SR2,gr_SR3,gr_SR4,obs_line,exp_line,text1,text2,text3,text4,c)
   else:
      DrawLegend(leg,gr_SR1,gr_SR2,obs_line,exp_line,text1,text2,c)

   l=ROOT.TLine()
   DrawDiagonal(gridname,l,c)   
   DrawTitle(gridname,c)
   c.SaveAs(filepath+outname+".pdf")

def GetValues(f,SR,mx,my,x1,y1,x2,y2,x3,y3,x4,y4,text1,text2,text3,text4,gridname):
   #terrible momentary hack for compressed plot
   if 'ComprGtt'==gridname:
         x2.append(800)
         y2.append(5)
         text2.append("Rpc2L2bH")
         
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
      if 'bS' in SR:
         x1.append(m0)
         y1.append(m12)
         text1.append(SR)
         continue
      if 'bH' in SR:
         x2.append(m0)
         y2.append(m12)
         text2.append(SR)
      #if 'soft1b' in SR and not "Gtt"==gridname:
      #   x1.append(m0)
      #   y1.append(m12)
      #   text1.append(SR)
      #   continue
      if 'soft1b' in SR:
         x3.append(m0)
         y3.append(m12)
         text3.append(SR)
         continue
      #if 'soft2b' in SR and not "Gtt"==gridname:
      #   x2.append(m0)
      #   y2.append(m12)
      #   text2.append(SR)
      #   continue
      if 'soft2b' in SR:
         x4.append(m0)
         y4.append(m12)
         text4.append(SR)
         continue
   print 'x1: ',len(x1)
   print 'x2: ',len(x2)
   print 'x3: ',len(x3)
   print 'x4: ',len(x4)

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

def DrawGraphs(gr,gr_SR1,gr_SR2,obs_line,exp_line,mx,my,x1,y1,x2,y2,gridname,c):
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
   gr.Draw("apl")

   gr_SR1.SetMarkerColor(632)
   #if 'ComprGtt' in gridname:
   #   gr_SR1.SetMarkerColor(416)
   gr_SR1.SetMarkerStyle(34)
   gr_SR1.Draw("p same")
   obs_line.Draw("same")
   exp_line.Draw("same")

   gr_SR2.SetMarkerColor(600)
   #if 'ComprGtt' in gridname:
   #   gr_SR2.SetMarkerColor(616)
   gr_SR2.SetMarkerStyle(34)
   gr_SR2.Draw("p same")
   
   return

def DrawGraphsGtt(gr,gr_SR1,gr_SR2,gr_SR3,gr_SR4,obs_line,exp_line,mx,my,x1,y1,x2,y2,x3,y3,x4,y4,gridname,c):
   c.cd()
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
   gr.Draw("apl")

   gr_SR1.SetMarkerColor(632)
   gr_SR1.SetMarkerStyle(34)
   gr_SR1.Draw("p same")
   obs_line.Draw("same")
   exp_line.Draw("same")

   gr_SR2.SetMarkerColor(600)
   gr_SR2.SetMarkerStyle(34)
   gr_SR2.Draw("p same")

   gr_SR3.SetMarkerColor(418)
   gr_SR3.SetMarkerStyle(34)
   gr_SR3.Draw("p same")

   gr_SR4.SetMarkerColor(618)
   gr_SR4.SetMarkerStyle(34)
   gr_SR4.Draw("p same")

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

   return

def DrawLegendGtt(leg,gr_SR1,gr_SR2,gr_SR3,gr_SR4,obs_line,exp_line,text1,text2,text3,text4,c):
   c.cd()
   leg.SetBorderSize(0)
   leg.SetTextFont(42)
   leg.SetTextSize(0.03)
   leg.SetFillColor(0)
   leg.SetFillStyle(0)
   leg.SetLineColor(0)

   leg.AddEntry(gr_SR1,text1[0],"P")
   leg.AddEntry(gr_SR2,text2[0],"P")
   leg.AddEntry(gr_SR3,text3[0],"P")
   leg.AddEntry(gr_SR4,text4[0],"P")
   leg.AddEntry(obs_line,"Observed exclusion","l")
   leg.AddEntry(exp_line,"Expected exclusion","l")
   leg.Draw("same")

   return

def DrawDiagonal(gridname,l,c):
   c.cd()
   diag_text = ROOT.TLatex()
   diag_text.SetTextSize(0.03)
   diag_text.SetTextColor(921)
   l.SetLineColor(921)
   l.SetLineStyle(3)
   l.SetLineWidth(2)

   if '2Step' in gridname:
      diag_text.SetTextAngle(45.)
      diag_text.DrawLatex(700,700,"m_{#tilde{g}} <  m_{W} + m_{Z} + m_{#tilde{#chi}^{0}_{1}}")
      l.SetX1(500)
      l.SetY1(330)
      l.SetX2(1400)
      l.SetY2(1230)
      l.Draw("same")
   if 'Btt' in gridname:
      diag_text.SetTextAngle(44.)
      diag_text.DrawLatex(500,260,"m_{#tilde{b}} <  m_{t} + m_{#tilde{#chi}^{0}_{1}} + 100 GeV");
      l.SetX1(350)
      l.SetY1(74.5)
      l.SetX2(900)
      l.SetY2(624.5)
      l.Draw("same")
   if 'GSL' in gridname:
      diag_text.SetTextAngle(41.)
      diag_text.DrawLatex(400,500,"m_{#tilde{g}} <  m_{#tilde{#chi}^{0}_{1}}")
      l.SetX1(400)
      l.SetY1(400)
      l.SetX2(1600)
      l.SetY2(1600)
      l.Draw("same")
   if 'Gtt'==gridname:
      diag_text.SetTextAngle(45.)
      diag_text.DrawLatex(800,680,"m_{#tilde{g}} <  2 m_{W} + m_{#tilde{#chi}^{0}_{1}}")
      l.SetX1(600)
      l.SetY1(440)
      l.SetX2(2300)
      l.SetY2(2140)
      l.Draw("same")
   if 'ComprGtt'==gridname:
      #diag_text.SetTextAngle(45.)
      #diag_text.DrawLatex(620,30,"m_{#tilde{g}} <  2 m_{t} + m_{#tilde{#chi}^{0}_{1}}")
      l.SetX1(600)
      l.SetY1(25)
      l.SetX2(1900)
      l.SetY2(25)
      #l.Draw("same")
   return 

def DrawTitle(gridname,c):
   c.cd()
   title = ROOT.TLatex()
   title.SetTextSize(0.03)
   title.SetTextColor(1)

   if '2Step' in gridname:
      title.SetTextSize(0.02)
      title.DrawLatex(500,1340,"#tilde{g} #tilde{g} production, #tilde{g} #rightarrow qqWZ#tilde{#chi}^{0}_{1} m(#tilde{#chi}^{#pm}_{1}) = (m(#tilde{g}) + m(#tilde{#chi}^{0}_{1}))/2, m(#tilde{#chi}^{0}_{2}) = (m(#tilde{#chi}^{#pm}_{1}) + m(#tilde{#chi}^{0}_{1}))/2")
   if 'Btt' in gridname:
      title.DrawLatex(300,695,"#tilde{b_{1}} #tilde{b}_{1} production, #tilde{b}_{1}#rightarrow t#tilde{#chi}^{#pm}_{1}, m(#tilde{#chi}^{#pm}_{1}) = m(#tilde{#chi}^{0}_{1}) + 100 GeV")
   if 'GSL' in gridname:
      title.SetTextSize(0.03)
      title.DrawLatex(250,1660,"#tilde{g} #tilde{g} production, #tilde{g} #rightarrow qq(ll/#nu#nu)#tilde{#chi}^{0}_{1}; m(#tilde{#chi}^{0}_{2}) = (m(#tilde{g}) + m(#tilde{#chi}^{0}_{1}))/2, m(#tilde{l},#tilde{#nu}) = (m(#tilde{#chi}^{0}_{2}) + m(#tilde{#chi}^{0}_{1}))/2")
   if 'ComprGtt' in gridname:
      title.DrawLatex(620,155,"#tilde{g} #tilde{g} production, #tilde{g}#rightarrow t#bar{t}#tilde{#chi}^{0}_{1}")
   if 'Gtt' in gridname:
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
