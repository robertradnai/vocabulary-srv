# https://python-bloggers.com/2020/10/docker-flask-dockerizing-a-python-api/


cd "$(dirname "$0")" || exit
cd ..

sudo docker build -t vocabulary-srv -f Dockerfile .
