#!/usr/bin/env python3
"""
[x] organize Directories
[x] Download rdf-toolkit
[x] create pre-commit hooks
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
import stat
import subprocess
import sys
from urllib import request
import pathlib
from pathlib import PosixPath

src_dir = pathlib.Path(__file__).parent

model_shape = src_dir/"model_shape.ttl"

term_query = src_dir/"undefined_terms.rq"

pre_commit = src_dir/"pre-commit.sh"
# import shutil


RDF_TOOLKIT_URL = "https://github.com/edmcouncil/rdf-toolkit/releases/download/v2.0/rdf-toolkit.jar"


def create_directory(path: str):
    if os.path.exists(path):
        print(f"Directory `{path}` Exists")
        return
    print(f"Creating `{path}`")
    os.makedirs(path)


def is_git() -> bool:

    is_git = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"], capture_output=True, check=False).stdout.decode("utf-8").strip()
    if is_git == "true":
        return True
    return False


def get_git_root() -> str:

    return subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, check=False).stdout.decode("utf-8").strip()


def change_to_git_root():
    git_dir = get_git_root()
    if git_dir == ".git":
        return
    os.chdir(git_dir.rstrip(".git"))


def write_template(target_path: str, template: PosixPath):
    with open(target_path, "a") as target_p:
        with open(template, "r") as template_p:
            target_p.write(template_p.read())


def initizalize_git():
    # initialize git repository
    if is_git():
        pass
    else:
        change_to_git_root()
        subprocess.run(["git", "init"], check=False)
    # create necessary directories
    print("Ensuring correct scaffolding is in place")
    for path in ("ontology", "shapes", "tools", "tools/serializer", "tests", "tests/queries"):
        create_directory(path)

    # check if java exists
    print("Installing RDF-ToolKit serializer")
    try:
        subprocess.check_output(
            ["java", "-version"], stderr=subprocess.STDOUT)
    except FileNotFoundError:
        print("Please install a java version that is compatible with rdf-toolkit")
        sys.exit(1)

    request.urlretrieve(RDF_TOOLKIT_URL, "tools/serializer/rdf-toolkit.jar")

    print("Adding tools/serializer to .gitignore")
    with open(".gitignore", "a") as gip:
        gip.write("""
# We are excluding the serializer binary from source countrol
tools/serializer/
"""
                  )

        # Move data files
        # First copy the undefined term query into the queries
        print("Copying over the Undefined Terms Query")
        write_template("tests/queries/undefined_terms.rq", term_query)

        # Next copy the shape into the shapes directory
        print("Copying the model shape")
        write_template("shapes/model_shape.ttl", model_shape)

        # Next copy the pre-commit hook into the .git directory
        print("Copying the pre-commit hook and making it executable")
        write_template(".git/hooks/pre-commit", pre_commit)
        os.chmod("./.git/hooks/pre-commit", stat.S_IRWXU | stat.S_IRUSR | stat.S_IWUSR |
                 stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IXOTH | stat.S_IROTH)
