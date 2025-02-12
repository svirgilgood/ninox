# ninox

[![PyPI - Version](https://img.shields.io/pypi/v/ontobean.svg)](https://pypi.org/project/ontobean)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ontobean.svg)](https://pypi.org/project/ontobean)

-----

## Table of Contents

- [Purpose](#Purpose)
- [Installation](#installation)
- [SPARQL Query Validation](#SPARQL)
- [SHACL](#Shacl)
- [Inference Testing](#Inference)
- [License](#license)

## Purpose 

The purpose of this script is to provide a suite of tools for using git to
develop and validate ontologies and RDF data models with git. 

First, it provides a deterministic formatter by downloading and wrapping
`rdf-toolkit` to provide a consistent code style and order to turtle files. 

Second, it provides a query harness to allow for automated tests to ensure the
quality of the ontology. A provided query `undefined_terms.rq`, searches for any
term that is referenced or used but doesn't have a class definition.

Third, it provides an OWL inference engine that can be used to create tests data
to prove the consistency of the ontology.

Fourth, these functions can be called individually, but they are also
conveniently wrapped in a pre-commit hook.

## Installation

Hopefully installation soon will be as simple as: 

```console 
pip install ninox 
```

However, currently to add this to an existing git repository (or to create a new
repository to work from). First, clone this repository. Then create a virtual
python3 environment inside the ontology repository and activate. Next use `pip`
to add the cloned repository. `pip install /path/to/cloned/repo/for/ninox`

After `ninox` is installed in the ontology repo, initialize the repo to be used
with ninox. `ninox init`. This will create the following structure in the
repository:

```console
├── ontology
├── shapes
│   └── model_shape.ttl
├── tests
│   └── queries
│       └── undefined_terms.rq
└── tools
    └── serializer
        └── rdf-toolkit.jar
```

The templates `undefined_terms.rq` and `model_shape.ttl` can be adjusted to fit
the needs of the ontology.

## SPARQL Query Validation

Additional queries for validating data can be added to the `tests/queries`
directory. The should be simple `SELECT` queries that when passing return no
values. The queries are run over all of the turtle files in `shapes` and
`ontology`.


## SHACL Validation 

The SHACL shapes will be run on all of the data in the `ontology` directory. The
shape that is installed with `ninox init` is an opinionated, closed shape. After
it is installed in the repository, it should be adjusted to fit the needs of the
ontology.

## Inference Testing

Test instances can be added inside the test folder. These should take the form
of a turtle file that has examples that you wish to prove the ontology works.
These examples will fit the ideal data your ontology matches with certain
additions for testing. 

All test instances should belong to the class `ninox:InferenceTest`, and have
the properties `ninox:expectedClass` for all of the classes that will be
expected for the instance to be inferred into. 

For example, the ontology: 

```turtle 
@prefix ex: <https://www.example.com#> .
@prefix ninox <https://svirgilgood.github.io/ninox/onto/> .

ex:StopSign 
  a owl:Class ;
skos:prefLabel "Stop Sign" ;
skos:definition "A sign that signals you to stop" ;
owl:equivalentClass [
    a owl:Class ;
    owl:intersectionOf (
      ex:Sign 
      [ 
        a owl:Restriction ;
        owl:onProperty ex:sides ;
        owl:hasValue ex:EightSides ;
      ]
      [ 
        a owl:Restriction ;
        owl:onProperty ex:color ;
        owl:hasValue ex:Red ;
      ]
    )
  ] ;
  .

  
```
Could be tested with the following instance.

```turtle 
ex:_TestSignA 
  a ex:Sign , ninox:InferenceTest ;
  ex:sides ex:EightSides ;
  ex:color ex:Red ;
  ninox:expectedClass rdfs:Resource , owl:Thing, ex:Sign, ex:StopSign ;
  .
  
```



## License

`ninox` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
