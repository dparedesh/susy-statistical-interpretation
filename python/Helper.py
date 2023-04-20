from sets import Set
import sys

class setBlind:

    def __init__(self,string_input):
        self.string_input=string_input
        self.SR=False
        self.CR=False
        self.VR=False
        self.regions=["SR","CR","VR","ALL"]

        self.reset(string_input)

    def reset(self,string_input):


        if string_input=="ALL":
            self.SR=True
            self.CR=True
            self.VR=True
        elif string_input is not "":

            blindList = string_input.split(",")
            self.checkRegion(blindList)

            self.SR="SR" in blindList
            self.CR="CR" in blindList
            self.VR="VR" in blindList


        print "- Blinding SR :",self.SR
        print "- Blinding CR :",self.CR
        print "- Blinding VR :",self.VR

    def checkRegion(self,blindList):

        if not Set(blindList).issubset(Set(self.regions)):
            sys.exit("-> Check your blinded regions, they don't correspond to the provided types: "+str(self.regions))


class sampleType:
    DATA, BKG, SIG = 0, 1, 2


class sample:

    def __init__(self,name,color,legend,isMC,kindOfSample,systTheoryUp={},systTheoryDown={},isAFII=False):
        self.name=name
        self.color=color
        self.legend=legend
        self.isMC=isMC
        self.kindOfSample=kindOfSample
        self.systTheoryUp=systTheoryUp
        self.systTheoryDown=systTheoryDown
        self.yields={}
        self.statUnc={}
        self.isAFII=isAFII
        self.systDataDrivenUp={}
        self.systDataDrivenDown={}

    def setYields(self,yields,statUnc):
        self.yields=yields
        self.statUnc=statUnc
    
    def setTheorySystematics(self,systTheoryUp,systTheoryDown):
        self.systTheoryUp=systTheoryUp
        self.systTheoryDown=systTheoryDown

    def setDataDrivenSystematics(self,systDataDrivenUp,systDataDrivenDown):        
        self.systDataDrivenUp=systDataDrivenUp
        self.systDataDrivenDown=systDataDrivenDown
        

    def setIsAFII(self,isAFII):
        self.isAFII=isAFII


    def getName(self):
        return self.name
    def getColor(self):
        return self.color
    def getLegendName(self):
        return self.legend
    def getMC(self):
        return self.isMC
    def getSampleType(self):
        return self.kindOfSample

    def getYields(self,region,var):
        if (region in self.yields) and (var in self.yields[region]): 
            return self.yields[region][var]
        else:
            return -1

    def getStatUnc(self,region,var):

        if (region in self.statUnc) and (var in self.statUnc[region]): 
            return self.statUnc[region][var]
        else:
            return -1 

    def getIsAFII(self):
        return self.isAFII


    def getTheorySystematicUp(self,region):
        val=self.checkSyst(self.systTheoryUp,region)
        return val

    def getTheorySystematicDown(self,region):
        val=self.checkSyst(self.systTheoryDown,region)
        return val


    def getDataDrivenSystematicUp(self,reg):
    
        if reg in self.systDataDrivenUp: return self.systDataDrivenUp[reg]
        return {}
        
    def getDataDrivenSystematicDown(self,reg):
        if reg in self.systDataDrivenDown: return self.systDataDrivenDown[reg]
        return {}           
    

    def checkSyst(self,dictSyst,region):
        if region in dictSyst:
            return float(dictSyst[region])
        else:
            return float(0)


class bkgsDef:

    def __init__(self):
        self.bkgList = []
        self.dataDrivenList = []

    def addSample(self,samp):
        self.bkgList.append(samp)
        self.updateDataDrivenList()

    '''
    def addSample(self,name,color,legend,isMC,kindOfSample,systUp={},systDown={}):
        self.bkgList.append(sample(name,color,legend,isMC,kindOfSample,systUp,systDown))
        self.updateDataDrivenList()
    '''

    def updateDataDrivenList(self):
        self.dataDrivenList=[ i for i in self.bkgList if not i.isMC]

    def getDataDrivenBkgNames(self):
        dataDrivenNames=[i.getName() for i in self.dataDrivenList]
        return dataDrivenNames

    def getBkgNames(self):
        bkgNames=[i.getName() for i in self.bkgList]
        return bkgNames



def GetBinnedFitOptions(binned,regions):

    binnedFit = {}

    if binned != "":
        for sr in binned.split(','):
          sr_def = sr.split(':')

          if sr_def[0] in regions:
            binnedFit[sr_def[0]]=sr_def[1]
          else:
            print "Region : '",sr_def[0],"' does not exist in",regions
            sys.exit("- Aborting!")       
    
    #for unbinned SRs assigned default
    for sr in regions:
       if sr not in binnedFit: binnedFit[sr] = 'cuts'
     

    return binnedFit

def CheckVarExistInBinningDict(binnedFit,binning):

    for r in binnedFit:
        if binnedFit[r] not in binning[r]:
            print binnedFit[r]," does not exist in binning dictionary: ",binning
            sys.exit("- Aborting") 

