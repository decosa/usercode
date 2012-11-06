
# **************************************************************************************** #
#   Author: Annapaola de Cosa
#     CERN, 06 November 2012
#
# python plotPvalue.py --help
# Usage: plotPvalue.py [options]
#
# Options:
#    -h, --help               show this help message and exit
#    -v, --verbose            Visualize details (for debugging purposes)
#    -e CM, --cm=CM           Indicate centre of mass energy: 7, 8 or 0 for 7+8
#    -l LOWER, --lower=LOWER  Indicate the lower edge of the mass range (default 200 GeV)
#                                              
#    -u UPPER, --upper=UPPER  Indicate the upper edge of the mass range (default 600 GeV)
# **************************************************************************************** #

import sys
sys.argv.append('-b')
import ROOT
import numpy

### OPTION PARSING
from optparse import OptionParser
parser = OptionParser(usage="usage: %prog [options]")
#parser.add_option("-h", "--help", action="help")
parser.add_option("-v", "--verbose",    dest="verbose",  help="Visualize details (for debugging purposes)", default=False, action="store_true")
parser.add_option("-e", "--cm",     dest="cm",   help="Indicate centre of mass energy: 7, 8 or 0 for 7+8",  type="int", default="0")
parser.add_option("-l", "--lower",     dest="lower",   help="Indicate the lower edge of the mass range (default 200 GeV)",  type="int", default="200")
parser.add_option("-u", "--upper",     dest="upper",   help="Indicate the upper edge of the mass range (default 600 GeV)",  type="int", default="600")
(options, args) = parser.parse_args()

### SETTING STYLE
ROOT.gROOT.Reset();
ROOT.gROOT.SetStyle('Plain')
ROOT.gROOT.SetBatch()
ROOT.gROOT.LoadMacro('tdrstyle.C')

### SET OPTIONS
debug = options.verbose
debug_v2 = False
cm = str(options.cm)
if(option.cm == 0):cm=""
low = options.lower
up = options.upper
dcName = "comb"+cm+"_hzz"

### GET THE RIGHT MASS RANGE
f = open("masses.txt", "r")
masses = f.readlines()
masses = [c.replace("\n", "") for c in masses]

def makeMassList(m):
    if (debug_v2): print "MASS: ", m, "--> ", (float(m) >= low and float(m)<= up)
    return (float(m) >= low and float(m)<= up)

masses = filter(makeMassList, masses)
if(debug): print masses

### GET PVALUES FOR ALL THE POINTS IN THE MASS RANGE
pValues = []

for m in masses:
    logFile =  open( m +"/"+dcName+".log.PLC", "r")
    for line in logFile:
        if (line.startswith("p-value")):
            line_ = line.split()
            if(debug):print line_
            pValues.append(line_[-1])
            

### DO THE TGRAPH (FILLING AND STYLE SETTING)
massList = [float(m) for m in masses]
### DRAW 1,2,3,4,5 SIGMAS LINES
oneSigma_line = ROOT.TLine(massList[0],0.1587, massList[-1],0.1587)
twoSigma_line = ROOT.TLine(massList[0],0.02275, massList[-1],0.02275)
threeSigma_line = ROOT.TLine(massList[0],0.0013499, massList[-1],0.0013499) 
fourSigma_line = ROOT.TLine(massList[0], 0.000031671, massList[-1], 0.000031671)
fiveSigma_line = ROOT.TLine(massList[0], 0.000000287, massList[-1], 0.000000287)

### NEED TO USE NUMPY ARRAYS
numpyMasses = numpy.array( massList, dtype=numpy.float )
numpyPValues = numpy.array( pValues, dtype=numpy.float )

if(debug):print numpyMasses
if(debug):print numpyPValues

pvalue_graph = ROOT.TGraph(len(numpyMasses), numpyMasses , numpyPValues);
pvalue_graph.SetLineWidth(2);
pvalue_graph.SetLineStyle(2);
pvalue_graph.SetMarkerStyle(22);
pvalue_graph.SetFillColor(ROOT.kWhite);
pvalue_graph.SetTitle("");
pvalue_graph.GetYaxis().SetTitle("Local p-value");
pvalue_graph.GetXaxis().SetTitle("Higgs boson mass [GeV]");
pvalue_graph.GetXaxis().SetRangeUser(low, up); 
pvalue_graph.SetMaximum(1.);
#pvalue_graph.SetMinimum(0.0);
#pvalue_graph.SetMinimum(0.000001);

c1 = ROOT.TCanvas()
     
pvalue_graph.Draw("ACP3");

oneSigma_line.SetLineColor(ROOT.kRed);
oneSigma_line.Draw("SAME");

twoSigma_line.SetLineColor(ROOT.kRed);
twoSigma_line.Draw("SAME");

threeSigma_line.SetLineColor(ROOT.kRed);
threeSigma_line.Draw("SAME");

fourSigma_line.SetLineColor(ROOT.kRed);
fourSigma_line.Draw("SAME");

fiveSigma_line.SetLineColor(ROOT.kRed);
fiveSigma_line.Draw("SAME");

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.SetTextAlign(11)

if(cm=="7"):intLumi = 4.9
elif(cm=="8"):intLumi = 5.1
else: intlumi = 4.9 + 5.1
latex.DrawLatex(0.1, 0.93, "CMS preliminary 2012");

latex.DrawLatex(0.63,0.93, str(intLumi) + " fb^{-1} at #sqrt{s} = "+cm+" TeV");
if(cm ==""):latex.DrawLatex(0.63,0.93, "4.9 fb^{-1} at #sqrt{s} = 7 TeV + 5.1 fb^{-1} at #sqrt{s} = 8 TeV"); 

latex2 = ROOT.TLatex()
latex2.SetNDC(False)
latex2.SetTextSize(0.04)
latex2.SetTextAlign(11)
latex2.SetTextColor(ROOT.kRed);
latex2.DrawLatex(200,0.15870,"1#sigma");
latex2.DrawLatex(200,0.02275,"2#sigma");
latex2.DrawLatex(200,0.0013499,"3#sigma");

c1.SetLogy();
c1.Print("pValue_"+cm+".png")
 
