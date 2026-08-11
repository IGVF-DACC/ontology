import requests
from urllib.error import HTTPError
from rdflib import ConjunctiveGraph, Namespace
from rdflib import RDFS, RDF, BNode, OWL
from rdflib.collection import Collection
from rdflib import namespace
import argparse
import gzip
import json
import os
import shutil
from datetime import date
from ontology.ntr_terms import (
    ntr_assays,
    ntr_biosamples
)
from ontology.manual_slims import manual_slims
from ontology.base_slims import base_slims
from ontology.ontology_assets import (
    METADATA_AUTHORITY,
    ONTOLOGY_ASSET_DICT,
    generation_ontology_keys,
    get_igvf_portal_ontology_files_dir,
    is_catalog_only,
)


IGVF_API_BASE = 'https://api.data.igvf.org'

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
DEFINITION = OBO['IAO_0000115']
COMMENT = RDFS.comment
OBOINOWL_DEPRECATED = OBO_OWL['deprecated']
OWL_DEPRECATED = OWL['deprecated']
OBOINOWL_OBSOLETE_CLASS = OBO_OWL['ObsoleteClass']


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

    def __init__(self, uri, comments=False):
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
        self.definitions = self.__get_all_definitions()
        if comments:
            self.comments = self.__get_all_comments()

    def __is_obsolete(self, subject):
        # Check for owl:deprecated true or oboInOwl:deprecated true
        for predicate in [OWL.deprecated, OBOINOWL_DEPRECATED]:
            for _, _, obj in self.rdf_graph.triples((subject, predicate, None)):
                if str(obj).lower() == "true":
                    return True

        # Check if class is a subclass of oboInOwl:ObsoleteClass
        for _, _, obj in self.rdf_graph.triples((subject, RDFS.subClassOf, OBOINOWL_OBSOLETE_CLASS)):
            return True

        # Check if the label starts with "obsolete:"
        for _, _, label in self.rdf_graph.triples((subject, RDFS.label, None)):
            if str(label).lower().startswith("obsolete:"):
                return True

        return False

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
        non_obsolete_classes = [cls for cls in classes if not self.__is_obsolete(cls)]
        return sort_uri_list_by_name(non_obsolete_classes)
    
    def __get_all_definitions(self):
        definitions = {}
        for subj, definition in self.rdf_graph.subject_objects(predicate=DEFINITION):
            definitions[getTermId(subj)] = str(definition)
        return definitions
    
    def __get_all_comments(self):
        comments = {}
        for subj, comment in self.rdf_graph.subject_objects(predicate=COMMENT):
            if getTermId(subj) not in comments:
               comments[getTermId(subj)] = [str(comment)]
            else:
                comments[getTermId(subj)].append(str(comment))
        return comments

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
        return list(set(synonyms))


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
        return term_string.split('#')[1].replace('_', ':')
    elif '/' in term_string:
        return term_string.rsplit('/', 1)[1].replace('_', ':')
    return term_string


def can_set_metadata(term_id, ontology_key):
    """Return True if this file may set name/definition for term_id."""
    if ':' not in term_id:
        return True
    prefix = term_id.split(':', 1)[0]
    authority = METADATA_AUTHORITY.get(prefix)
    if authority is None:
        return True
    return authority == ontology_key


def apply_term_metadata(terms, term_id, data, label_subject, ontology_key):
    """Set name/definition/preferred_name according to namespace authority rules."""
    if not can_set_metadata(term_id, ontology_key):
        return

    prefix = term_id.split(':', 1)[0] if ':' in term_id else None
    if term_id in data.definitions:
        if prefix in METADATA_AUTHORITY:
            terms[term_id]['definition'] = data.definitions[term_id]
        elif not terms[term_id].get('definition'):
            terms[term_id]['definition'] = data.definitions[term_id]

    label = str(data.rdf_graph.value(label_subject, namespace.RDFS.label, default=''))
    if label:
        terms[term_id]['name'] = label

    if PREFERRED_NAME.get(term_id):
        terms[term_id]['preferred_name'] = PREFERRED_NAME.get(term_id)


def getAncestors(parents, terms, key):
    visited = []
    queue = parents.copy()
    while queue:
        ancestor = queue.pop()
        # ancestor can be obsolete, then ignore it
        if ancestor in terms:
            visited.append(ancestor)
            parents_of_ancestor = terms[ancestor][key]
            for parent in parents_of_ancestor:
                if parent not in visited and parent not in queue:
                    queue.append(parent)
    return list(set(visited))


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
    return list(set(base_slim_names))

def get_igvf_released_file(file_set_accession):
    """Return the released reference-file object from an IGVF curated set."""
    url = f'{IGVF_API_BASE}/curated-sets/{file_set_accession}/'
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    files = response.json().get('files') or []
    released = [f for f in files if f.get('status') == 'released']
    if not released:
        raise RuntimeError(
            f'No released file found in curated set {file_set_accession}'
        )
    if len(released) > 1:
        accessions = ', '.join(f.get('accession', '?') for f in released)
        raise RuntimeError(
            f'Expected one released file in curated set {file_set_accession}, '
            f'found {len(released)}: {accessions}'
        )
    return released[0]


def get_igvf_download_url(file_obj):
    """Build absolute download URL from an IGVF file object's href."""
    href = file_obj.get('href')
    if not href:
        raise RuntimeError(
            f"Released file {file_obj.get('accession')} has no href"
        )
    if href.startswith('http://') or href.startswith('https://'):
        return href
    return IGVF_API_BASE + href


def download_and_gunzip_ontology_file(url, local_path):
    """Download a gzipped ontology file from IGVF and write the unzipped OWL/OBO."""
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    gzip_path = local_path + '.gz'
    print(f'Downloading {url}')
    print(f'Saving gzip to {gzip_path}')
    response = requests.get(url, stream=True, timeout=600)
    response.raise_for_status()
    with open(gzip_path, 'wb') as outfile:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                outfile.write(chunk)

    print(f'Unzipping to {local_path}\n')
    with gzip.open(gzip_path, 'rb') as src, open(local_path, 'wb') as dst:
        shutil.copyfileobj(src, dst, length=1024 * 1024)
    return local_path


def get_local_ontology_path(owl_file_name, force=False):
    """Return local OWL/OBO path from IGVF portal cache, downloading if needed."""
    if is_catalog_only(owl_file_name):
        raise ValueError(
            f'{owl_file_name} is catalog_only and is not used by generate_ontology'
        )

    asset = ONTOLOGY_ASSET_DICT[owl_file_name]
    local_file_name = asset['local_file_name']
    local_path = os.path.join(
        get_igvf_portal_ontology_files_dir(),
        local_file_name,
    )

    if os.path.isfile(local_path) and not force:
        print(f'Using cached file: {local_path}\n')
        return local_path

    file_set = asset['file_set']
    released_file = get_igvf_released_file(file_set)
    download_url = get_igvf_download_url(released_file)
    print(
        f"{local_file_name}: curated set {file_set}, "
        f"released file {released_file.get('accession')}"
    )
    return download_and_gunzip_ontology_file(download_url, local_path)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description='Generate ontology JSON from IGVF portal ontology files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s
  %(prog)s --force-download""",
    )
    parser.add_argument(
        '--force-download',
        action='store_true',
        help=(
            'Re-download ontology files from the IGVF portal even when cached '
            'copies exist in ontology_files_from_igvf_portal/.'
        ),
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    force_download = args.force_download

    whitelist = []
    for ontology_key in generation_ontology_keys():
        path = get_local_ontology_path(ontology_key, force=force_download)
        whitelist.append((ontology_key, path))

    # CLO is excluded from the main whitelist and handled separately below.
    clo_path = get_local_ontology_path('clo', force=force_download)

    print("Generating ontology file...")
    terms = {}
    # Run on ontologies defined in whitelist
    for ontology_key, path in whitelist:
        print("Processing file from:", path)
        data = Inspector(path)
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
                                        apply_term_metadata(
                                            terms, term_id, data, collection[0], ontology_key
                                        )
                                        terms[term_id]['part_of'] = terms[term_id].get('part_of', []) + [getTermId(subC)]
                                elif DEVELOPS_FROM in col_list:
                                    for subC in data.rdf_graph.objects(c, RDFS.subClassOf):
                                        term_id = getTermId(collection[0])
                                        if term_id not in terms:
                                            terms[term_id] = {}
                                        apply_term_metadata(
                                            terms, term_id, data, collection[0], ontology_key
                                        )
                                        terms[term_id]['develops_from'] = terms[term_id].get('develops_from', []) + [getTermId(subC)]
            else:
                term_id = getTermId(c)
                if term_id not in terms:
                    terms[term_id] = {}
                apply_term_metadata(terms, term_id, data, c, ontology_key)
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
                    terms[term_id]['synonyms'] = list(set(terms[term_id].get('synonyms', []) + synonyms))

    # Get only CLO terms from the CLO owl file
    print("Processing file from:", clo_path)
    data = Inspector(clo_path, comments=True)
    for c in data.allclasses:
        if c.startswith('http://purl.obolibrary.org/obo/CLO'):
            term_id = getTermId(c)
            if term_id not in terms:
                terms[term_id] = {}
                if term_id in data.comments:
                    terms[term_id]['comments'] = data.comments[term_id]
            apply_term_metadata(terms, term_id, data, c, 'clo')
            synonyms = data.getSynonyms(c)
            if synonyms:
                terms[term_id]['synonyms'] = list(set(terms[term_id].get('synonyms', []) + synonyms))
    
    for term in terms:
        terms[term]['data'] = list(set(terms[term].get('parents', [])) | set(terms[term].get('part_of', [])) | set(
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
        keys_to_remove = ['closure', 'parents', 'develops_from', 'has_part', 'achieves_planned_objective', 
            'data', 'data_with_develops_from', 'part_of', 'derives_from']
        for key in keys_to_remove:
            terms[term].pop(key, None)

        ancestors = []
        for term_id in terms[term]['closure_with_develops_from']:
            term_label = terms[term_id].get('name', '')
            if term_label:
                ancestors.append(term_label)
        if ancestors:
            terms[term]['ancestors'] = list(set(ancestors))
        terms[term].pop('closure_with_develops_from', None)

    terms.update(ntr_assays)
    terms.update(ntr_biosamples)

    today = date.today().strftime('%Y-%m-%d')
    file_name = 'ontology-' + today + '.json'
    with open(file_name, 'w') as outfile:
        json.dump(terms, outfile)
    print('Ontology json file is generated:', file_name)


if __name__ == '__main__':
    main()
