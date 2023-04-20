#!/usr/bin/env python
import os, pathUtilities,signalSameSignTools
import json
from subprocess import check_output

# this is just a grep. returns the line(s) to be parsed by the next function
def lookForSample(runnumber,mc_version):

    dbline=check_output(["grep -r -P  \"^"""+runnumber+"\\s\" "+pathUtilities.xsectionsDirectory(mc_version)+"*"],shell = True) 
    #print "dbline is ",dbline
    dbline=dbline.replace("\t"," ")
    #print "dbline is ",dbline
    return [l for l in dbline.split(" ") if l!=""]


def processFile(fileIn,fileOut,gridName,SigNameSchema):

    if( pathUtilities.isIn2p3() ) : os.chdir(pathUtilities.histFitterUser()+"/plot/")
    else : os.chdir(pathUtilities.histFitterUser())

    print "Processing json file ",fileIn

    fin= open(fileIn, "r")
    data = [json.load(fin)]
    
    for d in data[0]:

        if 'm0' in d.keys() and 'm12' in d.keys() and 'chan' in d.keys():
            #print 'The JSON file already has m0, m12 and chan: will not add any field, and just plog in the xsec'
            pass
        else:
            massesDict = signalSameSignTools.getRunnumberMassesDictSS(gridName,SigNameSchema)
            #print massesDict
            # either the masses of the chan are missing
            # note that THIS SHOULD NOT HAPPEN
            #print 'WARNING: the json file is missing m0 or m12 or chan. Will try to add the missing fields, then adjust the xsec'

            if "m0" in d.keys():
                # we are reading a hypotest. we add the channel
		chan=-999
                for key,entry in massesDict.iteritems():
                    if entry==[d["m0"], d["m12"]]:
                        #print "FOUND DS ",key
                        chan=int(key)
                        break
                d["chan"]=chan
            else:
                # we are reading a upperlimit result, so we add the xsec, lookup done by channel
                print(massesDict)
                masses=massesDict[str(int(d['chan']))]
                d['m0']=masses[0]
                d['m12']=masses[1]



        xsec=-1
        kfac=-1
        feff=-1
        mc_version=gridName[2:4]

        dbentry = lookForSample(str(int(d['chan'])),mc_version)
        #print "got dbentry for sample",d['chan'],dbentry


        xsec= float(dbentry[2])
        feff= float(dbentry[3])
        kfac= float(dbentry[4])

        xsecCorrected=xsec*kfac*1000
        xsecUp=xsecCorrected*(1+float(dbentry[5]))
        xsecDown=xsecCorrected*(1-float(dbentry[6]))
        if float(dbentry[6])==0: xsecDown = xsecCorrected - (xsecUp - xsecCorrected) #if no value, then symmetrize uncertainty

        # hack to bypass the filter efficiency
        #feff=1 
        # update existing numbers with the correct ones
        if 'xsec' in d.keys():
            #print "xsec:",d['xsec'],",    overwriting xsec with ",xsec*kfac
            d["xsec"]=xsecCorrected
            d["xsecUp"]=xsecUp
            d["xsecDown"]=xsecDown

        if 'excludedXsec' in d.keys() and 'upperLimit' in d.keys():

            d["excludedXsec"]=d["upperLimit"]*xsecCorrected
            d["excludedXsecExp"]=d["expectedUpperLimit"]*xsecCorrected
            d["excludedXsecMinus1Sig"]=d["expectedUpperLimitMinus1Sig"]*xsecCorrected
            d["excludedXsecMinus2Sig"]=d["expectedUpperLimitMinus2Sig"]*xsecCorrected
            d["excludedXsecPlus1Sig"]=d["expectedUpperLimitPlus1Sig"]*xsecCorrected
            d["excludedXsecPlus2Sig"]=d["expectedUpperLimitPlus2Sig"]*xsecCorrected

    # this will replace the file, if existing
    fout= open(fileOut, "w")
    json.dump(data[0],fout)

def FillJsonFilesWithMissingInfo(harvestfilein,harvestfileout,SigNameSchema):

    #if( pathUtilities.isIn2p3() ) : os.chdir(pathUtilities.histFitterUser()+"/plot/")
    #else : os.chdir(pathUtilities.histFitterUser())

    print "about to read the json file ",harvestfilein
    
    gridName = ''
    for string in harvestfilein.split('_'):
        if string not in  ['Nominal','Up','Down']:
            gridName += string+'_'
        else:
            gridName = gridName.strip('_')
            break   
  

    processFile(harvestfilein,harvestfileout,gridName,SigNameSchema)

    #Looking for theory variations:
    try:
        processFile(harvestfilein.replace("Nominal","Up"),harvestfileout.replace("Nominal","Up"),gridName,SigNameSchema)
    except:
        print (">>> ... Can't find theory Up files. Skipping.")

    try:
        processFile(harvestfilein.replace("Nominal","Down"),harvestfileout.replace("Nominal","Down"),gridName,SigNameSchema)
    except:
        print (">>> ... Can't find theory Down files. Skipping.")


    try:
        processFile(harvestfilein.replace("Nominal","upperlimit"),harvestfileout.replace("Nominal","UpperLimit"),gridName,SigNameSchema)
    except:
        print (">>> ... Can't find theory UL files. Skipping.")

