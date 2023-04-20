## General description:
Python scripts stored in this directory are mainly used to generate correct commands pass to HistFitter to do fit or getting yields, tables or plots

## Scripts are used:

### generateCommands.py:
* main script used to generate the command pass to HistFitter.
* if you are not running in batch mode, it will run fit for signal point one after the other.
* if you are running in batch mode, it will run fit for every signal point parallel to save time.
* `NOTE!` 
    * `lumitag` in the file need to be modified according to your input file (should be the same value what in your input file name)
    * `runNameTag` can be changed to what you prefer. 
    * for all the possible options, you should have a look at the first few lines in the script
    
### fitConfigSS3L.py:
* configuration file for HistFitter
* all parameters should be properly passed from `generateCommands.py` file
* in this you should/can implement:
    * configures for getting CLs scanning results:
        * configMgr.nTOYs
        * configMgr.calculatorType
        * configMgr.nPoints
        * configMgr.testStatType
        * ...
    * definitions of regions
    * individual weights used for calculation of event weight and weighted systematics
    * categories of backgrounds
    * tree based systematics that we should included

### jsonToBands.py:

 Script used to read the mass points `m0` and all `excludedXsec*` from the json file and create expected, observed, and 1 and 2-sigma bands in TGraphs.    Also, it will save the plots for `theory x-section`, including the systematic variations. This script is **not** used to create 2D exclusion contours, but only when the goal is to plot the upper-limit on x-sections as a function of the generated mass point `m0`    

### CheckJobs.C:

 Script used to check the status of the exclusion jobs run in batch. It will write a file with the name of the failed jobs. This file can be used to resubmit failed jobs.
 
### RemoveOldLogs.sh:

 This is bash script used to remove all the old logs file corresponding to the same job. It is called internally by CheckJobs.C


### Helper.py:

 This is a python script containing several methods and classes definitions used by the different scripts in the whole tool. 

### pathUtilities.py:
* script for handling the PATH that we might used
* one should add the needed PATH according to your case which is `mandatory`!

### CollectSignalYields.py:
* a script used for getting yields, systematics breakdowns and fit results
* all tables for yields and systematics breakdown should be stored in HistFitterUser directory

### FillJsonFilesWithMissingInfo.py:
* a script for checking if there is anything missing in the after fit Json files.


### massCheck.py:
* a script helped getting the mass information for each files
* need to be modified when a new grid was added

