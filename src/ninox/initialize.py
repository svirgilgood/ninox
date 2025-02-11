#!/usr/bin/env python3
"""
[x] organize Directories
[x] Download rdf-toolkit
[ ] create pre-commit hooks
[x] install sparql query
[x] install owl constraint shape

Directory structure should be something like this
├── .git
│   ├── HEAD
│   ├── config
│   ├── description
│   ├── hooks
│   │   └── pre-commit # These will be the pre commit hook installed 
│   ├── info
│   │   └── exclude
│   ├── objects
│   │   ├── info
│   │   └── pack
│   └── refs
│       ├── heads
│       └── tags
├── ontology
├── shapes
│   └── model_shape.ttl # the default shacl for owl ontologies
├── tests
│   └── queries
│       └── undefined_terms.rq # Default query
└── tools
    └── serializer
        └── rdf-toolkit.jar # installed jar


"""

import os
import subprocess
import sys
from urllib import request

# import shutil


RDF_TOOLKIT_URL = "https://github.com/edmcouncil/rdf-toolkit/releases/download/v2.0/rdf-toolkit.jar"


def create_directory(path: str):
    if os.path.exists(path):
        return
    os.makedirs(path)


class GitHandler:
    def is_git() -> bool:

        is_git = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"], capture_output=True, check=False).stdout.decode("utf-8").strip()
        if is_git == "true":
            return True
        return False

    def _get_git_root() -> str:

        return subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, check=False).stdout.decode("utf-8").strip()

    def change_to_git_root(self):
        git_dir = self._get_git_root()
        if git_dir == ".git":
            return
        os.chdir(git_dir.rstrip(".git"))

    def initizalize_git(self):
        # initialize git repository
        if self.is_git():
            pass
        else:
            self.change_to_git_root()
            subprocess.run(["git", "init"], check=False)
        # create necessary repositories
        for path in ("ontoloty", "shapes", "tools", "tools/serializer", "tests", "tests/queries"):
            create_directory(path)

        # check if java exists
        try:
            subprocess.check_output(
                ["java", "-version"], sterr=subprocess.STDOUT)
        except FileNotFoundError:
            print("Please install a java version")
            sys.exit(1)

        request.urlretrive(RDF_TOOLKIT_URL, "tools/serializer/rdf-toolkit.jar")

        # Move data files
        # sys.argv[0] is the path to the script that is running
        print(sys.argv[0])
        # shutil.copy2("./data/model_shape.ttl", "shapes/")

        # shutil.copy2("./data/undefined_terms.rq", "tests/quereis/")
