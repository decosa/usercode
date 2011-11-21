
#!/bin/csh                                                                                                                                                  

cd /afs/cern.ch/user/d/decosa/rootTest

bash

source /afs/cern.ch/user/d/decosa/rootTest/setroot.sh

#source /afs/cern.ch/sw/lcg/external/gcc/4.3.2/x86_64-slc5/setup.sh
#export ROOTSYS=/afs/cern.ch/sw/lcg/app/releases/ROOT/5.30.02/x86_64-slc5-gcc43-opt/root
#export PATH=$ROOTSYS/bin:$PATH
#export LD_LIBRARY_PATH=$ROOTSYS/lib:$LD_LIBRARY_PATH


root -l runCls.C                                                                                                                                           

gcc --version

rfcp Freq_CLs_grid_ts3_comb_hgg.root /castor/cern.ch/user/d/decosa/RooStats/Freq_CLs_grid_ts3_comb_hgg.root
#mv  Freq_CLs_grid_ts3_comb_hgg.root /tmp/decosa/CLs/Freq_CLs_grid_ts3_comb_hgg.root

