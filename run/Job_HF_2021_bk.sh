cd $path
echo $path

cd ../

. ./setup.sh

cd ./HistFitter

#################### Models for Interpretation and SROP ######################
python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR Rpc2L0BR --Model Mc16SusyC1N2N1_GGMHinoZh --SigNameSchema SP:4,LSP:5 --WithSigMass EXTRAOPTION
