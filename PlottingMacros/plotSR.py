import os
import sys
import time
import ROOT
import pickle
import SRTableTex
import json

from math import sqrt
from math import log
from glob import glob
from argparse import ArgumentParser
import pandas as pd


####___HOW TO USE___#####
#__Before running:____
#..1) Add SRs and VRs in  'allRegions' object in addSRs() and addVRs() functions
#..2) Add bkgs in 'allBkg' object.
#..3) Define 'lumiTag' (same as used in the main control script, in  pb-1)
#..4) Define 'luminosityError' (relative value): Used to compute up and down lumi variations
#..5) Define 'runNameTag': same as used in the main control script to get the fit
#..6) Define 'syst' tag: systematic tag used in the job. Normally is 'ALL'
#..7) Define 'blindTag': if regions were blinded then use "_blind<reg1>_<reg2>_<regN>". Example: '_blindSR'
#..9) Define ATLAS label ("Internal/Preliminary/")
#..10) Define 'treeSystematics': list containing the systematics affecting the shape of the distribution in the fit configuration. They can be found at the function GetTreeSystematics() 

#--> Macro has to be run independently for SRs and VRs of both. 

debug=False

class regionsDef:

    def __init__(self):
        self.regionList=[]
        self.regionObserved={}
        self.regionVetoBkg={}

    def addRegion(self,name,veto=[]):
        self.regionList.append(name)
        self.regionObserved[name]=0  #observed number of events for that region
        self.regionVetoBkg[name]=veto #this will show the symbol "-" in the table if this bkg does not apply to the determined region, for example, charge flip in 3L regions.

    def setObserved(self,name,observed):
        self.regionObserved[name]=int(observed)

    def getList(self):
        return self.regionList

    def getObserved(self,name):
        return self.regionObserved[name]

    def getVetoBkg(self,name):
        return self.regionVetoBkg[name]

    def hasVetoBkg(self):
        return self.regionVetoBkg


class sample:
   
    def __init__(self,name,color,legend,tex,isMC):
        self.name=name
        self.color=color
        self.legend=legend
        self.tex=tex
        self.isMC=isMC
        self.val={}
        self.stat={}
        self.dfSyst={}
        self.systUp={}
        self.systDown={}
        self.systSym={}

    def setYieldAndStatistical(self,reg,val,stat):
        self.val[reg]=val
        self.stat[reg]=stat   

    def setSystematics(self,reg,df):

        df['sigUp']  = df['High']-self.val[reg]        
        df['sigDown']= self.val[reg]-df['Low']

  
        #need to check if variations are exactly the same. If this is the case, symmetrize them.
        for index, row in df.iterrows():

            if row['High']==row['Low'] and row['sigUp'] !=0 and index not in treeSystematics:#symmetrization is applied only to OveralSyst
                print "- This uncertainty will be symmetrized: ", index
                if row['sigUp']<0: df.set_value(index,'sigUp',row['sigDown'])
                elif row['sigDown']<0: df.set_value(index,'sigDown',row['sigUp'])

        df['symmetric'] = abs(0.5*(df['sigUp']+df['sigDown']))
        df['symmetric2'] = df['symmetric']**2

        df['sigUp2'] = df['sigUp']**2
        df['sigDown2'] = df['sigDown']**2

        self.systUp[reg] = sqrt(df['sigUp2'].sum())  
        self.systDown[reg] = sqrt(df['sigDown2'].sum())
        self.systSym[reg] = sqrt(df['symmetric2'].sum())

        self.dfSyst[reg] = df

        if debug: print df

       

    def getName(self):
        return self.name
    def getColor(self):
        return self.color
    def getLegendName(self):
        return self.legend
    def getTexName(self):
        return self.tex
    def getIsMC(self):
        return self.isMC

    def getYield(self,reg):
        return self.val[reg]

    def getStatistical(self,reg):
        return self.stat[reg]

    def getSystematicDF(self,reg):
        return self.dfSyst[reg]

    def getUpAndDown(self,reg):

        up = sqrt(self.systUp[reg]**2+self.stat[reg]**2)
        down = sqrt(self.systDown[reg]**2+self.stat[reg]**2)
        sym = sqrt(self.systSym[reg]**2 + self.stat[reg]**2)

        return (up,down,sym)
 

class bkgsDef:

    def __init__(self):
        self.bkgList = []

    def addSample(self,name,color,legend,tex,isMC):
        self.bkgList.append(sample(name,color,legend,tex,isMC))


allRegions=regionsDef()

allBkg=bkgsDef()


##---- to define before running ------##
#allBkg.addSample('Multitop',ROOT.kAzure+7,"t(W)Z, t#bar{t}H, t#bar{t}VV, 3t, 4t","t(W)Z, $t\\bar{t}H, t\\bar{t}VV, 3t, 4t$")
allBkg.addSample('MisCharge',ROOT.kRed+2,'Charge-flip','Charge-flip',False)
allBkg.addSample('OtherMultiboson',ROOT.kGreen+2,"WW, ZZ, VH, VVV","$WW, ZZ, VH, VVV$",True)
allBkg.addSample('ttH',ROOT.kOrange,"t#bar{t}H","$t\\bar{t}H$",True)
allBkg.addSample('RareTop_NottH',ROOT.kCyan+1,"t(W)Z, t#bar{t}VV, 3t, 4t","$t(W)Z,t\\bar{t}VV, 3t, 4t$",True)
allBkg.addSample('ttW',ROOT.kViolet-9,"t#bar{t}W","$t\\bar{t}W$",True)
allBkg.addSample('ttZ',ROOT.kAzure+7,"t#bar{t}Z","$t\\bar{t}Z$",True)
allBkg.addSample('WZ',ROOT.kOrange+1,"WZ","$WZ$",True)
allBkg.addSample('Fakes',19,"Fake/non-prompt","Fake/non-prompt",False)

def addSRs():

    allRegions.addRegion("Rpc2L0b")
    allRegions.addRegion("Rpc2L1b")
    allRegions.addRegion("Rpc2L2b")
    allRegions.addRegion("Rpc3LSS1b",["ttV","ttW","ttZ","WZ"])
    allRegions.addRegion("Rpv2L")
    
    return

def addVRs():

    allRegions.addRegion("VRttV")
    allRegions.addRegion("VRWZ4j",['MisCharge'])
    allRegions.addRegion("VRWZ5j",['MisCharge'])

    return

lumiTag='138964'
luminosityError=0.017
ATLASlabel=''
runNameTag='_MCId_'
syst="ALL"
blindTag='_blindALL'
treeSystematics=['EG_Scale','EG_Resolution','JET_scale_NP1','JET_scale_NP2','JET_scale_NP3','JET_EtaIntercalibration_NonClosure_highE',
'JET_EtaIntercalibration_NonClosure_negEta','JET_EtaIntercalibration_NonClosure_posEta','JET_JER_DataVsMC','JET_JER_EffectiveNP_1','JET_JER_EffectiveNP_2',
'JET_JER_EffectiveNP_3','JET_JER_EffectiveNP_4','JET_JER_EffectiveNP_5','JET_JER_EffectiveNP_6','JET_JER_EffectiveNP_7restTerm','JET_AFII','Mu_ID','Mu_MS',
'Mu_Sagitta_Res','Mu_Sagitta_Rho','Mu_Scale','MET_Soft_reso_Para','MET_Soft_reso_Perp','MET_Soft_Scale']

#-------------------------------------##

AsymmetricUnc={}

region='SR'

luminosity=str(int(round(float(lumiTag)/1000)))

FileAsymmetricUnc='AsymmetricUnc.json'

def main():
    parser = ArgumentParser(description="Script for producing SR summary plot")
    parser.add_argument("--InDir",  help="Directory with yields tables",    default="")
    parser.add_argument("--Prefix", help="Prefix of .pickle files (before the SR name)",default="bkgOnly")
    parser.add_argument("--Blind", action='store_true', help="Observed = Expected")
    parser.add_argument("--Plot",   type=int, help="Creating plot with SR", default=1)
    parser.add_argument("--fitted", type=int, help="Use post-fit numbers",  default=0)
    parser.add_argument("--makeTex",type=int, help="Creating .tex output",  default=0)
    parser.add_argument("--Name",   help="Name of output plot/table",choices=["SRYields","VRYields","AllYields"],   default="SRYields")
    parser.add_argument("--Ratio",  type=int, help="Plot Nobs/Nexp",        default=1)  
    parser.add_argument("--LogY",   type=int, help="Using y-axis in log",   default=0) 
    parser.add_argument("--doPlotAsymUnc", type=int, help="Asymmetric uncertainties will be shown in tables and plots!!", default=0)
    parser.add_argument("--doSig", type=int, help="Plot significance at the bottom pad (if assymetric uncertaines, it will use the highest variation as input)",default=0)
    parser.add_argument("--readSystfromTxt",action='store_true',help="If activated then it will yiels (including observed ones), statistical and systematic uncertainties from the file AsymmetricUnc.json previously created. ")
    parser.add_argument("--debug",action='store_true',help="Print information to help debugging")

    options = parser.parse_args()

    global debug
    if options.debug: debug=True

    ## adding regions
    if 'VR' in options.Name:
	global region
	region='VR'
 
        addVRs()

    elif 'SR' in options.Name:

        addSRs()

    else:
  
        addVRs()
	addSRs()


    #Reading the workspace:
    if options.readSystfromTxt: readSystematicsFromFile()
    else: readWorkspace()


    print bold("-- Running in blind mode {0}".format(options.Blind))

    #initialize variables:
    SRNames = []; Nexp = []; NexpErr = []; Nobs = []; NobsErr = []; NBkg = []; EBkg = [];
    NexpErr_dn = []; EBkg_dn = [] #for asymmetric uncertainties. The up components will be rewritten in NexpErr and EBkg.


    #Get list regions:
    SRNames = allRegions.getList()

    #Get observed events
    Nobs = getObserved(SRNames,options.Blind,options.readSystfromTxt)


    #get yields
    if options.fitted:
        print bold("-- Using post-fit numbers {0}".format(options.fitted))

        Nexp, NBkg, NexpErr, EBkg = getFittedValues(SRNames,bkgList(),options.InDir,options.Prefix)
        
    else:
        print bold("-- Using pre-fit numbers...")

        Nexp, NBkg, NexpErr, NexpErr_dn, EBkg, EBkg_dn = getPrefitValues(SRNames,bkgList(),options.doPlotAsymUnc)
        

    if options.makeTex:

        if (options.doPlotAsymUnc and not options.fitted): makeTexAsymmetric(options.Name,SRNames,Nexp,NexpErr,NexpErr_dn,Nobs,NBkg,EBkg,EBkg_dn,len(SRNames))
        else: makeTex(options.Name, SRNames, Nexp, NexpErr, Nobs, NBkg, EBkg,len(SRNames))    

    if options.Plot:
        makePlot(options.Name, SRNames, Nexp, NexpErr, Nobs, NBkg, options.LogY, options.Ratio,options.doPlotAsymUnc,options.fitted,options.doSig)
        time.sleep(2)


    return


def getPrefitValues(SRNames,bkgs,doAsym):

    nExp=[]; Bkg=[];
    nExp_err_up=[]; nExp_err_dn = []; EBkg_up = []; EBkg_dn=[];

    for i in range(len(SRNames)):

        yid = AsymmetricUnc[SRNames[i]]["Total"]['yield']
        tot_up = AsymmetricUnc[SRNames[i]]["Total"]['up']
        tot_dn = AsymmetricUnc[SRNames[i]]["Total"]['down']
        
        if doAsym==False:
            tot_up = AsymmetricUnc[SRNames[i]]["Total"]['sym']
            tot_dn = tot_up

        nExp.append(yid)
        nExp_err_up.append(tot_up)
        nExp_err_dn.append(tot_dn)

        nbkg = []; err_up = []; err_dn =[];
        for j in range(len(bkgs)):
            bkg   = AsymmetricUnc[SRNames[i]][bkgs[j].getName()]['yield']
            eB_up = AsymmetricUnc[SRNames[i]][bkgs[j].getName()]['up']
            eB_dn = AsymmetricUnc[SRNames[i]][bkgs[j].getName()]['down']

            if doAsym==False: 
                eB_up = AsymmetricUnc[SRNames[i]][bkgs[j].getName()]['sym']
                eB_dn = eB_up            

            nbkg.append(float(bkg))
            err_up.append( float(eB_up) )
            err_dn.append( float(eB_dn) )

        Bkg.append(nbkg)
        EBkg_up.append(err_up)
        EBkg_dn.append(err_dn)


    print "total : ",nExp
    print "errors total up : ",nExp_err_up
    print "errors total dn : ",nExp_err_dn


    print "samples : : ",Bkg
    print "errors samples up : ", EBkg_up
    print "errors samples dn : ", EBkg_dn

    return nExp, Bkg, nExp_err_up, nExp_err_dn, EBkg_up, EBkg_dn

def getObserved(SRNames,blind,readfromText):

    Nobs = []

    for SRName in SRNames:

        if readfromText: obs = AsymmetricUnc[SRName]['observed']
        else: obs=allRegions.getObserved(SRName)

        if blind:
            obs = AsymmetricUnc[SRName]["Total"]['yield']
            print bold("Setting obs=expected")

        Nobs.append(obs)       

    print "Nobs = ", Nobs

    return Nobs

def getFittedValues(SRNames,bkgs,inDir,prefix):
    '''
    Return fitted yields contained in the pickled files

    '''

    Nexp = []; NexpErr = []; NBkg = []; EBkg = [];

    if not len(inDir) or not os.path.exists(inDir):
        print red("Please specify an input directory"); sys.exit(1)


    for SRName in SRNames:

        SRFile = inDir+"/"+prefix+"_"+SRName+".pickle"

        try: fYield = open(SRFile,"r")
        except:
            print red("{0} cannot be opened".format(SRFile)); continue


        SRYields = pickle.load(fYield)
        exp  = SRYields[keyBkgTot(True)][0]
        expE = SRYields[keyErrTot(True)][0]

        expE = addStats(expE, SRName,'Total',True)

        Nexp.append( float(exp) )
        NexpErr.append( float(expE) )

        nbkg = []; ebkg = [];
        for i in range(len(bkgList())):
            nB = SRYields[keyBkg(True)+bkgList()[i].getName()][0]
            eB = SRYields[keyErr(True)+bkgList()[i].getName()][0]

            eB = addStats(eB, SRName, bkgList()[i].getName(),True)

            nbkg.append( float(nB) )
            ebkg.append( float(eB) )
        NBkg.append(nbkg)
        EBkg.append(ebkg)

        print "--> {0}, Nexp={1:.2f} +/- {2:.2f}".format(SRName, exp, expE)
        for i in range(len(bkgList())):
            print "    {0} {1:.2f} +/- {2:.2f}  ".format(bkgList()[i].getName(),nbkg[i],ebkg[i]),
        print


    print bold("-- Retrieved numbers from {0} SR".format(len(Nexp)))

    return Nexp, NBkg, NexpErr, EBkg

def bkgList():
    return allBkg.bkgList

def  makeTexAsymmetric(name,srnames,nexp,err_exp_up,err_exp_dn,nobs,nbkg,ebkg_up,ebkg_dn,ncolumns):

    

    texFile = open("{0}.tex".format(name),"w")
         
    tabLabel1 = "observed_sr_yields_table1"
    if 'VR' in region:
        tabLabel1 = "observed_vr_yields_table1"

    texFile.write( SRTableTex.tableStart() )

    #table1  
    texFile.write( SRTableTex.tabularStartAsym(ncolumns) )
    texFile.write( SRTableTex.insertSRnamesAsym(srnames[0:ncolumns]) )
    texFile.write( SRTableTex.insertSingleLine() ) 
    texFile.write( SRTableTex.insertObservedAsym(nobs[0:ncolumns]) ) 
    texFile.write( SRTableTex.insertDoubleLine() )
    texFile.write( SRTableTex.insertTotalSMAsym(nexp[0:ncolumns],err_exp_up[0:ncolumns],err_exp_dn[0:ncolumns]) )
    texFile.write( SRTableTex.insertSingleLine() ) 

    
    for i in range(len(bkgList())):

        veto=[]
        #get positions of regions 

        for reg in srnames:
            if bkgList()[i].getName() in allRegions.getVetoBkg(reg):
               veto.append(srnames.index(reg))

        texFile.write( SRTableTex.insertBkgAsym( bkgList()[i].getTexName(), [b[i] for b in nbkg[0:ncolumns]], [e[i] for e in ebkg_up[0:ncolumns]],[e[i] for e in ebkg_dn[0:ncolumns]],veto) )
    


    texFile.write( SRTableTex.tabularEndAsym() )
    texFile.write( SRTableTex.tableEnd(tabLabel1,luminosity,'VR' in region,allRegions.hasVetoBkg()) )

    print bold("-- Created {0}".format(texFile.name))

    return

def makeTex(name, srnames, nexp, err_exp, nobs, nbkg, ebkg,ncolumns):

    texFile = open("{0}.tex".format(name),"w")

    tabLabel1 = "observed_sr_yields_table1"
    if 'VR' in region:
        tabLabel1 = "observed_vr_yields_table1"

    texFile.write( SRTableTex.tableStart() )

    #table1
    texFile.write( SRTableTex.tabularStart(ncolumns) )
    texFile.write( SRTableTex.insertSRnames(srnames[0:ncolumns]) )
    texFile.write( SRTableTex.insertSingleLine() )
    texFile.write( SRTableTex.insertObserved(nobs[0:ncolumns]) )
    texFile.write( SRTableTex.insertDoubleLine() )
    texFile.write( SRTableTex.insertTotalSM(nexp[0:ncolumns],err_exp[0:ncolumns]) )
    texFile.write( SRTableTex.insertSingleLine() )
    for i in range(len(bkgList())):

        veto=[]
        #get positions of regions 

        for reg in srnames:
            if bkgList()[i].getName() in allRegions.getVetoBkg(reg):
               veto.append(srnames.index(reg)) 

        texFile.write( SRTableTex.insertBkg( bkgList()[i].getTexName(), [b[i] for b in nbkg[0:ncolumns]], [e[i] for e in ebkg[0:ncolumns]],veto) )
    texFile.write( SRTableTex.tabularEnd() )

    texFile.write( SRTableTex.tableEnd(tabLabel1,luminosity,'VR' in region,allRegions.hasVetoBkg()) )
    
    print bold("-- Created {0}".format(texFile.name))
    return

def makePlot(name, srnames, nexp, err_exp, nobs, nbkg, logy, ratio, doPlotAsymUnc,fitted,doSig):    

    AtlasStyle = "atlasstyle-00-03-04/"
    if not os.path.exists(AtlasStyle):
        print red("{0} not found. Please set path for AtlasStyle".format(AtlasStyle)); return

    ROOT.gROOT.LoadMacro(AtlasStyle+"MyStyle.C")
    ROOT.gROOT.ProcessLine("SetMyStyle()")
    
    NSR = len(nexp)
    print green("Creating TH1F with {0} entries".format(NSR))

    hData = ROOT.TH1F("hData","hData", NSR, 0, NSR)
    hTot  = ROOT.TH1F("hTot", "hTot",  NSR, 0, NSR)

    hBkg  = ROOT.THStack("hBkg", "hBkg")

    bkgHist = []
    for i in range(len(bkgList())):
        hbkg = ROOT.TH1F(bkgList()[i].getName(),bkgList()[i].getName(), NSR, 0, NSR)
        bkgHist.append(hbkg)


    for sr in range(NSR):
        hTot.SetBinContent(sr+1, nexp[sr])
        hTot.SetBinError(sr+1, err_exp[sr])
        print 'Setting bin content for total SM',sr+1,": ",nexp[sr],", unc:",err_exp[sr]

        hData.SetBinContent(sr+1, nobs[sr])
        hData.SetBinError(sr+1, 0.01)

        for i in range(len(bkgList())):
            bkgHist[i].SetBinContent(sr+1, nbkg[sr][i])

    for i in range(len(bkgList())):
        bkgHist[i].SetLineWidth(1)
        bkgHist[i].SetLineColor(ROOT.kBlack)
        bkgHist[i].SetFillColor(bkgList()[i].getColor())
        hBkg.Add(bkgHist[i])
        
    if not ratio:
        c  = ROOT.TCanvas(name, name, 1, 10, 1150, 480)
        p1 = ROOT.TPad(name+"1",name+"1", 0.00, 0.00, 1.00, 1.00, -1, 0, 0)
        c.cd()
        p1.SetLeftMargin(0.07)  
        p1.Draw()
    
    else:

        c  = ROOT.TCanvas(name, name, 1, 10, 1150, 560)
        p1 = ROOT.TPad(name+"1",name+"1", 0.00, 0.35, 1.00, 1.00, -1, 0, 0)
        p2 = ROOT.TPad(name+"2",name+"2", 0.00, 0.00, 1.00, 0.35, -1, 0, 0)

        p1.SetRightMargin(0.08);
        p1.SetLeftMargin(0.07);
        p1.SetBottomMargin(0.0);
        p1.SetTopMargin(0.05);

        p2.SetRightMargin(0.08);
        p2.SetLeftMargin(0.07);
        p2.SetBottomMargin(0.35);
        p2.SetTopMargin(0.0);


        c.cd()
        p1.Draw()
        p2.Draw()
     
    setGrid = False       
    if logy: p1.SetLogy()
    if setGrid: p1.SetGridx()
    p1.cd()

    yMax = ROOT.TMath.Max(hData.GetMaximum(), hTot.GetMaximum())
    if logy:
        hTot.GetYaxis().SetRangeUser(0.5, yMax*10.)
    else:
        hTot.GetYaxis().SetRangeUser(0.105, yMax*2.1)

    for i in range(len(srnames)):
        hData.GetXaxis().SetBinLabel(i+1,srnames[i])

    setDataStyle(hData)
    #hData.Draw("P")
    gData = makeGraph(hData)
    setDataStyle(gData)
    #gData.Draw("SAME P")

    setMCStyle(hTot, "EX")

    hTot.DrawCopy("HIST")
    hBkg.Draw("HIST,same")

    gTot=ROOT.TGraphAsymmErrors(hTot)

    if doPlotAsymUnc and not fitted:
        setAsymmetricUnc(gTot)

        gTot.Draw("E2")

    else:
        hTot.Draw("SAME E2")

    gDataW = makeWhiteCopy(gData)
    #gDataW.Draw("SAME P")
    gData.Draw("SAME P,Z")

    leg = makeLegend(3)

    leg.SetTextFont(42)
    leg.SetTextSize(0.048)

    leg.AddEntry(hData,"Data",    "pe")
    leg.AddEntry(hTot, "Total uncertainty","f")
    bkgSize = len(bkgList())
    for i in range(bkgSize):
        leg.AddEntry(bkgHist[bkgSize-i-1], bkgList()[bkgSize-i-1].getLegendName(),"f")
    leg.Draw("same")
  
    drawATLASlabel(0.115,0.85,"ATLAS",ATLASlabel,luminosity)
    ROOT.gPad.RedrawAxis()

    if ratio:
        p2.cd()
        p2.SetGridx()
        p2.SetGridy()

        if doSig:

            #hSig  = ROOT.TH1F("hTot", "hSig",  NSR, 0, NSR)       
            hSig = makeSignificancePlot(hData,gTot)
     
            setSignificanceStyle(hSig)

            for i in range(len(srnames)):
                hSig.GetXaxis().SetBinLabel(i+1,srnames[i])

            hSig.Draw("HIST")


        else:

            hRatio = makeRatioPlotHisto(hData,hTot)
            setRatioStyle(hRatio,0,2)
            #hRatio.Draw("P")
            gRatio = makeRatioPlotGraph(gData,hTot)
            setRatioStyle(gRatio,0,2)
            #gRatio.Draw("P SAME")

            hRatioErrEX = makeRatioError(hTot)
            hRatioErrTH = makeRatioError(hTot)

            gRatioErrEX = makeRatioPlotGraph(gTot,hTot,True)

            setMCStyle(hRatioErrEX, "Ratio")
            #setMCStyle(hRatioErrTH, "TH")
    
            setMCStyleRatio(hRatioErrEX,0.0001,1.9999)
            setMCStyleRatio(gRatioErrEX,0.0001,1.9999)
            setErrorUncertaintyStyle(gRatioErrEX)
        
            #hRatioErrTH.Draw("SAME E2")
            hRatioErrEX.Draw("HIST")
            gRatioErrEX.Draw("SAME E2")

            for i in range(len(srnames)):
                hRatioErrEX.GetXaxis().SetBinLabel(i+1,srnames[i])

            gRatio.Draw("SAME PZ")

            setLine(NSR)

        ROOT.gPad.SetTicks()
        ROOT.gPad.RedrawAxis()

    plotName=name
    if doSig: plotName=name+"_sig"
    
    c.Print("{0}.C".format(plotName))
    c.Print("{0}.pdf".format(plotName))
    c.Print("{0}.eps".format(plotName))
    c.Print("{0}.png".format(plotName))

    print bold("-- Created {0}.C".format(plotName))
    print bold("-- Created {0}.pdf".format(plotName))
    return


def makeSignificancePlot(hData, gBkg):
    h = hData.Clone("Ratio_"+hData.GetName()+"_"+gBkg.GetName())
    h.Reset()

    for i in range(h.GetNbinsX()):

        s=hData.GetBinContent(i+1)

        x = ROOT.Double(0.)
        y = ROOT.Double(0.)
        gBkg.GetPoint(i, x, y)
 
        eU=gBkg.GetErrorYhigh(i)
        eL=gBkg.GetErrorYlow(i)

        e=eU
        if eL>eU:
            e=eL

        sig=GetSignificance(s,y,e)       

        h.SetBinContent(i+1,sig)

        print "Significance for SR : ",i+1,", sig:",sig


    return h


def setSignificanceStyle(h):

    h.GetXaxis().SetLabelSize(0.16)
    h.GetXaxis().SetLabelOffset(0.04)
    h.GetYaxis().SetLabelSize(0.12)
    h.GetYaxis().SetTitle("Significance")
    h.GetYaxis().SetTitleSize(0.12)
    h.GetYaxis().SetTitleOffset(0.26)
    h.GetYaxis().SetRangeUser(-5,5)
    h.GetYaxis().SetNdivisions(406) #6
    h.GetYaxis().CenterTitle()
    h.SetFillColor(2)
    h.SetFillStyle(3001)
    h.SetLineColor(1)
    h.SetLineWidth(2)
    h.SetMarkerSize(0)


def GetSignificance(n,bkg,errBkg):
    '''
    As recommended by Statistics Forum
    '''

    sigma2=errBkg*errBkg
    bkg2=bkg*bkg

    f1=n*log(n*(bkg+sigma2)/(bkg2+n*sigma2))

    f2=(bkg2/sigma2)*log((bkg2+n*sigma2)/(bkg*(bkg+sigma2)))

    sig=sqrt(2*(f1-f2))

    if n<bkg: sig=-sig

    return sig

def makeLegend(col):
    l = ROOT.TLegend(0.41, 0.64, 0.9, 0.90)
    l.SetNColumns(col)
    l.SetBorderSize(0)
    l.SetTextFont(42)
    l.SetTextSize(0.045)
    l.SetFillColor(0)
    l.SetFillStyle(0)
    l.SetLineColor(0)
    return l

                
def addStats(error, srname, bname, msg=False):
    if msg: print "addStats :: SR={0} \t Bkg={1} \t SysErr={2}".format(srname, bname, error)

    totErr2 = error*error
    totErr2 += AsymmetricUnc[srname][bname]['stat']**2

    totErr = ROOT.TMath.Sqrt(totErr2)

    if msg: print "addStats :: Updated error {0}".format(totErr)
    return totErr

def readWorkspace():

    '''
    This method reads the workspace created by HistFitter and return
    the yields, statistical and asymmetric systematics uncertainties, 
    always *before* fit.

    '''
    print bold("Starting to read workspace from HistFitter")


    jobPrefix = os.getenv("HFRUNDIR")+"/data/bkgOnly_nom"+runNameTag+lumiTag+"_"+syst+"_"
    jobSuffix =blindTag+"_bkg.root"

    reg=allRegions.getList()
    bkgs=bkgList()


    #initializing dictionary
    global AsymmetricUnc

    
    local_dict={"Total":{}}
    
    for i in range(len(bkgList())):
        local_dict[bkgList()[i].getName()]={}

    for i in range(len(reg)):
        AsymmetricUnc[reg[i]]=local_dict.copy()
   

    #now I will read every ws per SR
    for sr in reg:
        print "- Opening workspace for region: ",sr

        ws = jobPrefix+sr+jobSuffix

        pFile = ROOT.TFile(ws)

        #getting all keys in ws
        histoNames = [key.GetName() for key in pFile.GetListOfKeys()]
        
        #will separate all keys per sample reading the following format  --> h<sample><systematic><High/Low>_<region>_obs_cuts
        #nom --> h<sample>Nom_<region>_obs_cuts

        systTotalList=['Lumi']
        stat2=0

        totalBkg=0

        for i in range(len(bkgList())):
    
            bkgName=bkgList()[i].getName()

            print "-- Looking for histos for bkg :",bkgName

            systListSample={'High':{},'Low':{}}

            for histoName in histoNames:

                histo=pFile.Get(histoName)

                err=ROOT.Double(0.0)

                val=histo.IntegralAndError(1,histo.GetNbinsX(),err)

                if histoName=="hData_"+sr+"_obs_cuts":

                    allRegions.setObserved(sr,val)
                    print bold("-- Getting observed yield in region {0} : {1}".format(sr,val))

                #saving nominal
                elif histoName=='h'+bkgName+'Nom_'+sr+"_obs_cuts":

                    bkgList()[i].setYieldAndStatistical(sr,val,err)              
                    stat2 += err**2
                    totalBkg += val

                                        
                #otherwise it is a systematic:
                elif ("h"+bkgName in histoName and "_"+sr+"_obs_cuts" in histoName):

                    #extracting string
                    pref = "h"+bkgName
                    suf = "_"+sr+"_obs_cuts"

                    foundSuf=histoName.find(suf)                          

                    systName=histoName[len(pref):foundSuf]

                    localSyst=None
                    direction=None
                 
                    if 'High'==systName[-4:]:
                        localSyst=systName[:-4]
                        direction='High'

                    elif 'Low'==systName[-3:]:
                        localSyst=systName[:-3]
                        direction='Low'

                    if localSyst is not None: 
                        systListSample[direction][localSyst]=val
              
                        if localSyst not in systTotalList:
                            systTotalList.append(localSyst)


            #adding lumi (not included in the histograms from workspace)
            if bkgList()[i].getIsMC():
                systListSample['High']['Lumi']=(1+luminosityError)*bkgList()[i].getYield(sr)
                systListSample['Low']['Lumi']=(1-luminosityError)*bkgList()[i].getYield(sr)
                            
            systSample=pd.DataFrame(systListSample)

            bkgList()[i].setSystematics(sr,systSample)

            up, down, sym = bkgList()[i].getUpAndDown(sr)

            AsymmetricUnc[sr][bkgList()[i].getName()] = {'yield':bkgList()[i].getYield(sr),'stat':bkgList()[i].getStatistical(sr),'up':up,'down':down,'sym':sym}
                                                     

            print bkgList()[i].getYield(sr), " +", up, " -",down

        #now compute total uncertainty taking into account correlations
        systTotal={'sigUp':{},'sigDown':{}}

        for systName in systTotalList:

            systTotal["sigUp"][systName]=0
            systTotal["sigDown"][systName]=0

            for i in range(len(bkgList())):

                if systName in bkgList()[i].getSystematicDF(sr).index:             
                    systTotal['sigUp'][systName] += bkgList()[i].getSystematicDF(sr).loc[systName,'sigUp']
                    systTotal['sigDown'][systName] += bkgList()[i].getSystematicDF(sr).loc[systName,'sigDown'] 


            

        systTotalDF = pd.DataFrame(systTotal)

        systTotalDF['sigUp2'] = systTotalDF['sigUp']**2
        systTotalDF['sigDown2'] = systTotalDF['sigDown']**2
        systTotalDF['symmetric'] = abs(0.5*(systTotalDF['sigUp']+systTotalDF['sigDown']))
        systTotalDF['symmetric2'] = systTotalDF['symmetric']**2

        up = sqrt(systTotalDF['sigUp2'].sum() + stat2)
        down = sqrt(systTotalDF['sigDown2'].sum() + stat2)
        symSyst = sqrt(systTotalDF['symmetric2'].sum() +stat2)

        print "Total : ", up,  " ",down 
        AsymmetricUnc[sr]["Total"] = {'yield':totalBkg,'stat':sqrt(stat2),'up':up,'down':down,'sym':symSyst}
        AsymmetricUnc[sr]["observed"]=allRegions.getObserved(sr)

        if debug: print AsymmetricUnc

        with open(FileAsymmetricUnc,'w') as fp:
            json.dump(AsymmetricUnc,fp,sort_keys=True,indent=4)



    return

def readSystematicsFromFile():

    ''' 
    This method will read the yields and uncertainties stored in a json file
    previosly crated with this macro. It will run faster
    '''

    if not os.path.exists(FileAsymmetricUnc):
        print red("{0} not found. Returning original error".format(FileAsymmetricUnc)); return error

    global AsymmetricUnc

    with open(FileAsymmetricUnc) as json_file:
        AsymmetricUnc = json.load(json_file)


    print("Getting total asymmetric uncertainties: ")
    if debug: print AsymmetricUnc


    return

def setAsymmetricUnc(h):

    reg=allRegions.getList()

    for i in range(len(reg)):
        h.SetPointEYhigh(i,AsymmetricUnc[reg[i]]["Total"]['up'])
        h.SetPointEYlow(i,AsymmetricUnc[reg[i]]["Total"]['down'])


    return

def setDataStyle(h):
    h.GetXaxis().SetLabelSize(0.05)
    h.GetXaxis().SetLabelOffset(0.2)
    h.GetYaxis().SetLabelSize(0.04)
    h.GetYaxis().SetTitle("Events")
    h.GetYaxis().SetTitleSize(0.06)
    h.GetYaxis().SetTitleOffset(0.6)
    h.SetMarkerColor(ROOT.kBlack)
    h.SetLineColor(ROOT.kBlack)
    h.SetMarkerStyle(20);
    h.SetMarkerSize(1.2)
    h.SetLineWidth(1)
    return


def setMCStyleRatio(h,ymin,ymax):

    h.GetXaxis().SetLabelSize(0.16)
    h.GetXaxis().SetLabelOffset(0.04)
    h.GetYaxis().SetLabelSize(0.12)
    h.GetYaxis().SetTitle("Data/SM")
    h.GetYaxis().SetTitleSize(0.12)
    h.GetYaxis().SetTitleOffset(0.26)
    h.GetYaxis().SetRangeUser(ymin,ymax)
    h.GetYaxis().SetNdivisions(404) #6
    h.GetYaxis().CenterTitle()

    return

def setMCStyle(h,Type):

    h.GetXaxis().SetLabelOffset(0.2)
    h.GetYaxis().SetLabelSize(0.07)
    h.GetYaxis().SetTitle("Events")
    h.GetYaxis().SetTitleSize(0.08)
    h.GetYaxis().SetTitleOffset(0.45)  
    h.GetXaxis().SetNdivisions(1)

    if Type=="EX":
        print 'Setting MC FOR TOTAL MS'
        h.SetLineColor(ROOT.kGray+1)
        h.SetFillColor(ROOT.kGray+1)
        h.SetFillStyle(3254)

    if Type=="Ratio":
        print 'Setting MC FOR TOTAL MS'
        h.SetLineColor(0)
        h.SetFillColor(0)

    if Type=="TH":
        h.SetLineColor(ROOT.kYellow-9)
        h.SetFillColor(ROOT.kYellow-9)
        h.SetFillStyle(1111)
    h.SetLineWidth(1)
    h.SetMarkerSize(0)
    return


def setErrorUncertaintyStyle(g):

    g.SetLineColor(ROOT.kGray+1)
    g.SetFillColor(ROOT.kGray+1)
    g.SetFillStyle(3254)

    return
def setRatioStyle(h,ymin,ymax):
    h.GetXaxis().SetLabelSize(0.16)
    h.GetXaxis().SetLabelOffset(0.04)
    h.GetYaxis().SetLabelSize(0.1)
    h.GetYaxis().SetTitle("Data/SM")
    h.GetYaxis().SetTitleSize(0.11)
    h.GetYaxis().SetTitleOffset(0.23)
    h.GetYaxis().SetRangeUser(ymin,ymax)
    h.GetYaxis().SetNdivisions(6)
    h.SetMarkerColor(ROOT.kBlack)
    h.SetLineColor(ROOT.kBlack)
    h.SetMarkerStyle(20)
    h.SetMarkerSize(1.2)
    h.SetLineWidth(1)
    return
                                            

def makeWhiteCopy(h):
    copy = h.Clone(h.GetName()+"_white")
    copy.SetLineColor(ROOT.kWhite)
    copy.SetMarkerColor(ROOT.kWhite)
    copy.SetMarkerSize(1.1)
    copy.SetLineWidth(2)
    return copy

def makeRatioPlotHisto(h1, h2):
    h = h1.Clone("Ratio_"+h1.GetName()+"_"+h2.GetName())
    h.Reset()
    for i in range(h.GetNbinsX()):
        r = h1.GetBinContent(i+1) / h2.GetBinContent(i+1) if h2.GetBinContent(i+1)>0 else 0
        e = h1.GetBinError(i+1) / h1.GetBinContent(i+1) if h1.GetBinContent(i+1)>0 else 0
        h.SetBinContent(i+1,r)
        h.SetBinError(i+1,e)
    return h


def makeRatioPlotGraph(g, h,MC=False):
    gR = ROOT.TGraphAsymmErrors()
    gR.SetName("Ratio_{0}_{1}".format(g.GetName(),h.GetName()))
    for i in range(g.GetN()):
        if not h.GetBinContent(i+1): continue
        x = ROOT.Double(0.) 
        y = ROOT.Double(0.)
        g.GetPoint(i, x, y)

        r  = y / h.GetBinContent(i+1) 
        eL = g.GetErrorYlow(i) / h.GetBinContent(i+1)
        eU = g.GetErrorYhigh(i) / h.GetBinContent(i+1)

        eX=0

        if MC:
            eX=g.GetErrorXlow(i)

        gR.SetPoint(i, x, r)
        gR.SetPointError(i,eX,eX, eL, eU)
    return gR

def makeRatioError(h):
    hErr = h.Clone("RatioErr_"+h.GetName())
    hErr.Reset()
    for i in range(hErr.GetNbinsX()):
        e = h.GetBinError(i+1) / h.GetBinContent(i+1) if h.GetBinContent(i+1)>0 else 0
        hErr.SetBinContent(i+1,1)
        hErr.SetBinError(i+1,e)
    return hErr

def setLine(xmax):
    line = ROOT.TLine()
    line.SetLineColor(ROOT.kBlue+1)
    line.SetLineStyle(1)
    line.SetLineWidth(1)
    line.DrawLine(0, 1., xmax, 1.)
    return

def makeGraph(h):
    g = ROOT.TGraphAsymmErrors()
    g.SetName("Graph_{0}".format(h.GetName()))
    for i in range(h.GetNbinsX()):
        x = h.GetBinCenter(i+1)
        y = h.GetBinContent(i+1)

        eL = ROOT.Double(0)
        eU = ROOT.Double(0)
        ROOT.RooHistError.instance().getPoissonInterval(int(y),eL,eU,int(1))
        eL=y-eL
        eU=eU-y

        g.SetPoint(i, x, y)
        g.SetPointError(i,0,0, eL, eU)
        #g.SetPointError(i, h.GetBinWidth(i+1)/2., h.GetBinWidth(i+1)/2., eL, eU)
        print "--> DataPoint({0}) :: Obs={1:.1f}  \t errLow={2:.3f}, errUp={3:.3f}".format(i, y, eL, eU)
    return g

def drawATLASlabel(x,y,label1,label2,lumi):
    n = ROOT.TLatex()
    n.SetNDC()
    n.SetTextColor(ROOT.kBlack)
    n.SetTextFont(72)
    n.SetTextSize(0.07)
    n.DrawLatex(x,y,label1)
    n.SetTextFont(42)
    n.DrawLatex(x+0.08,y,label2)
    n.SetTextFont(42)
    n.DrawLatex(x,y-0.08,"#sqrt{s} = 13 TeV, %s fb^{-1}" % (lumi))
    #n.DrawLatex(x+0.20,y,"#sqrt{s} = 13 TeV, %s fb^{-1}" % (lumi))
    return

def keyBkgTot(f): 
    if f: return 'TOTAL_FITTED_bkg_events'
    else: return 'TOTAL_MC_EXP_BKG_events'
 
def keyErrTot(f): 
   if f: return 'TOTAL_FITTED_bkg_events_err'
   else: return 'TOTAL_MC_EXP_BKG_err'

def keyBkg(f):
    if f: return 'Fitted_events_'
    else: return 'MC_exp_events_'

def keyErr(f):
    if f: return 'Fitted_err_'
    else: return 'MC_exp_err_'
    
def green(msg): return "\033[0;32m{0}\033[0m".format(msg);
def red(msg): return "\033[0;31m{0}\033[0m".format(msg);
def bold(msg): return "\033[1m{0}\033[0m".format(msg);

    
if __name__ == "__main__":
    main()

