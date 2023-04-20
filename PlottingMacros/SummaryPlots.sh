## Get summary yields plot with VRs and SRs in the same plot:
python plotSR.py  --Plot 1  --makeTex 0 --Name AllYields  --LogY 1  --doPlotAsymUnc 1

## Get summary plot and table for VR
python plotSR.py  --Plot 1  --makeTex 1 --Name VRYields --doPlotAsymUnc 1

## Get summary plot with significance for SR
python plotSR.py  --Plot 1  --makeTex 0 --Name SRYields --doPlotAsymUnc 1 --doSig 1

## Get summary plot and table for SR
python plotSR.py  --Plot 1  --makeTex 1 --Name SRYields --doPlotAsymUnc 1


## Get grouped systematics:
python PlotSystematicsGrouped.py --InDir ../Run/SystematicTxt/
