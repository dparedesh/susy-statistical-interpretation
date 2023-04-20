#!/bin/bash

JobNameCR=Mc16SusySS2StepSL_Nominal_FullRun2_STRG_binned_WZNF_138965_ALL_THFLAT30_CRWZ2j_excl_Job

#JobNameSR=Mc16SusySS2StepSL_Nominal_FullRun2_STRG_binned_WZNF_138965_ALL_THFLAT30_RpcSSslep1excl_blindALL_excl_Job
#JobNameCRSR=Mc16SusySS2StepSL_Nominal_FullRun2_STRG_binned_WZNF_138965_ALL_THFLAT30_RpcSSslep1excl_CRWZ2j_blindSR_excl_Job

#JobNameSR=Mc16SusySS2StepSL_Nominal_FullRun2_STRG_binned_WZNF_138965_ALL_THFLAT30_RpcSSslep2_blindALL_excl_Job
#JobNameCRSR=Mc16SusySS2StepSL_Nominal_FullRun2_STRG_binned_WZNF_138965_ALL_THFLAT30_RpcSSslep2_CRWZ2j_blindSR_excl_Job

#JobNameSR=Mc16SusySS2StepSL_Nominal_FullRun2_STRG_binned_WZNF_138965_ALL_THFLAT30_RpcSSslep3_blindALL_excl_Job
#JobNameCRSR=Mc16SusySS2StepSL_Nominal_FullRun2_STRG_binned_WZNF_138965_ALL_THFLAT30_RpcSSslep3_CRWZ2j_blindSR_excl_Job

JobNameSR=Mc16SusySS2StepSL_Nominal_FullRun2_STRG_binned_WZNF_138965_ALL_THFLAT30_RpcSSslep4_blindALL_excl_Job
JobNameCRSR=Mc16SusySS2StepSL_Nominal_FullRun2_STRG_binned_WZNF_138965_ALL_THFLAT30_RpcSSslep4_CRWZ2j_blindSR_excl_Job

nJob=130

cacheDIR=$HISTFITTER/data


n=0
zero=0
while [ $n -ne 10 ]
do
#    echo "$n"
    rm -rf ${cacheDIR}/${JobNameCRSR}${zero}${n}.root
    echo "--- Running: hadd ${cacheDIR}/${JobNameCRSR}${zero}${n}.root ${cacheDIR}/${JobNameSR}${zero}${n}.root ${cacheDIR}/${JobNameCR}${zero}${n}.root" 
    hadd ${cacheDIR}/${JobNameCRSR}${zero}${n}.root ${cacheDIR}/${JobNameSR}${zero}${n}.root ${cacheDIR}/${JobNameCR}${zero}${n}.root
    n=$(($n+1))
done

i=10
while [ $i -ne ${nJob} ]
do
    #echo "$i"
    rm -rf ${cacheDIR}/${JobNameCRSR}${i}.root
    echo "--- Running: hadd ${cacheDIR}/${JobNameCRSR}${i}.root ${cacheDIR}/${JobNameSR}${i}.root ${cacheDIR}/${JobNameCR}${i}.root" 
    hadd ${cacheDIR}/${JobNameCRSR}${i}.root ${cacheDIR}/${JobNameSR}${i}.root ${cacheDIR}/${JobNameCR}${i}.root
    i=$(($i+1))
done

