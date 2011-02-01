#!/bin/csh

cd /afs/cern.ch/user/d/decosa/scratch0/Higgs/CMSSW_3_8_6/src/HiggsAnalysis/Higgs2l2b/test
eval `scramv1 runtime -csh`

bkgh2l2b


rfcp "TT.root" /castor/cern.ch/user/d/decosa/Higgs/TT/histos/TT.root
rfcp "ZZ.root" /castor/cern.ch/user/d/decosa/Higgs/ZZ/histos/ZZ.root
rfcp "WZ.root" /castor/cern.ch/user/d/decosa/Higgs/WZ/histos/WZ.root

