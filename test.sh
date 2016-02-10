#!/bin/sh -e
# Run all Python tests in the test directory.

for test in tests/*.py; do
  echo "Running ${test} ... "
  "${test}" -v
done
