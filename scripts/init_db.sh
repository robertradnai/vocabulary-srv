cd "$(dirname "$0")" || exit
cd ..
export FLASK_APP=vocabulary_srv
export FLASK_ENV=development
set -x
rm -r dev_instance_data
mkdir -p dev_instance_data/shared_collections
cp tests/testdata/testdict.xlsx dev_instance_data/shared_collections/testdict.xlsx
flask init-db
flask run
