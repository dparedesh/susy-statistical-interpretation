unset PYTHONPATH
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
alias setupATLAS='source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh'
export RUCIO_ACCOUNT=$USER
setupATLAS
#
#
#lsetup "views LCG_94 x86_64-centos7-gcc62-opt"
#
#lsetup 'root 6.18.04-x86_64-centos7-gcc8-opt'

lsetup "asetup 21.2.120,AnalysisBase" # able to use root 6.18, also suitable to use AnlysisBase as base software env

cd ./HistFitter/
. ./setup.sh
cd ./src/

make clean

make

cd ../../

TopDirectory=`pwd`

mkdir -p $TopDirectory/HistFitterUser
mkdir -p $TopDirectory/HistFitter/InputTrees

export PYTHONPATH=$TopDirectory/python:$PYTHONPATH
export HFRUNDIR=$TopDirectory/HistFitter
