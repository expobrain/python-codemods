#!/bin/bash -eux

command=$1
source_paths=${@:2}

python -m libcst.tool codemod "$command" $source_paths
