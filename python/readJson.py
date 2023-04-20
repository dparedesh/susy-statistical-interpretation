import os
import sys
import json
from ROOT import TFile, TH2F

if len(sys.argv) < 2:
    print "Please specify a json file"; sys.exit(1)

filename = sys.argv[1]
if not len(filename):
    print "Please specify a json file"; sys.exit(1)

if not os.path.exists(filename):
    print "File {0} does not exist".format(filename); sys.exit(1)

print "Reading {0} \n".format(filename)
gridname = filename.split("_")[0]

fin = open(filename, "r")
fout = TFile(gridname+"_CL.root", "recreate")
ftxt = open(gridname+"_CL.txt", "w")

h_CLObs = TH2F(gridname+"_CLObs", gridname+"_CLObs",1000, 0, 2000, 1000, 0, 2000)
h_CLExp = TH2F(gridname+"_CLExp", gridname+"_CLExp",1000, 0, 2000, 1000, 0, 2000)

data = [json.loads(line) for line in fin]
for d in data[0]:

    outline = "MCId {0:.0f} \t m0 {1:.0f} \t m12 {2:.0f} \t CLObs {3:.6f} \t CLExp {4:.6f}".format(d['chan'],d['m0'],d['m12'],d['CLs'],d['CLsexp'])
    print outline
    
    m0  = d['m0']
    m12 = d['m12']
    clobs = d['CLs']
    clexp = d['CLsexp']

    h_CLObs.Fill(m0, m12, clobs)
    h_CLExp.Fill(m0, m12, clexp)

    outline = outline +"\n"
    ftxt.write(outline)

h_CLObs.Write()
h_CLExp.Write()

print "Wrote",ftxt.name
print "Wrote",fout.GetName()
