Updating ontologies
=========================

This document describes how to update the ontology versions used for searching and validation in the encoded application, ```ontology.json``` .

Ontologies used
----------------

* [Uber anatomy ontology (Uberon)]
* [Cell Ontology (CL)]
* [Experimental Factor Ontology (EFO)]
* [Ontology for Biomedical Investigations (OBI)]
* [Cell Line Ontology (CLO)]
* [Human Disease Ontology (DOID)]

Ontology files to use:
----------------

* Uberon and CL: composite-metazoan.owl from [Uberon download]
* EFO: EFO_inferred.owl from [EFO src tree]
* OBI: obi.owl [OBI download]
* CLO: clo.owl [CLO download]
* DOID: doid.owl [DOID download]

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

7. Future ontology files to use:

    * [The Human Phenotype Ontology (HPO)](http://purl.obolibrary.org/obo/hp.owl) for disease
    * [Mondo Disease Ontology](http://purl.obolibrary.org/obo/mondo/releases/2022-04-04/mondo.owl) for disease
    * [Ontology of Biological Attributes covering all kingdoms of life](http://purl.obolibrary.org/obo/oba.owl) for traits
