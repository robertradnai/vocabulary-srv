FROM python:3.8

ARG COMMIT_HASH=main

RUN pip install gunicorn

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Installing vocabulary_srv from Github (and not from the local project folder)
RUN pip install git+https://github.com/robertradnai/vocabulary-srv.git@$COMMIT_HASH#egg=vocabulary_srv

# Copying starter scripts
COPY scripts/run_clean_db_docker.sh /starter_scripts/run_clean_db.sh

CMD ["bash", "/starter_scripts/run_clean_db.sh"]
