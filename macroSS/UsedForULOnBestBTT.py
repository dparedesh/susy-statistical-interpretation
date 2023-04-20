import numpy as np
import ROOT, os
from ROOT import TFile
from ROOT import TGraph2D
from array import array
files  = np.loadtxt("SusyBtt_ALLRpc2L1b_Obs_UpperLimits_best.txt", delimiter=',')

x = files[:,0]
y = files[:,1]
z = files[:,2]


xMass = array('d')
yMass = array('d')
obs = array('d')

for i in range(len(x)):
	xMass.append(float(x[i]))

for i in range(len(y)):
	yMass.append(float(y[i]))

for i in range(len(z)):
	obs.append(float(z[i]))



Out_File = TFile("Mc16SusyBtt_nom_FakesYieldsOrig139.00fb_ALLRpc2L1b_UL_winter2019SameSign_output_upperlimit__1_harvest_fix_list_best_Obs_UpperLimit.root", "RECREATE")
UpperLimits_gr = TGraph2D("upperLimits_gr", "upperLimits_gr", len(xMass), xMass, yMass, obs)
Out_File.cd()
UpperLimits_gr.Write()
Out_File.Close()
