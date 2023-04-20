TopDirectory=`pwd`

cd ./HistFitter/
. ./setup.sh
cd ../

mkdir -p $TopDirectory/HistFitterUser
mkdir -p $TopDirectory/HistFitter/InputTrees

export PYTHONPATH=$TopDirectory/python:$PYTHONPATH
export HFRUNDIR=$TopDirectory/HistFitter

echo 'cd ./HistFitter/InputTrees/'
cd ./HistFitter/InputTrees/
#echo 'xrdcp root://eosuser.cern.ch//eos/user/l/liuya/RECAST/SS3L_HF/background.138965.root ./'
#xrdcp root://eosuser.cern.ch//eos/user/l/liuya/RECAST/SS3L_HF/background.138965.root ./

echo 'copy bkg process root files from eos'
xrdcp root://eosuser.cern.ch//eos/user/l/liuya/RECAST/SS3L_HF/Multitop.138965.root
xrdcp root://eosuser.cern.ch//eos/user/l/liuya/RECAST/SS3L_HF/TTbarSgTop.138965.root
xrdcp root://eosuser.cern.ch//eos/user/l/liuya/RECAST/SS3L_HF/Vjets.138965.root
xrdcp root://eosuser.cern.ch//eos/user/l/liuya/RECAST/SS3L_HF/WZ.138965.root
xrdcp root://eosuser.cern.ch//eos/user/l/liuya/RECAST/SS3L_HF/ttH.138965.root
xrdcp root://eosuser.cern.ch//eos/user/l/liuya/RECAST/SS3L_HF/ttW.138965.root
xrdcp root://eosuser.cern.ch//eos/user/l/liuya/RECAST/SS3L_HF/ttZ.138965.root

echo 'xrdcp root://eosuser.cern.ch//eos/user/l/liuya/RECAST/SS3L_HF/signal.138965.root ./'
xrdcp root://eosuser.cern.ch//eos/user/l/liuya/RECAST/SS3L_HF/signal.138965.root ./

echo 'cd /SS3L_HF/run/'
cd /SS3L_HF/run/

echo 'python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR SRWZonshellTEST --Model Mc16SusyC1N2_onshellWZ  --parallize --signalGroupIndex 0 --signalList signal392234 --SigNameSchema "SP:4,LSP:5"'
python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR SRWZonshellTEST --Model Mc16SusyC1N2_onshellWZ  --parallize --signalGroupIndex 0 --signalList signal392234 --SigNameSchema "SP:4,LSP:5"
