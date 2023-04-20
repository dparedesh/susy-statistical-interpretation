#!/usr/bin/env python2.6
import ROOT, os, re
import math
import sys
from math import sqrt, pow
from ROOT import gStyle
from ROOT import gROOT
from ROOT import TStyle
from array import array
from optparse import OptionParser
# ROOT.gSystem.Load("libSusyFitter.so")

import pathUtilities
import signalSameSignTools
signalRunnumberToMassesDict = signalSameSignTools.getRunnumbersMassesDictSSAllGrids()
ROOT.gROOT.SetBatch()

debug = 0

def main():
    parser = OptionParser()
    parser.add_option('',"--FileName", dest='FileName', help="File with yields tables", default="")
    parser.add_option('',"--DirName", dest='DirName', help="Directory", default="/storage/users/pt1009/SS_HistFitter/run2/macroSS/1DPlot/")
    parser.add_option('',"--OutputName", dest='OutputName', help="OutputName", default="UpperCrossSections_Test")
    parser.add_option('',"--takeBest", dest='takeBest', help="Take best exclusion (True/False)", default="False")
    (options, args) = parser.parse_args()

    dirname = options.DirName 
    takeBest = options.takeBest

    fout_Exp = open(options.DirName+options.OutputName+"_Exp_Limit.txt", "w+")
    fout_Obs = open(options.DirName+options.OutputName+"_Obs_Limit.txt", "w+")
    
    if not len(options.FileName):
        print red("Please specify an input filename"); sys.exit(1)

    if not os.path.exists(dirname+options.FileName):
        print red("Input file doesn't exist: "); 
        print dirname+options.FileName;
        sys.exit(1)

    c_LightYellow   = ROOT.TColor.GetColor( "#ffe938" )
    c_myExp      = ROOT.TColor.GetColor("#28373c")
    c_LightRed   = ROOT.TColor.GetColor( "#aa000" )
    c_white=ROOT.TColor.GetColor( "#FFFFFF" )

#    setAtlasStyle()

    gStyle.SetPalette(1)
    gStyle.SetPaintTextFormat("0.3g")
    gStyle.SetOptStat(0)

    print 'Directory: ',dirname
    filename = options.FileName

    #if takeBest:
    #    filename = makeBest(filename,dirname)

    sigX=GetXsec(filename)
    sigXu=GetThUnc(filename)
    sigXd=GetThUnc(filename)
    kFac=GetKfac(filename)
    fEff=GetFeff(filename)

    print sigX

    preobs=[]
    exp=[]
    obs=[]
    expd=[]
    expu=[]
    exp2d=[]
    exp2u=[]
    cross=[]
    crossplus=[]
    crossminus=[]
    xMass =[]
    prexMass =[]
    signal_list=[]

    print 'using',filename
    _file = ROOT.TFile.Open(dirname+filename)

    for key in _file.GetListOfKeys():
        kname = key.GetName()
        if "ProcessID" in kname:
            continue
        if debug : print kname
        signal_list.append(kname)

    signal_list.sort()

    for s in signal_list:
        my_result=_file.Get(s)
        signalID=my_result.GetName()                
        print "signalID", signalID

        if "debug" in signalID : continue # when HF fails the fit
        
        grid = filename.split("_")[0]
        if "Rpv" in filename:
            grid = grid+"_"+filename.split("_")[1]
        print "signalID ",signalID," in grid ",grid
        mass = GetMass(signalID,grid)
        
        # check here if signal name is correct and one gets limits
        if debug : 
            print "The computed upper limit for signal named ", mass, "with correspinding gluino mass", mass, " is: ", my_result.UpperLimit()
            print "expected Upper limit ", my_result.GetExpectedUpperLimit(0.)
            print "expected Upper limit -1 sigma ", my_result.GetExpectedUpperLimit(-1.)
            print "expected Upper limit +1 sigma ", my_result.GetExpectedUpperLimit(1.)
            print "expected Upper limit -2 sigma ", my_result.GetExpectedUpperLimit(-2.)
            print "expected Upper limit +2 sigma ", my_result.GetExpectedUpperLimit(2.)       
            print "cross section for this signal is ", sigX[mass]*kFac[mass]*fEff[mass], "with uncertanity ", sigXu[mass]
        import string
        if string.atof(mass) < 800.0:
            print GetPreObs(grid,mass), sigX[mass] 
            preobs.append((GetPreObs(grid,mass)/1000.0)/fEff[mass])
            prexMass.append(float(mass))
#        exp.append(my_result.GetExpectedUpperLimit(0)*sigX[mass]*kFac[mass]*fEff[mass])
#        obs.append(my_result.UpperLimit()*sigX[mass]*kFac[mass]*fEff[mass])
#
#        exp_num = my_result.GetExpectedUpperLimit(0)*sigX[mass]*kFac[mass]*fEff[mass]*1000.0
#        obs_num = my_result.UpperLimit()*sigX[mass]*kFac[mass]*fEff[mass]*1000.0
        exp.append(my_result.GetExpectedUpperLimit(0)*sigX[mass]*kFac[mass])
        obs.append(my_result.UpperLimit()*sigX[mass]*kFac[mass])

        exp_num = my_result.GetExpectedUpperLimit(0)*sigX[mass]*kFac[mass]*1000.0
        obs_num = my_result.UpperLimit()*sigX[mass]*kFac[mass]*1000.0
        print>>fout_Obs, ("%15s,%15s" %(mass, obs_num))
        print>>fout_Exp, ("%15s,%15s" %(mass, exp_num))
        expd.append( (my_result.GetExpectedUpperLimit(1)-my_result.GetExpectedUpperLimit(0))
                     *sigX[mass]*kFac[mass])
        expu.append( (my_result.GetExpectedUpperLimit(0)-my_result.GetExpectedUpperLimit(-1))
                     *sigX[mass]*kFac[mass])
        
        exp2d.append( (my_result.GetExpectedUpperLimit(2)-my_result.GetExpectedUpperLimit(0))
                      *sigX[mass]*kFac[mass])
        exp2u.append( (my_result.GetExpectedUpperLimit(0)-my_result.GetExpectedUpperLimit(-2))
                      *sigX[mass]*kFac[mass])

        cross.append(sigX[mass]*kFac[mass])
        crossplus.append(sigX[mass]*kFac[mass]*(1-sigXu[mass]/100))
        crossminus.append(sigX[mass]*kFac[mass]*(1+sigXd[mass]/100))

#        expd.append( (my_result.GetExpectedUpperLimit(1)-my_result.GetExpectedUpperLimit(0))
#                     *sigX[mass]*kFac[mass]*fEff[mass])
#        expu.append( (my_result.GetExpectedUpperLimit(0)-my_result.GetExpectedUpperLimit(-1))
#                     *sigX[mass]*kFac[mass]*fEff[mass])
#        
#        exp2d.append( (my_result.GetExpectedUpperLimit(2)-my_result.GetExpectedUpperLimit(0))
#                      *sigX[mass]*kFac[mass]*fEff[mass])
#        exp2u.append( (my_result.GetExpectedUpperLimit(0)-my_result.GetExpectedUpperLimit(-2))
#                      *sigX[mass]*kFac[mass]*fEff[mass])
#
#        cross.append(sigX[mass]*kFac[mass]*fEff[mass])
#        crossplus.append(sigX[mass]*kFac[mass]*fEff[mass]*(1-sigXu[mass]/100))
#        crossminus.append(sigX[mass]*kFac[mass]*fEff[mass]*(1+sigXd[mass]/100))
        xMass.append(float(mass))
              
    if debug : 
        print "exp", exp
        print "obs", obs
        print "cross", cross
        print "xMass", xMass

    _hcrossLQ= ROOT.TGraph(len(xMass),array('f', xMass),array('f', cross))
    _hexpLQ = ROOT.TGraph(len(xMass),array('f', xMass),array('f', exp))
    _hobsLQ = ROOT.TGraph(len(xMass),array('f', xMass),array('f', obs))
    _hpreobsLQ = ROOT.TGraph(len(prexMass),array('f', prexMass),array('f', preobs))
    
    _hexp1LQ = ROOT.TGraphAsymmErrors( len(xMass),
                                       array('f', xMass),array('f', exp),
                                       array('f', [0]),array('f', [0]),
                                       array('f', expu),array('f', expd) )

    _hexp2LQ = ROOT.TGraphAsymmErrors( len(xMass),
                                       array('f', xMass),array('f', exp),
                                       array('f', [0]),array('f', [0]),
                                       array('f', exp2u),array('f', exp2d) )

    _hcrossLQu= ROOT.TGraph(len(xMass),array('f', xMass),array('f', crossplus))
    _hcrossLQd= ROOT.TGraph(len(xMass),array('f', xMass),array('f', crossminus))

    db_xMass=xMass+xMass
    _hcrosssigma=ROOT.TGraph(2*len(xMass),array('f', db_xMass),array('f', crossminus+crossplus))

    c1 =ROOT.TCanvas( "c", "A scan of m_{#tilde{g}} versus upper cross section",800, 600)
    c1.SetLeftMargin(0.2)
    c1.SetRightMargin(0.07)
    c1.SetTopMargin(0.07)
    c1.SetLogy()
    frame=ROOT.TH1F() 
    if "NUHM" in filename : 
        frame=c1.DrawFrame(200.,0.001,1000.,1.)
        frame.SetXTitle("m_{12} [GeV]")
    if "DD_Rpv" in filename : 
        frame=c1.DrawFrame(400.,0.002,1800.,3.)
        frame.SetXTitle("#tilde{d_{R}} [GeV]")    
    if "TT2Step" in filename:
        frame=c1.DrawFrame(200.,0.001,1000.,1.)
        frame.SetXTitle("m(#tilde{t}) [GeV]")

    frame.SetYTitle("#sigma [pb] * BR")
    
#    frame.GetXaxis().SetTitleSize( 0.04 )
#    frame.GetYaxis().SetTitleSize( 0.04 )
    
#    frame.GetXaxis().SetTitleOffset( 1.15 )
    frame.GetYaxis().SetTitleOffset( 1.8 )
        
    frame.GetXaxis().SetLabelSize( 0.035 )
    frame.GetYaxis().SetLabelSize( 0.035 )
    
    if "NUHM" in filename : 
        frame.GetXaxis().SetRangeUser(300,800)
        frame.GetYaxis().SetRangeUser(8E-4,9)
    if "DD_Rpv" in filename : 
        frame.GetXaxis().SetRangeUser(400,1600)    
    if "TT2Step" in filename:
        frame.GetXaxis().SetRangeUser(550,950)
        frame.GetYaxis().SetRangeUser(8E-3,4)
    frame.Draw()
    
    ROOT.gStyle.SetPaintTextFormat("2.2f")
    ROOT.gStyle.SetMarkerColor(14)
    ROOT.gStyle.SetTextColor(14)

    _hpreobsLQ.SetLineColor(ROOT.kMagenta)
    _hpreobsLQ.SetLineStyle(1)
    _hpreobsLQ.SetLineWidth(4)
      
    _hobsLQ.SetLineColor(ROOT.kOrange)
    _hobsLQ.SetLineStyle(1)
    _hobsLQ.SetLineWidth(4)
    _hexpLQ.SetLineColor(16)
    _hexpLQ.SetLineStyle(9)
    _hexpLQ.SetLineWidth(3)
    _hexpLQ.SetLineColor(c_myExp)
    _hexpLQ.SetLineStyle(9)
    _hexpLQ.SetLineWidth(3)
    _hobsLQ.SetLineColor(c_LightRed)
    _hobsLQ.SetLineStyle(1)
    _hobsLQ.SetLineWidth(4)
    
    _hcrossLQ.SetLineColor(ROOT.kBlue)
    _hcrossLQ.SetLineWidth(2)
    _hcrossLQu.SetLineColor(ROOT.kBlue)
    _hcrossLQu.SetLineWidth(2)
    _hcrossLQu.SetFillColor(ROOT.kBlue)
    _hcrossLQu.SetFillStyle(3004)
    _hcrossLQd.SetFillColor(10)
    _hcrossLQd.SetLineColor(ROOT.kBlue)
    _hcrossLQd.SetLineWidth(2)
    _hcrossLQd.SetLineStyle(2)
    _hcrossLQu.SetLineStyle(2)
    _hcrosssigma.SetFillStyle(3004)
    _hcrosssigma.SetFillColor(ROOT.kBlue)

    if "DD_Rpv" in filename:
        _hcross1,_hcross1u,_hcross1d = GetAdditionalRpvXs(xMass)

    _hexp2LQ.SetLineColor(c_LightYellow)
    _hexp2LQ.SetFillColor(c_LightYellow)
    _hexp2LQ.Draw("3:same")

    _hexp1LQ.SetLineColor(ROOT.kGreen)
    _hexp1LQ.SetFillColor(ROOT.kGreen)
    _hexp1LQ.Draw("3:same")    
    
    _hcrossLQu.Draw("L:same")
    _hcrossLQd.Draw("L:same")

    if "DD_Rpv" in filename:
        _hcross1.Draw("L:same")
        _hcross1u.Draw("L:same")
        _hcross1d.Draw("L:same")

    _hobsLQ.Draw("L:same")
    _hpreobsLQ.Draw("L:same")
    _hexpLQ.Draw("L:same")
    _hcrossLQ.Draw("L:same")
    
    upper_title = GetUpperTitle(filename)
    
    Leg0 = ROOT.TLatex()
#    Leg0.SetNDC()
#    Leg0.SetTextAlign( 11 )
#    Leg0.SetTextFont( 42 )
    Leg0.SetTextColor(ROOT.kBlack)
#    Leg0.SetTextSize(0.03)
    if "TT2Step" in filename:
        Leg0.SetTextSize(0.025)
        Leg0.DrawLatexNDC(0.2, 0.95, upper_title)
    else:
        Leg0.DrawLatexNDC(0.2, 0.95, upper_title)
    Leg0.Draw("same")
    
    atlasLabel = ROOT.TLatex()
    atlasLabel.SetNDC()
#    atlasLabel.SetTextFont(42)
    atlasLabel.SetTextColor(ROOT.kBlack)
    atlasLabel.SetTextSize( 0.043 )
    atlasLabel.DrawLatex(0.24, 0.85,"#splitline{#it{ATLAS} #bf{Internal}}{#bf{#splitline{#sqrt{s}=13 TeV, 139 fb^{-1}}{All limits at 95% CL}}}")
    atlasLabel.Draw()    
   
    clslimits = ROOT.TLatex()
    clslimits.SetNDC()
    clslimits.SetTextFont( 42 )
    clslimits.SetTextSize(0.032)
    clslimits.SetTextColor( ROOT.TColor.GetColor(ROOT.kBlack) )
    if "NUHM" in filename : 
        clslimits.DrawLatex(0.63, 0.63, "All limits at 95% CL")
    if "DD_Rpv" in filename : 
        clslimits.DrawLatex(0.63, 0.63, "All limits at 95% CL")
#    if "TT2Step" in filename:
#        clslimits.DrawLatex(0.63, 0.50, "All limits at 95% CL")
#    clslimits.Draw("same")
    
    Leg1 = ROOT.TLatex()
    Leg1.SetNDC()
    Leg1.SetTextFont( 72 )
    Leg1.SetTextSize( 0.032 )
    Leg1.SetTextColor( ROOT.kBlack )
    if "NUHM" in filename : 
        Leg1.DrawLatex(0.19, 0.71, " ")
    if "DD_Rpv" in filename : 
        Leg1.DrawLatex(0.19, 0.71, " ")
#    if "TT2Step" in filename:
#        Leg1.DrawLatex(0.19, 0.71, " ")
#    Leg1.Draw("same")

    if "NUHM" in filename : 
        Legend = ROOT.TLegend(0.57,0.68,0.79,0.91)
        Legend.SetFillColor(0)
        Legend.SetLineColor(ROOT.kWhite)
        Legend.SetTextSize( 0.033 )
        Legend.SetTextFont( 42 )
        Legend.AddEntry(_hcrossLQ,"pp#rightarrow#tilde{g}#tilde{g}","l")
        Legend.AddEntry(_hcrossLQu,"Theoretical uncertainty","l")
        Legend.AddEntry(_hexpLQ,"Expected limit","l")
        Legend.AddEntry(_hobsLQ,"Observed limit","l")
        Legend.AddEntry(_hexp1LQ,"Expected #pm 1#sigma","f")
        Legend.AddEntry(_hexp2LQ,"Expected #pm 2#sigma","f")

        Legend.Draw("same")

    if "TT2Step" in filename:
        Legend = ROOT.TLegend(0.57,0.5,0.79,0.91)
        Legend.SetFillColor(0)
        Legend.SetLineColor(ROOT.kWhite)
        Legend.SetTextSize( 0.04 )
        Legend.SetTextFont( 42 )
        Legend.AddEntry(_hcrossLQ,"pp#rightarrow#tilde{t} #tilde{t}","l")
        Legend.AddEntry(_hcrossLQu,"Theoretical uncertainty","l")
        Legend.AddEntry(_hexpLQ,"Expected limit","l")
        Legend.AddEntry(_hobsLQ,"Observed limit","l")
        Legend.AddEntry(_hexp1LQ,"Expected #pm 1#sigma","f")
        Legend.AddEntry(_hexp2LQ,"Expected #pm 2#sigma","f")
        Legend.AddEntry(_hpreobsLQ,"#splitline{SS/3L obs. 36 fb^{-1}}{[arXiv:1706.03731]}","l")

        Legend.Draw("same")

    if "DD_Rpv" in filename : 
        Legend = ROOT.TLegend(0.57,0.68,0.79,0.91)
        Legend.SetFillColor(0)
        Legend.SetLineColor(ROOT.kWhite)
        Legend.SetTextSize( 0.033 )
        Legend.SetTextFont( 42 )
        Legend.AddEntry(_hcrossLQ,"pp#rightarrow#tilde{d_{R}}#tilde{d_{R}} NLO, m(#tilde{g})=2.0TeV","l")
        Legend.AddEntry(_hcrossLQu,"Theoretical uncertainty","l")
        Legend.AddEntry(_hcross1,"pp#rightarrow#tilde{d_{R}}#tilde{d_{R}} NLO, m(#tilde{g})=1.4TeV","l")
        Legend.AddEntry(_hcross1u,"Theoretical uncertainty","l")
        Legend.AddEntry(_hexpLQ,"Expected limit","l")
        Legend.AddEntry(_hobsLQ,"Observed limit","l")
        Legend.AddEntry(_hexp1LQ,"Expected #pm 1#sigma","f")
        Legend.AddEntry(_hexp2LQ,"Expected #pm 2#sigma","f")
        Legend.Draw("same")
    
#    Leg1 = ROOT.TLatex()
#    Leg1.SetNDC()
#    Leg1.SetTextFont( 42 )
#    Leg1.SetTextSize( 0.033 )
#    Leg1.SetTextColor( ROOT.kBlack )
#    Leg1.DrawLatex(0.24, 0.82, "#sqrt{s}=13 TeV, 139 fb^{-1}")
#    Leg1.Draw("same")
    
    frame.Draw( "sameaxis" )
    c1.SaveAs(options.DirName+options.OutputName+".root")
    c1.SaveAs(options.DirName+options.OutputName+".pdf")
    c1.SaveAs(options.DirName+options.OutputName+".png")
    c1.SaveAs(options.DirName+options.OutputName+".eps")
    c1.SaveAs(options.DirName+options.OutputName+".C")

def GetMass(signalID,grid=""):    
    ID = signalID.strip('hypo_signal').strip('debug_signal')
    if ID in signalRunnumberToMassesDict[grid]:
        masses = signalRunnumberToMassesDict[grid][ID]
        return str(masses[0])
def GetPreObs(grid,mass):
    preobsDict={}
    Preobs=0.0
    if "TT2Step" not in grid:
        print "No previous obs regisrated!!!"
        return Preobs 
    else:
#        preobsDict={'550.0':10.0,'600.0':8.8,'650.0':8.2,'700.0':8.2,'750.0':11,'800.0':11,'850.0':11, '900.0':11, '950.0':11} # Those xsec use fb instead of pb
        preobsDict={'550.0':10.0,'600.0':8.8,'650.0':8.2,'700.0':8.2,'750.0':11} # Those xsec use fb instead of pb
        Preobs=preobsDict[mass]
        return Preobs

def GetXsec(gridName):
    if "DD_Rpv" in gridName:
        sigX={"400.0":0.14610000 ,"500.0":0.07288000 ,"600.0":0.04108000 ,"700.0":0.02446000 ,"800.0":0.01498000 ,
              "900.0":0.00937500 ,"1000.0":0.00596300 ,"1100.0":0.00381100 ,"1200.0":0.00245800 ,"1300.0":0.00159100 ,
              "1400.0":0.00102800 ,"1500.0":0.00067280 ,"1600.0":0.00043820 ,"1700.0":0.00028480 ,"1800.0":0.00018460}
        return sigX
    if "NUHMstrong" in gridName:
        sigX={'300.0':0.6083, '350.0':0.2513, '400.0':0.1123, '500.0':0.02619, '600.0':0.0072, '700.0':0.0022, '800.0':0.0008}
        return sigX
    if "NUHMweak" in gridName:
        sigX={'300.0':0.9700, '350.0':0.6165, '400.0':0.4154, '500.0':0.1896, '600.0':0.0938, '700.0':0.0469, '800.0':0.0252}
        return sigX
    if "TT2Step" in gridName:
        sigX={'550.0':0.347,'600.0':0.205,'650.0':0.125,'700.0':0.0783,'750.0':0.05,'800.0':0.0326,'850.0':0.0216, '900.0':0.0145, '950.0':0.00991}
        return sigX

def GetThUnc(gridName):
    if "DD_Rpv" in gridName:
        sigXu={"400.0":19.025901 ,"500.0":17.252949 ,"600.0":17.385592 ,"700.0":17.736995 ,"800.0":18.590992,
               "900.0":19.249648 ,"1000.0":19.852665 ,"1100.0":21.010647 ,"1200.0":22.027840 ,"1300.0":22.975705,
               "1400.0":24.195755 ,'1500.0':24.897010 ,'1600.0':25.778918 ,'1700.0':26.787544 ,'1800.0':27.585888}
        return sigXu
    if "NUHMstrong" in gridName:
        sigXu={"300.0":20.72, "350.0":22.71, "400.0":24.40, "500.0":28.81, "600.0":33.00, "700.0":37.73, "800.0":42.83}
        return sigXu
    if "NUHMweak" in gridName:
        sigXu={'300.0':0., '350.0':0., '400.0':0., '500.0':0., '600.0':0., '700.0':0., '800.0':0.}
        return sigXu
    if "TT2Step" in gridName:
        sigXu={'550.0':7.81,'600.0':8.12,'650.0':8.45,'700.0':8.80,'750.0':9.16,'800.0':9.53, '850.0':9.93,'900.0':10.33, '950.0':10.76}
        return sigXu

def GetKfac(gridName):
    if "DD_Rpv" in gridName:
        kFac={"400.0":1.0 ,"500.0":1.0 ,"600.0":1.0 ,"700.0":1.0 ,"800.0":1.0 ,
              "900.0":1.0 ,"1000.0":1.0 ,"1100.0":1.0 ,"1200.0":1.0 ,"1300.0":1.0 ,
              "1400.0":1.0 ,"1500.0":1.0 ,"1600.0":1.0 ,"1700.0":1.0 ,"1800.0":1.0}
        return kFac
    if "NUHMstrong" in gridName:
        kFac={"300.0":1., "350.0":1., "400.0":1., "500.0":1., "600.0":1., "700.0":1., "800.0":1.}
        return kFac
    if "NUHMweak" in gridName:
        kFac={"300.0":1., "350.0":1., "400.0":1., "500.0":1., "600.0":1., "700.0":1., "800.0":1.}
        return kFac
    if "TT2Step" in gridName:
        kFac={'550.0':1.,'600.0':1.,'650.0':1.,'700.0':1.,'750.0':1.,'800.0':1.,'850.0':1.,'900.0':1.,'950.0':1.}
        return kFac

def GetFeff(gridName):
    if "DD_Rpv" in gridName:
        fEff={"400.0":1.0 ,"500.0":1.0 ,"600.0":1.0 ,"700.0":1.0 ,"800.0":1.0 ,
              "900.0":1.0 ,"1000.0":1.0 ,"1100.0":1.0 ,"1200.0":1.0 ,"1300.0":1.0 ,
              "1400.0":1.0 ,"1500.0":1.0 ,"1600.0":1.0 ,"1700.0":1.0 ,"1800.0":1.0}
        return fEff
    if "NUHMstrong" in gridName:
        fEff={"300.0":1., "350.0":1., "400.0":1., "500.0":1., "600.0":1., "700.0":1., "800.0":1.}
        return fEff
    if "NUHMweak" in gridName:
        fEff={"300.0":1., "350.0":1., "400.0":1., "500.0":1., "600.0":1., "700.0":1., "800.0":1.}
        return fEff
    if "TT2Step" in gridName:
        fEff={'550.0':0.11895,'600.0':0.11901,'650.0':0.11906,'700.0':0.12013,'750.0':0.11883,'800.0':0.11816,'850.0':0.11870 ,'900.0':0.11994 , '950.0':0.12158}
        return fEff

def GetUpperTitle(gridName):
    if "DD_Rpv321" in gridName:
        uppertitle = "#tilde{d_{R}} #tilde{d_{R}} production, #tilde{d_{R}} #rightarrow #bar{s} #bar{t} (BR=100%) "
        return uppertitle
    if "DD_Rpv331" in gridName:
        uppertitle = "#tilde{d_{R}} #tilde{d_{R}} production, #tilde{d_{R}} #rightarrow #bar{b} #bar{t} (BR=100%) "
        return uppertitle
    if "NUHMstrong" in gridName:
        uppertitle = "NUHM2: m_{0}=5 TeV, A_{0}=-1.6m_{0}, tan#beta=15, #mu=150 GeV, m_{A}=1 TeV"
        return uppertitle
    if "NUHMweak" in gridName:
        uppertitle = "NUHM2weak"
        return uppertitle
    if "TT2Step" in gridName:
        uppertitle = "#tilde{t_{1}}#tilde{t_{1}} production, #tilde{t_{1}} #rightarrow tW^{#pm}#tilde{#chi}^{#pm}_{1}, #tilde{#chi}^{#pm}_{1} #rightarrow W*#tilde{#chi}^{0}_{1}; m(#tilde{#chi}^{0}_{1}) = m(#tilde{t_{1}})-275 GeV ; m(#tilde{#chi}^{0}_{2})=m(#tilde{#chi}^{0}_{1})+100 GeV ; m(#tilde{#chi}^{#pm}_{1}) #approx m(#tilde{#chi}^{0}_{1})"
        return uppertitle

def green(msg): return "\033[0;32m{0}\033[0m".format(msg);
def red(msg): return "\033[0;31m{0}\033[0m".format(msg);
def bold(msg): return "\033[1m{0}\033[0m".format(msg);

def GetAdditionalRpvXs(xMass):
    # sigX2 = [ 3.434e-01, 1.698e-01, 9.013e-02, 5.010e-02, 2.902e-02, 1.727e-02, 1.020e-02] # 1000
    # sigXu2=[ 0.08517075, 0.07941115, 0.08874666, 0.09657623, 0.10963218, 0.12151627, 0.13092962] #1000
    # sigX1 = [ 2.779e-01, 1.404e-01, 7.614e-02, 4.313e-02, 2.526e-02, 1.518e-02, 9.280e-03, 5.717e-03, 3.512e-03] # 1200
    # sigXu1=[ 0.07926095, 0.08190400, 0.08317371, 0.09246224, 0.09982204, 0.11119369, 0.12376407, 0.13449379, 0.14495552] # 1200 
    sigX1 = [ 2.270e-01, 1.165e-01, 6.464e-02, 3.727e-02, 2.212e-02, 1.346e-02, 8.284e-03, 5.155e-03, 3.245e-03, 2.050e-03, 1.289e-03]  # 1400
    sigXu1=[ 0.08076413, 0.07511568, 0.07772656, 0.08813797, 0.09427478, 0.10410281, 0.11180565, 0.12482838, 0.13742908, 0.14978198, 0.15827338] # 1400 

    sigXp1 = [ sigX1[i]*(1+(sigXu1[i]+0.1)) for i in range(len(sigX1))]
    sigXm1 = [ sigX1[i]*(1-(sigXu1[i]+0.1)) for i in range(len(sigX1))]

    _hcross1= ROOT.TGraph(len(sigX1),array('f', xMass),array('f', sigX1))
    _hcross1u= ROOT.TGraph(len(sigX1),array('f', xMass),array('f', sigXp1))
    _hcross1d= ROOT.TGraph(len(sigX1),array('f', xMass),array('f', sigXm1))

    _hcross1.SetLineColor(ROOT.kRed)
    _hcross1.SetLineWidth(2)
    _hcross1u.SetLineColor(ROOT.kRed)
    _hcross1u.SetLineWidth(2)
    _hcross1u.SetFillColor(ROOT.kRed)
    _hcross1u.SetFillStyle(3004)
    _hcross1d.SetFillColor(10)
    _hcross1d.SetLineColor(ROOT.kRed)
    _hcross1d.SetLineWidth(2)
    _hcross1d.SetLineStyle(2)
    _hcross1u.SetLineStyle(2)

    return _hcross1,_hcross1u,_hcross1d


def makeBest(filename,dirname):

    file1=filename
    file2=''
    if 'Rpv2L1bS' in filename:
        file2=file1.replace('Rpv2L1bS','Rpv2L1bM')
    if 'Rpv2L1bM' in filename:
        file2=file1.replace('Rpv2L1bM','Rpv2L1bS')
    print 'file1: ',file1
    print 'file2: ',file2

    outfile_name = file1.split(".")[0]+"_best.root"
    print 'outfile: ',outfile_name

    _file1 = ROOT.TFile.Open(dirname+file1,'r')
    _file2 = ROOT.TFile.Open(dirname+file2,'r')
    _outfile = ROOT.TFile.Open(dirname+outfile_name,'w')

    signal_list1=[]
    
    for key in _file1.GetListOfKeys():
        kname = key.GetName()
        if kname=="ProcessID0":
            continue
        if debug : print kname
        signal_list1.append(kname)

    signal_list1.sort()

    for s in signal_list1:
        my_result1=_file1.Get(s)
        my_result2=_file2.Get(s)
        ExpUL1 = my_result1.GetExpectedUpperLimit(0.)
        ExpUL2 = my_result2.GetExpectedUpperLimit(0.)
        if (ExpUL1 < ExpUL2):
            _outfile.write(my_result1)
        else:
            _outfile.write(my_result2)

        _outfile.close()
    return outfile_name

def setAtlasStyle():
   # AtlasStyle = pathUtilities.histFitterTopDirectory()+'/PlottingMacros/atlasstyle-00-03-04/' # Makes weird error message when loading macro
   AtlasStyle = "./../PlottingMacros/atlasstyle-00-03-04/"
   if not os.path.exists(AtlasStyle):
      print red("{0} not found. Please set path for AtlasStyle".format(AtlasStyle)); return
   ROOT.gROOT.LoadMacro(AtlasStyle+"AtlasStyle.C")
   ROOT.gROOT.ProcessLine("SetAtlasStyle()")

if __name__ == "__main__":
    main()
