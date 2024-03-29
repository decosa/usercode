
### This scripts provides datacards to run a limit. It takes in input txt reports files produced by plot.C mac

import os, commands


def makeDatacards(category):


    filename = "lljjmass"+category+".txt"
    if(category=="2btag"):
        filename = "lljjmass.txt"
    name = "_"+category+"_datacard.txt"

#    m = [ "250"]
    m = [ "250", "300", "350","400", "450", "500"]

    for mass in m:
        file = open(mass+filename, "r")
        newfile = open(mass+name, "w")
        muChannel = False
        elChannel = False
        mubkg = 0
        musig = 0
        muobs = 0
        elbkg = 0
        elsig = 0
        elobs = 0
        muChanBin = "mm"+category
        elChanBin = "ee"+category
        #kmax 0 number of nuisance parameters (sources of systematical uncertainties) "
        newfile.write('imax 2  number of channels\njmax 1  number of backgrounds\nkmax 1  number of nuisance parameters \n')
        newfile.write("------------\n")
        newfile.write("bin            "+muChanBin+"   "+elChanBin+"\n")
        
        while 1:
            line = file.readline()
            if line =="":
                break;
            if (line.startswith("Muon Channel")):
                muChannel=True
            if (line.startswith("Electron Channel")):
                muChannel=False
                elChannel = True
            if (line.startswith("Total yields")):
                muChannel = False
                elChannel = False
            if (line.startswith("AllBkg")):
                splitLine = line.split()
                if (muChannel==True):
                    mubkg = splitLine[1]
                if (elChannel==True):
                    elbkg = splitLine[1]
            if (line.startswith(mass)):
                splitLine = line.split()
                if (muChannel==True):
                    musig = splitLine[1]
                if (elChannel==True):
                    elsig = splitLine[1]
            if (line.startswith("data")):
                splitLine = line.split()
                if (muChannel==True):
                    muobs = splitLine[1]
                if (elChannel==True):
                    elobs = splitLine[1]
                                                
                                                                            
        newfile.write("observation     "+str(muobs)+"   "+ str(elobs)+"\n")
        newfile.write("------------\n")
        newfile.write("bin            "+muChanBin+"   "+muChanBin+"   "+elChanBin+"   "+elChanBin+"\nprocess        sig    bg    sig   bg\nprocess         0      1     0     1\n")
        newfile.write("rate          "+str(musig)+"  "+str(mubkg)+"  "+str(elsig)+"  "+str(elbkg)+"  "+"\n")
        newfile.write("------------\n")
        newfile.write("lumi  lnN     1.045    1.045   1.045    1.045  \n")

category = ["0btag","1btag", "2btag"]


for c in category:
     makeDatacards(c)

mass = ['250']
for m in mass:
    cmd = "combineCards.py "
    for c in category:
        cmd += m+ "_"+c+"_datacard.txt "
    cmd += " > "+m+"_datacard.txt"
    os.system(cmd)
#    if (line.startswith("")): elChannel=True


    #newline = string.replace(line, "/Freq_CLs_grid_ts3_comb_hgg.root", "/Freq_CLs_grid_ts3_comb_hgg_"+str(n)+".root")
    #newfile.write(newline)
    
 #   cmd = "chmod 775 "+ filename+"_"+str(n)+ext
  #  os.system(cmd)
  #  cmd = "bsub -q 8nh "+ filename+"_"+str(n)+ext
    #print cmd
   # os.system(cmd)
    
    #cmd = "bjobs"
   # os.system(cmd)
                                                                            
