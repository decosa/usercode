import os, commands
import string

mass = ['350']
lumiNorm = [0.00115,0.00034]

print "mass values: "
print mass
for a in mass:

    ### creation of python config file for GF and VBF samples
    
    cfgfilename = "higgs2l2bAnalysis.py"    
    file = open(cfgfilename, "r")
    newfileGF = open(a+"GF"+cfgfilename, "w")
    newfileVBF = open(a+"VBF"+cfgfilename, "w")
    ### need to know which are skim file names
    castor_path = "/castor/cern.ch/user/d/decosa/Higgs/h"+ a + "/skim/"

    cmd = "rfdir"+" "+castor_path
    status,ls_la = commands.getstatusoutput( cmd )
    if status: raise RFIOError('Directory %s not found' % dirname)
    dir = [ ]
    list = ls_la.split(os.linesep)

    for d in list:
        dd = d.split()
        for ddd in dd:
            if ddd.endswith('.root'):dir.append( ddd )

    GF=[]
    VBF=[]
    for filename in dir:
        if "GF"  in filename: GF.append('rfio:'+castor_path+filename )
        if "VBF"  in filename: VBF.append('rfio:'+castor_path+filename )


    gf2 = '\' , \''.join(GF)

    vbf2 = '\' , \''.join(VBF)

    while 1:
        riga = file.readline()
        if riga =="":
            break;
        rigaGF = string.replace(riga, "300GF", a+"GF")
        rigaVBF = string.replace(riga, "300GF", a+"VBF")
        if riga.startswith("process.source.fileNames=cms.untracked.vstring('file:filename.root')"):
            rigaGF = string.replace(rigaGF, 'file:filename.root', gf2 );
            rigaVBF = string.replace(rigaVBF, 'file:filename.root', vbf2 );
        if riga.startswith("    lumiNormalization"):
            rigaGF = string.replace(rigaGF,'0.00115', str(lumiNorm[0]) );
            print rigaGF
            rigaVBF = string.replace(rigaVBF,'0.00115', str(lumiNorm[1]) );
            print rigaVBF
        if riga.startswith("    output_name"):
            rigaGF = string.replace(rigaGF,'\"h350GF\"','\"h'+a+'GF\"' );
            rigaVBF = string.replace(rigaVBF,'\"h350GF\"','\"h'+a+'VBF\"' );
        newfileGF.write(rigaGF)
        newfileVBF.write(rigaVBF)

        
    file.close()
    newfileGF.close()
    newfileVBF.close()
        
    ### Create scripts for every value of mass and for GF and VBF to run analysis in batch queue 
        
    scriptname = "jobtest.csh"    
    script = open(scriptname, "r")
    newscriptGF = open(a+"GF"+scriptname, "w")
    newscriptVBF = open(a+"VBF"+scriptname, "w")
    ### need to know which are skim file names
    castor_path = "/castor/cern.ch/user/d/decosa/Higgs/h"+ a + "/skim/"

    while 1:
        riga = script.readline()
        if riga =="":
            break;
        rigaGF = string.replace(riga, "300GF", a + "GF")
        rigaGF = string.replace(rigaGF, "300", a)
        rigaVBF = string.replace(riga, "300GF", a+"VBF")
        rigaVBF = string.replace(rigaVBF, "300", a)
        rigaVBF = string.replace(rigaVBF, "GF", "VBF")
        print rigaVBF
        print rigaGF
        if riga.startswith("cmsRun "):
            rigaGF = string.replace(rigaGF, cfgfilename, a+"GF"+ cfgfilename );
            rigaVBF = string.replace(rigaVBF, cfgfilename, a+"VBF"+ cfgfilename );
            print  rigaGF
            print  rigaVBF


        newscriptGF.write(rigaGF)
        newscriptVBF.write(rigaVBF)

    script.close()
    newscriptGF.close()
    newscriptVBF.close()


    cmd_permission_GF = "chmod a+x "+a+"GF"+scriptname
    cmd_permission_VBF = "chmod a+x "+a+"VBF"+scriptname
    os.system(cmd_permission_GF);
    os.system(cmd_permission_VBF);
    commandGF = "bsub -q 8nh "+ a+"GF"+scriptname
    print commandGF
    os.system(commandGF);
    commandVBF = "bsub -q 8nh "+ a+"VBF"+scriptname
    print commandVBF
    os.system(commandVBF);
