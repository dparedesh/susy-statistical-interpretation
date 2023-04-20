def massCheck(fname, doExit=True, showMasses=False, SigNameSchema="SP:4,LSP:5"):
    import os, sys

    if not os.path.exists(fname):
        print fname,"not found"; sys.exit(1)

    posM = []
    for particle in list(SigNameSchema.split(",")):
        posM.append(int(particle.split(":")[-1]))

    masses = []
    numDM = 0;
    f = open(fname, "r")
    for line in f:
        if line.find("#") > -1: continue
        mcid = int(line.split(".")[1])
        name = line.split(".")[2]
        mass = "{0}_{1}".format(name.split("_")[posM[0]],name.split("_")[posM[1]])
    
        if showMasses: print "<INFO> massCheck: MCId {0} \t Masses({1})".format(mcid,mass)

        if masses.count(mass):
            numDM = numDM+1
            print "\033[0;31m<WARNING> massCheck: Mass point for MCId {0} ({1}) exist already \033[0m".format(mcid, mass)
        masses.append(mass)
    
    print "<INFO> massCheck: found {0} samples with same mass parameters".format(numDM)    
    if doExit and numDM: sys.exit(1)
    return
