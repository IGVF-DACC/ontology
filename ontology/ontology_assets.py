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


def get_igvf_portal_ontology_files_dir():
    """Return repo-root ontology_files_from_igvf_portal/ cache directory."""
    repo_root = os.path.dirname(get_ontology_files_dir())
    return os.path.join(repo_root, 'ontology_files_from_igvf_portal')


ONTOLOGY_ASSET_DICT = {
    'uberon': {
        'local_file_name': 'uberon.owl',
        'uri': 'http://purl.obolibrary.org/obo/uberon.owl',
        'ols_id': 'uberon',
        'file_set': 'IGVFDS2035XPMB',
    },
    'cl': {
        'local_file_name': 'cl.owl',
        'uri': 'http://purl.obolibrary.org/obo/cl.owl',
        'ols_id': 'cl',
        'file_set': 'IGVFDS2588RYXK',
    },
    'efo': {
        'local_file_name': 'efo.owl',
        'uri': 'http://www.ebi.ac.uk/efo/efo.owl',
        'ols_id': 'efo',
        'file_set': 'IGVFDS6003FOMG',
    },
    'mondo': {
        'local_file_name': 'mondo.owl',
        'uri': 'http://purl.obolibrary.org/obo/mondo.owl',
        'ols_id': 'mondo',
        'file_set': 'IGVFDS7295JLJQ',
    },
    'oba': {
        'local_file_name': 'oba.owl',
        'uri': 'http://purl.obolibrary.org/obo/oba.owl',
        'ols_id': 'oba',
        'file_set': 'IGVFDS0967KVGP',
    },
    'obi': {
        'local_file_name': 'obi.owl',
        'uri': 'http://purl.obolibrary.org/obo/obi.owl',
        'ols_id': 'obi',
        'file_set': 'IGVFDS2602QLHH',
    },
    'clo': {
        # Downloaded for generation, but processed in a dedicated CLO-only pass.
        'local_file_name': 'clo.owl',
        'uri': 'http://purl.obolibrary.org/obo/clo.owl',
        'ols_id': 'clo',
        'file_set': 'IGVFDS7562BUEW',
        'in_whitelist': False,
    },
    'doid': {
        'local_file_name': 'doid.owl',
        'uri': 'http://purl.obolibrary.org/obo/doid.owl',
        'ols_id': 'doid',
        'file_set': 'IGVFDS0076IZRZ',
    },
    'hp': {
        'local_file_name': 'hp.owl',
        'uri': 'http://purl.obolibrary.org/obo/hp.owl',
        'ols_id': 'hp',
        'file_set': 'IGVFDS5350TOZO',
    },
    'ncit': {
        'local_file_name': 'ncit.owl',
        'uri': 'http://purl.obolibrary.org/obo/ncit.owl',
        'ols_id': 'ncit',
        'file_set': 'IGVFDS6069UIHS',
    },
    'pcl': {
        'local_file_name': 'pcl.owl',
        'uri': 'http://purl.obolibrary.org/obo/pcl.owl',
        'ols_id': 'pcl',
        'file_set': 'IGVFDS4687SYMS',
    },
    'go': {
        'local_file_name': 'go.owl',
        'uri': 'https://purl.obolibrary.org/obo/go.owl',
        'ols_id': 'go',
        'file_set': 'IGVFDS9239KXAX',
    },
    'bao': {
        # Complete BAO OWL; not on OBO PURL. OLS id is "bao".
        # Official host often times out for scripted downloads; use GitHub mirror.
        'local_file_name': 'bao_complete.owl',
        'uri': 'https://www.bioassayontology.org/bao/bao_complete.owl',
        'download_uri': 'https://raw.githubusercontent.com/BioAssayOntology/BAO/master/bao_complete.owl',
        'ols_id': 'bao',
        'file_set': 'IGVFDS4680UUQJ',
    },
    'chebi': {
        # Full OWL ~826MB; download official .owl.gz (~66MB) instead.
        'local_file_name': 'chebi.owl',
        'uri': 'http://purl.obolibrary.org/obo/chebi.owl',
        'download_uri': 'http://purl.obolibrary.org/obo/chebi.owl.gz',
        'ols_id': 'chebi',
        'file_set': 'IGVFDS0762GKJU',
        'catalog_only': True,
    },
    'vario': {
        'local_file_name': 'vario.owl',
        'uri': 'http://purl.obolibrary.org/obo/vario.owl',
        'ols_id': 'vario',
        'file_set': 'IGVFDS3622SSGR',
        'catalog_only': True,
    },
    'orphanet': {
        # ORDO; OLS ontology id is "ordo".
        'local_file_name': 'ordo_orphanet.owl',
        'uri': 'https://www.orphadata.com/data/ontologies/ordo/last_version/ordo_orphanet.owl',
        'ols_id': 'ordo',
        'file_set': 'IGVFDS9088SLTK',
        'catalog_only': True,
    },
    'cellosaurus': {
        # No OWL release; ExPASy publishes OBO. Not in OLS.
        'local_file_name': 'cellosaurus.obo',
        'uri': 'https://ftp.expasy.org/databases/cellosaurus/cellosaurus.obo',
        'ols_id': None,
        'file_set': 'IGVFDS3922HDSH',
        'catalog_only': True,
    },
}


# Term prefixes that must take name/definition only from their own ontology file.
# Only includes ontologies loaded by generate_ontology (not catalog_only).
METADATA_AUTHORITY = {
    'UBERON': 'uberon',
    'CL': 'cl',
    'EFO': 'efo',
    'MONDO': 'mondo',
    'OBA': 'oba',
    'OBI': 'obi',
    'CLO': 'clo',
    'DOID': 'doid',
    'HP': 'hp',
    'NCIT': 'ncit',
    'PCL': 'pcl',
    'GO': 'go',
    'BAO': 'bao',
}


def get_ols_ontology_id(ontology_key: str):
    """Return OLS ontology id for ontology_key, or None if not in OLS."""
    return ONTOLOGY_ASSET_DICT[ontology_key].get('ols_id')


def is_catalog_only(ontology_key: str) -> bool:
    """True if the ontology is downloaded/cataloged but not used in generation."""
    return bool(ONTOLOGY_ASSET_DICT[ontology_key].get('catalog_only'))


def generation_ontology_keys():
    """Ontology keys used in the main generate_ontology whitelist.

    Excludes catalog-only assets and ontologies handled in dedicated passes
    (e.g. CLO with in_whitelist=False).
    """
    return [
        key
        for key, asset in ONTOLOGY_ASSET_DICT.items()
        if not is_catalog_only(key) and asset.get('in_whitelist', True)
    ]
