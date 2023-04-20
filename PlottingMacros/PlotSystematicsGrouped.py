#!/usr/bin/env python2.6
#
#####______HOW TO USE_________________________________ 
#
#__________Before running_____________________________
#
#..You have to specify the following variables.
#
#..1) 'lumi': value to be printed at the plot.
#..2) 'SR_name': signal regions as provided to HistFitter and to the script plotSR.py (they must be exactly the same!). 
#..3) 'Datadriven': a list containing the name of the datadriven backgrounds as were provided to HistFitter and to the script plotSR.py (they must be exactly the same!)
#..4) 'splitStatistical' if would like to split the statitiscal uncertaintines in MC and data-driven components
#
#The names of the folllowing variables, in a) and b), must be changed *IF AND ONLY IF*  you did the same in fitConfigSS3L.py file for (a) and plotSR.py (b): 
#
#..a) data_driven_syst_string','theory_syst_string', 'gamma_stat_string', and 'detector_syst_string' 
#  (You have to be sure that all the systematics to take into account are in those strings in the proper category.
#  If a systematic is not included in any category, then a warning message will be printed). 
#
#..b) 'MCStats':  Full path and name of the *.json file generated when running the script plotSR.py using "SRYields" was generated. The default name is 'AsymmetricUnc.json'. Change this one if and only if you did the same in the corresponding script.
#
#__________For running________________________________
#
#..1) You must specify the input directory --InDir indicating the directory where the grouped systematic 
#  files (produced with the HF patch) are located.
#
# use: python PlotSystematicsGrouped.py  --InDir <Path to files>
#
#__________After running______________________________
#..1) Check if warning messages about missing systematics are printed. The red warning from 'syserr_Lumi' is expected. 
#..2) Check the printed list of grouped systematic for each channel: check that the systematics added correspond to the
#  proper category.

import ROOT, os, re, sys, time
import math
import json

from math import sqrt, pow
from ROOT import gStyle
from ROOT import gROOT
from ROOT import TStyle
from array import array
from optparse import OptionParser


#___________Specify before running_______#
lumi = 139

SR_name=['Rpc2L0b',
         'Rpc2L1b',
         'Rpc2L2b',
         'Rpc3LSS1b',
         'Rpv2L']

Datadriven=["Fakes","MisCharge"]
splitStatistical=True
drawLines=False

# the lines below must *not* be changed at least that you change the strings in the fitConfigSS3L.py file
data_driven_syst_string = [ 'syst_'+ sam for sam in Datadriven]
MCStats="AsymmetricUnc.json"
theory_syst_string=['theoryUncert']
gamma_stat_string=['gamma_stat']
detector_syst_string=['_JET_','TRIG','_FT_','pileup','_el','_EG','_Mu','_MET','_mu','CHFLIP']
#__________________________________________#



#_________ Function definitions____________#
def drawSplitLines(n):

    all=[]
    for counter in range(1,nSR):
        line=ROOT.TLine(float(counter),0,float(counter),0.58)
        line.SetLineWidth(3)
        line.SetLineColor(0)
        line.Draw("same")
        all.append(line)

    lines=[]
    for counter in range(1,nSR):
        line2=ROOT.TLine(float(counter),0,float(counter),0.58)
        line2.SetLineWidth(1)
        line2.SetLineColor(921)
        line2.SetLineStyle(3)
        line2.Draw("same")
        lines.append(line2)

def getLegend():

    Legend = ROOT.TLegend(0.32,0.72,0.86,0.86)
    Legend.SetNColumns(2)
    Legend.SetFillColor(0)
    Legend.SetFillStyle(0)
    Legend.SetLineColor(ROOT.kWhite)
    Legend.SetTextSize( 0.038 )
    Legend.SetTextFont( 42 )

    return Legend

def setATLASLabels():

    atlasLabel = ROOT.TLatex()
    atlasLabel.SetNDC()
    atlasLabel.SetTextFont(72)
    atlasLabel.SetTextColor(ROOT.kBlack)
    atlasLabel.SetTextSize( 0.06 )
    atlasLabel.DrawLatex(0.13, 0.81,"ATLAS")
    atlasLabel.Draw("same")

    tex = ROOT.TLatex(0.21,0.81,"Preliminary")
    tex.SetNDC()
    tex.SetTextFont(42)
    tex.SetTextColor(ROOT.kBlack)
    tex.SetTextSize(0.06)
    tex.SetLineWidth(2)
    tex.Draw("same")

    lumiLabel = ROOT.TLatex()
    lumiLabel.SetNDC()
    lumiLabel.SetTextFont(42)
    lumiLabel.SetTextColor(ROOT.kBlack)
    lumiLabel.SetTextSize( 0.05 )
    lumiLabel.DrawLatex(0.13, 0.74,"#sqrt{s} = 13 TeV, %s fb^{-1}" % (lumi))
    lumiLabel.Draw("same")

    return

def setStyle(h,color,width,style):

    h.SetLineColor(color)
    h.SetLineWidth(width)
    h.SetLineStyle(style)

    return

def setBaseStyle(h,SR_name):

    y_min = 0.0; y_max = 0.6;

    h.GetYaxis().SetTitle('Relative uncertainty')
    h.GetYaxis().SetRangeUser(y_min,y_max)

    for i in range(len(SR_name)):
        h.GetXaxis().SetBinLabel(i+1,SR_name[i])

    h.GetXaxis().SetLabelSize(0.06)
    h.GetXaxis().SetLabelOffset(0.008)
    h.GetYaxis().SetLabelSize(0.04)
    h.GetYaxis().SetTitleSize(0.06)
    h.GetYaxis().SetTitleOffset(0.5)

    return

def fillHisto(name,n,binContent,color,width,style):
    h = ROOT.TH1F(name,"",n,0,n)

    for i in range(n):
        h.SetBinContent(i+1,binContent[i])

    setStyle(h,color,width,style)

    return h

def getStatistical(FileAsymmetricUnc,dataDriven,SR_list,yields):

    if not os.path.exists(FileAsymmetricUnc):
        print red("{0} not found. Returning original error".format(FileAsymmetricUnc)); return error

    AsymmetricUnc = {}

    with open(FileAsymmetricUnc) as json_file:
        AsymmetricUnc = json.load(json_file)


    stat_dd={}
    stat_mc={}    
    stat={}
    total = {}

    for SR in SR_list:
        print "- Reading SR: ",SR

        statSR2 = 0

        for bkg in dataDriven:
            print "Found statistical for : ",bkg, " -> stat : ",AsymmetricUnc[SR][bkg]['stat']

            statSR2 += AsymmetricUnc[SR][bkg]['stat']**2   

        stat_dd[SR] = sqrt(statSR2)

        stat_mc[SR]=sqrt( AsymmetricUnc[SR]['Total']['stat']**2 - statSR2 )
        stat[SR] = AsymmetricUnc[SR]['Total']['stat']
        total[SR] = AsymmetricUnc[SR]['Total']['sym']


    print ("Total statistical:")
    print stat

    print ("Total data-driven statistical: ")
    print stat_dd

    print ("Total MC statistical (it must match perfecty the one shown in the plot!!!)")
    print stat_mc

    print ("Total stat + syst: ")
    print total

    return stat,stat_dd,stat_mc,total


def GetRelative(num,den,SR_name):

    return [num[SR_name[i]]/den[SR_name[i]] for i in range(len(SR_name))]


def CheckSystGroup(dict_syst):

    for key,val in dict_syst.items():
        print("----------")
        print('Systematics included in category: '+key)

        for i in val: print i

    return

def bold(msg): return "\033[1m{0}\033[0m".format(msg);
def red(msg): return "\033[0;31m{0}\033[0m".format(msg);
#_____________ End of function definitions____________




######################################################
#___________________ Main code _______________________

parser = OptionParser()
parser.add_option("--InDir", help="Directory with the grouped systematic files generated with the HF patch",    default="")
(options, args) = parser.parse_args()

if not len(options.InDir) or not os.path.exists(options.InDir):
   print red("Please specify an input directory"); sys.exit(1)

gStyle.SetOptStat(0)
dirname = options.InDir

syst_name_list=['Data-driven','Experimental','Theory','Statistical']


TOT_syst = []
datadriven_syst=[]; theory_syst=[]; stat_unc=[]; detector_syst=[];

yields={}

for ch in SR_name:

   dict_syst_grouped={} 

   for i in syst_name_list: dict_syst_grouped[i]=[]

   print bold('*************  Looking at '+ch)
   f = open(dirname+ch+'_systematic_grouped.txt',"r")
   nfitted=0
   detector_syst.append(0)
   datadriven_syst.append(0)
   stat_unc.append(0)
   theory_syst.append(0)

   for line in f:
      syst_name = line.split()[0]
      syst_value = float(line.split()[1])

      if  syst_name=='nfitted':

         nfitted=syst_value
         yields[ch]=nfitted

      elif'totsyserr' in syst_name:

         TOT_syst.append(syst_value/nfitted)

      elif any([name in syst_name for name in data_driven_syst_string]):

         datadriven_syst[-1]=sqrt(datadriven_syst[-1]*datadriven_syst[-1]+syst_value*syst_value)
         dict_syst_grouped['Data-driven'].append(syst_name)

      elif any([name in syst_name for name in theory_syst_string]):

         theory_syst[-1]=sqrt(theory_syst[-1]*theory_syst[-1]+syst_value*syst_value)
         dict_syst_grouped['Theory'].append(syst_name)

      elif any([name in syst_name for name in detector_syst_string]):

         detector_syst[-1]=sqrt(detector_syst[-1]*detector_syst[-1]+syst_value*syst_value)
         dict_syst_grouped['Experimental'].append(syst_name)

      elif any([name in syst_name for name in gamma_stat_string]):

         stat_unc[-1]=(syst_value)
         dict_syst_grouped['Statistical'].append(syst_name)

      else:

          if ('sqrtnfitted' not in syst_name) and ('sqrtnobsa' not in syst_name):
              print red('WARNING: systematic not found in current setup --> '+syst_name)


   detector_syst[-1]=detector_syst[-1]/nfitted
   theory_syst[-1]=theory_syst[-1]/nfitted
   datadriven_syst[-1]=datadriven_syst[-1]/nfitted

   print bold('Systematics for: '+ch)
   print bold('Total Systematic: '+str(TOT_syst[-1]))

   #print systematic included for each category
   CheckSystGroup(dict_syst_grouped)

   
nSR=len(TOT_syst)

print('Total nSR  added to TOT_syst:'+str(nSR))
print("Yields: ")
print yields



###############################################

total_stat, stat_dd, stat_mc, total_bkg = getStatistical(MCStats,Datadriven,SR_name,yields)

total_stat_t=GetRelative(total_stat,yields,SR_name)
stat_dd_t = GetRelative(stat_dd,yields,SR_name)
stat_mc_t =GetRelative(stat_mc,yields,SR_name)

TOT_syst_t = [ sqrt(a**2+b**2) for a,b in zip(TOT_syst,total_stat_t)  ]


TOT_histo = fillHisto("histo_TOTsyst",nSR,TOT_syst_t,1,2,1)
TOT_histo.SetFillColor(590)
setBaseStyle(TOT_histo,SR_name)

hCLONE = TOT_histo.Clone("histo_Clone")
setBaseStyle(hCLONE,SR_name)
setStyle(hCLONE,0,1,1)


hSTAT = fillHisto("histo_STAT",nSR,total_stat_t,632,1,2)
hSTAT_MC = fillHisto("histo_STAT_MC",nSR,stat_mc_t,632,2,1)
hSTAT_DD = fillHisto("histo_STAT_DD",nSR,stat_dd_t,632,2,8)
hDETECTOR = fillHisto("histo_DETECTOR",nSR,detector_syst,600,2,2)
hTHEORY =   fillHisto("histo_THEORY",nSR,theory_syst,880,2,3)
hDATADRIVEN= fillHisto("histo_DATADRIVEN",nSR,datadriven_syst,417,2,4)


###############################################

setLogy = False
setGrid = False
c_SYST = ROOT.TCanvas('c_SYST','SYST Systematics', 1, 10, 1150, 480)
if setLogy: c_SYST.SetLogy()
if setGrid: c_SYST.SetGridx()
c_SYST.SetTicks()

hCLONE.Draw()

TOT_histo.Draw("same")

hDETECTOR.Draw("same")
hTHEORY.Draw("same")
hDATADRIVEN.Draw("same")

if splitStatistical:
    hSTAT_MC.Draw("same")
    hSTAT_DD.Draw("same")
else: hSTAT.Draw("same")


#TOT_histo.Draw("same")

if drawLines: drawSplitLines(nSR)

setATLASLabels()
Legend = getLegend()


Legend.AddEntry(TOT_histo,'Total unc.','f')
Legend.AddEntry(hTHEORY,'Theoretical unc.','l')
if splitStatistical:
    Legend.AddEntry(hSTAT_MC,'MC statistical unc.','l')
    Legend.AddEntry(hSTAT_DD,'Fakes/non-prompt, Charge-flip statistical unc.')

else: Legend.AddEntry(hSTAT,'Statistical unc.','l')
Legend.AddEntry(hDETECTOR,'Experimental unc.','l')
Legend.AddEntry(hDATADRIVEN,'Fakes/non-prompt, Charge-flip systematic unc.','l')

Legend.Draw("same")

ROOT.gPad.SetTicks()
ROOT.gPad.RedrawAxis()

time.sleep(2)
c_SYST.SaveAs('SystematicsSummary.C')
c_SYST.SaveAs('SystematicsSummary.pdf')
c_SYST.SaveAs('SystematicsSummary.eps')
c_SYST.SaveAs('SystematicsSummary.png')


