#ifndef HIGGS2L2BCANDIDATE_H
#define HIGGS2L2BCANDIDATE_H

struct Higgs2l2bCandidate {

        float zllmass, zllpt, zlleta, zllphi;
        float zjjmass, zjjpt, zjjeta, zjjphi;
        float met, metsig, metphi;
        float higgsmass, higgspt, higgseta, higgsphi;
        float lminpt, lmineta, lminphi;
        float lmaxpt, lmaxeta, lmaxphi;
        float jminpt, jmineta, jminphi;
        float jmaxpt, jmaxeta, jmaxphi;
        float jmincsv, jmincsvmva, jminjprob, jminjbprob, jminssvhe, jminssvhp, jminelpt, jminelip, jminmu, jminmupt, jminmuip, jmintkhe, jmintkhp;
        float jmaxcsv, jmaxcsvmva, jmaxjprob, jmaxjbprob, jmaxssvhe, jmaxssvhp, jmaxelpt, jmaxelip, jmaxmu, jmaxmupt, jmaxmuip, jmaxtkhe, jmaxtkhp;
        bool  jminbmatch, jmincmatch;
        bool  jmaxbmatch, jmaxcmatch;
        bool  jminid, jmaxid;
        float zzdphi, zzdeta, zzdr;
        float lldphi, lldeta, lldr;
        float jjdphi, jjdeta, jjdr;    
        bool  isMuon;

};

#endif
