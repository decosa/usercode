
#SAMPLE=/GluGluToHToZZTo2L2Q_M-200_8TeV-powheg-pythia6/local-SkimPAT_H2l2q_523_v3_l_GluGluToHToZZTo2L2Q_M-200-d66ed679473489da3d36e8bed5b99797/USER
#OUTFILE=GluGluToHToZZTo2L2Q_M-200_8TeV.list



#SAMPLE=/GluGluToHToZZTo2L2Q_M-300_8TeV-powheg-pythia6/local-SkimPAT_H2l2q_523_v3_l_GluGluToHToZZTo2L2Q_M-300-d66ed679473489da3d36e8bed5b99797/USER
#OUTFILE=GluGluToHToZZTo2L2Q_M-300_8TeV.list

#SAMPLE=/GluGluToHToZZTo2L2Q_M-525_8TeV-powheg-pythia6/local-SkimPAT_H2l2q_523_v3_l_GluGluToHToZZTo2L2Q_M-525-d66ed679473489da3d36e8bed5b99797/USER
#OUTFILE=GluGluToHToZZTo2L2Q_M-525_8TeV.list

#SAMPLE=/GluGluToHToZZTo2L2Q_M-600_8TeV-powheg-pythia6/local-SkimPAT_H2l2q_523_v3_l_GluGluToHToZZTo2L2Q_M-600-d66ed679473489da3d36e8bed5b99797/USER
#OUTFILE=GluGluToHToZZTo2L2Q_M-600_8TeV.list


#SAMPLE=/GluGluToHToZZTo2L2Q_M-700_8TeV-powheg-pythia6/local-SkimPAT_H2l2q_523_v3_l_GluGluToHToZZTo2L2Q_M-700-d66ed679473489da3d36e8bed5b99797/USER
#OUTFILE=GluGluToHToZZTo2L2Q_M-700_8TeV.list


#SAMPLE=/GluGluToHToZZTo2L2Q_M-800_8TeV-powheg-pythia6/local-SkimPAT_H2l2q_523_v3_l_GluGluToHToZZTo2L2Q_M-800-d66ed679473489da3d36e8bed5b99797/USER
#OUTFILE=GluGluToHToZZTo2L2Q_M-800_8TeV.list

SAMPLE=/GluGluToHToZZTo2L2Q_M-900_8TeV-powheg-pythia6/local-SkimPAT_H2l2q_523_v3_l_GluGluToHToZZTo2L2Q_M-900-d66ed679473489da3d36e8bed5b99797/USER

### The outfile name should be the same you use for the folder for that sample. 

OUTFILE=GluGluToHToZZTo2L2Q_M-900_8TeV.list


dbs search --noheader --url http://cmsdbsprod.cern.ch/cms_dbs_ph_analysis_02/servlet/DBSServlet --query="find file where dataset=$SAMPLE" | sed 's|h2l2qSkimData|h2l2q_ntuple|' | sed 's|/store|/pnfs/ciemat.es/data/cms/store|' > $OUTFILE
