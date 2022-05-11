Updating ontologies
=========================

This document describes how to update the ontology versions used for searching and validation in the encoded application, ```ontology.json``` .

Ontology files to use
----------------

* [Uber anatomy ontology (Uberon) and Cell Ontology (CL): composite-metazoan.owl](https://github.com/obophenotype/uberon/releases/download/v2022-04-18/composite-metazoan.owl)
* [Experimental Factor Ontology (EFO): EFO_inferred.owl](https://github.com/EBISPOT/efo/releases/download/v3.41.0/efo.owl)
* [Ontology for Biomedical Investigations (OBI): obi.owl](http://purl.obolibrary.org/obo/obi.owl)
* [Cell Line Ontology (CLO): clo.owl](http://purl.obolibrary.org/obo/clo.owl)
* [Human Disease Ontology (DOID): doid.owl](http://purl.obolibrary.org/obo/doid.owl)
* [The Human Phenotype Ontology (HPO): hp.owl](http://purl.obolibrary.org/obo/hp.owl)
* [Mondo Disease Ontology (MONDO): mondo.owl](http://purl.obolibrary.org/obo/mondo/releases/2022-04-04/mondo.owl)
* [Ontology of Biological Attributes covering all kingdoms of life (OBA): oba.owl](http://purl.obolibrary.org/obo/oba.owl)

How to update the ontology versions
----------------

1. Install ontology script:

    `pip install .`

2. Run generate_ontology:

    `generate_ontology`

3. The ontology file generated has a file name format like this: ontology.json       ontology-YYYY-MM-DD.json

4. Load new ontology file into the encoded-build/ontology directory on S3

    `aws s3 cp ontology-YYYY-MM-DD.json s3://...`

    Locate the file on S3 and change the permissions so that "Read" permission is granted to "Everybody (public access)."

5. Update the ontology version in the [Makefile]:

    `curl -o ontology.json https://.../ontology/ontology-YYYY-MM-DD.json`

6. Update the following information

    Site release version: N/A
    ontology.json file: N/A
    [UBERON release date]: 2021-10-01
    [OBI release date]: 2022-01-03
    [EFO release date]: 2022-01-17
    [CLO release date]: 2019-02-10
    [DOID release date]: 2021-12-15

    [Uber anatomy ontology (Uberon)]: http://uberon.org/
    [Cell Ontology (CL)]: http://cellontology.org/
    [Experimental Factor Ontology (EFO)]: http://www.ebi.ac.uk/efo
    [Ontology for Biomedical Investigations (OBI)]: http://obi-ontology.org/
    [Cell Line Ontology (CLO)]: http://www.clo-ontology.org
    [Human Disease Ontology (DOID)]: http://www.disease-ontology.org
    [Uberon download]: https://github.com/obophenotype/uberon/releases
    [EFO src tree]: https://github.com/EBISPOT/efo/
    [OBI download]: http://www.ontobee.org/ontology/OBI
    [CLO download]: http://www.ontobee.org/ontology/CLO
    [DOID download]: http://www.ontobee.org/ontology/DOID
    [Makefile]: ../../../Makefile
    [UBERON release date]: https://github.com/obophenotype/uberon/releases
    [OBI release date]: https://github.com/obi-ontology/obi/releases
    [EFO release date]: https://github.com/EBISPOT/efo/blob/master/ExFactor%20Ontology%20release%20notes.txt
    [CLO release date]: http://www.ontobee.org/ontology/CLO
    [DOID release date]: http://www.ontobee.org/ontology/DOID
