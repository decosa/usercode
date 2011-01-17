#include "TROOT.h"
#include "TChain.h"
#include "TCut.h"
#include "TH1F.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TSystem.h"

#include <iostream>
#include <algorithm> 
#include <exception>
#include <iterator>
#include <string>
#include <vector>
#include <map>
#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include<boost/tokenizer.hpp>
#include "FWCore/FWLite/interface/AutoLibraryLoader.h"

using namespace std;

void sigHist(TChain & EventsVBF, TChain & EventsGF, string variable, string title, int nBins, float min, float max, float GF, float VBF ){

  TCanvas c("");
  TH1F *hVBF = new TH1F("hVBF","hVBF", nBins, min, max);
  TH1F *hGF = new TH1F("hGF","hGF", nBins, min, max);
  EventsVBF.Project("hVBF",variable.c_str() );
  EventsGF.Project("hGF",variable.c_str() );
  //hVBF->Draw();
  EventsVBF.Draw("h.mass()");
  TH1F * h = new TH1F(title.c_str(),title.c_str(), nBins, min,max);

  
  h->Add(hVBF,hGF,VBF,GF);

    h->SetLineColor(kBlue+1);
    h->SetFillColor(kAzure+7);

  //h->SetLineColor(kMagenta+3);
  //h->SetFillColor(kMagenta-3);

  //    h->SetLineColor(kTeal+3);
  //  h->SetFillColor(kTeal+2);

  //  h->SetLineColor(kOrange+7);
  //  h->SetFillColor(kYellow-9);

  h->SetMarkerStyle(0);
  h->SetTitle( ("H350, "+title).c_str() );
  h->SetXTitle("m_{H} (GeV/c^{2})");
  //h->hGF->GetXaxis()->SeXmin();
  //h->Scale(1/h->GetEntries());
  h->Draw("HIST");

  h->Write();
  //c.SaveAs( (title+".eps").c_str() );
  delete hVBF;
  delete hGF;
  delete h;

}


int main(){

  gSystem->Load("libFWCoreFWLite.so");
  AutoLibraryLoader::enable();

  gROOT->Reset();
  gROOT->SetStyle("Plain");

  float sigmaVBF = 0.0024;
  float sigmaGF = 0.0256;
  float L = 1000;
  float nEvtVBF = 7122;
  float nEvtGF = 22278;
  float nBins = 20 ;
  float min = 200;
  float max = 600;  
  float VBF = sigmaVBF*L/nEvtVBF;
  float GF = sigmaGF*L/nEvtGF;

  TChain EventsVBF("Events"); 
  TChain EventsGF("Events"); 
  EventsVBF.Add("rfio:/castor/cern.ch/user/d/decosa/Higgs/h350/skim/h2l2b300VBF_1_1_Ukh.root");
  EventsGF.Add("rfio:/castor/cern.ch/user/d/decosa/Higgs/h350/skim/h2l2b300GF_1_1_Ukh.root");

  TFile * output_file = TFile::Open("H350.root", "RECREATE");
  
  sigHist(EventsVBF, EventsGF, "h.mass()", "h350mass", nBins, min,  max, GF, VBF );
  sigHist(EventsVBF, EventsGF, "h.pt()", "h350pt", 30, 0,  300, GF, VBF );
  sigHist(EventsVBF, EventsGF, "h.y()", "h350rapidity", 30, -3.5,  3.5, GF, VBF );
  
  sigHist(EventsVBF, EventsGF, "zmm.mass()", "h350zmm_mass", nBins, 70,  110, GF, VBF );
  sigHist(EventsVBF, EventsGF, "zmm.pt()", "h350zmm_pt", 30, 0,  300, GF, VBF );
  sigHist(EventsVBF, EventsGF, "zmm.y()", "h350zmm_rapidity", 30, -3.5,  3.5, GF, VBF );
  
  sigHist(EventsVBF, EventsGF, "zee.mass()", "h350zee_mass", nBins, 70,  110, GF, VBF );
  sigHist(EventsVBF, EventsGF, "zee.pt()", "h350zee_pt", 30, 0,  300, GF, VBF );
  sigHist(EventsVBF, EventsGF, "zee.y()", "h350zee_rapidity", 30, -3.5,  3.5, GF, VBF );
  
  sigHist(EventsVBF, EventsGF, "zjj.mass()", "h350zjj_mass", nBins, 70,  110, GF, VBF );
  sigHist(EventsVBF, EventsGF, "zjj.pt()", "h350zjj_pt", 30, 0,  300, GF, VBF );
  sigHist(EventsVBF, EventsGF, "zjj.y()", "h350zjj_rapidity", 30, -3.5,  3.5, GF, VBF );
  output_file->Close();
}
