#!/usr/bin/env bash

set -x
set -e


#echo "Initializing DB..."
#flask init-db
echo "Launching application..."
#flask run

gunicorn -w 4 -b 127.0.0.1:$PORT "vocabulary_srv:create_app(None, '/config/config.py')"
