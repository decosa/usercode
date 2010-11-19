#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
//#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"
#include "FWCore/Utilities/interface/EDMException.h"
//#include "CommonTools/UtilAlgos/interface/TFileService.h"

// #include "DataFormats/RecoCandidate/interface/IsoDeposit.h"
// #include "DataFormats/RecoCandidate/interface/IsoDepositFwd.h"
// #include "DataFormats/PatCandidates/interface/Isolation.h"
// #include "DataFormats/RecoCandidate/interface/IsoDepositVetos.h"
// #include "DataFormats/RecoCandidate/interface/IsoDepositDirection.h"

// #include "DataFormats/BeamSpot/interface/BeamSpot.h"
// #include "DataFormats/VertexReco/interface/VertexFwd.h"
// #include "DataFormats/VertexReco/interface/Vertex.h"

#include "PhysicsTools/CandUtils/interface/CenterOfMassBooster.h"
#include "PhysicsTools/CandUtils/interface/Booster.h"

#include <Math/VectorUtil.h>
#include <vector>

using namespace edm;
using namespace std;
using namespace reco;
//using namespace isodeposit;
//using namespace pat;

class Higgs2l2bUserData : public edm::EDProducer {
public:
  Higgs2l2bUserData( const edm::ParameterSet & );   
  //typedef math::XYZVector Vector;
private:
  void produce( edm::Event &, const edm::EventSetup & );
  
  InputTag higgsTag;
 
   

};



Higgs2l2bUserData::Higgs2l2bUserData( const ParameterSet & cfg ):
  higgsTag( cfg.getParameter<InputTag>( "higgs" ) ){
  produces<vector<pat::CompositeCandidate> >();
}

void Higgs2l2bUserData::produce( Event & evt, const EventSetup & ) {

  Handle<std::vector<reco::CompositeCandidate> > higgsH;
  evt.getByLabel(higgsTag, higgsH);

  auto_ptr<vector<pat::CompositeCandidate> > higgsColl( new vector<pat::CompositeCandidate> () );
  
  for (unsigned int i = 0; i< higgsH->size();++i){
    const reco::CompositeCandidate & H = (*higgsH)[i];
    edm::Ref<std::vector<reco::CompositeCandidate> > hRef(higgsH, i);
    pat::CompositeCandidate h(H);
    
   
    // Phi in H rest frame
    float phi;
    
    Booster hFrameBoost( H.boostToCM() );
    const Candidate * zDauRefl0 = H.daughter(0)->daughter(0);
    Candidate * boostedL0_HFrame = zDauRefl0->clone();
    hFrameBoost.set( *boostedL0_HFrame );
    const Candidate * zDauRefl1 = H.daughter(0)->daughter(1);
    Candidate * boostedL1_HFrame = zDauRefl1->clone();
    hFrameBoost.set( *boostedL1_HFrame);
    const Candidate * zDauRefj0 = H.daughter(1)->daughter(0);
    Candidate * boostedJ0_HFrame = zDauRefj0->clone();
    hFrameBoost.set( *boostedJ0_HFrame );
    const Candidate * zDauRefj1 = H.daughter(1)->daughter(1);  
    Candidate * boostedJ1_HFrame = zDauRefj1->clone();
    hFrameBoost.set( *boostedJ1_HFrame );
    
    phi =  ROOT::Math::VectorUtil::Angle( (boostedL0_HFrame->momentum()).Cross(boostedL1_HFrame->momentum()), (boostedJ0_HFrame->momentum()).Cross(boostedJ1_HFrame->momentum()) );
       
    if (phi>M_PI/2) phi = M_PI -phi;
    


    h.addUserFloat("azimuthalAngle", phi);
    
    higgsColl->push_back(h);
    
  }
  
  evt.put( higgsColl);
}

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE( Higgs2l2bUserData );

