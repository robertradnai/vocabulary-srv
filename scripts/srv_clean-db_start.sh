#!/usr/bin/env bash

set -e -x
SCRIPT_DIR="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
source config_local.sh

echo "Preparing instance folder..."
rm -r $SCRIPT_DIR/../instance
rsync -v -r $SCRIPT_DIR/../tests/testdata $SCRIPT_DIR/../instance/

echo "Initializing DB..."
flask init-db
echo "Launching application..."
flask run
