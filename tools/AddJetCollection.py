#import FWCore.ParameterSet.Config as cms
import copy
from PhysicsTools.PatAlgos.tools.helpers import *
from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
from PhysicsTools.PatAlgos.tools.RunBTagging import *
        
class AddJetCollection(ConfigToolBase):

    """ Add a collection of PAT Jets
    """
    _label='AddJetCollection'

    #def __init__(self):
     #   self._parameters={}
      #  self._label='AddJetCollection'
       # self._description=self.__doc__    
        
    def dumpPython(self):
        
        ## The string will be changed, because the import must not change:
        
        dumpPython = "\nfrom PhysicsTools.PatAlgos.tools.AddJetCollection import *\n\naddJetCollection(process, "
        dumpPython += str(self.getvalue('jetCollection'))+ ", "
        dumpPython += str(self.getvalue('postfixLabel'))+', '
        dumpPython += str(self.getvalue('doJTA'))+', '
        dumpPython += str(self.getvalue('doBTagging'))+', '
        dumpPython += str(self.getvalue('jetCorrLabel'))+', '
        dumpPython += str(self.getvalue('doType1MET'))+', '
        dumpPython += str(self.getvalue('doL1Counters'))+', '
        dumpPython += str(self.getvalue('genJetCollection'))+'\n'
        return dumpPython
        
    def __call__(self, process,
                 jetCollection=cms.InputTag('sisCone5CaloJets'),
                 label='SCS',
                 doJTA=True,
                 doBTagging=True,
                 jetCorrLabel=None,
                 doType1MET=True,
                 doL1Cleaning = True,
                 doL1Counters = False,
                 genJetCollection = cms.InputTag('sisCone5CaloJets')): 


        self.addParameter('process',process, 'description: process')
        self.addParameter('jetCollection',jetCollection, 'description: InputTag')
        self.addParameter('postfixLabel',label, 'description: label')
        self.addParameter('doJTA',doJTA, 'description: doJTA')
        self.addParameter('doBTagging',doBTagging, 'description: doBTagging')
        self.addParameter('jetCorrLabel',jetCorrLabel, 'description: jetCorrLabel')
        self.addParameter('doType1MET',doType1MET, 'description: doType1MET')
        self.addParameter('doL1Cleaning',doL1Cleaning, 'description: doL1Cleaning')
        self.addParameter('doL1Counters',doL1Counters, 'description: doL1Counters')
        self.addParameter('genJetCollection',genJetCollection, 'description: genJetCollection')

        process = self._parameters['process'].value
        jetCollection = self._parameters['jetCollection'].value
        postfixLabel = self._parameters['postfixLabel'].value
        doJTA = self._parameters['doJTA'].value
        doBTagging =self._parameters['doBTagging'].value
        jetCorrLabel = self._parameters['jetCorrLabel'].value
        doType1MET = self._parameters['doType1MET'].value
        doL1Cleaning = self._parameters['doL1Cleaning'].value
        doL1Counters = self._parameters['doL1Counters'].value
        genJetCollection = self._parameters['genJetCollection'].value            
        
        action = Action("AddJetCollection",copy.copy(self._parameters),self) 
        self.getvalue('process').addAction(action)
        
        #def addJetCollection(process,jetCollection,postfixLabel,
        #               doJTA=True,doBTagging=True,jetCorrLabel=None,doType1MET=True,doL1Counters=False,
        #              genJetCollection=cms.InputTag("iterativeCone5GenJets")):
        """Add a new collection of jets in PAT from the default value.
              postfixLabel: Postpone this label to the name of all modules that work with these jet collection.
                            it can't be an empty string
              doBTagging  : True to run the BTagging sequence on top of this jets, and import it into PAT.
              doJTA       : Run Jet Tracks Association and Jet Charge (will be forced to True if doBTagging is true)
              jetCorrLabel: Name of the algorithm and jet type JEC to pick corrections from, or None for no JEC 
                            Examples are ('IC5','Calo'), ('SC7','Calo'), ('KT4','PF')OB
                            It tries to find a 'L2L3JetCorrector' + algo + type , or otherwise to create if as a 
                            JetCorrectionServiceChain of 'L2RelativeJetCorrector' and 'L3AbsoluteJetCorrector'
              doType1MET  : Make also a new MET (NOT IMPLEMENTED)
              doL1Counters: copy also the filter modules that accept/reject the event looking at the number of jets
              genJetCollection : GenJet collection to match to.

            Note: This takes the configuration from the already-configured jets, so if you do 
                  replaces before calling addJetCollection then they will affect also the new jets
        """
        def addAlso (label,value):
            existing = getattr(process, label)
            setattr( process, label + postfixLabel, value)
            process.patDefaultSequence.replace( existing, existing * value )
        def addClone(label,**replaceStatements):
            new      = getattr(process, label).clone(**replaceStatements)
            addAlso(label, new)
        addClone('allLayer1Jets', jetSource = jetCollection)
        l1Jets = getattr(process, 'allLayer1Jets'+postfixLabel)
        addClone('selectedLayer1Jets', src=cms.InputTag('allLayer1Jets'+postfixLabel))
        addClone('cleanLayer1Jets', src=cms.InputTag('selectedLayer1Jets'+postfixLabel))
        if doL1Counters:
            addClone('countLayer1Jets', src=cms.InputTag('cleanLayer1Jets'+postfixLabel))
        addClone('jetPartonMatch',       src = jetCollection)
        addClone('jetGenJetMatch',       src = jetCollection)
        addClone('jetPartonAssociation', jets = jetCollection)
        addClone('jetFlavourAssociation',srcByReference = cms.InputTag('jetPartonAssociation' + postfixLabel))
        def fixInputTag(x): x.setModuleLabel(x.moduleLabel+postfixLabel)
        def fixVInputTag(x): x[0].setModuleLabel(x[0].moduleLabel+postfixLabel)
        fixInputTag(l1Jets.JetPartonMapSource)
        fixInputTag(l1Jets.genJetMatch)
        fixInputTag(l1Jets.genPartonMatch)
        def vit(*args) : return cms.VInputTag( *[ cms.InputTag(x) for x in args ] )
        if doBTagging :
            (btagSeq, btagLabels) = runBTagging(process,jetCollection,postfixLabel) 
            process.patAODCoreReco += btagSeq  # must add to Core, as it's needed by Extra
            addClone('patJetCharge', src=cms.InputTag(btagLabels['jta']))
            l1Jets.trackAssociationSource = cms.InputTag(btagLabels['jta'])
            l1Jets.tagInfoSources         = cms.VInputTag( *[ cms.InputTag(x) for x in btagLabels['tagInfos'] ] )
            l1Jets.discriminatorSources   = cms.VInputTag( *[ cms.InputTag(x) for x in btagLabels['jetTags']  ] )
            fixInputTag(l1Jets.jetChargeSource)
        else:
            l1Jets.addBTagInfo = False 
        if doJTA or doBTagging:
            if not doBTagging:
                process.load("RecoJets.JetAssociationProducers.ic5JetTracksAssociatorAtVertex_cfi")
                from RecoJets.JetAssociationProducers.ic5JetTracksAssociatorAtVertex_cfi import ic5JetTracksAssociatorAtVertex
                jtaLabel = 'jetTracksAssociatorAtVertex' + postfixLabel
                setattr( process, jtaLabel, ic5JetTracksAssociatorAtVertex.clone(jets = jetCollection) )
                process.patAODReco.replace(process.patJetTracksCharge, getattr(process,jtaLabel) + process.patJetTracksCharge)
                l1Jets.trackAssociationSource = cms.InputTag(jtaLabel)
                addClone('patJetCharge', src=cms.InputTag(jtaLabel)),
                fixInputTag(l1Jets.jetChargeSource)
        else: ## no JTA
            l1Jets.addAssociatedTracks = False
            l1Jets.addJetCharge = False
        if jetCorrLabel != None:
            if jetCorrLabel == False : raise ValueError, "In addJetCollection 'jetCorrLabel' must be set to None, not False"
            if jetCorrLabel == "None": raise ValueError, "In addJetCollection 'jetCorrLabel' must be set to None (without quotes), not 'None'"
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
            addClone('jetCorrFactors',       jetSource           = jetCollection) 
            switchJECParameters( getattr(process,'jetCorrFactors'+postfixLabel), jetCorrLabel[0], jetCorrLabel[1], oldalgo='IC5',oldtype='Calo' )
            fixVInputTag(l1Jets.jetCorrFactorsSource)
            if doType1MET:
                addClone('metJESCorIC5CaloJet', inputUncorJetsLabel = jetCollection.value(),
                         corrector = cms.string('L2L3JetCorrector%s%s' % jetCorrLabel))
                addClone('metJESCorIC5CaloJetMuons', uncorMETInputTag = cms.InputTag("metJESCorIC5CaloJet"+postfixLabel))
                addClone('layer1METs',              metSource = cms.InputTag("metJESCorIC5CaloJetMuons"+postfixLabel))
                l1MET = getattr(process, 'layer1METs'+postfixLabel)
                process.allLayer1Summary.candidates += [ cms.InputTag('layer1METs'+postfixLabel) ]
        else:
            l1Jets.addJetCorrFactors = False
        ## Add this to the summary tables (not strictly needed, but useful)
        if jetCollection not in process.aodSummary.candidates: 
            process.aodSummary.candidates += [ jetCollection ]
        process.allLayer1Summary.candidates      += [ cms.InputTag('allLayer1Jets'+postfixLabel) ]
        process.selectedLayer1Summary.candidates += [ cms.InputTag('selectedLayer1Jets'+postfixLabel) ]




addJetCollection=AddJetCollection()
