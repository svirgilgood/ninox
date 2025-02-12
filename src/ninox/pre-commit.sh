#!/bin/sh
#
# An example hook script to verify what is about to be committed.
# Called by "git commit" with no arguments.  The hook should
# exit with non-zero status after issuing an appropriate message if
# it wants to stop the commit.
#
# To enable this hook, rename this file to "pre-commit".

if git rev-parse --verify HEAD >/dev/null 2>&1; then
  against=HEAD
else
  # Initial commit: diff against an empty tree object
  against=$(git hash-object -t tree /dev/null)
fi

exec 1>&2

base_dir="$(git rev-parse --show-toplevel)"

echo "Virtual env"
ninox fmt || (echo "Is ninox installed globally? or is the venv active?" && exit 1)
ninox validate -d "$base_dir/ontology" -s "$base_dir/shapes" -q "$base_dir/tests/queries" -t "$base_dir/tests" -a || exit 1

# If there are whitespace errors, print the offending file names and fail.
exec git diff-index --check --cached $against --
