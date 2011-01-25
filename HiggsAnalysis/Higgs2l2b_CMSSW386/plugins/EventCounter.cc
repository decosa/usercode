#include <memory>
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/CandUtils/interface/AddFourMomenta.h"
#include "DataFormats/Candidate/interface/CompositeCandidate.h"
#include "DataFormats/Candidate/interface/CompositeCandidateFwd.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "PhysicsTools/CandUtils/interface/CenterOfMassBooster.h"
#include "PhysicsTools/CandUtils/interface/Booster.h"
#include <TTree.h>
#include <TMath.h>
#include <TH1.h>
#include <TVector3.h>
#include <algorithm>
#include <Math/VectorUtil.h>



class EventCounter : public edm::EDAnalyzer {
public:
  explicit EventCounter(const edm::ParameterSet&);
  ~EventCounter();
  
  
private:
  virtual void beginJob();
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob(); 
  int massSel, btagSel, zllptSel, metSel, jjdrSel, hmassSel;
  bool massSelected, btagSelected, zllptSelected, metSelected, jjdrSelected, hmassSelected;
  float met;
  edm::InputTag higgsTag, metTag;


  
        
};

EventCounter::EventCounter(const edm::ParameterSet& iConfig):
    higgsTag(iConfig.getParameter<edm::InputTag>("higgsTag"))
{
  edm::Service<TFileService> fs;
  massSel=0;
  massSelected=false;
  btagSel=0;
  btagSelected=false;
  zllptSel=0;
  zllptSelected=false;
  metSel=0;
  metSelected=false;
  jjdrSel=0;
  jjdrSelected=false;
  hmassSel=0;
  hmassSelected=false;

}


EventCounter::~EventCounter() {
}


void EventCounter::beginJob() {
}


void EventCounter::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
    using namespace edm;
    using namespace reco;
    using namespace std;

    // Get hzzjjlls collections

    std::cout<<"new event "<<std::endl;
    Handle<CandidateView> higgsH;
    iEvent.getByLabel(higgsTag, higgsH);

 //    Handle<pat::METCollection> metH;
//     iEvent.getByLabel(metTag, metH);
//     pat::METCollection met_h = *metH;
//     met = met_h.front().et();

    Handle<float> metH;
    //iEvent.getByLabel(metTag,metH);
    iEvent.getByLabel("hzzeejj","met",metH);
 



 
    massSelected = false;
    btagSelected = false;
    zllptSelected = false;
    metSelected = false;
    jjdrSelected = false;
    hmassSelected = false;
    float jjdr;

    std::cout<<" inizialization "<<massSelected<<std::endl;    
    
    for (size_t i = 0; i < higgsH->size(); ++i) {
    
      const Candidate &  h = (*higgsH)[i];
      const float &  met = (*metH);
      std::cout<<" MET "<<met<<std::endl;
      const Candidate * zll = h.daughter(0);    
      const Candidate * zjj = h.daughter(1);
      const Candidate * zDauRefl0 = h.daughter(0)->daughter(0);
      const Candidate * zDauRefl1 = h.daughter(0)->daughter(1);
      const Candidate * zDauRefj0 = h.daughter(1)->daughter(0);
      const Candidate * zDauRefj1 = h.daughter(1)->daughter(1);  

      const pat::Jet & j0 = dynamic_cast<const pat::Jet &>(*zDauRefj0->masterClone());
      const pat::Jet & j1 = dynamic_cast<const pat::Jet &>(*zDauRefj1->masterClone());

      jjdr = deltaR(zDauRefj0->eta(), zDauRefj0->phi(), zDauRefj1->eta(), zDauRefj1->phi() );


 
    if(TMath::Abs(zll->mass() - 91)< 10 && TMath::Abs(zjj->mass() - 91)< 15) massSelected=true ;

    std::cout<<"zll mass: "<< zll->mass()<<" zjj mass: "<< zjj->mass()<<std::endl;

 

    if( (TMath::Abs(zll->mass() - 91)< 10 && TMath::Abs(zjj->mass() - 91)< 15) && ((j0.bDiscriminator("combinedSecondaryVertexMVABJetTags")>0.5 && j1.bDiscriminator("jetProbabilityBJetTags")>0.9)||(j0.bDiscriminator("jetProbabilityBJetTags")>0.9 && j1.bDiscriminator("combinedSecondaryVertexMVABJetTags")>0.5) ) ) btagSelected=true ;

   
    if( (TMath::Abs(zll->mass() - 91)< 10 && TMath::Abs(zjj->mass() - 91)< 15) && ((j0.bDiscriminator("combinedSecondaryVertexMVABJetTags")>0.5 && j1.bDiscriminator("jetProbabilityBJetTags")>0.9)||(j0.bDiscriminator("jetProbabilityBJetTags")>0.9 && j1.bDiscriminator("combinedSecondaryVertexMVABJetTags")>0.5)) && (zll->pt()>90) ) zllptSelected=true ;

    
    if( (TMath::Abs(zll->mass() - 91)< 10 && TMath::Abs(zjj->mass() - 91)< 15) && ((j0.bDiscriminator("combinedSecondaryVertexMVABJetTags")>0.5 && j1.bDiscriminator("jetProbabilityBJetTags")>0.9)||(j0.bDiscriminator("jetProbabilityBJetTags")>0.9 && j1.bDiscriminator("combinedSecondaryVertexMVABJetTags")>0.5)) && (zll->pt()>90) &&  (met<35) ) metSelected=true ;

    if( (TMath::Abs(zll->mass() - 91)< 10 && TMath::Abs(zjj->mass() - 91)< 15) && ((j0.bDiscriminator("combinedSecondaryVertexMVABJetTags")>0.5 && j1.bDiscriminator("jetProbabilityBJetTags")>0.9)||(j0.bDiscriminator("jetProbabilityBJetTags")>0.9 && j1.bDiscriminator("combinedSecondaryVertexMVABJetTags")>0.5)) && (zll->pt()>90) &&  (met<35) && jjdr<1.7) jjdrSelected=true ;

    if( (TMath::Abs(zll->mass() - 91)< 10 && TMath::Abs(zjj->mass() - 91)< 15) && ((j0.bDiscriminator("combinedSecondaryVertexMVABJetTags")>0.5 && j1.bDiscriminator("jetProbabilityBJetTags")>0.9)||(j0.bDiscriminator("jetProbabilityBJetTags")>0.9 && j1.bDiscriminator("combinedSecondaryVertexMVABJetTags")>0.5)) && (zll->pt()>90) &&  (met<35) && jjdr<1.7 && h.mass()<385 && h.mass()>315) hmassSelected=true ;


  /*
      TCut massSelMu = baseSelMu && "TMath::Abs(muHiggszllMass - 91)< 10 && TMath::Abs(muHiggszjjMass - 91)< 15";
      TCut massSelEl = baseSelEl && "TMath::Abs(elHiggszllMass - 91)< 10 && TMath::Abs(elHiggszjjMass - 91)< 15";
      
      TCut btagSelMu = massSelMu && "((muHiggsJet1CSVMVA>0.5 && muHiggsJet2JbProb>0.9 )||( muHiggsJet2CSVMVA>0.5 && muHiggsJet1JbProb>0.9))";
      TCut btagSelEl = massSelEl && "((elHiggsJet1CSVMVA>0.5 && elHiggsJet2JbProb>0.9 )||(elHiggsJet2CSVMVA>0.5 && elHiggsJet1JbProb>0.9))";
      
      TCut ptllSelMu = btagSelMu && " muHiggszllPt > 90";
      TCut ptllSelEl = btagSelEl && " elHiggszllPt > 90";
      
      TCut metSelMu = ptllSelMu && " met < 35";
      TCut metSelEl = ptllSelEl && " met < 35";
      
      TCut drjjSelMu = metSelMu && " muHiggsjjdr < 1.7";
      TCut drjjSelEl = metSelEl && " elHiggsjjdr < 1.7";
      
      TCut hmassSelMu = drjjSelMu && " muHiggsMass < 385 &&  muHiggsMass > 315 ";
      TCut hmassSelEl = drjjSelEl && " elHiggsMass < 385 &&  elHiggsMass > 315 ";
    */
    

      
  }


    if(massSelected == true) ++massSel;
    std::cout<<" event has been selected? "<<massSelected<<std::endl;

    if(btagSelected == true) ++btagSel;
    std::cout<<" event has been selected after btag selection? "<<btagSelected<<std::endl;

    if(zllptSelected == true) ++zllptSel;
    std::cout<<" event has been selected after zll ptselection? "<<btagSelected<<std::endl;

    if(metSelected == true) ++metSel;
    std::cout<<" event has been selected after met selection? "<<metSelected<<std::endl;

    if(jjdrSelected == true) ++jjdrSel;
    std::cout<<" event has been selected after jjdr selection? "<<jjdrSelected<<std::endl;

    if(hmassSelected == true) ++hmassSel;
    std::cout<<" event has been selected after higgs mass selection? "<<hmassSelected<<std::endl;

}

void EventCounter::endJob() {
  // insert counter and write in a txt file
  std::cout<<std::endl;
  std::cout<<" events after mass selection: "<<massSel<<std::endl;
  std::cout<<" events after btag selection: "<<btagSel<<std::endl;
  std::cout<<" events after zllpt selection: "<<zllptSel<<std::endl;
  std::cout<<" events after met selection: "<<metSel<<std::endl;
  std::cout<<" events after jjdr selection: "<<jjdrSel<<std::endl;
  std::cout<<" events after hmass selection: "<<hmassSel<<std::endl;
}

DEFINE_FWK_MODULE(EventCounter);
