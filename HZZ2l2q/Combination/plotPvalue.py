import sys
#sys.argv.append('-b')
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
if(options.cm == 0):cm=""
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
def z(n):
    return  0.5*(1 - ROOT.TMath.Erf(n/(ROOT.TMath.Sqrt(2))))
one = z(1)
two = z(2)
three = z(3)
four = z(4)
five = z(5)
six = z(6)
seven = z(7)

print one
oneSigma_line = ROOT.TLine(massList[0],one, massList[-1],one)
twoSigma_line = ROOT.TLine(massList[0],two, massList[-1],two)
threeSigma_line = ROOT.TLine(massList[0], three, massList[-1],three) 
fourSigma_line = ROOT.TLine(massList[0], four, massList[-1], four)
fiveSigma_line = ROOT.TLine(massList[0], five, massList[-1], five)
sixSigma_line = ROOT.TLine(massList[0],six, massList[-1], six)
sevenSigma_line = ROOT.TLine(massList[0],seven, massList[-1], seven)

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
min_ = min(pValues)
print max(pValues)
print numpyPValues.min()
pvalue_graph.SetMinimum(0.1 * numpyPValues.min());
#pvalue_graph.SetMinimum(0.00000000000001);

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

sixSigma_line.SetLineColor(ROOT.kRed);
sixSigma_line.Draw("SAME");

sevenSigma_line.SetLineColor(ROOT.kRed);
sevenSigma_line.Draw("SAME");

latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.SetTextAlign(11)
intLumi = 0.
if(cm=="7"):intLumi = 4.9
elif(cm=="8"):intLumi = 5.1
else: intlumi = 4.9 + 5.1
latex.DrawLatex(0.1, 0.93, "CMS preliminary 2012");


if(cm ==""):latex.DrawLatex(0.40,0.93, "4.9 fb^{-1} at #sqrt{s} = 7 TeV + 5.1 fb^{-1} at #sqrt{s} = 8 TeV")
else: latex.DrawLatex(0.63,0.93, str(intLumi) + " fb^{-1} at #sqrt{s} = "+cm+" TeV")

latex2 = ROOT.TLatex()
latex2.SetNDC(False)
latex2.SetTextSize(0.04)
latex2.SetTextAlign(11)
latex2.SetTextColor(ROOT.kRed);
latex2.DrawLatex(220,one,"1#sigma");
latex2.DrawLatex(220,two,"2#sigma");
latex2.DrawLatex(220,three,"3#sigma");
latex2.DrawLatex(220,four,"4#sigma");
latex2.DrawLatex(220,five,"5#sigma");
latex2.DrawLatex(220,six,"6#sigma");
latex2.DrawLatex(220,seven,"7#sigma");

c1.SetLogy();
c1.Print("pValue_"+cm+".png")
 
