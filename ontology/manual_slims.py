manual_slims = {
    # this allows us to manually assign term X to slim Y while waiting for ontology updates
    'assay': {
        # DNA accessibility
        'OBI:0001924': ['DNA accessibility'],  # 'OBI:0000870' / MNase-seq
        'OBI:0002039': ['DNA accessibility'],  # 'OBI:0000870', / ATAC-seq,
        'OBI:0001853': ['DNA accessibility'],  # 'OBI:0000870', / DNase-seq
        'OBI:0001859': ['DNA accessibility'],  # 'OBI:0000870', / OBI:0000424  / FAIRE-seq
        'OBI:0002042': ['3D chromatin structure'],  # 'OBI:0000870' (Hi-C)
        'OBI:0001848': ['3D chromatin structure'],  # ChIA-PET / OBI:000870
        'OBI:0001923': ['Proteomics'],  # OBI:0000615': 'MS-MS'
        'OBI:0001849': ['Genotyping'],  # OBI:0000435 (DNA-PET)
        'OBI:0002044': ['RNA binding'],  # OBI:0001854 (RNA-Bind-N-Seq)
        'OBI:0002091': ['Transcription'],  # 5' RACE
        'OBI:0002092': ['Transcription'],  # 3' RACE
        'OBI:0002093': ['Transcription'],  # 5' RLM RACE
        'OBI:0002113': ['Transcription'],  # Bru-seq
        'OBI:0002114': ['Transcription'],  # BruChase-seq
        'OBI:0002143': ['Transcription'],  # BruUV-seq
        'OBI:0002045': ['Transcription'],  # PAS-seq
        'OBI:0002571': ['Transcription'],  # polyA plus RNA-seq
        'OBI:0002572': ['Transcription'],  # polyA minus RNA-seq
        'OBI:0002112': ['Transcription'],  # small RNA-seq
        'OBI:0001271': ['Transcription'],  # total RNA-seq
        'OBI:0002753': ['Transcription'],  # PRO-cap
        'OBI:0002457': ['Transcription'],  # PRO-seq
        'OBI:0001863': ['DNA methylation'],  # WGBS
        'OBI:0001862': ['DNA methylation'],  # RRBS
        'OBI:0001861': ['DNA methylation'],  # MRE-seq
        'OBI:0002086': ['DNA methylation'],  # TAB-seq
        'OBI:0000716': ['DNA binding'], # ChIP-seq
        'OBI:0001919': ['3D chromatin structure'], # 5C
        'OBI:0002160': ['DNA binding'], # Mint-ChIP-seq
        'OBI:0003033': ['DNA binding'], # CUT&RUN
        'OBI:0003034': ['DNA binding'], # CUT&Tag
        'OBI:0002083': ['Reporter assay'], # enhancer reporter assay
        'OBI:0002675': ['Massively parallel reporter assay'], # MPRA
        'OBI:0002041': ['Massively parallel reporter assay'], # STARR-seq
        'OBI:2100402': ['Library preparation'], # pooled clone sequencing
        'OBI:0002762': ['Single cell', 'DNA accessibility'],  # snATAC-seq,
        'OBI:0002631': ['Single cell', 'Transcription'],  # scRNA-seq,
        'OBI:0002038': ['Ribosome activity'], # Ribo-seq
    },
    'cells': {
        'CL:0000038': ['hematopoietic cell', 'myeloid cell', 'progenitor cell'], # 'hematopoietic cell' & 'myeloid cell' are ontology-based
        'CL:0000049': ['hematopoietic cell', 'progenitor cell'], # 'hematopoietic cell' is ontology-based
        'CL:0000050': ['hematopoietic cell', 'myeloid cell', 'progenitor cell'], # 'hematopoietic cell' & 'myeloid cell' are ontology-based
        'CL:0000051': ['hematopoietic cell', 'progenitor cell'], # 'hematopoietic cell' is ontology-based
        'CL:0000545': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD4+ T cell'],
        'CL:0000546': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD4+ T cell'],
        'CL:0000553': ['hematopoietic cell', 'myeloid cell', 'progenitor cell'], # 'hematopoietic cell' & 'myeloid cell' are ontology-based
        'CL:0000557': ['hematopoietic cell', 'myeloid cell', 'progenitor cell'], # 'hematopoietic cell' & 'myeloid cell' are ontology-based
        'CL:0000623': ['hematopoietic cell', 'leukocyte', 'NK cell'],
        'CL:0000624': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD4+ T cell'],
        'CL:0000625': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD8+ T cell'],
        'CL:0000765': ['hematopoietic cell', 'myeloid cell'],
        'CL:0000792': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD4+ T cell'],
        'CL:0000815': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD4+ T cell'],
        'CL:0000823': ['hematopoietic cell', 'leukocyte', 'NK cell'],
        'CL:0000837': ['hematopoietic cell', 'progenitor cell'], # 'hematopoietic cell' is ontology-based
        'CL:0000842': ['hematopoietic cell', 'leukocyte', 'mononuclear cell'],
        'CL:0000895': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD4+ T cell'],
        'CL:0000896': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD4+ T cell'],
        'CL:0000897': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD4+ T cell'],
        'CL:0000899': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD4+ T cell'],
        'CL:0000900': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD8+ T cell'],
        'CL:0000905': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD4+ T cell'],
        'CL:0000909': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD8+ T cell'],
        'CL:0000913': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD8+ T cell'],
        'CL:0000938': ['hematopoietic cell', 'leukocyte', 'NK cell'],
        'CL:0000939': ['hematopoietic cell', 'leukocyte', 'NK cell'],
        'CL:0001054': ['hematopoietic cell', 'leukocyte', 'monocyte', 'myeloid cell'],
        'CL:0001059': ['hematopoietic cell', 'progenitor cell', 'myeloid cell'],  # 'hematopoietic cell' is ontology-based
        'CL:0002061': ['T cell', 'hematopoietic cell', 'leukocyte', 'CD4+ T cell'],
        'CL:0002351': ['progenitor cell'],
        'CL:0002399': ['hematopoietic cell', 'leukocyte', 'dendritic cell', 'myeloid cell'],
        'CL:0011020': ['progenitor cell'],
        'CL:2000001': ['hematopoietic cell', 'leukocyte', 'mononuclear cell'],
        'CLO:0007123': ['cancer cell'],
        'CLO:0007052': ['cancer cell'],
        'CLO:0003771': ['epithelial cell'],
        'CLO:0004291': ['epithelial cell'],
        'CLO:0004290': ['epithelial cell'],
        'CLO:0007045': ['hematopoietic cell', 'cancer cell', 'leukocyte', 'T cell'],
        'CLO:0011092': ['fibroblast'],
        'CLO:0033911': ['fibroblast'],
        'CLO:0021511': ['fibroblast'],
        'CLO:0033902': ['fibroblast'],
        'CLO:0018813': ['fibroblast'],
        'CLO:0021752': ['fibroblast'],
        'CLO:0034140': ['fibroblast'],
        'CLO:0021754': ['fibroblast'],
        'CLO:0016536': ['fibroblast'],
        'CLO:0034837': ['fibroblast'],
        'CLO:0018812': ['fibroblast'],
        'EFO:0000681': ['cancer cell'],
        'EFO:0009319': ['stem cell'],
        'EFO:0009320': ['stem cell'],
        'EFO:0004038': ['stem cell']
    },
    'developmental': {
        'CL:0002451': ['ectoderm'],
        'CL:0011012': ['ectoderm'],
        'CL:0002319': ['ectoderm'],
        'CL:0011020': ['ectoderm'],
        'CL:2000054': ['endoderm'],
        'CL:0001053': ['endoderm', 'mesoderm'],
        'CL:0000842': ['endoderm', 'mesoderm'],
        'CL:0000823': ['endoderm', 'mesoderm'],
        'CL:0000788': ['endoderm', 'mesoderm'],
        'CL:0000785': ['endoderm', 'mesoderm'],
        'CL:0000623': ['endoderm', 'mesoderm'],
        'CL:0000451': ['endoderm', 'mesoderm'],
        'CL:0000815': ['endoderm', 'mesoderm'],
        'CL:0000792': ['endoderm', 'mesoderm'],
        'CL:0000625': ['endoderm', 'mesoderm'],
        'CL:0000624': ['endoderm', 'mesoderm'],
        'CL:0000236': ['endoderm', 'mesoderm'],
        'CL:0000084': ['endoderm', 'mesoderm'],
        'CL:0001059': ['mesoderm'],
        'CL:0000775': ['mesoderm'],
        'CL:0000765': ['mesoderm'],
        'CL:0000553': ['mesoderm'],
        'CL:0000081': ['mesoderm'],
        'CL:0000051': ['mesoderm'],
        'CL:0000050': ['mesoderm'],
        'CL:0000049': ['mesoderm'],
        'CL:0000038': ['mesoderm'],
        'CL:0000037': ['mesoderm'],
        'CL:0000650': ['mesoderm'],
        'CL:2000007': ['mesoderm'],
        'CL:2000068': ['mesoderm'],
        'CL:1001225': ['mesoderm'],
        'CL:1001111': ['mesoderm'],
        'CL:1000507': ['mesoderm'],
        'CL:0002584': ['mesoderm'],
        'CL:0002518': ['mesoderm'],
        'CL:1000500': ['mesoderm'],
        'CL:0000965': ['mesoderm'],
        'CL:0000763': ['mesoderm'],
        'CL:0000837': ['mesoderm'],
        'CL:0000138': ['mesoderm'],
        'CL:0000136': ['mesoderm'],
        'CL:0000134': ['mesoderm'],
        'CL:0000448': ['mesoderm'],
        'CLO:0007123': ['mesoderm'],
        'CLO:0007045': ['mesoderm'],
        'CLO:0011092': ['ectoderm'],
        'CLO:0033911': ['ectoderm'],
        'CLO:0021511': ['ectoderm'],
        'CLO:0018813': ['ectoderm'],
        'CLO:0021752': ['ectoderm'],
        'CLO:0004291': ['ectoderm'],
        'CLO:0034140': ['ectoderm'],
        'CLO:0016536': ['ectoderm'],
        'CLO:0034837': ['ectoderm'],
        'CLO:0018812': ['ectoderm'],
        'CLO:0033902': ['endoderm'],
        'CLO:0007052': ['endoderm'],
        'EFO:0009500': ['endoderm'],
        'EFO:0006639': ['endoderm'],
        'EFO:0006389': ['endoderm'],
        'EFO:0002824': ['endoderm'],
        'EFO:0002083': ['endoderm'],
        'EFO:0001232': ['endoderm'],
        'EFO:0001193': ['endoderm'],
        'EFO:0002368': ['endoderm'],
        'EFO:0001099': ['endoderm'],
        'EFO:0005713': ['endoderm'],
        'EFO:0002713': ['endoderm'],
        'EFO:0002357': ['endoderm', 'mesoderm'],
        'EFO:0002167': ['endoderm', 'mesoderm'],
        'EFO:0005441': ['endoderm', 'mesoderm'],
        'EFO:0005719': ['endoderm', 'mesoderm'],
        'EFO:0007611': ['endoderm', 'mesoderm'],
        'EFO:0006492': ['endoderm', 'mesoderm'],
        'EFO:0002324': ['endoderm', 'mesoderm'],
        'EFO:0005694': ['mesoderm'],
        'EFO:0002330': ['mesoderm'],
        'EFO:0002234': ['mesoderm'],
        'EFO:0002869': ['mesoderm'],
        'EFO:0004389': ['mesoderm'],
        'EFO:0009501': ['mesoderm'],
        'EFO:0002059': ['mesoderm'],
        'EFO:0005481': ['mesoderm'],
        'EFO:0005707': ['mesoderm'],
        'EFO:0005703': ['mesoderm'],
        'EFO:0002150': ['mesoderm'],
        'EFO:0001184': ['mesoderm'],
        'EFO:0001182': ['mesoderm'],
        'EFO:0002179': ['mesoderm'],
        'EFO:0002108': ['mesoderm'],
        'EFO:0000681': ['mesoderm'],
        'EFO:0002106': ['mesoderm'],
        'EFO:0005722': ['mesoderm'],
        'EFO:0005702': ['mesoderm'],
        'UBERON:0001322': ['ectoderm'],
        'UBERON:0001323': ['ectoderm'],
        'UBERON:0000310': ['ectoderm', 'mesoderm'],
        'UBERON:0002101': ['ectoderm', 'mesoderm'],
        'UBERON:0002102': ['ectoderm', 'mesoderm'],
        'UBERON:0002386': ['ectoderm', 'mesoderm'],
        'UBERON:0002470': ['ectoderm', 'mesoderm'],
        'UBERON:0003822': ['ectoderm', 'mesoderm'],
        'UBERON:0005417': ['ectoderm', 'mesoderm'],
        'UBERON:0005418': ['ectoderm', 'mesoderm'],
        'UBERON:0000059': ['endoderm'],
        'UBERON:0000160': ['endoderm'],
        'UBERON:0000317': ['endoderm'],
        'UBERON:0000320': ['endoderm'],
        'UBERON:0000945': ['endoderm'],
        'UBERON:0001043': ['endoderm'],
        'UBERON:0001150': ['endoderm'],
        'UBERON:0001155': ['endoderm'],
        'UBERON:0001157': ['endoderm'],
        'UBERON:0001159': ['endoderm'],
        'UBERON:0001199': ['endoderm'],
        'UBERON:0001264': ['endoderm'],
        'UBERON:0002108': ['endoderm'],
        'UBERON:0002114': ['endoderm'],
        'UBERON:0002115': ['endoderm'],
        'UBERON:0002469': ['endoderm'],
        'UBERON:0004550': ['endoderm'],
        'UBERON:0004992': ['endoderm'],
        'UBERON:0006920': ['endoderm'],
        'UBERON:0008971': ['endoderm'],
        'UBERON:0011878': ['endoderm'],
        'UBERON:0012488': ['endoderm'],
        'UBERON:0012489': ['endoderm'],
        'UBERON:0001211': ['endoderm', 'mesoderm'],
        'UBERON:0001013': ['mesoderm'],
        'UBERON:0001224': ['mesoderm'],
        'UBERON:0001285': ['mesoderm'],
        'UBERON:0001348': ['mesoderm'],
        'UBERON:0001383': ['mesoderm'],
        'UBERON:0001499': ['mesoderm'],
        'UBERON:0001774': ['mesoderm'],
        'UBERON:0002113': ['mesoderm'],
        'UBERON:0002324': ['mesoderm'],
        'UBERON:0002407': ['mesoderm'],
        'UBERON:0003662': ['mesoderm'],
        'UBERON:0003663': ['mesoderm'],
        'UBERON:0003830': ['mesoderm'],
        'UBERON:0003916': ['mesoderm'],
        'UBERON:0004538': ['mesoderm'],
        'UBERON:0004539': ['mesoderm'],
        'UBERON:0005270': ['mesoderm'],
        'UBERON:0008450': ['mesoderm'],
        'UBERON:0010754': ['mesoderm'],
        'UBERON:0011907': ['mesoderm'],
        'UBERON:0018117': ['mesoderm'],
        'UBERON:0018118': ['mesoderm'],
        'UBERON:8300001': ['mesoderm'],
        'UBERON:8300002': ['mesoderm'],
        'UBERON:8300003': ['mesoderm'],
        'UBERON:8300004': ['mesoderm']
    },
    'organs': {
        'CL:0000037': ['blood', 'bodily fluid'],
        'CL:0000081': ['blood', 'bodily fluid'],
        'CL:0000084': ['blood', 'bodily fluid'],
        'CL:0000236': ['blood', 'bodily fluid'],
        'CL:0000492': ['blood', 'bodily fluid'],
        'CL:0000545': ['blood', 'bodily fluid'],
        'CL:0000546': ['blood', 'bodily fluid'],
        'CL:0000576': ['blood', 'bodily fluid'],
        'CL:0000623': ['blood', 'bodily fluid'],
        'CL:0000624': ['blood', 'bodily fluid'],
        'CL:0000625': ['blood', 'bodily fluid'],
        'CL:0000775': ['blood', 'bodily fluid'],
        'CL:0000785': ['blood', 'bodily fluid'],
        'CL:0000787': ['blood', 'bodily fluid'],
        'CL:0000788': ['blood', 'bodily fluid'],
        'CL:0000792': ['blood', 'bodily fluid'],
        'CL:0000815': ['blood', 'bodily fluid'],
        'CL:0000837': ['blood', 'bodily fluid'],
        'CL:0000842': ['blood', 'bodily fluid'],
        'CL:0000862': ['blood', 'bodily fluid'],
        'CL:0000863': ['blood', 'bodily fluid'],
        'CL:0000895': ['blood', 'bodily fluid'],
        'CL:0000896': ['blood', 'bodily fluid'],
        'CL:0000897': ['blood', 'bodily fluid'],
        'CL:0000899': ['blood', 'bodily fluid'],
        'CL:0000900': ['blood', 'bodily fluid'],
        'CL:0000902': ['blood', 'bodily fluid'],
        'CL:0000905': ['blood', 'bodily fluid'],
        'CL:0000909': ['blood', 'bodily fluid'],
        'CL:0000913': ['blood', 'bodily fluid'],
        'CL:0000938': ['blood', 'bodily fluid'],
        'CL:0000939': ['blood', 'bodily fluid'],
        'CL:0001042': ['blood', 'bodily fluid'],
        'CL:0001053': ['blood', 'bodily fluid'],
        'CL:0001054': ['blood', 'bodily fluid'],
        'CL:0002061': ['blood', 'bodily fluid'],
        'CL:0002399': ['blood', 'bodily fluid'],
        'CL:0000765': ['bone marrow', 'bone element'],
        'CL:0000763': ['bone marrow', 'bone element'],
        'CL:0000038': ['bone marrow', 'bone element'],
        'CL:0001059': ['bone marrow', 'bone element'],
        'CL:0000553': ['bone marrow', 'bone element'],
        'CL:0000235': ['bone marrow', 'bone element'],
        'CL:0000051': ['bone marrow', 'bone element'],
        'CL:0000050': ['bone marrow', 'bone element'],
        'CL:0000049': ['bone marrow', 'bone element'],
        'CL:0000823': ['bone marrow', 'bone element', 'lymph node', 'spleen', 'thymus'],
        'CL:0000598': ['brain'],
        'CL:0000127': ['brain', 'spinal cord'],
        'CL:0000100': ['brain', 'spinal cord'],
        'CL:0000103': ['brain', 'spinal cord', 'ear', 'eye'],
        'CL:2000017': ['connective tissue', 'mouth'], # 'connective tissue' is ontology-based
        'CL:0011012': ['embryo'],
        'CL:0000681': ['embryo'],
        'CL:0000352': ['embryo'],
        'CL:0000047': ['embryo'],
        'CL:0002322': ['embryo'],
        'CL:0002259': ['embryo', 'epithelium'],
        'CL:0002351': ['endocrine gland', 'pancreas'],
        'CL:2000054': ['exocrine gland', 'liver', 'endocrine gland'],
        'CL:0000091': ['exocrine gland', 'liver', 'endocrine gland', 'blood vessel', 'vasculature'],
        'CL:0002451': ['exocrine gland', 'mammary gland'],
        'CL:0002328': ['lung', 'bronchus', 'epithelium'], # 'bronchus' & 'epithelium' are ontology-based
        'CL:0002598': ['lung', 'bronchus'], # 'bronchus' is ontology-based
        'CL:0000515': ['musculature of body'],
        'CL:0000187': ['musculature of body'],
        'CL:0000192': ['musculature of body'],
        'CL:0000680': ['musculature of body'],
        'CL:0000056': ['musculature of body'],
        'CL:0000746': ['musculature of body', 'heart'],
        'CL:0010021': ['musculature of body', 'heart'],
        'CL:0002098': ['musculature of body', 'heart'],
        'CL:0000019': ['testis'],
        'CLO:0007045': ['blood', 'bodily fluid'],
        'CLO:0007052': ['endocrine gland', 'thyroid gland'],
        'CLO:0004290': ['eye', 'epithelium'],
        'CLO:0003771': ['kidney', 'epithelium'],
        'CLO:0033902': ['lung', 'connective tissue'],
        'CLO:0004291': ['mammary gland', 'epithelium', 'exocrine gland'],
        'CLO:0021754': ['mouth', 'connective tissue'],
        'CLO:0011092': ['skin of body', 'connective tissue'],
        'CLO:0033911': ['skin of body', 'connective tissue'],
        'CLO:0021511': ['skin of body', 'connective tissue'],
        'CLO:0018813': ['skin of body', 'connective tissue'],
        'CLO:0021752': ['skin of body', 'connective tissue'],
        'CLO:0034140': ['skin of body', 'connective tissue'],
        'CLO:0016536': ['skin of body', 'connective tissue'],
        'CLO:0034837': ['skin of body', 'connective tissue'],
        'CLO:0018812': ['skin of body', 'connective tissue'],
        'CLO:0007123': ['urinary bladder'],
        'EFO:0005233': ['blood', 'bodily fluid', 'lymph node'], # 'blood' & 'bodily fluid' are ontology-based
        'EFO:0005719': ['blood', 'bodily fluid', 'lymph node'], # 'lymph node' is ontology-based
        'EFO:0006283': ['blood', 'bodily fluid', 'lymph node'], # 'blood' & 'bodily fluid' are ontology-based
        'EFO:0002939': ['brain'],
        'EFO:0005823': ['brain'],
        'EFO:0005694': ['bone element'],
        'EFO:0009500': ['colon', 'intestine', 'large intestine'],
        'EFO:0000586': ['connective tissue'],
        'EFO:0004038': ['embryo'],
        'EFO:0005824': ['eye'],
        'EFO:0000681': ['kidney'],
        'EFO:0005650': ['limb'],
        'EFO:0005744': ['limb', 'epithelium', 'embryo'], # 'epithelium' & 'embryo' are ontology-based
        'EFO:0002787': ['lymphoid tissue'],
        'EFO:0002779': ['skin of body', 'penis', 'connective tissue'], # 'connective tissue' & 'penis' are ontology-based
        'UBERON:8300001': ['bone element', 'skeleton', 'limb'], # 'limb' is ontology-based
        'UBERON:8300002': ['bone element', 'skeleton', 'limb'], # 'limb' is ontology-based
        'UBERON:8300003': ['bone element', 'skeleton', 'limb'], # 'limb' is ontology-based
        'UBERON:8300004': ['bone element', 'skeleton', 'limb'] # 'limb' is ontology-based
    },
    'systems': {
        'CL:0000103': ['central nervous system'],
        'CL:0011020': ['central nervous system'],
        'CL:0008030': ['central nervous system', 'peripheral nervous system'],
        'CL:0002319': ['central nervous system', 'peripheral nervous system'],
        'CL:0000540': ['central nervous system', 'peripheral nervous system'], # 'central nervous system' is ontology-based
        'CL:0000765': ['circulatory system'],
        'CL:0000081': ['circulatory system'],
        'CL:0002351': ['endocrine system'],
        'CL:0000083': ['endocrine system'],
        'CL:0000650': ['excretory system'],
        'CL:0000763': ['immune system'],
        'CL:2000054': ['immune system', 'endocrine system', 'digestive system'], # 'immune system' is ontology-based
        'CL:0002451': ['integumental system', 'exocrine system'],
        'CL:0000515': ['musculature'],
        'CL:0000187': ['musculature'],
        'CL:0000192': ['musculature'],
        'CL:0000680': ['musculature'],
        'CL:0000056': ['musculature'],
        'CL:0010021': ['musculature', 'circulatory system'],
        'CL:0000746': ['musculature', 'circulatory system'], # 'circulatory system' is ontology-based
        'CL:0000062': ['skeletal system'],
        'CL:0001059': ['immune system'],
        'CLO:0007052': ['endocrine system'],
        'CLO:0007123': ['excretory system'],
        'CLO:0003771': ['excretory system'],
        'CLO:0021754': ['digestive system'],
        'CLO:0007045': ['immune system'],
        'CLO:0011092': ['integumental system'],
        'CLO:0033911': ['integumental system'],
        'CLO:0021511': ['integumental system'],
        'CLO:0018813': ['integumental system'],
        'CLO:0021752': ['integumental system'],
        'CLO:0004291': ['integumental system'],
        'CLO:0034140': ['integumental system'],
        'CLO:0016536': ['integumental system'],
        'CLO:0034837': ['integumental system'],
        'CLO:0018812': ['integumental system'],
        'CLO:0033902': ['respiratory system'],
        'CLO:0004290': ['sensory system'],
        'EFO:0009500': ['digestive system'],
        'EFO:0005713': ['endocrine system'],
        'EFO:0002713': ['endocrine system'],
        'EFO:0000681': ['excretory system'],
        'EFO:0005441': ['reproductive system'],
        'EFO:0005824': ['sensory system'],
        'EFO:0005694': ['skeletal system'],
        'UBERON:0007650': ['digestive system'],
        'UBERON:0006566': ['musculature', 'circulatory system'], # 'circulatory system' is ontology-based
        'UBERON:0006567': ['musculature', 'circulatory system'], # 'circulatory system' is ontology-based
        'UBERON:0002101': ['musculature', 'skeletal system'],
        'UBERON:8300001': ['skeletal system'],
        'UBERON:8300002': ['skeletal system'],
        'UBERON:8300003': ['skeletal system'],
        'UBERON:8300004': ['skeletal system']
    }
}
