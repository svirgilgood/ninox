import os

from rdflib import Graph

from .bcolors import BColors


def validate(query_path: str, graph: Graph) -> list[tuple[bool, str]]:
    validation: list[tuple[bool, str]] = []

    for q_file in os.listdir(query_path):
        is_valid = True
        with open(os.path.join(query_path, q_file)) as fp:
            query = fp.read()
        query_result = graph.query(query)
        if len(query_result) > 0:
            print(f"{BColors.WARNING}RESULTS FROM: {q_file}{
                  BColors.ENDC}. NUMBER: {len(query_result)}")
            print(query_result.serialize(format="txt").decode("utf-8"))
            is_valid = False
        validation.append((is_valid, q_file))

    return validation
