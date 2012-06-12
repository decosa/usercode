
### Run this script to compute Asymptotic limit for 2l2q channel on mass points listed in masses2l2q.txt 
### Change CM to move from 7Tev to 8 TeV scenario, or put 0 to consider 7+8



FILE=masses2l2q.txt 
CM=7

### combine datacards
for M in $(cat $FILE ) ; do ./make_combined_card.py $M -d hzz -s 2l2q -e $CM ; done
### combine workspaces
for M in $(cat $FILE ) ; do ./make_binary_workspaces.sh $M comb7_hzz.txt; done

### compute limits, blind expected with --BE 
### observed put -O instead of --BE and remove set rMax = 1 in make_ASLCLS before running the observed limit 
for M in $(cat $FILE ) ; do ./make_ASCLS.sh --BE $M comb7_hzz.root; done

mkdir results
### put together the results in a unique file in results/folder 
./harvest.sh  ASCLS comb7_hzz


#for M in $(cat $FILE ) ; do ./make_ASCLS.sh -O $M comb7_hzz2l2q.root; done


