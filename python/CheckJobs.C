#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include "TString.h"
#include <string>
#include <map>
#include "TROOT.h"
#include <boost/algorithm/string.hpp>
#include <cstdlib>
//#include "RooStats/HypoTestInverterResult.h"


void Gettokens(std::string& str, char delim, std::vector<std::string>& tokens);

std::map<std::string,std::vector<std::string> > FillMap(std::string filename);

void RemovePreviousLogs(std::string filename);

bool LookForString(std::string file,std::string phrase);

bool IsJobRunning(TString JobName,std::string job,std::string jobID); 

bool LogsExist(TString job);

std::string getJobID(std::string job);

void CheckJobs(std::string name){


  string lumiTag="138965";

  string MissingSigFile = "InputTrees/signal."+lumiTag+".root does not exist";
  string MissingBkgFile = "InputTrees/\\w*."+lumiTag+".root does not exist";
  string MissingBkgFileError = "^SysError in <TFile::ReadBuffer>: error reading from file [\\/A-Za-z0-9_\\.\\/]*InputTrees/\\w*."+lumiTag+".root (Input/output error)";
  string MissingSigFileError = "^SysError in <TFile::ReadBuffer>: error reading from file [\\/A-Za-z0-9_\\.\\/]*InputTrees/signal."+lumiTag+".root (Input/output error)";
  string MissingTree = "Error in <TChain::AddFile>: cannot find tree with name";
  string MissingBkgFileError2 = "^Error in <TFile::ReadBuffer>: error reading all requested bytes from file [\\/A-Za-z0-9_\\.\\/]*InputTrees/\\w*."+lumiTag+".root";
  string MissingSigFileError2 = "^Error in <TFile::ReadBuffer>: error reading all requested bytes from file [\\/A-Za-z0-9_\\.\\/]*InputTrees/signal."+lumiTag+".root";
  string BadFile = "^Error in <TFile::Init>: file [\\/A-Za-z0-9_\\.\\/]*InputTrees/\\w+."+lumiTag+".root is truncated at";
  string Terminated = "Job terminated";
  string Killed = "Job removed by SYSTEM_PERIODIC_REMOVE due to wall time exceeded allowed max";
  string Aborted = "Job was aborted by the user";

  std::map< std::string,std::vector<std::string> > Job_key;

  Job_key=FillMap(name);


  int jobs_to_submit=0;
  int totalfailed=0;

  int total_missing_signal=0;
  int total_missing_bkg=0;
  int total_terminated=0;
  int total_aborted=0;
  int total_unknown=0;
  int total_badfit=0;
  int total_killed=0;
  int total_running=0;
  int total_missing_sigFile=0;
  int total_missing_tree=0;
  int total_missing_logs=0;
  int total_badFile=0;

  ofstream myfile ("ToSubmit.txt");

  std::system("condor_q >  RunningJobs.txt");


  //Loop over all jobs
  for (std::map<std::string,std::vector<std::string> >::iterator it=Job_key.begin(); it!=Job_key.end(); ++it){

      string path="../HistFitter/results/";
    
      TString JobName=it->first;
    
      if (JobName.Contains("UL")) JobName=path+JobName+"_output_upperlimit.root";
      else if (JobName.Contains("excl")) JobName=path+JobName+"_output_hypotest.root";


      std::vector<std::string> hypo_test=it->second;


      bool failJob=false;

      int counter=0;
      int bad_fit=0;
      int missing_signal=0;
      int huge_output=0;
      int terminus=0;
      int missing_bkg=0;
      int aborted=0;
      int missing_sigFile=0;
      int missing_tree=0;
      int missing_logs=0;
      int bad_file=0;

      RemovePreviousLogs(it->first);

      string jobID = getJobID(it->first);

      bool JobRunning=IsJobRunning(JobName,it->first,jobID);

      //check if job is running
      if (JobRunning){
          std::cout <<"-- Job still **RUNNING**...: " << it->first << std::endl;
          total_running+=1;
      }
      //if job finished, check the job was not killed: huge output or time of execution exceded!
      else if (LookForString("scripts/log/"+it->first+"."+jobID+".log",Killed)){

          total_killed+=1;
          huge_output +=1;

          counter += 1;
          failJob = true;

          std::cout << "-- Job killed by the system  --> " << it->first << std::endl;
      }
      //if job finished, check the job was not aborted
      else if (LookForString("scripts/log/"+it->first+"."+jobID+".log",Aborted)){

          aborted +=1;
          total_aborted+=1;

          counter += 1;
          failJob = true;

          std::cout << "-- Job aborted  --> " << it->first << std::endl;
      }
      //if job finished, check that *.out and *.err files exist. If they don't, then tag the job to be resubmit (job probably failed, or fit is wrong...)
      else if (LogsExist(it->first+"."+jobID)==false && LookForString("scripts/log/"+it->first+"."+jobID+".log",Terminated)){

          missing_logs += 1;
          counter += 1;
          failJob = true;

          total_missing_logs+=1;
          std::cout << "-- Job probably failed: missing *.out or  *.err files  --> " << it->first << std::endl;
      }
      //if job finished, check that it didn't miss any signal file
      else if (LookForString("scripts/error/"+it->first+"."+jobID+".err",MissingSigFile) || 
               LookForString("scripts/output/"+it->first+"."+jobID+".out",MissingSigFile) ||
               LookForString("scripts/error/"+it->first+"."+jobID+".err",MissingSigFileError) || 
               LookForString("scripts/output/"+it->first+"."+jobID+".out",MissingSigFileError) ||
               LookForString("scripts/error/"+it->first+"."+jobID+".err",MissingSigFileError2) ||
               LookForString("scripts/output/"+it->first+"."+jobID+".out",MissingSigFileError2) ) {
          missing_sigFile += 1;
          counter += 1;
          failJob=true;

          std::cout <<"-- Job failed: signal file has not been used!  -> " << it->first << std::endl;

          total_missing_sigFile+=1;

      }
      //if job finished, check that it didn't miss bkg any file
      else if (LookForString("scripts/error/"+it->first+"."+jobID+".err",MissingBkgFile) || 
               LookForString("scripts/output/"+it->first+"."+jobID+".out",MissingBkgFile)  || 
               LookForString("scripts/error/"+it->first+"."+jobID+".err",MissingBkgFileError) || 
               LookForString("scripts/output/"+it->first+"."+jobID+".out",MissingBkgFileError) ||
               LookForString("scripts/error/"+it->first+"."+jobID+".err",MissingBkgFileError2) ||
               LookForString("scripts/output/"+it->first+"."+jobID+".out",MissingBkgFileError2) ) {
          missing_bkg +=1;
          failJob=true;
          counter += 1;

          std::cout <<"-- Job failed : Bkg files have not been used!!  -> " << it->first << std::endl;

          total_missing_bkg+=1;

       }
       // if job finished, check that .root files are fine
       else if (LookForString("scripts/error/"+it->first+"."+jobID+".err",BadFile) ||
                LookForString("scripts/output/"+it->first+"."+jobID+".out",BadFile)){

           bad_file +=1;
           failJob=true;
           counter += 1;

           std::cout <<"-- Job to not be trusted...: some *.root files are bad  -> " << it->first << std::endl;
           total_badFile+=1;
       }
       //if job finished, check that it didn't run with a missing tree
       else if  (LookForString("scripts/error/"+it->first+"."+jobID+".err",MissingTree) || 
                 LookForString("scripts/output/"+it->first+"."+jobID+".out",MissingTree)){
          missing_tree += 1;
          failJob=true;
          counter += 1;
          std::cout <<"-- Job failed : One of the trees is missing in the ntuple!  -> " << it->first << std::endl;

          total_missing_tree+=1;

      }

       //if job is not running, and ntuples were properly used, then perform other checks
        if (failJob==false && JobRunning==false){ 

            TFile *pFile = new TFile(JobName);

            //if output file exists check that job finished well 
            if (pFile->IsOpen()){
    
     	        for (int i=0; i<hypo_test.size(); i++){

                    if (!pFile->GetListOfKeys()->Contains(("hypo_"+hypo_test[i]).c_str())){

                        failJob=true;
                        counter +=1;

                        std::string phrase="***nominal sample "+hypo_test[i]+" is empty for channel ";

                        if (pFile->GetListOfKeys()->Contains(("debug_"+hypo_test[i]).c_str())) {
                            bad_fit +=1;
                            total_badfit+=1;
                        }

                        if (LookForString("scripts/output/"+it->first+"."+jobID+".out",phrase)) {
                            missing_signal +=1;
                            total_missing_signal+=1;
                        }
                        if (bad_fit==0 && missing_signal==0 && LookForString("scripts/log/"+it->first+"."+jobID+".log",Terminated) ) {
                            terminus +=1;
                            total_terminated+=1;
                        }

                        if (bad_fit==0 && missing_signal==0 && terminus==0 ){
                            std::cout <<"-- Job failed: unknown reason..." << it->first <<  std::endl;
                            total_unknown+=1;
                        }
                        else{ 
                            std::cout <<"-- Job failed: " << it->first << " --> Found only " << hypo_test.size()-counter << " workspaces from " << hypo_test.size() << ":" << std::endl;
                        }

        	    }//if file is open 
 
    	        }//end loop over hypo_test

                pFile->Close();
         
            }//end if file open
            else {
                //if root file does not exist, check what happened.
                bool TerminatedJob=LookForString("scripts/log/"+it->first+"."+jobID+".log",Terminated);
 
                if (TerminatedJob){
                    std::cout <<"-- Job failed: No .root files but Job terminated -> " << it->first << std::endl;
                    counter += 1;
                    terminus += 1;           
                    total_terminated += 1;
                        
                    failJob=true;            
                    myfile << it->first << std::endl;
                }
                else{
                    std::cout << "-- Job still with unknown state...: " << it->first << std::endl;      
                    myfile << it->first << std::endl;

                    total_unknown+=1;
                }             
            }//end if root file does not exist
  
        }// end else failed=false

        if (failJob==true  && JobRunning==false){

            totalfailed +=1;

            std::cout <<"------- Bad fit points: "<< bad_fit << std::endl;
            std::cout <<"------- Missing sample: "<< missing_signal << std::endl;
            std::cout <<"------- Terminated: "<< terminus << std::endl;
            std::cout <<"------- Aborted: "<< aborted << std::endl;
            std::cout <<"------- Killed by the system: "<< huge_output << std::endl;
            std::cout <<"------- Missing bkg file: "<< missing_bkg << std::endl;
            std::cout <<"------- Missing signal file: "<< missing_sigFile << std::endl;
            std::cout <<"------- Missing missing tree: "<< missing_tree << std::endl;
            std::cout <<"------- Bad file: "<< bad_file << std::endl;
            std::cout <<"------- Missing logs: " << missing_logs << std::endl; 
            if (missing_signal != counter &&  counter >0) myfile << it->first << std::endl;
            else std::cout << "---> Nothing to do (failed jobs are due to signal yield==0 for that selection or missing sample)... **Job will not be resubmitted!**" << std::endl;

            if (missing_signal != counter && counter>0){
                jobs_to_submit +=1;
            }

            std::cout << "---> Check output file here :" << JobName << std::endl;

        }//if failed job

    }//end loop over jobs


    myfile.close();



    std::cout << "- Total failed jobs : " << totalfailed << std::endl;

    if (jobs_to_submit== 0) std::cout << "## ***** There are NO jobs to submit *****" << std::endl;
    else std::cout << "##  Number of jobs to submit :" << jobs_to_submit << std::endl;

    std::cout << "*** Summary of submission :" << std::endl;
    std::cout << "- Jobs running: "<< total_running << std::endl;
    std::cout << "- Jobs bad fit: "<< total_badfit << std::endl;
    std::cout << "- Jobs with missing signal: "<< total_missing_signal << std::endl;
    std::cout << "- Jobs with missing signal file: "<< total_missing_sigFile << std::endl;
    std::cout << "- Jobs with missing bkg file: "<< total_missing_bkg << std::endl;
    std::cout << "- Jobs with missing tree: "<< total_missing_tree << std::endl;
    std::cout << "- Jobs with bad *.root files: "<< total_badFile << std::endl;
    std::cout << "- Jobs aborted: "<< total_aborted << std::endl;
    std::cout << "- Jobs terminated: "<< total_terminated << std::endl;
    std::cout << "- Jobs killed: "<< total_killed << std::endl;
    std::cout << "- Jobs with missing logs: "<< total_missing_logs << std::endl;
    std::cout << "- Jobs failed unkown reason: "<< total_unknown << std::endl;


 return;
}

std::string getJobID(std::string job){

 std::string jobID = "";
 TString file ="";

 int res=std::system(("find scripts/log/ -name \""+job+".*\" "+" > tempJobID.txt").c_str());

 ifstream inFile;
 inFile.open("tempJobID.txt");
 if (!inFile) {
        cout << "Unable to open file";
        exit(1); // terminate with error
 }     
 else{
     inFile >> file;

     inFile.close();
     int res1 = std::system("rm tempJobID.txt");
     file = file.ReplaceAll("scripts/log/"+job+".","");
     jobID = file.ReplaceAll(".log","");

}
 

 //std::cout << " Job ID : " << jobID << std::endl;

 return jobID;
}
bool IsJobRunning(TString JobName,std::string job,std::string jobID){

    //string jobID = getJobID(job);


    bool running=false;

    int res=std::system(("grep -r \""+jobID+"\" RunningJobs.txt").c_str());

    if (res==0) running=true;
 
    return running;
}

void RemovePreviousLogs(std::string filename){

    system(("./RemoveOldLogs.sh "+filename+".").c_str());

    return;
}

bool LookForString(std::string file,std::string phrase){

    bool failed=false;

    int res=std::system(("grep -P -r \""+phrase+"\" "+file).c_str());

    if (res==0) failed=true;

    return failed;

}
bool LogsExist(TString job){

    ifstream fileOut(("scripts/output/"+job+".out").Data());
    ifstream fileErr(("scripts/error/"+job+".err").Data());

    if(!fileOut || !fileErr) return false;   
    else return true;
}
std::map<std::string,std::vector<std::string> > FillMap(std::string filename){

   std::map<std::string,std::vector<std::string> > mymap;
   std::string line;

   ifstream myfile (filename);

   if (myfile.is_open()){

       while ( getline (myfile,line) ){

           std::cout << line << std::endl;
           std::vector<std::string> temp;

           std::istringstream ss(line);
           std::string job;
           std::string signal;

           ss >> job >> signal;

           Gettokens(signal,';',temp);

           if (temp.size()>0) mymap[job]=temp;
           else std::cout << "... Something went wrong: ensure that the file containing the job names has also the hypotest names!!!"<<std::endl;
       }
       myfile.close();
    }
    else std::cout << "Unable to open file: "<< filename <<  std::endl;


 return mymap;
}
void Gettokens(std::string& str, char delim, std::vector<std::string>& tokens)
{
    tokens.clear();
    std::istringstream iss(str);
    std::string token;
    while ( std::getline(iss, token, delim) ){
         boost::algorithm::trim(token);
         token=token;
         tokens.push_back(token);
    }
    return;
} 
