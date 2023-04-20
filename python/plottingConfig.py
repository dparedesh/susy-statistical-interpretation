import  ROOT
from array import array
import pandas as pd
import pathUtilities

class Limit:

    def __init__(self,label,arrayX,arrayY):
        self.legend=label

        self.plot=ROOT.TGraph(len(arrayX),array('f',arrayX),array('f',arrayY))
      

class Model:

    def __init__(self,string_input):
        self.modelName=string_input

        self.xMin = 800
        self.xMax = 2000
        self.nsY = 24
        self.yMin = 0
        self.yMax = 900
   
        self.h_xMin = None
        self.h_xMax = None    
        self.h_yMin = None
        self.h_yMax = None

        self.yMinLine =0
        self.yMaxLine =0
        self.xMinLine =0
        self.xMaxLine =0
        self.valLinesX = 0
        self.valLinesY = 0
        self.useForbiddenRegion=False

        self.xLabel=''
        self.yLabel=''
        self.processDescription=''

        self.forbiddenFunction=None
        self.forbiddenCut = 0
        self.forbiddenLabelX = 0
        self.forbiddenLabelY = 0
        self.forbiddenLabelText = "None"
        self.extraText=None
        self.update()

        self.previousLimits={}
        self.theoryLegend=None

    def setXrange(self,xMin,xMax):
        self.xMin = xMin
        self.xMax = xMax

        self.update()

    def setYrange(self,yMin,yMax):
        self.yMin = yMin
        self.yMax = yMax

        self.update()

    def getRangeForContours(self):
        x1 = self.h_xMin
        x2 = self.h_xMax
        y1 = self.h_yMin
        y2 = self.h_yMax

        return x1,x2,y1,y2

    def setRangeForContours(self,xmin,xmax,ymin,ymax):
        self.h_xMin = str(xmin)
        self.h_xMax = str(xmax)
        self.h_yMin = str(ymin)
        self.h_yMax = str(ymax)

    def setValLines(self,valX,valY,useForbiddenRegion=False):
        self.valLinesX = valX
        self.valLinesY = valY
        self.useForbiddedRegion = useForbiddenRegion

        self.update()

    def setLabels(self,xLabel,yLabel,process):
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.processDescription = process

    def setExtraText(self,text):
        self.extraText=text

    def setTheoryLegend(self,text):
        self.theoryLegend=text

    def setForbiddenCutsAndLabels(self,forbiddenCut,xLabel,yLabel,labelTex,forbiddenFunction=None):
        self.forbiddenCut = forbiddenCut
        self.forbiddenLabelX = xLabel
        self.forbiddenLabelY = yLabel
        self.forbiddenLabelText = labelTex

        if forbiddenFunction is not None: self.forbiddenFunction = forbiddenFunction
        else:
            cut=-1*float(forbiddenCut)
            forbiddenFunction = "x"

            if cut < 0: forbiddenFunction= "x-"+str(abs(cut))
            elif cut > 0: forbiddenFunction= "x+"+str(cut)

            self.forbiddenFunction = forbiddenFunction

        self.update()

    def update(self):

        self.xMinLine = self.yMin + self.forbiddenCut
        self.xMaxLine = self.yMax + self.forbiddenCut
        self.yMinLine = self.xMin - self.forbiddenCut
        self.yMaxLine = self.xMax - self.forbiddenCut
        if self.xMinLine < self.xMin:
            self.xMinLine = self.xMin
        if self.yMinLine < self.yMin:
            self.yMinLine = self.yMin
        if self.xMaxLine > self.xMax:
            self.xMaxLine = self.xMax
        if self.yMaxLine > self.xMax:
            self.yMaxLine = self.yMax

        self.xMinLabel = self.xMinLine
        self.xMaxLabel = self.xMaxLine
        self.yMinLabel = self.yMinLine
        self.yMaxLabel = self.yMaxLine

        m = (self.yMaxLine-self.yMinLine)/(self.xMaxLine- self.xMinLine)
        q = self.yMinLine-m*self.xMinLine

        self.xMaxLine = self.valLinesX

        if self.useForbiddenRegion:
            self.yMaxLine = self.valLinesY - self.forbiddenCut
        else:
            self.yMaxLine = m*self.valLinesY + q

    def setPreviousLimit(self,tag,label,hepData,line=False,f=1):

        hep=pd.read_csv(hepData,comment="#")
        hep.columns=['x','y']

        localX=list(hep['x'])
        localY=list(hep['y'])
        # need to append min values in X and Y so that shaded area is well done
        if line==False:
            localX.append(self.xMin)  
            localY.append(self.yMin)
        else:#  if plotting x-section as a function of generated mass, then convert xsec to the desired unit using 'f' 
            temp = localY[:]
            localY = [ xs*f for xs in temp]

        lim=Limit(label,localX,localY)

        self.previousLimits[tag]=lim
    

modelDict={}


###############################################
Mc16SusyBtt = Model("SusyBtt")

Mc16SusyBtt.setXrange(600,1100)
Mc16SusyBtt.setYrange(50,1100)
Mc16SusyBtt.setValLines(950,950,True)
Mc16SusyBtt.setRangeForContours(500,1100,30,1100)

Mc16SusyBtt.setLabels('m(#tilde{b}_{1}) [GeV]',
                      'm(#tilde{#chi}^{0}_{1}) [GeV]',
                      '#tilde{b}_{1} #tilde{b}_{1} production, #tilde{b}_{1}#rightarrow t#tilde{#chi}^{#pm}_{1}, m(#tilde{#chi}^{#pm}_{1}) = m(#tilde{#chi}^{0}_{1}) + 100 GeV')

Mc16SusyBtt.setForbiddenCutsAndLabels(272.5, # 172.5+100 just to make a better plot
                700, 480, "m(#tilde{b}_{1}) <  m(t) + m(#tilde{#chi}^{0}_{1}) + 100 GeV")


Mc16SusyBtt.setPreviousLimit("36fb","#splitline{SS/3L obs. 36 fb^{-1}}{[arXiv:1706.03731]}",pathUtilities.pythonDirectory()+'/HEPData/Mc16SusyBtt_36ifb.csv')


modelDict["Mc16SusyBtt"]=Mc16SusyBtt


#############################################
Mc16SusyGtt = Model("SusyGtt")

Mc16SusyGtt.setXrange(1100,2200)
Mc16SusyGtt.setYrange(0,2200)
Mc16SusyGtt.setValLines(2200,2200)

Mc16SusyGtt.setLabels('m_{#tilde{g}} [GeV]',
        'm_{#tilde{#chi}^{0}_{1}} [GeV]',
        '#tilde{g} #tilde{g} production, #tilde{g}#rightarrow t#bar{t}#tilde{#chi}^{0}_{1}, m(#tilde{t_{1}}) >> m(#tilde{g})')

Mc16SusyGtt.setForbiddenCutsAndLabels(345,#2*172.5
                1400, 1100, "m_{#tilde{g}} <  2 m_{t} + m_{#tilde{#chi}^{0}_{1}} ")


modelDict["Mc16SusyGtt"]=Mc16SusyGtt


###########################################
Mc16SusyComprGtt = Model("SusyComprGtt")

Mc16SusyComprGtt.setXrange(750,2000)
Mc16SusyComprGtt.setYrange(5,150)
Mc16SusyComprGtt.setValLines(2000,650)

Mc16SusyComprGtt.setLabels('m_{#tilde{g}} [GeV]',
        '#Deltam_{#tilde{#chi}^{0}_{1}} = m_{#tilde{#chi}^{0}_{1}} + 2m_{t} - m_{#tilde{g}} [GeV]',
        '#tilde{g} #tilde{g} production, #tilde{g}#rightarrow t#bar{t}#tilde{#chi}^{0}_{1}')

Mc16SusyComprGtt.setForbiddenCutsAndLabels(160, #2*80
                810, 690, "m_{#tilde{g}} <  2 m_{W} + m_{#tilde{#chi}^{0}_{1}} ")



modelDict["Mc16SusyComprGtt"]=Mc16SusyComprGtt
################################################
Mc16SusyGSL = Model("SusyGSL")

Mc16SusyGSL.setXrange(600,2200)
Mc16SusyGSL.setYrange(200,2200)
Mc16SusyGSL.setValLines(1600,1600)

Mc16SusyGSL.setLabels('m_{#tilde{g}} [GeV]',
            'm_{#tilde{#chi}^{0}_{1}} [GeV]',
            "#tilde{g} #tilde{g} production, #tilde{g} #rightarrow qq(ll/#nu#nu)#tilde{#chi}^{0}_{1}; m(#tilde{#chi}^{0}_{2}) = (m(#tilde{g}) + m(#tilde{#chi}^{0}_{1}))/2, m(#tilde{l},#tilde{#nu}) = (m(#tilde{#chi}^{0}_{2}) + m(#tilde{#chi}^{0}_{1}))/2")


Mc16SusyGSL.setForbiddenCutsAndLabels(0,
                    800, 850, "m(#tilde{g}) <  m(#tilde{#chi}^{0}_{1}) ")


modelDict["Mc16SusyGSL"]=Mc16SusyGSL

###################################################

Mc16SusyGG2StepWZ = Model("SusyGG2StepWZ")

Mc16SusyGG2StepWZ.setXrange(1000,2300)
Mc16SusyGG2StepWZ.setYrange(100,2600)
Mc16SusyGG2StepWZ.setValLines(2100,2100,True)

Mc16SusyGG2StepWZ.setLabels("m(#tilde{g}) [GeV]",
        "m(#tilde{#chi}^{0}_{1}) [GeV]",
        "#tilde{g} #tilde{g} production, #tilde{g} #rightarrow qq'WZ#tilde{#chi}^{0}_{1}; m(#tilde{#chi}^{#pm}_{1}) = (m(#tilde{g}) + m(#tilde{#chi}^{0}_{1}))/2, m(#tilde{#chi}^{0}_{2}) = (m(#tilde{#chi}^{#pm}_{1}) + m(#tilde{#chi}^{0}_{1}))/2")

Mc16SusyGG2StepWZ.setForbiddenCutsAndLabels(320,#4*80
                     1400, 1150, "#Delta m(#tilde{#chi}_{1}^{#pm},#tilde{#chi}_{2}^{0}) < m(W), #Delta m(#tilde{#chi}_{2}^{0},#tilde{#chi}_{1}^{0}) < m(Z)",'x')


Mc16SusyGG2StepWZ.setPreviousLimit("36fb",
				"#splitline{SS/3L obs. 36 fb^{-1}}{[arXiv:1706.03731]}",pathUtilities.pythonDirectory()+'/HEPData/Mc16SusyGG2StepWZ_36ifb.csv')


modelDict["Mc16SusyGG2StepWZ"]=Mc16SusyGG2StepWZ

###################################################
Mc16SusyGG_Rpv331 = Model("SusyGG_Rpv331")

Mc16SusyGG_Rpv331.setXrange(600,2300)
Mc16SusyGG_Rpv331.setYrange(400,2100)
Mc16SusyGG_Rpv331.setValLines(1400,1400,True)

Mc16SusyGG_Rpv331.setLabels('m(#tilde{g}) [GeV]',
            'm(#tilde{t}) [GeV]',
            "#tilde{g} #tilde{g} production, #tilde{g} #rightarrow #tilde{t} #bar{t}, #tilde{t} #rightarrow #bar{b} #bar{d}")

#setForbiddenCutsAndLabels(self,forbiddenCut,xLabel,yLabel,labelTex,forbiddenFunction=None)
Mc16SusyGG_Rpv331.setForbiddenCutsAndLabels(172.5, #172.5
                         1000, 870, "m(#tilde{g}) <  m(#tilde{t}) + m(t) ")


#Mc16SusyGG_Rpv331.setPreviousLimit("36fb","#splitline{SS/3L obs. 36 fb^{-1}}{[arXiv:1706.03731]}",pathUtilities.pythonDirectory()+"/HEPData/Mc16Susy_Rpv331_36ifb.csv")
Mc16SusyGG_Rpv331.setPreviousLimit("139fb","#splitline{SS/3L obs. 139 fb^{-1}}{[arXiv:1909.08457]}",pathUtilities.pythonDirectory()+"/HEPData/Mc16Susy_Rpv331_139ifb.csv")

modelDict["Mc16SusyGG_Rpv331"]=Mc16SusyGG_Rpv331

###################################################
Mc16SusyGG_Rpv321 = Model("SusyGG_Rpv321")

Mc16SusyGG_Rpv321.setXrange(800,1600)
Mc16SusyGG_Rpv321.setYrange(400,1600)
Mc16SusyGG_Rpv321.setValLines(1400,1400)

Mc16SusyGG_Rpv321.setLabels('m_{#tilde{g}} [GeV]',
            'm_{#tilde{t}} [GeV]',
            "#tilde{g} #tilde{g} production, #tilde{g} #rightarrow #tilde{t} #bar{t}, #tilde{t} #rightarrow #bar{d} #bar{s}")

Mc16SusyGG_Rpv321.setForbiddenCutsAndLabels(0,
                         700, 640, "m_{#tilde{d}} =  m_{#tilde{g}} ")


modelDict["Mc16SusyGG_Rpv321"]=Mc16SusyGG_Rpv321

###################################################
Mc16SusyTT2Step = Model("SusyTT2Step")

Mc16SusyTT2Step.setXrange(550,950)
Mc16SusyTT2Step.setYrange(8E-3,4)
Mc16SusyTT2Step.setValLines(1400,1400)

Mc16SusyTT2Step.setLabels('m(#tilde{t}_{1}) [GeV]',
            '#sigma [pb]',
            "#tilde{t}_{1}#tilde{t}_{1} production, #tilde{t}_{1} #rightarrow tW^{#pm}#tilde{#chi}^{#pm}_{1}, #tilde{#chi}^{#pm}_{1} #rightarrow W*#tilde{#chi}^{0}_{1}; m(#tilde{#chi}^{0}_{1}) = m(#tilde{t}_{1})-275 GeV ; m(#tilde{#chi}^{0}_{2})=m(#tilde{#chi}^{0}_{1})+100 GeV ; m(#tilde{#chi}^{#pm}_{1}) #approx m(#tilde{#chi}^{0}_{1})")

Mc16SusyTT2Step.setPreviousLimit("36fb","#splitline{SS/3L obs. 36 fb^{-1}}{[arXiv:1706.03731]}",pathUtilities.pythonDirectory()+"/HEPData/Mc16SusyTT2Step_36ifb.csv",line=True,f=0.001)

Mc16SusyTT2Step.setExtraText("#bf{BR(#tilde{t}_{1}#rightarrow tW^{#pm}(W*)#tilde#chi_{1}^{0})=100%}")

Mc16SusyTT2Step.setTheoryLegend("pp #rightarrow #tilde{t}_{1} #tilde{t}_{1}")

modelDict["Mc16SusyTT2Step"]=Mc16SusyTT2Step

###################################################
Mc16SusyGG_RpvLQD = Model("SusyGG_RpvLQD")

Mc16SusyGG_RpvLQD.setXrange(1000,3000)
Mc16SusyGG_RpvLQD.setYrange(50,3300)
Mc16SusyGG_RpvLQD.setValLines(2000,2000)

Mc16SusyGG_RpvLQD.setForbiddenCutsAndLabels(0,
                         1300, 1400, "m_{#tilde{g}} <  m_{#tilde{#chi}^{0}_{1}} ")

Mc16SusyGG_RpvLQD.setLabels('m_{#tilde{g}} [GeV]',
            'm_{#tilde{#chi}^{0}_{1}} [GeV]',
            "#tilde{g} #tilde{g} production, #tilde{g} #rightarrow qq#tilde{#chi}^{0}_{1}, #tilde{#chi}^{0}_{1} #rightarrow lqq")

Mc16SusyGG_RpvLQD.setPreviousLimit("36fb","SS/3L obs. 36 fb^{-1}",pathUtilities.pythonDirectory()+"/HEPData/Mc16SusyGG_RpvLQD_36ifb.csv")

modelDict["Mc16SusyGG_RpvLQD"]=Mc16SusyGG_RpvLQD

#################################################
Mc16SusyC1N2WZonshell = Model("Mc16SusyC1N2_onshellWZ")

Mc16SusyC1N2WZonshell.setXrange(100,600)
Mc16SusyC1N2WZonshell.setYrange(0,600)
Mc16SusyC1N2WZonshell.setValLines(450,450,True)
Mc16SusyC1N2WZonshell.setRangeForContours(100,400,0,600)
Mc16SusyC1N2WZonshell.setLabels('m(#tilde{#chi}^{#pm}_{1}/#tilde{#chi}^{0}_{2}) [GeV]', 'm(#tilde{#chi}^{0}_{1}) [GeV]', '#tilde{#chi}^{#pm}_{1}#tilde{#chi}^{0}_{2} #rightarrow #tilde{#chi}^{0}_{1}#tilde{#chi}^{0}_{1}WZ(on-shell) production')

Mc16SusyC1N2WZonshell.setForbiddenCutsAndLabels(91, 250,180,'#Delta m(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1}) < m(W), #Delta m(#tilde{#chi}^{0}_{2},#tilde{#chi}^{0}_{1})<m(Z)')

modelDict["Mc16SusyC1N2_onshellWZ"]=Mc16SusyC1N2WZonshell

#################################################
Mc16SusyC1N2WZoffshell = Model("Mc16SusyC1N2_offshellWZ")

Mc16SusyC1N2WZoffshell.setXrange(100,600)
Mc16SusyC1N2WZoffshell.setYrange(0,600)
Mc16SusyC1N2WZoffshell.setValLines(350,350,True)
Mc16SusyC1N2WZoffshell.setRangeForContours(100,100,0,350)
Mc16SusyC1N2WZoffshell.setLabels('m(#tilde{#chi}^{#pm}_{1}/#tilde{#chi}^{0}_{2}) [GeV]','m(#tilde{#chi}^{0}_{1}) [GeV]','#tilde{#chi}^{#pm}_{1}#tilde{#chi}^{0}_{2} #rightarrow #tilde{#chi}^{0}_{1}#tilde{#chi}^{0}_{1}WZ production')
Mc16SusyC1N2WZoffshell.setForbiddenCutsAndLabels(191,250,180,'#Delta m(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1}) < m(W), #Delta m(#tilde{#chi}^{0}_{2},#tilde{#chi}^{0}_{1})<m(Z)')
modelDict["Mc16SusyC1N2_offshellWZ"]=Mc16SusyC1N2WZoffshell


#################################################
Mc16SusyC1N2WZ = Model("Mc16SusyC1N2_allWZ")

Mc16SusyC1N2WZ.setXrange(100,600)
Mc16SusyC1N2WZ.setYrange(0,600)
Mc16SusyC1N2WZ.setValLines(500,500,True)
Mc16SusyC1N2WZ.setRangeForContours(100,600,0,600)
Mc16SusyC1N2WZ.setLabels('m(#tilde{#chi}^{#pm}_{1}/#tilde{#chi}^{0}_{2}) [GeV]','m(#tilde{#chi}^{0}_{1}) [GeV]','#tilde{#chi}^{#pm}_{1}#tilde{#chi}^{0}_{2} #rightarrow #tilde{#chi}^{0}_{1}#tilde{#chi}^{0}_{1}WZ production')
Mc16SusyC1N2WZ.setForbiddenCutsAndLabels(0,200,200,'#Delta m(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1}) < 0',forbiddenFunction='x')
modelDict["Mc16SusyC1N2_allWZ"]=Mc16SusyC1N2WZ


###################################################
Mc16SusyC1N2N1_GGMHinoZh = Model("Mc16SusyC1N2N1_GGMHinoZh")
Mc16SusyC1N2N1_GGMHinoZh.setXrange(200,900)
Mc16SusyC1N2N1_GGMHinoZh.setYrange(0,100)
Mc16SusyC1N2N1_GGMHinoZh.setForbiddenCutsAndLabels(0,0,0,'',forbiddenFunction='500')
Mc16SusyC1N2N1_GGMHinoZh.setLabels('m(#tilde{#chi}^{#pm}_{1}/#tilde{#chi}^{0}_{2}/#tilde{#chi}^{0}_{1}) [GeV]', 'B(#tilde{#chi}^{#pm}_{1} #rightarrow Z #tilde{G}) %', 'Higgsino m(#tilde{#chi}^{#pm}_{1}/#tilde{#chi}^{0}_{2})/#tilde{#chi}^{0}_{1}), #tilde{#chi}^{0}_{1}) #rightarrow Z/h#tilde{G}')
modelDict['Mc16SusyC1N2N1_GGMHinoZh'] = Mc16SusyC1N2N1_GGMHinoZh


###################################################
Mc16SusySS2StepWZ = Model("SusySS2StepWZ")
Mc16SusySS2StepWZ.setXrange(500,1900)
Mc16SusySS2StepWZ.setYrange(100,2200)
Mc16SusySS2StepWZ.setValLines(1700,1700,True)
#Mc16SusySS2StepWZ.setRangeForContours(500,1500,0,1200)
Mc16SusySS2StepWZ.setLabels("m(#tilde{q}) [GeV]",
        "m(#tilde{#chi}^{0}_{1}) [GeV]",
        "#tilde{q} #tilde{q} production, #tilde{q} #rightarrow q'WZ#tilde{#chi}^{0}_{1}; m(#tilde{#chi}^{#pm}_{1}) = (m(#tilde{q}) + m(#tilde{#chi}^{0}_{1}))/2, m(#tilde{#chi}^{0}_{2}) = (m(#tilde{#chi}^{#pm}_{1}) + m(#tilde{#chi}^{0}_{1}))/2")
Mc16SusySS2StepWZ.setForbiddenCutsAndLabels(320,#4*80
                     1350, 1050, "#Delta m(#tilde{#chi}_{1}^{#pm},#tilde{#chi}_{2}^{0}) < m(W), #Delta m(#tilde{#chi}_{2}^{0},#tilde{#chi}_{1}^{0}) < m(Z)",'x')
#                     900, 950, "m(#tilde{#chi}_{1}^{0}) < m(#tilde{q})",'x')
Mc16SusySS2StepWZ.setPreviousLimit("20.3fb",
                                "#splitline{SS/3L obs. 20.3 fb^{-1}}{[arXiv:1404.2500]}",pathUtilities.pythonDirectory()+'/HEPData/Mc16SusySS2StepWZ_20ifb.csv')
modelDict["Mc16SusySS2StepWZ"]=Mc16SusySS2StepWZ

##############################################
Mc16SusySS2StepSL = Model("SusySS2StepSL")
Mc16SusySS2StepSL.setXrange(600,2600)
Mc16SusySS2StepSL.setYrange(100,2300)
Mc16SusySS2StepSL.setValLines(1800,1600,True)
Mc16SusySS2StepSL.setLabels("m(#tilde{q}) [GeV]",
        "m(#tilde{#chi}^{0}_{1}) [GeV]",
        "#tilde{q} #tilde{q} production, #tilde{q} #rightarrow q#tilde{#chi}^{#pm}_{1}/#tilde{#chi}^{0}_{2} #rightarrow qlv(ll/vv)#tilde{#chi}^{0}_{1}")
Mc16SusySS2StepSL.setForbiddenCutsAndLabels(1,#4*80
                     1000, 1000, "m(#tilde{#chi}_{1}^{0}) < m(#tilde{q})",'x')

Mc16SusySS2StepSL.setPreviousLimit("20.3fb",
                               "#splitline{SS/3L obs. 20.3 fb^{-1}}{[arXiv:1404.2500]}",pathUtilities.pythonDirectory()+'/HEPData/Mc16SusySS2StepSL_20ifb.csv')

modelDict["Mc16SusySS2StepSL"]=Mc16SusySS2StepSL
