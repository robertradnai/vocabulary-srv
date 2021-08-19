set -e -x

SCRIPT_PATH=$(readlink -f "$BASH_SOURCE")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")

export FLASK_CONFIG_PATH=${SCRIPT_DIR}/testconfig.py
export FLASK_APP="vocabulary_srv:create_app(None, '${FLASK_CONFIG_PATH}')"
export FLASK_ENV=development

