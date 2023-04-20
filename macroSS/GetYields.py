#!/usr/bin/env python

##########################################
#
# Tools for making final SS contour plots
#
##########################################

import ROOT, argparse, sys, os, math, subprocess
from array import array

ROOT.gROOT.SetBatch()

parser = argparse.ArgumentParser()
parser.add_argument("--Regions", type = str, help="input regions", default="SR7jTEl,SR7jTMu")
parser.add_argument("--DirName", type = str, help="input Dir name", default="")
parser.add_argument("--OutFile", type = str, help="output name", default="")

args = parser.parse_args()


Sampels = "ttV,ttH,FourTop,Rare,Diboson,Fakes,MisCharge"

targetregionDict={
		"Rpc2L0bS":  'Mc15SusyGG2StepWZ',
		"Rpc2L1bS":  'Mc15SusyBtt',
		"Rpc3LSS1b": "Mc15SusyTT2Step",
		"Rpc3L0bS": "Mc15SusyGSL",
}

targetSignalDict={
		"Rpc2L0bS":  '371317_1600.0_1000.0',
		"Rpc2L1bS":  '372368_900.0_625.0',
		"Rpc3LSS1b": "388238_800.0_525.0",
		"Rpc3L0bS": "373478_2200.0_1100.0",
}

def main():
	"""Main function for driving the whole thing..."""
	print(">>>Welcome to GetYields script!!!")

	# Print out the settings
	for setting in dir(args):
		if not setting[0]=="_":
			print( ">>> ... Setting: {: >20} {: >40}".format(setting, eval("args.%s"%setting) ) )

	Regions = args.Regions.split(",")
	for Region in Regions:
		Model = targetregionDict[Region]
		Signal = targetSignalDict[Region]

		WorkSpace = args.DirName + "/" + Model + "_nom_FakesYieldsOrig_36.08fb_" + Region + "_Excl_Job00_winter2015SameSign/" + Model + "_signal" + Signal + "_combined_NormalMeasurement_model_afterFit.root"
		OutFile = args.OutFile + "/" + Model + "_" + Region + ".tex"

		cmd = "YieldsTable.py -c {0} -w {1} -o {2} -s {3}".format(Region, WorkSpace, OutFile, Sampels) 
		print "launching command ",cmd
		subprocess.call(cmd+"\n", shell=True)


if __name__ == "__main__":
		main()

