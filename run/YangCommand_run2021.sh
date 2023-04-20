#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZonshell1
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZonshell1
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZonshell1ee
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZonshell1ee
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZonshell1em
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZonshell1em
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZonshell1mm
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZonshell1mm
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZonshell2
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZonshell2
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZonshell2ee
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZonshell2ee
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZonshell2em
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZonshell2em
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZonshell2mm
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZonshell2mm

#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost1
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost1
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost1ee
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost1ee
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost1em
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost1em
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost1mm
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost1mm
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost2
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost2
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost2ee
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost2ee
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost2em
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost2em
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost2mm
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellBoost2mm
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal1
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal1
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal1ee
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal1ee
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal1em
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal1em
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal1mm
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal1mm
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal2
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal2
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal2ee
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal2ee
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal2em
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal2em
#
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal2mm
#python ../python/generateCommands.py --yields --doBlind ALL --fitmodel bkg  --SR SRWZoffshellDiagonal2mm
#

#nohup python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR SRWZonshell1ee,SRWZonshell1em,SRWZonshell1mm,SRWZonshell2ee,SRWZonshell2em,SRWZonshell2mm --Model Mc16SusyC1N2_onshellWZ --SigNameSchema SP:4,LSP:5 --extraFitConfig '--binnedFitSR SRWZonshell1ee:met_Sig,SRWZonshell1em:met_Sig,SRWZonshell1mm:met_Sig,SRWZonshell2ee:met_Sig,SRWZonshell2em:met_Sig,SRWZonshell2mm:met_Sig' 1>./LOG/Log_onShell.txt 2>./LOG/Err_onShell.txt &

#nohup python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR SRWZoffshellBoost1ee,SRWZoffshellBoost1em,SRWZoffshellBoost1mm --Model Mc16SusyC1N2_offshellWZ --SigNameSchema SP:4,LSP:5 --extraFitConfig '--binnedFitSR SRWZonshell1ee:met_Sig,SRWZonshell1em:met_Sig,SRWZonshell1mm:met_Sig,SRWZonshell2ee:met_Sig,SRWZonshell2em:met_Sig,SRWZonshell2mm:met_Sig' 1>./LOG/Log_onShell.txt 2>./LOG/Err_onShell.txt &
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR SRWZonshell1ee,SRWZonshell1em,SRWZonshell1mm,SRWZonshell2ee,SRWZonshell2em,SRWZonshell2mm --Model Mc16SusyC1N2_onshellWZ --SigNameSchema SP:4,LSP:5 --extraFitConfig '--binnedFitSR SRWZonshell1ee:met_Sig,SRWZonshell1em:met_Sig,SRWZonshell1mm:met_Sig,SRWZonshell2ee:met_Sig,SRWZonshell2em:met_Sig,SRWZonshell2mm:met_Sig' --extra syst:HTCondor,queue:8nh,storage:2000 --batch


#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR SRWZoffshellDiagonal1,SRWZoffshellDiagonal2,SRWZoffshellBoost1,SRWZoffshellBoost2 --Model Mc16SusyC1N2_allWZ --SigNameSchema SP:4,LSP:5 --extraFitConfig '--binnedFitSR SRWZoffshellDiagonal1:cuts,SRWZoffshellDiagonal2:cuts,SRWZoffshellBoost1:cuts,SRWZoffshellBoost2:cuts' --extra syst:HTCondor,queue:8nh,storage:2000 --batch

#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR SRWZoffshellDiagonal1,SRWZoffshellDiagonal2,SRWZoffshellBoost1,SRWZoffshellBoost2 --Model Mc16SusyC1N2_allWZ --SigNameSchema SP:4,LSP:5 --extraFitConfig '--binnedFitSR SRWZoffshellDiagonal1:SSChannel,SRWZoffshellDiagonal2:SSChannel,SRWZoffshellBoost1:SSChannel,SRWZoffshellBoost2:SSChannel' --extra syst:HTCondor,queue:8nh,storage:2000 --batch

#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR SRWZoffshellDiagonal1,SRWZoffshellDiagonal2,SRWZoffshellBoost1,SRWZoffshellBoost2 --Model Mc16SusyC1N2_allWZ --SigNameSchema SP:4,LSP:5 --extraFitConfig '--binnedFitSR SRWZoffshellDiagonal1:met_Sig,SRWZoffshellDiagonal2:met_Sig,SRWZoffshellBoost1:met_Sig,SRWZoffshellBoost2:met_Sig' --extra syst:HTCondor,queue:8nh,storage:2000 --batch

#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR SRWZoffshellDiagonal1ee,SRWZoffshellDiagonal1em,SRWZoffshellDiagonal1mm,SRWZoffshellDiagonal2ee,SRWZoffshellDiagonal2em,SRWZoffshellDiagonal2mm,SRWZoffshellBoost1ee,SRWZoffshellBoost1em,SRWZoffshellBoost1mm,SRWZoffshellBoost2ee,SRWZoffshellBoost2em,SRWZoffshellBoost2mm --Model Mc16SusyC1N2_allWZ --SigNameSchema SP:4,LSP:5 --extraFitConfig '--binnedFitSR SRWZoffshellDiagonal1ee:met_Sig,SRWZoffshellDiagonal2ee:met_Sig,SRWZoffshellBoost1ee:met_Sig,SRWZoffshellBoost2ee:met_Sig,SRWZoffshellDiagonal1em:met_Sig,SRWZoffshellDiagonal2em:met_Sig,SRWZoffshellBoost1em:met_Sig,SRWZoffshellBoost2em:met_Sig,SRWZoffshellDiagonal1mm:met_Sig,SRWZoffshellDiagonal2mm:met_Sig,SRWZoffshellBoost1mm:met_Sig,SRWZoffshellBoost2mm:met_Sig' --extra syst:HTCondor,queue:8nh,storage:2000 --batch

#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --Model Mc16SusyC1N2_allWZ --SigNameSchema SP:4,LSP:5 --extra syst:HTCondor,queue:8nh,storage:2000 --batch

### This line is for HF CI test
#python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR SRWZonshellTEST --Model Mc16SusyC1N2_onshellWZ  --parallize --signalGroupIndex 0 --signalList signal392234 --SigNameSchema "SP:4,LSP:5" 

python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR Rpc2L0BR --Model Mc16SusyC1N2N1_GGMHinoZh --SigNameSchema SP:4,LSP:5 --withSigMass --extra syst:HTCondor,queue:8nh,storage:2000 --batch
