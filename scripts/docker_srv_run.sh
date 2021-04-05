#!/bin/bash

set -e -x

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"

sudo docker run --rm --network="host" --name vocabulary_srv_container \
  -v "$PROJECT_DIR/scripts/dockerconfig.py:/config/testconfig.py" \
  -v "$PROJECT_DIR/tests/testdata/shared_collections:/config/shared_collections" \
  -v "$PROJECT_DIR/tests/testdata/shared_collections_metadata.yml:/config/shared_collections_metadata.yml" \
  -e 'PORT=5000' \
  vocabulary_srv


# Interactive mode: add
# -it vocabulary_srv /bin/bash