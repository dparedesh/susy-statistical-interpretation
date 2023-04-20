import os

motherDirectory="/".join(os.getcwd().split("/")[:-1])

def histFitterTopDirectory():

    return motherDirectory

def eosDataDirectory():
    if os.getenv('USER')=='ptornamb':
        return  "root://eosatlas.cern.ch//eos/atlas/user/p/ptornamb/SS_HistFitter/"
    if os.getenv('USER')=='disimone':
        return  "root://eosatlas.cern.ch//eos/atlas/user/d/disimone/SSHistFitter/InputTrees/"
    if os.getenv('USER')=='fcardill':
        return "root://eosatlas.cern.ch//eos/atlas/user/f/fcardill/SSHistFitter/"
    if os.getenv('USER')=='dparedes':
        return '/eos/user/d/dparedes/SUSYComplex/'


def remoteDataDirectory():
    if isFreiburg():
        if os.getenv('USER')=='pt1009':
            return  '/storage/users/pt1009/SS_HistFitter/run2/InputTrees/'
        if os.getenv('USER')=='ad1029':
            return  '/storage/users/ad1029/FitInputs/'
        if os.getenv('USER')=='fc12':
            return '/home/fc12/HistFitter2017/Run/HistFitterUser/InputTrees/'

def isCambridge():
    import subprocess
    return 'cam.ac.uk' in subprocess.Popen('hostname -d', stdout=subprocess.PIPE, shell=True).communicate()[0]

def isFreiburg():
    import subprocess
    return 'freiburg.de' in subprocess.Popen('hostname -d', stdout=subprocess.PIPE, shell=True).communicate()[0]

def isIn2p3():
    import subprocess
    return 'in2p3.fr' in subprocess.Popen('hostname -d', stdout=subprocess.PIPE, shell=True).communicate()[0]

def xsectionsDirectory(version):

    return motherDirectory+'/prepare/xsections/mc'+version+'_13TeV/'


def pythonDirectory():

    return motherDirectory+'/python'


def macrosDirectory():

    return motherDirectory+'/macroSS'


def histFitterSource():

    return motherDirectory+'/HistFitter'



def histFitterUser():
 
   return motherDirectory+'/HistFitterUser'


def histFitterResults():

    return motherDirectory+'/HistFitter'
