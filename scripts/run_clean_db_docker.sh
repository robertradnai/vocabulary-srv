#!/usr/bin/env bash

set -x
set -e

export FLASK_APP="vocabulary_srv:create_app(None, '/config/testconfig.py')"
export FLASK_ENV=development

echo "FLASK_APP=$FLASK_APP"
echo "Initializing DB..."
flask init-db
echo "Launching application..."
flask run
