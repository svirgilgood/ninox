#!/usr/bin/env python3
"""
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
from pathlib import Path
import hashlib
from .bcolors import BColors

src_dir = pathlib.Path(__file__).parent

model_shape = src_dir/"model_shape.ttl"

term_query = src_dir/"undefined_terms.rq"

pre_commit = src_dir/"pre-commit.sh"

RDF_TOOLKIT_URL = "https://github.com/edmcouncil/rdf-toolkit/releases/download/v2.0/rdf-toolkit.jar"
RDF_TOOLKIT_HASH = "d9998747e44c018245c8d769abb62e1b3d6b84405d2c456396e18f2e5088b8f1"


def create_directory(path: Path):
    """Create a directory based on the Path, if the Path already exists log a
    warning"""
    try:
        os.makedirs(path)
    except FileExistsError:
        print(f"Directory `{path}` Exists")
        return


def is_git() -> bool:
    """Check to see if the repository is a git repository"""

    is_git = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"], capture_output=True, check=False).stdout.decode().strip()
    return is_git == "true"


def get_git_root() -> str:
    """Finds the path to the root directory for the git repo."""

    return subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, check=False).stdout.decode().strip()


def change_to_git_root():
    """Move to the root of the git repository"""
    git_dir = get_git_root()
    if git_dir == ".git":
        return
    os.chdir(git_dir.rstrip(".git"))


def install_rdf_toolkit():
    """Install the rdf-toolkit from the github repository. Validate the
    downloaded jar based on the SHA256 value."""

    rdf_target = pathlib.Path("tools")/"serializer"/"rdf-toolkit.jar"

    response = request.urlopen(RDF_TOOLKIT_URL)
    if response.status != 200:
        print(f"{BColors.FAIL}Error in Downloading rdf-toolkit{BColors.ENDC}")
        sys.exit(1)
    with open(rdf_target, "wb") as fp:
        fp.write(response.read())

    print("Verifying Hash")
    with open(rdf_target, "rb") as fp:
        sha256 = hashlib.sha256(fp.read())

    if sha256.hexdigest() == RDF_TOOLKIT_HASH:

        print(f"{BColors.OKGREEN}Hashes Match{BColors.ENDC}")
        return

    os.remove(rdf_target)
    print(f"{BColors.WARNING}Hashes did not match{BColors.ENDC}")
    print(
        f"rdf-toolkit hash did not match. In order to check installation please download a version of rdf-toolkit and place it {rdf_target}")


def write_template(target_path: Path, template: Path):
    """Appends the template to any existing file, or just append to the existing files."""
    with open(target_path, "a") as target_p:
        with open(template, "r") as template_p:
            target_p.write(template_p.read())


def initizalize_git(*args):
    """Initialize the git repository.
    1. Makes sure the repository is a git directory.
    2. Creates the scaffolding that matches what the ontology directory structure
    3. Install rdf-toolkit and verify that it matches the hash
    4. Update .gitignore to ignore the rdf-toolkit
    5. Copy over templates (undefined_terms.rq, pre-commit, and model_shape.ttl)
    """
    # initialize git repository
    if not is_git():
        try:
            subprocess.run(["git", "init", "-b", "main"], check=True)
        except FileNotFoundError as error:
            print(f"Is Git installed?\n{error}")
            sys.exit(1)

    change_to_git_root()

    # create necessary directories
    print("Ensuring correct scaffolding is in place")
    for path in (
        Path("ontology"),
        Path("shapes"),
        Path("tools"),
        Path("tools")/"serializer",
        Path("tests"),
        Path("tests")/"queries"
    ):
        create_directory(path)

    # check if java exists
    print("Installing RDF-ToolKit serializer")
    try:
        subprocess.check_output(
            ["java", "-version"], stderr=subprocess.STDOUT)
    except FileNotFoundError:
        print("Please install a java version that is compatible with rdf-toolkit")
        sys.exit(1)

    install_rdf_toolkit()

    print("Adding tools/serializer to .gitignore")
    with open(".gitignore", "a") as gip:
        gip.write("""
# We are excluding the serializer binary from source countrol
tools/serializer/
# Remove the following line if the project needs a tools directory in source control
tools/
"""
                  )

    # Move data files
    # First copy the undefined term query into the queries
    print("Copying over the Undefined Terms Query")
    write_template(Path("tests")/"queries"/"undefined_terms.rq", term_query)

    # Next copy the shape into the shapes directory
    print("Copying the model shape")
    write_template(Path("shapes")/"model_shape.ttl", model_shape)

    # Next copy the pre-commit hook into the .git directory
    print("Copying the pre-commit hook and making it executable")
    pre_commit_path = Path(".git")/"hooks"/"pre-commit"
    write_template(pre_commit_path, pre_commit)
    os.chmod(pre_commit_path, stat.S_IRWXU | stat.S_IRUSR | stat.S_IWUSR |
             stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IXOTH | stat.S_IROTH)
