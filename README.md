Updating ontologies
=========================

This repository builds the combined ontology term file used for searching and validation in the IGVF application (`ontology.json`).

Shared source config lives in `ontology/ontology_assets.py` (`ONTOLOGY_ASSET_DICT`): canonical download URI, OLS id, IGVF curated-set accession (`file_set`), and flags such as `catalog_only` / `in_whitelist`.

There are two main scripts:

1. **`download_ontology_metadata`** — download latest ontology files from their canonical URLs and write portal upload metadata.
2. **`generate_ontology`** — download released ontology files from IGVF curated sets and build `ontology-YYYY-MM-DD.json`.

Ontology inventory
----------------

Used in `generate_ontology` (combined JSON)
----------------

| Key | File | Source URI | Curated set |
| ----- | ------ | ------------ | ------------- |
| uberon | uberon.owl | [http://purl.obolibrary.org/obo/uberon.owl](http://purl.obolibrary.org/obo/uberon.owl) | IGVFDS2035XPMB |
| cl | cl.owl | [http://purl.obolibrary.org/obo/cl.owl](http://purl.obolibrary.org/obo/cl.owl) | IGVFDS2588RYXK |
| efo | efo.owl | [http://www.ebi.ac.uk/efo/efo.owl](http://www.ebi.ac.uk/efo/efo.owl) | IGVFDS6003FOMG |
| mondo | mondo.owl | [http://purl.obolibrary.org/obo/mondo.owl](http://purl.obolibrary.org/obo/mondo.owl) | IGVFDS7295JLJQ |
| oba | oba.owl | [http://purl.obolibrary.org/obo/oba.owl](http://purl.obolibrary.org/obo/oba.owl) | IGVFDS0967KVGP |
| obi | obi.owl | [http://purl.obolibrary.org/obo/obi.owl](http://purl.obolibrary.org/obo/obi.owl) | IGVFDS2602QLHH |
| clo | clo.owl | [http://purl.obolibrary.org/obo/clo.owl](http://purl.obolibrary.org/obo/clo.owl) | IGVFDS7562BUEW |
| doid | doid.owl | [http://purl.obolibrary.org/obo/doid.owl](http://purl.obolibrary.org/obo/doid.owl) | IGVFDS0076IZRZ |
| hp | hp.owl | [http://purl.obolibrary.org/obo/hp.owl](http://purl.obolibrary.org/obo/hp.owl) | IGVFDS5350TOZO |
| ncit | ncit.owl | [http://purl.obolibrary.org/obo/ncit.owl](http://purl.obolibrary.org/obo/ncit.owl) | IGVFDS6069UIHS |
| pcl | pcl.owl | [http://purl.obolibrary.org/obo/pcl.owl](http://purl.obolibrary.org/obo/pcl.owl) | IGVFDS4687SYMS |
| go | go.owl | [https://purl.obolibrary.org/obo/go.owl](https://purl.obolibrary.org/obo/go.owl) | IGVFDS9239KXAX |
| bao | bao_complete.owl | [https://www.bioassayontology.org/bao/bao_complete.owl](https://www.bioassayontology.org/bao/bao_complete.owl) | IGVFDS4680UUQJ |

Catalog-only (download/metadata; not used in generation)
----------------

| Key | File | Source URI | Curated set |
| ----- | ------ | ------------ | ------------- |
| chebi | chebi.owl | [http://purl.obolibrary.org/obo/chebi.owl](http://purl.obolibrary.org/obo/chebi.owl) | IGVFDS0762GKJU |
| vario | vario.owl | [http://purl.obolibrary.org/obo/vario.owl](http://purl.obolibrary.org/obo/vario.owl) | IGVFDS3622SSGR |
| orphanet | ordo_orphanet.owl | [https://www.orphadata.com/data/ontologies/ordo/last_version/ordo_orphanet.owl](https://www.orphadata.com/data/ontologies/ordo/last_version/ordo_orphanet.owl) | IGVFDS9088SLTK |
| cellosaurus | cellosaurus.obo | [https://ftp.expasy.org/databases/cellosaurus/cellosaurus.obo](https://ftp.expasy.org/databases/cellosaurus/cellosaurus.obo) | IGVFDS3922HDSH |

Install
----------------

```bash
pip install .
```

This installs the `generate_ontology` console script. The metadata downloader is run as a module (see below).

Download ontology files and write metadata
----------------

Use this when refreshing source files for IGVF portal upload (curated sets).

```bash
python -m ontology.download_ontology_metadata
python -m ontology.download_ontology_metadata --dry-run
python -m ontology.download_ontology_metadata --ontology bao --ontology go
python -m ontology.download_ontology_metadata -o ontology_files_metadata.json
```

Behavior:

* Downloads each asset’s `uri` (or `download_uri` when set: BAO GitHub mirror, ChEBI `.owl.gz`). Uncompressed downloads are gzipped locally for portal upload.
* Writes `ontology_files_metadata-YYYY-MM-DD.json` with per-file portal fields (`content_type`, `file_format`, `award`, `lab`, `file_set`, `source_url`, `version`, `controlled_access`, `submitted_file_name`).
* Version resolution order:
  1. Cellosaurus: [https://api.cellosaurus.org/release-info](https://api.cellosaurus.org/release-info)
  2. EBI OLS4: [https://www.ebi.ac.uk/ols4/api/ontologies/{ols_id}](https://www.ebi.ac.uk/ols4/api/ontologies/{ols_id}) (`version`, else parse `config.versionIri`)
  3. Fallback: HTTP `Last-Modified` of the download URL
* Versions in metadata are prefixed with `v` (e.g. `v2.8.19`, `v2026-06-23`).

Generate combined ontology JSON
----------------

`generate_ontology` loads **released** files from IGVF curated sets (not directly from PURLs):

1. `GET https://api.data.igvf.org/curated-sets/{file_set}/`
2. Pick the single `files[]` entry with `status == "released"`
3. Download `href` (gzipped) into `ontology_files_from_igvf_portal/`, gunzip to the local OWL/OBO name

```bash
generate_ontology
generate_ontology --force-download
```

* Default: use cached files under `ontology_files_from_igvf_portal/` when present.
* `--force-download`: re-fetch from the portal even if cached.
* Output: `ontology-YYYY-MM-DD.json` in the current working directory.

Both `ontology_files/` and `ontology_files_from_igvf_portal/` are gitignored.

Publish the ontology JSON
----------------

1. Load the new file into the encoded-build/ontology directory on S3:

    `aws s3 cp ontology-YYYY-MM-DD.json s3://...`

    Locate the file on S3 and grant “Read” to “Everybody (public access).”

2. Update the ontology version in the application Makefile:

    `curl -o ontology.json https://.../ontology/ontology-YYYY-MM-DD.json`

Current versions (from metadata dry-run 2026-08-12)
----------------

* UBERON: v2026-06-19
* CL: v2026-06-08
* EFO: v3.92.0
* MONDO: v2026-08-04
* OBA: v2026-07-14
* OBI: v2026-07-27
* CLO: v2026-06-19
* DOID: v2026-07-31
* HP: v2026-06-23
* NCIT: v26.02d
* PCL: v2025-07-07
* GO: v2026-07-26
* BAO: v2.8.19
* CHEBI: v253
* Vario: v2025-02-28
* Orphanet (ORDO): v4.9
* Cellosaurus: v56.0

Resources
----------------

* [Uberon](http://uberon.org/) — [PURL](http://purl.obolibrary.org/obo/uberon.owl)
* [Cell Ontology (CL)](http://cellontology.org/) — [PURL](http://purl.obolibrary.org/obo/cl.owl)
* [EFO](http://www.ebi.ac.uk/efo) — [OWL](http://www.ebi.ac.uk/efo/efo.owl)
* [Mondo](https://mondo.monarchinitiative.org/) — [PURL](http://purl.obolibrary.org/obo/mondo.owl)
* [OBA](https://obofoundry.org/ontology/oba.html) — [PURL](http://purl.obolibrary.org/obo/oba.owl)
* [OBI](http://obi-ontology.org/) — [PURL](http://purl.obolibrary.org/obo/obi.owl)
* [CLO](http://www.clo-ontology.org) — [PURL](http://purl.obolibrary.org/obo/clo.owl)
* [DOID](http://www.disease-ontology.org) — [PURL](http://purl.obolibrary.org/obo/doid.owl)
* [HPO](https://hpo.jax.org/) — [PURL](http://purl.obolibrary.org/obo/hp.owl)
* [NCIT](https://github.com/ncit-obo-org/ncit-obo-edition) — [PURL](http://purl.obolibrary.org/obo/ncit.owl)
* [PCL](https://obofoundry.org/ontology/pcl.html) — [PURL](http://purl.obolibrary.org/obo/pcl.owl)
* [GO](https://geneontology.org/) — [PURL](https://purl.obolibrary.org/obo/go.owl)
* [BAO](http://bioassayontology.org) — [bao_complete.owl](https://www.bioassayontology.org/bao/bao_complete.owl) (download mirror: [GitHub](https://raw.githubusercontent.com/BioAssayOntology/BAO/master/bao_complete.owl)) — [OLS API](https://www.ebi.ac.uk/ols4/api/ontologies/bao)
* [ChEBI](https://www.ebi.ac.uk/chebi/) — [PURL](http://purl.obolibrary.org/obo/chebi.owl) (download: [chebi.owl.gz](http://purl.obolibrary.org/obo/chebi.owl.gz))
* [VariO](https://variationontology.org/) — [PURL](http://purl.obolibrary.org/obo/vario.owl)
* [Orphanet / ORDO](https://www.orphadata.com/) — [ordo_orphanet.owl](https://www.orphadata.com/data/ontologies/ordo/last_version/ordo_orphanet.owl)
* [Cellosaurus](https://www.cellosaurus.org/) — [OBO](https://ftp.expasy.org/databases/cellosaurus/cellosaurus.obo) — [release-info API](https://api.cellosaurus.org/release-info)
* [EBI OLS4](https://www.ebi.ac.uk/ols4/) — version metadata for most ontologies
* [IGVF data portal API](https://api.data.igvf.org/) — curated-set files used by `generate_ontology`
