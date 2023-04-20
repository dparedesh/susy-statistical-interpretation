#!/usr/bin/env python

def main():
    import ROOT, sys
    command = sys.argv[1]
    print "passing to ROOT the command ", command
    ROOT.gROOT.ProcessLine(command)


main()
