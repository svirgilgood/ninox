"""
Create a script that allows for shacl validation
"""


import pyshacl
from rdflib import Graph
from rdflib.namespace import SH

from .bcolors import BColors


def validate(data_graph: Graph, shape_graph: Graph) -> tuple[bool, Graph]:
    r = pyshacl.validate(data_graph, shacl_graph=shape_graph)
    conforms, results_graph, results_text = r
    if conforms:
        return (True, Graph())
    # Should we add a check for
    violations = results_graph.triples((None, SH.resultSeverity, SH.Violation))
    warning_graph = Graph()
    for warning in results_graph.subjects(SH.resultSeverity, SH.Warning):
        for triple in results_graph.triples((warning, None, None)):
            warning_graph.add(triple)
            results_graph.remove(triple)
        results_graph.remove((None, SH.result, warning))
    for info in results_graph.subjects(SH.resultSeverity, SH.Info):
        for triple in results_graph.triples((info, None, None)):
            warning_graph.add(triple)
            results_graph.remove(triple)
        results_graph.remove((None, SH.result, info))
    print(f"{BColors.WARNING}Warnings and Info from SHACL Validation{
        BColors.ENDC}")
    print(warning_graph.serialize(format="longturtle"))
    if len(list(violations)) > 0:
        return (False, results_graph)

    return (True, results_graph)
