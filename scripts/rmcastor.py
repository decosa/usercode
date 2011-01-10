import os, commands
import string


def remove(directory):
    
    mass = ['300','400']
    print "mass values: "
    print mass
    for a in mass:
        castor_path = "/castor/cern.ch/user/d/decosa/Higgs/h"+ a + "/" + directory + "/"
        cmd = "rfdir"+" "+castor_path
        status,ls_la = commands.getstatusoutput( cmd )
        if status: raise RFIOError('Directory %s not found' % dirname)
        dir = [ ]
        list = ls_la.split(os.linesep)

        for d in list:
            dd = d.split()
            for ddd in dd:
                if ddd.endswith('.root'):dir.append( ddd )

        for filename in dir:
            if "GF"  in filename:
                os.system('rfrm '+castor_path+filename)
            if "VBF"  in filename: 
                os.system('rfrm '+castor_path+filename)
        



### uncomment the following lines to make empty histos and edmntp dir on castor

                
#remove("histos")
#remove("edmntp")
