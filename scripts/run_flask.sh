cd "$(dirname "$0")" || exit
cd ..
export FLASK_APP=vocabulary_srv
export FLASK_ENV=development
flask run