
### Run this script after  "source ~fabozzi/setdpm_host.csh cmsse02"

import os, commands

### Dirnames is the list of directories from which copying files
### indirnames is the list of directories to which copying files

#dirnames =  ['MuRun2012A']
#indirnames =  ['Run2012A_v3']

#dirnames =  [ 'DYJetsToLL_M-50']
#indirnames =  [ 'DYJetsToLL_M-50_v1']

#dirnames =  ['MuRun2012A', 'DYJetsToLL_M-50']
#indirnames =  ['Run2012A_v3', 'DYJetsToLL_M-50_v1']

#dirnames =  ['ElRun2012A']
#indirnames =  ['ElRun2012A_v3']

outpath = '/data3/scratch/users/decosa/Higgs/Summer12/'
#outpath = '/data3/scratch/users/decosa/Higgs/TestSummer12/'
ntpdir = '/edmntp22Jun12/'

#outpath = '/data3/scratch/users/decosa/Higgs/Fall11/'
#ntpdir = '/edmntp14May12EleID2012/'


#inputpath = "/store/group/local/DYJetsToLL_M-50/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/SkimPAT_H2l2q_523_v1_DYJetsToLL_M-50/b428990d57786df6bdb8c147bfaef542/"
#dirnames =  [ 'TT', 'WZ', 'ZZ']
#dirnames =  [ 'ZZ']

#dirnames =  ['ElRun2012A', 'ElRun2012B']
#dirnames =  ['DYJetsToLL_M-50',  'TT', 'WZ', 'ZZ', 'MuRun2012A',  'MuRun2012B']
#dirnames =  [  'ZZ', 'MuRun2012A',  'MuRun2012B', 'WZ']
#dirnames =  [ 'DYJetsToLL_M-50']

#dirnames =  ['ElRun2012A']

#dirnames =  ['ElRun2012A']
#dirnames =  ['GluGluToHToZZTo2L2Q_M-300', 'GluGluToHToZZTo2L2Q_M-200']
#dirnames =  ['GluGluToHToZZTo2L2Q_M-500']
dirnames = ['GluGluToHToZZTo2L2Q_M-200_8TeV', 'GluGluToHToZZTo2L2Q_M-300_8TeV', 'GluGluToHToZZTo2L2Q_M-525_8TeV', 'GluGluToHToZZTo2L2Q_M-600_8TeV', 'GluGluToHToZZTo2L2Q_M-700_8TeV', 'GluGluToHToZZTo2L2Q_M-800_8TeV', 'GluGluToHToZZTo2L2Q_M-900_8TeV']

for a in dirnames:

    

    ### Create the directory to store output and set permission, also remove files in that folder if already exists

    cmdLocalDisk = "mkdir "+ outpath 
    os.system(cmdLocalDisk)
    cmdLocalDisk = "mkdir "+ outpath + a 
    os.system(cmdLocalDisk)
    cmdLocalDisk = "mkdir "+ outpath + a +ntpdir
    os.system(cmdLocalDisk)   
    cmdPermission = "chmod 775 " + outpath + a +ntpdir
    os.system(cmdPermission)
    cmdClean = "rm "+ outpath + a +ntpdir + "*"
    os.system(cmdClean)
    #    print cmdLocalDisk
    #    print cmdPermission
    #    print  cmdClean

    ### Look at the original folder and identify a list of root files
    
    # cmd = "rfdir /dpm/na.infn.it/home/cms/store/user/decosa/" +indirnames[dirnames.index(a)]

    f = open(a+".list", "r")
    files = f.readlines()
 
    #cmd = "mkdir " + a
    #os.system(cmd)
    #    list = ls_la.split(os.linesep)

    ### Take every file in the original folder and copy it to the output folder

   # print files
    for c in files:
        
   
        #print c
        #if (c.startswith('h2l2q_ntuple') and c.endswith('.root')):
        if ('h2l2q_ntuple' in c ):
            c = c.rstrip("\n")
            b = c.split("/")
            for k in b:
                if k.startswith("h2l2q_ntuple"): filename = k 
            
            
            #print c
            cmd =  "lcg-cp -D srmv2 srm://srm.ciemat.es:8443"+ c + " " +outpath + a + ntpdir + k
            print cmd
            os.system(cmd)
            #files.append(c)


                
    #print files
                   



