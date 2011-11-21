

void RunCLs(const char * fileName, int npoints = 4, double rmin = 3, double rmax = 6, int type = 0, int ts = 3) { 

   gROOT->ProcessLine(".L $ROOTSYS/tutorials/roostats/StandardHypoTestInvDemo.C+");
   //gROOT->ProcessLine(".L ../StandardHypoTestInvDemo.C+");


   bool useNC = true;   // use number counting
   // int ntoys = 20000;   // number of toys
   int ntoys = 100;   // number of toys
   nworkers = 8;       
   useProof = true;    // use Proof
   writeResult = true; 
   optimize = false;
   rebuild=false;      // rebuild toys for bands and expected limits
   nToyToRebuild = 20;
   nToysRatio = 5;
   

   StandardHypoTestInvDemo(fileName,"w","ModelConfig","ModelConfig_bonly","data_obs",type,ts,true,
                           npoints,rmin,rmax,ntoys,useNC,"nuisancePdf");

}

