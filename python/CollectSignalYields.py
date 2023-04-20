from ROOT import *
import subprocess,os
Target = [
"376800",
"376807",
"376844",
"436556",
"436562",
"436567",
"436542",
"436560",
"436575",
        ]

def NPInfo(grid,thUnc,nameTag,analysis,SRs,fittypetag):
    for SR in list(SRs.split("_")):
        if SR == "": continue
        if not "disc" == fittypetag:
            folderNameBase=grid+'_'+thUnc+nameTag+'_Excl_Job*'+analysis
        else:
            folderNameBase='Discovery_'+thUnc+nameTag+'_Dis_Job*'+analysis
    #    folderNameBase=grid+'_'+thUnc+nameTag+'_UL*'+analysis
    
        import pathUtilities,glob,os,fnmatch,signalSameSignTools
    
        resultsDir=pathUtilities.histFitterSource()+'/results/'
        
        # find list of directories
        if not "bkg" == fittypetag and not "disc" == fittypetag:
            massesDict = signalSameSignTools.getRunnumberMassesDictSS(grid)
    
        for root, dirs, files in os.walk(resultsDir):
            for name in dirs:
                #print 'found folder',name
                #print 'matching with',folderNameBase
                if fnmatch.fnmatch(name, folderNameBase):
                    print 'scanning folder',(os.path.join(root, name))
                    if "bkg" == fittypetag:
                        fileList=glob.glob(os.path.join(root, name)+'/bkgOnly_combined_NormalMeasurement_model_afterFit.root')
                    elif "disc" == fittypetag:
                        fileList=glob.glob(os.path.join(root, name)+'/Discovery_combined_NormalMeasurement_model_afterFit.root')
                    else:
                        fileList=glob.glob(os.path.join(root, name)+'/'+grid+'*combined_NormalMeasurement_model_afterFit.root')
                    
                    for f in fileList:
                        print 'reading file',f
                        # extract sample name
                        if not "bkg" == fittypetag and not "disc" == fittypetag:
                            one=f.split('/')[-1]
                            print one
                            if "GG_Rpv331" in grid:
                                dsid=f.split('/')[-1].split('_')[2][6:13]
                            else:
                                dsid=f.split('/')[-1].split('_')[1][6:13]
                            print 'looking at sample ',dsid
                            # get masses
                            masses=massesDict[dsid]
        #                    if dsid not in Target:
        #                        continue
        
                            fout = pathUtilities.histFitterUser()+'/NP_Info/'+grid+"_"+SR+fittypetag+'/'+grid+'_'+thUnc+'_'+nameTag+'_'+dsid+'_'+str(masses[0])+'_'+str(masses[1])+'_Excl_FitResult.tex'
                            fout1 = pathUtilities.histFitterUser()+'/NP_Info/'+grid+"_"+SR+fittypetag+'/'+grid+'_'+thUnc+'_'+nameTag+'_'+dsid+'_'+str(masses[0])+'_'+str(masses[1])+'_Excl_NP_Ranking'
                        else:
                            fout = pathUtilities.histFitterUser()+'/NP_Info/'+grid+"_"+SR+fittypetag+'/'+grid+'_'+thUnc+'_'+nameTag+'_FitResults.tex'
                            fout1 = pathUtilities.histFitterUser()+'/NP_Info/'+grid+"_"+SR+fittypetag+'/'+grid+'_'+thUnc+'_'+nameTag+'_NP_Ranking'
                        print "creating output file",fout,fout1
    
                        # read histo
    #                    cmd1 = 'SysTable.py -c ' + SR + ' -w ' + f + ' -o ' + fout1 + ' -b '
                        cmd = 'PrintFitResult.py -c ' + SR + ' -w ' + f + ' -o ' + fout 
                        cmd1 = 'SystRankingPlot.py -f ' + SR + ' -w ' + f + ' -n ' + fout1 + ' -o ' + pathUtilities.histFitterSource()+'/RankingPlots/'+grid+SR+'/' + ' -p mu_'+SR+' --lumi 140'
                        print cmd
    #                    print cmd1
                        subprocess.call(cmd+'\n',shell=True)
    #                    subprocess.call(cmd+'\n'+cmd1+'\n',shell=True)

def SysBreakDown(grid,thUnc,nameTag,analysis,SRs,fittypetag):
    for SR in list(SRs.split("_")):
        if SR == "": continue
        if not "disc" == fittypetag:
            folderNameBase=grid+'_'+thUnc+nameTag+'_Excl_Job*'+analysis
        else:
            folderNameBase='Discovery_'+thUnc+nameTag+'_Dis_Job*'+analysis
    
        import pathUtilities,glob,os,fnmatch,signalSameSignTools
    
        resultsDir=pathUtilities.histFitterSource()+'/results/'
        
        # find list of directories
        if not "bkg" == fittypetag and not "disc" == fittypetag:
            massesDict = signalSameSignTools.getRunnumberMassesDictSS(grid)
    
        for root, dirs, files in os.walk(resultsDir):
            for name in dirs:
                #print 'found folder',name
                #print 'matching with',folderNameBase
                if fnmatch.fnmatch(name, folderNameBase):
                    print 'scanning folder',(os.path.join(root, name))
                    if "bkg" == fittypetag:
                        fileList=glob.glob(os.path.join(root, name)+'/bkgOnly_combined_NormalMeasurement_model_afterFit.root')
                    elif "disc" == fittypetag:
                        fileList=glob.glob(os.path.join(root, name)+'/Discovery_combined_NormalMeasurement_model_afterFit.root')
                    else:
                        fileList=glob.glob(os.path.join(root, name)+'/'+grid+'*combined_NormalMeasurement_model_afterFit.root')
    
                    
                    for f in fileList:
                        print 'reading file',f
                        # extract sample name
                        if not "bkg" == fittypetag and not "disc" == fittypetag:
                            one=f.split('/')[-1]
                            print one
                            if "GG_Rpv331" in grid:
                                dsid=f.split('/')[-1].split('_')[2][6:13]
                            else:
                                dsid=f.split('/')[-1].split('_')[1][6:13]
                            print 'looking at sample ',dsid
                            # get masses
                            masses=massesDict[dsid]
        #                    if dsid not in Target:
        #                        continue
                            fout = pathUtilities.histFitterUser()+'/Sys_BreakDown/'+grid+"_"+SR+fittypetag+'/'+grid+'_'+thUnc+'_'+nameTag+'_'+dsid+'_'+str(masses[0])+'_'+str(masses[1])+'_Excl_SysBreak_PostFit.tex'
                            fout1 = pathUtilities.histFitterUser()+'/Sys_BreakDown/'+grid+"_"+SR+fittypetag+'/'+grid+'_'+thUnc+'_'+nameTag+'_'+dsid+'_'+str(masses[0])+'_'+str(masses[1])+'_Excl_SysBreak_PreFit.tex'
                        else:
                            fout = pathUtilities.histFitterUser()+'/Sys_BreakDown/'+grid+"_"+SR+fittypetag+'/'+grid+'_'+thUnc+'_'+nameTag+'_SysBreak_PostFit.tex'
                            fout1 = pathUtilities.histFitterUser()+'/Sys_BreakDown/'+grid+"_"+SR+fittypetag+'/'+grid+'_'+thUnc+'_'+nameTag+'_SysBreak_PreFit.tex'
    
    
                        print "creating output file",fout
    
                        # read histo
                        cmd1 = 'SysTable.py -% -c ' + SR + ' -w ' + f + ' -o ' + fout1 + ' -b '
                        cmd = 'SysTable.py -% -c ' + SR + ' -w ' + f + ' -o ' + fout 
                        subprocess.call(cmd+'\n'+cmd1+'\n',shell=True)

def CollectYields(grid,thUnc,nameTag,analysis,SRs,fittypetag):
    for SR in list(SRs.split("_")):
        if SR == "": continue
        if "excl" == fittypetag:
            folderNameBase=grid+'_'+thUnc+nameTag+'_Excl_Job*'+analysis
        elif "bkg" == fittypetag:
            folderNameBase=grid+'_'+thUnc+nameTag+'_bkg*'+analysis
        else:
            folderNameBase='Discovery_'+thUnc+nameTag+'_Dis_Job*'+analysis
    
    
        import pathUtilities,glob,os,fnmatch,signalSameSignTools
    
        resultsDir=pathUtilities.histFitterSource()+'/results/'
        
        # find list of directories
        if not "bkg" == fittypetag and not "disc" == fittypetag:
            massesDict = signalSameSignTools.getRunnumberMassesDictSS(grid)
    
        for root, dirs, files in os.walk(resultsDir):
            for name in dirs:
                print 'found folder',name
                print 'matching with',folderNameBase
                if fnmatch.fnmatch(name, folderNameBase):
                    print 'scanning folder',(os.path.join(root, name))
                    if "bkg" == fittypetag:
                        fileList=glob.glob(os.path.join(root, name)+'/bkgOnly_combined_NormalMeasurement_model_afterFit.root')
                    elif "disc" == fittypetag:
                        fileList=glob.glob(os.path.join(root, name)+'/Discovery_combined_NormalMeasurement_model_afterFit.root')
                    else:
                        fileList=glob.glob(os.path.join(root, name)+'/'+grid+'*combined_NormalMeasurement_model_afterFit.root')
    
                    
                    for f in fileList:
                        print 'reading file',f
                        # extract sample name
                        if not "bkg" == fittypetag and not "disc" == fittypetag:
                            one=f.split('/')[-1]
                            print one
                            if "GG_Rpv331" in grid:
                                dsid=f.split('/')[-1].split('_')[2][6:13]
                            else:
                                dsid=f.split('/')[-1].split('_')[1][6:13]
                            print 'looking at sample ',dsid
                            # get masses
                            masses=massesDict[dsid]
        #                    if dsid not in Target:
        #                        continue
    
                            fout = pathUtilities.histFitterUser()+'/Yields/'+grid+"_"+SR+fittypetag+'/'+grid+'_'+thUnc+'_'+nameTag+'_'+dsid+'_'+str(masses[0])+'_'+str(masses[1])+'_Excl_Yields.tex'
                        else:
                            fout = pathUtilities.histFitterUser()+'/Yields/'+grid+"_"+SR+fittypetag+'/'+grid+'_'+thUnc+'_'+nameTag+'_Yields.tex'
    
                        print "creating output file",fout
    
                        # read histo
                        if "excl" in fittypetag:
                            cmd = 'YieldsTable.py -c ' + SR + ' -s Multiboson,Multitop,ttV,Fakes,MisCharge,' + f.split('/')[-1].split('_')[1] + ' -w ' + f + ' -o ' + fout + ' -b '
                        if "bkg" in fittypetag:
                            cmd = 'YieldsTable.py -c ' + SR + ' -s Multitop,OtherMultiboson,ttH,ttW,ttZ,WZ,TTbarSgTop,Vjets' + ' -w ' + f + ' -o ' + fout + ' -b '
    #                        cmd = 'YieldsTable.py -c ' + SR + ' -s Multiboson,Multitop,ttV,Fakes,MisCharge' + ' -w ' + f + ' -o ' + fout + ' -b '
                        print cmd
                        subprocess.call(cmd+'\n',shell=True)


def CollectSignalYields(grid,thUnc,nameTag,analysis,SRs,fittypetag):
    for SR in list(SRs.split("_")):
        if SR == "": continue
        if  not "excl" == fittypetag:
            return 0
        folderNameBase=grid+'_'+thUnc+nameTag+'_Excl_Job*'+analysis
    
        import pathUtilities,glob,os,fnmatch,signalSameSignTools
    
        resultsDir=pathUtilities.histFitterSource()+'/results/'
        
        # find list of directories
        if not "bkg" == fittypetag and not "disc" == fittypetag:
            massesDict = signalSameSignTools.getRunnumberMassesDictSS(grid)
    
        fout = open(pathUtilities.histFitterUser()+'/Yields/'+grid+'_'+thUnc+nameTag+'_Excl_SignalYields.txt', 'w')
    
        print "creating output file",grid+'_'+thUnc+'_'+nameTag+'_Excl_SignalYields.txt'
    
        for root, dirs, files in os.walk(resultsDir):
            for name in dirs:
                #print 'found folder',name
                #print 'matching with',folderNameBase
                if fnmatch.fnmatch(name, folderNameBase):
                    print 'scanning folder',(os.path.join(root, name))
                    fileList=glob.glob(os.path.join(root, name)+'/'+grid+'*combined_NormalMeasurement_model.root')
                    
                    for f in fileList:
                        print 'reading file',f
                        # extract sample name
                        one=f.split('/')[-1]
                        print one
                        if "GG_Rpv331" in grid:
                            dsid=f.split('/')[-1].split('_')[2][6:13]
                        else:
                            dsid=f.split('/')[-1].split('_')[1][6:13]
                        print 'looking at sample ',dsid
                        # get masses
                        masses=massesDict[dsid]
                        # read histo
                        infile= TFile(f,"READ")
                        sighisto=infile.Get(SR+'_cuts_hists/signal'+dsid+'/hsignal'+dsid+'Nom_'+SR+'_obs_cuts')
                        nsig=0
                        errsig=0
                        if 'TH1F' in type(sighisto).__name__:
                            # get counts
                            nsig=sighisto.GetBinContent(1)
                            errsig=sighisto.GetBinError(1)
                            print 'counts',nsig,'error',errsig
                        fout.write('{0} {1} {2} {3}\n'.format(masses[0],masses[1],nsig,errsig))
    
        fout.close()
