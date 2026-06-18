Updating ontologies
=========================

This document describes how to update the ontology versions used for searching and validation in the igvf application, ```ontology.json``` .

Ontology files to use
----------------

The `generate_ontology` script downloads the latest release of each ontology (when needed), caches OWL files locally in `ontology_files/`, and parses them to produce `ontology-YYYY-MM-DD.json`.

* [Uber anatomy ontology (Uberon): composite-metazoan.owl](https://github.com/obophenotype/uberon/releases)
* [Cell Ontology (CL): cl.owl](https://github.com/obophenotype/cell-ontology/releases) — loaded after composite-metazoan for fresher CL terms
* [Experimental Factor Ontology (EFO): efo.owl](https://github.com/EBISPOT/efo/releases)
* [Ontology for Biomedical Investigations (OBI): obi.owl](http://purl.obolibrary.org/obo/obi.owl)
* [Cell Line Ontology (CLO): clo.owl](http://purl.obolibrary.org/obo/clo.owl)
* [Human Disease Ontology (DOID): doid.owl](http://purl.obolibrary.org/obo/doid.owl)
* [The Human Phenotype Ontology (HPO): hp.owl](http://purl.obolibrary.org/obo/hp.owl)
* [Mondo Disease Ontology (MONDO): mondo.owl](http://purl.obolibrary.org/obo/mondo.owl)
* [Ontology of Biological Attributes covering all kingdoms of life (OBA): oba.owl](http://purl.obolibrary.org/obo/oba.owl)
* [Provisional Cell Ontology (PCL): pcl.owl](http://purl.obolibrary.org/obo/pcl.owl)
* [NCI Thesaurus (NCIT): ncit.owl](http://purl.obolibrary.org/obo/ncit.owl)
* [Gene Ontology (GO): go.owl](https://purl.obolibrary.org/obo/go.owl)

How to update the ontology versions
----------------

1. Install ontology script:

    `pip install .`

2. Run generate_ontology:

    By default, the script uses cached OWL files in `ontology_files/` when they exist. Missing files are downloaded automatically.

    `generate_ontology`

    To re-download all ontology files from their latest releases:

    `generate_ontology --force-download`

3. The ontology file generated has a file name format like this:       ontology-YYYY-MM-DD.json

4. Load new ontology file into the encoded-build/ontology directory on S3

    `aws s3 cp ontology-YYYY-MM-DD.json s3://...`

    Locate the file on S3 and change the permissions so that "Read" permission is granted to "Everybody (public access)."

5. Update the ontology version in the [Makefile]:

    `curl -o ontology.json https://.../ontology/ontology-YYYY-MM-DD.json`

6. Update the following information

    * Site release version: N/A

    * ontology.json file: N/A

    * UBERON release date: 2025-12-04

    * CL release date: 2026-06-15

    * OBI release date:  2025-12-18

    * EFO release date:  2026-03-16

    * CLO release date: 2023-03-28

    * DOID release date:  2026-02-28

    * HP release date:  2026-02-16

    * MONDO release date:  2026-03-03

    * OBA release date:  2025-10-29

    * NCIT release date:  2026-03-19

    * PCL release date:  2025-07-07

    * GO release date:  2026-01-23

7. Resources

    * [Uber anatomy ontology (Uberon)](http://uberon.org/)

    * [Cell Ontology (CL)](http://cellontology.org/)

    * [Experimental Factor Ontology (EFO)](http://www.ebi.ac.uk/efo)

    * [Ontology for Biomedical Investigations (OBI)](http://obi-ontology.org/)

    * [Cell Line Ontology (CLO)](http://www.clo-ontology.org)

    * [Human Disease Ontology (DOID)](http://www.disease-ontology.org)

    * [Uberon download](https://github.com/obophenotype/uberon/releases)

    * [Cell Ontology (CL) download](https://github.com/obophenotype/cell-ontology/releases)

    * [EFO src tree](https://github.com/EBISPOT/efo/)

    * [OBI download](http://www.ontobee.org/ontology/OBI)

    * [CLO download](http://www.ontobee.org/ontology/CLO)

    * [DOID download](http://www.ontobee.org/ontology/DOID)

    * [UBERON release date](https://github.com/obophenotype/uberon/releases)

    * [CL release date](https://github.com/obophenotype/cell-ontology/releases)

    * [OBI release date](https://github.com/obi-ontology/obi/releases)

    * [EFO release date](https://github.com/EBISPOT/efo/blob/master/ExFactor%20Ontology%20release%20notes.txt)

    * [CLO release date](http://www.ontobee.org/ontology/CLO)

    * [DOID release date](http://www.ontobee.org/ontology/DOID)

    * [Provisional Cell Ontology (PCL)](https://obofoundry.org/ontology/pcl.html)

    * [NCI Thesaurus (NCIT)](https://github.com/ncit-obo-org/ncit-obo-edition)

    * [Gene Ontology (GO)](https://geneontology.org/)
