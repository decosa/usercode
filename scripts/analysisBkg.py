import os, commands
import string

#bkg = ['TT', 'ZZ','WZ', 'Z1jet', 'Z2jet', 'Z3jet', 'Z4jet', 'Z5jet']
#bkg = ['Z1jet', 'Z1jet100_300', 'Z1jet300_800']
#bkg = ['Z2jet', 'Z2jet100_300', 'Z2jet300_800']
#bkg = ['Z3jet', 'Z3jet100_300', 'Z3jet300_800']
#bkg = ['Z4jet', 'Z4jet100_300', 'Z4jet300_800']
#bkg = ['Z5jet', 'Z5jet100_300', 'Z5jet300_800']
bkg = ['Z0Jet','Z1Jet','Z2Jet','Z3Jet','Z4Jet','Z5Jet','Z1Jet100_300','Z2Jet100_300','Z3Jet100_300','Z4Jet100_300','Z5Jet100_300','Z1Jet300_800','Z2Jet300_800','Z3Jet300_800','Z4Jet300_800','Z5Jet300_800','Z1Jet800_1600','Z2Jet800_1600','Z3Jet800_1600','Z4Jet800_1600','Z5Jet800_1600','ZBB0', 'ZBB1', 'ZBB2', 'ZBB3', 'ZCC0', 'ZCC1', 'ZCC2', 'ZCC3']
lumiNorm = [1.755,1.5229,1.1105,0.528,0.104,0.132,0.0417,0.0839,0.0911,0.0372,0.057206, 0.00085,0.00134,0.00195, 0.00460, 0.002217,0.000005, 0.00003, 0.00003, 0.00002, 0.000008, 0.0062, 0.0060,0.426, 0.0186, 0.0049, 0.0066, 0.0433, 0.0205]
#bkgJet = ["Z0jet","Z1jet", "Z2jet","Z3jet","Z4jet","Z5jet", "Z0jet100_300","Z1jet100_300", "Z2jet100_300","Z3jet100_300","Z4jet100_300","Z5jet100_300"]
#bkg = ['ZBB0']
#bkgJet =["","100_300", "300_800"]


def filesource(dirname, dir):
        castor_path = "/castor/cern.ch/user/d/decosa/Higgs/"+ dirname + "/skim/"
        cmd = "rfdir"+" "+castor_path
        status,ls_la = commands.getstatusoutput( cmd )
        #if status: raise RFIOError('Directory %s not found' % dirname)

        list = ls_la.split(os.linesep)
        
        for d in list:
            dd = d.split()
            for ddd in dd:
                if ddd.endswith('.root'):dir.append('rfio:'+castor_path+ ddd )
	return 0	


#print "bkg type: "
#print bkg
for a in bkg:
	print "A" + a
    ### creation of python config file for GF and VBF samples
	
	cfgfilename = "higgs2l2bAnalysis.py"    
	file = open(cfgfilename, "r")
	newfile = open(a+cfgfilename, "w")
    ### need to know which are skim file names
	dir=[];
	
	filesource(a,dir)		

	source = '\' , \''.join(dir)    
	#print "SOURCE " + source
	while 1:
		line = file.readline()
		if line =="":
			break;
		newline = string.replace(line, "300GF", a)

		if line.startswith("process.source.fileNames=cms.untracked.vstring('file:filename.root')"):
			newline = string.replace(newline, 'file:filename.root', source );
		if line.startswith("    lumiNormalization"):
			newline = string.replace(newline,'0.00115', str(lumiNorm[bkg.index(a)] ) );
		if line.startswith("    output_name"):
			newline = string.replace(newline,'h350GF', a) ;

											
		newfile.write(newline)
	

	file.close()
	newfile.close()
        
         ### Create scripts for every value of mass and for GF and VBF to run analysis in batch queue 
        
	scriptname = "jobtest.csh"    
	script = open(scriptname, "r")
	newscript = open(a+scriptname, "w")
	
        ### need to know which are skim file names
	castor_path = "/castor/cern.ch/user/d/decosa/Higgs/"+ a + "/skim/"

	#print "NEW PATH "+ castor_path
	#print "folder " + a
	while 1:
		line = script.readline()
		if line =="":
			break;
		newline = string.replace(line, "300GF", a )
		newline = string.replace(newline, "h350GF", a )
		print newline

		if line.startswith("cmsRun "):
			newline = string.replace(newline, cfgfilename, a+ cfgfilename );
		print  newline

		newscript.write(newline)


	script.close()
	newscript.close()
	
	cmd_permission = "chmod a+x "+a+scriptname
	os.system(cmd_permission)
	command = "bsub -q 8nh "+ a+scriptname
	print command
	os.system(command)

