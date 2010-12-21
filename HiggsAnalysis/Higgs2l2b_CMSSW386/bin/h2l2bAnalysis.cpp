#include "TROOT.h"
#include "TChain.h"
#include "TCut.h"
#include "TH1F.h"
#include "TFile.h"

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

using namespace std;
//using namespace boost;


/* fill a histo with the distribution of a variable taken by TChain Events*/

void setGraphics(TH1F *histo){

  histo->SetFillColor(kAzure+7);
  histo->SetLineColor(kBlue+1);
}


TH1F * makeHist(string variable, string title, int nBins, float min, float max, TChain & Events,float scale){
  TH1F * h = new TH1F(title.c_str(),title.c_str(), nBins, min, max);
  Events.Project(title.c_str(), variable.c_str());
  h->Scale(scale);
  cout<<h->Integral(min, max)<<endl;
  //h->Write();
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

TH1F * singleChannel(string channel, string variable1,string variable2, string title, int nBins, float min, float max, TChain & EventsVBF, TChain & EventsGF, float VBF, float GF){

  TH1F * h1VBF = makeHist((channel+"Higgs"+variable1).c_str(), title, nBins, min,  max, EventsVBF,1);
  TH1F * h2VBF = makeHist((channel+"Higgs"+variable2).c_str(), title, nBins, min,  max, EventsVBF,1);
  TH1F * hVBF = addHistos(h1VBF,h2VBF,1,1,title);  
  TH1F * h1GF = makeHist((channel+"Higgs"+variable1).c_str(), title, nBins, min,  max, EventsGF,1);
  TH1F * h2GF = makeHist((channel+"Higgs"+variable2).c_str(), title, nBins, min,  max, EventsGF,1);
  TH1F * hGF = addHistos(h1GF,h2GF,1,1,title);
  setGraphics(addHistos(hVBF, hGF, VBF, GF, title));
  return addHistos(hVBF, hGF, VBF, GF, title);

}

/* create an histo combining electron and muon channel for that variable (VBF and GF)*/

TH1F * combHistos(string variable, string title, int nBins, float min, float max, TChain & EventsVBF, TChain & EventsGF,float VBF, float GF){
  TH1F * hVBF = makeHist(variable, title + "VBF", nBins, min, max, EventsVBF, VBF);
  TH1F * hGF = makeHist(variable, title + "GF", nBins, min, max, EventsGF, GF);
  //  TH1F * hVBF = new TH1F((title+"VBF").c_str(),(title+"VBF").c_str(), nBins, min, max);
  //  TH1F * hGF = new TH1F((title+"GF").c_str(),(title+"GF").c_str(), nBins, min, max);
  TH1F * h = new TH1F((title).c_str(),title.c_str(), nBins, min, max);

  //  EventsVBF.Project((title+"VBF").c_str(), (variable).c_str());
  //  EventsGF.Project((title+"GF").c_str(), (variable).c_str());

  //  hVBF->Scale(VBF);
  //  hGF->Scale(GF);

  h->Add(hVBF,hGF);
  cout<<h->Integral(min, max)<<endl;
  
  //h->Write();
  

  delete hVBF;
  delete hGF;
  setGraphics(h);
  return h;

}

void histo(string variable, string title, int nBins, float min, float max, TChain & EventsVBF, TChain & EventsGF,float VBF, float GF, TCut & cutMu, TCut & cutEl, bool b=false){

  TH1F * h = new TH1F((title).c_str(),title.c_str(), nBins, min, max);
  TH1F * hVBFmu = new TH1F((title+"VBFmu").c_str(),(title+"VBFmu").c_str(), nBins, min, max);
  TH1F * hVBFel = new TH1F((title+"VBFel").c_str(),(title+"VBFel").c_str() , nBins, min, max);
  TH1F * hGFmu = new TH1F((title + "GFmu").c_str(),(title+"GFmu").c_str() , nBins, min, max);
  TH1F * hGFel = new TH1F((title+"GFel").c_str(), (title+"GFel").c_str(), nBins, min, max);


  /*TH1F * hVBFmu = makeHist(variable, title + "VBFmu", nBins, min, max, EventsVBF, VBF, file);
  TH1F * hGFmu = makeHist(variable, title + "GFmu", nBins, min, max, EventsGF, GF, file);
  TH1F * hVBFel = makeHist(variable, title + "VBFel", nBins, min, max, EventsVBF, VBF, file);
  TH1F * hGFel = makeHist(variable, title + "GFel", nBins, min, max, EventsGF, GF, file);
  */

 /* muon channel + electron channel for VBF events */

  EventsVBF.Project((title+"VBFmu").c_str(), ("muHiggs"+variable).c_str(), cutMu);
  EventsVBF.Project((title+"VBFel").c_str(), ("elHiggs"+variable).c_str(), cutEl);
  hVBFmu->Sumw2();
  //  cout<<" mu "<<hVBFmu->GetEntries() <<endl;
  //  cout<<" el "<<hVBFel->GetEntries() <<endl;
  hVBFmu->Add(hVBFel);
  //  cout<<" el + mu VBF "<<hVBFmu->Integral(0,1000) <<endl;
    
  /* muon channel + electron channel for GF events */
  
  EventsGF.Project((title+"GFmu").c_str(), ("muHiggs"+variable).c_str(),cutMu);
  EventsGF.Project((title+"GFel").c_str(), ("elHiggs"+variable).c_str(),cutEl );
  hGFmu->Sumw2();
  hGFmu->Add(hGFel);
  

//  cout<<" el + mu GF "<<hGFmu->Integral(0,1000) <<endl;
  //h->Sumw2();
  
  
  /* VBF + GF - First Method - Bin per Bin */
  /*
    for(int b=0; b<h_presel->GetNbinsX(); ++b){
    
    h_presel->SetBinContent(b, (hVBF_presel_mu->GetBinContent(b))*VBF + (hGF_presel_mu->GetBinContent(b))*GF);
    }    
    
    cout<<"Number of higgs candidate (VBF channel) after pre-selection: "<<h_presel->Integral(min, max) <<endl;
  */
  /* VBF + GF - Second Method - Scale*/
  

  float VBFerror = sqrt(hVBFmu->Integral(min, max))*VBF;
  float GFerror = sqrt(hGFmu->Integral(min, max))*GF;
  hVBFmu->Scale(VBF);
  //  cout<<" VBF after Scale "<<hVBFmu->Integral(min, max)<<endl;
  hGFmu->Scale(GF);
  //  cout<<" GF after Scale "<<hGFmu->Integral(min, max)<<endl;
  //h->Sumw2();
  h->Add(hVBFmu,hGFmu);
  float error = sqrt(pow(VBFerror,2)+pow(GFerror,2));
  if(b==true) cout<<h->Integral(min, max)<<" +/- "<<error<<endl;
  setGraphics(h);
  h->Write();
  
  delete hVBFmu;
  delete hVBFel;
  delete hGFmu;
  delete hGFel;
  delete h;
}

void createHistos(string variable, string title, int nBins, float min, float max, TChain & EventsVBF, TChain & EventsGF,float VBF, float GF, bool b = false ){


    TCut baseSelMu = "(muHiggsLeptDau1Pt>20 && muHiggsLeptDau2Pt>20  && abs(muHiggsLeptDau1dB)<0.02 && abs(muHiggsLeptDau2dB)<0.02 && (muHiggsLeptDau1Eta < 2.1 || muHiggsLeptDau2Eta < 2.1) && muHiggsJetDau1Pt>30 && muHiggsJetDau2Pt>30 )"; 
    TCut baseSelEl = "elHiggsLeptDau1Pt>20 && elHiggsLeptDau2Pt>20 && elHiggsJetDau1Pt>30 && elHiggsJetDau2Pt>30 && (elHiggsEleDau1VBTF80CombID!=0 || elHiggsEleDau1VBTF80CombID!=0)";

    TCut massSelMu = baseSelMu && "abs(muHiggszllMass - 91)< 10 && abs(muHiggszjjMass - 91)< 15";
    TCut massSelEl = baseSelEl && "abs(elHiggszllMass - 91)< 10 && abs(elHiggszjjMass - 91)< 15";

    //    TCut btagSelMu = massSelMu && "((muHiggsJet1CSVMVA>0.5 && muHiggsJet2JbProb>0.9 )||( muHiggsJet2CSVMVA>0.5 && muHiggsJet1JbProb>0.9))";
    //    TCut btagSelEl = massSelEl && "((elHiggsJet1CSVMVA>0.5 && elHiggsJet2JbProb>0.9 )||(elHiggsJet2CSVMVA>0.5 && elHiggsJet1JbProb>0.9))";

    TCut btagSelMu = massSelMu && "(muHiggsJet1CSVMVA>0.5 ||muHiggsJet2CSVMVA>0.5)";;
    TCut btagSelEl = massSelEl && "(elHiggsJet1CSVMVA>0.5 ||elHiggsJet2CSVMVA>0.5)";

    //    TCut btagSelMu = massSelMu && "((muHiggsJet1CSVMVA>0.5 && muHiggsJet2JbProb>0.9 )||( muHiggsJet2CSVMVA>0.5 && muHiggsJet1JbProb>0.9))";
    //    TCut btagSelEl = massSelEl && "((elHiggsJet1CSVMVA>0.5 && elHiggsJet2JbProb>0.9 )||(elHiggsJet2CSVMVA>0.5 && elHiggsJet1JbProb>0.9))";

    TCut drjjSelMu = btagSelMu && " muHiggsjjdr < 1.8";
    TCut drjjSelEl = btagSelEl && " elHiggsjjdr < 1.8";

    TCut metSelMu = drjjSelMu && " met < 35";
    TCut metSelEl = drjjSelEl && " met < 35";
    
    TCut hmassSelMu = metSelMu && " muHiggsMass < 330 &&  muHiggsMass > 270 ";
    TCut hmassSelEl = metSelEl && " elHiggsMass < 330 &&  elHiggsMass > 270 ";

    if(b==true) cout<<"number of Higgs Candidate after base Selection: "<<endl;
    histo(variable,(title+"BaseSel").c_str(), nBins, min, max, EventsVBF, EventsGF, VBF,GF, baseSelMu, baseSelEl, b);
    if(b==true) cout<<"number of Higgs Candidate after mass cut: "<<endl;
    histo(variable,(title+"MassSel").c_str() , nBins, min, max, EventsVBF, EventsGF, VBF,GF, massSelMu, massSelEl, b);
    if(b==true) cout<<"number of Higgs Candidate after btag cut: "<<endl;
    histo(variable,(title+"BtagSel").c_str() , nBins, min, max, EventsVBF, EventsGF, VBF,GF,  btagSelMu, btagSelEl, b);
    if(b==true) cout<<"number of Higgs Candidate after met cut: "<<endl;
    histo(variable,(title+"metSel").c_str() , nBins, min, max, EventsVBF, EventsGF, VBF,GF,  metSelMu, metSelEl, b);
    if(b==true) cout<<"number of Higgs Candidate after higgs mass cut: "<<endl;
    histo(variable,(title+"hmassSel").c_str() , nBins, min, max, EventsVBF, EventsGF, VBF,GF, hmassSelMu, hmassSelEl, b);

 
}





int main() {

  TFile * output_file = TFile::Open("histoH2l2b.root", "RECREATE");


  typedef boost::tokenizer<boost::char_separator<char> > tokenizer;
  boost::char_separator<char> sep(" ");
  const int max_line_len = 1024;
  gROOT->SetStyle("Plain");
  
  char str[max_line_len];
  ifstream inFile("test.txt");

  bool hFlag = true;
  map<string,vector<double> > data;

  while ( inFile ) {
    inFile.getline(str, max_line_len);
    //cout << str << endl;
    string s(str);
    tokenizer tok(s, sep);
    tokenizer::iterator i = tok.begin();
    if(i == tok.end() || (*i)[0] == '#') continue;
    string key = *i; ++i;
    if(hFlag && key != "hMass") {
      cerr << "first datacard line must be hMass" << endl;
      exit(100);
    }
    hFlag = false;
    vector<double> & v = data[key];
    for(; i!=tok.end();++i){
      stringstream ss(stringstream::in | stringstream::out);
      ss << *i;
      double x;
      ss>>x;
      v.push_back(x);
    }
    if(v.size() != data["hMass"].size()) {
      cerr << "all data lines must have the same number of entries" << endl;
      exit (101);
    }
  }


  cout<<"vbf events"<<data["VBFevents"][0]<<endl;
  TChain EventsVBF("Events"); 
  TChain EventsGF("Events"); 


  //  for(int k; k < v.size(); ++k){

  //TDirectory * dir = output_file->mkdir("hmassPlots");

  cout<<"size "<<data["hMass"].size()<<endl; 
  for(unsigned int k = 0; k <1; ++k){
    //  for(unsigned int k = 0; k < data["hMass"].size(); ++k){
  
    cout<< "MASS " << data["hMass"][k]<< endl;
  //    cout<<"mass"<<mass<<endl;
    //EventsVBF.Add("H300VBFEdmNtuples.root");
    EventsVBF.Add("rfio:/castor/cern.ch/user/d/decosa/Higgs/h300/edmntp/H300VBFEdmNtuples.root");
    EventsGF.Add("rfio:/castor/cern.ch/user/d/decosa/Higgs/h300/edmntp/H300GFEdmNtuples.root");
    //EventsGF.Add("H300GFEdmNtuples.root");

    float VBF = data["VBFxsec"][k]*1000/data["VBFevents"][k] ;
    float GF = data["GFxsec"][k]*1000/data["GFevents"][k];

    
    cout<<"VBF "<<VBF <<endl;
    cout<<"GF "<<GF <<endl;

    //    TCut sel_el(" elHiggsjjdr < 1.8 && ((elHiggsJet1CSVMVA>0.5 && elHiggsJet2JbProb>0.9 )||(elHiggsJet2CSVMVA>0.5 && elHiggsJet1JbProb>0.9)) && met < 35");


    TCut baseSelMu = "(muHiggsLeptDau1Pt>20 && muHiggsLeptDau2Pt>20  && abs(muHiggsLeptDau1dB)<0.02 && abs(muHiggsLeptDau2dB)<0.02 && (muHiggsLeptDau1Eta < 2.1 || muHiggsLeptDau2Eta < 2.1) && muHiggsJetDau1Pt>30 && muHiggsJetDau2Pt>30 )"; 
    TCut baseSelEl = "elHiggsLeptDau1Pt>20 && elHiggsLeptDau2Pt>20 && elHiggsJetDau1Pt>30 && elHiggsJetDau2Pt>30 && (elHiggsEleDau1VBTF80CombID!=0 || elHiggsEleDau1VBTF80CombID!=0)";
    TCut massSelMu = baseSelMu && "abs(muHiggszllMass - 91)< 10 && abs(muHiggszjjMass - 91)< 15";
    TCut massSelEl = baseSelEl && "abs(elHiggszllMass - 91)< 10 && abs(elHiggszjjMass - 91)< 15";
    
    //dir->cd();


    /* *** BASE SELECTION *** */

    /*    TH1F * mupt = new TH1F("mupt", "mupt", 200, 0, 1000);
    TH1F * elpt = new TH1F("elpt", "elpt", 200, 0, 1000);
    TH1F * jpt = new TH1F("jpt", "jpt", 200, 0, 1000);
    TH1F * gf_mupt = new TH1F("GFmupt", "GFmupt", 200, 0, 1000);
    TH1F * gf_elpt = new TH1F("GFelpt", "GFelpt", 200, 0, 1000);
    TH1F * gf_jpt = new TH1F("GFjpt", "GFjpt", 200, 0, 1000);
    TH1F * met = new TH1F("met", "met", 200, 0, 1000);
    TH1F * btag1 = new TH1F("btag1", "btag1", 200, 0, 1000);
    TH1F * btag2 = new TH1F("batg2", "btag2", 200, 0, 1000);
    TH1F * gf_met = new TH1F("GFmet", "GFmet", 200, 0, 1000);
    TH1F * gf_btag1 = new TH1F("GFbtag1", "GFbtag1", 200, 0, 1000);
    TH1F * gf_btag2 = new TH1F("GFbatg2", "GFbtag2", 200, 0, 1000);
    TH1F * drjj = new TH1F("drjj", "drjj", 200, 0, 1000);
    TH1F * zllmass = new TH1F("zllmass", "zllmass", 200, 0, 1000);
    TH1F * zjjmass = new TH1F("zjjmass", "zjjmass", 200, 0, 1000);
    TH1F * gf_drjj = new TH1F("GFdrjj", "GFdrjj", 200, 0, 1000);
    TH1F * gf_zllmass = new TH1F("GFzllmass", "GFzllmass", 200, 0, 1000);
    TH1F * gf_zjjmass = new TH1F("GFzjjmass", "GFzjjmass", 200, 0, 1000);
    TH1F * hmass = new TH1F("hmass", "hmass", 200, 0, 1000);
    TH1F * dileptPt = new TH1F("dileptPt", "dileptPt", 200, 0, 1000);
    TH1F * gf_hmass = new TH1F("GFhmass", "GFhmass", 200, 0, 1000);
    TH1F * gf_dileptPt = new TH1F("GFdileptPt", "GFdileptPt", 200, 0, 1000);
    TH1F * hMassmu = new TH1F("hMassmu", "hMassmu", 200, 0, 1000);
    TH1F * hMassel = new TH1F("hMassel", "hMassel", 200, 0 ,1000);
    TH1F * gf_hMassmu = new TH1F("GFhMassmu", "GFhMassmu", 200, 0, 1000);
    TH1F * gf_hMassel = new TH1F("GFhMassel", "GFhMassel", 200, 0 ,1000);

    */
    //createHistos("Eta", "Eta", 10, -3,3, EventsVBF, EventsGF, VBF, GF);
    createHistos("Mass", "HMass", 200, 0,1000, EventsVBF, EventsGF, VBF, GF, true);
    createHistos("Pt", "HPt", 200, 0,1000, EventsVBF, EventsGF, VBF,GF);
    createHistos("Eta", "HEta", 13, -6.5,6.5, EventsVBF, EventsGF, VBF, GF);
    createHistos("Phi", "HPhi", 7, -3.5,3.5, EventsVBF, EventsGF, VBF, GF);
    createHistos("zllMass", "ZllMass", 200, 0,200, EventsVBF, EventsGF, VBF, GF);
    createHistos("zjjMass", "ZjjMass", 200, 0,200, EventsVBF, EventsGF, VBF, GF);
    createHistos("zllPt", "ZllPt", 200, 0,200, EventsVBF, EventsGF, VBF, GF);
    createHistos("zjjPt", "ZjjPt", 200, 0,200, EventsVBF, EventsGF, VBF, GF);
    createHistos("zllEta", "ZllEta", 13, -6.5,6.5, EventsVBF, EventsGF, VBF, GF);
    createHistos("zjjEta", "ZjjEta", 13, -6-5,6.5, EventsVBF, EventsGF, VBF, GF);
    createHistos("zllPhi", "ZllPhi", 13, -6.5,6.5, EventsVBF, EventsGF, VBF, GF);
    createHistos("zjjPhi", "ZjjPhi", 13, -6-5,6.5, EventsVBF, EventsGF, VBF, GF);
    createHistos("Jet1CSVMVA", "Jet1CSVMVA", 100, -100,100, EventsVBF, EventsGF, VBF, GF);
    createHistos("Jet2CSVMVA", "Jet2CSVMVA", 100, -100,100, EventsVBF, EventsGF, VBF, GF);
    createHistos("Jet1JbProb", "Jet1JbProb", 100, -100,100, EventsVBF, EventsGF, VBF, GF);
    createHistos("Jet2JbProb", "Jet2JbProb", 100, -100,100, EventsVBF, EventsGF, VBF, GF);
    createHistos("jjdr", "jjdr", 100, -100,100, EventsVBF, EventsGF, VBF, GF);
    combHistos("met", "met", 100, -100,100, EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("mu", "LeptDau1Mass","LeptDau2Mass", "muMass", 100, 0, 100,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("mu", "LeptDau1Pt","LeptDau2Pt", "muPt", 100, 0, 100,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("mu", "LeptDau1Eta","LeptDau2Eta", "muEta", 100, -6., 6.,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("mu", "LeptDau1Phi","LeptDau2Phi", "muPhi", 100, -3., 3.,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("el", "LeptDau1Mass","LeptDau2Mass", "elMass", 100, 0, 100,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("el", "LeptDau1Pt","LeptDau2Pt", "elPt", 100, 0, 100,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("el", "LeptDau1Eta","LeptDau2Eta", "elEta", 100, -6., 6.,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("el", "LeptDau1Phi","LeptDau2Phi", "elPhi", 100, -3., 3.,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("mu", "JetDau1Mass","JetDau2Mass", "muChanJetMass", 100, 0, 100,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("mu", "JetDau1Pt","JetDau2Pt", "muChanJetPt", 100, 0, 100,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("mu", "JetDau1Eta","JetDau2Eta", "muChanJetEta", 100, -6., 6.,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("mu", "JetDau1Phi","JetDau2Phi", "muChanJetPhi", 100, -3., 3.,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("el", "JetDau1Mass","JetDau2Mass", "elChanJetMass", 100, 0, 100,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("el", "JetDau1Pt","JetDau2Pt", "elChanJetPt", 100, 0, 100,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("el", "JetDau1Eta","JetDau2Eta", "elChanJetEta", 100, -6., 6.,  EventsVBF, EventsGF, VBF, GF)->Write();
    singleChannel("el", "JetDau1Phi","JetDau2Phi", "elChanJetPhi", 100, -3., 3.,  EventsVBF, EventsGF, VBF, GF)->Write();


    //    makeHist(string variable, string title, int nBins, float min, float max, Events,1, output_file);

  }

  for(map<string,vector<double> >::const_iterator k = data.begin(); k != data.end(); ++k) {
    cout << k->first << ":";
    
    for(vector<double>::const_iterator j = k->second.begin(); j != k->second.end(); ++j) {
      cout << " " << *j;
    }
    cout << endl;
  }



 }
