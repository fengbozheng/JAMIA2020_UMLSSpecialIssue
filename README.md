This repository is for JAMIA 2020 UMLS Special Issue submission -- A Transformation-based Method for Auditing the IS-A Hierarchy of Biomedical Terminologies in the Unified Medical Language System (UMLS) 

There are two folders:

  code: contains code for concept name transformation and missing IS-A relations identification for source terminologies of the UMLS.
  
    conceptNameTransformation.py    Given a concept name in the UMLS, we first identify its base and secondary noun chunks. For each identified noun chunk, we generate replacement candidates which are more general than the noun chunk. Then we replace the noun chunks with their replacement candidates to generate new potential concept names which may serve as supertypes of the original concept. If a newly generated name is an existing concept name in the same source terminology with the original concept, then we consider there is a potentially missing IS-A relation between the original and new concepts.
    
  supplementFile: contains two evaluation files.
  
    Supplementary-Appendix-II-SNOMEDCT-Evaluation.xlsx    200 evaluated samples from SNOMED CT
    Supplementary-Appendix-III-GeneOntology-Evaluation.xlsx   100 evaluated samples from Gene Ontology

You could download UMLS from: https://www.nlm.nih.gov/research/umls/index.html
The UMLS file used in this work includes: 
MRREL.RRF (relation), MRCONSO.RRF (concept name), MRSTY.RRF (semantic type)

In this work, we also explored transformation based on normalized concept names.
You can download the normalization tools from: https://lexsrv3.nlm.nih.gov/LexSysGroup/Projects/lvg/current/web/download.html
