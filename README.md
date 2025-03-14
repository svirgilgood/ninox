# ninox

[![PyPI - Version](https://img.shields.io/pypi/v/ninox.svg)](https://pypi.org/project/ninox)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ninox.svg)](https://pypi.org/project/ninox)

-----

## Table of Contents

- [Purpose](#Purpose)
- [Installation](#installation)
- [SPARQL Query Validation](#sparql-query-validation)
- [SHACL Validation](#shacl-validation)
- [Inference Testing](#inference-testing)
- [License](#license)

## Purpose 

The purpose of this script is to provide a suite of tools for using git to
develop and validate ontologies and RDF data models with git hooks.

First, it provides a deterministic formatter by downloading and wrapping
[`rdf-toolkit`](https://github.com/edmcouncil/rdf-toolkit) to provide a consistent code style and order to turtle files.

Second, it provides SHACL shapes that can validate an ontology in owl syntax.
This provides an opinionated style enforcement for ontologies. For example, all
classes and properties must have `skos:prefLabel` and classes must be title
cased, and properties must be lower cased.

Third, it provides a query harness to allow for automated tests to ensure the
quality of the ontology. A provided query `undefined_terms.rq`, searches for any
term that is referenced or used but doesn't have a class definition.

Fourth, it provides an OWL inference engine that can be used to create tests
data to prove the consistency of the ontology.

Fifth, these functions can be called individually, but they are also
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
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

@prefix ex: <https://www.example.com#> .
@prefix ninox: <https://svirgilgood.github.io/ninox/onto#> .

ex:StopSign
  a owl:Class ;
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
        owl:onProperty ex:hasColor ;
        owl:hasValue ex:Red ;
      ]
    ) ;
  ] ;
  skos:definition "A sign that signals you to stop" ;
  skos:prefLabel "Stop Sign" ;
  .
```

Could be tested with the following instance:

```turtle 
ex:_TestSignA
  a
    ninox:InferenceTest ,
    ex:Sign
    ;
  ninox:expectedClass
    rdfs:Resource ,
    owl:Thing ,
    ninox:InferenceTest ,
    ex:Sign ,
    ex:StopSign
    ;
  ex:hasColor ex:Red ;
  ex:sides ex:EightSides ;
  .
```



## Usage

`ninox` has three subcommands: `validate`, `fmt`, and `init`.

`ninox init` - will only be used for initializing the repository, creating the
directory structure and creating the templates.

`ninox fmt` - is a wrapper for `rdf-toolkit` with sane defaults, if called with
a turtle file, it will only run the formatter on that file, if run without
arguments it will run the formatter on all files staged for commit.

`ninox validate` - has many options for testing and validating. See `ninox validate --help` for more information.


## License

`ninox` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
