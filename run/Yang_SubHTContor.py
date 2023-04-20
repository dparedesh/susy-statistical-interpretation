import os,sys,subprocess
import itertools
SR2L_list = ["Rpc2LS0BR","Rpc2LS25BR","Rpc2LS50BR","Rpc2LH0BR","Rpc2LH25BR","Rpc2LH50BR","Rpc2LD75BR","Rpc2LD100BR"]
SR3L_list = ["Rpc3LS0BR","Rpc3LS25BR","Rpc3LS50BR","Rpc3LH0BR","Rpc3LH25BR","Rpc3LH50BR","Rpc3LH75BR","Rpc3LH100BR"]
SR4L_list = ["Rpc4LS0BR","Rpc4LS25BR","Rpc4LS50BR","Rpc4LS75BR","Rpc4LS100BR","Rpc4LH25BR","Rpc4LH50BR","Rpc4LM75BR","Rpc4LM100BR","Rpc4LHF75BR","Rpc4LHF100BR","Rpc4LHS75BR","Rpc4LHS100BR"]

combi_SR = list(itertools.product(SR2L_list,SR3L_list,SR4L_list))

for SR in combi_SR:
    SR_name = ''
    isTarget = True
    tag = int(SR[0][SR[0].find('Rpc')+6:SR[0].find('BR')])
    for itr in range(len(SR)):
        if "2LD" in SR[itr]: continue
        if itr != len(SR) - 1:
            SR_name = SR_name + SR[itr] + ','
        else:
            SR_name = SR_name + SR[itr]
        if itr>0:
            if tag >0:
                if str(tag) not in SR[itr]: isTarget = False
            else:
                if not ('S0BR' in SR[itr] or 'H0BR' in SR[itr]): isTarget = False

    if not isTarget: continue
    with open("Tem_Command.sh",'w+') as outfile:
        #outfile.write('python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR {0} --Model Mc16SusyC1N2N1_GGMHinoZh --SigNameSchema SP:4,LSP:5 --WithSigMass --extra syst:HTCondor,queue:8nh,storage:2000 --batch'.format(SR_name))
        #outfile.write('python ../python/generateCommands.py --merge --drawCLs --doBlind ALL --fitmodel excl --SR {0} --Model Mc16SusyC1N2N1_GGMHinoZh --SigNameSchema SP:4,LSP:5 --WithSigMass'.format(SR_name))
        outfile.write('python ../python/generateCommands.py --plot --drawCLs --extraHarvestToContours " --xMin 200 --xMax 900 --yMin 0 --yMax 100" --doBlind ALL --fitmodel excl --SR {0} --Model Mc16SusyC1N2N1_GGMHinoZh --SigNameSchema SP:4,LSP:5 --WithSigMass'.format(SR_name))

        outfile.close()


    out = open('tem_2021.sh','w+')
    with open('Job_HF_2021.sh','r') as infile:
        for line in infile.readlines():
            if line.startswith('python ../python/generateCommands.py'):
                out.write('python ../python/generateCommands.py --fit --doBlind ALL --fitmodel excl --SR {0} --Model Mc16SusyC1N2N1_GGMHinoZh --SigNameSchema SP:4,LSP:5 --WithSigMass EXTRAOPTION'.format(SR_name))
            else:
                out.write(line)
        infile.close()

    out.close()
    print("Submitting: {0}".format(SR_name))
    subprocess.call('mv tem_2021.sh Job_HF_2021.sh',shell=True)
    subprocess.call('chmod +x Job_HF_2021.sh',shell=True)
    subprocess.call('bash ./Tem_Command.sh',shell=True)
#    subprocess.call('cat ./Tem_Command.sh',shell=True)
