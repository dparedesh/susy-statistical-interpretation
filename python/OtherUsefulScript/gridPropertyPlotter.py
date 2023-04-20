#!/usr/bin/env python
import sys
sys.path.append('python')
import  ROOT, math, sys, os, pathUtilities
signalTrees = os.path.join(pathUtilities.currentTreeDirectory(), 'signal.root')
targetLumi = 20.3
inputLumi = 20.3
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel=10001;") #make root shut up
currentName = '_0303NewCFNewttHFullSymmetrisation'

def main():
    gridPropertyMaker = GridPropertyMaker(signalTrees)
    #gridPropertyMaker.printListOfMissingPoints()
    
    #gridPropertyMaker.gridsToRunOn  = 'Mc12SusyRPVUDD'#'Mc12SusyGtt'# 'Mc12SusySgluon'
    gridPropertyMaker.generateEventsDictAllGrids()
    '''
    crossSectionDict = gridPropertyMaker.getCrossSectionPerPoint()
    massesAcceptancePerGridDict = gridPropertyMaker.getAcceptancePerSRPerPoint()
    nEventsPerGridDict = gridPropertyMaker.getEventsPerSRPassingPerPoint()
    nEventsUnweightedPerGridDict =  gridPropertyMaker.getEventsPerSRPassingPerPointUnweighted()
    crossSectionUncertaintyDict = gridPropertyMaker.getCrossSectionUncertaintyPerPoint()
    totalEventsPerSignalPointDict = gridPropertyMaker.getTotalEventsPerSignalPoint()
    '''
    observedClsValuesPointDict = gridPropertyMaker.getClsValues('observed')
    expectedClsValuesPointDict = gridPropertyMaker.getClsValues('expected')
    '''
    experimentalUncertaintiesDict = gridPropertyMaker.makeExperiementalUncertaintiesDict()
    statUncertaintyPerGridDict = gridPropertyMaker.getStatUncertaintyPerSignalPointPerSR()
    '''
    #eemmRatioPerSRGrid =  gridPropertyMaker.getEEMMRatio()
    
    
    #crossSectionLimits = gridPropertyMaker.getXSecLimits()    
    #dumpToFile(crossSectionLimits, '/r02/atlas/thibaut/histFitterSummer2013/HEPDATA/crossSectionLimits')
    #dumpToFile(massesAcceptancePerGridDict , '/r02/atlas/thibaut/histFitterSummer2013/HEPDATA/acceptances')
    #dumpToFile(nEventsPerGridDict, '/r02/atlas/thibaut/histFitterSummer2013/HEPDATA/nEventsDict')
    
    
    print 'now plotting....'
    #gridPlotter = GridPropertyPlotter( eemmRatioPerSRGrid, 'eemmRatio')
    #gridPlotter.makeAndWritePlots()
    '''
    gridPlotter = GridPropertyPlotter(nEventsPerGridDict, 'nEvents')
    gridPlotter.makeAndWritePlots()
    gridPlotter = GridPropertyPlotter(experimentalUncertaintiesDict, 'experimentalUncertainty')
    gridPlotter.makeAndWritePlots()
    gridPlotter = GridPropertyPlotter(statUncertaintyPerGridDict, 'statisticalUncertainty')
    gridPlotter.makeAndWritePlots()
    gridPlotter = GridPropertyPlotter(crossSectionDict, 'crossSection')
    gridPlotter.makeAndWritePlots()
    gridPlotter = GridPropertyPlotter(massesAcceptancePerGridDict, 'acceptance')
    gridPlotter.makeAndWritePlots()
    gridPlotter = GridPropertyPlotter(crossSectionUncertaintyDict, 'crossSectionUncertainty')
    gridPlotter.makeAndWritePlots()
    gridPlotter = GridPropertyPlotter(nEventsUnweightedPerGridDict, 'nEventsUnweighted')
    gridPlotter.makeAndWritePlots()
    gridPlotter = GridPropertyPlotter(totalEventsPerSignalPointDict, 'totalEventsPerPoint')
    gridPlotter.makeAndWritePlots()
    '''
    gridPlotter = GridPropertyPlotter(observedClsValuesPointDict, 'observedCLs')
    gridPlotter.makeAndWritePlots()
    gridPlotter = GridPropertyPlotter(expectedClsValuesPointDict, 'expectedCLs')
    gridPlotter.makeAndWritePlots()
    

class GridPropertyMaker(object):
    def __init__(self, fileName):
        self.srConfigs =  ['SR0b,SR1b,SR3b,SR3Llow,SR3Lhigh', 'SR0b', 'SR1b', 'SR3b','SR3Llow','SR3Lhigh']
        self.targetLumi = 20.3
        self.inputLumi = 20.3
        self.gridsToRunOn = ''

        self._signalFile = ROOT.TFile(fileName)
        self._gridEventsDict = {}
        self._runNumbersInTree = self._getAllRunNumbersInTree()
        import signalSameSignTools
        self._signalRunnumberToMassesDict = signalSameSignTools.getRunnumbersMassesDictSSAllGrids()

        self._crossSectionRunnumberDict = self._getCrossSectionRunnumberDict()
    
    def getEventsPerSRPassingPerPoint(self):
        massesNEventsDict = {}
        for grid in self._gridEventsDict:
            massesNEventsDict[grid] = {}
            for sr in self._gridEventsDict[grid]:
                massesNEventsDict[grid][sr] = []
                for runNumber in self._gridEventsDict[grid][sr]:                
                    nEventsWeighted = self._gridEventsDict[grid][sr][runNumber][1]
                    massesNEventsDict[grid][sr].append([self._signalRunnumberToMassesDict[grid][runNumber][0], self._signalRunnumberToMassesDict[grid][runNumber][1],\
                                                      nEventsWeighted])
        return massesNEventsDict

    def getStatUncertaintyPerSignalPointPerSR(self):
        import math
        massesStatUncertaintyDict = {}
        for grid in self._gridEventsDict:
            massesStatUncertaintyDict[grid] = {}
            for sr in self._gridEventsDict[grid]:
                massesStatUncertaintyDict[grid][sr] = []
                for runNumber in self._gridEventsDict[grid][sr]:          
                    # to ge the % stat uncertainty: 1/sqrt(nRaw) * 100
                    nEventsWeighted = self._gridEventsDict[grid][sr][runNumber][1]
                    nEvents = self._gridEventsDict[grid][sr][runNumber][0]
                    if nEvents > 0: percentStatUncertainty = 1/math.sqrt(nEvents)*100
                    else: percentStatUncertainty = 0
                    massesStatUncertaintyDict[grid][sr].append([self._signalRunnumberToMassesDict[grid][runNumber][0], self._signalRunnumberToMassesDict[grid][runNumber][1],  percentStatUncertainty])
        return massesStatUncertaintyDict

    def getEventsPerSRPassingPerPointUnweighted(self):
            massesNEventsDict = {}
            for grid in self._gridEventsDict:
                massesNEventsDict[grid] = {}
                for sr in self._gridEventsDict[grid]:
                    massesNEventsDict[grid][sr] = []
                    for runNumber in self._gridEventsDict[grid][sr]:                
                        nEvents = self._gridEventsDict[grid][sr][runNumber][0]

                        massesNEventsDict[grid][sr].append([self._signalRunnumberToMassesDict[grid][runNumber][0], \
                                                            self._signalRunnumberToMassesDict[grid][runNumber][1], nEvents])
            return massesNEventsDict 

    def getAcceptancePerSRPerPoint(self):
        import signalSameSignTools
        totalEventsInSignalSamplesDict = self._getTotalEventsInSignalSamples()
        acceptanceDict = {}
        for grid in self._gridEventsDict:
            acceptanceDict[grid] = {}
            for sr in self._gridEventsDict[grid]:
                acceptanceDict[grid][sr] = []
                for runNumber in self._gridEventsDict[grid][sr]:
                    if runNumber in totalEventsInSignalSamplesDict:

                        filterEfficiency = signalSameSignTools.getFilterEfficiency(int(runNumber))
                        acceptance = self._gridEventsDict[grid][sr][runNumber][0]*filterEfficiency/totalEventsInSignalSamplesDict[runNumber]*100
                        acceptanceDict[grid][sr].append([self._signalRunnumberToMassesDict[grid][runNumber][0], self._signalRunnumberToMassesDict[grid][runNumber][1], acceptance])
        return acceptanceDict

    def getTotalEventsPerSignalPoint(self):
        totalEventsInSignalSamplesDict = self._getTotalEventsInSignalSamples()
        totalEventsPerPointDict = {}
        for gridName in self._signalRunnumberToMassesDict:
            totalEventsPerPointDict[gridName] = []
            for runNumber in self._signalRunnumberToMassesDict[gridName]:
                if runNumber in totalEventsInSignalSamplesDict:
                    totalEventsPerPointDict[gridName].append([str(runNumber)+', '+str(self._signalRunnumberToMassesDict[gridName][runNumber][0]), \
                                                       self._signalRunnumberToMassesDict[gridName][runNumber][1], totalEventsInSignalSamplesDict[runNumber]])

        return totalEventsPerPointDict
    
        
    def getCrossSectionPerPoint(self):
        crossSectionDict = {}
        for gridName in self._signalRunnumberToMassesDict:
            #print gridName
            crossSectionDict[gridName] = []
            for runNumber in self._signalRunnumberToMassesDict[gridName]:
                if runNumber in self._crossSectionRunnumberDict:
                    crossSectionDict[gridName].append([self._signalRunnumberToMassesDict[gridName][runNumber][0], self._signalRunnumberToMassesDict[gridName][runNumber][1], self._crossSectionRunnumberDict[runNumber][0]*1000])
                else:
                    print 'missing runnumber in xSec file:', runNumber
        return crossSectionDict
    
    def getCrossSectionUncertaintyPerPoint(self):              
        crossSectionUncertDict = {}
        for gridName in self._signalRunnumberToMassesDict:
            crossSectionUncertDict[gridName] = []
            for runNumber in self._signalRunnumberToMassesDict[gridName]:
                if runNumber in self._crossSectionRunnumberDict and self._crossSectionRunnumberDict[runNumber][0] > 0:
                    crossSectionUncertDict[gridName].append([self._signalRunnumberToMassesDict[gridName][runNumber][0], \
                                                             self._signalRunnumberToMassesDict[gridName][runNumber][1], 100*self._crossSectionRunnumberDict[runNumber][1]/self._crossSectionRunnumberDict[runNumber][0]])
        return crossSectionUncertDict

    def getClsValues(self, mode):
        clsValuesDict = {}
        for gridName in self._signalRunnumberToMassesDict:
            listFileName = '/r02/atlas/thibaut/histFitterSummer2013/HistFitterUser/MET_jets_2lep_SS/macroSS/{0}_nom{1}_summer2013SameSign_output_hypotest__1_harvest_list'.format(gridName, currentName)
            
            if os.path.isfile(listFileName):
                clsValuesDict[gridName] = []
                openFile = open(listFileName)
                for point in openFile:
                    entries = point.split()
                    if mode == 'expected': cls = entries[6]
                    elif mode == 'observed' : cls = entries[2]
                    else:
                        print 'unkonw mode {0}, has to be either \'expected\' or \'observed\''.format(mode)
                        return {}
                    clsValuesDict[gridName].append([float(entries[-3]), float(entries[-2]), float(cls)])
                    
        return clsValuesDict

    def getXSecLimits(self):
        clsValuesDict = {}
        for gridName in self._signalRunnumberToMassesDict:
            listFileName = '/r02/atlas/thibaut/histFitterSummer2013/HistFitterUser/MET_jets_2lep_SS/macroSS/{0}_nom{1}_summer2013SameSign_output_upperlimit__1_harvest_list_updated'.format(gridName, currentName)
            
            print listFileName
            if os.path.isfile(listFileName):
                clsValuesDict[gridName] = []
                openFile = open(listFileName)
                for point in openFile:
                    entries = point.split()
                    limit = entries[-9]
                    clsValuesDict[gridName].append([float(entries[-2]), float(entries[-1]), float(limit)*1000])
        return clsValuesDict
        
    def makeExperiementalUncertaintiesDict(self):
        outDict = {}
        import csv
        experimentalUncertaintiesDict = {}
        for key, val in csv.reader(open("../share/experimentalUncertainties.csv")):
            experimentalUncertaintiesDict[key] = eval(val)

        for grid in experimentalUncertaintiesDict:
            outDict[grid] = {}
            for signalPoint in experimentalUncertaintiesDict[grid]:
                runNumber = signalPoint.strip('signal')
                for signalRegion in experimentalUncertaintiesDict[grid][signalPoint]:
                    if not signalRegion in outDict[grid]: outDict[grid][signalRegion] = []
                    if grid in self._signalRunnumberToMassesDict:
                        if runNumber in self._signalRunnumberToMassesDict[grid]:
                            outDict[grid][signalRegion].append([self._signalRunnumberToMassesDict[grid][runNumber][0], self._signalRunnumberToMassesDict[grid][runNumber][1],  experimentalUncertaintiesDict[grid][signalPoint][signalRegion]])

        return outDict
    

    def generateEventsDictAllGrids(self):
        for grid in self._signalRunnumberToMassesDict:
            self._gridEventsDict[grid] = {}
            if self.gridsToRunOn == '' or grid in self.gridsToRunOn:
                try:
                    for srConfig in self.srConfigs:
                        self._gridEventsDict[grid][srConfig] = self._runCutsOnGrid(self._signalRunnumberToMassesDict[grid], grid, srConfig)
                except:
                    print 'This grid did not work:', grid
                

    def printListOfMissingPoints(self):
        for gridName in self._signalRunnumberToMassesDict:
            for runNumber in self._signalRunnumberToMassesDict[gridName]:
                if not runNumber in self._runNumbersInTree:
                    print 'this point is missing in the tree', runNumber, self._signalRunnumberToMassesDict[gridName][runNumber][0], self._signalRunnumberToMassesDict[gridName][runNumber][1]


    def _runCutsOnGrid(self, gridDict, gridName, sr='SR0b,SR1b,SR3b,SR3Llow,SR3Lhigh'):
        runNumbersToEventsDict = {}
        for runNumber in gridDict:
            if runNumber in self._runNumbersInTree:
                tree = self._signalFile.Get('signal'+runNumber+'_nom')
                nEvents, nEventsWeighted = self._runCutsOnTree(tree, sr)
                runNumbersToEventsDict[runNumber] = [nEvents, nEventsWeighted]
        return runNumbersToEventsDict
    
    def _runCutsOnTree(self, tree, sr):
        nEventsPass = 0
        nEventsWeighted = 0
        for event in tree:
            if  (((event.nLep15==2 and event.met>150000 and event.nJets40>=3 and event.nBJets20==0 and event.mt>100000 and event.meff > 400000) and 'SR0b' in sr)\
                   or ((event.nLep15==2 and event.met>150000 and event.nJets40>=3 and event.nBJets20>=1 and event.mt>100000 and event.meff > 700000) and not (event.nLep15>=2 and event.nJets40>=5 and event.nBJets20 >2 and event.meff > 350000)  and 'SR1b' in sr) or \
                   ((event.nLep15>=2 and event.nJets40>=5 and event.nBJets20 >2 and event.meff > 350000)  and 'SR3b' in sr) or \
                 ((event.nLep15>=3 and event.met>50000 and event.met<150000 and event.nJets40>=4 and (event.mllSFOS1 < 84000 or event.mllSFOS1 > 98000) and  (event.mllSFOS2 < 84000 or event.mllSFOS2 > 98000)  and event.meff > 400000)  and not (event.nLep15>=2 and event.nJets40>=5 and event.nBJets20 >2 and event.meff > 350000) and 'SR3Llow' in sr) or \
                (event.nLep15>=3 and  event.met>150000 and event.nJets40>=4  and event.meff > 400000)  and not (event.nLep15>=2 and event.nJets40>=5 and event.nBJets20 >2 and event.meff > 350000) and 'SR3Lhigh' in sr):
                nEventsPass += 1
                nEventsWeighted += event.mcWgt * event.pileupWgt * event.trigWgt * \
                                  event.eGammaWgt * event.muonWgt * event.lumiScaling * event.bTagWgt * targetLumi/inputLumi

        return nEventsPass, nEventsWeighted

    def _getTotalEventsInSignalSamples(self):
        import os
        totalEventsPerRunnumberDict = {}
        totalEventsFile = '/r02/atlas/thibaut/histFitterSummer2013/HistFitterUser/MET_jets_2lep_SS/share/totalEventsInfo'
        openFile = open(totalEventsFile)
        for line in openFile:
            if not line.startswith('#'):
                totalEventsPerRunnumberDict[line.split()[0]] = float(line.split()[1])
        return totalEventsPerRunnumberDict

    def _getCrossSectionRunnumberDict(self):
        import os
        crossSectionRunnumberDict = {}
        crossSectionFile =  '/r02/atlas/thibaut/histFitterSummer2013/HistFitterUser/MET_jets_2lep_SS/share/crossSectionInfo'
        openFile = open(crossSectionFile)
        for line in openFile:
            if not line.startswith('#'):
                crossSectionRunnumberDict[line.split()[0]] = [float(line.split()[1]), float(line.split()[2])]
        return crossSectionRunnumberDict

    def _getAllRunNumbersInTree(self):
        runNumbersInTree = []
        keys = self._signalFile.GetListOfKeys()
        for name in keys:
            if name.GetName().endswith('_nom'):
                runNumbersInTree.append(name.GetName().strip('_nom').strip('signal'))
        return runNumbersInTree
    
    # only a little test
    def getEEMMRatio(self):
        eemmRatioDictPerSR = self._getEEMMRatioDict()
        eemmRatioPerGridDict = {}

        for grid in self._gridEventsDict:
            eemmRatioPerGridDict[grid] = {}
            for sr in [     'GG1stepCC_PRatioGT1_SF.txt',    
                                 'GG1stepCC_PRatioGT1_SSSF.txt',
                                 'GG1stepCC_PRatioGT1_exactly2.txt', 
                                 'GG2CNsl_PRatioGT1_SF.txt',
                                 'GG2CNsl_PRatioGT1_SSSF.txt',
                                 'GG2CNsl_PRatioGT1_exactly2.txt', 
                                 'SS2CNsl_PRatioGT1_SF.txt',        
                                 'SS2CNsl_PRatioGT1_SSSF.txt',    
                                 'SS2CNsl_PRatioGT1_exactly2.txt', 
                                 ]:
                eemmRatioPerGridDict[grid][sr] = []
                for runNumber in eemmRatioDictPerSR[sr]:
                    if eemmRatioDictPerSR[sr][runNumber] < 5 and (runNumber in self._signalRunnumberToMassesDict[grid]) and  eemmRatioDictPerSR[sr][runNumber] > 0:
                        eemmRatioPerGridDict[grid][sr].append([self._signalRunnumberToMassesDict[grid][runNumber][0], self._signalRunnumberToMassesDict[grid][runNumber][1], eemmRatioDictPerSR[sr][runNumber]])
        return eemmRatioPerGridDict

    def _getEEMMRatioDict(self):
        import os
        eemmRatioPerSRDict = {}
        srList = [ 
            'GG1stepCC_PRatioGT1_SF.txt',    
            'GG1stepCC_PRatioGT1_SSSF.txt',
            'GG1stepCC_PRatioGT1_exactly2.txt', 
            'GG2CNsl_PRatioGT1_SF.txt',
            'GG2CNsl_PRatioGT1_SSSF.txt',
            'GG2CNsl_PRatioGT1_exactly2.txt', 
            'SS2CNsl_PRatioGT1_SF.txt',        
            'SS2CNsl_PRatioGT1_SSSF.txt',    
            'SS2CNsl_PRatioGT1_exactly2.txt', 
            ]
        baseFileName =  '/r02/atlas/thibaut/histFitterSummer2013/HistFitterUser/MET_jets_2lep_SS/share/SM'
        for sr in srList:
            eemmRatioPerSRDict[sr] = {}
            openFile = open(baseFileName+sr)
            for line in openFile:
                if not line.startswith('#'):
                    if line.split()[1] != 'nan': eemmRatioPerSRDict[sr][line.split()[0]] = float(line.split()[1])
        return  eemmRatioPerSRDict



class GridPropertyPlotter(object):
    def __init__(self, pointsDict, mode):
        self.mode = mode
        self.pointsDict = pointsDict
        self.outputDirectory = '/r02/atlas/thibaut/histFitterSummer2013/acceptanceForSignal'
        
        self._getLabels()
        
        if mode == 'acceptance':
            self.title = 'Acceptance x Efficiency [%];'
            self._roundNumber = 2
            self.zLabel = 'Acceptance x Efficiency [%]'
        elif mode == 'nEvents':
            self.title = 'number of Events in SRs for 20.3 fb^{-1};'
            self._roundNumber = 2
            self.zLabel = 'number of Events/Point for 20.3 fb^{-1}'
        elif mode == 'crossSection':
            self.title = 'Cross section X filter efficiency in fb;'
            self._roundNumber = 1
            self.zLabel = 'Cross section X Efficiency  [fb]'
        elif mode == 'crossSectionUncertainty':
            self.title = 'cross section uncertainty [%];'
            self._roundNumber = 1
            self.zLabel = 'Cross Section Uncertainty [%]'
        elif mode == 'nEventsUnweighted':
            self.title = 'Unweighted number of events passing signal selection;'
            self._roundNumber = 0
            self.zLabel = 'nEvents/Point'
        elif mode == 'totalEventsPerPoint':
             self.title = 'Total events in each point;'
             self._roundNumber = 0
             self.zLabel = 'Total Events/Point'
        elif mode == 'observedCLs':
             self.title = 'Observed CLs values;'
             self._roundNumber = 2
             self.zLabel = 'Observed CLs value'
        elif mode == 'expectedCLs':
             self.title = 'Expected CLs values;'
             self._roundNumber = 2
             self.zLabel = 'Expected CLs value'
        elif mode == 'eemmRatio':
            self.title = 'EEMM ratio;'
            self._roundNumber = 3
            self.zLabel = 'eeMM Ratio'
        elif mode == 'statisticalUncertainty':
            self.title = 'Statistical Uncertainty on signal estimate [%];'
            self._roundNumber = 2
            self.zLabel = 'Statistical Uncertainty on signal estimate [%]'
        elif mode == 'experimentalUncertainty':
            self.title = 'Experimental Uncertainty on signal estimate [%];'
            self._roundNumber = 2
            self.zLabel = 'Experimental Uncertainty on signal estimate [%]'

        print mode

    def makeAndWritePlots(self):
        histDict = {}
        for gridName in self.pointsDict:
            if type(self.pointsDict[gridName]) is dict:
                for signalRegionConfig in self.pointsDict[gridName]:
                    try:
                        coordinates = self._getCoordiantes(self.pointsDict[gridName][signalRegionConfig])
                        self._makeExclusionPlot(coordinates, gridName, signalRegionConfig)
                    except: print '\tcould not make this plot... moving on!'
            else:
                try:
                    coordinates = self._getCoordiantes(self.pointsDict[gridName])
                    self._makeExclusionPlot(coordinates, gridName, '')
                except: print '\tcould not make this plot... moving on!'

    def _getCoordiantes(self, pointsList):
        coordinates = []
        for point in pointsList:
            if point[2] != 'inf':
                zValue = float(point[2])
            else:
                zValue = 1000
            coordinates.append([float(point[0]), float(point[1]), zValue])
        return coordinates

    def _makeExclusionPlot(self, coordinates, gridName, signalRegionConfig):
        print gridName
        self._setColourScale()
        from ROOT import TCanvas, TGraph2D, TGraph, gROOT
        canvas = TCanvas('canvas', 'canvas', 800, 800)
        canvas.SetLeftMargin(0.13)
        canvas.SetRightMargin(0.17)
        canvas.SetBottomMargin(0.15)
        canvas.SetTopMargin(0.15)
        if self.mode == 'nEvents' or self.mode == 'crossSection':
            canvas.SetLogz()
        pointsGraph = TGraph2D()
        exclusionGraph = TGraph2D()
        #exclusionGraph.SetName('exclusion_'+gridName+'_'+title)
        #exclusionGraph.SetTitle(self.title+' '+signalRegionConfig)
        exclusionGraph.SetTitle(' ')

        i = 0
        for x,y,z in coordinates:
            exclusionGraph.SetPoint(i, x, y, z)
            pointsGraph.SetPoint(i, x, y, z)
            i += 1
        xMin, xMax, yMin, yMax, zMin, zMax = self._getMaxMin(coordinates)
        
        exclusionGraph.GetHistogram().GetXaxis().SetTitle(self._labelsPerGrid[gridName].xLabel)
        exclusionGraph.GetHistogram().GetXaxis().SetTitleOffset(1.2)
        exclusionGraph.GetHistogram().GetYaxis().SetTitle(self._labelsPerGrid[gridName].yLabel)
        exclusionGraph.GetHistogram().GetYaxis().SetTitleOffset(1.8)
        exclusionGraph.GetHistogram().GetZaxis().SetTitleOffset(1.4)
        exclusionGraph.GetHistogram().GetZaxis().SetTitle(self.zLabel)
        
        if self.mode != 'acceptance':
            if zMin == 0 and ( self.mode == 'nEvents'):
                exclusionGraph.GetHistogram().GetZaxis().SetRangeUser(0.01, zMax*1.2)
            elif self.mode == 'crossSection' or  self.mode == 'nEventsUnweighted' or self.mode == 'totalEventsPerPoint' or self.mode == 'crossSectionUncertainty':
                exclusionGraph.GetHistogram().GetZaxis().SetRangeUser(zMin*0.8, zMax*1.2)
            elif self.mode == 'statisticalUncertainty' or self.mode == 'experimentalUncertainty':
                exclusionGraph.GetHistogram().GetZaxis().SetRangeUser(0, 100)
            else:
                #print "hack!"
                #exclusionGraph.GetHistogram().GetZaxis().SetRangeUser(0.75 * zMin, zMax*1.5)
                exclusionGraph.GetHistogram().GetZaxis().SetRangeUser(0, 1)
        else:
            exclusionGraph.GetHistogram().GetZaxis().SetRangeUser(0, 4)

        contourGraph = exclusionGraph.Clone('contour')
        contourGraph.GetHistogram().SetContour(1)
        contourGraph.GetHistogram().SetContourLevel(0, 2)
        from ROOT import kRed, kBlue
        contourGraph.SetLineColor(kBlue)
        contourGraph.SetLineStyle(2)
        contourGraph.SetLineWidth(2)
        exclusionGraph.Draw('colz')
        #contourGraph.Draw('cont3same')
      
        #pointsGraph.SetMarkerStyle(20)
        #pointsGraph.SetMarkerSize(0.6)
        #pointsGraph.Draw("psame")

        from ROOT import TLine, TLatex
        Leg0 = ROOT.TLatex(xMin, yMax+yMax*0.02, self._labelsPerGrid[gridName].processDescription)
        Leg0.SetTextAlign(11)
        Leg0.SetTextFont(42)
        Leg0.SetTextSize(0.035)
        Leg0.Draw("same")

        # Mandatory ATLAS Label
        atlasLabel = ROOT.TLatex(xMin, yMax * (1 + 0.07), "ATLAS")
        #atlasLabel.SetNDC()
        atlasLabel.SetTextFont(72)
        atlasLabel.SetTextSize( 0.035 )
        atlasLabel.Draw("same")
        
        progressLabel = ROOT.TLatex(xMin, yMax * (1 + 0.07),"             Internal")
        #progressLabel.SetNDC()
        progressLabel.SetTextFont(42)
        progressLabel.SetTextSize( 0.035 )
        #progressLabel.Draw("same")

        pointLatexDict = {}
        for x,y,z in coordinates:
            if self._roundNumber == 0:
                roundedZ = str(int(z))
            else:
                if z > 10000: roundedZ = str(round((z/10000), 1))+'E4'
                elif z > 1000: roundedZ = str(round((z/1000), 1))+'E3'
                elif z > 100:
                    roundedZ = str(int(z))
                elif z > 10:
                    roundedZ = str(round(z, 1))
                else:
                    roundedZ = str(round(z, self._roundNumber))
            pointLatexDict[str(x)+str(y)] = ROOT.TLatex(x - 0.02 * (x-xMin), y - 0.01 * (y-yMin), roundedZ)
            pointLatexDict[str(x)+str(y)].SetTextFont(42)
            pointLatexDict[str(x)+str(y)].SetTextSize(0.012)
            pointLatexDict[str(x)+str(y)].SetTextAngle(45)
            pointLatexDict[str(x)+str(y)].Draw("same")
            
        '''
        print 'AAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC'
        if self._labelsPerGrid[gridName].forbiddenLabelText != 'None':
            xMin, xMax, yMin, yMax, zMin, zMax = self._getMaxMin(coordinates)
            yMinLine = xMin - self._labelsPerGrid[gridName].forbiddenCut
            yMaxLine = xMax - self._labelsPerGrid[gridName].forbiddenCut
            xMinLine = yMin + self._labelsPerGrid[gridName].forbiddenCut
            xMaxLine = yMax + self._labelsPerGrid[gridName].forbiddenCut
            
            if (xMinLine < xMin):  xMinLine = xMin
            else: yMinLine = yMin
            if (xMaxLine > xMax): xMaxLine = xMax;
            else: yMaxLine = yMax;
     
            
            lineExcl = ROOT.TLine(xMinLine, yMinLine, xMaxLine, yMaxLine)
            lineExcl.SetLineStyle(3)
            lineExcl.SetLineWidth(1)
            lineExcl.SetLineColor(14)
            lineExcl.Draw("same")

            forbiddenLabel = ROOT.TLatex(self._labelsPerGrid[gridName].forbiddenLabelXVal, self._labelsPerGrid[gridName].forbiddenLabelYVal, \
                                         self._labelsPerGrid[gridName].forbiddenLabelText)
            forbiddenLabel.SetTextSize(0.025)
            forbiddenLabel.SetTextColor(14)
            import math
            try:
                forbiddenLabel.SetTextAngle(180/3.1415927*math.atan2((yMaxLine-yMinLine)/(yMax-yMin),1))
                forbiddenLabel.SetTextFont(42)
                forbiddenLabel.Draw("same")
            except:
                print "some float division here"
                '''
        

        import os.path, datetime
        datetag = str(datetime.date.today()).replace('-', '')
        # datetag+'_'+
        canvas.SaveAs(os.path.join(self.outputDirectory, self.mode+'_'+gridName+signalRegionConfig.replace(',', '')+'.pdf'))


    def _setColourScale(self):
        colourscale = []
        r = [0.2, 0.4, 0.3, 1.0, 1.0]
        g = [0.2, 0.7, 0.8, 1.0, 0.4]
        b = [0.8, 1.0, 0.0, 0.0, 0.0]
        s = [0.0, 0.14, 0.43, 0.71, 1.0]
        from array import array
        rar = array('d',r)
        gar = array('d',g)
        bar = array('d',b)
        sar = array('d',s)
        import ROOT
        colourtable = ROOT.TColor.CreateGradientColorTable(5, sar, rar, gar, bar, 50)
        for i in range(50):
            colourscale.append(colourtable+i)
        car = array('i',colourscale)
        ROOT.gStyle.SetPalette(50,car)
        

    def _getMaxMin(self, coordinates):
        xMin = 1e6
        xMax = -1
        yMin = 1e6
        yMax = -1
        zMin = 1e6
        zMax = -1
        for x,y,z in coordinates:
            if x < xMin:
                xMin = x
            if x > xMax:
                xMax = x
            if y < yMin:
                yMin = y
            if y > yMax:
                yMax = y
            if z < zMin:
                zMin = z
            if z > zMax:
                zMax = z
        return xMin, xMax, yMin, yMax, zMin, zMax

    def _getLabels(self):
        import sys
        sys.path.append('python')
        import axisLabelsProcessDescriptions
        self._labelsPerGrid = axisLabelsProcessDescriptions.getLabelsPerGrid()


def dumpToFile(dict, outFileName):
    openFile = open(outFileName, 'w+')
    
    for gridName in dict:
        print type(dict[gridName])
        openFile.write('\n################\n\n##'+gridName+'\n\n################\n')
        if type(dict[gridName]) == type({}):
        #if type(dict[gridName]) is dict:
            for signalRegion in dict[gridName]:
                openFile.write('\n\n#'+signalRegion+'\n')
                for point in  dict[gridName][signalRegion]:
                    openFile.write(str(point[0])+', '+str(point[1])+' : '+str(point[2])+'\n')
        else:
            for point  in  dict[gridName]:
                    openFile.write(str(point[0])+', '+str(point[1])+' : '+str(point[2])+'\n')

    openFile.close()
    

if __name__ == "__main__":
    main()
