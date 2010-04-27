#!/bin/csh 

#echo "$i" 
set j = 1

while($j<20)
  echo" **** start copy ****"
  echo "$j"
 #echo "lcg-cp --verbose --vo cms --defaultsetype srmv2 srm://t2-srm-02.lnl.infn.it:8443/srm/managerv2'?'SFN=/pnfs/lnl.infn.it/data/cms/store/user/degrutto/Zmumu/testEWK_ZMuMuSubSkim_zmm/aa58da5e00dd1bb3b2b306ca5f4fd9de/testZMuMuSubSkim_$j.root srm://cmsse01.na.infn.it:8446/srm/managerv2'?'SFN=/dpm/na.infn.it/home/cms/store/user/degrutto/EWK_ZMM_OCT_EX/zmm/testZMuMuSubSkim_$j.root" 

rfcp /tmp/decosa/NtupleLooseTestNew_oneshot_all_33X_$j'_1'.root /castor/cern.ch/user/d/decosa/MC_33X/

# lcg-cp --verbose --vo cms --defaultsetype srmv2 srm://t2-srm-02.lnl.infn.it:8443/srm/managerv2'?'SFN=/pnfs/lnl.infn.it/data/cms/store/user/decosa/2010//35X_MC/NtupleLooseTestNew_oneshot_all_Test_$j'_1'.root /tmp/decosa/NtupleLooseTestNew_oneshot_all_35X_$j'_1'.root
 
  set j = `expr $j + 1`

end


echo" **** end copy ****"

