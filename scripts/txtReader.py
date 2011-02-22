import os, commands

#samples = ['Z0jet','Z1jet','Z2jet','Z3jet','Z4jet','Z5jet']
zjets = ['Z0Jet','Z1Jet','Z2Jet','Z3Jet','Z4Jet','Z5Jet','Z1Jet100_300','Z2Jet100_300','Z3Jet100_300','Z4Jet100_300','Z5Jet100_300','Z1Jet300_800','Z2Jet300_800','Z3Jet300_800','Z4Jet300_800','Z5Jet300_800','Z1Jet800_1600','Z2Jet800_1600','Z3Jet800_1600','Z4Jet800_1600','Z5Jet800_1600','ZBB0', 'ZBB1', 'ZBB2','ZBB3', 'ZCC0', 'ZCC1', 'ZCC2', 'ZCC3']

zjetsTocopy = ['Z1Jet800_1600','Z2Jet800_1600','Z3Jet800_1600','Z4Jet800_1600','Z5Jet800_1600','ZBB0', 'ZBB1', 'ZBB2','ZBB3', 'ZCC0', 'ZCC1', 'ZCC2', 'ZCC3']



TT = ['TT']
WZ = ['WZ']
ZZ = ['ZZ']

HGFVBF = ['h350GF', 'h350VBF']


def readFile(file):
	numbers=[]
	while 1:
		line = file.readline()
		print line
		if line =="":
			break
		if line.startswith(" events after skimming"):
			l= line.split(" ")
			a = l[-1].replace("\n","")
			numbers.append(float(a))
		if line.startswith(" events after mass"):
			l= line.split(" ")
			a = l[-1].replace("\n","")
			numbers.append(float(a))
		if line.startswith(" events after btag"):
			l= line.split(" ")
			a = l[-1].replace("\n","")
			numbers.append(float(a))
		if line.startswith(" events after zllpt"):
			l= line.split(" ")
			a = l[-1].replace("\n","")
			numbers.append(float(a))
		if line.startswith(" events after met"):
			l= line.split(" ")
			a = l[-1].replace("\n","")
			numbers.append(float(a))
		if line.startswith(" events after jjdr"):
			l= line.split(" ")
			a = l[-1].replace("\n","")
			numbers.append(float(a))
		if line.startswith(" events after hmass"):
			l= line.split(" ")
			a = l[-1].replace("\n","")
			numbers.append(float(a))

	return numbers

def getNumEvts(samples, filename):
	
	skimming=0 
	mass=0
	btag=0
	zllpt=0
	met=0
	jjdr=0
	hmass=0
	file = open(filename+"Selection.txt", "w")
	
	
	for a in samples:
		muonfilename = a+"MuonSelection.txt"
		electronfilename = a+"ElectronSelection.txt"
		fileMu = open(muonfilename, "r")
		fileEl = open(electronfilename, "r")
		numMu = readFile(fileMu)
		numEl = readFile(fileEl)

		skimming+= numMu[0]+numEl[0] 
		mass+= numMu[1]+numEl[1] 
		btag+= numMu[2]+numEl[2] 
		zllpt+= numMu[3]+numEl[3]
		met+= numMu[4]+numEl[4] 
		jjdr+= numMu[5]+numEl[5]
		hmass+= numMu[6]+numEl[6] 

	file.write("events after skimming: "+ str(skimming)+"\n" )		

	file.write("events after mass cut: "+ str(mass)+"\n" )		

	file.write("events after btag cut: "+ str(btag)+"\n" )		

	file.write("events after zllpt cut: "+ str(zllpt)+"\n" )		

	file.write("events after met cut: "+ str(met) +"\n")		

	file.write("events after jjdr cut: "+ str(jjdr) +"\n")		

	file.write("events after hmass cut: "+ str(hmass) +"\n")		
	file.close()

	
scpzjetstxt = ['Z0jet','Z1jet','Z2jet','Z3jet','Z4jet','Z5jet','Z1jet100_300','Z2jet100_300','Z3jet100_300','Z4jet100_300','Z5jet100_300','Z1jet300_800','Z2jet300_800','Z3jet300_800','Z4jet300_800','Z5jet300_800','Z1jet800_1600','Z2jet800_1600','Z3jet800_1600','Z4jet800_1600','Z5jet800_1600','ZBB0', 'ZBB1', 'ZBB2','ZBB3', 'ZCC0', 'ZCC1', 'ZCC2', 'ZCC3']

scpzjetstxtToCopy = ['Z1jet800_1600','Z2jet800_1600','Z3jet800_1600','Z4jet800_1600','Z5jet800_1600','ZBB0', 'ZBB1', 'ZBB2','ZBB3', 'ZCC0', 'ZCC1', 'ZCC2', 'ZCC3'] 

H = ['h350']
def scpTxtFiles(sample, sample2): 
	for a in sample:

		commandMu = "rfcp /castor/cern.ch/user/d/decosa/Higgs/"+a+"/histos/"+sample2[sample.index(a)]+"MuonSelection.txt ."
		print commandMu
		commandEl = "rfcp /castor/cern.ch/user/d/decosa/Higgs/"+a+"/histos/"+sample2[sample.index(a)]+"ElectronSelection.txt ."  
		print commandEl
		os.system(commandMu)
		os.system(commandEl)

scpTxtFiles(scpzjetstxtToCopy, scpzjetstxtToCopy)
#scpTxtFiles(TT, TT)
#scpTxtFiles(WZ, WZ)
#scpTxtFiles(ZZ, ZZ)
HGF = ['h350GF']
HVBF = ['h350VBF']

#scpTxtFiles(H, HGF)
#scpTxtFiles(H, HVBF)

getNumEvts(scpzjetstxt, "ZJets")
#getNumEvts(TT, "TT")
#getNumEvts(WZ, "WZ")
#getNumEvts(ZZ, "ZZ")
#getNumEvts(HGFVBF, "h350")


## 	if line =="":
## 		break;
## 	newline = string.replace(line, "300GF", a)
	
## 	if line.startswith("process.source.fileNames=cms.untracked.vstring('file:filename.root')"):
## 		newline = string.replace(newline, 'file:filename.root', source );
##         if line.startswith("    lumiNormalization"):
##                         newline = string.replace(newline,'0.00115', str(lumiNorm[bkg.index(a)] ) );
##                 if line.startswith("    output_name"):
##                         newline = string.replace(newline,'h350GF', a) ;


##                 newfile.write(newline)


##         file.close()
##         newfile.close()
