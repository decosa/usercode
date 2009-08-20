
import copy
from PhysicsTools.PatAlgos.tools.helpers import *
from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
from PhysicsTools.PatAlgos.tools.AddJetCollection import *
from PhysicsTools.PatAlgos.tools.RunBTagging import *
        
class SwitchJetCollection(ConfigToolBase):

    """Switch the collection of jets in PAT from the default value.
       doBTagging  : True to run the BTagging sequence on top of this jets, and import it into PAT.
       doJTA       : Run Jet Tracks Association and Jet Charge (will be forced to True if doBTagging is true)
       jetCorrLabel: Name of the algorithm and jet type JEC to pick corrections from, or None for no JEC
                     Examples are ('IC5','Calo'), ('SC7','Calo'), ('KT4','PF')
                     It tries to find a 'L2L3JetCorrector' + algo + type , or otherwise to create if as a
                     JetCorrectionServiceChain of 'L2RelativeJetCorrector' and 'L3AbsoluteJetCorrector'
       doType1MET  : If jetCorrLabel is not 'None', set this to 'True' to remake Type1 MET from these jets
                     NOTE: at the moment it must be False for non-CaloJets otherwise the JetMET POG module crashes.
       genJetCollection : GenJet collection to match to."""
    
    _label='SwitchJetCollection'
    
            
    def dumpPython(self):

        dumpPython= "\nfrom PhysicsTools.PatAlgos.tools.SwitchJetCollection import *\n\nswitchJetCollection(process, "
        dumpPython += str(self.getvalue('jetCollection'))+', '
        dumpPython += str(self.getvalue('doJTA'))+', '
        dumpPython += str(self.getvalue('doBTagging'))+', '
        dumpPython += str(self.getvalue('jetCorrLabel'))+', '
        dumpPython += str(self.getvalue('doType1MET'))+', '
        dumpPython += str(self.getvalue('genJetCollection'))+'\n'
        return dumpPython
        #infile=open('PATconfigfile.py','r')
        #text=infile.read()
        #infile.close()
        #print text


    def __call__(self, process,
                 jetCollection,
                 doJTA            = True,
                 doBTagging       = True,
                 jetCorrLabel     = None,
                 doType1MET       = True,
                 genJetCollection = cms.InputTag("iterativeCone5GenJets")):

        self.addParameter('process',process, 'description: process')
        self.addParameter('jetCollection',jetCollection, 'description: InputTag')
        self.addParameter('doJTA',doJTA, 'description: doJTA')
        self.addParameter('doBTagging',doBTagging, 'description: doBTagging')
        self.addParameter('jetCorrLabel',jetCorrLabel, 'description: jetCorrLabel')
        self.addParameter('doType1MET',doType1MET, 'description: doType1MET')
        self.addParameter('genJetCollection',genJetCollection, 'description: genJetCollection')


        process=self._parameters['process'].value
        oldLabel = process.allLayer1Jets.jetSource;
        jetCollection = self._parameters['jetCollection'].value
        doJTA = self._parameters['doJTA'].value
        doBTagging =self._parameters['doBTagging'].value
        jetCorrLabel = self._parameters['jetCorrLabel'].value
        doType1MET = self._parameters['doType1MET'].value
        genJetCollection = self._parameters['genJetCollection'].value
        process.jetPartonMatch.src        = jetCollection
        process.jetGenJetMatch.src        = jetCollection
        process.jetGenJetMatch.match      = genJetCollection
        process.jetPartonAssociation.jets = jetCollection
        process.allLayer1Jets.jetSource = jetCollection


        # quickly make VInputTag from strings
        def vit(*args) : return cms.VInputTag( *[ cms.InputTag(x) for x in args ] )
        if doBTagging :
            (btagSeq, btagLabels) = runBTagging(process, jetCollection, 'AOD')
            process.patAODCoreReco += btagSeq # must add to Core, as it's needed by ExtraReco
            process.patJetCharge.src                     = btagLabels['jta']
            process.allLayer1Jets.trackAssociationSource = btagLabels['jta']
            process.allLayer1Jets.tagInfoSources       = cms.VInputTag( *[ cms.InputTag(x) for x in btagLabels['tagInfos'] ] )
            process.allLayer1Jets.discriminatorSources = cms.VInputTag( *[ cms.InputTag(x) for x in btagLabels['jetTags']  ] )
        else:
            process.patAODReco.remove(process.patBTagging)
            process.allLayer1Jets.addBTagInfo = False
        if doJTA or doBTagging:
            if not doBTagging:
                process.load("RecoJets.JetAssociationProducers.ic5JetTracksAssociatorAtVertex_cfi")
                from RecoJets.JetAssociationProducers.ic5JetTracksAssociatorAtVertex_cfi import ic5JetTracksAssociatorAtVertex
                process.jetTracksAssociatorAtVertex = ic5JetTracksAssociatorAtVertex.clone(jets = jetCollection)
                process.patAODReco.replace(process.patJetTracksCharge, process.jetTracksAssociatorAtVertex + process.patJetTracksCharge)
                process.patJetCharge.src                     = 'jetTracksAssociatorAtVertex'
                process.allLayer1Jets.trackAssociationSource = 'jetTracksAssociatorAtVertex'
        else: ## no JTA
            process.patAODReco.remove(process.patJetTracksCharge)
            process.allLayer1Jets.addAssociatedTracks = False
            process.allLayer1Jets.addJetCharge = False
        if jetCorrLabel != None:
            if jetCorrLabel == False : raise ValueError, "In switchJetCollection 'jetCorrLabel' must be set to None, not False"
            if jetCorrLabel == "None": raise ValueError, "In switchJetCollection 'jetCorrLabel' must be set to None (without quotes), not 'None'"
            if type(jetCorrLabel) != type(('IC5','Calo')):
                raise ValueError, "In switchJetCollection 'jetCorrLabel' must be None, or a tuple ('Algo', 'Type')"
            if not hasattr( process, 'L2L3JetCorrector%s%s' % jetCorrLabel ):
                setattr( process,
                         'L2L3JetCorrector%s%s' % jetCorrLabel,
                         cms.ESSource("JetCorrectionServiceChain",
                                      correctors = cms.vstring('L2RelativeJetCorrector%s%s' % jetCorrLabel,
                                                               'L3AbsoluteJetCorrector%s%s' % jetCorrLabel),
                                      label      = cms.string('L2L3JetCorrector%s%s' % jetCorrLabel)
                                      )
                         )
            switchJECParameters(process.jetCorrFactors, jetCorrLabel[0], jetCorrLabel[1], oldalgo='IC5',oldtype='Calo')
            process.jetCorrFactors.jetSource = jetCollection
            if doType1MET:
                process.metJESCorIC5CaloJet.inputUncorJetsLabel = jetCollection.value() # FIXME it's metJESCorIC5CaloJet that's broken
                process.metJESCorIC5CaloJet.corrector           = 'L2L3JetCorrector%s%s' % jetCorrLabel
        else:
            process.patJetMETCorrections.remove(process.jetCorrFactors)
            process.allLayer1Jets.addJetCorrFactors = False
            ## Add this to the summary tables (not strictly needed, but useful)
        if oldLabel in process.aodSummary.candidates:
            process.aodSummary.candidates[process.aodSummary.candidates.index(oldLabel)] = jetCollection
        else:
            process.aodSummary.candidates += [jetCollection]
                                                                                
        action = Action("switchJetCollection",copy.copy(self._parameters),self)
        process.addAction(action)
        
switchJetCollection=SwitchJetCollection()
