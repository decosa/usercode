
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

TFile * h_file = new TFile("h350.root","read");
TH1D * h = (TH1D*) h_file->Get("HMassdrjjSel");
 for(int i=0; i<h->GetNbinsY();++i){
   h->SetBinError(i,0);
     }

TFile * tt_file = new TFile("TT.root","read");
TH1D * tt = (TH1D*) tt_file->Get("HMassdrjjSelmu");


TFile * zz_file = new TFile("ZZ.root","read");
TH1D * zz = (TH1D*) tt_file->Get("HMassdrjjSelmu");

TFile * wz_file = new TFile("WZ.root","read");
TH1D * wz = (TH1D*) tt_file->Get("HMassdrjjSelmu");


 string bkg[]={"Z1Jet","Z2Jet","Z3Jet","Z4Jet","Z5Jet",};
 TH1D * zjet = new TH1D("HMassdrjj", "M_{H} after cut on #Delta r_{jj}", 20,200,600);

 for(int i=0;i<2;++i){
   TFile * f = new TFile((bkg[i]+".root").c_str(),"read");
   TH1D * b = (TH1D*) f->Get("HMassdrjjSelmu");
   zjet->SetBins(b->GetNbinsX(), b->GetXaxis()->GetXmin(),b->GetXaxis()->GetXmax() );

   zjet->Add(b);
}


TH1D * S0 = new TH1D("S0","H mass",20,200,600);
S0->SetStats(kFALSE);
S0->SetXTitle("m_{H} (GeV/c^{2})");
S0->SetYTitle("Events/5 GeV/c^{2}");
 S0->SetMinimum(0.5);
 S0->GetYaxis()->SetRangeUser(0,0.4);
S0->GetXaxis()->SetTitleSize(0.045);
S0->GetXaxis()->SetTitleOffset(0.95);
S0->GetXaxis()->SetLabelSize(0.045);
S0->GetYaxis()->SetTitleOffset(0.9);
S0->GetYaxis()->SetLabelSize(0.045);
S0->GetYaxis()->SetTitleSize(0.05);

 TH1D * S1 = new TH1D(*tt);
 S1->SetLineColor(kBlue);
 TH1D * S12 = new TH1D(* S1); S12->Add(zz);
 S12->SetLineColor(kGreen);
 TH1D * S123 = new TH1D(* S1); S123->Add(wz);
 S123->SetLineColor(kYellow);
 TH1D * S1234 = new TH1D(* S1); S1234->Add(zjet);
 S1234->SetLineColor(kViolet);
 TH1D * S12345 = new TH1D(* S1); S12345->Add(h);
 S12345->SetLineColor(kMagenta);
//TH1D * S12345 = new TH1D(* S1234); S12345->Add(wwToMuMu_draw);
//S12345->SetLineColor(kMagenta);
//TH1D * S12345 = new TH1D(* S1); S12345->Add(zToMuMu);
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



// S12345->SetMarkerStyle(0);

 S0->Draw("HIST");
// S12345->Draw("HSAME");
 
 S12345->Draw("HISTSAME");
 S1234->Draw("HISTSAME");
 S123->Draw("HISTSAME");
 S12->Draw("HISTSAME");
 S1->Draw("HISTSAME");


 leg = new TLegend(.75,.75,1.0,1.0);
 leg->SetFillColor(0);
 leg->AddEntry(S1,"t #bar{t}","f");
 leg->AddEntry(S12,"ZZ","f");
 leg->AddEntry(S123,"WZ ","f");
 leg->AddEntry(S1234,"Zjets","f");
 leg->AddEntry(S12345,"H350","f");


//leg->AddEntry(S12345,"WW inclusive","f");
//leg->AddEntry(S12345,"Z->#mu #mu","f");


 leg->Draw("SAME");
 S1->SetFillColor(kTeal+5);
 S1->SetMarkerColor(kTeal+3);
 S12->SetFillColor(kMagenta+3);
 S12->SetMarkerColor(kMagenta+4);
 S123->SetFillColor(kViolet+4);
 S123->SetMarkerColor(kViolet+3);
 S1234->SetFillColor(kOrange-2);
 S1234->SetMarkerColor(kOrange+8);
 S12345->SetFillColor(kPink-3);
 S12345->SetMarkerColor(kPink-7);


//S12345->SetFillColor(kMagenta);
//S12345->SetFillColor(kRed);
//c1->SetLogy();
 c1->SetTickx(0);
 c1->SetTicky(0);

//c1->SaveAs("zmumu_sel.eps");



}
