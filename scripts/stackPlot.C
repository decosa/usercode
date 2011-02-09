{
gROOT->Reset();
gROOT->SetStyle("Plain");
//Z->mu mu

//double w_zmumu = 10.0/247.16;
//double w_wmunu = 10.0/18.966;
//double w_ztautau = 10.0/129.63;
//double w_ppmux = 10.0/7.9278;

//double w_ttbar = 10.0/321.0;

// Z->mumu sample

 TCanvas c1;
 // TH1F * h = new TH1F("h", "M_{H} after cut on #Delta r_{jj}", 200,0,1000);
 TFile * h_file = TFile::Open("h350.root", "READ");
 TH1 * h_original = (TH1*) h_file->Get("HMassdrjjSel");
 TH1 * h = h_original->Clone("h");
 h->Rebin(5); 
 h->Draw();


 TH1F * tt = new TH1F("tt", "M_{H} after cut on #Delta r_{jj}", 200,0,1000);
 TFile * tt_file = new TFile("TT.root");
 TH1 * tt_original = (TH1*) tt_file->Get("HMassdrjjSelmu");
 tt->Add(tt_original);
 tt->Rebin(5);
 

 TH1F * zz = new TH1F("zz", "M_{H} after cut on #Delta r_{jj}", 200,0,1000);
 TFile * zz_file = new TFile("ZZ.root");
 TH1 * zz_original = (TH1*)zz_file->Get("HMassdrjjSelmu");
 cout<<"n bins zz pre rebin"<<zz->GetNbinsX()<<endl;
 zz->Add(zz_original);
 zz->Rebin(5);
 cout<<"n bins zz post rebin"<<zz->GetNbinsX()<<endl;

 TH1F * wz = new TH1F("wz", "M_{H} after cut on #Delta r_{jj}", 200,0,1000);
 TFile * wz_file = new TFile("WZ.root");
 TH1 * wz_original = (TH1*) wz_file->Get("HMassdrjjSelmu");
 wz->Add(wz_original);
 wz->Rebin(5);


 TH1F * zjet = new TH1F("HMassdrjj", "M_{H} after cut on #Delta r_{jj}", 200,0,1000);

 // string bkg[24]; 
 //string bkg[] ={"Z0Jet","Z1Jet","Z2Jet","Z3Jet","Z4Jet","Z5Jet","Z1Jet100_300","Z2Jet100_300","Z3Jet100_300","Z1Jet300_800","Z2Jet300_800","Z3Jet300_800","Z4Jet300_800","Z5Jet300_800","ZBB0","ZBB1", "ZBB2", "ZBB3","ZCC0", "ZCC2", "ZCC3"};

 string bkg[] ={"Z0Jet","Z1Jet","Z2Jet","Z3Jet","Z4Jet","Z5Jet","Z1Jet100_300","Z2Jet100_300","Z3Jet100_300","Z4Jet100_300","Z5Jet100_300","Z1Jet300_800","Z2Jet300_800","Z3Jet300_800","Z4Jet300_800","Z5Jet300_800","ZBB0","ZBB1", "ZBB2", "ZBB3","ZCC0", "ZCC2", "ZCC3"};


 
 const unsigned int nFiles = sizeof(bkg)/sizeof(string);
 TFile * files[nFiles];
 cout<<"array size "<<nFiles<<endl;
 for(int i=0;i<nFiles;++i){
   files[i] = TFile::Open((bkg[i]+".root").c_str(), "READ");
   TH1 * b = (TH1*) files[i]->Get("HMassdrjjSelmu");
   //cout<<"file: "<< bkg[i]+".root"<<endl;
   zjet->Add(b);
   //cout<<"t: "<<zjet->Integral(0,1000)<<endl;
}
 


 zjet->Rebin(5);
 zjet->Draw("HIST");


 TH1F * S0 = new TH1F("S0","H mass",200,0,1000); 
 S0->Rebin(5);
 S0->SetStats(kFALSE);
 S0->SetXTitle("m_{H} (GeV/c^{2})");
 S0->SetYTitle("Events/5 GeV/c^{2}");
 //S0->SetMinimum(0.5);
 S0->GetYaxis()->SetRangeUser(0,1.);
 S0->GetXaxis()->SetTitleSize(0.045);
 S0->GetXaxis()->SetTitleOffset(0.95);
 S0->GetXaxis()->SetLabelSize(0.045);
 S0->GetYaxis()->SetTitleOffset(0.9);
 S0->GetYaxis()->SetLabelSize(0.045);
 S0->GetYaxis()->SetTitleSize(0.05);

  cout<<"n bins zz "<<zz->GetNbinsX()<<endl;
  //S1->SetBins(20, 200,600 );

  

  cout<<"n bins zjet "<<zjet->GetNbinsX()<<endl;




 // zz->Draw();
 TH1F * S1 = new TH1F(*wz);
 TH1F * S12 = new TH1F(* S1);
 S12->Add(zz);
 TH1F * S123 = new TH1F(* S12); 
 S123->Add(tt);
 TH1F * S1234 = new TH1F(* S123); 
 S1234->Add(zjet);
 TH1F * S12345 = new TH1F(* S1234);
 S12345->Add(h);


//TH1D * S12345 = new TH1D(* S1234); S12345->Add(wwToMuMu_draw);
//S12345->SetLineColor(kMagenta);
//TH1D * S12345 = new TH1Dnnnn(* S1); S12345->Add(zToMuMu);
//S12345->SetLineColor(kRed);

//S12345->SetStats(kFALSE);

 S12345->SetStats(kFALSE);
 S1234->SetStats(kFALSE);
 S123->SetStats(kFALSE);
 S12->SetStats(kFALSE);
 S1->SetStats(kFALSE);

//S12345->SetTitle("CMS preliminary, L = 10 pb^{-1}");
 S12345->SetTitle("H mass");
 S1234->SetTitle("H mass");
 S123->SetTitle("H mass");
 S12->SetTitle("H mass");
 S1->SetTitle("H mass");
 

// S12345->SetXTitle("m_{#mu #mu} (GeV/c^{2})");
 
 S12345->SetXTitle("m_{H} (GeV/c^{2})");
 S1234->SetXTitle("m_{H} (GeV/c^{2})");
 S123->SetXTitle("m_{H} (GeV/c^{2})");
 S12->SetXTitle("m_{H} (GeV/c^{2})");
 S1->SetXTitle("m_{H} (GeV/c^{2})");


 
// S12345->SetYTitle("Events/1 GeV/c^{2}");
 
 S12345->SetYTitle("Events/5 GeV/c^{2}");
 S1234->SetYTitle("Events/5 GeV/c^{2}");
 S123->SetYTitle("Events/5 GeV/c^{2}");
 S12->SetYTitle("Events/5 GeV/c^{2}");
 S1->SetYTitle("Events/5 GeV/c^{2}");
 S0->SetMarkerStyle(0);
 S1->SetMarkerStyle(0);
 S12->SetMarkerStyle(0);
 S123->SetMarkerStyle(0);
 S1234->SetMarkerStyle(0);
 S12345->SetMarkerStyle(0);



 S12345->SetMarkerStyle(0);

 S0->Draw("HIST");
 
 
 //S12345->Draw("HISTSAME");
 S1234->Draw("HISTSAME");
 S123->Draw("HISTSAME");
 S12->Draw("HISTSAME");
 S1->Draw("HISTSAME");
 h->SetLineColor(kBlack);
 h->SetFillColor(0);
 h->SetLineWidth(2);
 h->Draw("HISTSAME");

 leg = new TLegend(.75,.75,1.0,1.0);
 leg->SetFillColor(0);
 leg->AddEntry(S1,"WZ","f");
 leg->AddEntry(S12,"ZZ","f");
 leg->AddEntry(S123,"t #bar{t}","f");
 leg->AddEntry(S1234,"ZJets ","f");
 // leg->AddEntry(S12345,"H350","f");
 leg->AddEntry(h,"H350","l");


//leg->AddEntry(S12345,"WW inclusive","f");
//leg->AddEntry(S12345,"Z->#mu #mu","f");


 leg->Draw("SAME");
 S1->SetFillColor(kTeal+5);
 S1->SetLineColor(kTeal+3);
 S12->SetFillColor(kMagenta+3);
 S12->SetLineColor(kMagenta+4);
 S123->SetFillColor(kViolet+4);
 S123->SetLineColor(kViolet+3);
 S1234->SetFillColor(kOrange-2);
 S1234->SetLineColor(kOrange+8);
 S12345->SetFillColor(kPink-3);
 S12345->SetLineColor(kPink-7);


//S12345->SetFillColor(kMagenta);
//S12345->SetFillColor(kRed);
//c1->SetLogy();
 c1->SetTickx(0);
 c1->SetTicky(0);

//c1->SaveAs("zmumu_sel.eps");
//  zz_file->Close();
//  tt_file->Close();
//  wz_file->Close();
//  h_file->Close();
//  for(int i=0;i<nFiles;++i) files[i]->Close();

}
