#!/bin/bash


mkdir -p Tables


YieldsTable.py -c VRWZ4j -w results/Mc15SusyTest_nom_TablesBgOnly_VRWZ4j_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/Disc_VRWZ4j.tex -s WZ,OtherMultiboson,ttW,ttZ,Multitop,Fakes,MisCharge -b -B -C 'Yields in VRWZ4j' -L "tab:HF_yields_VRWZ4j";
YieldsTable.py -c VRWZ5j -w results/Mc15SusyTest_nom_TablesBgOnly_VRWZ5j_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/Disc_VRWZ5j.tex -s WZ,OtherMultiboson,ttW,ttZ,Multitop,Fakes,MisCharge -b -B -C 'Yields in VRWZ5j' -L "tab:HF_yields_VRWZ5j";
 
YieldsTable.py -c VRttV -w results/Mc15SusyTest_nom_TablesBgOnly_VRttV_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/Disc_VRttV.tex -s WZ,OtherMultiboson,ttW,ttZ,Multitop,Fakes,MisCharge -b -B -C 'Yields in VRttV' -L "tab:HF_yields_VRttV";

YieldsTable.py -c Rpc2L0b -w results/Mc15SusyTest_nom_TablesBgOnly_Rpc2L0b_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/Disc_Rpc2L0b.tex -s WZ,OtherMultiboson,ttW,ttZ,Multitop,Fakes,MisCharge -b -B -C 'Yields in Rpc2L0b' -L "tab:HF_yields_Rpc2L0b";

YieldsTable.py -c Rpc2L1b -w results/Mc15SusyTest_nom_TablesBgOnly_Rpc2L1b_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/Disc_Rpc2L1b.tex -s WZ,OtherMultiboson,ttW,ttZ,Multitop,Fakes,MisCharge -b -B -C 'Yields in Rpc2L1b' -L "tab:HF_yields_Rpc2L1b"; 

YieldsTable.py -c Rpc2L2b -w results/Mc15SusyTest_nom_TablesBgOnly_Rpc2L2b_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/Disc_Rpc2L2b.tex -s WZ,OtherMultiboson,ttW,ttZ,Multitop,Fakes,MisCharge -b -B -C 'Yields in Rpc2L2b' -L "tab:HF_yields_Rpc2L2b";
 
YieldsTable.py -c Rpv2L -w results/Mc15SusyTest_nom_TablesBgOnly_Rpv2L_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/Disc_Rpv2L.tex -s WZ,OtherMultiboson,ttW,ttZ,Multitop,Fakes,MisCharge -b -B -C 'Yields in Rpv2L' -L "tab:HF_yields_Rpv"; 

YieldsTable.py -c Rpc3LSS1b -w results/Mc15SusyTest_nom_TablesBgOnly_Rpc3LSS1b_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/Disc_Rpc3LSS1b.tex -s WZ,OtherMultiboson,ttW,ttZ,Multitop,Fakes,MisCharge -b -B -C 'Yields in Rpc3LSS1b' -L "tab:HF_yields_Rpc3LSS1b";

SysTable.py -c Rpv2L -w results/Mc15SusyTest_nom_TablesBgOnly_Rpv2L_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/BeforeFit_Syst_BkgOnly_Rpv2L.tex -b  -%

SysTable.py -c Rpc2L2b -w results/Mc15SusyTest_nom_TablesBgOnly_Rpc2L2b_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/BeforeFit_Syst_BkgOnly_Rpc2L2b.tex -b  -%

SysTable.py -c Rpc2L1b -w results/Mc15SusyTest_nom_TablesBgOnly_Rpc2L1b_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/BeforeFit_Syst_BkgOnly_Rpc2L1b.tex -b -%

SysTable.py -c Rpc2L0b -w results/Mc15SusyTest_nom_TablesBgOnly_Rpc2L0b_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/BeforeFit_Syst_BkgOnly_Rpc2L0b.tex -b  -%

SysTable.py -c Rpc3LSS1b -w results/Mc15SusyTest_nom_TablesBgOnly_Rpc3LSS1b_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/BeforeFit_Syst_BkgOnly_Rpc3LSS1b.tex -b -%

SysTable.py -c VRttV -w results/Mc15SusyTest_nom_TablesBgOnly_VRttV_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/BeforeFit_Syst_BkgOnly_VRttV.tex -b -%

SysTable.py -c VRWZ4j -w results/Mc15SusyTest_nom_TablesBgOnly_VRWZ4j_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/BeforeFit_Syst_BkgOnly_VRWZ4j.tex -b -%

SysTable.py -c VRWZ5j -w results/Mc15SusyTest_nom_TablesBgOnly_VRWZ5j_winter2019SameSign/Mc15SusyTest_bkgOnly_combined_NormalMeasurement_model_afterFit.root -o Tables/BeforeFit_Syst_BkgOnly_VRWZ5j.tex -b  -%
