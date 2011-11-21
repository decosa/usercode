import os, commands
import string


toys = 50

filename = "cls"
ext = ".csh"


for n in range(0, toys):
    
    file = open(filename+ext, "r")
    newfile = open(filename+"_"+str(n)+ext, "w")
    print str(n)        
    while 1:
        line = file.readline()
        if line =="":
            break;
        newline = string.replace(line, "/Freq_CLs_grid_ts3_comb_hgg.root", "/Freq_CLs_grid_ts3_comb_hgg_"+str(n)+".root")
        newfile.write(newline)
                        
    cmd = "chmod 775 "+ filename+"_"+str(n)+ext
    os.system(cmd)
    cmd = "bsub -q 8nh "+ filename+"_"+str(n)+ext
    #print cmd
    os.system(cmd)

cmd = "bjobs"
os.system(cmd)
