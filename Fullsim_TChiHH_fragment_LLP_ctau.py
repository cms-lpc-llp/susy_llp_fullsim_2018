import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

import math
baseSLHATable="""
BLOCK MASS  # Mass Spectrum
# PDG code           mass       particle
   1000001     1.00000000E+05   # ~d_L
   2000001     1.00000000E+05   # ~d_R
   1000002     1.00000000E+05   # ~u_L
   2000002     1.00000000E+05   # ~u_R
   1000003     1.00000000E+05   # ~s_L
   2000003     1.00000000E+05   # ~s_R
   1000004     1.00000000E+05   # ~c_L
   2000004     1.00000000E+05   # ~c_R
   1000005     1.00000000E+05   # ~b_1
   2000005     1.00000000E+05   # ~b_2
   1000006     1.00000000E+05   # ~t_1
   2000006     1.00000000E+05   # ~t_2
   1000011     1.00000000E+05   # ~e_L
   2000011     1.00000000E+05   # ~e_R
   1000012     1.00000000E+05   # ~nu_eL
   1000013     1.00000000E+05   # ~mu_L
   2000013     1.00000000E+05   # ~mu_R
   1000014     1.00000000E+05   # ~nu_muL
   1000015     1.00000000E+05   # ~tau_1
   2000015     1.00000000E+05   # ~tau_2
   1000016     1.00000000E+05   # ~nu_tauL
   1000021     1.00000000E+05   # ~g
   1000022     1.00000000E+00   # ~chi_10
   1000023     %MCHI%           # ~chi_20
   1000025     %MCHI%           # ~chi_30
   1000035     1.00000000E+05   # ~chi_40
   1000024     1.00000000E+05   # ~chi_1+
   1000037     1.00000000E+05   # ~chi_2+
   1000039     1.00000000E+05   # ~gravitino

# DECAY TABLE
#         PDG            Width
DECAY   1000001     0.00000000E+00   # sdown_L decays
DECAY   2000001     0.00000000E+00   # sdown_R decays
DECAY   1000002     0.00000000E+00   # sup_L decays
DECAY   2000002     0.00000000E+00   # sup_R decays
DECAY   1000003     0.00000000E+00   # sstrange_L decays
DECAY   2000003     0.00000000E+00   # sstrange_R decays
DECAY   1000004     0.00000000E+00   # scharm_L decays
DECAY   2000004     0.00000000E+00   # scharm_R decays
DECAY   1000005     0.00000000E+00   # sbottom1 decays
DECAY   2000005     0.00000000E+00   # sbottom2 decays
DECAY   1000006     0.00000000E+00   # stop1 decays
DECAY   2000006     0.00000000E+00   # stop2 decays
DECAY   1000011     0.00000000E+00   # selectron_L decays
DECAY   2000011     0.00000000E+00   # selectron_R decays
DECAY   1000012     0.00000000E+00   # snu_elL decays
DECAY   1000013     0.00000000E+00   # smuon_L decays
DECAY   2000013     0.00000000E+00   # smuon_R decays
DECAY   1000014     0.00000000E+00   # snu_muL decays
DECAY   1000015     0.00000000E+00   # stau_1 decays
DECAY   2000015     0.00000000E+00   # stau_2 decays
DECAY   1000016     0.00000000E+00   # snu_tauL decays
DECAY   1000021     0.00000000E+00   # gluino decays
DECAY   1000022     0.00000000E+00   # neutralino1 decays
DECAY   1000023     %CTAU%   # neutralino2 decays
    0.00000000E+00   3    1000022   5   -5  #dummy decay
    1.00000000E+00   2    1000022   25
DECAY   1000024     0.00000000E+00   # chargino1+ decays
DECAY   1000025     %CTAU%   # neutralino3 decays
    0.00000000E+00   3    1000022   5   -5  #dummy decay
    1.00000000E+00   2    1000022   25
DECAY   1000035     0.00000000E+00   # neutralino4 decays
DECAY   1000037     0.00000000E+00   # chargino2+ decays
"""
def matchParams(mass):
  if mass < 199: return 76,0.52
  elif mass<299: return 76,0.524
  elif mass<399: return 76,0.492
  elif mass<499: return 76,0.464
  elif mass<599: return 76,0.451
  elif mass<699: return 76,0.437
  elif mass<799: return 76,0.425
  elif mass<899: return 76,0.413
  elif mass<999: return 76,0.402
  elif mass<1099: return 76,0.40
  else: return 76,0.4

# weighted average of matching efficiencies for the full scan
# must equal the number entered in McM generator params
mcm_eff = 0.455

model = "TChiHH_HToBB_HToBB"
process = "N2N3"
    
hBarCinGeVmm = 1.973269788e-13

mchi=200
ctau0 = 1000
ctau = hBarCinGeVmm / ctau0
print mchi, ctau0, ctau

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args =  cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.4.2/sus_sms/LO_PDF/SMS-%s/v1/SMS-%s_mN-%i_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz' % (process,process,mchi)),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

qcut, tru_eff = matchParams(mchi)
slhatable = baseSLHATable.replace('%MCHI%','%e' % mchi)
slhatable = slhatable.replace('%CTAU%','%e' % ctau)

basePythiaParameters = cms.PSet(
    pythia8CommonSettingsBlock,
    pythia8CP5SettingsBlock,
    JetMatchingParameters = cms.vstring(
        'JetMatching:setMad = off',
        'JetMatching:scheme = 1',
        'JetMatching:merge = on',
        'JetMatching:jetAlgorithm = 2',
        'JetMatching:etaJetMax = 5.',
        'JetMatching:coneRadius = 1.',
        'JetMatching:slowJetPower = 1',
        'JetMatching:qCut = %.0f' % qcut, #this is the actual merging scale
        'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
        'JetMatching:nJetMax = 2', #number of partons in born matrix element for highest multiplicity
        'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
        '6:m0 = 172.5',
        '25:onMode = off',
        '25:onIfMatch = 5 -5',
	'Check:abortIfVeto = on',
        '25:doForceWidth = true',
        '25:mWidth = 2.0',
        '25:mMin = 30.0',
        '25:m0 = 125.0',
    ), 
    parameterSets = cms.vstring('pythia8CommonSettings',
			        'pythia8CP5Settings',
                                'JetMatchingParameters'
    )
)

particleList = [1000023, 1000025]
for p in particleList:
   basePythiaParameters.pythia8CommonSettings.extend([str(p)+':tau0 = %e' % ctau0])
basePythiaParameters.pythia8CommonSettings.extend(['ParticleDecays:tau0Max = 1000.1'])
basePythiaParameters.pythia8CommonSettings.extend(['LesHouches:setLifetime = 2'])
basePythiaParameters.pythia8CommonSettings.extend(['RHadrons:allow = on'])

generator = cms.EDFilter("Pythia8HadronizerFilter",
  maxEventsToPrint = cms.untracked.int32(1),
  pythiaPylistVerbosity = cms.untracked.int32(1),
  filterEfficiency = cms.untracked.double(1.0),
  pythiaHepMCVerbosity = cms.untracked.bool(False),
  comEnergy = cms.double(13000.),
  ConfigDescription = cms.string('%s_%i_%i' % (model, mchi,ctau0)),
  SLHATableForPythia8 = cms.string('%s' % slhatable),
  PythiaParameters = basePythiaParameters,
)
