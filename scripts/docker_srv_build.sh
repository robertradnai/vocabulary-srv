#!/bin/bash

set -x
set -e

cd "$(dirname "$0")"
cd ..

sudo docker build -t vocabulary_srv -f Dockerfile --build-arg COMMIT_HASH="$(git rev-parse HEAD)" .
