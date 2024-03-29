
import FWCore.GuiBrowsers.ParameterSet_patch  

# This is an example PAT configuration showing the usage of PAT on fast sim samples

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# load the standard PAT config
process.load("PhysicsTools.PatAlgos.patSequences_cff")

# use a fastsim file as input
process.source.filenames = fileNames = cms.untracked.vstring('/store/relval/CMSSW_3_1_0_pre10/RelValQCD_FlatPt_15_3000/GEN-SIM-DIGI-RECO/IDEAL_31X_FastSim_v1/0008/D65E768E-CF57-DE11-B64F-001D09F23D1D.root')

# let it run
process.p = cms.Path(
        process.patDefaultSequence
    )


# In addition you usually want to change the following parameters:
#
#   process.GlobalTag.globaltag =  ...      (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#   process.source.fileNames = [ ... ]      (e.g. 'file:AOD.root')
#   process.maxEvents.input = ...           (e.g. -1 to run on all events)
#   process.out.outputCommands = [ ... ]    (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#   process.out.fileName = ...              (e.g. 'myTuple.root')
#   process.options.wantSummary = False     (to suppress the long output at the end of the job)




