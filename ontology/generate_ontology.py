import requests
from requests.structures import CaseInsensitiveDict
from urllib.error import HTTPError
from rdflib import ConjunctiveGraph, Namespace
from rdflib import RDFS, RDF, BNode, OWL
from rdflib.collection import Collection
import json
from datetime import date
from ontology.ntr_terms import (
    ntr_assays,
    ntr_biosamples
)
from ontology.manual_slims import manual_slims
from ontology.base_slims import base_slims


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
        'asset_name': 'composite-metazoan.owl',
        'uri': 'http://purl.obolibrary.org/obo/uberon.owl'
    },
    'efo': {
        'ontology_repo': 'EBISPOT/efo',
        'asset_name': 'efo.owl',
        'uri': 'http://www.ebi.ac.uk/efo/efo.owl'
    },
    'mondo': {
        'ontology_repo': 'monarch-initiative/mondo',
        'asset_name': 'mondo.owl',
        'uri': 'http://purl.obolibrary.org/obo/mondo.owl'
    },
    'oba': {
        'ontology_repo': 'obophenotype/bio-attribute-ontology',
        'asset_name': 'oba.owl',
        'uri': 'http://purl.obolibrary.org/obo/oba.owl'
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
    },
    'hp': {
        'ontology_repo': 'obophenotype/human-phenotype-ontology',
        'asset_name': 'hp.owl',
        'uri': 'http://purl.obolibrary.org/obo/hp.owl'
    }
}

PREFERRED_NAME = {
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
    base_slim_names = []
    slimTerms = base_slims[slimType]
    for slimTerm_key in slimTerms:
        if slimTerm_key in slim_candidates:
            base_slim_names.append(slimTerms[slimTerm_key])
    if slimType in manual_slims:
        # Overrides all Ontology based-slims
        shims_override = manual_slims[slimType].get(term, [])
        if shims_override:
            return shims_override
    return base_slim_names

def get_downLoad_url(owl_file_name):
    ontology_repo = ONTOLOGY_ASSET_DICT[owl_file_name]['ontology_repo']
    asset_name = ONTOLOGY_ASSET_DICT[owl_file_name]['asset_name']
    ontology_url = 'https://api.github.com/repos/' + ontology_repo + '/releases/latest'
    download_url = None
    data = None
    headers = CaseInsensitiveDict()
    headers['Accept'] = 'application/vnd.github.v3+json'
    response = requests.get(ontology_url, headers=headers)
    if response.status_code == 200:    
        data = response.json()
        assets = data['assets']
        if assets:
            for asset in assets:
                if asset['name'] == asset_name:
                    download_url = asset['browser_download_url']
                    break
    if not download_url:
        download_url = ONTOLOGY_ASSET_DICT[owl_file_name]['uri']

    print(asset_name + ':', download_url)
    if data:
        print('release name: ' + data['name'])
        print('release tag: ' + data['tag_name'] + '\n')
    else:
        print('release info: not available \n')

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
    # The Human Phenotype Ontology (HPO) for disease
    hp_url = get_downLoad_url('hp')
    # Mondo Disease Ontology for disease
    mondo_url = get_downLoad_url('mondo')
    # Ontology of Biological Attributes covering all kingdoms of life
    oba_url = get_downLoad_url('oba')

    whitelist = [uberon_url, efo_url, obi_url, doid_url, hp_url, mondo_url, oba_url]
    
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
                                            terms[term_id] = {}
                                        terms[term_id]['part_of'] = terms[term_id].get('part_of', []) + [getTermId(subC)]
                                elif DEVELOPS_FROM in col_list:
                                    for subC in data.rdf_graph.objects(c, RDFS.subClassOf):
                                        term_id = getTermId(collection[0])
                                        if term_id not in terms:
                                            terms[term_id] = {}
                                        terms[term_id]['develops_from'] = terms[term_id].get('develops_from', []) + [getTermId(subC)]
            else:
                term_id = getTermId(c)
                if term_id not in terms:
                    terms[term_id] = {}
                terms[term_id]['id'] = term_id
                if str(data.rdf_graph.label(c)):
                    terms[term_id]['name'] = str(data.rdf_graph.label(c))
                if PREFERRED_NAME.get(term_id):
                    terms[term_id]['preferred_name'] = PREFERRED_NAME.get(term_id)
                # Get all parents
                for parent in data.get_classDirectSupers(c, excludeBnodes=False):
                    if type(parent) == BNode:
                        for s, v, o in data.rdf_graph.triples((parent, OWL.onProperty, None)):
                            if o == PART_OF:
                                for o1 in data.rdf_graph.objects(parent, OWL.someValuesFrom):
                                    if type(o1) != BNode:
                                        terms[term_id]['part_of'] = terms[term_id].get('part_of', []) + [getTermId(o1)]
                            elif o == DEVELOPS_FROM:
                                for o1 in data.rdf_graph.objects(parent, OWL.someValuesFrom):
                                    if type(o1) != BNode:
                                        terms[term_id]['develops_from'] = terms[term_id].get('develops_from', []) + [getTermId(o1)]
                            elif o == HAS_PART:
                                for o1 in data.rdf_graph.objects(parent, OWL.someValuesFrom):
                                    if type(o1) != BNode:
                                        terms[term_id]['has_part'] = terms[term_id].get('has_part', []) + [getTermId(o1)]
                            elif o == DERIVES_FROM:
                                for o1 in data.rdf_graph.objects(parent, OWL.someValuesFrom):
                                    if type(o1) != BNode:
                                        terms[term_id]['derives_from'] = terms[term_id].get('derives_from', []) + [getTermId(o1)]
                                    else:
                                        for o2 in data.rdf_graph.objects(o1, OWL.intersectionOf):
                                            for o3 in data.rdf_graph.objects(o2, RDF.first):
                                                if type(o3) != BNode:
                                                    terms[term_id]['derives_from'] = terms[term_id].get('derives_from', []) + [getTermId(o3)]
                                            for o3 in data.rdf_graph.objects(o2, RDF.rest):
                                                for o4 in data.rdf_graph.objects(o3, RDF.first):
                                                    for o5 in data.rdf_graph.objects(o4, OWL.someValuesFrom):
                                                        for o6 in data.rdf_graph.objects(o5, OWL.intersectionOf):
                                                            for o7 in data.rdf_graph.objects(o6, RDF.first):
                                                                if type(o7) != BNode:
                                                                    terms[term_id]['derives_from'] = terms[term_id].get('derives_from', []) + [getTermId(o7)]
                                                                    for o8 in data.rdf_graph.objects(o6, RDF.rest):
                                                                        for o9 in data.rdf_graph.objects(o8, RDF.first):
                                                                            if type(o9) != BNode:
                                                                                terms[term_id]['derives_from'] = terms[term_id].get('derives_from', []) + [getTermId(o9)]
                            elif o == ACHIEVES_PLANNED_OBJECTIVE:
                                for o1 in data.rdf_graph.objects(parent, OWL.someValuesFrom):
                                    if type(o1) != BNode:
                                        terms[term_id]['achieves_planned_objective'] = terms[term_id].get('achieves_planned_objective', []) + [getTermId(o1)]
                    else:
                        terms[term_id]['parents'] = terms[term_id].get('parents', []) + [getTermId(parent)]
                synonyms = data.getSynonyms(c)
                if synonyms:
                    terms[term_id]['synonyms'] = terms[term_id].get('synonyms', []) + synonyms

    # Get only CLO terms from the CLO owl file
    data = Inspector(clo_url)
    for c in data.allclasses:
        if c.startswith('http://purl.obolibrary.org/obo/CLO'):
            term_id = getTermId(c)
            if term_id not in terms:
                terms[term_id] = {}
                if str(data.rdf_graph.label(c)):
                    terms[term_id]['name'] = str(data.rdf_graph.label(c))
            synonyms = data.getSynonyms(c)
            if synonyms:
                terms[term_id]['synonyms'] = terms[term_id].get('synonyms', []) + synonyms

    for term in terms:
        terms[term]['data'] = list(set(terms[term].get('parents', [])) | set(terms[term].get('  ', [])) | set(
            terms[term].get('derives_from', [])) | set(terms[term].get('achieves_planned_objective', [])))
        terms[term]['data_with_develops_from'] = list(set(terms[term].get('data', [])) | set(terms[term].get('develops_from', [])))
    for term in terms:
        terms[term]['closure'] = getAncestors(terms[term]['data'], terms, 'data')
        terms[term]['closure_with_develops_from'] = getAncestors(
            terms[term]['data_with_develops_from'], terms, 'data_with_develops_from')
        terms[term]['closure'].append(term)
        terms[term]['closure_with_develops_from'].append(term)

        keys = ['systems', 'organs', 'cells', 'assay', 'category', 'objectives', 'types']
        for key in keys:
            value = getBaseSlims(term, key, terms[term]['closure'])
            if value:
                terms[term][key] = value
        
        developmental = getBaseSlims(term, 'developmental', terms[term]['closure_with_develops_from'])
        if developmental:
            terms[term]['developmental'] = developmental

    for term in terms:
        keys_to_remove = ['closure', 'closure_with_develops_from', 'parents', 'develops_from', 'has_part', 'achieves_planned_objective', 
            'id', 'data', 'data_with_develops_from', 'part_of', 'derives_from']
        for key in keys_to_remove:
            terms[term].pop(key, None)

    terms.update(ntr_assays)
    terms.update(ntr_biosamples)

    today = date.today().strftime('%Y-%m-%d')
    file_name = 'ontology-' + today + '.json'
    with open(file_name, 'w') as outfile:
        json.dump(terms, outfile)
    print('Ontology json file is generated:', file_name)


if __name__ == '__main__':
    main()
