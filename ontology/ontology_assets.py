"""Shared ontology source config and local cache path helpers."""

import os


def get_ontology_files_dir():
    """Return repo-root ontology_files/ (works when installed in site-packages)."""
    for start in (os.getcwd(), os.path.dirname(__file__)):
        path = os.path.abspath(start)
        while True:
            if os.path.isfile(os.path.join(path, 'setup.py')):
                return os.path.join(path, 'ontology_files')
            parent = os.path.dirname(path)
            if parent == path:
                break
            path = parent

    return os.path.join(os.getcwd(), 'ontology_files')


ONTOLOGY_ASSET_DICT = {
    'uberon': {
        'local_file_name': 'uberon.owl',
        'uri': 'http://purl.obolibrary.org/obo/uberon.owl',
        'ols_id': 'uberon',
    },
    'cl': {
        'local_file_name': 'cl.owl',
        'uri': 'http://purl.obolibrary.org/obo/cl.owl',
        'ols_id': 'cl',
    },
    'efo': {
        'local_file_name': 'efo.owl',
        'uri': 'http://www.ebi.ac.uk/efo/efo.owl',
        'ols_id': 'efo',
    },
    'mondo': {
        'local_file_name': 'mondo.owl',
        'uri': 'http://purl.obolibrary.org/obo/mondo.owl',
        'ols_id': 'mondo',
    },
    'oba': {
        'local_file_name': 'oba.owl',
        'uri': 'http://purl.obolibrary.org/obo/oba.owl',
        'ols_id': 'oba',
    },
    'obi': {
        'local_file_name': 'obi.owl',
        'uri': 'http://purl.obolibrary.org/obo/obi.owl',
        'ols_id': 'obi',
    },
    'clo': {
        'local_file_name': 'clo.owl',
        'uri': 'http://purl.obolibrary.org/obo/clo.owl',
        'ols_id': 'clo',
    },
    'doid': {
        'local_file_name': 'doid.owl',
        'uri': 'http://purl.obolibrary.org/obo/doid.owl',
        'ols_id': 'doid',
    },
    'hp': {
        'local_file_name': 'hp.owl',
        'uri': 'http://purl.obolibrary.org/obo/hp.owl',
        'ols_id': 'hp',
    },
    'ncit': {
        'local_file_name': 'ncit.owl',
        'uri': 'http://purl.obolibrary.org/obo/ncit.owl',
        'ols_id': 'ncit',
    },
    'pcl': {
        'local_file_name': 'pcl.owl',
        'uri': 'http://purl.obolibrary.org/obo/pcl.owl',
        'ols_id': 'pcl',
    },
    'go': {
        'local_file_name': 'go.owl',
        'uri': 'https://purl.obolibrary.org/obo/go.owl',
        'ols_id': 'go',
    },
    'chebi': {
        'local_file_name': 'chebi.owl',
        'uri': 'http://purl.obolibrary.org/obo/chebi.owl',
        'ols_id': 'chebi',
        'catalog_only': True,
    },
    'vario': {
        'local_file_name': 'vario.owl',
        'uri': 'http://purl.obolibrary.org/obo/vario.owl',
        'ols_id': 'vario',
        'catalog_only': True,
    },
    'orphanet': {
        # ORDO; OLS ontology id is "ordo".
        'local_file_name': 'ordo_orphanet.owl',
        'uri': 'https://www.orphadata.com/data/ontologies/ordo/last_version/ordo_orphanet.owl',
        'ols_id': 'ordo',
        'catalog_only': True,
    },
    'cellosaurus': {
        # No OWL release; ExPASy publishes OBO. Not in OLS.
        'local_file_name': 'cellosaurus.obo',
        'uri': 'https://ftp.expasy.org/databases/cellosaurus/cellosaurus.obo',
        'ols_id': None,
        'catalog_only': True,
    },
}



def get_ols_ontology_id(ontology_key: str):
    """Return OLS ontology id for ontology_key, or None if not in OLS."""
    return ONTOLOGY_ASSET_DICT[ontology_key].get('ols_id')


def is_catalog_only(ontology_key: str) -> bool:
    """True if the ontology is downloaded/cataloged but not used in generation."""
    return bool(ONTOLOGY_ASSET_DICT[ontology_key].get('catalog_only'))


def generation_ontology_keys():
    """Ontology keys used by generate_ontology (excludes catalog-only assets)."""
    return [
        key
        for key in ONTOLOGY_ASSET_DICT
        if not is_catalog_only(key)
    ]
