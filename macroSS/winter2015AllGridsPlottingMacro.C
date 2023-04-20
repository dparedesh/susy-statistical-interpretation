#include "contourmacros/CombinationGlob.C"
#include "TColor.h"
#include <TFile.h>
#include <TTree.h>
#include <Riostream.h>
//#include "zleptonoffciallcontours.C"
#include <algorithm>
//#include "contourmacros/SUSY_m0_vs_m12_all_withBand_cls.C"
//#include "summary_harvest_tree_description.h"
//#include "../../common/ATLAS_EPS_contours.C"

//#include "summer2013ExclusionsOtherAnalyses/summer2013ExclusionLimittherAnalyses.C"
//#include "summer2013ExclusionsOtherAnalyses/plotsForPaper/SimplifiedModels_7TeV.C"
//#include "summer2013ExclusionsOtherAnalyses/plotsForPaper/GMSB_Dilepton_7TeV.C"

//#include "../share/mSugraGridtanbeta30_gluinoSquarkMasses_TJExtended20140114_withSomeFunnyFeatures_SquarkMassesMacroEdited.C"

TH2F* Draw1fbLimit();

void PlotFunc3Par(double p0, double p1,double p2,double p3,double xmin,double xmax);
void PlotFunc4Par(double p0, double p1,double p2,double p3,double p4,double xmin,double xmax);

void DrawUpperLimits(const char*upperLimitFile,TH1*frame);


enum SIGNAL_MODEL
{
  SUSY_GTT,
  SUSY_COMPR_GTT,
  SUSY_TEST,
  SUSY_BTT,
  SUSY_GG2STEPWZ,
  SUSY_TT2STEP,
  SUSY_GSL,
  SUSY_GG_RPV321,
  SUSY_GG_RPV331,
  SUSY_DD_RPV321,
  SUSY_DD_RPV331,
  SUSY_UNKNOWN
};
SIGNAL_MODEL model = SUSY_UNKNOWN;

void CompressedCurve(bool draw){
  if(!draw) return;
  TFile* fIn = new TFile("/home/fc12/HistFitter2017/Run/macroSS/SusyComprGtt_observed_exclusion_line_MoriondV6.root");
  TGraph *gIn = (TGraph*)fIn->Get("obs_exclusion_line");
  if(!gIn) return;
  TGraph * gOut = new TGraph();
  for(int n(0); n<gIn->GetN(); n++){
    double x(0), y(0);
    gIn->GetPoint(n,x,y);
    gOut->SetPoint(n,x,y+(x-2*175));
  }
  gOut->SetLineWidth(3);
  gOut->SetLineStyle(1);
  gOut->SetLineColor(kGreen);
  gOut->Draw("l same");
  return;
}

void Run1Curve(TString grid, bool doSS=true, bool doExp=false){

  /*
  TFile* f =new TFile("/home/fc12/HistFitter2016/Run/Run1Lim/"+grid+"_mergedHists.graphs.root");
  TGraph* g = (TGraph*)f->Get("combined_observed_0");
  TGraph* gE = (TGraph*)f->Get("combined_expected_0");
  TGraph* gSS = (TGraph*)f->Get("SS3L-jets-ETmiss_observed_0");
  */

  TFile* f = new TFile("/afs/cern.ch/work/p/ptornamb/SS3L-Full/SS3l-FullLumi-HistFitter/FullRun2/Run1Lim/allCont.root");
  TGraph *g(0);
  if(grid=="Gtt")    g = (TGraph*)f->Get("SS3L_GG_ttn1_observed");
  if(grid=="2step")  g = (TGraph*)f->Get("SS3L_GG_2stepWZ_observed");
  if(grid=="Btt")    g = (TGraph*)f->Get("SS3L_BB_onestepC1__observed");
  if(grid=="GSL")    g = (TGraph*)f->Get("SS3L_GG_N2_SLN1_4fl_observed");
  
  if(grid=="Gtt" || grid=="2step" || grid=="Btt" || grid=="GSL"){
    g->SetLineWidth(3);
    g->SetLineStyle(1);
    g->SetLineColor(kBlue);
    g->Draw("l");
  }

  if(grid=="2step"){

    TFile* f2 = new TFile("/storage/users/pt1009/SS_HistFitter/run2/Run1Lim/MultiJet_2Step.root");
    TGraph *g2(0);
    g2 = (TGraph*)f2->Get("obsCLs");
    double x,y;

    for(int i=0; i<g2->GetN();i++){
      g2->GetPoint(i,x,y);
    }
    for(int i=0; i<96;i++){
      g2->RemovePoint(0);
    }

    for(int i=0; i<27;i++){
      g2->RemovePoint(g2->GetN()-1);
    }
    
    g2->SetLineWidth(3);
    g2->SetLineStyle(1);
    g2->SetLineColor(kViolet);
    g2->Draw("l same");
    
  }

  if(grid=="RPV_GG"){

    cout<<"Getting contour from 8 TeV.."<<endl;
    TFile* f3 = new TFile("/storage/users/pt1009/SS_HistFitter/run2/Run1Lim/Gtt_RPV_mergedHists.graphs.root");
    TGraph *g3(0);
    g3 = (TGraph*)f3->Get("combined_observed_0");
    double x,y;

    /*for(int i=0; i<g3->GetN();i++){
      g3->GetPoint(i,x,y);                                                                                       
      cout<<"i: "<<i<<"\t x: "<<x<<"\t y: "<<y<<endl;                                                            
      }*/

    for(int i=0; i<15;i++){
      g3->RemovePoint(0);
    }

    cout<<"Npoints: "<<g3->GetN()<<endl;

    /*for(int i=0; g3->GetN();i++){
      g3->GetPoint(i,x,y);
      cout<<"i: "<<i<<"\t x: "<<x<<"\t y: "<<y<<endl;
      }*/
    for(int i=0; i<34;i++){
      g3->RemovePoint(g3->GetN()-1);
    }
    
    g3->SetLineWidth(3);
    g3->SetLineStyle(1);
    g3->SetLineColor(kBlue);
    g3->Draw("l");

  }

  /*
  // To draw expected too:
  if(doExp){
    gE->SetLineWidth(3);
    gE->SetLineStyle(7);
    gE->SetLineColor(kOrange);
    gE->Draw("l");
  }
  // To draw SS/3L only too:
  if(doSS){
    gSS->SetLineWidth(3);
    gSS->SetLineStyle(2);
    gSS->SetLineColor(kBlue);
    gSS->Draw("l");
  } 
  */
  
} 


TGraph* joinGraphs(TGraph* gr1, TGraph* gr2){

  TGraph* outGraph = new TGraph();
  Double_t x, y;
  Int_t count = 0;
  for (Int_t i=0; i<gr1->GetN(); i++) {
    gr1->GetPoint(i, x, y);
    cout<<"Set "<<x<<" "<<y<<endl;
    outGraph->SetPoint(count, x, y);
    count ++;
  }
  for (int i=0; i<gr2->GetN(); i++) {
    gr2->GetPoint(i, x, y);
    cout<<"Set "<<x<<" "<<y<<endl;
    outGraph->SetPoint(count, x, y);
    count ++;
  }
  return outGraph;
}


TGraph* ContourGraphWithAdding( TH2F* hist, double xmin = 0, double xmax = 6000) {
  TGraph* gr0 = new TGraph();
  TH2F* h = (TH2F*)hist->Clone();
  TGraph*  gr1 = (TGraph*)gr0->Clone(h->GetName());
  cout<<"Taking "<<h->GetName()<<endl;
  h->SetContour( 1 );
  cout<<"Just limited range to: "<<xmin<<" "<<xmax<<endl;

  double pval = CombinationGlob::cl_percent[1];
  double signif = TMath::NormQuantile(1-pval);
  cout<<"Set contour level "<<signif<<endl;
  h->SetContourLevel(0, signif );
  // draw contours
  h->Draw("CONT LIST");
  h->SetDirectory(0);
  gPad->Update();
  // get contours from plot
  TObjArray *contours = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
  Int_t ncontours     = contours->GetSize();
  cout << "Found " << ncontours << " contours " << endl;
  TList *oldlist = (TList*)contours->At(0);
  cout<<"Entries oldlist: "<<oldlist->GetEntries()<<endl;
  TList *list = new TList();
  
  if(oldlist->GetEntries()>2){
    int i=0;
    TIter next(oldlist);
    TObject* object = 0;
    while ((object = next()))
      {
	TGraph* tmp  = (TGraph*) oldlist->At(i);
	cout<<"tmp: "<<tmp->GetN()<<endl;
	if(i!=0){
	  list->Add(object);
	}
	i++;
      }
  }
  else
    list = oldlist;
  

  cout<<"Entries list: "<<list->GetEntries()<<endl;

  if (list->GetEntries() == 0) return NULL;
  else{
    // Find the longest graph
    // the two longest graphs?
    TGraph* tempgr  = (TGraph*) list->First();
    TGraph* gr2 =  (TGraph*) list->First();
    
    int npoints1 = gr1->GetN();
    cout<<"npoints1 before: "<<npoints1<<endl;
    
    //gr2->Set(0);

    /*    while(tempgr) {
      cout<<"tempgr before: "<<tempgr->GetN()<<endl;
      cout<<"gr1 points before: "<<gr1->GetN()<<endl;
      cout<<"gr2 points before: "<<gr2->GetN()<<endl;

      //if (tempgr->GetN() > npoints1) {
	gr2 = gr1;
	gr1 = tempgr;
	npoints1 = gr1->GetN();
	//}
      cout<<"npoints1 after: "<<npoints1<<endl;

      cout<<"tempgr after: "<<tempgr->GetN()<<endl;
      cout<<"gr1 points: "<<gr1->GetN()<<endl;
      cout<<"gr2 points: "<<gr2->GetN()<<endl;

      tempgr = (TGraph*) list->After(tempgr);
      }*/

    gr1 = (TGraph*)list->First();
    gr2 = (TGraph*)list->At(1);

    TGraph* outGraph = new TGraph();
    double xMin1; 
    double xMin2;
    double y;

    //gr1->GetPoint(gr1->GetN(), xMax1, y);
    gr1->GetPoint(0, xMin1, y); 
    gr2->GetPoint(0, xMin2, y);

    cout<<"xMin1: "<<xMin1<<"  xMin2: "<<xMin2<<endl;
    cout<<"-------------------"<<endl;
    cout<<"gr1 points: "<<gr1->GetN()<<endl;
    cout<<"gr2 points: "<<gr2->GetN()<<endl;

    /*TCanvas *pippo = new TCanvas("pippo","pippo");
    pippo->cd();
    pippo->Divide(2,2,0,0);
    pippo->cd(1);
    cout<<"------GR1------"<<endl;
    gr1->Print();
    gr1->DrawClone("la");
    pippo->cd(2);
    cout<<"------GR2------"<<endl;
    gr2->Print();
    gr2->DrawClone("la");
    */
    cout<<"-------------------"<<endl;
    cout<<"gr1 points: "<<gr1->GetN()<<endl;
    cout<<"gr2 points: "<<gr2->GetN()<<endl;
    
    if (xMin2 > xMin1) outGraph = joinGraphs(gr1, gr2);
    else outGraph = joinGraphs(gr2, gr1);
    cout<<"outGraph points: "<<outGraph->GetN()<<endl;    
    /*pippo->cd(3);
    outGraph->Print();
    outGraph->DrawClone("la");
    pippo->WaitPrimitive();
    */

    return outGraph;
  }
}//close function

TGraph* removeArea(SIGNAL_MODEL model, TGraph* graph, double yMin, double yMax, TString type){
  // returns a new graph with a subset of the points removed, according to the model and the type
  double x1 = 0;
  double y1 = 0;
  double x2 = -1;
  double y2 = -1;
  TGraph *outGraph = new TGraph();

  const Int_t nPoints = graph->GetN();
  
  if (nPoints > 0){

  const Int_t N = nPoints;
  Double_t x[N+1], y[N+1];
  Double_t x0, y0;
  for(int i = 0; i < N; i++) {
    graph->GetPoint(i, x0, y0);
    x[i] = x0;
    y[i] = y0;
  }
  
  // exclusions by grid:
  if (model == SUSY_GTT){
    if (type == "observedUp"){
      x1 = 750;
      y1 = 0;
    } else if (type == "observedDown"){
      x1 = 750;
      y1 = 0;
    }
  }
  int count = 0;
  //adding initital points
  
  
  for (int i = 0; i < N; i ++){
    if ((((y[i] < (y1 - x1*(y2-y1)/(x2-x1) + x[i]*(y2-y1)/(x2-x1)) ) && (x2 > 0)) || 
	 ((x2 == -1) && x[i] > x1)) && ((y[i] > yMin && (y[i] < yMax)))){
      
      outGraph->SetPoint(count, x[i], y[i]);
      count ++;
      
      
    }
  }
  
  //set endpoint
  
  outGraph->SetPoint(count, x[N-1], 0);//add point to make it go to 0
  
  return outGraph;
  
  }
  
  else return outGraph;
  
}

TGraph* addPoints(SIGNAL_MODEL model, TGraph* graph, TString type, TString gridName, bool writeFile){

  // this returns a graph with some points added to it

  return graph;
  // skip all this for the time being

//  TGraph *outGraph = new TGraph();
//
//  Int_t nPoints = graph->GetN();
//  
//  Int_t N = nPoints;
//  Double_t x[N+1], y[N+1];
//  Double_t x0, y0;
//  for(int i = 0; i < N; i++) {
//    graph->GetPoint(i, x0, y0);
//    x[i] = x0;
//    y[i] = y0;
//  }
//  // TUNE HERE THE MAX NUMBER OF ADDITIONAL POINTS
//
//  double additionalPointsX[5] = 0;
//  double additionalPointsY[5] = 0;
//
//  // this is the *actual* number of additional points
//  int npoints=0;
//
//    if (model == SUSY_GLUINOSTOP){
//       additionalPointsX[0]  = {700};
//       additionalPointsY[0] = {700- 220};
//       npoints=1;
//
//    } else if (model == SUSY_GLUINOSTOPCHARM){
//      additionalPointsX[0]  = {350};
//      additionalPointsY[0] = {350- 200};
//      npoints=1;
//    } else if (model == SUSY_MSUGRA){
//    if (type == "expected"){
//      additionalPointsX[0]  = {230};
//      additionalPointsY[0] = {460};
//      npoints=1;
//    } else if (type == "expectedUp"){
//      additionalPointsX[0]  = {240};
//      additionalPointsY[0] = {440};
//       npoints=1;
//    } else if (type == "expectedDown"){
//      additionalPointsX[0]  = 240;
//      additionalPointsX[0]  = 240;
//      additionalPointsY[0] = {440, 470};
//    } else if (type == "observed"){
//      additionalPointsX[0]  = {230};
//      additionalPointsY[0] = {450};
//    } else if (type == "observedUp"){
//      additionalPointsX[0]  = {245};
//      additionalPointsY[0] = {455};
//    } else if (type == "observedDown"){
//    additionalPointsX[0]  = {220};
//    additionalPointsY[0] = {430};
//    } else{
//      additionalPointsX[0]  = {220};
//      additionalPointsY[0] = {430};
//    }
//  } else if (model == SUSY_SBOTTOMTOPCHARGINON60){
//    if (type == "expected"){
//      additionalPointsX[0]  = {538};
//      additionalPointsY[0] = {538 - 175};
//    } else if (type == "expectedUp"){
//      additionalPointsX[0]  = {485};
//      additionalPointsY[0] = {485- 175};
//    } else if (type == "expectedDown"){
//      double additionalPointsX[2]  = {485, 592};
//      double additionalPointsY[2] = {485 - 175, 592-175};
//    } else if (type == "observed"){
//      additionalPointsX[0]  = {485};
//      additionalPointsY[0] = {485- 175};
//    } else if (type == "observedUp"){
//      additionalPointsX[0]  = {502};
//      additionalPointsY[0] = {502- 175};
//    } else if (type == "observedDown"){
//      additionalPointsX[0]  = {455};
//      additionalPointsY[0] = {455- 175};
//    } else if (type == "SR1b"){
//      additionalPointsX[0]  = {515};
//      additionalPointsY[0] = {515-175};
//    }else if (type == "SR3Llow"){
//      additionalPointsX[0]  = {415};
//      additionalPointsY[0] = {415-175};
//    }else if (type == "SR3Lhigh"){
//      additionalPointsX[0]  = {450};
//      additionalPointsY[0] = {450-175};
//    } else{
//      additionalPointsX[0] = {250};
//      additionalPointsY[0] = {0};
//    }
//  
//} else if (model ==  SUSY_SBOTTOMTOPCHARGINONHALFC){
//    if (type == "expected"){
//      additionalPointsX[0]  = {478};
//      additionalPointsY[0] = {150};
//    } else if (type == "expectedUp"){
//      additionalPointsX[0]  = {460};
//      additionalPointsY[0] = {142};
//    } else if (type == "expectedDown"){
//      additionalPointsX[0]  = {460};
//      additionalPointsY[0] = {142};
//    } else if (type == "observed"){
//      additionalPointsX[0]  = {465};
//      additionalPointsY[0] = {144};
//    } else if (type == "observedUp"){
//      additionalPointsX[0]  = {480};
//      additionalPointsY[0] = {152};
//    } else if (type == "observedDown"){
//      additionalPointsX[0]  = {440};
//      additionalPointsY[0] = {132};
//    } else if (type == "SR1b"){
//      additionalPointsX[0]  = {445};
//      additionalPointsY[0] = {136};
//    }else if (type == "SR3Llow"){
//      additionalPointsX[0]  = {415};
//      additionalPointsY[0] = {120};
//    }else if (type == "SR3Lhigh"){
//      additionalPointsX[0]  = {418};
//      additionalPointsY[0] = {123};
//    } else{
//      additionalPointsX[0]  = {250};
//      additionalPointsY[0] = {0};
//    }
// 
//  } else if (model == SUSY_GMSB2D){
//    if (type == "SR0b"){
//      additionalPointsX[0]  = {67};
//      additionalPointsY[0] = {60};
//    }else if (type == "SR1b"){
//      additionalPointsX[0]  = {60};
//      additionalPointsY[0] = {60};
//    }else if (type == "SR3b"){
//      additionalPointsX[0]  = {56};
//      additionalPointsY[0] = {50};
//    }else if (type == "SR3Llow"){
//      additionalPointsX[0]  = {60};
//      additionalPointsY[0] = {52};
//    }else if (type == "observedDown"){
//      additionalPointsX[0]  = {75};
//      additionalPointsY[0] = {60};
//    } else{
//      double additionalPointsX  = 0;
//      double additionalPointsY = 0;
//    }
// 
//    }else if (model == SUSY_GG2STEPSLEP){
//      additionalPointsX[0]  = {380};
//      additionalPointsY[0] = {300};
//    } else if (model == SUSY_STRONGSQUARKSLEP){
//      additionalPointsX[0]  = {300};
//      additionalPointsY[0] = {220};
//
////   } else if (model == SUSY_GG2STEPSLEP){
////     additionalPointsX[0]  = {350};
////     additionalPointsY[0] = {250};
////   } else if (model == SUSY_GTB){
////     additionalPointsX[0]  = {400};
////     additionalPointsY[0] = {190};
////   } else if (model == SUSY_GG1STEPLSP60){
////     additionalPointsX[0]  = {690};
////     additionalPointsY[0] = {1};
//  // } else if (model == SUSY_RPV){
//  //   additionalPointsX[0] = {800};
//  //   additionalPointsY[0] = {200} ;
//   }  else {
//    double additionalPointsX = 0;
//    double additionalPointsY = 0;
// }
//
//  int count = 0;
//  if (additionalPointsX != 0){
//    for (int i = 0; i < sizeof(additionalPointsX) / sizeof(*additionalPointsX); i++){
//      outGraph->SetPoint(count, additionalPointsX[i], additionalPointsY[i]);
//      count ++;
//    }
//  }
//  for (int i = 0; i < N; i ++){
//      outGraph->SetPoint(count, x[i], y[i]);
//      count ++;
//  }
//
// Double_t x1, y1;
//  if ((type == "observed") || (type == "expected")){
//    cout<<type<<endl;
//    for (int i = 0; i < count; i ++) {
//      graph->GetPoint(i, x1, y1);
//      cout<<i<<", "<<x1<<", "<<y1<<endl;
//    }
//  }
//
//  //if (writeFile){
//    // hacky, I know, I am sorry. Works though.
//    TGraph* writtenGraph = outGraph->Clone(gridName+"_"+type);
//    TFile* openFile =new TFile("/r02/atlas/thibaut/histFitterSummer2013/HistFitterUser/MET_jets_2lep_SS/0807SameSignSummer2013PreliminaryExclusions.root", "UPDATE");
//    openFile->cd();
//    writtenGraph->Write();
//    openFile->Close();
//    //} 
//  return outGraph;
//
}


void GetExclusionFromFile(TString filePath, 
			  TString graphName, 
			  int lineColor, 
			  TString legendName,
			  TLegend *legend , 
			  TString drawOption = "same"){
							
  
  TFile* openFile = TFile::Open(filePath, "READ");
  TGraph* limitGraph = (TGraph*)openFile->Get(graphName)->Clone();
  
  limitGraph->SetLineColor(lineColor);
  

  limitGraph->SetLineStyle(1);
  legend->AddEntry(limitGraph, legendName, "l");  
  limitGraph->SetLineWidth(2);
  
  //c->cd();
  limitGraph->Draw(drawOption);
}


void DummyLegendExpected(TLegend* leg, TString what,  Int_t fillColor, Int_t fillStyle, Int_t lineColor, Int_t lineStyle, Int_t lineWidth) {
  // fills a legend with properties, using a dummy TGraph as proxy
  TGraph* gr = new TGraph();
  gr->SetFillColor(fillColor);
  gr->SetFillStyle(fillStyle);
  gr->SetLineColor(lineColor);
  gr->SetLineStyle(lineStyle);
  gr->SetLineWidth(lineWidth);
  leg->AddEntry(gr,what,"LF");
}


TGraph* ContourGraph( TH2F* hist, double xmin = 0, double xmax = 6000) {
  // draws the histo to create the contours, then extract the longest one and returns it
  TGraph* gr0 = new TGraph();
  TH2F* h = (TH2F*)hist->Clone();
  TGraph* gr = (TGraph*)gr0->Clone(h->GetName());
  h->SetContour( 1 );
  cout<<"------------------------------>>>>>> Taking "<<h->GetName()<<endl;

  double pval = CombinationGlob::cl_percent[1];
  double signif = TMath::NormQuantile(1-pval);
  h->SetContourLevel(0, signif );
  h->Draw("CONT LIST");
  h->SetDirectory(0);
  gPad->Update();
  TObjArray *contours = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
  Int_t ncontours     = contours->GetSize();
  TList *list = (TList*)contours->At(0);

  if (list->GetEntries() == 0) return gr; // this is a hack, will return an empty graph
  else{
    // Find the longest graph
    TGraph* tempgr = (TGraph*) list->First();
    int npoints = gr->GetN();
    while(tempgr) {
      if(tempgr->GetN() > npoints) {
	gr = tempgr;
	npoints = gr->GetN();
	
      }
      tempgr = (TGraph*) list->After(tempgr);
    }
    gr->SetName(hist->GetName());

    return gr;
  }

}//close function

TGraph* DrawExpectedBand(TGraph* gr1,  TGraph* gr2, Int_t fillColor, Int_t fillStyle,
			 double xlow, double xhigh, double ylow, double yhigh,
			 int cutx = 0, int cuty = 0) {


  //this is for the case in which the TheoryUp has no exclusion
  // and thus we don't know where to draw the lower boundary
  if ((!gr1)){
    double x = gr2->GetX()[0];
    double y = gr2->GetY()[0];
    Int_t gr2N = gr2->GetN();
  
    gr2->SetPoint(gr2N, x, y);

    gr2->SetFillStyle(fillStyle);
    gr2->SetFillColor(fillColor);
    gr2->Draw("F");
  
    return gr2;
  }

  else{
    int number_of_bins = max(gr1->GetN(),gr2->GetN());
  
    Int_t gr1N = gr1->GetN();
    Int_t gr2N = gr2->GetN();
    const Int_t N = number_of_bins;
    Double_t x1[N], y1[N], x2[N], y2[N];

    // Get the points in the first graph
    Double_t xx0, yy0;
    for(int j=0; j<gr1N; j++) {
      gr1->GetPoint(j,xx0,yy0);
      x1[j] = xx0;
      y1[j] = yy0;
    }
    // fill the rest with the last point
    if (gr1N < N) {
      for(int i=gr1N; i<N; i++) {
	x1[i] = x1[gr1N-1];
	y1[i] = y1[gr1N-1];
      }
    }

    // Get the points in the second graph
    Double_t xx1, yy1;
    for(int j=0; j<gr2N; j++) {
      gr2->GetPoint(j,xx1,yy1);
      x2[j] = xx1;
      y2[j] = yy1; 
    }
    if (gr2N < N) {
      // fill the rest with the last point
      for(int i=gr2N; i<N; i++) {
	x2[i] = x2[gr2N-1];
	y2[i] = y2[gr2N-1];
      }      
    }

    // Prepare and fill the 2D region enclosed by the error band
    TGraph *grshade = new TGraph(2*N+10);

    int point = 0;
    double lastx = 0; // This is the last point in the first graph
    double lasty = 0;
    double firstx = -875; // This is the first point drawn in the first graph
    double firsty = -875; // Set an arbitrary initial value so we can check if it's filled!
    for (int i=0;i<N;i++) {
      if (x1[i] > cutx && y1[i] > cuty) { // Allow to exclude some points from being plotted
	grshade->SetPoint(point,x1[i],y1[i]);
	lastx = x1[i]; 
	lasty = y1[i]; 
	if(firstx == -875) {
	  firstx = x1[i];
	  firsty = y1[i];
	}
	point++;
      }
    }

    // Find the first point to be drawn in the second graph
    double nextx = 0;
    double nexty = 0;
    for (int i=0;i<N;i++) {
      if (x2[N-i-1] > cutx && y2[N-i-1] > cuty) {
	nextx = x2[N-i-1];
	nexty = y2[N-i-1];
	i = N;
      }
    }

    for(int i=0;i<grshade->GetN();i++)
      {
	double x,y;
	grshade->GetPoint(i,x,y);
	//cout<<"SHADE point: "<<x<<" "<<y<<endl;
      }


    // Make expected band reach axes where needed
    // Find the closest frame edge to the end of the first contour
    int nearestedge1 = 0; // left
    double dist = fabs(lastx-1-xlow);
    if(fabs(lasty-yhigh) < dist) { // top
      dist = fabs(lasty-yhigh);
      nearestedge1 = 1;
    }
    if(fabs(lastx-1-xhigh) < dist) { // right
      dist = fabs(lastx-1-xhigh);
      nearestedge1 = 2;
    }
    if(fabs(lasty-ylow) < dist) { // bottom
      dist = fabs(lasty-ylow);
      nearestedge1 = 3;
    }

    // Find the closest frame edge to the end of the second contour
    int nearestedge2 = 0; // left
    dist = fabs(nextx-1-xlow);
    if(fabs(nexty-yhigh) < dist) { // top
      dist = fabs(nexty-yhigh);
      nearestedge2 = 1;
    }
    if(fabs(nextx-1-xhigh) < dist) { // right
      dist = fabs(nextx-1-xhigh);
      nearestedge2 = 2;
    }
    if(fabs(nexty-ylow) < dist) { // bottom
      dist = fabs(nexty-ylow);
      nearestedge2 = 3;
    }

    if(nearestedge2 == nearestedge1) {
      // when graphs will be connected on the same frame edge
      // add two points just outside the boundary
      switch(nearestedge1) {
      case 0:
	grshade->SetPoint(point,xlow-100,lasty);
	point++;
	grshade->SetPoint(point,xlow-100,nexty);
	point++;
	break;
      case 1:
	grshade->SetPoint(point,lastx,yhigh+100);
	point++;
	grshade->SetPoint(point,nextx,yhigh+100);
	point++;
	break;
      case 2:
	grshade->SetPoint(point,xhigh+100,lasty);
	point++;
	grshade->SetPoint(point,xhigh+100,nexty);
	point++;
	break;
      case 3:
	grshade->SetPoint(point,lastx,ylow-100);
	point++;
	grshade->SetPoint(point,nextx,ylow-100);
	point++;
	break;
      }
    } else if(nearestedge2 == (nearestedge1-1 >= 0 ? nearestedge1-1 : nearestedge1+3)) {
      // when graphs will be connected across a corner, usually a triangle will be left in
      // to fix, add three points, two outside the boundary, and one outside the corner.
      switch(nearestedge2) {
      case 0:
	grshade->SetPoint(point,lastx,yhigh+100);
	point++;
	grshade->SetPoint(point,xlow-100,yhigh+100);
	point++;
	grshade->SetPoint(point,xlow-100,nexty);
	point++;
	break;      
      case 1:
	grshade->SetPoint(point,xhigh+100,lasty);
	point++;
	grshade->SetPoint(point,xhigh+100,yhigh+100);
	point++;
	grshade->SetPoint(point,nextx,yhigh+100);
	point++;
	break;      
      case 2:
	grshade->SetPoint(point,lastx,ylow-100);
	point++;
	grshade->SetPoint(point,xhigh+100,ylow-100);
	point++;
	grshade->SetPoint(point,xhigh+100,nexty);
	point++;
	break;      
      case 3:
	grshade->SetPoint(point,xlow-100,lasty);
	point++;
	grshade->SetPoint(point,xlow-100,ylow-100);
	point++;
	grshade->SetPoint(point,nextx,ylow-100);
	point++;
	break;      
      }
    }

    // this is the last point drawn in the second graph
    double finalx = 0;
    double finaly = 0;
    for (int i=0;i<N;i++) {
      if (x2[N-i-1] > cutx && y2[N-i-1] > cuty) {
	grshade->SetPoint(point,x2[N-i-1],y2[N-i-1]);
	finalx = x2[N-i-1];
	finaly = y2[N-i-1];
	point++;
      }
    }

    // repeat for the other end of the band
    int nearestedge3 = 0;
    dist = fabs(finalx-1-xlow);
    if(fabs(finaly-yhigh) < dist) {
      dist = fabs(finaly-yhigh);
      nearestedge3 = 1;
    }
    if(fabs(finalx-1-xhigh) < dist) {
      dist = fabs(finalx-1-xhigh);
      nearestedge3 = 2;
    }
    if(fabs(finaly-ylow) < dist) {
      dist = fabs(finaly-ylow);
      nearestedge3 = 3;
    }

    int nearestedge4 = 0;
    dist = fabs(firstx-1-xlow);
    if(fabs(firsty-yhigh) < dist) {
      dist = fabs(firsty-yhigh);
      nearestedge4 = 1;
    }
    if(fabs(firstx-1-xhigh) < dist) {
      dist = fabs(firstx-1-xhigh);
      nearestedge4 = 2;
    }
    if(fabs(firsty-ylow) < dist) {
      dist = fabs(firstx-ylow);
      nearestedge4 = 3;
    }

    if(nearestedge4 == nearestedge3) {
      switch(nearestedge3) {
      case 0:
	grshade->SetPoint(point,xlow-100,finaly);
	point++;
	grshade->SetPoint(point,xlow-100,firsty);
	point++;
	break;
      case 1:
	grshade->SetPoint(point,finalx,yhigh+100);
	point++;
	grshade->SetPoint(point,firstx,yhigh+100);
	point++;
	break;
      case 2:
	grshade->SetPoint(point,xhigh+100,finaly);
	point++;
	grshade->SetPoint(point,xhigh+100,firsty);
	point++;
	break;
      case 3:
	grshade->SetPoint(point,finalx,ylow-100);
	point++;
	grshade->SetPoint(point,firstx,ylow-100);
	point++;
	break;
      }
    } else if(nearestedge4 == (nearestedge3-1 >= 0 ? nearestedge3-1 : nearestedge3+3)) {
      switch(nearestedge4) {
      case 0:
	grshade->SetPoint(point,finalx,yhigh+100);
	point++;
	grshade->SetPoint(point,xlow-100,yhigh+100);
	point++;
	grshade->SetPoint(point,xlow-100,firsty);
	point++;
	break;      
      case 1:
	grshade->SetPoint(point,xhigh+100,finaly);
	point++;
	grshade->SetPoint(point,xhigh+100,yhigh+100);
	point++;
	grshade->SetPoint(point,firstx,yhigh+100);
	point++;
	break;      
      case 2:
	grshade->SetPoint(point,finalx,ylow-100);
	point++;
	grshade->SetPoint(point,xhigh+100,ylow-100);
	point++;
	grshade->SetPoint(point,xhigh+100,firsty);
	point++;
	break;      
      case 3:
	grshade->SetPoint(point,xlow-100,finaly);
	point++;
	grshade->SetPoint(point,xlow-100,ylow-100);
	point++;
	grshade->SetPoint(point,firstx,ylow-100);
	point++;
	break;      
      }
    }
    grshade->Set(point);

    // Now draw the plot...
    grshade->SetFillStyle(fillStyle);
    grshade->SetFillColor(fillColor);
    //  grshade->SetMarkerStyle(21);
  
    grshade->Draw("F");
  
    return grshade;
  }
}



TH2F* AddBorders( const TH2& hist, const char* name=0, const char* title=0) {

  // this appears to add "hidden" overflow and underflow bins to visible 2D histo
  // add new border of bins around original histogram,
  // ... so 'overflow' bins become normal bins

  int nbinsx = hist.GetNbinsX();
  int nbinsy = hist.GetNbinsY();
  
  double xbinwidth = ( hist.GetXaxis()->GetBinCenter(nbinsx) - hist.GetXaxis()->GetBinCenter(1) ) / double(nbinsx-1);
  double ybinwidth = ( hist.GetYaxis()->GetBinCenter(nbinsy) - hist.GetYaxis()->GetBinCenter(1) ) / double(nbinsy-1);
  
  double xmin = hist.GetXaxis()->GetBinCenter(0) - xbinwidth/2. ;
  double xmax = hist.GetXaxis()->GetBinCenter(nbinsx+1) + xbinwidth/2. ;
  double ymin = hist.GetYaxis()->GetBinCenter(0) - ybinwidth/2. ;
  double ymax = hist.GetYaxis()->GetBinCenter(nbinsy+1) + ybinwidth/2. ;
  
  TH2F* hist2 = new TH2F(name, title, nbinsx+2, xmin, xmax, nbinsy+2, ymin, ymax);
  
  for (Int_t ibin1=0; ibin1 <= hist.GetNbinsX()+1; ibin1++) {
    for (Int_t ibin2=0; ibin2 <= hist.GetNbinsY()+1; ibin2++)
      hist2->SetBinContent( ibin1+1, ibin2+1, hist.GetBinContent(ibin1,ibin2) );
  }
  
  return hist2;
}


void SetBorders( TH2 &hist, Double_t val=0 )
{
  // this set over/underflow bins to val
  int numx = hist.GetNbinsX();
  int numy = hist.GetNbinsY();
  
  for(int i=0; i <= numx+1 ; i++){
    hist.SetBinContent(i,0,val);
    hist.SetBinContent(i,numy+1,val);
  }
  for(int i=0; i <= numy+1 ; i++) {
    hist.SetBinContent(0,i,val);
    hist.SetBinContent(numx+1,i,val);
  }
}


void MirrorBorders( TH2& hist) {
  // mirror values of border bins into overflow bins
  int numx = hist.GetNbinsX();
  int numy = hist.GetNbinsY();
  
  Float_t val;
  hist.SetBinContent(0,0,hist.GetBinContent(1,1));
  hist.SetBinContent(numx+1,numy+1,hist.GetBinContent(numx,numy));
  hist.SetBinContent(numx+1,0,hist.GetBinContent(numx,1));
  hist.SetBinContent(0,numy+1,hist.GetBinContent(1,numy));
  
  for(int i=1; i<=numx; i++){
    hist.SetBinContent(i,0,	   hist.GetBinContent(i,1));
    hist.SetBinContent(i,numy+1, hist.GetBinContent(i,numy));
  }
  for(int i=1; i<=numy; i++) {
    hist.SetBinContent(0,i,      hist.GetBinContent(1,i));
    hist.SetBinContent(numx+1,i, hist.GetBinContent(numx,i));
  }
}


TH2F* FixAndSetBorders( const TH2& hist, const char* name=0, const char* title=0, Double_t val=0) {
  TH2F* hist0 = (TH2F*)hist.Clone(); // histogram we can modify
  
  MirrorBorders( *hist0 );    // mirror values of border bins into overflow bins
  
  TH2F* hist1 = AddBorders( *hist0, "hist1", "hist1" );   
  // add new border of bins around original histogram,
  // ... so 'overflow' bins become normal bins
  SetBorders( *hist1, val );                              
  // set overflow bins to value 1
  
  TH2F* histX = AddBorders( *hist1, "histX", "histX" );   
  // add new border of bins around original histogram,
  // ... so 'overflow' bins become normal bins
  
  TH2F* hist3 =(TH2F*) histX->Clone();
  hist3->SetName( name!=0 ? name : "hist3" );
  hist3->SetTitle( title!=0 ? title : "hist3" );
  
  delete hist0; delete hist1; delete histX;
  return hist3; // this can be used for filled contour histograms
}



void DrawContourSameColor( TLegend *leg, TH2F* hist, Int_t nsigma, TString color, Bool_t second=kFALSE, TH2F* inverse=0, Bool_t linesOnly=kFALSE, Bool_t isnobs=kFALSE) {
 
 if (nsigma < 1 || nsigma > 3) {
    cout << "*** Error in CombinationGlob::DrawContour: nsigma out of range: " << nsigma 
	 << "==> abort" << endl;
    exit(1);
  }

  nsigma--; // used as array index, starts from 0
  
  Int_t lcol_sigma;
  Int_t fcol_sigma[3];
  
  if( color == "pink" ){
    lcol_sigma    = CombinationGlob::c_VDarkPink;
    fcol_sigma[0] = CombinationGlob::c_LightPink;
    fcol_sigma[1] = CombinationGlob::c_LightPink;
    fcol_sigma[2] = CombinationGlob::c_LightPink;
  }
  else if( color == "green" ){ // HF
    lcol_sigma    = CombinationGlob::c_VDarkGreen;
    fcol_sigma[0] = CombinationGlob::c_DarkGreen;
    fcol_sigma[1] = CombinationGlob::c_LightGreen;
    fcol_sigma[2] = CombinationGlob::c_VLightGreen;
  } 
  else if( color == "yellow" ){
    lcol_sigma    = CombinationGlob::c_VDarkYellow;
    fcol_sigma[0] = CombinationGlob::c_DarkYellow;
    fcol_sigma[1] = CombinationGlob::c_DarkYellow;
    fcol_sigma[2] = CombinationGlob::c_White; //c_DarkYellow;
  }
  else if( color == "orange" ){
    lcol_sigma    = CombinationGlob::c_VDarkOrange;
    fcol_sigma[0] = CombinationGlob::c_DarkOrange;
    fcol_sigma[1] = CombinationGlob::c_LightOrange; // c_DarkOrange
    fcol_sigma[2] = CombinationGlob::c_VLightOrange;
  }
  else if( color == "gray" ){
    lcol_sigma    = CombinationGlob::c_VDarkGray;
    fcol_sigma[0] = CombinationGlob::c_LightGray;
    fcol_sigma[1] = CombinationGlob::c_LightGray;
    fcol_sigma[2] = CombinationGlob::c_LightGray;
  }
  else if( color == "blue" ){
    lcol_sigma    = CombinationGlob::c_DarkBlueT1;
    fcol_sigma[0] = CombinationGlob::c_BlueT5;
    fcol_sigma[1] = CombinationGlob::c_BlueT3;
    fcol_sigma[2] = CombinationGlob::c_White;  //CombinationGlob::c_BlueT2;
  }
  
  // contour plot
  TH2F* h = new TH2F( *hist );
  h->SetContour( 1 );
  double pval = CombinationGlob::cl_percent[1];
  double signif = TMath::NormQuantile(1-pval);
  double dnsigma = double(nsigma)-1.;
  double dsignif = signif + dnsigma;
  h->SetContourLevel( 0, dsignif );

  if( !second ){
    h->SetFillColor( fcol_sigma[nsigma] );
    
    if (!linesOnly) h->Draw( "samecont0" );
  }

  h->SetLineColor( nsigma==1? 4 : lcol_sigma );
   if (isnobs)h->SetLineColor( nsigma==1? 1 : lcol_sigma );
  h->SetLineWidth( 2 );
  h->Draw( "samecont3" );
  
  if (linesOnly&&!isnobs)
    if(nsigma==1){ leg->AddEntry(h,"expected 95% C.L. exclusion ","l");}
  if (isnobs)
    if(nsigma==1){ leg->AddEntry(h,"observed 95% C.L. exclusion","l");}  
  if (!linesOnly) {
  if(nsigma==0){ leg->AddEntry(h,"expected 68% C.L. exclusion","l"); }
  if(nsigma==2){ leg->AddEntry(h,"expected 99% C.L. exclusion","l");}
  }

}

void DrawContourSameColorDisc( TLegend *leg, TH2F* hist, Double_t nsigma, TString color, Bool_t second=kFALSE, TH2F* inverse=0, Bool_t linesOnly=kFALSE )
{
  if (nsigma < 0.5 || nsigma > 10.5 ) {
    cout << "*** Error in CombinationGlob::DrawContour: nsigma out of range: " << nsigma 
	 << "==> abort" << endl;
    exit(1);
  }
  
  Int_t lcol_sigma;
  Int_t fcol_sigma[3];

  if( color == "pink" ){
    lcol_sigma    = CombinationGlob::c_DarkPink;
    fcol_sigma[0] = CombinationGlob::c_VLightPink;
    fcol_sigma[1] = CombinationGlob::c_VLightPink;
    fcol_sigma[2] = CombinationGlob::c_VLightPink;
  }
  else if( color == "green" ){ // HF
    lcol_sigma    = CombinationGlob::c_VDarkGreen;
    fcol_sigma[0] = CombinationGlob::c_DarkGreen;
    fcol_sigma[1] = CombinationGlob::c_LightGreen;
    fcol_sigma[2] = CombinationGlob::c_VLightGreen;
  } 
  else if( color == "yellow" ){
    lcol_sigma    = CombinationGlob::c_VDarkYellow;
    fcol_sigma[0] = CombinationGlob::c_DarkYellow;
    fcol_sigma[1] = CombinationGlob::c_DarkYellow;
    fcol_sigma[2] = CombinationGlob::c_White; //c_DarkYellow;
  }
  else if( color == "orange" ){
    lcol_sigma    = CombinationGlob::c_VDarkOrange;
    fcol_sigma[0] = CombinationGlob::c_DarkOrange;
    fcol_sigma[1] = CombinationGlob::c_LightOrange; // c_DarkOrange
    fcol_sigma[2] = CombinationGlob::c_VLightOrange;
  }
  else if( color == "gray" ){
    lcol_sigma    = CombinationGlob::c_VDarkGray;
    fcol_sigma[0] = CombinationGlob::c_LightGray;
    fcol_sigma[1] = CombinationGlob::c_LightGray;
    fcol_sigma[2] = CombinationGlob::c_LightGray;
  }
  else if( color == "blue" ){
    lcol_sigma    = CombinationGlob::c_DarkBlueT1;
    fcol_sigma[0] = CombinationGlob::c_LightBlue;
    fcol_sigma[1] = CombinationGlob::c_LightBlue;
    fcol_sigma[2] = CombinationGlob::c_LightBlue;
  }

  // contour plot
  TH2F* h = new TH2F( *hist );
  h->SetContour( 1 );
  double dsignif = double (nsigma);
  h->SetContourLevel( 0, dsignif );

  // ADS ?!?!?
  Int_t mycolor = (nsigma==3   ? 0 : 2);
  mycolor = (nsigma==2 ? 1 : 2);

  h->SetFillStyle(3003);

  if( !second ){
    h->SetFillColor( fcol_sigma[mycolor] );
    if (!linesOnly) h->Draw( "samecont0" );
  }

  h->SetLineColor( (nsigma==3) ? lcol_sigma : lcol_sigma );

  h->SetLineStyle( nsigma==3 || nsigma==2 ? 1 : 2 );
  h->SetLineWidth( nsigma==3 || nsigma==2 ? 2 : 1 );

  
  h->Draw( "samecont3" );

  if(nsigma==3)   { leg->AddEntry(h,"3 #sigma evidence","l"); }
  if(nsigma==6)   { leg->AddEntry(h,"N (int) #sigma","l"); }
  if(nsigma==2)   { leg->AddEntry(h,"2 #sigma evidence","l"); }
}

// these two are just doing a draw after setting colors
void 
DrawContourLine95( TLegend *leg, TGraph* hist, const TString& text="", Int_t linecolor=CombinationGlob::c_VDarkGray, Int_t linestyle=2, Int_t linewidth=2)
{
  TGraph* h = hist;

  h->SetLineColor( linecolor );
  h->SetLineWidth( linewidth );
  h->SetLineStyle( linestyle );
  h->Draw( "same");//cont3" );

  if (!text.IsNull()) leg->AddEntry(h, text.Data(),"l");
}

void 
DrawContourLine95Hist( TLegend *leg, TH2F* hist, const TString& text="", Int_t linecolor=CombinationGlob::c_VDarkGray, Int_t linestyle=2, Int_t linewidth=2 )
{
  // contour plot
  TH2F* h = new TH2F( *hist );
  h->SetContour( 1 );
  double pval = CombinationGlob::cl_percent[1];
  double signif = TMath::NormQuantile(1-pval);
  //cout << "signif: " <<signif << endl;
  h->SetContourLevel( 0, signif );

  h->SetLineColor( linecolor );
  h->SetLineWidth( linewidth );
  h->SetLineStyle( linestyle );
  h->Draw( "samecont3" );

 
  if (!text.IsNull()) leg->AddEntry(h,text.Data(),"l");
}

// now deprecated, but staying as model. I was not able to get it to transform to a TGraph inside this function, and boy did I try...
//TJM, 28/12/2013
void  
DrawSingleSignalRegionExclusion(char* fileName, TString histName, TLegend* leg, char* legendLabel, Int_t linecolor)   
{
  TFile* file = TFile::Open(fileName, "READ");
  TH2F* observed; 
  observed = (TH2F*)file->Get(histName);
  if (observed) {
    observed->SetDirectory(0);
    file->Close();
    
    TH2F* contourObserved = FixAndSetBorders(*observed, "contour2", "contour2", 0);
    TGraph* test ;
    test  = (TGraph*) ContourGraph(observed)->Clone();
  
    //DrawContourLine95Hist(leg, contourObserved, legendLabel, linecolor , 3, 4);

    // cout<<"moooo "<<test<<endl;
    //DrawContourLine95(leg, test, legendLabel, linecolor , 3, 4);   
  }
  
}

void
DrawContourLine99( TLegend *leg, TH2F* hist, const TString& text="", Int_t linecolor=CombinationGlob::c_VDarkGray, Int_t linestyle=2 )
{
  // contour plot
  TH2F* h = new TH2F( *hist );
  h->SetContour( 1 );
  double pval = CombinationGlob::cl_percent[2];
  double signif = TMath::NormQuantile(1-pval);

  h->SetContourLevel( 0, signif );

  h->SetLineColor( linecolor );
  h->SetLineWidth( 2 );
  h->SetLineStyle( linestyle );
  h->Draw( "samecont3" );

  if (!text.IsNull()) leg->AddEntry(h,text.Data(),"l");
}


void
DrawContourLine68( TLegend *leg, TH2F* hist, const TString& text="", Int_t linecolor=CombinationGlob::c_VDarkGray, Int_t linestyle=2 )
{
  // contour plot
  TH2F* h = new TH2F( *hist );
  h->SetContour( 1 );
  double pval = CombinationGlob::cl_percent[0];
  double signif = TMath::NormQuantile(1-pval);

  h->SetContourLevel( 0, signif );

  h->SetLineColor( linecolor );
  h->SetLineWidth( 2 );
  h->SetLineStyle( linestyle );
  h->Draw( "samecont3" );

  if (!text.IsNull()) leg->AddEntry(h,text.Data(),"l");
}




void DrawCaptions( double x, double y, TString caption){

  TLatex* l = new TLatex(x,y,caption);
  l->SetTextAlign(23);
  l->SetTextSize(0.02);
  l->SetTextAngle(90);
  //  l->SetTextColor(kGray+3);
  l->SetTextColor(14);

  l->Draw();

  return;
}

void DrawTheoryUncertaintyOnLegend(TLegend*leg)
{
	if(!leg) return;
	TList*list = leg->GetListOfPrimitives();
	if(!list) return;
	int nentries = list->GetSize();
	for(int i=0;i<nentries;i++)
	{
		TLegendEntry *e = (TLegendEntry*)list->At(i);
		if(!e) continue;
		TString lbl = e->GetLabel();
		if(!lbl.Contains("Observed limit ")) continue;

		float lxmin = leg->GetX1();
		float lxmax = leg->GetX2();
		float lymin = leg->GetY1();
		float lymax = leg->GetY2();	
		cout<<"Found legend	at "<<lxmin<<" "<<lymin<<" "<<lxmax<<" "<<lymax<<endl;
		cout<<"Legend has "<<nentries<<" entries, label is #"<<i<<endl;		
		float r_margin = 0.15;
		float lbl_xmin = lxmin + r_margin*leg->GetMargin()*(lxmax-lxmin);
		float lbl_xmax = lxmin + (1-r_margin)*leg->GetMargin()*(lxmax-lxmin);
		float lbl_height = (lymax-lymin)/nentries;
		float lbl_y = lymin + (nentries-i-0.5)*lbl_height;
		cout<<"Computed label position at "<<lbl_xmin<<" "<<lbl_y<<" "<<lbl_xmax<<" "<<lbl_y<<" with total height "<<lbl_height<<endl;		
		float roff_unc = 0.25;
		Color_t color = TColor::GetColor("#aa000");;
		//TObject *obj = e->GetObject();
		//if(obj)
		//	if(obj->InheritsFrom(TAttLine::Class()))
		//		color = ((TAttLine*)obj)->GetLineColor(); // Not working, for some reason

		TLine *obsPOneSigma = new TLine(lbl_xmin,lbl_y+roff_unc*lbl_height,lbl_xmax,lbl_y+roff_unc*lbl_height);
		obsPOneSigma->SetBit(TLine::kLineNDC);
		obsPOneSigma->SetLineStyle(3);
		obsPOneSigma->SetLineWidth(2);
		obsPOneSigma->SetLineColor(color);
		obsPOneSigma->Draw("same");

		TLine *obsMOneSigma = new TLine(lbl_xmin,lbl_y-roff_unc*lbl_height,lbl_xmax,lbl_y-roff_unc*lbl_height);
		obsMOneSigma->SetBit(TLine::kLineNDC);
		obsMOneSigma->SetLineStyle(3);
		obsMOneSigma->SetLineWidth(2);
		obsMOneSigma->SetLineColor(color);
		obsMOneSigma->Draw("same");		
	}
}



void
DrawContourMassLine(TH2F* hist, Double_t mass, int color=14 )
{

  // contour plot
  TH2F* h = new TH2F( *hist );

  //  Double_t contours[5] = {500, 1000, 1500, 2000, 2500}
  h->SetContour( 1 );
  //h->SetContour( 5, contours )
  //  h->SetContourLevel( 0, contours );
  h->SetContourLevel( 0, mass );

  h->SetLineColor( color );
  h->SetLineStyle( 7 );
  h->SetLineWidth( 1 );
  h->Draw( "samecont3" );

}



//adapted from Jeanette's scripts. Thanks to her!
void addMSUGRALabels(TLegend*leg, SIGNAL_MODEL model){

  return;

  // skipping all for the time being
//  TFile* f4=NULL;
//  // add squark, gluino mass contour lines HERE (TILL)
//  if (model == SUSY_MSUGRA) f4 = TFile::Open("../share/mSugraGridtanbeta30_gluinoSquarkMasses_updated01Nov2013.root", "READ" );
//  else if (model == SUSY_BRPV) f4 = TFile::Open("../share/mSugraGridtanbeta30_gluinoSquarkMasses_TJExtended20140114_withSomeFunnyFeatures.root", "READ" );
//  TH2F* histSq = (TH2F*)f4->Get( "mSugraGrid_squarkMasses" );
//  TH2F* histGl = (TH2F*)f4->Get( "mSugraGrid_gluinoMasses" );
//  histSq->SetDirectory(0);
//  histGl->SetDirectory(0);
//  f4->Close();
//  TH2F* histSquarkMass=NULL;
//  if (model == SUSY_MSUGRA)  histSquarkMass   = FixAndSetBorders( *histSq, "SquarkMass", "SquarkMass", 10000 );
//  else  histSquarkMass   =  getCorrectedSquarkMassesHist();
//  TH2F* histGluinoMass   = FixAndSetBorders( *histGl, "GluinoMass", "GluinoMass", 10000 );
//  
//  
//
//  DrawContourMassLine( histSquarkMass, 1000.0 );  
//  DrawContourMassLine( histSquarkMass, 1400.0 , 17);
//  DrawContourMassLine( histSquarkMass, 1800.0 );
//  DrawContourMassLine( histSquarkMass, 2200.0 , 17);  
//  // DrawContourMassLine( histSquarkMass, 1600.0 , 14);
//  // DrawContourMassLine( histSquarkMass, 2000.0 , 14);  
//  DrawContourMassLine( histSquarkMass, 2600.0 );
//  DrawContourMassLine( histSquarkMass, 3000.0 , 17);   
//  DrawContourMassLine( histSquarkMass, 3400.0 );
//  DrawContourMassLine( histSquarkMass, 3800.0 , 17);
//  DrawContourMassLine( histSquarkMass, 4200.0 );  
//  DrawContourMassLine( histSquarkMass, 4600.0 , 17);
//  DrawContourMassLine( histSquarkMass, 5000.0 );   
//  DrawContourMassLine( histSquarkMass, 5400.0 , 17);
//  DrawContourMassLine( histSquarkMass, 5800.0 );  
//  DrawContourMassLine( histSquarkMass, 6200.0 , 17);  
//  DrawContourMassLine( histSquarkMass, 6600.0 );  
//
//  DrawContourMassLine( histGluinoMass, 800.0 , 17);
//  DrawContourMassLine( histGluinoMass, 1000.0 );  
//  DrawContourMassLine( histGluinoMass, 1200.0 , 17);  
//  DrawContourMassLine( histGluinoMass, 1400.0);
//  DrawContourMassLine( histGluinoMass, 1600.0, 17 ); 
//  DrawContourMassLine( histGluinoMass, 1800.0);
//  DrawContourMassLine( histGluinoMass, 2000.0, 17);  
//  DrawContourMassLine( histGluinoMass, 2200.0);  
//  DrawContourMassLine( histGluinoMass, 2400.0, 17 );    
//
//  DrawContourMassLine( histGluinoMass, 2600.0);    
//  DrawContourMassLine( histGluinoMass, 2800.0, 17 );    
//  DrawContourMassLine( histGluinoMass, 3000.0);    
//
//  //find gluino ~ squark mass exclusion limit
//  // DrawContourMassLine( histSquarkMass, 820.0 );
//  // DrawContourMassLine( histGluinoMass, 820.0 );
//  
//
//  if (model == SUSY_MSUGRA) {
//  TLatex * s2600 = new TLatex(2570, 390, "#tilde{q} (2600 GeV)" );
//  s2600->SetTextAlign( 11 );
//  s2600->SetTextAngle(-87);
//  s2600->SetTextSize( 0.025 );
//  s2600->SetTextColor( 16 );
//  s2600->Draw();   
//  TLatex * s1800 = new TLatex( 1685, 390, "#tilde{q} (1800 GeV)" );
//  s1800->SetTextAlign( 11 );
//  s1800->SetTextAngle(-83);
//  s1800->SetTextSize( 0.025 );
//  s1800->SetTextColor( 16 );
//  s1800->Draw();    
//
//  } else if (model == SUSY_BRPV) {
//    TLatex * s2200 = new TLatex( 1530, 840, "#tilde{q} (2200 GeV)" );
//    s2200->SetTextAlign( 11 );
//    s2200->SetTextAngle(-40);
//    s2200->SetTextSize( 0.025 );
//    s2200->SetTextColor( 16 );
//    s2200->Draw();   
//    TLatex * s1800 = new TLatex( 1565, 470, "#tilde{q} (1800 GeV)" );
//    s1800->SetTextAlign( 11 );
//    s1800->SetTextAngle(-55);
//    s1800->SetTextSize( 0.025 );
//    s1800->SetTextColor( 16 );
//    s1800->Draw();    
//  }
// 
//  if (model == SUSY_MSUGRA) {
//  TLatex * g1000 = new TLatex( 850, 420, "#tilde{g} (1000 GeV)" );
//  g1000->SetTextAlign( 11 );
//  g1000->SetTextAngle(-6); 
//  g1000->SetTextSize( 0.025 );
//  g1000->SetTextColor( 16 );
//  g1000->Draw();
//  TLatex * g1400 = new TLatex( 1650, 584, "#tilde{g} (1400 GeV)" );
//  g1400->SetTextAlign( 11 );
//  g1400->SetTextAngle(-6); 
//  g1400->SetTextSize( 0.025 );
//  g1400->SetTextColor( 16 );
//  g1400->Draw();
//
//   }  else if (model == SUSY_BRPV) {
//  TLatex * g1000 = new TLatex( 850, 420, "#tilde{g} (1000 GeV)" );
//  g1000->SetTextAlign( 11 );
//  g1000->SetTextAngle(-3); 
//  g1000->SetTextSize( 0.025 );
//  g1000->SetTextColor( 16 );
//  g1000->Draw();
//
//  TLatex * g1400 = new TLatex( 1200, 801, "#tilde{g} (1800 GeV)" );
//  g1400->SetTextAlign( 11 );
//  g1400->SetTextAngle(-2); 
//  g1400->SetTextSize( 0.025 );
//  g1400->SetTextColor( 16 );
//  g1400->Draw();
//  }						      
//
//
//
//  TGraph* staulsp = new TGraph();
//  TGraph* noRGE = new TGraph();  
//  TGraph* noEWSB = new TGraph(); 
//  TGraph* tachyon = new TGraph();   
//  TGraph* negmasssq = new TGraph(); 
//  TGraph* lepchrg = new TGraph(); 
//
//  msugraThExcl("../../../HistFitterUser/common/msugra_status_tanb30.txt", staulsp, negmasssq, noRGE, noEWSB, tachyon, "../../../HistFitterUser/common/mSugraGridtanbeta30_charginoMasses.root", lepchrg);   
//  
//  staulsp->SetFillColor(ROOT::kGreen+2);
//
//  c->cd();  
//  //staulsp->Draw("Fsame");
//  //leg->AddEntry(staulsp, "Stau LSP","F" );
//
}


void DrawUpperLimits(const char*upperLimitFile,TH1*frame, SIGNAL_MODEL model)
{
  cout<<upperLimitFile<<endl;
  std::ifstream fin(upperLimitFile,std::ios_base::in);
  if(!fin.is_open()){
    cout<<"cannot oper upperlimit file!"<<endl;
    return;
  }

  bool isNSig=TString(upperLimitFile).Contains("SignalYields");

  while(!fin.eof())
    {
      TString line;
      line.ReadLine(fin);

      if(isNSig){
	TString delim=" ";
	TObjArray*tokens=line.Tokenize(delim);
	int ntokens=tokens->GetEntries();

	if(ntokens<4) continue;

	double m12 = ((TObjString*)tokens->At(1))->String().Atof();
	double m0 = ((TObjString*)tokens->At(0))->String().Atof();
	double nsig= ((TObjString*)tokens->At(2))->String().Atof();
	double errsig= ((TObjString*)tokens->At(3))->String().Atof();

	std::cout<<"nsig: "<<m0<<" "<<m12<<" "<<nsig<<std::endl;
	TLatex point;
	point.SetTextSize(0.02);
	point.SetTextFont(42);
	point.SetTextColor(14);
	char nsig_text[10];
	//if(excludedXsec>=0.1) sprintf(excludedXsec_text,"%1.0f", excludedXsec*1000); // %1.0f"
	//else if(excludedXsec>=0.01) sprintf(excludedXsec_text,"%1.0f", excludedXsec*1000); // %1.0f"
	sprintf(nsig_text,"%1.1f #pm %1.1f", nsig,errsig); // %1.0f"
	
	
	//if ((model == SUSY_RPV) &&  (m2 > 1000 )  &&  (m2 < 1100 ) && m1 < frame->GetXaxis()->GetXmax() && m1 > frame->GetXaxis()->GetXmin() ) point.DrawLatex(m1, 980, excludedXsec_text);
	//else if ((model == SUSY_RPV) &&  (m2 < 300 )  && m1 < frame->GetXaxis()->GetXmax() && m1 > frame->GetXaxis()->GetXmin() ) point.DrawLatex(m1, 300, excludedXsec_text);
	
	//else {
	if (m0 > frame->GetXaxis()->GetXmin() && m12 > frame->GetYaxis()->GetXmin() && m0 < frame->GetXaxis()->GetXmax() && m12<frame->GetYaxis()->GetXmax()){
	  point.DrawLatex(m0, m12, nsig_text);
	  //}
	}
      } else {

	if(line.Length()<10) continue;
	TString delim=" ";
	TObjArray*tokens=line.Tokenize(delim);
	int ntokens=tokens->GetEntries();
	if(ntokens<3) continue;
	double m12 = ((TObjString*)tokens->At(ntokens-5))->String().Atof();
	double m0 = ((TObjString*)tokens->At(ntokens-25))->String().Atof();
	double excludedXsec = ((TObjString*)tokens->At(ntokens-11))->String().Atof();
	
	std::cout<<"upper limit: "<<m0<<" "<<m12<<" "<<excludedXsec<<std::endl;
	
	
	TLatex point;
	point.SetTextSize(0.02);
	point.SetTextFont(42);
	point.SetTextColor(14);
	char excludedXsec_text[10];
	if(excludedXsec>=0.1) sprintf(excludedXsec_text,"%1.0f", excludedXsec*1000); // %1.0f"
	else if(excludedXsec>=0.01) sprintf(excludedXsec_text,"%1.0f", excludedXsec*1000); // %1.0f"
	else sprintf(excludedXsec_text,"%1.1f", excludedXsec*1000); // %1.0f"
	
	
	//if ((model == SUSY_RPV) &&  (m2 > 1000 )  &&  (m2 < 1100 ) && m1 < frame->GetXaxis()->GetXmax() && m1 > frame->GetXaxis()->GetXmin() ) point.DrawLatex(m1, 980, excludedXsec_text);
	//else if ((model == SUSY_RPV) &&  (m2 < 300 )  && m1 < frame->GetXaxis()->GetXmax() && m1 > frame->GetXaxis()->GetXmin() ) point.DrawLatex(m1, 300, excludedXsec_text);
	
	//else {
	if (m0 > frame->GetXaxis()->GetXmin() && m12 > frame->GetYaxis()->GetXmin() && m0 < frame->GetXaxis()->GetXmax() && m12<frame->GetYaxis()->GetXmax()){
	  point.DrawLatex(m0, m12, excludedXsec_text);
	  //}
	}
      }

    }
  fin.close();
  gStyle->SetPaintTextFormat("1.2f");
}



/////////////////////Stuff from 
//TPolyLine*
void plot_region_opal_stau(double low_lambda=40, double high_lambda=60, double high_tanbeta=60)
{
  return;
//"Drawing OPAl stau exclusion region" << std::endl;
//
//on (pol4) from OPAL stau mass limit of 87.4 GeV
// {-333.077, 30.7151, -1.01958, 0.0156407, -9e-05};
//
// new TF1("f_pol4", "pol4");
//rameters(p);
//
//e on the fly
//ouble> l, tb;
//bda
//(low_lambda); i <= high_lambda; ++i){
//(double(i));
//k(f_pol4->Eval(double(i)));
//
//sure
//igh_lambda); tb.push_back(high_tanbeta);
//ow_lambda);  tb.push_back(high_tanbeta); 
//ow_lambda);  tb.push_back(tb[0]);
//
//reference
//"const int max(" << l.size() << ");" << std::endl;
//"double lambda[max] = {";
//(0); i < l.size(); ++i) {
//< l[i] << ",";
//
//"};" << std::endl;
//"double tanbeta[max] = {";
//(0); i < tb.size(); ++i) {
//< tb[i] << ",";
//
//"};" << std::endl;
//
//stdout
//(24);
//[max] = {40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,60,40,40};
//a[max] = {34.8038,35.9823,37.1536,38.3219,39.4893,40.6555,41.8185,42.9736,44.1143,45.2319,46.3155,47.3519,48.326,49.2203,50.0153,50.6892,51.2183,51.5763,51.7353,51.6648,51.3322,60,60,34.8038};
//
//ine = new TPolyLine(max, lambda, tanbeta);
//eColor(26);
//lColor(26);
//lStyle(1001);
//eWidth(4);
//F");
//
//
}



//TPolyLine* 
void plot_region_theory(double low_lambda=40, double high_lambda=77, double high_tanbeta=60)
{
  return;

//  std::cout << "Drawing theory exclusion region" << std::endl;
//
//  // fit function (pol6) from theory exclusion plot
//  double p[7] = {-4.79481, 2.5644, -0.0890627, 0.00207083, -2.44895e-05, 1.37365e-07, -2.93332e-10};
//
//  TF1 *f_pol6 = new TF1("f_pol6", "pol6");
//  f_pol6->SetParameters(p);
//  
//  // interpolate on the fly
//  std::vector<double> l, tb;
//  // sample lambda
//  for (size_t i(low_lambda); i <= high_lambda; ++i){
//    l.push_back(double(i));
//    tb.push_back(f_pol6->Eval(double(i)));
//  }
//  // corner closure
//  l.push_back(high_lambda); tb.push_back(high_tanbeta);
//  l.push_back(low_lambda);  tb.push_back(high_tanbeta); 
//  l.push_back(low_lambda);  tb.push_back(tb[0]);
//
//  // print for reference
//  std::cout << "const int max(" << l.size() << ");" << std::endl;
//  std::cout << "double lambda[max] = {";
//  for (size_t i(0); i < l.size(); ++i) {
//    std::cout << l[i] << ",";
//  }
//  std::cout << "};" << std::endl;
//  std::cout << "double tanbeta[max] = {";
//  for (size_t i(0); i < tb.size(); ++i) {
//    std::cout << tb[i] << ",";
//  }
//  std::cout << "};" << std::endl;
//  
//  // copied from stdout
//  const int max(41);
//  double lambda[max] = {40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,77,40,40,};
//  double tanbeta[max] = {37.9856,38.6746,39.3655,40.0578,40.7512,41.4453,42.1396,42.8334,43.5262,44.2174,44.9061,45.5916,46.2733,46.9502,47.6216,48.2867,48.9446,49.5945,50.2356,50.8671,51.4882,52.098,52.6959,53.2811,53.8529,54.4106,54.9536,55.4813,55.9931,56.4884,56.9669,57.428,57.8715,58.2969,58.704,59.0926,59.4625,59.8135,60,60,37.9856,};
//  
//  // prepare and draw polyline
//  TPolyLine *pline = new TPolyLine(max, lambda, tanbeta);
//  pline->SetFillStyle(1001);
//  pline->SetFillColor(12);
//  pline->SetLineColor(12);
//  pline->SetLineWidth(4);
//  pline->Draw("F");
//
//  TLatex latex;
//  latex.SetTextFont(42);
//  latex.SetTextSize(0.04);
//  latex.SetTextColor(kWhite);
//  
//  latex.DrawTextNDC(0.2,0.86, "Theory");
//  latex.DrawTextNDC(0.2,0.82, "excl.");
//
//  //return pline;
}


void plot_gluino_lines()
{
  std::cout << "Drawing gluino lines" << std::endl;

  TLine *line = new TLine();
  line->SetLineColor(kGray+2);
  line->SetLineStyle(7);
  // line->DrawLine(16.42, 2, 16.42, 24);
  // line->DrawLine(25.95, 2, 25.95, 31.5);
  // line->DrawLine(35.47, 2, 35.47, 41);
  line->DrawLine(45.00, 2, 45.00, 40.5);
  line->DrawLine(54.53, 2, 54.53, 48);
  line->DrawLine(64.06, 2, 64.06, 53.5);
  line->DrawLine(73.54, 2, 73.54, 58.5);
  line->DrawLine(83.12, 2, 83.12, 60);
  line->DrawLine(92.64, 2, 92.64, 60);
  line->DrawLine(101.64, 2, 101.64, 60);

  // DrawCaptions(16.7,20,"#tilde{g} (400 GeV)");
  // DrawCaptions(26.2,25,"#tilde{g} (600 GeV)");
  // DrawCaptions(35.7,31,"#tilde{g} (800 GeV)");
  DrawCaptions(45.2,37,"#tilde{g} (1000 GeV)");
  DrawCaptions(54.7,44,"#tilde{g} (1200 GeV)");
  DrawCaptions(64.3,50.2,"#tilde{g} (1400 GeV)");
  DrawCaptions(73.7,53.5,"#tilde{g} (1600 GeV)");
  DrawCaptions(83.4, 55,"#tilde{g} (1800 GeV)");
  DrawCaptions(92.9, 55,"#tilde{g} (2000 GeV)");
  DrawCaptions(101.9, 55,"#tilde{g} (2200 GeV)");

  return;
}

// the MAIN FUNCTION

void winter2015MakeExclusion(TString nominalFileName = "m0m12_nofloat_exp.root",
			    TString theoryUpFileName = "m0m12_nofloat_exp.root", 
			    TString theoryDownFileName = "m0m12_nofloat_exp.root", 
			    TString upperLimitFile = "Merged_Output_hypotest_SM_SS_twostepCN_sleptons_SR4_combined_ul__1_harvest_list",
			    TString fileNameSR3b = "None",
			    TString fileNameSR3bDesc = "None",
			    TString fileNameSR1b = "None",
			    TString fileNameSR1bDesc = "None",
			    TString fileNameSR0b3j = "None",
			    TString fileNameSR0b3jDesc = "None",
			    TString fileNameSR0b5j = "None",
			    TString fileNameSR0b5jDesc = "None",
			    const char* prefix="",
			    const float& lumi = 20,
			    bool showsig = true,
			    int discexcl = 1,
			    int showtevatron = 0,
			    TString  xLabel = "notSpecified",
			    TString yLabel = "notSpecified",
			    TString processDescription = "unknown grid",
			    double forbiddenRegionCut = 0,
			    double forbiddenLabelX = 0,
			    double forbiddenLabelY = 0,
			    TString forbiddenLabelText = "None",
			    bool showSingleSR = false,
			    TString hname0 = "sigp1clsf", //"sigCLs",
			    TString hname0_exp = "sigp1expclsf",//"sigCLsexp",
			    TString hname0_1su = "sigclsu1s",//"sigCLsexp1su",
			    TString hname0_1sd = "sigclsd1s",//"sigCLsexp1sd",
			    TString hname1 = "sigp0",
			    TString hname1_exp = "sigp0",
			    TString fnameMass= "mSugraGridtanbeta10_gluinoSquarkMasses.root"
			    )
{


  CombinationGlob::Initialize();
 
  TFile* openNominalFile = TFile::Open(nominalFileName, "READ" );
  TFile* openTheoryUpFile = TFile::Open( theoryUpFileName, "READ" ); 
  TFile* openTheoryDownFile = TFile::Open( theoryDownFileName, "READ" ); 
  
  TFile* openSR3bFile=0;
  TFile* openSR1bFile=0;
  TFile* openSR0b3jFile=0;
  TFile* openSR0b5jFile=0;
  if(fileNameSR3b!="None") openSR3bFile=TFile::Open(fileNameSR3b, "READ");
  if(fileNameSR1b!="None") openSR1bFile=TFile::Open(fileNameSR1b, "READ");
  if(fileNameSR0b3j!="None") openSR0b3jFile=TFile::Open(fileNameSR0b3j, "READ");
  if(fileNameSR0b5j!="None") openSR0b5jFile=TFile::Open(fileNameSR0b5j, "READ");
  
  cout<< "files opened"<<endl;

  TH2F* hist0; 
  TH2F* hist0_1su; 
  TH2F* hist0_1sd; 
  TH2F* hist1;
  TH2F* hist1_unc;
  TH2F* hist0_all;

  TH2F* SR3bIndivHist=0;
  TH2F* SR1bIndivHist=0;
  TH2F* SR0b3jIndivHist=0;
  TH2F* SR0b5jIndivHist=0;
 
  hist0     = (TH2F*)openNominalFile->Get( hname0_exp );
  hist1     = (TH2F*)openNominalFile->Get( hname0 );
  hist1_unc = (TH2F*)openTheoryDownFile->Get( hname0 );
  hist0_all = (TH2F*)openTheoryUpFile->Get( hname0 );
  hist0_1su = (TH2F*)openNominalFile->Get( hname0_1su );
  hist0_1sd = (TH2F*)openNominalFile->Get( hname0_1sd );

  if(openSR3bFile) SR3bIndivHist = (TH2F*) openSR3bFile->Get( hname0_exp )->Clone("SR3b");
  if(openSR1bFile) SR1bIndivHist = (TH2F*) openSR1bFile->Get( hname0_exp )->Clone("SR1b");
  if(openSR0b3jFile) SR0b3jIndivHist = (TH2F*) openSR0b3jFile->Get( hname0_exp )->Clone("SR0b3j");
  if(openSR0b5jFile) SR0b5jIndivHist = (TH2F*) openSR0b5jFile->Get( hname0_exp )->Clone("SR0b5j");

  cout<< "histos retrieved"<<endl;

  hist0->SetDirectory(0);
  hist1->SetDirectory(0);
  hist1_unc->SetDirectory(0);
  hist0_all->SetDirectory(0);
  hist0_1su->SetDirectory(0);
  hist0_1sd->SetDirectory(0);

  if(SR3bIndivHist) SR3bIndivHist->SetDirectory(0);
  if(SR1bIndivHist) SR1bIndivHist->SetDirectory(0);
  if(SR0b3jIndivHist) SR0b3jIndivHist->SetDirectory(0);
  if(SR0b5jIndivHist) SR0b5jIndivHist->SetDirectory(0);

  openNominalFile->Close();
  openTheoryUpFile->Close();
  openTheoryDownFile->Close();

  if(openSR3bFile) openSR3bFile->Close();
  if(openSR1bFile) openSR1bFile->Close();
  if(openSR0b3jFile) openSR0b3jFile->Close();
  if(openSR0b5jFile) openSR0b5jFile->Close();
  
  TH2F* contour_exp          = FixAndSetBorders( *hist0,         "contour",             "contour",          0 );
  TH2F* contour_obs_thDOWN  = FixAndSetBorders( *hist1_unc,     "contour_obs_thDOWN",     "contour_obs_thDOWN",  0 );
  TH2F* contour_obs_thUP  = FixAndSetBorders( *hist0_all,     "contour_obs_thUP",     "contour_obs_thUP",  0 );
  TH2F* contour_obs      = FixAndSetBorders( *hist1,         "contour_obs",         "contour_obs",      0 );


  TH2F* contour_1su  = FixAndSetBorders( *hist0_1su, "contour_1su",     "contour_1su",     0 );
  TH2F* contour_1sd  = FixAndSetBorders( *hist0_1sd, "contour_1sd",     "contour_1sd",     0 );
  

  TGraph* gr_contour_1su;
  TGraph* gr_contour_1sd;
  TGraph* gr_contour_obs_thUP;
  TGraph* gr_contour;
  TGraph* gr_contour_obs_thDOWN;
  TGraph* gr_contour_obs;

  TGraph* SR3bIndivGraph=0;
  TGraph* SR1bIndivGraph=0;
  TGraph* SR0b3jIndivGraph=0;
  TGraph* SR0b5jIndivGraph=0;

  gr_contour_1su   = (TGraph*) ContourGraph( hist0_1su)->Clone();
  gr_contour           = (TGraph*) ContourGraph( hist0)->Clone();
  gr_contour_1sd   = (TGraph*) ContourGraph( hist0_1sd)->Clone();

  cout<<"Saving in root file.."<<endl;
  TString line_file_name="MyFile.root";
  if (nominalFileName.Contains("SusyGG2StepWZ") ) line_file_name="SusyGG2StepWZ_observed_exclusion_line";
  if (nominalFileName.Contains("SusyBtt") ) line_file_name="SusyBtt_observed_exclusion_line";
  if (nominalFileName.Contains("SusyGtt") ) line_file_name="SusyGtt_observed_exclusion_line";
  if (nominalFileName.Contains("SusyComprGtt") ) line_file_name="SusyComprGtt_observed_exclusion_line";
  if (nominalFileName.Contains("SusyGSL") ) line_file_name="SusyGSL_observed_exclusion_line";
  
  TObjArray* arr1 = nominalFileName.Tokenize("_");
  TObjString* objstring1 = (TObjString*)arr1->At(2);
  TString outtag = objstring1->GetString();

  TFile *f = TFile::Open(line_file_name+"_"+outtag+".root", "RECREATE");
  f->cd(); // make sure that we will write to this ROOT file
  cout<<"nominalFileName: "<<nominalFileName<<endl;
  gr_contour->Write("exp_exclusion_line");

  gr_contour_obs_thUP   = (TGraph*) ContourGraph( hist0_all)->Clone();
  gr_contour_obs       = (TGraph*) ContourGraph( hist1)->Clone();
  gr_contour_obs_thDOWN   = (TGraph*) ContourGraph( hist1_unc)->Clone();

  gr_contour_obs->Write("obs_exclusion_line");
  f->ls();
  
  /*TCanvas *ysjs = new TCanvas("ysjs","ysjs");
  ysjs->cd();

  gr_contour_obs_thUP->Draw("la");
  gr_contour_obs_thDOWN->Draw("same");
  
  ysjs->WaitPrimitive();
  */
  if(SR3bIndivHist) SR3bIndivGraph =  (TGraph*) ContourGraph(SR3bIndivHist)->Clone("SR3bGraph");
  if(SR1bIndivHist) SR1bIndivGraph =  (TGraph*) ContourGraph(SR1bIndivHist)->Clone("SR1bGraph");
  if(SR0b3jIndivHist) SR0b3jIndivGraph =  (TGraph*) ContourGraph(SR0b3jIndivHist)->Clone("SR0b3jGraph");
  if(SR0b5jIndivHist) SR0b5jIndivGraph =  (TGraph*) ContourGraph(SR0b5jIndivHist)->Clone("SR0b5jGraph");
  cout<< "countours retrieved"<<endl;




  //++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  //
  // Here, we set up all the custom variables for the different grids
  // Caveat Emptor: if you would like non-standard things (e.g. forbidden regions),
  // you have to put them in explicitly further down. TJM, 12/25/12
  //
  //+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

  //standard values
  model=SUSY_UNKNOWN;
  TString modelName = "";
  int nBinsX = 19;
  double xMin = 800;
  double xMax = 2000;
  int nBinsY = 24;
  double yMin = 0;
  double yMax = 900;

  double xMinLeg = 0.55;
  double xMaxLeg = 0.90;
  double yMinLeg = 0.60;
  double yMaxLeg = 0.92;
  
  /*
  double xMinLeg = 0.50;
  double xMaxLeg = 0.85;
  double yMinLeg = 0.60;
  double yMaxLeg = 0.92;
  */
  double xMinLeg2 = 0.17;
  double xMaxLeg2 = 0.45;
  double yMinLeg2 = 0.61;
  double yMaxLeg2 = 0.89;


  if (showSingleSR == true) double yMinLeg = 0.5;

  if (nominalFileName.Contains("SusyGtt") || nominalFileName.Contains("SusyTest") )
    {
      model = SUSY_GTT;
      modelName = "Gtt";

      nBinsX = 1100;
      xMin = 750;
      xMax = 1850;
      nBinsY = 1600;
      yMin = 100;
      yMax = 1900;
      
 
    }

  if (nominalFileName.Contains("SusyComprGtt") )
    {
      model = SUSY_COMPR_GTT;
      modelName = "ComprGtt";

      nBinsX = 1100;
      xMin = 750;
      xMax = 2000;
      nBinsY = 1600;
      yMin = 5;
      yMax = 150;

      yMinLeg = 0.48;
      yMaxLeg = 0.78;

    }


  if (nominalFileName.Contains("SusyGG2StepWZ") )
    {
      model = SUSY_GG2STEPWZ;
      modelName = "SusyGG2StepWZ";

      nBinsX = 19;
      xMin = 700;
      xMax = 2000;
      nBinsY = 24;
      yMin = 100;
      yMax = 2000;
      
   
    }

  if (nominalFileName.Contains("SusyTT2Step") )
    {
      model = SUSY_TT2STEP;
      modelName = "SusyTT2Step";

      nBinsX = 19;
      xMin = 500;
      xMax = 900;
      nBinsY = 24;
      yMin = 200;
      yMax = 600;


    }

   if (nominalFileName.Contains("SusyBtt") )
    {
      model = SUSY_BTT;
      modelName = "SusyBtt";

      nBinsX = 19;
      xMin = 400;
      xMax = 950;
      nBinsY = 23;
      yMin = 1;
      yMax = 700;
      
 
    }


     if (nominalFileName.Contains("SusyGSL") )
    {
      model = SUSY_GSL;
      modelName = "SusyGSL";

      nBinsX = 20;
      xMin = 600;
      xMax = 2300;
      nBinsY = 23;
      yMin = 200;
      yMax = 2200;
      
  
    }

     if (nominalFileName.Contains("SusyGG_Rpv321") )
       {
	 model = SUSY_GG_RPV321;
	 modelName = "SusyGG_Rpv321";

	 nBinsX = 19;
	 xMin = 800;
	 xMax = 1600;
	 nBinsY = 24;
	 yMin = 400;
	 yMax = 1600;


       }
     if (nominalFileName.Contains("SusyGG_Rpv331") )
       {
         model = SUSY_GG_RPV331;
         modelName = "SusyGG_Rpv331";

         nBinsX = 19;
         xMin = 800;
         xMax = 1600;
         nBinsY = 24;
         yMin = 400;
         yMax = 1800;


       }

     if (nominalFileName.Contains("SusyDD_Rpv321") )
       {
         model = SUSY_DD_RPV321;
         modelName = "SusyDD_Rpv321";

         nBinsX = 13;
         xMin = 450;
         xMax = 1150;
         nBinsY = 16;
         yMin = 450;
         yMax = 2050;


       }

     if (nominalFileName.Contains("SusyDD_Rpv331") )
       {
         model = SUSY_DD_RPV331;
         modelName = "SusyDD_Rpv331";

         nBinsX = 25;
         xMin = 450;
         xMax = 1100;
         nBinsY = 25;
         yMin = 450;
         yMax = 2400;


       }






   // end definition of upper/lower limits
   //+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

  //if (contour==0) { 
  //  cout << "contour is zero" << endl;
  //  return;
  //}
 
  gStyle->SetPaintTextFormat(".2g");
  Float_t nsigmax = hist0->GetMaximum();


  // create canvas
  TCanvas* c = new TCanvas( "c", "A scan of m_{0} versus m_{12}", 0, 0, 650,640);
  // create and draw the frame
  TH2F *frame ;

  frame = new TH2F("frame", "m_{0} vs m_{12} - ATLAS", nBinsX, xMin, xMax, nBinsY, yMin, yMax);
   
  CombinationGlob::SetFrameStyle2D( frame, 1.0 ); // the size (scale) is 1.0
  gPad->SetTopMargin( 0.07  );
  gPad->SetBottomMargin( 0.120  );
  gPad->SetRightMargin( 0.05 );
  gPad->SetLeftMargin( 0.14  );
  gPad->SetLogz();

  //Palette  
  const Int_t NRGBs = 2;
  const Int_t NCont = 20;
  
  Double_t stops[NRGBs] = { 0.00, 1.0 };
  
  Double_t red   [NRGBs] = { 1.0, 0.10 };
  Double_t green [NRGBs] = { 1.00, 0.10 };
  Double_t blue  [NRGBs] = { 1.00, 0.10 };
  
  TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);

  frame->SetXTitle(xLabel);
  frame->SetYTitle(yLabel);		
  

  frame->SetZTitle( "X-Section" );
  frame->GetXaxis()->SetTitleOffset(1.15);
  frame->GetYaxis()->SetTitleOffset(1.7);
  frame->GetZaxis()->SetTitleOffset(2.5);

  frame->GetXaxis()->SetTitleFont(42);
  frame->GetXaxis()->SetLabelFont(42);
  frame->GetYaxis()->SetTitleFont(42);
  frame->GetYaxis()->SetLabelFont(42);

  frame->GetXaxis()->SetTitleSize( 0.04 );
  frame->GetYaxis()->SetTitleSize( 0.04 );
  frame->GetXaxis()->SetLabelSize( 0.035 );
  frame->GetYaxis()->SetLabelSize( 0.035 );
  frame->GetZaxis()->SetLabelSize( 0.015 );

  frame->Draw();

  TPolyLine *pline1;
  TPolyLine *pline2;
  TPolyLine *pline3;


  // +++++++++++++++++++++++++++
  // building legend
  // ++++++++++++++++++++++++++++++

  TString basecolor = "yellow";
  Int_t nsigma = 2;
  TLegend *leg = new TLegend(xMinLeg, yMinLeg, xMaxLeg, yMaxLeg); 
  
  //leg->SetTextSize( CombinationGlob::DescriptionTextSize*0.8 ); 
  //if (model == SUSY_GMSB2D) leg->SetTextSize( 0.025 );
  //  else
  leg->SetTextSize( 0.03);
  leg->SetTextFont( 42 );
  leg->SetFillColor(kWhite);
  leg->SetFillStyle(1001);
  
   // if (discexcl==0) {  
   //  DrawContourSameColorDisc( leg, contour, 2, "pink", kFALSE, 0, kFALSE ) ;
   //  for (Double_t dnsigma=1.0; dnsigma<=10.0; dnsigma+=1.0) {
   //    if (dnsigma!=2.0){
   // 	bool lineonly = ( dnsigma==3 ? false : true );
   //      DrawContourSameColorDisc( leg, contour, dnsigma, "blue", lineonly, 0, lineonly ) ;
   //    }
   //  }
   // }


  //++++++++++++++++++++++++++++++++++++++++++++
  //
  // Only if there are forbidden regions
  //
  //++++++++++++++++++++++++++++++++++++++++++++
   Double_t dx = xMax - xMin;
   Double_t dy = yMax - yMin;
   double m,q;
   double xMinLine, xMaxLine, yMinLine, yMaxLine;
   double xMinLabel, xMaxLabel, yMinLabel, yMaxLabel;
   TLatex* forbiddenLabel = 0;
   TLatex* forbiddenLabel2 = 0;
   TLine* lineExcl  = 0;
   TLine* lineExcl2 = 0;

   bool  line2(true);
   float vDiff = 2*(172. - 80.);

   if (forbiddenLabelText != "None"){
     yMinLine = xMin - forbiddenRegionCut;
     yMaxLine = xMax - forbiddenRegionCut;
     xMinLine = yMin + forbiddenRegionCut;
     xMaxLine = yMax + forbiddenRegionCut;
     if(xMinLine < xMin)  xMinLine = xMin;
     else yMinLine = yMin;
     if (xMaxLine > xMax) xMaxLine = xMax;
     else yMaxLine = yMax;

     xMinLabel=xMinLine;
     xMaxLabel=xMaxLine;
     yMinLabel=yMinLine;
     yMaxLabel=yMaxLine;

     m = (yMaxLine-yMinLine)/(xMaxLine-xMinLine);
     q = yMinLine-m*xMinLine;
     cout<<"FORBIDDEN REGION "<<yMinLine<< " "<<yMaxLine<< " "<<xMinLine<< " "<<xMaxLine<<endl;
     if (nominalFileName.Contains("SusyGSL") ){
       yMaxLine=m*1600+q;
     //cout<<"----------------->yMaxLine: "<<yMaxLine<<endl;
       lineExcl = new TLine(xMinLine,yMinLine,1600,yMaxLine);
       }
     if (nominalFileName.Contains("SusyGG2StepWZ") ){
       yMaxLine=m*1350+q;
       cout<<"FORBIDDEN REGION "<<yMinLine<< " "<<yMaxLine<< " "<<xMinLine<< " "<<xMaxLine<<endl;
       lineExcl = new TLine(xMinLine,yMinLine,1350,yMaxLine);
     }
     if (nominalFileName.Contains("SusyBtt") ){
       yMaxLine=m*650+q;
       cout<<"FORBIDDEN REGION "<<yMinLine<< " "<<yMaxLine<< " "<<xMinLine<< " "<<xMaxLine<<endl;
       lineExcl = new TLine(xMinLine,yMinLine,650,yMaxLine);
     }
     if (nominalFileName.Contains("SusyComprGtt") ){
       //yMaxLine=m*650+q;
       cout<<"FORBIDDEN REGION "<<yMinLine<< " "<<yMaxLine<< " "<<xMinLine<< " "<<xMaxLine<<endl;
       //lineExcl = new TLine(xMinLine,yMinLine,xMaxLine,yMaxLine);
       //lineExcl = new TLine(600,25,2000,25);
     }
     if(!nominalFileName.Contains("SusyGG2StepWZ") && !nominalFileName.Contains("SusyGSL") && !nominalFileName.Contains("SusyBtt") && !nominalFileName.Contains("SusyComprGtt")){
       cout<<"FORBIDDEN REGION "<<yMinLine<< " "<<yMaxLine<< " "<<xMinLine<< " "<<xMaxLine<<endl;
       yMaxLine=m*1400+q;
       lineExcl = new TLine(xMinLine,yMinLine,1400,yMaxLine);
       if(line2) lineExcl2 = new TLine(xMinLine,yMinLine-vDiff,1400,yMaxLine-vDiff);
     }

     if(lineExcl){
       lineExcl->SetLineStyle(3);
       lineExcl->SetLineWidth(1);
       lineExcl->SetLineColor(14);
       lineExcl->Draw("same");
     }  

     if(lineExcl2){
       lineExcl2->SetLineStyle(3);
       lineExcl2->SetLineWidth(1);
       lineExcl2->SetLineColor(14);
       lineExcl2->Draw("same");
     }

     forbiddenLabel = new TLatex(forbiddenLabelX, forbiddenLabelY, forbiddenLabelText);
     forbiddenLabel->SetTextSize(0.028);
     forbiddenLabel->SetTextColor(14);
     if (!nominalFileName.Contains("SusyComprGtt") )
       forbiddenLabel->SetTextAngle(180/3.1415927*atan2((yMaxLabel-yMinLabel)/(yMax-yMin),(xMaxLabel-xMinLabel)/(xMax-xMin)));
     forbiddenLabel->SetTextFont(42);
     forbiddenLabel->Draw("same");

     if(lineExcl2){
       TString description = "m_{#tilde{g}} <  2 m_{t} + m_{#tilde{#chi}^{0}_{1}} ";
       forbiddenLabel2 = new TLatex(forbiddenLabelX, forbiddenLabelY-vDiff, description);
       forbiddenLabel2->SetTextSize(0.028);
       forbiddenLabel2->SetTextColor(14);
       forbiddenLabel2->SetTextAngle(180/3.1415927*atan2((yMaxLabel-yMinLabel)/(yMax-yMin),(xMaxLabel-xMinLabel)/(xMax-xMin))); 
       forbiddenLabel2->SetTextFont(42);
       forbiddenLabel2->Draw("same");
     }

   } 
  //+++++++++++++++++++++++++END forbidden regions only


  //+++++++++fiddle with TGraphs for different Grids+++++++

   if(SR3bIndivGraph) SR3bIndivGraph = removeArea(model, SR3bIndivGraph, yMin, yMax, "SR3b");
   if(SR1bIndivGraph) SR1bIndivGraph = removeArea(model, SR1bIndivGraph, yMin, yMax, "SR1b");
   if(SR0b3jIndivGraph) SR0b3jIndivGraph = removeArea(model, SR0b3jIndivGraph, yMin, yMax, "SR0b3j");
   if(SR0b5jIndivGraph) SR0b5jIndivGraph = removeArea(model, SR0b5jIndivGraph, yMin, yMax, "SR0b5j");

   gr_contour = removeArea(model, gr_contour, yMin, yMax, "expected");
   gr_contour_1su = removeArea(model, gr_contour_1su, yMin, yMax, "expectedUp");
   gr_contour_1sd = removeArea(model, gr_contour_1sd, yMin, yMax, "expectedDown");
   gr_contour_obs_thDOWN = removeArea(model, gr_contour_obs_thDOWN, yMin, yMax, "observedDown");
   gr_contour_obs_thUP = removeArea(model, gr_contour_obs_thUP, yMin, yMax, "observedUp");
   gr_contour_obs = removeArea(model, gr_contour_obs, yMin, yMax, "observed");
  

   //SR3bIndivGraph->Draw("ap");
   //gr_contour->Draw("sp");
   //c->WaitPrimitive();

   

   //++++++++++++++++++++++++++++++++++

   gr_contour = addPoints(model, gr_contour, "expected", modelName, showSingleSR);
   gr_contour_1su = addPoints(model, gr_contour_1su, "expectedUp", modelName, showSingleSR);
   gr_contour_1sd = addPoints(model, gr_contour_1sd, "expectedDown", modelName, showSingleSR);
   gr_contour_obs_thDOWN = addPoints(model, gr_contour_obs_thDOWN, "observedDown", modelName, showSingleSR);
   gr_contour_obs_thUP = addPoints(model, gr_contour_obs_thUP, "observedUp", modelName, showSingleSR);
   gr_contour_obs = addPoints(model, gr_contour_obs, "observed", modelName, showSingleSR);
   
   if(SR3bIndivGraph) SR3bIndivGraph = addPoints(model,  SR3bIndivGraph, "SR3b", modelName, showSingleSR);
   if(SR1bIndivGraph) SR1bIndivGraph = addPoints(model,  SR1bIndivGraph, "SR1b", modelName, showSingleSR);
   if(SR0b3jIndivGraph) SR0b3jIndivGraph = addPoints(model,  SR0b3jIndivGraph, "SR0b3j", modelName, showSingleSR);
   if(SR0b5jIndivGraph) SR0b5jIndivGraph = addPoints(model,  SR0b5jIndivGraph, "SR0b5j", modelName, showSingleSR);

   //SR3bIndivGraph->Draw("ap");
   //gr_contour->Draw("sp");
   //c->WaitPrimitive();



   //++++end fiddling with TGraphs++++++++++++

  Int_t c_myYellow   = TColor::GetColor("#ffe938");
  Int_t c_myRed      = TColor::GetColor("#aa000");
  Int_t c_myExp      = TColor::GetColor("#28373c");
  TGraph* grshadeExp;
  // Draws the yellow band. Sometimes it even works.
  //if (model == SUSY_RPV) grshadeExp =(TGraph*) DrawExpectedBand(gr_contour_1su, gr_contour_1sd, c_myYellow , 1001, xMin, xMax, yMin, yMax)->Clone();
  grshadeExp = (TGraph*)DrawExpectedBand(gr_contour_1su, gr_contour_1sd, c_myYellow , 1001, xMin, xMax, yMin, yMax)->Clone();
 

  if (discexcl==1) {
  
    //if  (model != SUSY_MUED) DrawContourLine95(leg, gr_contour_obs,     "Observed limit (#pm1 #sigma^{SUSY}_{theory})", c_myRed, 1, 4);
    DrawContourLine95(leg, gr_contour_obs,     "Observed limit ", c_myRed, 1, 4);    
    DrawContourLine95(leg, gr_contour_obs_thUP, "", c_myRed, 3, 2 );  
    DrawContourLine95(leg, gr_contour_obs_thDOWN, "", c_myRed, 3, 2 ); 

    DrawContourLine95(leg, gr_contour,         "", c_myExp, 6, 2 ); 

    DummyLegendExpected(leg, "Expected limit (#pm1 #sigma_{exp})", c_myYellow, 1001, c_myExp, 6, 2);

    if(SR3bIndivGraph){
      cout<<"drawing SR3b line with "<<SR3bIndivGraph->GetN()<<" points"<<endl;
      DrawContourLine95(leg,  SR3bIndivGraph,  fileNameSR3bDesc, kBlue+1, 3, 2);
    }   
    if(SR1bIndivGraph){
      cout<<"drawing SR1b line with "<<SR1bIndivGraph->GetN()<<" points"<<endl;
      DrawContourLine95(leg,  SR1bIndivGraph, fileNameSR1bDesc, kGreen, 3, 2);   
    }
    if(SR0b3jIndivGraph){
      cout<<"drawing SR0b3j line with "<<SR0b3jIndivGraph->GetN()<<" points"<<endl;
      DrawContourLine95(leg,  SR0b3jIndivGraph,fileNameSR0b3jDesc, kAzure+10, 3, 2);   
    }
    if(SR0b5jIndivGraph){
      cout<<"drawing SR0b5j line with "<<SR0b5jIndivGraph->GetN()<<" points"<<endl;
      DrawContourLine95(leg,  SR0b5jIndivGraph,  fileNameSR0b5jDesc, kMagenta, 3, 2);   
    }
  }


  // draw run1 limits
  //DummyLegendExpected (TLegend* leg, TString what,  Int_t fillColor, Int_t fillStyle, Int_t lineColor, Int_t lineStyle, Int_t lineWidth)
  cout<<"Adding lines..."<<endl;
 if(model==SUSY_GTT){
    
   //Run1Curve("Gtt", false);
   CompressedCurve(false);
   //DummyLegendExpected(leg, "#splitline{Run 1 limit}{[arXiv:1507.05525]}",  kWhite, 0, kOrange, 1, 3);
   DummyLegendExpected(leg, "#splitline{SS/3L obs. limit 2015}{[arXiv:1602.09058]}",  kWhite, 0, kBlue, 1, 3);

  } else if(model==SUSY_GG2STEPWZ){

   //Run1Curve("2step",false);
   DummyLegendExpected(leg, "#splitline{SS/3L obs. limit 2015}{[arXiv:1602.09058]}",  kWhite, 0, kBlue, 1, 3);
   DummyLegendExpected(leg, "#splitline{Multijet obs. limit 2015}{[arXiv:1602.06194]}",  kWhite, 0, kViolet, 1, 3);

   //DummyLegendExpected(leg, "#splitline{Run 1 limit}{[arXiv:1507.05525]}",  kWhite, 0, kOrange, 1, 3);
    //DummyLegendExpected(leg, "#splitline{Run 1 limit, SS only}{[arXiv:1507.05525]}",  kWhite, 0, kBlue, 2, 3);

    
  } else if(model==SUSY_BTT){
    

   //Run1Curve("Btt",false);
   DummyLegendExpected(leg, "#splitline{SS/3L obs. limit 2015}{[arXiv:1602.09058]}",  kWhite, 0, kBlue, 1, 3);

    //sbottom();
    


    //DummyLegendExpected(leg, "#splitline{Run 1 limit}{[arXiv:1507.05525]}",  kWhite, 0, kOrange, 1, 3);
    //DummyLegendExpected(leg, "#splitline{Run 1 limit, SS only}{[arXiv:1507.05525]}",  kWhite, 0, kBlue, 2, 3);

    
  } else if(model==SUSY_GSL){

    //Run1Curve("GSL",false); 
    DummyLegendExpected(leg, "#splitline{SS/3L obs. limit 2015}{[arXiv:1602.09058]}",  kWhite, 0, kBlue, 1, 3);

    //DummyLegendExpected(leg, "#splitline{Run 1 limit}{[arXiv:1507.05525]}",  kWhite, 0, kOrange, 1, 3);
    //DummyLegendExpected(leg, "#splitline{Run 1 limit, SS only}{[arXiv:1507.05525]}",  kWhite, 0, kBlue, 2, 3);


  }

 else if(model==SUSY_GG_RPV331){

   cout<<"...RPV_GG line"<<endl;
   //Run1Curve("RPV_GG",false);
   DummyLegendExpected(leg, "ATLAS 8 TeV, 20.3 fb^{-1}",  kWhite, 0, kBlue, 1, 3);
 }

  //  diagonal.Draw("same");

  cout<<"upperLimitFile is "<<upperLimitFile<<std::endl;

  if(upperLimitFile!="None"){
    cout<<"trying to draw upper limits"<<std::endl;
    
    DrawUpperLimits(upperLimitFile,frame, model);

  }



  //++++++++++++++++++++++++++++++++++++++++++++++++++++
  float standardTextSize = 0.05;

  //if (model == SUSY_GMSB2D)  standardTextSize = 0.04;


  //++++++++++++++++++++++++++++++++++++++++++++++++++++

  //if (model == SUSY_MSUGRA || model == SUSY_BRPV) addMSUGRALabels(leg, model);
  
  // build legend
  Float_t textSizeOffset = +0.000;  
  TLatex *Leg0 = 0;
  Leg0 = new TLatex( xMin, yMax + dy*0.025, processDescription );

  Leg0->SetTextAlign( 11 );
  Leg0->SetTextFont( 42 );
  Leg0->SetTextSize( CombinationGlob::DescriptionTextSize);
  Leg0->SetTextColor( 1 );
  if(model == SUSY_GSL || model==SUSY_GG2STEPWZ)
    Leg0->SetTextSize(CombinationGlob::DescriptionTextSize*0.7);
  Leg0->AppendPad();
 

  prefix="Test SR";

  TLatex *Leg1 = new TLatex();
  Leg1->SetNDC();
  Leg1->SetTextFont( 42 );
  Leg1->SetTextSize(  standardTextSize/1.5 );
  Leg1->SetTextColor( kBlack );
  
  //this name will be displayed on all plots
  TString analysisName = "2 same-charge leptons/3 leptons + jets";
  
  //Leg1->DrawLatex(xMinLeg, yMaxLeg + 0.01, analysisName);
  //Leg1->AppendPad();
  
  if( model == SUSY_COMPR_GTT) Leg1->DrawLatex(0.54, yMaxLeg2 - 0.09, TString("#sqrt{s}=13 TeV , ")+Form("%.1f",lumi/1000.)+TString(" fb^{-1}"));
  else Leg1->DrawLatex(xMinLeg2, yMaxLeg2 - 0.09, TString("#sqrt{s}=13 TeV , ")+Form("%.1f",lumi/1000.)+TString(" fb^{-1}"));


  frame->Draw( "sameaxis" );
  
  TLatex* atlasLabel = new TLatex();
  atlasLabel->SetNDC();
  atlasLabel->SetTextFont(72);
  atlasLabel->SetTextColor(kBlack);
  atlasLabel->SetTextSize( standardTextSize - 0.002 );
  if( model == SUSY_COMPR_GTT){ 
    atlasLabel->DrawLatex(0.54, yMaxLeg2 - 0.03,"ATLAS");
    atlasLabel->SetTextFont(42);
    atlasLabel->DrawLatex(0.54+0.16, yMaxLeg2 - 0.03,"Preliminary");
  }
  else{ 
    atlasLabel->DrawLatex(xMinLeg2, yMaxLeg2 - 0.03,"ATLAS");
    atlasLabel->SetTextFont(42);
    atlasLabel->DrawLatex(xMinLeg2+0.16, yMaxLeg2 - 0.03,"Preliminary");
  }
  atlasLabel->AppendPad();


  leg->AddEntry((TObject*)0, "All limits at 95% CL","");
  leg->Draw("same");
  DrawTheoryUncertaintyOnLegend(leg); // keep this line after all modifications on leg are applied!
  c->Update();

  // create plots
  // store histograms to output file
  TObjArray* arr = nominalFileName.Tokenize("/");
  TObjString* objstring = (TObjString*)arr->At( arr->GetEntries()-1 );
  string Strobj = (string)objstring->GetString();
  Strobj.replace(Strobj.find(".root"),5,"");
  TString outfile = Strobj;
  //const TString StrBefore = ".root";
  //const TString StrAfter = "";
//  const char *CharBefore = StrBefore.c_str();
//  const char *CharAfter = StrAfter.c_str();
  //TString outfile = (TString)objstring->GetString().ReplaceAll(".root", "");
  delete arr;

  TString prefixsave = TString(prefix).ReplaceAll(" ","_") + Form("%finvpb_",lumi);
  
  c->SaveAs(Form("exclusion2015SameSign%s.C",outfile.Data()));

  if (showSingleSR) CombinationGlob::imgconv( c, Form("exclusion2015SameSign_Slot%s",outfile.Data()) );   
  else  CombinationGlob::imgconv( c, Form("exclusion2015SameSign%s",outfile.Data()) );   

}
