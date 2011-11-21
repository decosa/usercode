// merge  the HTI results 
#include <sstream>

gSystem->Load("libRooStats");
using namespace RooStats;

void merge_CLs(const char * filename) {
  int n =10;
  for (int i=0;i<n;++i){

    std::string s;
    std::stringstream out;
    out << i;
    s = out.str();
    const char* postfix = ".root";
    string file1 = string(filename) +string("_0")+string(postfix); 
    TFile f1(file1.c_str());
    HypoTestInverterResult * r1 = f1.Get("result_r");

    string file2 = string(filename) + string("_")+s + string(postfix);
    //    const char* file2 = (filename + str(n)+".root").c_str();
    //    cout<<"file1: "<<file1<<endl;    
    TFile f2(file2.c_str());
    HypoTestInverterResult * r2 = f2.Get("result_r");
    
    // do the merge 
    
    r1->Add(*r2);
    new TCanvas();
    HypoTestInverterPlot * pl2 = new HypoTestInverterPlot("rcomb","combined result",r1);
    pl2->Draw("2CL");
  }
}
