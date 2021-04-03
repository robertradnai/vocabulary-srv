#!/bin/bash

# https://python-bloggers.com/2020/10/docker-flask-dockerizing-a-python-api/
set -x
set -e

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )"

cd "$(dirname "$0")" || exit
cd ..

sudo docker build -t vocabulary-srv -f Dockerfile --build-arg COMMIT_HASH="$(git rev-parse HEAD)" .

sudo docker run --rm -p 5000:5000 --network="host" --name vocabulary_srv \
  -v "$PROJECT_DIR"/scripts/dockerconfig.py:/config/testconfig.py \
  -v "$PROJECT_DIR"/tests/testdata/shared_collections:/config/shared_collections \
  -v "$PROJECT_DIR"/tests/testdata/shared_collections_metadata.yml:/config/shared_collections_metadata.yml \
  vocabulary-srv

# Interactive mode: add -it and at the end: /bin/bash
