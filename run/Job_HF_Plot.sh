
cd ./HistFitter


#################### Models for Interpretation and SROP ######################
#python ../python/runWinter2015SameSign.py plot Mc15SusyGG2StepWZ Rpc2L0bS
#mv ../HistFitterUser/SUSY_GG2STEPWZ.pdf ../HistFitterUser/SUSY_GG2STEPWZ_Rpc2L0bS.pdf
#
#python ../python/runWinter2015SameSign.py plot Mc15SusyGG2StepWZ Rpc2L0bH
#mv ../HistFitterUser/SUSY_GG2STEPWZ.pdf ../HistFitterUser/SUSY_GG2STEPWZ_Rpc2L0bH.pdf
#
#python ../python/runWinter2015SameSign.py plot makeBest Mc15SusyGG2StepWZ Rpc2L0bH
#mv ../HistFitterUser/SUSY_GG2STEPWZ.pdf ../HistFitterUser/SUSY_GG2STEPWZ_BEST.pdf
#
#python ../python/runWinter2015SameSign.py plot Mc15SusyBtt Rpc2L1bS
#mv ../HistFitterUser/SUSY_BTT.pdf ../HistFitterUser/SUSY_BTT_Rpc2L1bS.pdf
#
#python ../python/runWinter2015SameSign.py plot Mc15SusyBtt Rpc2L1bH
#mv ../HistFitterUser/SUSY_BTT.pdf ../HistFitterUser/SUSY_BTT_Rpc2L1bH.pdf
#
#python ../python/runWinter2015SameSign.py plot makeBest Mc15SusyBtt Rpc2L1bH
#mv ../HistFitterUser/SUSY_BTT.pdf ../HistFitterUser/SUSY_BTT_BEST.pdf
#
#
#python ../python/runWinter2015SameSign.py plot Mc15SusyGG_RpvLQD Rpv2L0b

#################### Models for SROP ######################

python ../python/runWinter2015SameSign.py plot Mc15SusyGtt Rpc2L2bS
mv ../HistFitterUser/SUSY_GTT.pdf ../HistFitterUser/SUSY_GTT_Rpc2L2bS.pdf

python ../python/runWinter2015SameSign.py plot Mc15SusyGtt Rpc2L2bH
mv ../HistFitterUser/SUSY_GTT.pdf ../HistFitterUser/SUSY_GTT_Rpc2L2bH.pdf

python ../python/runWinter2015SameSign.py plot makeBest Mc15SusyGtt Rpc2L2bH
mv ../HistFitterUser/SUSY_GTT.pdf ../HistFitterUser/SUSY_GTT_BEST.pdf
#
#python ../python/runWinter2015SameSign.py plot Mc15SusyGSL Rpc3L0bS
#mv ../HistFitterUser/SUSY_GSL.pdf ../HistFitterUser/SUSY_GSL_Rpc3L0bS.pdf
#
#python ../python/runWinter2015SameSign.py plot Mc15SusyGSL Rpc3L0bH
#mv ../HistFitterUser/SUSY_GSL.pdf ../HistFitterUser/SUSY_GSL_Rpc3L0bH.pdf
#
#python ../python/runWinter2015SameSign.py plot makeBest Mc15SusyGSL Rpc3L0bH
#mv ../HistFitterUser/SUSY_GSL.pdf ../HistFitterUser/SUSY_GSL_BEST.pdf
#
#python ../python/runWinter2015SameSign.py plot Mc15SusyGG_Rpv321 Rpv2L1bH
#
#python ../python/runWinter2015SameSign.py plot Mc15SusyGG_Rpv331 Rpv2L1bH

cd -

