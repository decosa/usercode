#include "TROOT.h"
#include "TChain.h"
#include "TCut.h"
#include "TH1F.h"
#include "TFile.h"
#include "TSystem.h"
#include "TMath.h"

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

void setGraphics(TH1F *histo){

  histo->SetFillColor(kAzure+7);
  histo->SetLineColor(kBlue+1);
}


TH1F * makeHist(string variable, string title, int nBins, float min, float max, TChain & Events,float scale=1.){

  TH1F * h = new TH1F(title.c_str(),title.c_str(), nBins, min, max);
  Events.Project(title.c_str(), variable.c_str());
  h->Scale(scale);
  setGraphics(h);
  return h;
}

/* add two histos with two different weights*/

TH1F * addHistos(TH1F*h1,TH1F*h2, float w1, float w2, string title){
  TH1F * h = new TH1F(title.c_str(),title.c_str(), h1->GetNbinsX(),h1->GetXaxis()->GetXmin() ,h1->GetXaxis()->GetXmax());
  h->Add(h1,h2,w1,w2);
  //h->Write();
  setGraphics(h);
  return h;
}


/* create a single channel histo adding dau1 and dau2 variable for VBF and GF*/

void singleChannel(string channel, string variable1,string variable2, string title, int nBins, float min, float max, TChain & Events, float scale){

  TH1F * h1 = makeHist((channel+"Higgs"+variable1).c_str(), (title+"1").c_str(), nBins, min,  max, Events,scale);
  TH1F * h2 = makeHist((channel+"Higgs"+variable2).c_str(), (title+"2").c_str(), nBins, min,  max, Events,scale);
  TH1F * h = addHistos(h1,h2,1,1,(title+"Histo").c_str());
  h->Write();
  delete h1; 
  delete h2; 
  delete h; 

}

void histo(string variable, string title, int nBins, float min, float max, TChain & Events,  TCut & cutMu, TCut & cutEl, ofstream & f, float scale, bool b=false, bool w=false){

  TH1F * hmu = new TH1F((title+"mu").c_str(),(title+"mu").c_str(), nBins, min, max);
  TH1F * hel = new TH1F((title+"el").c_str(),(title+"el").c_str() , nBins, min, max);

 /* muon channel + electron channel for VBF events */

  Events.Project((title+"mu").c_str(), ("muHiggs"+variable).c_str(), cutMu);
  Events.Project((title+"el").c_str(), ("elHiggs"+variable).c_str(), cutEl);
  hmu->Sumw2();
  hmu->Add(hel);
  //cout<<"events number: "<<hmu->Integral(0,nBins)<<endl;
  hmu->Scale(scale);
  hmu->SetTitle(title.c_str());

  float error = sqrt(hmu->GetEntries())*scale;

  if(b==true){
    cout<<hmu->GetEntries()*scale<<" +/- "<<error<<endl;
    f<<cout<<hmu->GetEntries()*scale<<" +/- "<<error<<endl;
  }
  setGraphics(hmu);
  if (w==true) hmu->Write();
  
  delete hmu;
  delete hel;

}

void createHistos(string variable, string title, int nBins, float min, float max, TChain & Events, ofstream & f, float scale, bool b = false ){


  /* ****************** */
  /* SELECTION FOR H350 */
  /* ****************** */


    TCut baseSelMu = "(muHiggsLeptDau1Pt>20 && muHiggsLeptDau2Pt>20  && TMath::Abs(muHiggsLeptDau1dB)<0.02 && TMath::Abs(muHiggsLeptDau2dB)<0.02 && (muHiggsLeptDau1Eta < 2.1 || muHiggsLeptDau2Eta < 2.1) && muHiggsJetDau1Pt>30 && muHiggsJetDau2Pt>30 )"; 
    TCut baseSelEl = "elHiggsLeptDau1Pt>20 && elHiggsLeptDau2Pt>20 && elHiggsJetDau1Pt>30 && elHiggsJetDau2Pt>30 && (elHiggsEleDau1VBTF80CombID==7 || elHiggsEleDau2VBTF80CombID==7)";

    TCut massSelMu = baseSelMu && "TMath::Abs(muHiggszllMass - 91)< 10 && TMath::Abs(muHiggszjjMass - 91)< 15";
    TCut massSelEl = baseSelEl && "TMath::Abs(elHiggszllMass - 91)< 10 && TMath::Abs(elHiggszjjMass - 91)< 15";

    TCut btagSelMu = massSelMu && "((muHiggsJet1CSVMVA>0.5 && muHiggsJet2JbProb>0.9 )||( muHiggsJet2CSVMVA>0.5 && muHiggsJet1JbProb>0.9))";
    TCut btagSelEl = massSelEl && "((elHiggsJet1CSVMVA>0.5 && elHiggsJet2JbProb>0.9 )||(elHiggsJet2CSVMVA>0.5 && elHiggsJet1JbProb>0.9))";

    TCut ptllSelMu = btagSelMu && " muHiggszllPt > 90";
    TCut ptllSelEl = btagSelEl && " elHiggszllPt > 90";
    
    TCut metSelMu = ptllSelMu && " met < 35";
    TCut metSelEl = ptllSelEl && " met < 35";

    TCut drjjSelMu = metSelMu && " muHiggsjjdr < 1.7";
    TCut drjjSelEl = metSelEl && " elHiggsjjdr < 1.7";
    
    TCut hmassSelMu = drjjSelMu && " muHiggsMass < 385 &&  muHiggsMass > 315 ";
    TCut hmassSelEl = drjjSelEl && " elHiggsMass < 385 &&  elHiggsMass > 315 ";


    if(b==true){
      cout<<"number of Higgs Candidate after base Selection: "<<endl;
      f<<"number of Higgs Candidate after base Selection: \n";
    }
    histo(variable,(title+"BaseSel").c_str(), nBins, min, max, Events, baseSelMu, baseSelEl, f, scale, b, true);

    if(b==true){
      cout<<"number of Higgs Candidate after mass cut: "<<endl;
      f<<"number of Higgs Candidate after mass cut: \n";
    }
    histo(variable,(title+"MassSel").c_str() , nBins, min, max, Events, massSelMu, massSelEl, f, scale, b);

    if(b==true){
      cout<<"number of Higgs Candidate after btag cut: "<<endl;
      f<<"number of Higgs Candidate after btag cut: \n";
    }
    histo(variable,(title+"BtagSel").c_str() , nBins, min, max, Events,  btagSelMu, btagSelEl, f, scale, b);

    if(b==true){
      cout<<"number of Higgs Candidate after dilepton pt cut: "<<endl;
      f<<"number of Higgs Candidate after dilepton pt cut: \n";
    }
    histo(variable,(title+"ptllSel").c_str() , nBins, min, max, Events,  ptllSelMu, ptllSelEl, f,scale, b);
    
    if(b==true){
      cout<<"number of Higgs Candidate after met cut: "<<endl;
      f<<"number of Higgs Candidate after met cut: \n";
    }
    histo(variable,(title+"metSel").c_str() , nBins, min, max, Events,  metSelMu, metSelEl, f,scale, b );
    
    if(b==true){
      cout<<"number of Higgs Candidate after deltaR jj cut: "<<endl;
      f<<"number of Higgs Candidate after deltaR jj cut: \n";
    }
    histo(variable,(title+"drjjSel").c_str() , nBins, min, max, Events,  drjjSelMu, drjjSelEl, f, scale, b, true);

    if(b==true){
      cout<<"number of Higgs Candidate after higgs mass cut: "<<endl;
      f<<"number of Higgs Candidate after higgs mass cut: \n";
    }
    histo(variable,(title+"hmassSel").c_str() , nBins, min, max, Events, hmassSelMu, hmassSelEl, f,scale, b);
}




void bkgPlots(string s, TChain & Events, float sigma, float nevtin) {

  TFile * output_file = TFile::Open( (s+".root").c_str(), "RECREATE");
  ofstream outFile( (s+"Selection.txt").c_str() );
  if(!outFile) {
    cout<<"Error in file creation!";
  }
  float L= 1000;
  float scaleFact = L*sigma/nevtin ;
 

  
  cout<<s<<endl;
  outFile<<s<<endl;

  //createHistos("Eta", "Eta", 10, -3,3, EventsVBF, EventsGF, VBF, GF);
  createHistos("Mass", "HMass", 200, 0,1000, Events, outFile,scaleFact, true);
  createHistos("Pt", "HPt", 200, 0,1000, Events, outFile, scaleFact);
  createHistos("Eta", "HEta", 13, -6.5,6.5, Events, outFile, scaleFact);
  createHistos("Phi", "HPhi", 7, -3.5,3.5, Events, outFile, scaleFact);
  createHistos("zllMass", "ZllMass", 200, 0,200, Events, outFile, scaleFact);
  createHistos("zjjMass", "ZjjMass", 200, 0,200, Events, outFile, scaleFact);
  createHistos("zllPt", "ZllPt", 200, 0,200, Events, outFile, scaleFact);
  createHistos("zjjPt", "ZjjPt", 200, 0,200, Events, outFile, scaleFact);
  createHistos("zllEta", "ZllEta", 13, -6.5,6.5, Events, outFile, scaleFact);
  createHistos("zjjEta", "ZjjEta", 13, -6-5,6.5, Events, outFile, scaleFact);
  createHistos("zllPhi", "ZllPhi", 13, -6.5,6.5, Events, outFile, scaleFact);
  createHistos("zjjPhi", "ZjjPhi", 13, -6-5,6.5, Events, outFile, scaleFact);
  createHistos("Jet1CSVMVA", "Jet1CSVMVA", 100, -100,100, Events, outFile, scaleFact);
  createHistos("Jet2CSVMVA", "Jet2CSVMVA", 100, -100,100, Events, outFile, scaleFact);
  createHistos("Jet1JbProb", "Jet1JbProb", 100, -100,100, Events, outFile, scaleFact);
  createHistos("Jet2JbProb", "Jet2JbProb", 100, -100,100, Events, outFile, scaleFact);
  createHistos("jjdr", "jjdr", 100, -100,100, Events, outFile, scaleFact);
    
  TH1F * h = makeHist("met", "met", 100, -100,100, Events, scaleFact);
  h->Write();
  delete h;
  /*  singleChannel("mu", "LeptDau1Pt","LeptDau2Pt", "muPt", 100, 0, 200,  Events, scaleFact);
  singleChannel("mu", "LeptDau1Eta","LeptDau2Eta", "muEta", 100, -6., 6.,  Events, scaleFact);
  singleChannel("mu", "LeptDau1Phi","LeptDau2Phi", "muPhi", 100, -3., 3.,  Events, scaleFact);
  singleChannel("el", "LeptDau1Pt","LeptDau2Pt", "elPt", 100, 0, 200,  Events, scaleFact);
  singleChannel("el", "LeptDau1Eta","LeptDau2Eta", "elEta", 100, -6., 6.,  Events, scaleFact);
  singleChannel("el", "LeptDau1Phi","LeptDau2Phi", "elPhi", 100, -3., 3.,  Events, scaleFact);
  singleChannel("mu", "JetDau1Pt","JetDau2Pt", "muChanJetPt", 100, 0, 200,  Events, scaleFact);
  singleChannel("mu", "JetDau1Eta","JetDau2Eta", "muChanJetEta", 100, -6., 6.,  Events, scaleFact);
  singleChannel("mu", "JetDau1Phi","JetDau2Phi", "muChanJetPhi", 100, -3., 3.,  Events, scaleFact);
  singleChannel("el", "JetDau1Pt","JetDau2Pt", "elChanJetPt", 100, 0, 200,  Events, scaleFact);
  singleChannel("el", "JetDau1Eta","JetDau2Eta", "elChanJetEta", 100, -6., 6.,  Events, scaleFact);
  singleChannel("el", "JetDau1Phi","JetDau2Phi", "elChanJetPhi", 100, -3., 3.,  Events, scaleFact);
  */

  outFile.close();
  output_file->Close();
 }


int main() {


  gSystem->Load("libFWCoreFWLite.so");
  AutoLibraryLoader::enable();
  gROOT->SetStyle("Plain");
  TChain EventsTT("Events"); 
  EventsTT.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/TT/edmntp/HTTEdmNtuples.root");
  TChain EventsWZ("Events"); 
  EventsWZ.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/WZ/edmntp/HWZEdmNtuples.root");
  TChain EventsZZ("Events"); 
  EventsZZ.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/ZZ/edmntp/HZZEdmNtuples.root");

  TChain EventsZ0Jet("Events"); 
  EventsZ0Jet.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z0jet/edmntp/HZ0jetEdmNtuples.root");
  TChain EventsZ1Jet("Events"); 
  EventsZ1Jet.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z1jet/edmntp/HZ1jetEdmNtuples.root");
  TChain EventsZ2Jet("Events"); 
  EventsZ2Jet.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z2jet/edmntp/HZ2jetEdmNtuples.root");
  TChain EventsZ3Jet("Events"); 
  EventsZ3Jet.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z3jet/edmntp/HZ3jetEdmNtuples.root");
  TChain EventsZ4Jet("Events"); 
  EventsZ4Jet.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z4jet/edmntp/HZ4jetEdmNtuples.root");
  TChain EventsZ5Jet("Events"); 
  EventsZ5Jet.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z5jet/edmntp/HZ5jetEdmNtuples.root");

  TChain EventsZ1Jet100_300("Events"); 
  EventsZ1Jet100_300.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z1jet100_300/edmntp/HZ1jet100_300EdmNtuples.root");
  TChain EventsZ2Jet100_300("Events"); 
  EventsZ2Jet100_300.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z2jet100_300/edmntp/HZ2jet100_300EdmNtuples.root");
  TChain EventsZ3Jet100_300("Events"); 
  EventsZ3Jet100_300.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z3jet100_300/edmntp/HZ3jet100_300EdmNtuples.root");
  TChain EventsZ4Jet100_300("Events"); 
  EventsZ4Jet100_300.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z4jet100_300/edmntp/HZ4jet100_300EdmNtuples.root");
  TChain EventsZ5Jet100_300("Events"); 
  EventsZ5Jet100_300.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z5jet100_300/edmntp/HZ5jet100_300EdmNtuples.root");


  TChain EventsZ1Jet300_800("Events"); 
  EventsZ1Jet300_800.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z1jet300_800/edmntp/HZ1jet300_800EdmNtuples.root");
  TChain EventsZ2Jet300_800("Events"); 
  EventsZ2Jet300_800.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z2jet300_800/edmntp/HZ2jet300_800EdmNtuples.root");
  TChain EventsZ3Jet300_800("Events"); 
  EventsZ3Jet300_800.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z3jet300_800/edmntp/HZ3jet300_800EdmNtuples.root");
  TChain EventsZ4Jet300_800("Events"); 
  EventsZ4Jet300_800.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z4jet300_800/edmntp/HZ4jet300_800EdmNtuples.root");
  TChain EventsZ5Jet300_800("Events"); 
  EventsZ5Jet300_800.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/Z5jet300_800/edmntp/HZ5jet300_800EdmNtuples.root");

  TChain EventsZBB0("Events"); 
  EventsZBB0.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/ZBB0/edmntp/HZBB0EdmNtuples.root");
  TChain EventsZBB1("Events"); 
  EventsZBB1.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/ZBB1/edmntp/HZBB1EdmNtuples.root");
  TChain EventsZBB2("Events"); 
  EventsZBB2.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/ZBB2/edmntp/HZBB2EdmNtuples.root");
  TChain EventsZBB3("Events"); 
  EventsZBB3.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/ZBB3/edmntp/HZBB3EdmNtuples.root");
  TChain EventsZCC0("Events"); 
  EventsZCC0.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/ZCC0/edmntp/HZCC0EdmNtuples.root");
  TChain EventsZCC1("Events"); 
  EventsZCC1.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/ZCC1/edmntp/HZCC1EdmNtuples.root");
  TChain EventsZCC2("Events"); 
  EventsZCC2.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/ZCC2/edmntp/HZCC2EdmNtuples.root");
  TChain EventsZCC3("Events"); 
  EventsZCC3.Add( "rfio:/castor/cern.ch/user/d/decosa/Higgs/ZCC3/edmntp/HZCC3EdmNtuples.root");

  //bkgPlots("TT", EventsTT, 16.5,940000);
  //bkgPlots("ZZ", EventsZZ, 7.76,1000000);
  //bkgPlots("WZ", EventsWZ, 18.2,2194752);

  //bkgPlots("ZBB3", 0.0353,10898);

  bkgPlots("Z0Jet", EventsZ0Jet, 2006.411, 1411019 );
  bkgPlots("Z1Jet", EventsZ1Jet, 211.824, 37567);
  bkgPlots("Z2Jet", EventsZ2Jet, 36.5417, 118361);
  bkgPlots("Z3Jet", EventsZ3Jet, 4.7675, 55037);
  bkgPlots("Z4Jet", EventsZ4Jet, 0.5866, 44432);
  bkgPlots("Z5Jet", EventsZ5Jet, 0.1182, 10934);

  bkgPlots("Z1Jet100_300", EventsZ1Jet100_300, 5.0173, 265406);
  bkgPlots("Z2Jet100_300", EventsZ2Jet100_300, 3.425, 116852);
  bkgPlots("Z3Jet100_300", EventsZ3Jet100_300, 0.973, 55058);
  bkgPlots("Z4Jet100_300", EventsZ4Jet100_300, 0.199, 44276);
  bkgPlots("Z5Jet100_300", EventsZ5Jet100_300, 0.065, 10563);

  bkgPlots("Z1Jet300_800", EventsZ1Jet300_800, 0.0307, 110308);
  bkgPlots("Z2Jet300_800", EventsZ2Jet300_800, 0.0368, 109393);
  bkgPlots("Z3Jet300_800", EventsZ3Jet300_800, 0.0199, 54262);
  bkgPlots("Z4Jet300_800", EventsZ4Jet300_800, 0.0062, 10874);
  bkgPlots("Z5Jet300_800", EventsZ5Jet300_800, 0.0029, 11146);

  bkgPlots("ZBB0", EventsZBB0, 1.0922, 347393);
  bkgPlots("ZBB1", EventsZBB1, 0.3567, 202581);
  bkgPlots("ZBB2", EventsZBB2, 0.0846, 10842);
  bkgPlots("ZBB3", EventsZBB3, 0.0353, 10898);
  bkgPlots("ZCC0", EventsZCC0, 1.1468, 438067);
  bkgPlots("ZCC1", EventsZCC1, 0.3654, 184365);
  bkgPlots("ZCC2", EventsZCC2, 0.0878, 10735);
  bkgPlots("ZCC3", EventsZCC3, 0.0378, 10177);

}
