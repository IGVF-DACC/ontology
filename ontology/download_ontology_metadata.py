#!/usr/bin/env python3
"""Download latest ontology OWL files and write per-file metadata JSON.

Uses shared source config from ontology.ontology_assets.

Download:
  Always use ONTOLOGY_ASSET_DICT uri (OBO PURL or other canonical URL).

Version:
  1. Cellosaurus: https://api.cellosaurus.org/release-info
  2. EBI OLS4 API: version, else parse config.versionIri
  3. Fallback: HTTP Last-Modified of the download URL

Modes:
  default   Resolve release metadata, download OWL files, write metadata JSON
  --dry-run Resolve release metadata and write metadata JSON only (no download)

Examples:
  python -m ontology.download_ontology_metadata
  python -m ontology.download_ontology_metadata --dry-run
  python -m ontology.download_ontology_metadata -o ontology_files_metadata.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime

import requests

from ontology.ontology_assets import (
    ONTOLOGY_ASSET_DICT,
    get_ols_ontology_id,
    get_ontology_files_dir,
)


DEFAULT_AWARD = '/awards/Community/'
DEFAULT_LAB = '/labs/community/'
OLS_ONTOLOGY_URL = 'https://www.ebi.ac.uk/ols4/api/ontologies/{ols_id}'
CELLOSAURUS_RELEASE_INFO_URL = 'https://api.cellosaurus.org/release-info'


def get_release_info(owl_file_name: str) -> dict:
    """Resolve download URL and version metadata for one ontology.

    How release info is obtained:
    1. download_url / source_url: always ONTOLOGY_ASSET_DICT uri
       (PURL when available, else canonical host such as Orphadata / ExPASy).
    2. version:
       - cellosaurus: GET https://api.cellosaurus.org/release-info
       - others: OLS4 version, else parse config.versionIri
       - fallback: HTTP Last-Modified
    """
    asset = ONTOLOGY_ASSET_DICT[owl_file_name]
    local_file_name = asset['local_file_name']
    source_url = asset['uri']
    download_url = source_url

    if owl_file_name == 'cellosaurus':
        version = get_cellosaurus_version()
    else:
        version = get_ols_version(owl_file_name)
    if not version:
        print(f'No version found for {owl_file_name}. Using HTTP Last-Modified.')
        version = get_http_last_modified_version(download_url)

    print(f'{local_file_name}: {download_url}')
    if version:
        print(f'version: {version}')
    print()

    return {
        'local_file_name': local_file_name,
        'source_url': source_url,
        'download_url': download_url,
        'version': version,
    }


def get_cellosaurus_version() -> str | None:
    """Return Cellosaurus release version from api.cellosaurus.org."""
    try:
        response = requests.get(CELLOSAURUS_RELEASE_INFO_URL, timeout=60)
        if response.status_code != 200:
            return None
        data = response.json()
    except requests.RequestException:
        return None

    release = (
        data.get('Cellosaurus', {})
        .get('header', {})
        .get('release', {})
    )
    version = release.get('version')
    if version:
        return str(version).strip() or None
    return None


def get_ols_version(ontology_key: str) -> str | None:
    """Return ontology version from EBI OLS4, if available."""
    ols_id = get_ols_ontology_id(ontology_key)
    if not ols_id:
        return None

    url = OLS_ONTOLOGY_URL.format(ols_id=ols_id)
    try:
        response = requests.get(url, timeout=60)
        if response.status_code != 200:
            return None
        data = response.json()
    except requests.RequestException:
        return None

    config = data.get('config') or {}
    version = data.get('version') or config.get('version')
    if version:
        return str(version).strip() or None

    return version_from_iri(config.get('versionIri'))


def version_from_iri(version_iri: str | None) -> str | None:
    """Extract a release stamp from an OWL versionIRI when version is empty."""
    if not version_iri:
        return None

    match = re.search(r'/releases/([^/]+)/', version_iri)
    if match:
        return match.group(1).lstrip('v')

    match = re.search(r'ORDO_en_([0-9.]+)', version_iri, re.IGNORECASE)
    if match:
        return match.group(1).rstrip('.')

    # e.g. http://purl.obolibrary.org/obo/chebi/253/chebi.owl
    # or    http://purl.obolibrary.org/obo/obi/2026-05-08/obi.owl
    match = re.search(r'/obo/[A-Za-z0-9_]+/([^/]+)/', version_iri)
    if match and match.group(1).lower() != 'releases':
        return match.group(1)

    return None


def get_http_last_modified_version(url: str) -> str | None:
    """Return YYYY-MM-DD from HTTP Last-Modified when OLS has no version."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=60)
        last_modified = response.headers.get('Last-Modified')
        if not last_modified:
            # Some hosts do not support HEAD; try a ranged GET
            response = requests.get(
                url,
                headers={'Range': 'bytes=0-0'},
                allow_redirects=True,
                timeout=60,
            )
            last_modified = response.headers.get('Last-Modified')
        if last_modified:
            return last_modified_to_date(last_modified)
    except requests.RequestException:
        return None
    return None


def last_modified_to_date(last_modified: str) -> str | None:
    """Convert an HTTP Last-Modified header to YYYY-MM-DD."""
    try:
        return parsedate_to_datetime(last_modified).date().isoformat()
    except (TypeError, ValueError, IndexError, OverflowError):
        return None


def file_format_from_name(local_file_name: str) -> str:
    ext = os.path.splitext(local_file_name)[1].lstrip('.').lower()
    if ext in ('owl', 'obo'):
        return ext
    return 'owl'


def download_ontology_file(url: str, local_path: str) -> str:
    """Download url and overwrite local_path."""
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    print(f'Downloading {url}')
    print(f'Saving to {local_path}\n')
    response = requests.get(url, stream=True, timeout=600)
    response.raise_for_status()
    with open(local_path, 'wb') as outfile:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                outfile.write(chunk)
    return local_path


def build_file_metadata(release_info: dict) -> dict:
    """Build IGVF-style file metadata for one ontology file."""
    version = release_info.get('version')
    if not version:
        print(f'No version found for {release_info["local_file_name"]}. Using today\'s date.')
        version = f'{date.today().isoformat()}'

    return {
        'content_type': 'ontology terms',
        'file_format': file_format_from_name(release_info['local_file_name']),
        'award': DEFAULT_AWARD,
        'lab': DEFAULT_LAB,
        'source_url': release_info['source_url'],
        'version': version,
        'controlled_access': False,
    }


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description='Download latest ontology files and write metadata JSON.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s
  %(prog)s --dry-run
  %(prog)s -o ontology_files_metadata.json""",
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Only resolve release info and write metadata JSON; do not download OWL files.',
    )
    parser.add_argument(
        '-o',
        '--output',
        default=None,
        help='Output metadata JSON path. Defaults to ontology_files_metadata-YYYY-MM-DD.json.',
    )
    parser.add_argument(
        '--ontology',
        action='append',
        dest='ontologies',
        default=None,
        help='Limit to one ontology key (repeatable), e.g. --ontology cl --ontology go.',
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    ontology_keys = args.ontologies or list(ONTOLOGY_ASSET_DICT.keys())

    unknown = [k for k in ontology_keys if k not in ONTOLOGY_ASSET_DICT]
    if unknown:
        raise SystemExit(f'Unknown ontology key(s): {", ".join(unknown)}')

    files_dir = get_ontology_files_dir()
    if not args.dry_run:
        os.makedirs(files_dir, exist_ok=True)

    metadata_by_ontology = {}
    for key in ontology_keys:
        print(f'=== {key} ===')
        release_info = get_release_info(key)
        local_path = os.path.join(files_dir, release_info['local_file_name'])
        if not args.dry_run:
            download_ontology_file(release_info['download_url'], local_path)
        metadata_by_ontology[key] = build_file_metadata(release_info)

    today = date.today().isoformat()
    output_path = args.output or f'ontology_files_metadata-{today}.json'
    payload = {
        'generated_on': today,
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'ontology_files_dir': files_dir,
        'dry_run': args.dry_run,
        'files': metadata_by_ontology,
    }

    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(payload, outfile, indent=2, ensure_ascii=False)
        outfile.write('\n')

    print(f'Metadata JSON written: {output_path}')
    print(f'Ontology files dir: {files_dir}')
    print(f'Files recorded: {len(metadata_by_ontology)}')
    if args.dry_run:
        print('Dry run: no OWL files were downloaded.')


if __name__ == '__main__':
    main()
