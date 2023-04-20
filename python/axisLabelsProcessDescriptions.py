#!/usr/bin/env python
import sys
sys.path.append('python') #this is a hack to import the sameSignTools from /python
import os, pathUtilities
dataDir = os.path.join(pathUtilities.histFitterTopDirectory(), 'susyGridFiles')

#def main():
#    getLabelsPerGrid()

def getLabelsPerGrid():
    import os, sys
    labelsPerGrid = {}
    for file in os.listdir(dataDir):
        if file.startswith('Mc') and 'Susy' in file and 'Susy_missingPoints' not in file\
               and not file.endswith('~') and not file.endswith('.root') and not os.path.isdir(os.path.join(dataDir,file)):
            labelsPerGrid[file] = sameSignLabelsAndAxes(file[4:]) #model name does not depend on mc version.
            labelsPerGrid[file].getLabels()

    return labelsPerGrid

class sameSignLabelsAndAxes():
    def __init__(self, gridName):
        self.gridName = gridName
        self.processDescription = ""
        self.xLabel = ""
        self.yLabel = ""

        self.forbiddenCut = 0
        self.forbiddenLabelXVal = 0
        self.forbiddenLabelYVal = 0
        self.forbiddenLabelText = "None"

    def getLabels(self):
        processDescriptionAndAxisLabels = getProcessDescriptionAndAxisLabels()
        forbiddenCutsAndLabels = getForbiddenCutsAndLabels()
        for grid in processDescriptionAndAxisLabels:
            if grid == self.gridName:
                self.xLabel = processDescriptionAndAxisLabels[grid][0]
                self.yLabel = processDescriptionAndAxisLabels[grid][1]
                self.processDescription = processDescriptionAndAxisLabels[grid][2]

                if grid in forbiddenCutsAndLabels:
                    self.forbiddenCut = forbiddenCutsAndLabels[grid][0]
                    self.forbiddenLabelXVal = forbiddenCutsAndLabels[grid][1]
                    self.forbiddenLabelYVal = forbiddenCutsAndLabels[grid][2]
                    self.forbiddenLabelText = forbiddenCutsAndLabels[grid][3]

def getProcessDescriptionAndAxisLabels():
    processDescriptionAndAxisLabels = {
    'SusyGtt': [
        'm_{#tilde{g}} [GeV]',
        'm_{#tilde{#chi}^{0}_{1}} [GeV]',
        '#tilde{g} #tilde{g} production, #tilde{g}#rightarrow t#bar{t}#tilde{#chi}^{0}_{1}, m(#tilde{t_{1}}) >> m(#tilde{g})'],
    'SusyTest': [
        'm_{#tilde{g}} [GeV]',
        'm_{#tilde{#chi}^{0}_{1}} [GeV]',
        '#tilde{g} #tilde{g} production, #tilde{g}#rightarrow t#bar{t}#tilde{#chi}^{0}_{1}'],
    'SusyComprGtt': [
        'm_{#tilde{g}} [GeV]',
        '#Deltam_{#tilde{#chi}^{0}_{1}} = m_{#tilde{#chi}^{0}_{1}} + 2m_{t} - m_{#tilde{g}} [GeV]',
        '#tilde{g} #tilde{g} production, #tilde{g}#rightarrow t#bar{t}#tilde{#chi}^{0}_{1}'],
    'SusyGG2StepWZ':[
        "m(#tilde{g}) [GeV]",
        "m(#tilde{#chi}^{0}_{1}) [GeV]",
#        "#tilde{g} #tilde{g} production, #tilde{g} #rightarrow qqWZ#tilde{#chi}^{0}_{1}; m(#tilde{#chi}^{#pm}_{1}) = (m(#tilde{g}) + m(#tilde{#chi}^{0}_{1}))/2, m(#tilde{#chi}^{0}_{2}) = (m(#tilde{#chi}^{#pm}_{1}) + m(#tilde{#chi}^{0}_{1}))/2"],
        "#tilde{g} #tilde{g} production, #tilde{g} #rightarrow qq'WZ#tilde{#chi}^{0}_{1}; m(#tilde{#chi}^{#pm}_{1}) = (m(#tilde{g}) + m(#tilde{#chi}^{0}_{1}))/2, m(#tilde{#chi}^{0}_{2}) = (m(#tilde{#chi}^{#pm}_{1}) + m(#tilde{#chi}^{0}_{1}))/2"],
    'SusyTT2Step':[
            'm_{#tilde{t}} [GeV]',
            'm_{#tilde{#chi}^{0}_{1}} [GeV]',
            ""],
    'SusyBtt':[
        'm(#tilde{b}) [GeV]',
        'm(#tilde{#chi}^{0}_{1}) [GeV]',
        "#tilde{b_{1}} #tilde{b}_{1} production, #tilde{b}_{1}#rightarrow t#tilde{#chi}^{#pm}_{1}, m(#tilde{#chi}^{#pm}_{1}) = m(#tilde{#chi}^{0}_{1}) + 100 GeV"],
    'SusyGSL':[
            'm_{#tilde{g}} [GeV]',
            'm_{#tilde{#chi}^{0}_{1}} [GeV]',
            "#tilde{g} #tilde{g} production, #tilde{g} #rightarrow qq(ll/#nu#nu)#tilde{#chi}^{0}_{1}; m(#tilde{#chi}^{0}_{2}) = (m(#tilde{g}) + m(#tilde{#chi}^{0}_{1}))/2, m(#tilde{l},#tilde{#nu}) = (m(#tilde{#chi}^{0}_{2}) + m(#tilde{#chi}^{0}_{1}))/2"],
    'SusyGG_Rpv321':[
            'm_{#tilde{g}} [GeV]',
            'm_{#tilde{t}} [GeV]',
            "#tilde{g} #tilde{g} production, #tilde{g} #rightarrow #tilde{t} #bar{t}, #tilde{t} #rightarrow #bar{d} #bar{s}"],
    'SusyGG_Rpv331':[
            'm(#tilde{g}) [GeV]',
            'm(#tilde{t}) [GeV]',
            "#tilde{g} #tilde{g} production, #tilde{g} #rightarrow #tilde{t} #bar{t}, #tilde{t} #rightarrow #bar{b} #bar{d}"],
    'SusyDD_Rpv321':[
            'm_{#tilde{d_{R}}} [GeV]',
            'm_{#tilde{g}} [GeV]',
            "#tilde{d_{R}} #tilde{d_{R}} production, #tilde{d_{R}} #rightarrow #bar{s} #bar{t}"],
    'SusyDD_Rpv331':[
            'm_{#tilde{d_{R}}} [GeV]',
            'm_{#tilde{g}} [GeV]',
            "#tilde{d_{R}} #tilde{d_{R}} production, #tilde{d_{R}} #rightarrow #bar{b} #bar{t}"],
    'SusyGG_RpvLQD':[
            'm_{#tilde{g}} [GeV]',
            'm_{#tilde{#chi}^{0}_{1}} [GeV]',
            "#tilde{g} #tilde{g} production, #tilde{g} #rightarrow qq#tilde{#chi}^{0}_{1}, #tilde{#chi}^{0}_{1} #rightarrow lqq"],
    'SusyGG_RpvUUD':[
            'm_{#tilde{g}} [GeV]',
            'm_{#tilde{#chi}^{0}_{1}} [GeV]',
            "#tilde{g} #tilde{g} production, #tilde{g} #rightarrow t#bar{t}#tilde{#chi}^{0}_{1}, #tilde{#chi}^{0}_{1} #rightarrow uds"],
    }

    return processDescriptionAndAxisLabels


def getForbiddenCutsAndLabels():
    forbiddenCutsAndLabels = {
    'SusyGtt': [2*172.5,
                1400, 1100, "m_{#tilde{g}} <  2 m_{t} + m_{#tilde{#chi}^{0}_{1}} "],
    'SusyComprGtt': [2*80,
                810, 690, "m_{#tilde{g}} <  2 m_{W} + m_{#tilde{#chi}^{0}_{1}} "],
    'SusyBtt': [172.5+100, # 172.5+100 just to make a better plot
                700, 480, "m(#tilde{b}) <  m(t) + m(#tilde{#chi}^{0}_{1}) + 100 GeV"],
#    'SusyGG2StepWZ': [80+90,
#                    1200, 1100, "m_{#tilde{g}} <  m_{W} + m_{Z} + m_{#tilde{#chi}^{0}_{1}} "],
#    'SusyGG2StepWZ': [4*80,
#                    1550, 1300, "#Delta m(#tilde{#chi}_{1}^{#pm},#tilde{#chi}_{2}^{0}) < m(W ), #Delta m(#tilde{#chi}_{2}^{0},#tilde{#chi}_{1}^{0}) < m(Z)"],
    'SusyGG2StepWZ': [4*80,
                     1400, 1150, "#Delta m(#tilde{#chi}_{1}^{#pm},#tilde{#chi}_{2}^{0}) < m(W ), #Delta m(#tilde{#chi}_{2}^{0},#tilde{#chi}_{1}^{0}) < m(Z)"],
    'SusyGSL': [0,
                    800, 850, "m(#tilde{g}) <  m(#tilde{#chi}^{0}_{1}) "],
    'SusyGG_Rpv321':[172.5,
                         1000, 860, "m_{#tilde{g}} <  m_{#tilde{t}} + m_{t} "],
    'SusyGG_Rpv331':[172.5,
                         1000, 870, "m(#tilde{g}) <  m(#tilde{t}) + m(t) "],
    'SusyDD_Rpv321':[0,
                         700, 640, "m_{#tilde{d}} =  m_{#tilde{g}} "],
    'SusyDD_Rpv331':[0,
                         700, 640, "m_{#tilde{d}} =  m_{#tilde{g}} "],
    #'SusyComprGtt': [0,
     #               700, 30, "m_{#tilde{g}} <  2 m_{t} + m_{#tilde{#chi}^{0}_{1}} "],
    'SusyGG_RpvLQD':[0,
                         1300, 1400, "m_{#tilde{g}} <  m_{#tilde{#chi}^{0}_{1}} "],
    'SusyGG_RpvUUD':[2*172.5,
                         1300, 1050, "m_{#tilde{g}} <  2 m_{t} + m_{#tilde{#chi}^{0}_{1}} "],
     }
    return forbiddenCutsAndLabels

#main()
