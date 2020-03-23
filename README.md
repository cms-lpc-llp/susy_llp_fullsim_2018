# susy_llp_fullsim_2018
2018 Autumn18 SUSY LLP Fullsim signal generation

# PPD RunII guideline
https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVAnalysisSummaryTable

Take 2018 condition.

# Setup

```
export SCRAM_ARCH=slc6_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW CMSSW_10_2_11
cd CMSSW_10_2_11/src
eval `scram runtime -sh`

mkdir -p Configuration/GenProduction/python/
```

# step 0: LHE, GEN, SIM
```
seed=$(($(date +%s) % 100 + 1))

cmsDriver.py Configuration/GenProduction/python/Fullsim_TChiHH_fragment_LLP_ctau.py --fileout file:Fullsim_TChiHH_200_pl1000_step0.root --mc --eventcontent RAWSIM,LHE --datatier GEN-SIM,LHE --conditions 102X_upgrade2018_realistic_v20 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN,SIM --geometry DB:Extended --era Run2_2018 --python_filename Fullsim_TChiHH_200_pl1000_step0_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${seed})" -n 10

cmsRun Fullsim_TChiHH_200_pl1000_step0_cfg.py
```
#step 1: DIGI
```
cmsDriver.py step1 --fileout file:Fullsim_TChiHH_200_pl1000_step1.root --pileup_input dbs:/Neutrino_E-10_gun/RunIISummer17PrePremix-PUAutumn18_102X_upgrade2018_realistic_v15-v1/GEN-SIM-DIGI-RAW --mc --eventcontent PREMIXRAW --datatier GEN-SIM-RAW --conditions 102X_upgrade2018_realistic_v20 --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:@relval2018 --procModifiers premix_stage2 --nThreads 8 --geometry DB:Extended --datamix PreMix --era Run2_2018 --python_filename Fullsim_TChiHH_200_pl1000_step1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 10

cp Fullsim_TChiHH_200_pl1000_step0.root step1_SIM.root
cmsRun Fullsim_TChiHH_200_pl1000_step1_cfg.py
```
#Step 2: RECO --> AODSIM
```
cmsDriver.py step2 --filein file:Fullsim_TChiHH_200_pl1000_step1.root --fileout file:Fullsim_TChiHH_200_pl1000_step2.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 102X_upgrade2018_realistic_v20 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --procModifiers premix_stage2 --nThreads 8 --era Run2_2018 --python_filename Fullsim_TChiHH_200_pl1000_step2_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 10

cmsRun Fullsim_TChiHH_200_pl1000_step2_cfg.py
```
