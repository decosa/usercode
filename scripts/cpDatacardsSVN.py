import os, commands

f = open("masseshzz2l2q.list", "r")
masses = f.readlines()
masses = [c.rstrip("\n") for c in masses]      

for a in masses:

    cmd = "cp ~mmozer/public/7TeVCards/datacards_HR11_v2_fitMC/"+str(a)+"/* "+str(a)+"/"
    #    os.system(cmd)

    #    00/hzz2l2q_ee0b_7TeV.txt  200/hzz2l2q_ee1b_7TeV.txt  200/hzz2l2q_ee2b_7TeV.txt  200/hzz2l2q_mm0b_7TeV.txt  200/hzz2l2q_mm1b_7TeV.txt  200/hzz2l2q_mm2b_7TeV.txt

    cmd = "svn add "+a+"/hzz2l2q_ee0b_7TeV.txt"
    os.system(cmd)
    cmd = "svn add "+a+"/hzz2l2q_ee1b_7TeV.txt"
    os.system(cmd)
    cmd = "svn add "+a+"/hzz2l2q_ee2b_7TeV.txt"
    os.system(cmd)
    cmd = "svn add "+a+"/hzz2l2q_mm0b_7TeV.txt"
    os.system(cmd)
    cmd = "svn add "+a+"/hzz2l2q_mm1b_7TeV.txt"
    os.system(cmd)
    cmd = "svn add "+a+"/hzz2l2q_mm2b_7TeV.txt"
    os.system(cmd)



    cmd = "svn add "+a+"/hzz2l2q_ee0b_7TeV.input.root"
    os.system(cmd)
    cmd = "svn add "+a+"/hzz2l2q_ee1b_7TeV.input.root"
    os.system(cmd)
    cmd = "svn add "+a+"/hzz2l2q_ee2b_7TeV.input.root"
    os.system(cmd)
    cmd = "svn add "+a+"/hzz2l2q_mm0b_7TeV.input.root"
    os.system(cmd)
    cmd = "svn add "+a+"/hzz2l2q_mm1b_7TeV.input.root"
    os.system(cmd)
    cmd = "svn add "+a+"/hzz2l2q_mm2b_7TeV.input.root"
    os.system(cmd)
