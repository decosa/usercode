#include "TFile.h"
#include "TH1F.h"
#include "TCut.h"
#include "TTree.h"
#include "TAxis.h"
#include "TCanvas.h"
#include "TChain.h"
#include "TROOT.h"
#include "TStyle.h"
#if !defined(__CINT__) && !defined(__MAKECINT__)                                                                                                          
#include <string>
#include <iostream>
#endif   




void setGraphics(TH1F *histo){

  histo->SetFillColor(kAzure+7);
  //histo->SetLineWidth(2);
  histo->SetLineColor(kBlue+1);
}


void H2l2b(){

 gStyle->SetOptStat();
 gROOT->SetStyle("Plain");
 using namespace std;


 TChain Events("Events"); 
//   // one need 130 events... each file has 1000 ev
 Events.Add("H300EdmNtuples.root", 65);
//   //  Events.Add("zmmNtuple/NtupleLooseTestNew_oneshot_all_Test_1_None.root", 65);

  
 TFile * output_file = TFile::Open("higgsHisto.root", "RECREATE");
//   // TFile * output_file = TFile::Open("histo_test.root", "RECREATE");
  
 // TCut cut_muons("muHiggsLeptDau1Pt>20 && muHiggsLeptDau2Pt>20  && abs(muHiggsLeptDau1dB)<0.02 && abs(muHiggsLeptDau2dB)<0.02 && (muHiggsLeptDau1Eta < 2.1 || muHiggsLeptDau2Eta < 2.1)");
//  TCut cut_electrons("elHiggsLeptDau1Pt>20 && elHiggsLeptDau2Pt>20");
//  TCut cut_mujets("muHiggsJetDau1Pt>30 && muHiggsJetDau2Pt>30 ");
//  TCut cut_eljets("elHiggsJetDau1Pt>30 && elHiggsJetDau2Pt>30 && (elHiggsEleDau1VBTF80CombID || elHiggsEleDau1VBTF80CombID");


 TCut selection("muHiggsLeptDau1Pt>20 && muHiggsLeptDau2Pt>20  && abs(muHiggsLeptDau1dB)<0.02 && abs(muHiggsLeptDau2dB)<0.02 && (muHiggsLeptDau1Eta < 2.1 || muHiggsLeptDau2Eta < 2.1) &&  elHiggsLeptDau1Pt>20 && elHiggsLeptDau2Pt>20 && muHiggsJetDau1Pt>30 && muHiggsJetDau2Pt>30 && elHiggsJetDau1Pt>30 && elHiggsJetDau2Pt>30 && (elHiggsEleDau1VBTF80CombID || elHiggsEleDau1VBTF80CombID)");

 TDirectory * dir = output_file->mkdir("muHiggsPlots");
 dir->cd();
 TH1F * hMass = new TH1F("hMass", "hMass", 200, 200, 500);
 Events.Project("hMass", "muHiggsMass", selection );
 // Events.Project("hMass", "muHiggsMass");
 cout<<"Number of higgs candidate : "<<hMass->GetEntries()<<endl;
//   hMass->SetFillColor(kAzure+7);
//   hMass->SetLineColor(kBlue+1);
 setGraphics(hMass);
 hMass->Draw(); 
 hMass->Write();
 delete hMass;

 // output_file->Close();

// //   TCut cut_zGoldenPt15("zGoldenMass>20 && zGoldenDau1Pt> 15 && zGoldenDau2Pt>15 && zGoldenDau1Iso< 3.0 && zGoldenDau2Iso < 3.0  &&  abs(zGoldenDau1Eta)<2.1 &&  abs(zGoldenDau2Eta)<2.1 && zGoldenDau1Chi2<10 && zGoldenDau2Chi2<10 && abs(zGoldenDau1dxyFromBS)<0.2 && abs(zGoldenDau2dxyFromBS)<0.2 &&(zGoldenDau1NofStripHits + zGoldenDau1NofPixelHits)>=10 && (zGoldenDau2NofStripHits + zGoldenDau2NofPixelHits)>=10 && zGoldenDau1NofMuonHits>0 && zGoldenDau2NofMuonHits>0 && (zGoldenDau1HLTBit==1 || zGoldenDau2HLTBit==1)");
// //   dir->cd();
  
// //   TH1F * zMassPt15 = new TH1F("zMassPt15", "zMassPt15", 200, 0, 200);
// //   Events.Project("zMassPt15", "zGoldenMass", cut_zGoldenPt15  );
// //   setGraphics(zMassPt15);
// //   cout<<"Number of zGoldenPt15 : "<<zMassPt15->GetEntries()<<endl;
// //   zMassPt15->Write();
// //   delete zMassPt15;



// //   output_file->cd("/");
  


// //  output_file->Close();
 
 
}
