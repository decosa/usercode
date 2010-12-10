#include "TROOT.h"
#include "TChain.h"

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
#include<boost/tokenizer.hpp>

using namespace std;
//using namespace boost;






int main() {


  typedef boost::tokenizer<boost::char_separator<char> > tokenizer;
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
    tokenizer tok(s);
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
  TChain Events("Events"); 
  
  Events.Add("H300VBFEdmNtuples.root", 65);
  
  int zMassCut = Events.GetEntries("muHiggsLeptDau1Pt>20 && muHiggsLeptDau2Pt>20  && abs(muHiggsLeptDau1dB)<0.02 && abs(muHiggsLeptDau2dB)<0.02 && (muHiggsLeptDau1Eta < 2.1 || muHiggsLeptDau2Eta < 2.1) && muHiggsJetDau1Pt>30 && muHiggsJetDau2Pt>30 && abs(muHiggszllMass - 91)< 10 && abs(muHiggszjjMass - 91)< 15");
  
  //  int nMassCut = zMassCut/data["VBFevents"][1]*data["VBFxsec"][0];
  
  cout<<"Number of higgs candidate (zMass cut): "<<nMassCut<<endl;


  for(map<string,vector<double> >::const_iterator k = data.begin(); k != data.end(); ++k) {
    cout << k->first << ":";
    
    for(vector<double>::const_iterator j = k->second.begin(); j != k->second.end(); ++j) {
      cout << " " << *j;
    }
    cout << endl;
  }

  // 

  // Events.Add("H300VBFEdmNtuples.root", 65);

  // int zMassCut = Events.GetEntries("muHiggsLeptDau1Pt>20 && muHiggsLeptDau2Pt>20  && abs(muHiggsLeptDau1dB)<0.02 && abs(muHiggsLeptDau2dB)<0.02 && (muHiggsLeptDau1Eta < 2.1 || muHiggsLeptDau2Eta < 2.1) && muHiggsJetDau1Pt>30 && muHiggsJetDau2Pt>30 && abs(muHiggszllMass - 91)< 10 && abs(muHiggszjjMass - 91)< 15");

  // cout<<"Number of higgs candidate (zMass cut): "<<zMassCut<<endl;

  // cout<<"prova"<<endl;

 
//  for (int y = 0 ; y < j-1 ; y++){
   
//    cout << strings[y] << endl;
//  } 


 }
