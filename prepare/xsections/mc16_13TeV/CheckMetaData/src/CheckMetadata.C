#include <vector>
#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <algorithm>
#include <math.h>
#include <TLorentzVector.h>
#include <string>
#include <fstream>
#include <iomanip>
#include "../include/GetCorrectInfo.h"

void CheckMetadata(string filename){

	string PATH_input = "../include/"+filename;

	string PATH_output = "../include/Wrong_Info_DSID_"+filename;

	ofstream Outputs(PATH_output.c_str());

	FILE* Inputs = fopen(PATH_input.c_str(),"r");
	char CurrentFileLine[99999];
	char CurrentFile[99999];
	string CurrentFileName;
	int Num_line = 0;
	while (fgets(CurrentFileLine, sizeof(CurrentFileLine), Inputs)){
		sscanf(CurrentFileLine, "%s", CurrentFile);
		CurrentFileName = CurrentFile;
		Num_line ++;


		TString Line = CurrentFileName;
		cout << "Now processesing... " << Line <<endl;
		
		if (Line.Contains("dataset")) {continue;}
//		if (Line.Contains("#lsetup")) {Outputs << "#lsetup  \"asetup AthAnalysis,21.2.63\" pyAMI" << endl; continue;}
//		if (Line.Contains("#getMetadata.py")) {Outputs << "#getMetadata.py --timestamp=\"2019-02-14 14:32:10\" --physicsGroups=\"SUSY,PMG,MCGN\" --fields=\"ldn,dataset_number,subprocessID,crossSection,kFactor,genFiltEff,crossSectionTotalRelUncertUP,crossSectionRef\" --inDsTxt=\"" <<filename << "\"" << endl; continue;}

		TObjArray *ArryLine = Line.Tokenize(";");
		TObjString *ObjDataSet = (TObjString*)ArryLine->At(1);
		TObjString *ObjDSID = (TObjString*)ArryLine->At(0);
		TObjString *ObjXsec = (TObjString*)ArryLine->At(2);
		TObjString *ObjKFac = (TObjString*)ArryLine->At(4);
		TObjString *ObjGenEff = (TObjString*)ArryLine->At(3);
		TObjString *ObjRelUnc = (TObjString*)ArryLine->At(5);

		TString DataSet =ObjDataSet->GetString();
		TString DSID =ObjDSID->GetString();
		TString Xsec =ObjXsec->GetString();
		TString KFac =ObjKFac->GetString();
		TString GenEff =ObjGenEff->GetString();
		TString RelUnc =ObjRelUnc->GetString();
cout << DataSet << endl;
		TObjString *ObjProcess = (TObjString*)DataSet.Tokenize("_")->At(2);
		TObjString *ObjP1Mass = (TObjString*)DataSet.Tokenize("_")->At(4);

		TString Process = ObjProcess->GetString();
		TString P1Mass = ObjP1Mass->GetString();
cout << Process << "    " << P1Mass << endl;
		vector<string> CorrectInfo = GetCorrectInfo(Process, P1Mass);

		if ( atof(CorrectInfo.at(0).c_str()) != Xsec.Atof() ){

			cout << "Mass: " << P1Mass << " Xsec: " << setiosflags(ios::scientific) << atof(CorrectInfo.at(0).c_str())/1000.0 << " RelUnc: " << atof(CorrectInfo.at(1).c_str())/100.0 << endl;

			Xsec = to_string(atof(CorrectInfo.at(0).c_str())/1000.0);
			RelUnc = to_string(atof(CorrectInfo.at(1).c_str())/100.0);
			//		XsecRef = "XsecSUSY";


			//		Outputs << DataSet << ";" << DSID << ";" << SubID << ";" << setiosflags(ios::scientific) << atof(CorrectInfo.at(0).c_str())/1000.0 << ";" << KFac << ";" << GenEff << ";" << RelUnc << ";" << XsecRef << ";" << endl;
			Outputs  << DSID << "    " << DataSet << "    " << setiosflags(ios::scientific) << atof(CorrectInfo.at(0).c_str()) << "    " << GenEff << "    " << KFac << "    " << RelUnc << "    " << RelUnc << "    " << "NULL" << endl;
		}


	}
	return 0;

}


