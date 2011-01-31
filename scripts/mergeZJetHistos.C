
void mergeZJetHistos(){
  
  string bkg[]={"Z0Jet", "Z1Jet","Z2Jet","Z3Jet","Z4Jet","Z5Jet", "Z1Jet100_300","Z2Jet100_300","Z3Jet100_300","Z4Jet100_300","Z5Jet100_300", "Z1Jet300_800","Z2Jet300_800","Z3Jet300_800","Z4Jet300_800","Z5Jet300_800","Z1Jet800_1600","Z2Jet800_1600","Z3Jet800_1600","Z4Jet800_1600","Z5Jet800_1600", "ZCC0", "ZCC1", "ZCC2", "ZCC3", "ZBB0", "ZBB1","ZBB2","ZBB3"};

  
  string weights[]={"1.755,","1.523,","1.,","1.,","0.104,","0.132,","0.042,","0.0839,","0.0911,","0.0372,","0.057,","0.00085,","0.00134,","0.00195,","0.0046,","0.002217,","0.000005,","0.00003,","0.00003,","0.00002,","0.000008,","0.0049,","0.0066,","0.0433,","0.0205,","0.0062,","0.0060,","0.0426,","0.0186"};

  const unsigned int nFiles = sizeof(bkg)/sizeof(string);
  string h1 = "Zjets.root";

  string mergeHistos = "mergeTFileServiceHistograms -o "+h1+" -i ";
  string w = " -w ";
  for(int i=0;i<nFiles;++i){

    mergeHistos += bkg[i]+".root";
    mergeHistos += " ";
    w += weights[i];

    //cout<<"merge "<<mergeHistos<<endl;
  }
  mergeHistos += w;
  cout<<"merge "<<mergeHistos<<endl;
  system(mergeHistos.c_str());

}
