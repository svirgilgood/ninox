import subprocess
import os
from pathlib import Path
import sys


def format_turtle():

    staged_files = subprocess.run(
        ["git", "diff", "--cached", "--name-only"], capture_output=True).stdout.decode("utf-8").split('\n')

    if len(staged_files) < 1:
        return

    base_dir = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                              capture_output=True).stdout.decode("utf-8").strip()
    serializer_jar = Path(base_dir) / "tools" / "serializer"/"rdf-toolkit.jar"

    for staged_file in staged_files:
        if staged_file == "":
            continue
        _, ext = os.path.splitext(staged_file)
        if ext != ".ttl":
            continue
        print(f"formatting: {staged_file}")
        try:
            subprocess.run(["java", '-jar', serializer_jar, "-i", '"  "',
                            "-ibn", "--source", staged_file, "--target", staged_file], check=True, stderr=subprocess.DEVNULL)
            subprocess.run(["git", "add", "--update", staged_file], check=True)
        except subprocess.CalledProcessError:
            print(f"Error in formatting execution for {staged_file}")
            sys.exit(1)
