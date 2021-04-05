#!/bin/bash

# https://python-bloggers.com/2020/10/docker-flask-dockerizing-a-python-api/
set -x
set -e

cd "$(dirname "$0")"
cd ..

sudo docker build -t vocabulary_srv -f Dockerfile --no-cache --build-arg COMMIT_HASH="$(git rev-parse HEAD)" .
# no-cache is needed because the COPY command didn't recognize that
# the source file was updated

