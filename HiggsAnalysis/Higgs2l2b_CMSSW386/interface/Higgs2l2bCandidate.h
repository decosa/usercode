#ifndef HIGGS2L2BCANDIDATE_H
#define HIGGS2L2BCANDIDATE_H

struct Higgs2l2bCandidate {

        float zllmass, zllpt, zlleta, zllphi;
        float zjjmass, zjjpt, zjjeta, zjjphi;
        float higgsmass, higgspt, higgseta, higgsphi;
        float lminpt, lminet, lmineta, lminphi, lminHLT;
        float lmaxpt, lmaxet, lmaxeta, lmaxphi, lmaxHLT;
        float jminpt, jmineta, jminphi;
        float jmaxpt, jmaxeta, jmaxphi;
        float jmincsv, jmincsvmva, jminjprob, jminjbprob, jminssvhe, jminssvhp, jminelpt, jminelip, jminmu, jminmupt, jminmuip, jmintkhe, jmintkhp;
        float jmaxcsv, jmaxcsvmva, jmaxjprob, jmaxjbprob, jmaxssvhe, jmaxssvhp, jmaxelpt, jmaxelip, jmaxmu, jmaxmupt, jmaxmuip, jmaxtkhe, jmaxtkhp;
        float numel, nummu, numjet;
        float zzdphi, zzdeta, zzdr;
        float lldphi, lldeta, lldr;
        float jjdphi, jjdeta, jjdr;    
        bool isMuon;

};

#endif
