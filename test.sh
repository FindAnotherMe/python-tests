#!/bin/sh -e
# Run all Python tests in the test directory.

version="${1}"

for test in tests/*.py; do
  echo "Running ${test} on python${version} ..."

  for encoding in en_US.UTF-8 C; do
    echo "Testing encoding ${encoding} ..."
    LC_ALL="${encoding}" LANG="${encoding}" "python${version}" "${test}" -v
  done
done
