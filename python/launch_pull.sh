

mkdir -p PullPlots/

python scripts/new_pull_maker.py -i Logs/SR_Rpc2L0b.log -o pull_Rpc2L0b

python scripts/new_pull_maker.py -i Logs/SR_Rpc2L1b.log -o pull_Rpc2L1b

python scripts/new_pull_maker.py -i Logs/SR_Rpc2L2b.log -o pull_Rpc2L2b

python scripts/new_pull_maker.py -i Logs/SR_Rpc3LSS1b.log -o pull_Rpc3LSS1b

python scripts/new_pull_maker.py -i Logs/SR_Rpv2L.log -o pull_Rpv2L

python scripts/new_pull_maker.py -i Logs/VRttV.log -o pull_VRttV

python scripts/new_pull_maker.py -i Logs/VRWZ4j.log -o pull_VRWZ4j

python scripts/new_pull_maker.py -i Logs/VRWZ5j.log -o pull_VRWZ5j

mv pull_* PullPlots/
