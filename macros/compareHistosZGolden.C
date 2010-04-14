#include "TFile.h"
#include "TH1F.h"
#include "TTree.h"
#include "TAxis.h"
#include "TCanvas.h"
//#if !defined(__CINT__) && !defined(__MAKECINT__)
#include <string>
#include <iostream>
//#endif
void histodiff( TFile *out,TTree* events, TTree* events2, const char* category,const char* variable, int bins, int min, int max){

  gStyle->SetOptStat();
  std::string value = std::string(category) + std::string(variable) ;
  int min_ = min;
  int max_ = max;
  int nBins = bins;
  double a,b;
  TCanvas *c = new TCanvas((value).c_str(),(value).c_str());

  // c->Divide(1,4);
  c->Divide(1,3);
  c->SetLogy();    
  c->cd(1);

  TH1F * histo = new TH1F((value + "_NewNtp").c_str(),(value + "_NewNtp").c_str(), nBins, min_, max_);
  events->Project((value + "_NewNtp").c_str(), value.c_str() );

  histo->Draw();
  //histo->Fill(0.6,30);
  
  TH1F * histo2 = new TH1F((value).c_str(),(value).c_str() , nBins, min_, max_);
  
  
  //TH1F * histo3 = new TH1F((value +"2").c_str(),(value+"2").c_str() , nBins, min_, max_);
  //histo3->Clone((value).c_str());
  events2->Project((value).c_str(), value.c_str() );
  //histo2->Fill(0.1,30);
  
  histo2->SetLineColor(kRed);
  
  //TH1F * histo3 = (TH1F*)histo2->Clone((value+"_comparison").c_str());
  //histo2->Draw("same");
  TH1F * histo3 = new TH1F((value+"comp").c_str(),(value+"comp").c_str() , nBins, min_, max_);
  
  //a->SetLimits(-1,1);
  //histo2->SetMaximum(1);
  //histo2->SetMinimum(-1);
  c->cd(2);
  histo2->Draw();
  c->cd(3);
  //histo3->Add(histo, -1);
  //histo3->Draw();
  //histo->Draw();
  //histo2->Draw("same");
  //c->cd(4);
  for(int i=0; i<histo->GetEntries(); ++i){
    a=histo->GetBinContent(i);
    b=histo2->GetBinContent(i);
    histo3->SetBinContent(i,(a-b));
  }
  histo3->SetMaximum(10);
  histo3->SetMinimum(-10);
  histo3->Draw();
  //TDirectory * dir = output_file->mkdir(category);
  //dir->cd();
  
  //c->SaveAs((value+".png").c_str());
  c->Write();
  //histo2->Write();
  delete c;
}

void compareHistos(){
  
  gSystem->Load("libFWCoreFWLite");

  AutoLibraryLoader::enable();

  TFile *file = TFile::Open("NtupleLooseTestNew.root");
  TTree * events = dynamic_cast< TTree *> (file->Get("Events"));
  TFile *file2 = TFile::Open("NtupleLoose_test.root");
  TTree * events2 = dynamic_cast< TTree *> (file2->Get("Events"));

  TFile out("zGolden.root", "RECREATE");
  //histodi\%ff("","", , ,);
  histodiff( &out, events, events2, "zGolden","Mass",80 ,0 ,110);
  histodiff( &out, events, events2, "zGolden","Pt",80 ,0 ,300);
  histodiff( &out, events, events2, "zGolden","Eta",80 ,-5,5);
  histodiff( &out, events, events2, "zGolden","Phi",80 ,-3.5 ,3.5);
  histodiff( &out, events, events2, "zGolden","Y",80 ,-2.5,2.5);
  histodiff( &out, events, events2, "zGolden","Dau1Pt",80 ,0 ,250);
  histodiff( &out, events, events2, "zGolden","Dau2Pt",80 ,0 ,250);
  histodiff( &out, events, events2, "zGolden","Dau1Q",80 ,-2 ,2);
  histodiff( &out, events, events2, "zGolden","Dau2Q",80 ,-2 ,2);
  histodiff( &out, events, events2, "zGolden","Dau1Eta",80 ,-2.5, 2.5);
  histodiff( &out, events, events2, "zGolden","Dau1Phi",80 ,-3.5, 3.5);
  histodiff( &out, events, events2, "zGolden","Dau2Eta",80 ,-2.5, 2.5);
  histodiff( &out, events, events2, "zGolden","Dau2Phi",80 ,-3.5, 3.5);
  histodiff( &out, events, events2, "zGolden","Dau1NofHit",80 ,0, 26);
  histodiff( &out, events, events2, "zGolden","Dau1NofHitTk",80 ,0 ,26);
  histodiff( &out, events, events2, "zGolden","Dau1NofHitSta",80 ,0 ,55);
  histodiff( &out, events, events2, "zGolden","Dau1NofMuChambers",80 ,0 ,11);
  histodiff( &out, events, events2, "zGolden","Dau1NofMuMatches",80 ,0 ,8);
  histodiff( &out, events, events2, "zGolden","Dau2NofHit",80 ,0, 26);
  histodiff( &out, events, events2, "zGolden","Dau2NofHitTk",80 ,0 ,26);
  histodiff( &out, events, events2, "zGolden","Dau2NofHitSta",80 ,0 ,55);
  histodiff( &out, events, events2, "zGolden","Dau2NofMuChambers",80 ,0 ,11);
  histodiff( &out, events, events2, "zGolden","Dau2NofMuMatches",80 ,0 ,8);
  histodiff( &out, events, events2, "zGolden","Dau1Chi2",80 ,0 ,3.25);
  histodiff( &out, events, events2, "zGolden","Dau2Chi2",80 ,0 ,3.25);
  histodiff( &out, events, events2, "zGolden","Dau1HLTBit",80 ,0 ,1.3);  
  histodiff( &out, events, events2, "zGolden","Dau2HLTBit",80 ,0 ,1.3);  
  histodiff( &out, events, events2, "zGolden","Dau1Iso",80 ,0 ,2.3);  
  histodiff( &out, events, events2, "zGolden","Dau2Iso",80 ,0 ,2.3);  
  histodiff( &out, events, events2, "zGolden","Dau1TrkIso",80 ,0 ,2.3);
  histodiff( &out, events, events2, "zGolden","Dau1EcalIso",80 ,0 ,1.2);
  histodiff( &out, events, events2, "zGolden","Dau1HcalIso",80 ,0 ,1);
  histodiff( &out, events, events2, "zGolden","Dau2TrkIso",80 ,0 ,2.3);
  histodiff( &out, events, events2, "zGolden","Dau2EcalIso",80 ,0 ,1.2);
  histodiff( &out, events, events2, "zGolden","Dau2HcalIso",80 ,0 ,1);
  histodiff( &out, events, events2, "zGolden","Dau1dxyFromBS",800 ,-1 ,1);
  histodiff( &out, events, events2, "zGolden","Dau1dzFromBS",800 ,-10 ,9);
  histodiff( &out, events, events2, "zGolden","Dau1dxyFromPV",800 ,-1 ,1);
  histodiff( &out, events, events2, "zGolden","Dau1dzFromPV",800 ,-1,1);
  histodiff( &out, events, events2, "zGolden","Dau2dxyFromBS",800 ,-1 ,1);
  histodiff( &out, events, events2, "zGolden","Dau2dzFromBS",800 ,-10 ,9);
  histodiff( &out, events, events2, "zGolden","Dau2dxyFromPV",800 ,-1 ,1);
  histodiff( &out, events, events2, "zGolden","Dau2dzFromPV",800 ,-1, 1);
  histodiff( &out, events, events2, "zGolden","VtxNormChi2",80 ,-1,1);
  histodiff( &out, events, events2, "zGolden","Dau1TrkChi2",80 ,0 ,1.7);
  histodiff( &out, events, events2, "zGolden","Dau2TrkChi2",80 ,0 ,1.7);
  histodiff( &out, events, events2, "zGolden","Dau1MuEnergyHad",80 ,0 ,6);
  histodiff( &out, events, events2, "zGolden","Dau2MuEnergyHad",80 ,0 ,6);
  histodiff( &out, events, events2, "zGolden","Dau1MuEnergyEm",80 ,-0.1 ,1);
  histodiff( &out, events, events2, "zGolden","Dau2MuEnergyEm",80 ,-0.1 ,1);
  histodiff( &out, events, events2, "zGolden","TrueMass",80 ,0 ,1.3);
  histodiff( &out, events, events2, "zGolden","TruePt",80 ,0 ,1.3);
  histodiff( &out, events, events2, "zGolden","TrueEta",80 ,0 ,1.3);
  histodiff( &out, events, events2, "zGolden","TruePhi",80 ,0 ,1.3);
  histodiff( &out, events, events2, "zGolden","TrueY",80 ,0 ,1.3);
  histodiff( &out, events, events2, "zGolden","MassSa",80 ,0 ,250);
  histodiff( &out, events, events2, "zGolden","Dau1SaPt",80 ,0 ,250);
  histodiff( &out, events, events2, "zGolden","Dau1SaEta",80 ,-2.5 ,2.5);
  histodiff( &out, events, events2, "zGolden","Dau1SaPhi",80 ,-3.5 ,3.5);
  histodiff( &out, events, events2, "zGolden","Dau2SaPt",80 ,0 ,250);
  histodiff( &out, events, events2, "zGolden","Dau2SaEta",80 ,-2.5,2.5);
  histodiff( &out, events, events2, "zGolden","Dau2SaPhi",80 ,-3.5 ,3.5);

 //return 0;
  out.Close(); 
}
