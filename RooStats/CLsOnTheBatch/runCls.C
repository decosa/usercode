{
  gROOT->ProcessLine(".L RunCLS.C");
  gROOT->ProcessLine(".L PLC.C");
  gROOT->ProcessLine("RunCLs(\"comb_hgg.root\")");
  //gROOT->ProcessLine("PLC(\"comb_hgg.root\")");
  gROOT->ProcessLine(".q");
  gApplication->Terminate();
}
