#!/usr/bin/env bash

set -x
set -e

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd "$(dirname "$0")" || exit

export FLASK_APP="vocabulary_srv:create_app(None, '${SCRIPTPATH}/testconfig.py')"
export FLASK_ENV=development

echo "Preparing instance folder..."
rm -r $SCRIPTPATH/../instance
rsync -v -r $SCRIPTPATH/../tests/testdata $SCRIPTPATH/../instance/

echo "FLASK_APP=$FLASK_APP"
echo "Initializing DB..."
flask init-db
echo "Launching application..."
flask run
