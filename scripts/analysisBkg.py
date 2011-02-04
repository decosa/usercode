import os, commands
import string

bkg = ['Z0jet', 'Z1jet', 'Z2jet', 'Z3jet', 'Z4jet', 'Z5jet']
lumiNorm = [1.755,1.5229,1.1105,0.528,0.13202,0.1318]
#bkg = [ 'Z1jet100_300', 'Z2jet100_300', 'Z3jet100_300', 'Z4jet100_300', 'Z5jet100_300']
#lumiNorm = [0.04173,0.08395,0.09114,0.03723,0.057206]
#bkg = [ 'Z1jet300_800', 'Z2jet300_800', 'Z3jet300_800', 'Z4jet300_800', 'Z5jet300_800']
#lumiNorm = [0.00085,0.00134,0.00195, 0.00460, 0.002217]
#bkg = [ 'Z1jet800_1600', 'Z2jet800_1600', 'Z3jet800_1600', 'Z4jet800_1600', 'Z5jet800_1600']
#lumiNorm = [0.000005, 0.00003, 0.00003, 0.00002, 0.000008]
#bkg = [ 'ZBB0', 'ZBB1', 'ZBB2', 'ZBB3', 'ZCC0', 'ZCC1', 'ZCC2', 'ZCC3']
#lumiNorm = [0.0062, 0.0060, 0.426, 0.0186, 0.0049, 0.0066, 0.0433, 0.0205]
#bkg = ['TT', 'ZZ','WZ']

#lumiNorm = [0.01755, 0.00767, 0.00829]

#bkg = ['TT', 'ZZ']
#lumiNorm = [0.01755, 0.00767]

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
		newline = string.replace(newline, "H300GF", a )
		newline = string.replace(newline, "h350GF", a )
		newline = string.replace(newline, "h300", a )
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

