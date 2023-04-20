cd $path
echo $path

cd ../

. ./setup.sh

cd ./HistFitter

######### Clear up running dir
#cd ./results
#rm -rf ./*
#mkdir ./merged
#cd ../

#################### Models for Interpretation and SROP ######################
python ../python/runWinter2015SameSign.py --FUNCTION --doBlind --fitmodel FITMODEL --Model MODEL --SR REGION --Sys SYSLIST EXTRAOPTION
#python ../python/runWinter2015SameSign.py --FUNCTION --fitmodel FITMODEL --Model MODEL --SR REGION --Sys SYSLIST

#################### Command to get the yields ######################
#python UpperLimitsPlotter.py --FileName Mc16SusyTT2Step_nom_FakesYieldsOrig139.00fb_ALLRpc3LSS1b_UL_winter2019SameSign_output_upperlimit.root --DirName /publicfs/atlas/atlasnew/SUSY/users/liuy/SS3LWorkSpace/SS3L_Packages/SS3L_HF/FullRun2/HistFitter/results/ --OutputName ../../HistFitterUser/SUSY_TT2STEP_ALLRpc3LSS1b
#python BestSignalRegion.py --file1 /publicfs/atlas/atlasnew/SUSY/users/liuy/SS3LWorkSpace/SS3L_Packages/SS3L_HF/FullRun2/HistFitter/results/Mc16SusyBtt_nom_FakesYieldsOrig139.00fb_ALLRpc2L1b_Excl_winter2019SameSign_output_hypotest.root --file2 /publicfs/atlas/atlasnew/SUSY/users/liuy/SS3LWorkSpace/SS3L_Packages/SS3L_HF/FullRun2/HistFitter/results/Mc16SusyBtt_nom_FakesYieldsOrig139.00fb_ALLRpc2L2b_Excl_winter2019SameSign_output_hypotest.root --output ../HistFitterUser/Mc16SusyBtt_nom_FakesYieldsOrig139.00fb_ALLRpc2L1b_Excl_winter2019SameSign_output_hypotest__1_harvest_fix_list_best.txt
#python plotBestSR_For2019Only.py --InDir ../HistFitterUser/ --Grid Btt --Out Btt_ALLBest
#pull_maker.py -i /publicfs/atlas/atlasnew/SUSY/users/liuy/SS3LWorkSpace/SS3L_Packages/SS3L_HF/FullRun2/run/LOG/Log_Mc16SusyGG2StepWZ_Rpc2L0b_bkg_Blind_fit_ALL.txt -o /publicfs/atlas/atlasnew/SUSY/users/liuy/SS3LWorkSpace/SS3L_Packages/SS3L_HF/FullRun2/HistFitterUser/Pulls_GG2StepWZ_Rpc2L0b
#pull_maker.py -i /publicfs/atlas/atlasnew/SUSY/users/liuy/SS3LWorkSpace/SS3L_Packages/SS3L_HF/FullRun2/run/LOG/Log_Mc16SusyBtt_Rpc2L1b_bkg_Blind_fit_ALL.txt -o /publicfs/atlas/atlasnew/SUSY/users/liuy/SS3LWorkSpace/SS3L_Packages/SS3L_HF/FullRun2/HistFitterUser/Pulls_Btt_Rpc2L1b
#pull_maker.py -i /publicfs/atlas/atlasnew/SUSY/users/liuy/SS3LWorkSpace/SS3L_Packages/SS3L_HF/FullRun2/run/LOG/Log_Mc16SusyBtt_Rpc2L2b_bkg_Blind_fit_ALL.txt -o /publicfs/atlas/atlasnew/SUSY/users/liuy/SS3LWorkSpace/SS3L_Packages/SS3L_HF/FullRun2/HistFitterUser/Pulls_Btt_Rpc2L2b
#pull_maker.py -i /publicfs/atlas/atlasnew/SUSY/users/liuy/SS3LWorkSpace/SS3L_Packages/SS3L_HF/FullRun2/run/LOG/Log_Mc16SusyTT2Step_Rpc3LSS1b_bkg_Blind_fit_ALL.txt -o /publicfs/atlas/atlasnew/SUSY/users/liuy/SS3LWorkSpace/SS3L_Packages/SS3L_HF/FullRun2/HistFitterUser/Pulls_TT2Step_Rpc3LSS1b
#pull_maker.py -i /publicfs/atlas/atlasnew/SUSY/users/liuy/SS3LWorkSpace/SS3L_Packages/SS3L_HF/FullRun2/run/LOG/Log_Mc16SusyGG_Rpv331_Rpv2L_bkg__fit_ALL.txt -o /publicfs/atlas/atlasnew/SUSY/users/liuy/SS3LWorkSpace/SS3L_Packages/SS3L_HF/FullRun2/HistFitterUser/Pulls_GG_Rpv331_Rpv2L
