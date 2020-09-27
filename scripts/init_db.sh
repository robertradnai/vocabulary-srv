cd "$(dirname "$0")" || exit
cd ..
export FLASK_APP=vocabulary_srv
export FLASK_ENV=development
set -x
flask init-db
flask run
