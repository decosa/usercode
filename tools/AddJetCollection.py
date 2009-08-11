import FWCore.ParameterSet.Config as cms

import copy

from PhysicsTools.PatAlgos.tools.helpers import *

from PhysicsTools.PatAlgos.tools.ConfigToolBase import *


class Action(object):

    def __init__(self,label,parameters,referenceToFunctor):

        self.label=label
        self.parameters=parameters
        self.referenceToFunctor=referenceToFunctor
        
        
class AddJetCollection(ConfigToolBase):

    """ Add a collection of PAT Jets
    """
    
    description="class description "
    
    #class parameter:
        #pass
        
    def __init__(self):
        self.parameters={}
        self._label='AddJetCollection'
        self._description=self.__doc__    

        
#    def dumpPython(self):
 #       outfile=open('PATconfigfile.py','a')
  #      outfile.write("from PhysicsTools.PatAlgos.tools.AddJetCollection import *\n addJetCollection(process, "+str(cms.InputTag('sisCone5CaloJets'))+ ", "+str(self.getvalue('label'))+', '+str(self.getvalue('doJTA'))+', '+str(self.getvalue('doBTagging'))+', '+str(self.getvalue('jetCorrLabel'))+', '+str(self.getvalue(' doType1MET'))+', '+str(self.getvalue('doL1Counters'))+', '+str(self.getvalue('genJetCollection'))+'\n')
   #     outfile.close()
    #    infile=open('PATconfigfile.py','r')
     #   text=infile.read()
     #   infile.close()
     #   print text
        
        
    def addParameter(self,parname, parvalue, description):
        par=self.parameter()
        par.name=parname
        par.value=parvalue
        par.description=description
        par.type=type(parvalue)
        print type(parvalue)
        self.parameters[par.name]=par


    def getvalue(self,name):
        return self.parameters[name].value
        
    def getParameters(self):
        print 'Inside function parameters()'
        for key in self.parameters.keys():
            print key
            print 'par name = '+self.parameters[key].name
            print 'par value = '+str(self.parameters[key].value)
            print 'par type = '+str(self.parameters[key].type)
        return self.parameters

    def setParameter(self, name, value):
        print 'Inside function setParameters()'
        #avoid the loop, use assert as check
        assert(self.parameters.has_key(name))
        self.parameters[name].value=value
        print 'New parameter value ('+name + ') '+str(self.parameters[name].value) 

    def setComment(self, comment):
        outfile=open('PATconfigfile.py','a')
        outfile.write(comment+'\n')
        outfile.close()
        infile=open('PATconfigfile.py','r')
        text=infile.read()
        infile.close()
        print text
                                                
        
    def switchJECParameters(self,jetCorrFactors,newalgo,newtype="Calo",oldalgo="IC5",oldtype="Calo"):
        """Replace input tags in the JetCorrFactorsProducer -- L5Flavor is taken out as it is said not to be dependend on the specific jet algorithm"""
        for k in ['L1Offset', 'L2Relative', 'L3Absolute', 'L4EMF', 'L6UE', 'L7Parton']:
            vv = getattr(jetCorrFactors, k).value();
            if (vv != "none"):
                setattr(jetCorrFactors, k, vv.replace(oldalgo+oldtype,newalgo+newtype).replace(oldalgo,newalgo) )
                # the first replace is good for L2, L3; the last for L7 (which don't have type dependency, at least not in the name)
                                                                                                      
    def runBTagging(self,label):
        """Define a sequence to run BTagging on AOD on top of jet collection 'jetCollection', appending 'label' to module labels.
        The sequence will be called "btaggingAOD" + 'label', and will already be added to the process (but not to any Path)
        The sequence will include a JetTracksAssociatorAtVertex with name "jetTracksAssociatorAtVertex" + 'label'
        The method will return a pair (sequence, labels) where 'sequence' is the cms.Sequence object, and 'labels' contains
        labels["jta"]      = the name of the JetTrackAssociator module
        labels["tagInfos"] = list of names of TagInfo modules
        labels["jetTags "] = list of names of JetTag modules
        these labels are meant to be used for PAT BTagging tools
        NOTE: 'label' MUST NOT BE EMPTY
        """
        if (label == ''):
            raise ValueError, "Label for re-running BTagging can't be empty, it will crash CRAB."
        self.getvalue('process').load("RecoJets.JetAssociationProducers.ic5JetTracksAssociatorAtVertex_cfi")
        self.getvalue('process').load("RecoBTag.Configuration.RecoBTag_cff")
        from RecoJets.JetAssociationProducers.ic5JetTracksAssociatorAtVertex_cfi import ic5JetTracksAssociatorAtVertex
        import RecoBTag.Configuration.RecoBTag_cff as btag
        # quickly make VInputTag from strings
        def vit(*args) : return cms.VInputTag( *[ cms.InputTag(x) for x in args ] )
        
        # define labels
        jtaLabel =  'jetTracksAssociatorAtVertex' + label
        ipTILabel = 'impactParameterTagInfos'     + label
        svTILabel = 'secondaryVertexTagInfos'     + label
        seTILabel = 'softElectronTagInfos'        + label
        smTILabel = 'softMuonTagInfos'            + label
        
        # make JTA and TagInfos
        setattr( self.getvalue('process'), jtaLabel,  ic5JetTracksAssociatorAtVertex.clone(jets = self.getvalue('jetCollection')))
        setattr( self.getvalue('process'), ipTILabel, btag.impactParameterTagInfos.clone(jetTracks = cms.InputTag(jtaLabel)) )
        setattr( self.getvalue('process'), svTILabel, btag.secondaryVertexTagInfos.clone(trackIPTagInfos = cms.InputTag(ipTILabel)) )
        setattr( self.getvalue('process'), seTILabel, btag.softElectronTagInfos.clone(jets = self.getvalue('jetCollection')) )
        setattr( self.getvalue('process'), smTILabel, btag.softMuonTagInfos.clone(jets = self.getvalue('jetCollection')) )
        setattr( self.getvalue('process'), 'jetBProbabilityBJetTags'+label, btag.jetBProbabilityBJetTags.clone(tagInfos = vit(ipTILabel)) )
        setattr( self.getvalue('process'), 'jetProbabilityBJetTags' +label,  btag.jetProbabilityBJetTags.clone(tagInfos = vit(ipTILabel)) )
        setattr( self.getvalue('process'), 'trackCountingHighPurBJetTags'+label, btag.trackCountingHighPurBJetTags.clone(tagInfos = vit(ipTILabel)) )
        setattr( self.getvalue('process'), 'trackCountingHighEffBJetTags'+label, btag.trackCountingHighEffBJetTags.clone(tagInfos = vit(ipTILabel)) )
        setattr( self.getvalue('process'), 'simpleSecondaryVertexBJetTags'+label, btag.simpleSecondaryVertexBJetTags.clone(tagInfos = vit(svTILabel)) )
        setattr( self.getvalue('process'), 'combinedSecondaryVertexBJetTags'+label, btag.combinedSecondaryVertexBJetTags.clone(tagInfos = vit(ipTILabel, svTILabel)) )
        setattr( self.getvalue('process'), 'combinedSecondaryVertexMVABJetTags'+label, btag.combinedSecondaryVertexMVABJetTags.clone(tagInfos = vit(ipTILabel, svTILabel)) )
        setattr( self.getvalue('process'), 'softMuonBJetTags'+label, btag.softMuonBJetTags.clone(tagInfos = vit(smTILabel)) )
        setattr( self.getvalue('process'), 'softMuonByPtBJetTags'+label, btag.softMuonByPtBJetTags.clone(tagInfos = vit(smTILabel)) )
        setattr( self.getvalue('process'), 'softMuonByIP3dBJetTags'+label, btag.softMuonByIP3dBJetTags.clone(tagInfos = vit(smTILabel)) )
        setattr( self.getvalue('process'), 'softElectronByPtBJetTags'+label, btag.softElectronByPtBJetTags.clone(tagInfos = vit(smTILabel)) )
        setattr( self.getvalue('process'), 'softElectronByIP3dBJetTags'+label, btag.softElectronByIP3dBJetTags.clone(tagInfos = vit(smTILabel)) )
        
        def mkseq(process, firstlabel, *otherlabels):
            seq = getattr(self.getvalue('process'), firstlabel)
            for x in otherlabels: seq += getattr(self.getvalue('process'), x)
            return cms.Sequence(seq)
        
        labels = { 'jta' : jtaLabel,
                   'tagInfos' : (ipTILabel,svTILabel,seTILabel,smTILabel),
                   'jetTags'  : [ (x + label) for x in ('jetBProbabilityBJetTags',
                                                        'jetProbabilityBJetTags',
                                                        'trackCountingHighPurBJetTags',
                                                        'trackCountingHighEffBJetTags',
                                                        'simpleSecondaryVertexBJetTags',
                                                        'combinedSecondaryVertexBJetTags',
                                                        'combinedSecondaryVertexMVABJetTags',
                                                        'softElectronByPtBJetTags',
                                                        'softElectronByIP3dBJetTags',
                                                        'softMuonBJetTags',
                                                        'softMuonByPtBJetTags',
                                                        'softMuonByIP3dBJetTags') ]
        }

        setattr( self.getvalue('process'), 'btaggingTagInfos' + label, mkseq(self.getvalue('process'), *(labels['tagInfos']) ) )
        setattr( self.getvalue('process'), 'btaggingJetTags' + label,  mkseq(self.getvalue('process'), *(labels['jetTags'])  ) )
        seq = mkseq(self.getvalue('process'), jtaLabel, 'btaggingTagInfos' + label, 'btaggingJetTags' + label)
        setattr( self.getvalue('process'), 'btagging' + label, seq )
        return (seq, labels)


    def __call__(self, process,InputTag=cms.InputTag('sisCone5CaloJets'),label='SCS', doJTA=True, doBTagging=True, jetCorrLabel=None, doType1MET=True,doL1Cleaning=True, doL1Counters=False, genJetCollection=cms.InputTag('sisCone5CaloJets')): 


        self.addParameter('process',process, 'description: process')
        self.addParameter('jetCollection',InputTag, 'description: InputTag')
        self.addParameter('postfixLabel',label, 'description: label')
        self.addParameter('doJTA',doJTA, 'description: doJTA')
        self.addParameter('doBTagging',doBTagging, 'description: doBTagging')
        self.addParameter('jetCorrLabel',jetCorrLabel, 'description: jetCorrLabel')
        self.addParameter('doType1MET',doType1MET, 'description: doType1MET')
        self.addParameter('doL1Cleaning',doL1Cleaning, 'description: doL1Cleaning')
        self.addParameter('doL1Counters',doL1Counters, 'description: doL1Counters')
        self.addParameter('genJetCollection',genJetCollection, 'description: genJetCollection')
        par=copy.copy(self)
        action = Action("AddJetCollection",copy.copy(self.parameters),self) 
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
            existing = getattr(self.getvalue('process'), label)
            setattr( self.getvalue('process'), label + self.getvalue('postfixLabel'), value)
            self.getvalue('process').patDefaultSequence.replace( existing, existing * value )
        def addClone(label,**replaceStatements):
            new      = getattr(self.getvalue('process'), label).clone(**replaceStatements)
            addAlso(label, new)
        addClone('allLayer1Jets', jetSource = self.getvalue('jetCollection'))
        l1Jets = getattr(self.getvalue('process'), 'allLayer1Jets'+self.getvalue('postfixLabel'))
        addClone('selectedLayer1Jets', src=cms.InputTag('allLayer1Jets'+self.getvalue('postfixLabel')))
        addClone('cleanLayer1Jets', src=cms.InputTag('selectedLayer1Jets'+self.getvalue('postfixLabel')))
        if self.getvalue('doL1Counters'):
            addClone('countLayer1Jets', src=cms.InputTag('cleanLayer1Jets'+self.getvalue('postfixLabel')))
        addClone('jetPartonMatch',       src = self.getvalue('jetCollection'))
        addClone('jetGenJetMatch',       src = self.getvalue('jetCollection'))
        addClone('jetPartonAssociation', jets = self.getvalue('jetCollection'))
        addClone('jetFlavourAssociation',srcByReference = cms.InputTag('jetPartonAssociation' + self.getvalue('postfixLabel')))
        def fixInputTag(x): x.setModuleLabel(x.moduleLabel+self.getvalue('postfixLabel'))
        def fixVInputTag(x): x[0].setModuleLabel(x[0].moduleLabel+self.getvalue('postfixLabel'))
        fixInputTag(l1Jets.JetPartonMapSource)
        fixInputTag(l1Jets.genJetMatch)
        fixInputTag(l1Jets.genPartonMatch)
        def vit(*args) : return cms.VInputTag( *[ cms.InputTag(x) for x in args ] )
        if self.getvalue('doBTagging') :
            (btagSeq, btagLabels) = self.runBTagging(self.getvalue('postfixLabel')) 
            self.getvalue('process').patAODCoreReco += btagSeq  # must add to Core, as it's needed by Extra
            addClone('patJetCharge', src=cms.InputTag(btagLabels['jta']))
            l1Jets.trackAssociationSource = cms.InputTag(btagLabels['jta'])
            l1Jets.tagInfoSources         = cms.VInputTag( *[ cms.InputTag(x) for x in btagLabels['tagInfos'] ] )
            l1Jets.discriminatorSources   = cms.VInputTag( *[ cms.InputTag(x) for x in btagLabels['jetTags']  ] )
            fixInputTag(l1Jets.jetChargeSource)
        else:
            l1Jets.addBTagInfo = False 
        if self.getvalue('doJTA') or self.getvalue('doBTagging'):
            if not self.getvalue('doBTagging'):
                self.getvalue('process').load("RecoJets.JetAssociationProducers.ic5JetTracksAssociatorAtVertex_cfi")
                from RecoJets.JetAssociationProducers.ic5JetTracksAssociatorAtVertex_cfi import ic5JetTracksAssociatorAtVertex
                jtaLabel = 'jetTracksAssociatorAtVertex' + self.getvalue('postfixLabel')
                setattr( self.getvalue('process'), jtaLabel, ic5JetTracksAssociatorAtVertex.clone(jets = self.getvalue('jetCollection')) )
                self.getvalue('process').patAODReco.replace(self.getvalue('process').patJetTracksCharge, getattr(self.getvalue('process'),jtaLabel) + self.getvalue('process').patJetTracksCharge)
                l1Jets.trackAssociationSource = cms.InputTag(jtaLabel)
                addClone('patJetCharge', src=cms.InputTag(jtaLabel)),
                fixInputTag(l1Jets.jetChargeSource)
        else: ## no JTA
            l1Jets.addAssociatedTracks = False
            l1Jets.addJetCharge = False
        if self.getvalue('jetCorrLabel') != None:
            if self.getvalue('jetCorrLabel') == False : raise ValueError, "In addJetCollection 'jetCorrLabel' must be set to None, not False"
            if self.getvalue('jetCorrLabel') == "None": raise ValueError, "In addJetCollection 'jetCorrLabel' must be set to None (without quotes), not 'None'"
            if type(self.getvalue('jetCorrLabel')) != type(('IC5','Calo')): 
                raise ValueError, "In switchJetCollection 'jetCorrLabel' must be None, or a tuple ('Algo', 'Type')"
            if not hasattr( self.getvalue('process'), 'L2L3JetCorrector%s%s' % self.getvalue('jetCorrLabel') ):
                setattr( self.getvalue('process'), 
                         'L2L3JetCorrector%s%s' % self.getvalue('jetCorrLabel'), 
                         cms.ESSource("JetCorrectionServiceChain",
                                      correctors = cms.vstring('L2RelativeJetCorrector%s%s' % self.getvalue('jetCorrLabel'),
                                                               'L3AbsoluteJetCorrector%s%s' % self.getvalue('jetCorrLabel')),

                                      label      = cms.string('L2L3JetCorrector%s%s' % self.getvalue('jetCorrLabel'))
                                      )
                         )
            addClone('jetCorrFactors',       jetSource           = self.getvalue('jetCollection')) 
            self.switchJECParameters( getattr(self.getvalue('process'),'jetCorrFactors'+self.getvalue('postfixLabel')), self.getvalue('jetCorrLabel')[0], self.getvalue('jetCorrLabel')[1], oldalgo='IC5',oldtype='Calo' )
            fixVInputTag(l1Jets.jetCorrFactorsSource)
            if self.getvalue('doType1MET'):
                addClone('metJESCorIC5CaloJet', inputUncorJetsLabel = self.getvalue('jetCollection').value(),
                         corrector = cms.string('L2L3JetCorrector%s%s' % self.getvalue('jetCorrLabel')))
                addClone('metJESCorIC5CaloJetMuons', uncorMETInputTag = cms.InputTag("metJESCorIC5CaloJet"+self.getvalue('postfixLabel')))
                addClone('layer1METs',              metSource = cms.InputTag("metJESCorIC5CaloJetMuons"+self.getvalue('postfixLabel')))
                l1MET = getattr(self.getvalue('process'), 'layer1METs'+self.getvalue('postfixLabel'))
                self.getvalue('process').allLayer1Summary.candidates += [ cms.InputTag('layer1METs'+self.getvalue('postfixLabel')) ]
        else:
            l1Jets.addJetCorrFactors = False
        ## Add this to the summary tables (not strictly needed, but useful)
        if self.getvalue('jetCollection') not in self.getvalue('process').aodSummary.candidates: 
            self.getvalue('process').aodSummary.candidates += [ self.getvalue('jetCollection') ]
        self.getvalue('process').allLayer1Summary.candidates      += [ cms.InputTag('allLayer1Jets'+self.getvalue('postfixLabel')) ]
        self.getvalue('process').selectedLayer1Summary.candidates += [ cms.InputTag('selectedLayer1Jets'+self.getvalue('postfixLabel')) ]




addJetCollection=AddJetCollection()
