sudo docker run --rm --name postgres-test -d -p 5432:5432 -e POSTGRES_PASSWORD=vocabulary_test -e POSTGRES_USER=vocabulary_test postgres

# Look into the container with sudo docker exec -it postgres-test /bin/bash
# Wait half a minute between starting db Docker image and launching the app
