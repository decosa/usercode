{
  TChain chain("Events"); // create the chain with tree "T"
  gStyle->SetOptStat();
  gROOT->SetStyle("Plain");
  chain.Add("NtupleLooseTestNew_oneshot_all_132605.root"); // add the files
  chain.Add("NtupleLooseTestNew_oneshot_all_132653.root");
  chain.Add("NtupleLooseTestNew_oneshot_all_132654.root");
  chain.Add("NtupleLooseTestNew_oneshot_all_132658.root");
  chain.Add("NtupleLooseTestNew_oneshot_all_132656.root");
  chain.Add("NtupleLooseTestNew_oneshot_all_132661.root");
  chain.Add("NtupleLooseTestNew_oneshot_all_132662.root");
  chain.Add("NtupleLooseTestNew_oneshot_all_132716.root");
  TFile out("histo.root", "RECREATE");
  std::string value = std::string("zMuTrk");
  int min_ = 0;
  int max_ = 100;
  int nBins = 100;

  TCanvas *c = new TCanvas((value).c_str(),(value).c_str());

  TH1F * histo = new TH1F((value + "Mass").c_str(),(value + "Mass").c_str(), nBins, min_, max_);
  TH1F * histo2 = new TH1F((value + "Dau1Pt").c_str(),(value + "Dau1Pt").c_str(), nBins, min_, max_);
  TH1F * histo3 = new TH1F((value + "Dau2Pt").c_str(),(value + "Dau2Pt").c_str(), nBins, min_, max_);
  histo->SetLineColor(kBlue);
  histo2->SetLineColor(kBlue);
  histo3->SetLineColor(kBlue);
  chain->Project((value + "Mass").c_str(), (value + "Mass").c_str(), "zMuTrkDau1Pt>5 && zMuTrkDau2Pt>5");
  chain->Project((value + "Dau1Pt").c_str(), (value + "Dau1Pt").c_str(), "zMuTrkDau1Pt>5 && zMuTrkDau2Pt>5");
  chain->Project((value + "Dau2Pt").c_str(), (value + "Dau2Pt").c_str(), "zMuTrkDau1Pt>5 && zMuTrkDau2Pt>5");

  histo->Draw();
  c->SaveAs("zMuTrkMass.pdf");
  histo2->Draw();
  c->SaveAs("zMuTrkDau1Pt.pdf");
  histo3->Draw();
  c->SaveAs("zMuTrkDau2Pt.pdf");
  //  c->Write();
  delete c;
  out.Close();
}
