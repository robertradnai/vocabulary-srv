
sudo docker run --rm -p 5000:5000 --network="host" --name vocabulary_srv \
  -v "$PROJECT_DIR"/scripts/dockerconfig.py:/config/testconfig.py \
  -v "$PROJECT_DIR"/tests/testdata/shared_collections:/config/shared_collections \
  -v "$PROJECT_DIR"/tests/testdata/shared_collections_metadata.yml:/config/shared_collections_metadata.yml \
  vocabulary-srv


# Interactive mode: add -it and at the end: /bin/bash