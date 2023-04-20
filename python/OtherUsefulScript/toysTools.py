def main():
    import ROOT
    ROOT.gSystem.Load("libSusyFitter.so")
    '''
    a = getPValuesDictPerFile("/r02/atlas/thibaut/histFitterTag/HistFitterUser/MET_jets_2lep_SS/results/Mc12SusyGtt_nom_CONF_FinalToys_summer2013SameSign_output_hypotest.root")
    b = getPValuesDictPerFile("/r02/atlas/thibaut/histFitterTag/HistFitterUser/MET_jets_2lep_SS/results/Mc12SusyGtt_nom_CONF_summer2013SameSign_output_hypotest.root")

    for key in a:
        try:
            #if b[key] != 0.5 and a[key] > 0.0001:
            if b[key] < 0.05 and a[key] > 0.05:
                 print key, a[key], b[key]
        except:
            print 'damn', key
    '''
    #print getPValuesDictPerFile("/r02/atlas/thibaut/histFitterTag/HistFitterUser/MET_jets_2lep_SS/results/Mc12SusyGtt_nom_CONF_summer2013SameSign_output_hypotest.root", ["hypo_signal_1000_100", "hypo_signal_900_500"])
    #print getPValuesDictPerFile("/r02/atlas/thibaut/histFitterTag/HistFitterUser/MET_jets_2lep_SS/results/Mc12SusyGG1step_x12Toys_nom_CONF_FinalToys_summer2013SameSign_output_hypotest.root")
    #print getPValuesDictPerFile("/r02/atlas/thibaut/histFitterTag/HistFitterUser/MET_jets_2lep_SS/results/Mc12SusyGG1step_x12_nom_CONF_summer2013SameSign_output_hypotest.root", ["hypo_signal_785_305"])
    

def getPValuesDictPerFile(filename):
    import ROOT
    ROOT.gSystem.Load("libSusyFitter.so")
    
    print filename
    pValuesDict = {}
    workspaceList = []
    try:
        openFile = ROOT.TFile.Open(filename, 'READ')
        for workspace in openFile.GetListOfKeys():
            workspaceList.append(workspace.GetName())
    except:
        print 'could not get workspaces!'
    for workspaceName in workspaceList:
        if workspaceName.startswith('hypo_signal'):
            openWorkspace = openFile.Get(workspaceName)
            result = ROOT.RooStats.get_Pvalue(openWorkspace)
            masses = workspaceName.split('_')[2]+'_'+workspaceName.split('_')[3]
            pValuesDict[masses] = result.GetP1()
    try:
        openFile.Close()
    except:
        print 'see above'
    return pValuesDict


def mergeToysResults(outFileName, inFileList):
    import ROOT
    openInFiles = []
    workspacesDict, outFile = getWorkspacesInOutFileDict(outFileName)
    for inFile in inFileList:
        openInFile = ROOT.TFile(inFile, "READ")
        openInFiles.append(openInFile)
        for workspace in openInFile.GetListOfKeys():
            workspaceName = workspace.GetName()
            if workspaceName.startswith('hypo_signal'):
                hypoResult = openInFile.Get(workspaceName)
                if not workspaceName in workspacesDict:
                    workspacesDict[workspaceName] = hypoResult
                else:
                    workspacesDict[workspaceName].Add(hypoResult)

    if outFile is None:
        outFile = ROOT.TFile(outFileName, "RECREATE")
    for workspace in workspacesDict:
        outFile.Add(workspacesDict[workspace])    
    outFile.Write()
    for openFile in openInFiles:
        openFile.Close()
    outFile.Close()    

def getWorkspacesInOutFileDict(outFileName):
    workspacesDict = {}
    import os
    outFile = None
    if os.path.exists(outFileName):
        import ROOT
        outFile = ROOT.TFile(outFileName, "UPDATE")
        for workspace in outFile.GetListOfKeys():
            workspaceName = workspace.GetName()
            if workspaceName.startswith('hypo_signal'):
                hypoResult = outFile.Get(workspaceName)
                workspacesDict[workspaceName] = hypoResult
    print workspacesDict
    return workspacesDict, outFile


main()
