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

 Events.Add("H300VBFEdmNtuples.root", 65);

 TFile * output_file = TFile::Open("higgsHisto.root", "RECREATE");

 

 TCut selection_el(" elHiggsLeptDau1Pt>20 && elHiggsLeptDau2Pt>20 && elHiggsJetDau1Pt>30 && elHiggsJetDau2Pt>30 && (elHiggsEleDau1VBTF80CombID || elHiggsEleDau1VBTF80CombID) && elHiggsjjdr < 1.8 && ((elHiggsJet1CSVMVA>0.5 && elHiggsJet2JbProb>0.9 )||(elHiggsJet2CSVMVA>0.5 && elHiggsJet1JbProb>0.9)) && met < 35");


 TDirectory * dir = output_file->mkdir("muHiggsPlots");
 dir->cd();


 int zMassCut = Events.GetEntries("muHiggsLeptDau1Pt>20 && muHiggsLeptDau2Pt>20  && abs(muHiggsLeptDau1dB)<0.02 && abs(muHiggsLeptDau2dB)<0.02 && (muHiggsLeptDau1Eta < 2.1 || muHiggsLeptDau2Eta < 2.1) && muHiggsJetDau1Pt>30 && muHiggsJetDau2Pt>30 && abs(muHiggszllMass - 91)< 10 && abs(muHiggszjjMass - 91)< 15");

 cout<<"Number of higgs candidate (zMass cut): "<<zMassCut<<endl;

 int bTaggingCut = Events.GetEntries("muHiggsLeptDau1Pt>20 && muHiggsLeptDau2Pt>20  && abs(muHiggsLeptDau1dB)<0.02 && abs(muHiggsLeptDau2dB)<0.02 && (muHiggsLeptDau1Eta < 2.1 || muHiggsLeptDau2Eta < 2.1) && muHiggsJetDau1Pt>30 && muHiggsJetDau2Pt>30 && abs(muHiggszllMass - 91)< 10 && abs(muHiggszjjMass - 91)< 15 && ((muHiggsJet1CSVMVA>0.5 && muHiggsJet2JbProb>0.9 )||(muHiggsJet2CSVMVA>0.5 && muHiggsJet1JbProb>0.9)) && met < 35");

 cout<<"Number of higgs candidate (btagging cut): "<<bTaggingCut<<endl;


 TH1F * hMass = new TH1F("hMass", "hMass", 200, 200, 500);

 TCut selection_mu("muHiggsLeptDau1Pt>20 && muHiggsLeptDau2Pt>20  && abs(muHiggsLeptDau1dB)<0.02 && abs(muHiggsLeptDau2dB)<0.02 && (muHiggsLeptDau1Eta < 2.1 || muHiggsLeptDau2Eta < 2.1) && muHiggsJetDau1Pt>30 && muHiggsJetDau2Pt>30 && muHiggsjjdr < 1.8 && ((muHiggsJet1CSVMVA>0.5 && muHiggsJet2JbProb>0.9 )||(muHiggsJet2CSVMVA>0.5 && muHiggsJet1JbProb>0.9)) && met < 35");
 Events.Project("hMass", "muHiggsMass", selection_mu );

 cout<<"Number of higgs candidate : "<<hMass->GetEntries()<<endl;

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
