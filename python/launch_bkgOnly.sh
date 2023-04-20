
mkdir -p Logs

rm -rf Logs/VR*.log

HistFitter.py -twf -u " --lumiTag 138964 --signalGridName Mc15SusyTest --additionalOutName nom_TablesBgOnly_VRWZ4j --signalList bkgOnly --theoryUncertMode nom --signalRegions VRWZ4j " ../python/winter2019SameSign.py  > Logs/VRWZ4j.log;
HistFitter.py -twf -u " --lumiTag 138964 --signalGridName Mc15SusyTest --additionalOutName nom_TablesBgOnly_VRWZ5j --signalList bkgOnly --theoryUncertMode nom --signalRegions VRWZ5j " ../python/winter2019SameSign.py > Logs/VRWZ5j.log;
HistFitter.py -twf -u " --lumiTag 138964 --signalGridName Mc15SusyTest --additionalOutName nom_TablesBgOnly_VRttV --signalList bkgOnly --theoryUncertMode nom --signalRegions VRttV " ../python/winter2019SameSign.py > Logs/VRttV.log;

rm -rf Logs/SR*.log
HistFitter.py -twf -u " --lumiTag 138964 --signalGridName Mc15SusyTest --additionalOutName nom_TablesBgOnly_Rpc2L0b --signalList bkgOnly --theoryUncertMode nom --signalRegions Rpc2L0b " ../python/winter2019SameSign.py > Logs/SR_Rpc2L0b.log;
HistFitter.py -twf -u " --lumiTag 138964 --signalGridName Mc15SusyTest --additionalOutName nom_TablesBgOnly_Rpc2L1b --signalList bkgOnly --theoryUncertMode nom --signalRegions Rpc2L1b " ../python/winter2019SameSign.py > Logs/SR_Rpc2L1b.log;
HistFitter.py -twf -u " --lumiTag 138964 --signalGridName Mc15SusyTest --additionalOutName nom_TablesBgOnly_Rpc2L2b --signalList bkgOnly --theoryUncertMode nom --signalRegions Rpc2L2b " ../python/winter2019SameSign.py > Logs/SR_Rpc2L2b.log;
HistFitter.py -twf -u " --lumiTag 138964 --signalGridName Mc15SusyTest --additionalOutName nom_TablesBgOnly_Rpv2L --signalList bkgOnly --theoryUncertMode nom --signalRegions Rpv2L " ../python/winter2019SameSign.py > Logs/SR_Rpv2L.log;
HistFitter.py -twf -u " --lumiTag 138964 --signalGridName Mc15SusyTest --additionalOutName nom_TablesBgOnly_Rpc3LSS1b --signalList bkgOnly --theoryUncertMode nom --signalRegions Rpc3LSS1b " ../python/winter2019SameSign.py > Logs/SR_Rpc3LSS1b.log;
