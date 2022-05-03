import requests
from requests.structures import CaseInsensitiveDict
from urllib.error import HTTPError
from rdflib import ConjunctiveGraph, exceptions, Namespace
from rdflib import RDFS, RDF, BNode, OWL
from rdflib.collection import Collection
import json
from datetime import date
from ontology.ntr_terms import (
    ntr_assays,
    ntr_biosamples
)
from ontology.manual_slims import slim_shims


OBO_OWL = Namespace('http://www.geneontology.org/formats/oboInOwl#')
OBO = Namespace('http://purl.obolibrary.org/obo/')

ALTERNATIVE_TERM = OBO['IAO_0000118']
HAS_EXACT_SYNONYM = OBO_OWL['hasExactSynonym']
PART_OF = OBO['BFO_0000050']
DEVELOPS_FROM = OBO['RO_0002202']
HUMAN_TAXON = OBO['NCBITaxon_9606']
HAS_PART = OBO['BFO_0000051']
DERIVES_FROM = OBO['RO_0001000']
ACHIEVES_PLANNED_OBJECTIVE = OBO['OBI_0000417']

ONTOLOGY_ASSET_DICT = {
    'uberon': {
        'ontology_repo': 'obophenotype/uberon',
        'asset_name': 'composite-metazoan.owl'
    },
    'efo': {
        'ontology_repo': 'EBISPOT/efo',
        'asset_name': 'efo.owl'
    },
    'mondo': {
        'ontology_repo': 'monarch-initiative/mondo',
        'asset_name': 'mondo.owl'
    },
    'oba': {
        'ontology_repo': 'obo/oba',
        'asset_name': 'oba.owl'
    },
    'obi': {
        'ontology_repo': 'obi-ontology/obi',
        'asset_name': 'obi.owl',
        'uri': 'http://purl.obolibrary.org/obo/obi.owl'
    },
    'clo': {
        'ontology_repo': 'CLO-ontology/CLO',
        'asset_name': 'clo.owl',
        'uri': 'http://purl.obolibrary.org/obo/clo.owl'
    },
    'doid': {
        'ontology_repo': 'DiseaseOntology/HumanDiseaseOntology',
        'asset_name': 'doid.owl',
        'uri': 'http://purl.obolibrary.org/obo/doid.owl'
    }
}

SLIMS_DICT = {
    'developmental': {
        'UBERON:0000926': 'mesoderm',
        'UBERON:0000924': 'ectoderm',
        'UBERON:0000925': 'endoderm'
    },
    'system': {
        'UBERON:0001015': 'musculature',
        'UBERON:0000949': 'endocrine system',
        'UBERON:0002330': 'exocrine system',
        'UBERON:0000990': 'reproductive system',
        'UBERON:0001004': 'respiratory system',
        'UBERON:0001007': 'digestive system',
        'UBERON:0001008': 'excretory system',
        'UBERON:0001009': 'circulatory system',
        'UBERON:0001434': 'skeletal system',
        'UBERON:0002405': 'immune system',
        'UBERON:0002416': 'integumental system',
        'UBERON:0001032': 'sensory system',
        'UBERON:0001017': 'central nervous system',
        'UBERON:0000010': 'peripheral nervous system'
    },

    'organ': {
        'UBERON:0002369': 'adrenal gland',
        'UBERON:0002110': 'gallbladder',
        'UBERON:0002106': 'spleen',
        'UBERON:0001043': 'esophagus',
        'UBERON:0000004': 'nose',
        'UBERON:0000056': 'ureter',
        'UBERON:0000057': 'urethra',
        'UBERON:0000059': 'large intestine',
        'UBERON:0000165': 'mouth',
        'UBERON:0000945': 'stomach',
        'UBERON:0000948': 'heart',
        'UBERON:0000955': 'brain',
        'UBERON:0000970': 'eye',
        'UBERON:0000991': 'gonad',
        'UBERON:0001255': 'urinary bladder',
        'UBERON:0001264': 'pancreas',
        'UBERON:0001474': 'bone element',
        'UBERON:0002048': 'lung',
        'UBERON:0002097': 'skin of body',
        'UBERON:0002107': 'liver',
        'UBERON:0002108': 'small intestine',
        'UBERON:0002113': 'kidney',
        'UBERON:0002240': 'spinal cord',
        'UBERON:0002367': 'prostate gland',
        'UBERON:0002370': 'thymus',
        'UBERON:0003126': 'trachea',
        'UBERON:0001723': 'tongue',
        'UBERON:0001737': 'larynx',
        'UBERON:0006562': 'pharynx',
        'UBERON:0001103': 'diaphragm',
        'UBERON:0002185': 'bronchus',
        'UBERON:0000029': 'lymph node',
        'UBERON:0001132': 'parathyroid gland',
        'UBERON:0002046': 'thyroid gland',
        'UBERON:0001981': 'blood vessel',
        'UBERON:0001473': 'lymphatic vessel',
        'UBERON:0000178': 'blood',
        'UBERON:0007844': 'cartilage element',
        'UBERON:0001690': 'ear',
        'UBERON:0001987': 'placenta',
        'UBERON:0001911': 'mammary gland',
        'UBERON:0000007': 'pituitary gland',
        'UBERON:0016887': 'extraembryonic component',
        'UBERON:0001013': 'adipose tissue',
        'UBERON:0000310': 'breast',
        'UBERON:0000989': 'penis',
        'UBERON:0004288': 'skeleton',
        'UBERON:0000995': 'uterus',
        'UBERON:0000996': 'vagina',
        'UBERON:0000992': 'ovary',
        'UBERON:0000473': 'testis',
        'UBERON:0003509': 'arterial blood vessel',
        'UBERON:0001638': 'vein',
        'UBERON:0000160': 'intestine',
        'UBERON:0002384': 'connective tissue',
        'UBERON:0002101': 'limb',
        'UBERON:0000922': 'embryo',
        'UBERON:0000383': 'musculature of body',
        'UBERON:0001021': 'nerve',
        'UBERON:0002371': 'bone marrow',
        'UBERON:0006314': 'bodily fluid',
        'UBERON:0002049': 'vasculature',
        'UBERON:0000483': 'epithelium',
        'UBERON:0002407': 'pericardium',
        'UBERON:0001744': 'lymphoid tissue',
        'UBERON:0001155': 'colon',
        'UBERON:0003547': 'brain meninx',
        'UBERON:0001350': 'coccyx',
        'UBERON:0002368': 'endocrine gland',
        'UBERON:0002365': 'exocrine gland',
        'UBERON:0002073': 'hair follicle',
        'UBERON:0005057': 'immune organ',
        'UBERON:0001817': 'lacrimal gland',
        'UBERON:0002182': 'main bronchus',
        'UBERON:0001829': 'major salivary gland',
        'UBERON:0000414': 'mucous gland',
        'UBERON:0001821': 'sebaceous gland',
        'UBERON:0000998': 'seminal vesicle',
        'UBERON:0001820': 'sweat gland',
        'UBERON:0001471': 'skin of prepuce of penis'
    },

    'cell': {
        'CL:0000236': 'B cell',
        'EFO:0001640': 'B cell',  # B cell derived cell line
        'EFO:0001639': 'cancer cell',  # cancer cell line
        'CL:0002494': 'cardiocyte',
        'CL:0002320': 'connective tissue cell',
        'CL:0002321': 'embryonic cell',
        'CL:0000115': 'endothelial cell',
        'EFO:0005730': 'endothelial cell',  # endothelial cell derived cell line
        'CL:0000066': 'epithelial cell',
        'EFO:0001641': 'epithelial cell',  # epithelial cell derived cell line
        'CL:0000057': 'fibroblast',
        'EFO:0002009': 'fibroblast',  # fibroblast derived cell line
        'CL:0000988': 'hematopoietic cell',
        'EFO:0004905': 'induced pluripotent stem cell',
        'EFO:0005740': 'induced pluripotent stem cell',  # induced pluripotent stem cell derived cell line
        'CL:0000312': 'keratinocyte',
        'CL:0000738': 'leukocyte',
        'EFO:0005292': 'lymphoblast',  # lymphoblastoid cell line
        'CL:0000148': 'melanocyte',
        'CL:0000576': 'monocyte',
        'CL:0000763': 'myeloid cell',
        'CL:0000056': 'myoblast',
        'CL:0002319': 'neural cell',
        'EFO:0005214': 'neuroblastoma cell',  # neuroblastoma cell line
        'CL:0000669': 'pericyte',
        'CL:0000192': 'smooth muscle cell',
        'EFO:0005735': 'smooth muscle cell',  # smooth muscle cell derived cell line
        'CL:0000034': 'stem cell',
        'EFO:0002886': 'stem cell',  # stem cell derived cell line
        'CL:0000084': 'T cell',
        'NTR:0000550': 'progenitor cell'
    },

    'assay': {
        # Note shortened synonyms are provided
        'OBI:0000634': 'DNA methylation',  # 'DNA methylation profiling'
        'OBI:0000424': 'Transcription',  # 'transcription profiling'
        'OBI:0001398': 'DNA binding',  # "protein and DNA interaction"
        'OBI:0001854': 'RNA binding',  # "protein and RNA interaction"
        'OBI:0001917': '3D chromatin structure',  # 'chromosome conformation identification objective'
        'OBI:0000870': 'DNA accessibility',  # 'single-nucleotide-resolution nucleic acid structure mapping assay'
        'OBI:0001916': 'Replication timing',
        'OBI:0000435': 'Genotyping',
        'OBI:0000615': 'Proteomics',
        'OBI:0000626': 'DNA sequencing',
        'OBI:0000845': 'RNA structure',
        'OBI:0002082': 'Reporter assay',  # 'Reporter gene assay'
        'OBI:0002675': 'Massively parallel reporter assay',
        'NTR:0000520': 'CRISPR screen',
        'OBI:0000711': 'Library preparation',
        'NTR:0000675': 'Ribosome activity'
    },

    'preferred_name':  {
        'OBI:0002117': 'WGS',
        'OBI:0001247': 'genotyping HTS',
        'OBI:0001332': 'DNAme array',
        'OBI:0001335': 'microRNA counts',
        'OBI:0001463': 'RNA microarray',
        'OBI:0001863': 'WGBS',
        'OBI:0001923': 'MS-MS',
        'OBI:0001271': 'RNA-seq',
        'OBI:0000716': 'ChIP-seq',
        'OBI:0001853': 'DNase-seq',
        'OBI:0001920': 'Repli-seq',
        'OBI:0001864': 'RAMPAGE',
        'OBI:0001393': 'genotyping array',
        'OBI:0002042': 'Hi-C',
        'OBI:0002457': 'PRO-seq',
        'OBI:0002458': '4C',
        'OBI:0002629': 'direct RNA-seq',
        'OBI:0002144': 'Circulome-seq',
        'OBI:0002459': 'genotyping HiC',
        'OBI:0002675': 'MPRA',
        'OBI:0002571': 'polyA plus RNA-seq',
        'OBI:0002572': 'polyA minus RNA-seq',
        'OBI:0002631': 'scRNA-seq',
        'OBI:0002112': 'small RNA-seq',
        'OBI:0002083': 'enhancer reporter assay',
        'OBI:0002762': 'snATAC-seq',
        'OBI:0002764': 'scATAC-seq',
        'OBI:0002038': 'Ribo-seq',
        'OBI:0002984': 'capture Hi-C',
        'OBI:0003033': 'CUT&RUN',
        'OBI:0003034': 'CUT&Tag'
    },

    'category': {
        'OBI:0000634': 'DNA methylation profiling',
        'OBI:0000424': 'transcription profiling',
        'OBI:0000435': 'genotyping',
        'OBI:0000615': 'proteomics',
        'OBI:0001916': 'replication',
        'OBI:0001398': 'protein and DNA interaction',
        'OBI:0001854': 'protein and RNA interaction'
    },

    'objective': {
        'OBI:0000218': 'cellular feature identification objective',
        'OBI:0001691': 'cellular structure feature identification objective',
        'OBI:0001916': 'DNA replication identification objective',
        'OBI:0001917': 'chromosome conformation identification objective',
        'OBI:0001234': 'epigenetic modification identification objective',
        'OBI:0001331': 'transcription profiling identification objective',
        'OBI:0001690': 'molecular function identification objective',
        'OBI:0000268': 'organism feature identification objective',
        'OBI:0001623': 'organism identification objective',
        'OBI:0001398': 'protein and DNA interaction identification objective',
        'OBI:0001854': 'protein and RNA interaction identification objective'
    },

    'type': {
        'OBI:0001700': 'immunoprecipitation assay',
        'OBI:0000424': 'transcription profiling assay',
        'OBI:0000634': 'DNA methylation profiling assay',
        'OBI:0000435': 'genotyping assay'
    }

}


class Inspector(object):

    """ Class that includes methods for querying an RDFS/OWL ontology """

    def __init__(self, uri, language=''):
        super(Inspector, self).__init__()
        self.rdf_graph = ConjunctiveGraph()
        try:
            self.rdf_graph.parse(uri, format='application/rdf+xml')
        except HTTPError:
            print("This uri is not found:", uri)
        except Exception as e:
            print("Can't parse the file:", uri)
            print("Error:", e)

        self.allclasses = self.__getAllClasses()

    def __getAllClasses(self):

        classes = []
        classes.append(OWL.Thing)
        # subjuects that is type of class
        for s in self.rdf_graph.subjects(RDF.type, RDFS.Class):
            classes.append(s)
        for s in self.rdf_graph.subjects(RDF.type, OWL.Class):
            classes.append(s)
        for o in self.rdf_graph.objects(None, RDFS.domain):
            classes.append(o)
        for o in self.rdf_graph.objects(None, RDFS.range):
            classes.append(o)
        for s, v, o in self.rdf_graph.triples((None, RDFS.subClassOf, None)):
            classes.append(s)
            classes.append(o)
        for o in self.rdf_graph.objects(None, RDF.type):
            classes.append(o)

        classes = list(set(classes))
        return sort_uri_list_by_name(classes)

    # methods for getting ancestores and descendants of classes: by default, we do not include blank nodes
    def get_classDirectSupers(self, aClass, excludeBnodes=True):
        parents = set()
        for o in self.rdf_graph.objects(aClass, RDFS.subClassOf):
            if o != OWL.Thing:
                if excludeBnodes:
                    if type(o) != BNode:
                        parents.add(o)
                else:
                    parents.add(o)
        return list(parents)

    def getSynonyms(self, anEntity):

        synonyms = []
        # Uberon synonyms and EFO synonyms
        for o in self.rdf_graph.objects(anEntity, HAS_EXACT_SYNONYM):
            synonyms += [str(o)]
        # OBO synonyms
        for o in self.rdf_graph.objects(anEntity, ALTERNATIVE_TERM):
            synonyms += [str(o)]
        return synonyms


def sort_uri_list_by_name(uri_list):

    def get_last_bit(uri_string):
        if '#' in uri_string:
            x = uri_string.split('#')[1]
        else:
            x = uri_string.split('/')[-1]
        return x

    return sorted(uri_list, key=lambda uri: get_last_bit(str(uri)))


def getTermId(term):
    term_string = str(term)
    if '#' in term_string:
        term_id = term_string.split('#')[1]
    else:
        term_id = term_string.rsplit('/', 1)[1]
    return term_id.replace('_', ':')


def getAncestors(parents, terms, key):
    visited = []
    queue = parents.copy()
    while queue:
        ancestor = queue.pop()
        visited.append(ancestor)
        parents_of_ancestor = terms[ancestor][key]
        for parent in parents_of_ancestor:
            if parent not in visited and parent not in queue:
                queue.append(parent)
    return visited


def getBaseSlims(term, slimType, slim_candidates):
    base_slims = []
    slimTerms = SLIMS_DICT[slimType]
    for slimTerm_key in slimTerms:
        if slimTerm_key in slim_candidates:
            base_slims.append(slimTerms[slimTerm_key])
    if slimType in slim_shims:
        # Overrides all Ontology based-slims
        shims_override = slim_shims[slimType].get(term, [])
        if shims_override:
            return shims_override
    return base_slims


def getTermStructure():
    return {
        'id': '',
        'name': '',
        'preferred_name': '',
        'parents': [],
        'part_of': [],
        'has_part': [],
        'derives_from': [],
        'develops_from': [],
        'achieves_planned_objective': [],
        'organs': [],
        'cells': [],
        'closure': [],
        'slims': [],
        'data': [],
        'closure_with_develops_from': [],
        'data_with_develops_from': [],
        'synonyms': [],
        'category': [],
        'assay': [],
        'types': [],
        'objectives': []
    }


def get_downLoad_url(owl_file_name):
    ontology_repo = ONTOLOGY_ASSET_DICT[owl_file_name]['ontology_repo']
    asset_name = ONTOLOGY_ASSET_DICT[owl_file_name]['asset_name']
    ontology_url = 'https://api.github.com/repos/' + ontology_repo + '/releases/latest'
    download_url = None
    headers = CaseInsensitiveDict()
    headers['Accept'] = 'application/vnd.github.v3+json'
    response = requests.get(ontology_url, headers=headers)
    if response.status_code != 200:
        download_url = 'http://purl.obolibrary.org/obo/' + owl_file_name + '.owl'
        print(asset_name + ':', download_url)
        print(asset_name, 'release info not available \n')
        return download_url
    data = response.json()
    assets = data['assets']

    if assets:
        for asset in assets:
            if asset['name'] == asset_name:
                download_url = asset['browser_download_url']
                break
    else:
        download_url = 'http://purl.obolibrary.org/obo/' + owl_file_name + '.owl'

    print(asset_name + ':', download_url)
    print('release name: ' + data['name'])
    print('release tag: ' + data['tag_name'] + '\n')

    return download_url


def main():
    # Uberon multi-species anatomy ontology for biosample
    uberon_url = get_downLoad_url('uberon')
    # The Experimental Factor Ontology (EFO) for biosample
    efo_url = get_downLoad_url('efo')
    # Ontology for Biomedical Investigations for assays
    obi_url = get_downLoad_url('obi')
    # The Cell Line Ontology for cell line information for biosamples
    clo_url = get_downLoad_url('clo')
    # Human Disease Ontology for disease
    doid_url = get_downLoad_url('doid')

    whitelist = [uberon_url, efo_url, obi_url, doid_url]
    
    print("Generating ontology file...")
    terms = {}
    # Run on ontologies defined in whitelist
    for url in whitelist:
        data = Inspector(url)
        for c in data.allclasses:
            if type(c) == BNode:
                for o in data.rdf_graph.objects(c, RDFS.subClassOf):
                    if type(o) != BNode:
                        for o1 in data.rdf_graph.objects(c, OWL.intersectionOf):
                            collection = Collection(data.rdf_graph, o1)
                            col_list = []
                            for col in data.rdf_graph.objects(collection[1]):
                                col_list.append(col)
                            if HUMAN_TAXON in col_list:
                                if PART_OF in col_list:
                                    for subC in data.rdf_graph.objects(c, RDFS.subClassOf):
                                        term_id = getTermId(collection[0])
                                        if term_id not in terms:
                                            terms[term_id] = getTermStructure()
                                        terms[term_id]['part_of'].append(getTermId(subC))
                                elif DEVELOPS_FROM in col_list:
                                    for subC in data.rdf_graph.objects(c, RDFS.subClassOf):
                                        term_id = getTermId(collection[0])
                                        if term_id not in terms:
                                            terms[term_id] = getTermStructure()
                                        terms[term_id]['develops_from'].append(getTermId(subC))
            else:
                term_id = getTermId(c)
                if term_id not in terms:
                    terms[term_id] = getTermStructure()
                terms[term_id]['id'] = term_id
                terms[term_id]['name'] = str(data.rdf_graph.label(c))
                terms[term_id]['preferred_name'] = SLIMS_DICT['preferred_name'].get(term_id, '')
                # Get all parents
                for parent in data.get_classDirectSupers(c, excludeBnodes=False):
                    if type(parent) == BNode:
                        for s, v, o in data.rdf_graph.triples((parent, OWL.onProperty, None)):
                            if o == PART_OF:
                                for o1 in data.rdf_graph.objects(parent, OWL.someValuesFrom):
                                    if type(o1) != BNode:
                                        terms[term_id]['part_of'].append(getTermId(o1))
                            elif o == DEVELOPS_FROM:
                                for o1 in data.rdf_graph.objects(parent, OWL.someValuesFrom):
                                    if type(o1) != BNode:
                                        terms[term_id]['develops_from'].append(
                                            getTermId(o1))
                            elif o == HAS_PART:
                                for o1 in data.rdf_graph.objects(parent, OWL.someValuesFrom):
                                    if type(o1) != BNode:
                                        terms[term_id]['has_part'].append(
                                            getTermId(o1))
                            elif o == DERIVES_FROM:
                                for o1 in data.rdf_graph.objects(parent, OWL.someValuesFrom):
                                    if type(o1) != BNode:
                                        terms[term_id]['derives_from'].append(
                                            getTermId(o1))
                                    else:
                                        for o2 in data.rdf_graph.objects(o1, OWL.intersectionOf):
                                            for o3 in data.rdf_graph.objects(o2, RDF.first):
                                                if type(o3) != BNode:
                                                    terms[term_id]['derives_from'].append(
                                                        getTermId(o3))
                                            for o3 in data.rdf_graph.objects(o2, RDF.rest):
                                                for o4 in data.rdf_graph.objects(o3, RDF.first):
                                                    for o5 in data.rdf_graph.objects(o4, OWL.someValuesFrom):
                                                        for o6 in data.rdf_graph.objects(o5, OWL.intersectionOf):
                                                            for o7 in data.rdf_graph.objects(o6, RDF.first):
                                                                if type(o7) != BNode:
                                                                    terms[term_id]['derives_from'].append(
                                                                        getTermId(o7))
                                                                    for o8 in data.rdf_graph.objects(o6, RDF.rest):
                                                                        for o9 in data.rdf_graph.objects(o8, RDF.first):
                                                                            if type(o9) != BNode:
                                                                                terms[term_id]['derives_from'].append(
                                                                                    getTermId(o9))
                            elif o == ACHIEVES_PLANNED_OBJECTIVE:
                                for o1 in data.rdf_graph.objects(parent, OWL.someValuesFrom):
                                    if type(o1) != BNode:
                                        terms[term_id]['achieves_planned_objective'].append(
                                            getTermId(o1))
                    else:
                        terms[term_id]['parents'].append(getTermId(parent))
                terms[term_id]['synonyms'] = terms[term_id]['synonyms'] + data.getSynonyms(c)

    # Get only CLO terms from the CLO owl file
    data = Inspector(clo_url)
    for c in data.allclasses:
        if c.startswith('http://purl.obolibrary.org/obo/CLO'):
            term_id = getTermId(c)
            if term_id not in terms:
                terms[term_id] = getTermStructure()
                terms[term_id]['name'] = str(data.rdf_graph.label(c))
            terms[term_id]['synonyms'] = terms[term_id]['synonyms'] + data.getSynonyms(c)

    for term in terms:
        terms[term]['data'] = list(set(terms[term]['parents']) | set(terms[term]['part_of']) | set(
            terms[term]['derives_from']) | set(terms[term]['achieves_planned_objective']))
        terms[term]['data_with_develops_from'] = list(set(terms[term]['data']) | set(terms[term]['develops_from']))
    for term in terms:
        terms[term]['closure'] = getAncestors(terms[term]['data'], terms, 'data')
        terms[term]['closure_with_develops_from'] = getAncestors(
            terms[term]['data_with_develops_from'], terms, 'data_with_develops_from')
        terms[term]['closure'].append(term)
        terms[term]['closure_with_develops_from'].append(term)

        terms[term]['systems'] = getBaseSlims(term, 'system', terms[term]['closure'])
        terms[term]['organs'] = getBaseSlims(term, 'organ', terms[term]['closure'])
        terms[term]['cells'] = getBaseSlims(term, 'cell', terms[term]['closure'])
        terms[term]['developmental'] = getBaseSlims(term, 'developmental', terms[term]['closure_with_develops_from'])
        terms[term]['assay'] = getBaseSlims(term, 'assay', terms[term]['closure'])
        terms[term]['category'] = getBaseSlims(term, 'category', terms[term]['closure'])
        terms[term]['objectives'] = getBaseSlims(term, 'objective', terms[term]['closure'])
        terms[term]['types'] = getBaseSlims(term, 'type', terms[term]['closure'])

    for term in terms:
        del terms[term]['closure'], terms[term]['closure_with_develops_from']
        del terms[term]['parents'], terms[term]['develops_from']
        del terms[term]['has_part'], terms[term]['achieves_planned_objective']
        del terms[term]['id'], terms[term]['data'], terms[term]['data_with_develops_from']

    terms.update(ntr_assays)
    terms.update(ntr_biosamples)

    today = date.today().strftime('%Y-%m-%d')
    file_name = 'ontology-' + today + '.json'
    with open(file_name, 'w') as outfile:
        json.dump(terms, outfile)
    print('Ontology json file is generated:', file_name)


if __name__ == '__main__':
    main()
